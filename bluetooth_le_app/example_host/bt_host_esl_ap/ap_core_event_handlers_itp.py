# Copyright 2026 Silicon Laboratories Inc. www.silabs.com
#
# SPDX-License-Identifier: Zlib
#
# The licensor of this software is Silicon Laboratories Inc.
#
# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

"""
ESL AP Core - image throughput stress test event handler extensions.

Provides the image throughput stress test: iterates over synchronized ESL tags,
connecting to one tag per PAwR group at a time (since only one device per
subevent/group can be connected simultaneously). Parallel connections across
*different* groups are maintained up to the dynamic limit reported by the ESL
library.

Within each group, tags are visited sequentially. Across groups, connection
requests follow the closest-subevent-first order so that the PAwR schedule is
respected.

Each tag gets up to ``ITP_MAX_ATTEMPTS`` connection tries before being skipped.
A tag that has been successfully processed is placed on the *done* set and
will not be visited again in the same run. When every tag has been either
completed or permanently skipped, the AP reverts to its previous operating
mode.
"""

import random
import time
from collections import deque

from ap_config import ITP_MAX_ATTEMPTS, ITP_MAX_PARALLEL_CONNECTIONS
from ap_logger import getLogger, log
import esl_lib
import esl_lib_wrapper as elw
from esl_tag import ImageUpdateFailed, TagState, EslState

ITP_LOG_PREFIX = "ITP"

# OTS error statuses that trigger slot skip
_OTS_ERROR_STATUSES = (
    elw.ESL_LIB_STATUS_OTS_ERROR,
    elw.ESL_LIB_STATUS_OTS_TRANSFER_FAILED,
    elw.ESL_LIB_STATUS_OTS_GOTO_FAILED,
    elw.ESL_LIB_STATUS_OTS_UNEXPECTED_OFFSET,
    elw.ESL_LIB_STATUS_OTS_WRITE_RESP_FAILED,
)

# Connection error statuses that trigger retry
_CONN_ERROR_STATUSES = (
    elw.ESL_LIB_STATUS_CONN_FAILED,
    elw.ESL_LIB_STATUS_CONN_CLOSE_FAILED,
    elw.ESL_LIB_STATUS_CONN_TIMEOUT,
)

# Statuses that set max_conn_count_reached
_LIMIT_EXCEEDED_STATUSES = (
    elw.SL_STATUS_BT_CTRL_CONNECTION_LIMIT_EXCEEDED,
    elw.SL_STATUS_NO_MORE_RESOURCE,
    elw.SL_STATUS_BT_CTRL_COMMAND_DISALLOWED,
)


class ImageThroughputState:
    """Per-tag bookkeeping for an active image throughput session."""
    __slots__ = ("tag", "current_slot", "slots_done", "error_count", "connect_time")

    def __init__(self, tag):
        self.tag = tag
        self.current_slot = 0
        self.slots_done = 0
        self.error_count = 0
        self.connect_time = time.monotonic()


class ImageThroughputEventHandlersMixin:
    """Image throughput event handler extensions.

    Activated by the ``image_throughput`` CLI command. Uses the ``itp_`` prefix so
    that ``subscribe_event_handlers`` picks up methods named
    ``itp_esl_event_<event_name>``.
    """

    def _itp_init(self, max_tag_count=None, max_group_id=None, parallel_connections=None):
        """Initialise (or reset) image throughput bookkeeping.

        Args:
            max_tag_count: if set, at most this many synchronized tags are enrolled.
            max_group_id: if set, only tags whose ESL group id is <= this value are enrolled.
            parallel_connections: if ``None``, keep an existing ``_itp_max_conn_limit`` (or
                initialise to ``None`` on first run). If ``0``, clear to ``None`` (dynamic
                re-discovery). If 1 to ``ITP_MAX_PARALLEL_CONNECTIONS``, set a fixed
                cap on parallel BLE connections.
        """
        self._itp_log = getLogger(ITP_LOG_PREFIX)
        self._itp_max_tag_count = max_tag_count
        self._itp_max_group_id = max_group_id
        self._itp_group_queues = {}        # group_id -> deque([tag, ...])
        self._itp_initiating = set()  # tags for which connect() was called, connection_opened not yet received
        self._itp_active = {}              # tag -> ImageThroughputState (only after connection_opened)
        self._itp_done = set()        # tags successfully processed in this run
        self._itp_attempts = {}            # tag -> int (total connection attempts)
        self.next_subevent = 0
        self._itp_pawr_data_count = 1      # max concurrent requests per PAwR interval
        self._itp_total_images = 0
        self._itp_total_bytes = 0
        self._itp_xfer_in_flight = 0
        self._itp_xfer_wall_start = 0.0
        self._itp_xfer_wall_time = 0.0
        self._itp_sync_losses = 0
        self._itp_total_sync_losses = 0
        self._itp_sync_lost_tags = set(self.tag_db.list_esl_state(EslState.UNSYNCHRONIZED))
        self._itp_total_errors = 0
        self._itp_tags_done = 0
        self._itp_tags_skipped = 0
        self._itp_start_time = time.monotonic()
        self._itp_previous_cmd_mode = self.cmd_mode
        self._itp_queue_fill_slot_request_pending = False
        self._itp_image_cache = {}          # path -> bytes
        if parallel_connections is None:
            if not hasattr(self, "_itp_max_conn_limit"):
                self._itp_max_conn_limit = None  # discovered dynamically via resource errors
        elif parallel_connections == 0:
            self._itp_max_conn_limit = None
        else:
            self._itp_max_conn_limit = parallel_connections
        self._last_error = None

    # ---- transfer-time tracking -------------------------------------------

    def _itp_xfer_begin(self):
        """Signal that an OTS transfer has started."""
        if self._itp_xfer_in_flight == 0:
            self._itp_xfer_wall_start = time.monotonic()
        self._itp_xfer_in_flight += 1

    def _itp_xfer_end(self):
        """Signal that an OTS transfer has ended (success or error)."""
        self._itp_xfer_in_flight -= 1
        if self._itp_xfer_in_flight <= 0:
            self._itp_xfer_in_flight = 0
            if self._itp_xfer_wall_start > 0:
                self._itp_xfer_wall_time += time.monotonic() - self._itp_xfer_wall_start
                self._itp_xfer_wall_start = 0.0

    # ---- helpers ------------------------------------------------

    def _itp_group_id(self, tag):
        """Return the group ID for a tag, defaulting to 0."""
        return tag.group_id if tag.group_id is not None else 0

    def _itp_num_slots(self, tag):
        """Return the number of image slots for a tag."""
        if tag.max_image_index is None:
            return 0
        return tag.max_image_index + 1

    def _itp_attempt_count(self, tag):
        """Return the number of connection attempts for a tag."""
        return self._itp_attempts.get(tag, 0)

    def _itp_retries_exhausted(self, tag):
        """True if the tag has exhausted its retry budget."""
        return self._itp_attempt_count(tag) >= ITP_MAX_ATTEMPTS

    def _itp_pawr_connect_blocked(self):
        """True when the controller cannot accept a new PAwR connection request.

        Advertisement-based establishment (unsynchronized tags, mandatory ESL
        recovery, auto provisioning, etc.) monopolizes the stack until bonding
        completes. Parallel PAwR requests are allowed only while every in-flight
        connection is a synchronized PAwR request owned by this ITP run.
        """
        if (
            self.lib_connection_mode == elw.ESL_LIB_CONNECTION_MODE_SINGLE
            and not self.bonding_finished
        ):
            return True
        for tag in self.tag_db.list_state(TagState.CONNECTING):
            if tag.esl_state != EslState.SYNCHRONIZED:
                return True
            if tag not in self._itp_initiating:
                return True
        return False

    def _itp_tag_eligible_for_queue(self, tag, busy):
        """True if tag is eligible to be added to the work queue."""
        return (
            tag not in busy
            and tag not in self._itp_active
            and tag not in self._itp_initiating
            and tag not in self._itp_done
            and tag.state == TagState.IDLE
            and not tag.blocked
            and tag.has_image_transfer
            and tag.max_image_index is not None
            and not self._itp_retries_exhausted(tag)
        )

    def _itp_tag_stale(self, tag):
        """True if a queued tag should be silently discarded (state changed since enqueue)."""
        return (
            tag.esl_state != EslState.SYNCHRONIZED
            or tag.state != TagState.IDLE
            or tag.blocked
            or tag in self._itp_active
            or tag in self._itp_initiating
            or tag in self._itp_done
        )

    def _itp_advance_slot_or_finish(self, state, tag):
        """Advance to next slot and upload, or finish the tag if no more slots."""
        next_slot = state.current_slot + 1
        if next_slot < self._itp_num_slots(tag):
            state.current_slot = next_slot
            self._itp_upload_slot(tag)
        else:
            self._itp_finish_tag(tag, success=True)

    # ---- queue management ------------------------------------------------

    def _itp_request_fill_slots_async(self):
        self._itp_queue_fill_slot_request_pending = True

    def _itp_build_queue(self):
        """Build per-group work queues from synchronized, idle tags.

        Tags already in ``_itp_done`` (successfully processed in this run),
        tags that have exhausted their retry budget, and tags with an active
        session are excluded."""
        synced = self.tag_db.list_esl_state(EslState.SYNCHRONIZED)
        busy = set(self.tag_db.list_state((TagState.CONNECTED, TagState.CONNECTING)))
        eligible_tags = []
        # Order by ESL id, then group id: enroll one logical index across all groups
        # before the next (better overlap across PAwR subevents / one connection per group).
        for t in sorted(
            synced,
            key=lambda x: (
                x.esl_id if x.esl_id is not None else 0,
                self._itp_group_id(x),
            ),
        ):
            if self._itp_max_group_id is not None:
                if self._itp_group_id(t) > self._itp_max_group_id:
                    continue
            if self._itp_tag_eligible_for_queue(t, busy):
                eligible_tags.append(t)
                if (
                    self._itp_max_tag_count is not None
                    and len(eligible_tags) >= self._itp_max_tag_count
                ):
                    break
        group_queues = {}
        for t in eligible_tags:
            gid = self._itp_group_id(t)
            group_queues.setdefault(gid, deque()).append(t)
        self._itp_group_queues = group_queues
        self._itp_log.info(
            "Work queue rebuilt: %d tag(s) in %d group(s), starting near subevent %d",
            sum(len(q) for q in group_queues.values()),
            len(group_queues),
            self.next_subevent,
        )

    def _itp_fill_slots(self, count=None):
        """Initiate one connection per available group, up to system limit.

        A group is busy only if it has a connection initiation in progress (not
        if it already has an active connection). Groups are visited in
        closest-subevent-first order. The number of new connection requests
        per call is capped at ``_itp_pawr_data_count`` to avoid synchronisation
        loss on remote devices."""
        if self._itp_pawr_connect_blocked():
            self._itp_log.debug(
                "Deferring PAwR connection requests: foreign connection establishment in progress.",
            )
            self._itp_request_fill_slots_async()
            return
        busy_groups = {self._itp_group_id(t) for t in self._itp_initiating}
        ns = self.next_subevent
        sc = self.subevent_count

        available = sorted(
            (gid for gid in self._itp_group_queues
             if gid not in busy_groups and self._itp_group_queues[gid]),
            key=lambda gid: (gid - ns) % sc,
        )

        if count is None:
            count = self._itp_pawr_data_count

        initiated = 0
        for gid in available:
            # Check for both hard and dynamic connection limits
            total_busy = len(self._itp_active)

            if self.max_conn_count_reached or (self._itp_max_conn_limit is not None and total_busy >= self._itp_max_conn_limit):
                self._itp_log.debug(
                    "Connection limit reached (%d active, %d initiating, limit: %s).",
                    len(self._itp_active),
                    len(self._itp_initiating),
                    str(self._itp_max_conn_limit) if self._itp_max_conn_limit else "unknown"
                )
                break
            if initiated >= count:
                self._itp_log.debug(
                    "PAwR subevent window full (%d/%d), deferring remaining requests.",
                    initiated,
                    self._itp_pawr_data_count,
                )
                break
            tag = self._itp_pop_eligible(gid)
            if tag is None:
                continue
            state = ImageThroughputState(tag)
            self._itp_active[tag] = state
            self._itp_initiating.add(tag)
            self._itp_attempts[tag] = self._itp_attempt_count(tag) + 1
            self._itp_log.info(
                "Connecting to ESL ID %d (group %d) at %s [%d connections, %d initiating, attempt %d/%d]",
                tag.esl_id,
                tag.group_id,
                tag.ble_address,
                len(self._itp_active),
                len(self._itp_initiating),
                self._itp_attempts[tag],
                ITP_MAX_ATTEMPTS,
            )
            self.connect(tag)
            initiated += 1

            # Check immediately if the synchronous connect() hited the stack limit
            if self.max_conn_count_reached:
                break

    def _itp_pop_eligible(self, gid):
        """Pop and return the first eligible tag from *gid*'s queue.

        Tags whose state changed since the queue was built, or that have
        exhausted their retry budget, are silently discarded."""
        queue = self._itp_group_queues.get(gid)
        while queue:
            tag = queue.popleft()
            if self._itp_retries_exhausted(tag):
                self._itp_tags_skipped += 1
                self._itp_log.warning(
                    "Skipping ESL at %s after %d failed attempt(s).",
                    tag.ble_address,
                    self._itp_attempt_count(tag),
                )
                continue
            if self._itp_tag_stale(tag):
                continue
            return tag
        return None

    def _itp_requeue(self, tag):
        """Put *tag* back at the front of its group queue for a retry."""
        if self._itp_retries_exhausted(tag):
            self._itp_tags_skipped += 1
            self._itp_log.warning(
                "Giving up on ESL at %s after %d attempt(s).",
                tag.ble_address,
                self._itp_attempt_count(tag),
            )
            if not self._itp_active and not self._itp_initiating and not any(self._itp_group_queues.values()):
                self._itp_stop()
            return
        gid = self._itp_group_id(tag)
        self._itp_group_queues.setdefault(gid, deque()).appendleft(tag)

    def _itp_remove_from_queues(self, tag):
        """Remove *tag* from any work queue it might be in."""
        gid = self._itp_group_id(tag)
        queue = self._itp_group_queues.get(gid)
        if queue:
            try:
                queue.remove(tag)
                return True
            except ValueError:
                pass
        return False

    # ---- per-tag operations ----------------------------------------------

    def _itp_start_upload(self, tag):
        """Begin uploading to slot 0 of *tag*."""
        state = self._itp_active.get(tag)
        if state is None:
            return

        if not self.image_files:
            self._itp_log.warning("No image files available for ITP test, disconnecting.")
            self._itp_finish_tag(tag)
            return
        if self._itp_num_slots(tag) < 1:
            self._itp_log.warning("No image slots discovered for ESL at %s (max_image_index is None), disconnecting.", tag.ble_address)
            self._itp_finish_tag(tag)
            return

        state.current_slot = 0
        self._itp_upload_slot(tag)

    def _itp_upload_slot(self, tag):
        """Upload a random image to the current slot of *tag*."""
        state = self._itp_active.get(tag)
        if state is None:
            return
        image_name = random.choice(self.image_files)
        image_path = self.image_path + image_name

        # Cache the image data to avoid repeated disk I/O
        if image_path not in self._itp_image_cache:
            try:
                with open(image_path, "rb") as f:
                    self._itp_image_cache[image_path] = f.read()
            except Exception as e:
                self._itp_log.error("Failed to read image %s: %s", image_path, e)
                self._itp_finish_tag(tag, success=False)
                return

        image_data = self._itp_image_cache[image_path]

        self._itp_log.debug(
            "Uploading image to slot %d/%d of ESL at %s",
            state.current_slot,
            tag.max_image_index,
            tag.ble_address,
        )
        # Pass the cached byte data instead of the file path
        try:
            self.ap_imageupdate(state.current_slot, image_data, address=tag.ble_address)
        except ImageUpdateFailed as e:
            self.log.error(e)
            self._itp_finish_tag(tag, success=False)
        else:
            self._itp_xfer_begin()

    def _itp_finish_tag(self, tag, success=True):
        """Gracefully finish a tag session and initiate disconnection.

        On *success* the ESL-spec-compliant Update Complete opcode is sent
        first so that the tag transitions back to Synchronized state before
        the connection is closed by the library. On failure a raw disconnect
        is issued instead and the tag is re-queued for another attempt
        (subject to the retry budget)."""
        state = self._itp_active.pop(tag, None)
        if state is not None:
            tag_elapsed = time.monotonic() - state.connect_time
            self._itp_log.debug(
                "%s ESL at %s: %d slot(s), %d error(s) in %.1f s [%d active]",
                "Finished" if success else "Releasing",
                tag.ble_address,
                state.slots_done,
                state.error_count,
                tag_elapsed,
                len(self._itp_active),
            )
            if success:
                self._itp_tags_done += 1
                self._itp_done.add(tag)
            else:
                self._itp_requeue(tag)
        if tag.state != TagState.CONNECTED:
            return
        if success and tag.esl_id is not None:
            self.ap_update_complete(tag.esl_id, tag.group_id)
        else:
            self.disconnect(tag)

    # ---- statistics & lifecycle ------------------------------------------

    def _itp_log_stats(self, header="Image throughput summary"):
        """Print timing and throughput statistics."""
        elapsed = time.monotonic() - self._itp_start_time
        avg = elapsed / self._itp_tags_done if self._itp_tags_done else 0.0
        kbits = (self._itp_total_bytes * 8) / 1000
        eff_throughput = kbits / elapsed if elapsed > 0 else 0.0
        xfer = self._itp_xfer_wall_time
        if self._itp_xfer_in_flight > 0 and self._itp_xfer_wall_start > 0:
            xfer += time.monotonic() - self._itp_xfer_wall_start
        peak_throughput = kbits / xfer if xfer > 0 else 0.0
        log(f"{header} (elapsed: {elapsed:.3f} s)", _half_indent_log=True)
        log(f"Tags completed : {self._itp_tags_done}")
        log(f"Tags skipped   : {self._itp_tags_skipped}")
        log(f"Images sent    : {self._itp_total_images}")
        log(f"Data sent      : {self._itp_total_bytes / 1024:.1f} kB")
        log(f"Transfer time  : {xfer:.3f} s of all elapsed")
        log(f"Errors         : {self._itp_total_errors}")
        log(f"Sync losses    : {self._itp_sync_losses} / {self._itp_total_sync_losses}")
        log(f"Avg. per tag   : {avg:.3f} s")
        log(f"Eff. throughput: {eff_throughput:.2f} kbit/s")
        log(f"Peak throughput: {peak_throughput:.2f} kbit/s")

    def _itp_has_eligible_tags(self):
        """True if there is at least one tag in the queues that is not stale."""
        for gid, queue in self._itp_group_queues.items():
            for tag in queue:
                if not self._itp_tag_stale(tag) and not self._itp_retries_exhausted(tag):
                    return True
        return False

    def _itp_stop(self):
        """Stop the image throughput test and revert to the previous operating mode."""
        self.image_throughput_test = False
        self.cmd_mode = self._itp_previous_cmd_mode
        self.set_mode_handlers()
        self._itp_log.info("Reverted to %s mode.", "manual" if self.cmd_mode else "automated")
        self._itp_log_stats("Image throughput test finished")

    # ------------------------------------------------------------------
    # Event handlers (itp_ prefix)
    # ------------------------------------------------------------------

    def itp_esl_event_pawr_status(self, evt: esl_lib.EventPawrStatus):
        """Cancel throuput test if sync is stopped"""
        if evt.status not in (elw.ESL_LIB_PAWR_STATE_RUNNING, elw.ESL_LIB_PAWR_STATE_RUNNING_ADVERTISING):
            self._itp_stop()

    def itp_esl_event_pawr_data_request(self, evt: esl_lib.EventPawrDataRequest):
        """Update the per-interval connection request cap and fill slots if pending."""
        if self.max_conn_count_reached or self._last_error == elw.SL_STATUS_BT_CTRL_COMMAND_DISALLOWED:
            return
        self._itp_pawr_data_count = evt.subevent_data_count
        if self._itp_queue_fill_slot_request_pending:
            # Use system-wide busy count to decide fill amount
            total_busy = len(self.tag_db.list_state((TagState.CONNECTED, TagState.CONNECTING)))
            fill_count = None if self._itp_max_conn_limit is None else max(0, self._itp_max_conn_limit - total_busy)

            self._itp_fill_slots(fill_count)
            # Keep the request pending if we still have tags to process and haven't hit the stack limit
            self._itp_queue_fill_slot_request_pending = any(self._itp_group_queues.values()) and not self.max_conn_count_reached

    def itp_esl_event_bonding_finished(self, evt:esl_lib.EventBondingFinished):
        tag = self.tag_db.find(evt.address)
        if tag is not None and tag in self._itp_initiating:
            self._itp_initiating.discard(tag)
            self._last_error = None # // safe to clear last error here
        if (
            not self.max_conn_count_reached
            and any(self._itp_group_queues.values())
        ):
            self._itp_request_fill_slots_async()

    def itp_esl_event_connection_opened(self, evt: esl_lib.EventConnectionOpened):
        """Move tag from initiating to active and start upload, or requeue on failure."""
        tag = self.tag_db.find(evt.address)
        if tag is None:
            return
        elif tag in self._itp_active:
            if self._itp_num_slots(tag):  # advertisement based connections have to wait for tag info
                self._itp_start_upload(tag)
        elif self._itp_sync_lost_tags:
            # Irrelevant for ITP test, but must be synced according to ESLP spec
            self.past(tag)
        else:
            self.disconnect(tag)

    def itp_esl_event_tag_info(self, evt: esl_lib.EventTagInfo):
        tag = self.tag_db.find(evt.connection_handle)
        if tag is not None and tag in self._itp_active:
            self._itp_start_upload(tag)

    def itp_esl_event_tag_found(self, evt: esl_lib.EventTagFound):
        """Re-sync tags which lost sync during the procedure"""
        if self.max_conn_count_reached or self._last_error == elw.SL_STATUS_BT_CTRL_COMMAND_DISALLOWED:
            return # // can't really do anything useful at the moment until there's enough resource...
        tag = self.tag_db.find(evt.address)
        if (
            self.pawr_active
            and tag is not None
            and tag.esl_state == EslState.UNSYNCHRONIZED
            and tag.state == TagState.IDLE
        ):
            # Is this tag part of the current ITP run?
            is_active = tag in self._itp_active
            is_queued = any(tag in q for q in self._itp_group_queues.values())

            if is_active or is_queued:
                self._itp_log.warning("Recovery connection for relevant tag %s", tag.ble_address)
                if is_queued:
                    # Move from queue to active state immediately
                    self._itp_remove_from_queues(tag)
                    state = ImageThroughputState(tag)
                    self._itp_active[tag] = state
                    self._itp_attempts[tag] = self._itp_attempt_count(tag) + 1

                if tag not in self._itp_sync_lost_tags:
                    self._itp_sync_losses += 1
                # Treat this as a normal initiation so group slots are respected
                self._itp_initiating.add(tag)
                self.connect(tag)
            elif tag.provisioned:
                # Irrelevant but known: Connect, PAST will follow, then library closes.
                self._itp_log.debug("Recovery connection for irrelevant tag %s", tag.ble_address)
                self.connect(tag)
            if tag.provisioned and tag not in self._itp_sync_lost_tags:
                self._itp_total_sync_losses += 1
                self._itp_sync_lost_tags.add(tag)

    def itp_esl_event_image_transfer_finished(
        self, evt: esl_lib.EventImageTransferFinished
    ):
        """Handle image transfer result: advance to next slot or finish."""
        tag = self.tag_db.find(evt.connection_handle)
        if tag is None or tag not in self._itp_active:
            return

        self._itp_xfer_end()
        state = self._itp_active[tag]
        if evt.status == elw.SL_STATUS_OK:
            state.slots_done += 1
            self._itp_total_images += 1
            if tag.raw_image is not None:
                self._itp_total_bytes += len(tag.raw_image)
            self._itp_log.debug(
                "Slot %d done for ESL at %s (total images: %d)",
                state.current_slot,
                tag.ble_address,
                self._itp_total_images,
            )
        else:
            state.error_count += 1
            self._itp_total_errors += 1
            self._itp_log.error(
                "Image transfer to slot %d of ESL at %s failed: %s",
                state.current_slot,
                tag.ble_address,
                esl_lib.get_sl_status_str(evt.status),
            )

        self._itp_advance_slot_or_finish(state, tag)

    def itp_esl_event_connection_closed(self, evt: esl_lib.EventConnectionClosed):
        """Clear tag from active/initiating and try to fill the freed group slot."""
        tag = self.tag_db.find(evt.address)
        if tag is not None:
            self._itp_initiating.discard(tag)
            self._itp_active.pop(tag, None)
            if not tag.synchronized:
                self.log.debug("Refresh Basic State for ESL at address %s", tag.ble_address);
                self.ap_ping(tag.ble_address)
            elif tag in self._itp_sync_lost_tags:
                self._itp_sync_lost_tags.remove(tag)
        if self._itp_sync_lost_tags and self._last_error != elw.SL_STATUS_BT_CTRL_COMMAND_DISALLOWED:
            advertising_tag_to_connect = next((t for t in self._itp_sync_lost_tags if t.provisioned and t.advertising), None)
            if advertising_tag_to_connect:
                self._itp_log.warning(
                    "Attempting to recover out-of-sync Tag at %s (ESL ID %s in group %s)",
                    advertising_tag_to_connect.ble_address,
                    advertising_tag_to_connect.esl_id,
                    advertising_tag_to_connect.group_id,
                )
                self.connect(advertising_tag_to_connect)
        elif any(self._itp_group_queues.values()):
            self._itp_request_fill_slots_async()
        if not self._itp_active and not self._itp_initiating and not any(self._itp_group_queues.values()) and not self.tag_db.list_state((TagState.CONNECTED, TagState.CONNECTING)):
            self._itp_stop()

    def itp_esl_event_error(self, evt: esl_lib.EventError):
        """Handle OTS and connection errors during the image throughput test."""
        tag = self.tag_db.find(evt.node_id)
        if tag is None or (tag not in self._itp_active):
            return

        is_limit_error = evt.sl_status in _LIMIT_EXCEEDED_STATUSES
        if is_limit_error:
            # Dynamic limit discovery: how many tags were busy when the stack pushed back?
            busy_count = len(self.tag_db.list_state((TagState.CONNECTED, TagState.CONNECTING)))
            self._last_error = evt.sl_status
            if (self._itp_max_conn_limit is None or busy_count < self._itp_max_conn_limit) and self._last_error != elw.SL_STATUS_BT_CTRL_COMMAND_DISALLOWED:
                self._itp_max_conn_limit = busy_count
                self._itp_log.warning("Discovered dynamic connection limit: %d", self._itp_max_conn_limit)
        else:
            self._itp_total_errors += 1

        self._itp_initiating.discard(tag)

        if evt.lib_status in _OTS_ERROR_STATUSES:
            self._itp_handle_ots_error(tag, evt)
        elif evt.lib_status in _CONN_ERROR_STATUSES:
            self._itp_handle_conn_error(tag, evt)

    def _itp_handle_ots_error(self, tag, evt):
        """Handle an OTS error by skipping to the next slot."""
        state = self._itp_active.get(tag)
        if state is None:
            return
        self._itp_xfer_end()
        self._itp_log.warning(
            "OTS error for ESL at %s (slot %d): %s / %s - skipping to next slot",
            tag.ble_address,
            state.current_slot,
            esl_lib.get_enum("ESL_LIB_STATUS_", evt.lib_status),
            esl_lib.get_sl_status_str(evt.sl_status),
        )
        self._itp_advance_slot_or_finish(state, tag)

    def _itp_handle_conn_error(self, tag, evt):
        """Handle a connection error by re-queuing the tag for retry."""
        is_limit_error = evt.sl_status in _LIMIT_EXCEEDED_STATUSES
        self._itp_log.warning(
            "Connection error for ESL at %s: %s / %s - %s",
            tag.ble_address,
            esl_lib.get_enum("ESL_LIB_STATUS_", evt.lib_status),
            esl_lib.get_sl_status_str(evt.sl_status),
            "deferring" if is_limit_error else "will retry",
        )

        if is_limit_error:
            # Resource limit reached: don't count this as a failed attempt
            self._itp_attempts[tag] = max(0, self._itp_attempt_count(tag) - 1)

        state = self._itp_active.pop(tag, None)
        if state is not None:
            self._itp_requeue(tag)
        if tag.state == TagState.CONNECTED:
            self.disconnect(tag)

        # Don't request a fill if we just hit the resource limit
        if not is_limit_error:
            self._itp_request_fill_slots_async()
