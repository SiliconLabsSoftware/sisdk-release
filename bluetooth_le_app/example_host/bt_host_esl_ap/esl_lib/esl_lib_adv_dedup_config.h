/***************************************************************************//**
 * @file
 * @brief ESL Host Library advertisement deduplication configuration.
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * SPDX-License-Identifier: Zlib
 *
 * The licensor of this software is Silicon Laboratories Inc.
 *
 * This software is provided 'as-is', without any express or implied
 * warranty. In no event will the authors be held liable for any damages
 * arising from the use of this software.
 *
 * Permission is granted to anyone to use this software for any purpose,
 * including commercial applications, and to alter it and redistribute it
 * freely, subject to the following restrictions:
 *
 * 1. The origin of this software must not be misrepresented; you must not
 *    claim that you wrote the original software. If you use this software
 *    in a product, an acknowledgment in the product documentation would be
 *    appreciated but is not required.
 * 2. Altered source versions must be plainly marked as such, and must not be
 *    misrepresented as being the original software.
 * 3. This notice may not be removed or altered from any source distribution.
 *
 ******************************************************************************/

#ifndef ESL_LIB_ADV_DEDUP_CONFIG_H
#define ESL_LIB_ADV_DEDUP_CONFIG_H

// <<< Use Configuration Wizard in Context Menu >>>

// <h> ESL Host Library Advertisement Deduplication

// <e ESL_LIB_ADV_DEDUP_ENABLE> Enable advertisement deduplication at init
// <i> When enabled, esl_lib_init() activates the cache using the values below.
// <i> When disabled, dedup stays off until esl_lib_adv_dedup_configure() is
// <i> called with enabled = TRUE.
// <i> Default: Off
#define ESL_LIB_ADV_DEDUP_ENABLE  0

// <o ESL_LIB_ADV_DEDUP_CACHE_SIZE> Max cached advertisers <63-8191>
// <i> Oldest FIFO entry is evicted when the cache is full. Evicted tags are
// <i> reported as new on the next advertisement that exposes the ESL Service UUID.
// <i> Default: 1800
#define ESL_LIB_ADV_DEDUP_CACHE_SIZE  1800

// <o ESL_LIB_ADV_DEDUP_REFRESH_MS> tag_found event refresh [ms] <2000-180000>
// <i> While advertisements continue, a new tag_found is emitted at this interval so
// <i> the application layer can refresh its own advertising watchdog. The ESL AP
// <i> host app's ADVERTISING_TIMEOUT must be greater than or equal to this value
// <i> when the advertising deduplication feature is enabled.
// <i> Default: 45s
#define ESL_LIB_ADV_DEDUP_REFRESH_MS  45000u

// <o ESL_LIB_ADV_DEDUP_PERIOD_MULTIPLIER> Absence watchdog period multiplier <21-100>
// <i> Value is stored in tenths of the multiplier: 21 = 2.1x, 25 = 2.5x, 100 = 10.0x.
// <i> After at least three interval samples, watchdog will be updated as follows:
// <i> watchdog_ms = avg(three largest intervals) * (value / 10).
// <i> Default: 21 (2.1x)
#define ESL_LIB_ADV_DEDUP_PERIOD_MULTIPLIER  21

// <o ESL_LIB_ADV_DEDUP_SKIPLIST_MAX_LEVEL> Skip list max level <6-13>
// <i> Skip list height for O(log2 N) advertiser lookup. 11 supports well over
// <i> the default N = ESL_LIB_ADV_DEDUP_CACHE_SIZE of 1800 entries, but needs
// <i> to be adjusted if a larger (or even smaller) number of entries is needed.
// <i> Default: 11
#define ESL_LIB_ADV_DEDUP_SKIPLIST_MAX_LEVEL  11

// <o ESL_LIB_ADV_DEDUP_INTERVAL_HISTORY_SIZE> Interval sample history size <4-16>
// <i> Rolling buffer of inter-arrival times between ESL service advertisements
// <i> per advertiser (used for adaptive watchdog; three largest values are averaged).
// <i> Default: 5
#define ESL_LIB_ADV_DEDUP_INTERVAL_HISTORY_SIZE  5

// <o ESL_LIB_ADV_DEDUP_INTERVAL_SAMPLE_MAX_MS> Max valid interval sample [ms] <1000-60000>
// <i> Gaps longer than this between ESL Service reports are treated as absence.
// <i> Default: 10s
#define ESL_LIB_ADV_DEDUP_INTERVAL_SAMPLE_MAX_MS  10000u

// <o ESL_LIB_ADV_DEDUP_SWEEP_INTERVAL> Lazy stale-entry sweep period <1-256>
// <i> Run a full cache sweep every N ESL service reports to evict advertisers
// <i> whose last_seen_ms exceeds their watchdog_ms (approximate, low overhead).
// <i> Default: 32
#define ESL_LIB_ADV_DEDUP_SWEEP_INTERVAL  32

// </e>

// </h>

// <<< end of configuration section >>>

// Runtime esl_lib_adv_dedup_configure() clamp bounds

// Lower bound for refresh_ms passed to configure().
#define ESL_LIB_ADV_DEDUP_REFRESH_MS_MIN  2000u

// Upper bound for refresh_ms passed to configure().
#define ESL_LIB_ADV_DEDUP_REFRESH_MS_MAX  180000u

// Lower bound for cache_size_max passed to configure() (CMSIS wizard minimum).
#define ESL_LIB_ADV_DEDUP_CACHE_SIZE_MIN  64u

// Upper bound for cache_size_max passed to configure() (CMSIS wizard maximum).
#define ESL_LIB_ADV_DEDUP_CACHE_SIZE_MAX  4096u

// Lower bound for compile-time period multiplier in tenths (21 = 2.1x).
#define ESL_LIB_ADV_DEDUP_PERIOD_MULTIPLIER_MIN  21

// Upper bound for compile-time period multiplier in tenths (100 = 10.0x).
#define ESL_LIB_ADV_DEDUP_PERIOD_MULTIPLIER_MAX  100

// Runtime esl_lib_adv_dedup_configure() clamp bounds for period_multiplier.
#define ESL_LIB_ADV_DEDUP_PERIOD_MULTIPLIER_F_MIN \
  ((float)ESL_LIB_ADV_DEDUP_PERIOD_MULTIPLIER_MIN / 10.0f)
#define ESL_LIB_ADV_DEDUP_PERIOD_MULTIPLIER_F_MAX \
  ((float)ESL_LIB_ADV_DEDUP_PERIOD_MULTIPLIER_MAX / 10.0f)

// Default watchdog interval for ESL tag absence detection until enough adv.
// interval samples are collected to calculate a better-fitting watchdog timeout.
#define ESL_LIB_ADV_DEDUP_DEFAULT_WATCHDOG_MS  ESL_LIB_ADV_DEDUP_REFRESH_MS

#endif // ESL_LIB_ADV_DEDUP_CONFIG_H
