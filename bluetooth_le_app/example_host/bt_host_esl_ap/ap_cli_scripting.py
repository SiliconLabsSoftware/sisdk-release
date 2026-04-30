"""
ESL AP CLI script mixin: register/unregister, wait, record, playback.
"""

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

import argparse
import io
import re
import sys
import time
import threading
import esl_lib_wrapper as elw
from esl_lib import Address, EVENT_PREFIX, EVENT_FIELDS
from ap_cli_argtypes import event_type, address_type, esl_group_id_type
from ap_cli_resolvers import (
    EventFieldResolver,
    VirtualFieldResolver,
    IfResolver,
    CaseResolver,
    VIRTUAL_PLACEHOLDERS,
    DEVICE_ID_FIELDS,
    split_conditional,
)
from ap_logger import log

def make_event_name_upper(name: str) -> str:
    return EVENT_PREFIX + name.upper()

class ScriptMixin:
    """Mixin providing script register/unregister, wait, record and playback functionality."""

    def arg_script(self):
        parser_script = self.subparsers.add_parser(
            "script",
            formatter_class=lambda prog: argparse.RawDescriptionHelpFormatter(
                prog, max_help_position=30
            ),
            description=self.do_script.__doc__,
            epilog="""
        Notes: Scripting is an experimental feature only. It also supports basic waiting with timeouts and
               optional device filtering for events, as well as custom event actions based on optional
               configuration- or status-dependent conditional execution.
               Recorded script files may also contain script commands, even recursively.
               However, it is strongly advised to avoid this, as recursive execution cannot be interrupted
               and may lead to uncontrolled behavior.""",
        )

        # create subparsers for record / run / wait
        sub = parser_script.add_subparsers(dest="subcommand", required=True)

        # subcommand: record
        p_record = sub.add_parser(
            "record",
            help="Record commands to an output file. Issue 'script record stop' to stop recording and close the file."
        )
        p_record.add_argument(
            "filename",
            help="Filename to write AP commands to. Note: the word 'stop' is reserved, can't be used as a valid file name."
        )

        # subcommand: run
        p_run = sub.add_parser(
            "run",
            help="Run commands from an input file."
        )
        p_run.add_argument(
            "filename",
            help="Filename to read AP commands from."
        )

        # subcommand: wait
        p_wait = sub.add_parser(
            "wait",
            help="Wait before running the next command. "
        )
        p_wait.add_argument(
            "seconds",
            type=int,
            help="Seconds to wait"
        )
        p_wait.add_argument(
            "event",
            nargs="?",
            type=event_type,
            help="Event name (e.g. connection_opened, ESL_LIB_EVT_TAG_FOUND)"
        )
        p_wait.add_argument(
            "address",
            nargs="?",
            type=address_type,
            help="ESL ID (0-254), BLE address, or 'all'"
        )
        p_wait.add_argument(
            "--group_id",
            "-g",
            metavar="<u7>",
            type=esl_group_id_type,
            help="ESL group ID (optional, default 0 if an address is given, None otherwise); with address 'all', wait for first event from this group"
        )

        # subcommand: registered
        p_registered = sub.add_parser(
            "registered",
            help="List or clean all currently registered actions to events."
        )
        p_registered.add_argument(
            "action",
            choices=["list", "clean"],
            help="'list' to show registrations, 'clean' to remove all of them."
        )
        p_registered.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="With 'list': show full command templates. "
                 "With 'clean': show each removed binding in detail."
        )

        # subcommand: register
        p_register = sub.add_parser(
            "register",
            help="Register a CLI command to execute automatically when an ESL event occurs. "
                 "Use {field_name} placeholders for event-derived runtime values."
        )
        p_register.add_argument(
            "event",
            type=event_type,
            help="Event name to react to (e.g. connection_opened, tag_found)",
        )
        p_register.add_argument(
            "command",
            help="CLI command to execute (e.g. ping, disconnect, led)",
        )
        p_register.add_argument(
            "params",
            nargs=argparse.REMAINDER,
            help="Command parameters; use {field_name} for event-derived values (e.g. {address}). "
                 "Virtual placeholders {ble_address}, {esl_id}, {group_id} are resolved via tag database lookup."
        )

        # subcommand: unregister
        p_unregister = sub.add_parser(
            "unregister",
            help="Remove a previously registered event-to-command binding."
        )
        p_unregister.add_argument(
            "event",
            type=event_type,
            help="Event name to unregister from"
        )

    def do_script(self, arg):
        """
        Record commands to an output file, execute them from an input file,
        or register/unregister CLI commands as automatic reactions to ESL events.
        """
        if arg.subcommand == "record":
            filename = arg.filename
            self.record_commands(filename)

        elif arg.subcommand == "run":
            filename = arg.filename
            self.playback_commands(filename)

        elif arg.subcommand == "registered":
            if arg.action == "list":
                self._script_list_registered(verbose=arg.verbose)
            else:
                self._script_clean_registered(verbose=arg.verbose)

        elif arg.subcommand == "register":
            self._script_register(arg)

        elif arg.subcommand == "unregister":
            self._script_unregister(arg)

        elif arg.subcommand == "wait":
            seconds = arg.seconds
            event_name = arg.event
            address = arg.address
            wait_group_id = arg.group_id

            device_tag = None
            if address is None:
                # no device filtering
                pass
            elif address == "all":
                # group filtering only
                wait_group_id = arg.group_id # May be None if not given, integer in range 0..127, otherwise
            else:
                # address is guaranteed valid by address_type()
                if ":" in address:
                    # arg.address is BLE address → create Address object
                    node_id = Address.from_str(address)
                else:
                    # arg.address is an ESL ID
                    esl_id = int(address)
                    group_id = arg.group_id if arg.group_id is not None else 0
                    node_id = (esl_id, group_id)

                device_tag = self.ap.tag_db.find(node_id)

                if device_tag is None:
                    self.log.error(
                        "Unknown device: %s. Device must exist in tag database (use 'list' to see known devices).",
                        address,
                    )
                    return
            self.ap_wait(
                seconds,
                event_name=event_name,
                device_tag=device_tag,
                group_id=wait_group_id if device_tag is None else device_tag.group_id,
            )

    def _get_available_commands(self):
        """Return sorted list of CLI command names (without 'do_' prefix)."""
        return sorted(
            name[3:] for name in dir(self)
            if name.startswith("do_") and callable(getattr(self, name))
            and name not in ("do_foreach_group",)
        )

    @staticmethod
    def _is_conditional(token):
        """Check if a token is a conditional placeholder {if|...} or {case|...}."""
        return (token.startswith("{") and token.endswith("}")
                and (token[1:].startswith("if|") or token[1:].startswith("case|")))

    # Matches conditional placeholders with up to two levels of brace nesting,
    # e.g. {if|f|v|{if|g|w|{x}|{y}}|z} where inner conditionals and simple
    # {name} placeholders may appear inside output values.
    _CONDITIONAL_RE = re.compile(
        r'\{((?:if|case)\|(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}'
    )
    _SIMPLE_RE = re.compile(r'\{([^}|]+)\}')

    _CONST_NAME_RE = re.compile(r'^[A-Z][A-Z0-9_\-]{2,}$')

    @classmethod
    def _extract_placeholder_fields(cls, template_str):
        """Extract event field names, virtual placeholders and comparison constants.

        Returns (simple_placeholders, compound_fields, comparison_values) where
        compound_fields are the condition field names from if|/case| expressions,
        simple_placeholders are all other {name} references (including those
        nested inside conditional output values), and comparison_values are the
        literal values used for conditional matching (e.g. ``SL_STATUS_OK``).

        Handles arbitrarily nested conditionals by recursing into output values.
        """
        simple = set()
        compound = set()
        comparisons = set()

        def _walk(text):
            for m in cls._CONDITIONAL_RE.finditer(text):
                inner = m.group(1)
                parts = split_conditional(inner)
                if len(parts) >= 2:
                    compound.add(parts[1])
                    if parts[0] == "if" and len(parts) >= 3:
                        comparisons.add(parts[2])
                    elif parts[0] == "case":
                        for i in range(2, len(parts) - 1, 2):
                            comparisons.add(parts[i])
                    for value in parts[2:]:
                        _walk(value)
            stripped = cls._CONDITIONAL_RE.sub("", text)
            for match in cls._SIMPLE_RE.findall(stripped):
                simple.add(match)

        _walk(template_str)
        return simple, compound, comparisons

    def _script_register(self, arg):
        """Validate and register a CLI command to execute on an ESL event."""
        event_name = arg.event
        cmd_name = arg.command
        params = list(arg.params)

        is_conditional_cmd = self._is_conditional(cmd_name)

        if not is_conditional_cmd and not hasattr(self, "do_" + cmd_name):
            self.log.error(
                "Unknown command '%s'. Available commands: %s",
                cmd_name,
                ", ".join(self._get_available_commands()),
            )
            return

        full_template = cmd_name + (" " + " ".join(params) if params else "")
        placeholders, compound_fields, comparisons = self._extract_placeholder_fields(full_template)

        unknown_consts = {
            v for v in comparisons
            if self._CONST_NAME_RE.match(v) and not isinstance(getattr(elw, v, None), int)
        }
        if unknown_consts:
            self.log.error(
                "Unknown constant%s %s in conditional expression. "
                "Check spelling (e.g. SL_STATUS_OK, ESL_LIB_STATUS_IDLE). "
                "Numeric values (e.g. 0) are also accepted.",
                "s" * (len(unknown_consts) != 1),
                ", ".join("'" + c + "'" for c in sorted(unknown_consts)),
            )
            return

        valid_fields = EVENT_FIELDS.get(event_name, set())
        used_virtual = placeholders & VIRTUAL_PLACEHOLDERS
        if used_virtual and not (valid_fields & DEVICE_ID_FIELDS):
            self.log.error(
                "Virtual placeholder%s %s require the event to carry a device identifier "
                "(address, connection_handle, or node_id), but event '%s' has none. "
                "Available fields: %s",
                "s" * (len(used_virtual) != 1),
                ", ".join("'{" + p + "}'" for p in sorted(used_virtual)),
                make_event_name_upper(event_name),
                ", ".join(sorted(valid_fields)) if valid_fields else "(none)",
            )
            return
        invalid_simple = placeholders - valid_fields - VIRTUAL_PLACEHOLDERS
        invalid_compound = compound_fields - valid_fields
        invalid = invalid_simple | invalid_compound
        if invalid:
            self.log.error(
                "Invalid placeholder%s %s for event '%s'. Available fields: %s. "
                "Virtual placeholders: %s",
                "s" * (len(invalid) != 1),
                ", ".join("'{" + p + "}'" for p in sorted(invalid)),
                make_event_name_upper(event_name),
                ", ".join(sorted(valid_fields)) if valid_fields else "(none)",
                ", ".join("{" + p + "}" for p in sorted(VIRTUAL_PLACEHOLDERS)),
            )
            return

        if not is_conditional_cmd:
            any_placeholder_re = re.compile(r'\{[^}]+\}')
            test_tokens = [cmd_name] + [any_placeholder_re.sub("0", t) for t in params]
            saved_stderr = sys.stderr
            try:
                sys.stderr = io.StringIO()
                _, unknown = self.command_parser.parse_known_args(test_tokens)
                if unknown:
                    self.log.error(
                        "Command '%s' does not accept argument%s: %s. "
                        "Use 'help %s' to see the expected syntax.",
                        cmd_name,
                        "s" * (len(unknown) != 1),
                        " ".join(unknown),
                        cmd_name,
                    )
                    sys.stderr = saved_stderr
                    return
            except SystemExit:
                pass
            finally:
                sys.stderr = saved_stderr

        if event_name in self._registered_commands:
            existing_cmd, existing_params, _ = self._registered_commands[event_name]
            self.log.error(
                "Event '%s' already has a registered command: '%s %s'. "
                "Unregister it first with: script unregister %s",
                make_event_name_upper(event_name),
                existing_cmd,
                " ".join(existing_params),
                event_name,
            )
            return

        def _on_event(event):
            resolved = self._substitute_placeholders(cmd_name, params, event)
            if resolved is not None and self.ap.cli_queue is not None:
                self.log.debug(
                    "Event %s triggered registered command: %s",
                    make_event_name_upper(event_name),
                    resolved,
                )
                self.ap.cli_queue.put(resolved)
            elif resolved is None:
                self.log.debug(
                    "Event %s: placeholder resolution failed for '%s %s'",
                    make_event_name_upper(event_name),
                    cmd_name,
                    " ".join(params),
                )

        self.ap.evt_dispatcher.subscribe(
            event_name, _on_event, prefix="script_cmd", protected=True
        )
        self._registered_commands[event_name] = (cmd_name, params, _on_event)
        self.log.info(
            "Registered command '%s %s' for event %s",
            cmd_name,
            " ".join(params),
            make_event_name_upper(event_name),
        )

    def _script_list_registered(self, verbose=False):
        """List all currently registered command to event bindings."""
        if not self._registered_commands:
            log("No registered event-command bindings.", _half_indent_log=True)
            return
        if verbose:
            log("Registered event-command bindings:", _half_indent_log=True)
            for event_name, (cmd_name, params, _) in sorted(self._registered_commands.items()):
                param_str = " ".join(params)
                full_cmd = ("%s %s" % (cmd_name, param_str)).strip()
                log(f"{make_event_name_upper(event_name)} -> {full_cmd}")
        else:
            log("Events with registered commands:", _half_indent_log=True)
            for event_name in sorted(self._registered_commands):
                log(f"{make_event_name_upper(event_name)}")

    def _script_unregister(self, arg):
        """Remove a previously registered event-to-command binding."""
        event_name = arg.event

        if event_name not in self._registered_commands:
            self.log.error(
                "No command is registered for event '%s'. Nothing to unregister.",
                make_event_name_upper(event_name),
            )
            return

        existing_cmd, _, callback = self._registered_commands[event_name]

        self.ap.evt_dispatcher.unsubscribe(event_name, callback, forced=True)
        del self._registered_commands[event_name]
        self.log.info(
            "Unregistered command '%s' from event %s",
            existing_cmd,
            make_event_name_upper(event_name),
        )

    def _script_clean_registered(self, verbose=False):
        """Remove all registered command bindings."""
        if not self._registered_commands:
            log("No registered event-command bindings to remove.", _half_indent_log=True)
            return
        count = len(self._registered_commands)
        log("Cleaning up registered event-command bindings:", _half_indent_log=True)
        for event_name in sorted(self._registered_commands):
            cmd_name, params, callback = self._registered_commands[event_name]
            self.ap.evt_dispatcher.unsubscribe(event_name, callback, forced=True)
            if verbose:
                param_str = " ".join(params)
                full_cmd = ("%s %s" % (cmd_name, param_str)).strip()
                log(f"Removed: {make_event_name_upper(event_name)} -> {full_cmd}")
        self._registered_commands.clear()
        log(f"Removed {count} event-command binding{'s' * (count != 1)}.")

    def _tag_from_event(self, event):
        """Resolve a Tag object from an event using whatever device identifier it carries."""
        if hasattr(event, "node_id"):
            return self.ap.tag_db.find(event.node_id)
        if hasattr(event, "address"):
            return self.ap.tag_db.find(event.address)
        if hasattr(event, "connection_handle"):
            return self.ap.tag_db.find(event.connection_handle)
        return None


    def _substitute_placeholders(self, cmd_name, template_params, event):
        """Two-phase placeholder resolution.

        Phase 1: Resolve conditional placeholders ({if|...}, {case|...}).
                 These may return multi-word strings with nested {placeholder} tokens.
        Phase 2: Resolve simple and virtual placeholders in the Phase 1 output.
        """
        full_template = cmd_name + (" " + " ".join(template_params) if template_params else "")

        conditional_re = self._CONDITIONAL_RE
        simple_re = self._SIMPLE_RE

        conditional_resolvers = [IfResolver(), CaseResolver()]
        value_resolvers = [
            VirtualFieldResolver(self._tag_from_event),
            EventFieldResolver(),
        ]

        def resolve_conditional(m):
            field = m.group(1)
            for r in conditional_resolvers:
                if r.can_resolve(field):
                    return r.resolve(field, event)
            raise AttributeError(field)

        def resolve_value(m):
            field = m.group(1)
            for r in value_resolvers:
                if r.can_resolve(field):
                    return r.resolve(field, event)
            raise AttributeError(field)

        try:
            resolved = full_template
            # Phase 1 — iteratively peel nested conditionals from outside in;
            # capped at 6 iterations to guard against pathological input.
            for _ in range(6):
                prev = resolved
                resolved = conditional_re.sub(resolve_conditional, resolved)
                if resolved == prev:
                    break
            # Phase 2 — resolve remaining simple / virtual placeholders.
            resolved = simple_re.sub(resolve_value, resolved)
        except (AttributeError, ValueError):
            return None

        return resolved


    def ap_wait(self, w_time, event_name=None, device_tag=None, group_id=None):
        """
        Wait <w_time> seconds before running the next command.
        If event_name is given, wait until that event occurs or timeout.
        If device_tag is given with event_name, only resume when the event
        originates from that device. If group_id is given (and device_tag is None),
        resume on the first event from any device in that group.

        Note: The wait blocks the CLI pipeline until the event or timeout occurs.
        However, internal system operations not handled by the command interpreter
        will proceed concurrently.
        """
        if event_name is None:
            self.log.info("Waiting " + str(w_time) + " seconds")
            time.sleep(int(w_time))
            return
        # Wait for event with optional device filter
        condition = threading.Condition()
        event_received = [False]  # list to allow closure to mutate

        def _on_event(event):
            tag = self._tag_from_event(event)
            if device_tag is not None:
                if tag is not device_tag:
                    return
            elif group_id is not None:
                if tag is None or getattr(tag, "group_id", None) != group_id:
                    return
            with condition:
                event_received[0] = True
                condition.notify()

        prefix = "script_wait_" + str(threading.get_ident())
        event_display = make_event_name_upper(event_name) if event_name else ""
        try:
            self.ap.evt_dispatcher.subscribe(event_name, _on_event, prefix=prefix)
            if device_tag is not None:
                device_desc = " from ESL ID " + str(device_tag)
            elif group_id is not None:
                device_desc = " from group " + str(group_id)
            else:
                device_desc = ""
            self.log.info(
                "Waiting up to %s s for event %s%s",
                w_time,
                event_display,
                device_desc,
            )
            with condition:
                condition.wait(timeout=float(w_time))
            if event_received[0]:
                self.log.info("Event %s received%s", event_display, device_desc)
            else:
                self.log.info("Timeout waiting for event %s%s", event_display, device_desc)
        finally:
            self.ap.evt_dispatcher.unsubscribe_prefix(prefix)

    def playback_commands(self, fname):
        """Playback commands from an input file"""
        try:
            with open(fname) as f:
                self.log.info("Executing commands from file: " + fname)
                # Remove lines starting with '#' comment character
                command_list = [
                    i for i in f.read().splitlines() if not i.startswith("#")
                ]
                for line in command_list:
                    self.onecmd(line)
        except FileNotFoundError:
            self.log.warning("File not found: " + fname)

    def record_commands(self, fname):
        """Record commands to a file"""
        if fname != "stop":
            try:
                self.log.info("Recording commands to file: " + fname)
                self.record_file = open(fname, "w")
            except OSError:
                self.log.warning("Cannot open file: " + fname)
        else:
            if self.record_file:
                self.log.info("Recording of commands stopped")
                self.record_file.close()
                self.record_file = None
            else:
                self.log.info("There's no recording to stop!")
