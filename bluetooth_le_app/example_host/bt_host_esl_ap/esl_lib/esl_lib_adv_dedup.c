/***************************************************************************//**
 * @file
 * @brief ESL Host Library advertisement deduplication cache implementation.
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

#include <inttypes.h>
#include <string.h>
#include "esl_lib_adv_dedup.h"
#include "esl_lib_adv_dedup_config.h"
#include "skip_list.h"
#include "esl_lib_memory.h"
#include "esl_lib_log.h"

#ifdef _WIN32
#include <windows.h>
#else
#include <time.h>
#endif

// -----------------------------------------------------------------------------
// Local types

typedef struct esl_lib_adv_dedup_entry_s {
  struct esl_lib_adv_dedup_entry_s *fifo_prev;
  struct esl_lib_adv_dedup_entry_s *fifo_next;
  uint64_t                          last_seen_ms;
  uint64_t                          last_notified_ms;
  esl_lib_address_t                 address;
  uint32_t                          watchdog_ms;
  uint32_t                          intervals[ESL_LIB_ADV_DEDUP_INTERVAL_HISTORY_SIZE];
  int8_t                            last_rssi;
  uint8_t                           interval_count;
  uint8_t                           interval_write_index;
} esl_lib_adv_dedup_entry_t;

typedef struct {
  skip_list_p                list;
  esl_lib_adv_dedup_entry_t  *fifo_head;
  esl_lib_adv_dedup_entry_t  *fifo_tail;
  uint32_t                   sweep_counter;
  esl_lib_adv_dedup_config_t config;
} esl_lib_adv_dedup_cache_t;

// -----------------------------------------------------------------------------
// Local variables

static esl_lib_adv_dedup_cache_t adv_dedup_cache;

// -----------------------------------------------------------------------------
// Active-state check helper
static bool adv_dedup_cache_active(void)
{
  return adv_dedup_cache.config.enabled == ESL_LIB_TRUE
         && adv_dedup_cache.list != NULL;
}

// -----------------------------------------------------------------------------
// Monotonic millisecond clock for lazy expiry checks.
static uint64_t adv_dedup_now_ms(void)
{
#ifdef _WIN32
  return (uint64_t)GetTickCount64();
#else
  struct timespec ts;

  (void)clock_gettime(CLOCK_MONOTONIC, &ts);
  return ((uint64_t)ts.tv_sec * 1000u) + ((uint64_t)ts.tv_nsec / 1000000u);
#endif
}

// -----------------------------------------------------------------------------
// Skip list key compare helper
static int adv_dedup_compare_entry(void *a, void *b)
{
  register uint64_t addr_a = ((esl_lib_adv_dedup_entry_t *)a)->address.u64;
  register uint64_t addr_b = ((esl_lib_adv_dedup_entry_t *)b)->address.u64;

  return addr_a > addr_b ? 1 : addr_a < addr_b ? -1 : 0;
}

// -----------------------------------------------------------------------------
// Configuration helpers

static void adv_dedup_set_default_config(esl_lib_adv_dedup_config_t *config)
{
  config->refresh_ms            = ESL_LIB_ADV_DEDUP_REFRESH_MS;
  config->default_watchdog_ms   = ESL_LIB_ADV_DEDUP_DEFAULT_WATCHDOG_MS;
  config->enabled               = (esl_lib_bool_t)ESL_LIB_ADV_DEDUP_ENABLE;
  config->cache_size_max        = ESL_LIB_ADV_DEDUP_CACHE_SIZE;
  config->period_multiplier =
    (float)ESL_LIB_ADV_DEDUP_PERIOD_MULTIPLIER / 10.0f;
}

static uint32_t adv_dedup_clamp_refresh_ms(uint32_t refresh_ms)
{
  if (refresh_ms < ESL_LIB_ADV_DEDUP_REFRESH_MS_MIN) {
    return ESL_LIB_ADV_DEDUP_REFRESH_MS_MIN;
  }
  if (refresh_ms > ESL_LIB_ADV_DEDUP_REFRESH_MS_MAX) {
    return ESL_LIB_ADV_DEDUP_REFRESH_MS_MAX;
  }
  return refresh_ms;
}

static float adv_dedup_clamp_multiplier(float multiplier)
{
  if (multiplier < ESL_LIB_ADV_DEDUP_PERIOD_MULTIPLIER_F_MIN) {
    return ESL_LIB_ADV_DEDUP_PERIOD_MULTIPLIER_F_MIN;
  }
  if (multiplier > ESL_LIB_ADV_DEDUP_PERIOD_MULTIPLIER_F_MAX) {
    return ESL_LIB_ADV_DEDUP_PERIOD_MULTIPLIER_F_MAX;
  }
  return multiplier;
}

// -----------------------------------------------------------------------------
// FIFO insertion order for cache eviction; independent of skip list sort

static void adv_dedup_fifo_append(esl_lib_adv_dedup_entry_t *entry)
{
  entry->fifo_prev = adv_dedup_cache.fifo_tail;
  entry->fifo_next = NULL;

  if (adv_dedup_cache.fifo_tail != NULL) {
    adv_dedup_cache.fifo_tail->fifo_next = entry;
  } else {
    adv_dedup_cache.fifo_head = entry;
  }
  adv_dedup_cache.fifo_tail = entry;
}

static void adv_dedup_fifo_remove(esl_lib_adv_dedup_entry_t *entry)
{
  if (entry->fifo_prev != NULL) {
    entry->fifo_prev->fifo_next = entry->fifo_next;
  } else {
    adv_dedup_cache.fifo_head = entry->fifo_next;
  }

  if (entry->fifo_next != NULL) {
    entry->fifo_next->fifo_prev = entry->fifo_prev;
  } else {
    adv_dedup_cache.fifo_tail = entry->fifo_prev;
  }

  entry->fifo_prev = NULL;
  entry->fifo_next = NULL;
}

// -----------------------------------------------------------------------------
// Remove from FIFO and skip list, then free entry storage.
static void adv_dedup_free_entry(esl_lib_adv_dedup_entry_t *entry)
{
  adv_dedup_fifo_remove(entry);
  (void)skip_list_remove_node(adv_dedup_cache.list, entry);
  esl_lib_memory_free(entry);
}

// -----------------------------------------------------------------------------
// Adaptive absence watchdog (ESL service intervals only)
// After three samples, use the average of the three largest stored intervals
// multiplied by period_multiplier.
static uint32_t adv_dedup_compute_watchdog_ms(const esl_lib_adv_dedup_entry_t *entry)
{
  float mult = adv_dedup_cache.config.period_multiplier;

  if (entry->interval_count < 3) {
    return adv_dedup_cache.config.default_watchdog_ms;
  }

  uint32_t top[3] = { 0, 0, 0 };

  for (uint8_t i = 0; i < entry->interval_count; ++i) {
    uint32_t value = entry->intervals[i];
    if (value >= top[0]) {
      top[2] = top[1];
      top[1] = top[0];
      top[0] = value;
    } else if (value >= top[1]) {
      top[2] = top[1];
      top[1] = value;
    } else if (value > top[2]) {
      top[2] = value;
    }
  }

  uint32_t avg = (top[0] + top[1] + top[2]) / 3u;
  uint32_t watchdog = (uint32_t)((float)avg * mult);
  uint32_t min_watchdog =
    (uint32_t)((float)avg * ESL_LIB_ADV_DEDUP_PERIOD_MULTIPLIER_F_MIN);

  if (watchdog < min_watchdog) {
    watchdog = min_watchdog;
  }

  return watchdog;
}

// -----------------------------------------------------------------------------
// Reset helper
static void adv_dedup_reset_period_state(esl_lib_adv_dedup_entry_t *entry)
{
  entry->interval_count       = 0;
  entry->interval_write_index = 0;
  entry->watchdog_ms          = adv_dedup_cache.config.default_watchdog_ms;
}

// -----------------------------------------------------------------------------
// Record inter-arrival time between ESL service reports (caller filters UUID already).
static void adv_dedup_record_interval(esl_lib_adv_dedup_entry_t *entry, uint64_t gap_ms)
{
  if (gap_ms == 0 || gap_ms > ESL_LIB_ADV_DEDUP_INTERVAL_SAMPLE_MAX_MS) {
    return;
  }

  entry->intervals[entry->interval_write_index] = (uint32_t)gap_ms;
  entry->interval_write_index = (entry->interval_write_index + 1)
                                % ESL_LIB_ADV_DEDUP_INTERVAL_HISTORY_SIZE;

  if (entry->interval_count < ESL_LIB_ADV_DEDUP_INTERVAL_HISTORY_SIZE) {
    ++entry->interval_count;
  }

  entry->watchdog_ms = adv_dedup_compute_watchdog_ms(entry);
}

// -----------------------------------------------------------------------------
// Cache lookup and entry lifecycle

static esl_lib_adv_dedup_entry_t *adv_dedup_find_entry(esl_lib_address_t address)
{
  esl_lib_adv_dedup_entry_t key;

  memset(&key, 0, sizeof(key));
  key.address = address;
  skip_node_p node = skip_list_find_node(adv_dedup_cache.list, &key);

  return node ? (esl_lib_adv_dedup_entry_t *)skip_list_get_node_data(node) : NULL;
}

// -----------------------------------------------------------------------------
// Drop oldest FIFO entry when cache is at capacity.
static void adv_dedup_evict_fifo_oldest(void)
{
  if (adv_dedup_cache.fifo_head != NULL) {
    adv_dedup_free_entry(adv_dedup_cache.fifo_head);
  }
}

// -----------------------------------------------------------------------------
// New cache entry: always results in a tag_found notification to the application.
static esl_lib_adv_dedup_entry_t *adv_dedup_create_entry(esl_lib_address_t address,
                                                         int8_t rssi,
                                                         uint64_t now_ms)
{
  if (skip_list_get_node_count(adv_dedup_cache.list) >= adv_dedup_cache.config.cache_size_max) {
    adv_dedup_evict_fifo_oldest();
  }

  esl_lib_adv_dedup_entry_t *entry = esl_lib_memory_allocate(sizeof(esl_lib_adv_dedup_entry_t));
  if (entry == NULL) {
    return NULL;
  }

  memset(entry, 0, sizeof(*entry));
  entry->address              = address;
  entry->last_rssi            = rssi;
  entry->last_seen_ms         = now_ms;
  entry->last_notified_ms     = now_ms;
  adv_dedup_reset_period_state(entry);

  skip_node_p node = skip_list_insert_node(adv_dedup_cache.list, entry);
  if (node == NULL) {
    esl_lib_memory_free(entry);
    return NULL;
  }

  if (skip_list_get_node_data(node) != entry) {
    esl_lib_memory_free(entry);
    return (esl_lib_adv_dedup_entry_t *)skip_list_get_node_data(node);
  }

  adv_dedup_fifo_append(entry);
  return entry;
}

// -----------------------------------------------------------------------------
// Lazy sweep: remove advertisers silent longer than their watchdog_ms.
static void adv_dedup_expire_stale_entries(uint64_t now_ms)
{
  esl_lib_adv_dedup_entry_t *entry = adv_dedup_cache.fifo_head;

  while (entry != NULL) {
    esl_lib_adv_dedup_entry_t *next = entry->fifo_next;
    uint64_t idle_ms = now_ms - entry->last_seen_ms;

    if (idle_ms >= entry->watchdog_ms) {
      adv_dedup_free_entry(entry);
    }
    entry = next;
  }
}

// -----------------------------------------------------------------------------
// Update last_seen / RSSI and learn advertisement period from ESL service reports.
static void adv_dedup_update_entry_seen(esl_lib_adv_dedup_entry_t *entry,
                                        int8_t rssi,
                                        uint64_t now_ms)
{
  uint64_t gap_ms = now_ms - entry->last_seen_ms;

  if (entry->last_seen_ms != 0) {
    adv_dedup_record_interval(entry, gap_ms);
  }

  entry->last_seen_ms = now_ms;
  entry->last_rssi    = rssi;
}

// -----------------------------------------------------------------------------
// Emit tag_found and restart period learning for this advertiser.
static bool adv_dedup_notify_new(esl_lib_adv_dedup_entry_t *entry, uint64_t now_ms)
{
  entry->last_notified_ms = now_ms;
  adv_dedup_reset_period_state(entry);
  return true;
}

// -----------------------------------------------------------------------------
// Decide whether a known advertiser should produce tag_found again.
static bool adv_dedup_process_existing(esl_lib_adv_dedup_entry_t *entry,
                                       int8_t rssi,
                                       uint64_t now_ms)
{
  uint64_t gap_ms = (entry->last_seen_ms != 0) ? (now_ms - entry->last_seen_ms) : 0;

  // Long gap: treat as rediscovery (same entry, new notification cycle).
  if (gap_ms >= entry->watchdog_ms) {
    adv_dedup_update_entry_seen(entry, rssi, now_ms);
    return adv_dedup_notify_new(entry, now_ms);
  }

  // Continuous advertising: periodic refresh evicts and re-inserts as new.
  if ((now_ms - entry->last_notified_ms) >= adv_dedup_cache.config.refresh_ms) {
    esl_lib_address_t saved_address = entry->address;

    adv_dedup_free_entry(entry);
    return adv_dedup_create_entry(saved_address, rssi, now_ms) != NULL;
  }

  // Suppress duplicate tag_found; still refresh last_seen for watchdog accounting.
  adv_dedup_update_entry_seen(entry, rssi, now_ms);
  return false;
}

// -----------------------------------------------------------------------------
// touch_only: update cache without emitting tag_found (connection deferral path).
static bool adv_dedup_process_report(esl_lib_address_t address, int8_t rssi, bool touch_only)
{
  if (!adv_dedup_cache_active()) {
    return !touch_only;
  }

  uint64_t now_ms = adv_dedup_now_ms();

  if (++adv_dedup_cache.sweep_counter >= ESL_LIB_ADV_DEDUP_SWEEP_INTERVAL) {
    adv_dedup_cache.sweep_counter = 0;
    adv_dedup_expire_stale_entries(now_ms);
  }

  esl_lib_adv_dedup_entry_t *entry = adv_dedup_find_entry(address);

  if (entry == NULL) {
    if (touch_only) {
      // Deferred report for an unknown address: do not seed the cache silently.
      return false;
    }
    entry = adv_dedup_create_entry(address, rssi, now_ms);
    return entry != NULL;
  }

  if (touch_only) {
    adv_dedup_update_entry_seen(entry, rssi, now_ms);
    return false;
  }

  return adv_dedup_process_existing(entry, rssi, now_ms);
}

// -----------------------------------------------------------------------------
// Public API

static void adv_dedup_reset_cache(void)
{
  if (adv_dedup_cache.list != NULL) {
    skip_list_destroy_list(adv_dedup_cache.list);
    adv_dedup_cache.list = NULL;
  }
  adv_dedup_cache.fifo_head     = NULL;
  adv_dedup_cache.fifo_tail     = NULL;
  adv_dedup_cache.sweep_counter = 0;
  adv_dedup_set_default_config(&adv_dedup_cache.config);
}

void esl_lib_adv_dedup_deinit(void)
{
  adv_dedup_reset_cache();
}

sl_status_t esl_lib_adv_dedup_configure(const esl_lib_adv_dedup_config_t *config)
{
  adv_dedup_reset_cache();

  if (config != NULL) {
    adv_dedup_cache.config = *config;
  } else {
    adv_dedup_set_default_config(&adv_dedup_cache.config);
  }

  adv_dedup_cache.config.refresh_ms =
    adv_dedup_clamp_refresh_ms(adv_dedup_cache.config.refresh_ms);
  adv_dedup_cache.config.period_multiplier =
    adv_dedup_clamp_multiplier(adv_dedup_cache.config.period_multiplier);

  if (adv_dedup_cache.config.default_watchdog_ms == 0) {
    adv_dedup_cache.config.default_watchdog_ms = adv_dedup_cache.config.refresh_ms;
  } else if (adv_dedup_cache.config.default_watchdog_ms
             < adv_dedup_cache.config.refresh_ms) {
    esl_lib_log_core_warning("The requested default watchdog time of %u ms is"
                             " below the requested refresh interval of %u ms"
                             "; raising watchdog to the refresh interval."
                             APP_LOG_NL,
                             adv_dedup_cache.config.default_watchdog_ms,
                             adv_dedup_cache.config.refresh_ms);
    adv_dedup_cache.config.default_watchdog_ms = adv_dedup_cache.config.refresh_ms;
  }

  if (adv_dedup_cache.config.cache_size_max == 0) {
    adv_dedup_cache.config.cache_size_max = ESL_LIB_ADV_DEDUP_CACHE_SIZE;
  }

  if (adv_dedup_cache.config.enabled != ESL_LIB_TRUE) {
    return SL_STATUS_OK;
  }

  adv_dedup_cache.list = skip_list_create_list(ESL_LIB_ADV_DEDUP_SKIPLIST_MAX_LEVEL,
                                               adv_dedup_compare_entry);
  if (adv_dedup_cache.list == NULL) {
    adv_dedup_cache.config.enabled = ESL_LIB_FALSE;
    return SL_STATUS_ALLOCATION_FAILED;
  }

  esl_lib_log_core_debug("Advertisement deduplication enabled for up to %u ESLs"
                         " with refresh interval of %u ms." APP_LOG_NL,
                         adv_dedup_cache.config.cache_size_max,
                         adv_dedup_cache.config.refresh_ms);

  return SL_STATUS_OK;
}

void esl_lib_adv_dedup_touch(esl_lib_address_t address, int8_t rssi)
{
  (void)adv_dedup_process_report(address, rssi, true);
}

bool esl_lib_adv_dedup_should_notify(esl_lib_address_t address, int8_t rssi)
{
  return adv_dedup_process_report(address, rssi, false);
}

void esl_lib_adv_dedup_forget_address(esl_lib_address_t address)
{
  esl_lib_adv_dedup_entry_t *entry;

  if (!adv_dedup_cache_active()) {
    return;
  }

  entry = adv_dedup_find_entry(address);
  if (entry != NULL) {
    adv_dedup_free_entry(entry);
  }
}
