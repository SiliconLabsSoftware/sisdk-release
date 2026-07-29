"""
ESL AP Core - advertisement deduplication mixin.
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

from ap_config import ESL_ADV_DEDUP_ENABLE
from ap_logger import log
import esl_lib_wrapper as elw

class AdvDedupMixin:
    """Runtime control of esl_lib advertisement deduplication."""

    @staticmethod
    def _adv_dedup_lib_defaults():
        return {
            "refresh_ms": elw.ESL_LIB_ADV_DEDUP_REFRESH_MS,
            "watchdog_ms": elw.ESL_LIB_ADV_DEDUP_DEFAULT_WATCHDOG_MS,
            "cache_size": elw.ESL_LIB_ADV_DEDUP_CACHE_SIZE,
            "period_multiplier": elw.ESL_LIB_ADV_DEDUP_PERIOD_MULTIPLIER / 10.0,
        }

    def _adv_dedup_reset_sticky_defaults(self):
        defaults = self._adv_dedup_lib_defaults()
        self.adv_dedup_refresh_ms = defaults["refresh_ms"]
        self.adv_dedup_watchdog_ms = defaults["watchdog_ms"]
        self.adv_dedup_cache_size = defaults["cache_size"]
        self.adv_dedup_multiplier = defaults["period_multiplier"]

    def _adv_dedup_resolve_params(
        self,
        use_defaults=False,
        refresh_ms=None,
        cache_size=None,
        watchdog_ms=None,
        period_multiplier=None,
        clamp_watchdog=True,
    ):
        if use_defaults:
            resolved = self._adv_dedup_lib_defaults()
            refresh = resolved["refresh_ms"]
            watchdog = resolved["watchdog_ms"]
            cache = resolved["cache_size"]
            multiplier = resolved["period_multiplier"]
        else:
            refresh = self.adv_dedup_refresh_ms
            watchdog = self.adv_dedup_watchdog_ms
            cache = self.adv_dedup_cache_size
            multiplier = self.adv_dedup_multiplier

        if refresh_ms is not None:
            refresh = refresh_ms
        if cache_size is not None:
            cache = cache_size
        if watchdog_ms is not None:
            watchdog = watchdog_ms
        if period_multiplier is not None:
            multiplier = period_multiplier

        if clamp_watchdog and watchdog < refresh:
            watchdog = refresh

        return refresh, watchdog, cache, multiplier

    def _init_adv_dedup_state(self):
        """Initialize sticky dedup parameters before the ESL lib process starts."""
        self.adv_dedup_enabled = ESL_ADV_DEDUP_ENABLE
        self._adv_dedup_reset_sticky_defaults()

    def _adv_dedup_status_text(self):
        return (
            f"Advertisement deduplication is currently "
            f"{'enabled' if self.adv_dedup_enabled else 'disabled'}.\n"
            f"  refresh: {self.adv_dedup_refresh_ms // 1000}s\n"
            f"  watchdog: {self.adv_dedup_watchdog_ms // 1000}s\n"
            f"  cache: {self.adv_dedup_cache_size}\n"
            f"  multiplier: {self.adv_dedup_multiplier:.1f}x"
        )

    def _adv_dedup_apply(self):
        # esl_lib_adv_dedup_configure() always resets the C-side advertiser cache.
        status = self.lib.adv_dedup_configure(
            self.adv_dedup_enabled,
            self.adv_dedup_refresh_ms,
            self.adv_dedup_watchdog_ms,
            self.adv_dedup_cache_size,
            self.adv_dedup_multiplier,
        )
        if status is None:
            return False
        if status != elw.SL_STATUS_OK:
            self.log.error(
                "Advertisement deduplication configure failed: 0x%04x", status
            )
            return False

        if self.adv_dedup_enabled:
            self.log.info(
                "Advertisement deduplication enabled (refresh %ds, cache %d)",
                self.adv_dedup_refresh_ms // 1000,
                self.adv_dedup_cache_size,
            )
        else:
            self.log.info("Advertisement deduplication disabled.")
        return True

    def ap_adv_dedup(
        self,
        choice=None,
        refresh_ms=None,
        cache_size=None,
        watchdog_ms=None,
        period_multiplier=None,
        use_defaults=False,
    ):
        """
        Enable, disable or reconfigure advertisement deduplication.

        choice:
            True  - enable with sticky / updated parameters
            False - disable while keeping sticky parameters
            None  - query status, or update parameters only (config)
        use_defaults:
            Reset sticky parameters to esl_lib compile-time defaults before
            applying any explicit optional values.
        """
        params_given = use_defaults or any(
            v is not None
            for v in (refresh_ms, cache_size, watchdog_ms, period_multiplier)
        )

        if use_defaults:
            self._adv_dedup_reset_sticky_defaults()

        if refresh_ms is not None:
            self.adv_dedup_refresh_ms = refresh_ms
        if cache_size is not None:
            self.adv_dedup_cache_size = cache_size
        if watchdog_ms is not None:
            self.adv_dedup_watchdog_ms = watchdog_ms
        if period_multiplier is not None:
            self.adv_dedup_multiplier = period_multiplier

        if self.adv_dedup_watchdog_ms < self.adv_dedup_refresh_ms:
            self.adv_dedup_watchdog_ms = self.adv_dedup_refresh_ms

        if choice is None:
            if params_given:
                if self.adv_dedup_enabled:
                    self._adv_dedup_apply()
                else:
                    self.log.info(
                        "Advertisement deduplication parameters updated; "
                        "they will apply on the next 'adv_dedup on'."
                    )
            else:
                log(self._adv_dedup_status_text())
            return

        self.adv_dedup_enabled = choice
        self._adv_dedup_apply()
