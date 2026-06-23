/***************************************************************************//**
 * @file
 * @brief Watchdog Manager Service Implementation
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

#include "sl_watchdog_manager.h"
#include "sli_watchdog_manager.h"
#include "sl_watchdog_manager_config.h"
#include "sli_watchdog_manager_hal.h"
#include "sl_assert.h"
#include "sl_common.h"
#include "sl_core.h"
#include "sl_hal_emu.h"

#include <string.h>

/***************************************************************************//**
 * @addtogroup watchdog_manager
 * @{
 ******************************************************************************/

/*******************************************************************************
 *******************************   TYPEDEFS   **********************************
 ******************************************************************************/

/// Watchdog manager internal state.
typedef struct {
  uint32_t watchdog_uids[SL_WATCHDOG_MANAGER_MAX_SW_WATCHDOGS]; ///< UID per slot (for debugging).
  uint32_t fed_mask;      ///< Bitmask of watchdogs that have been fed this period.
  uint32_t enabled_mask;  ///< Bitmask of enabled watchdogs.
  uint32_t allocated_mask; ///< Bitmask of allocated watchdogs.
  bool initialized;       ///< Whether the manager has been initialized.
  bool started;           ///< Whether the manager has been started.
} watchdog_manager_state_t;

/// No-init state for preserving data across resets.
typedef struct {
  uint32_t faulty_handle; ///< Handle of watchdog that caused reset.
  uint32_t magic;         ///< Magic number to validate data.
  bool valid;             ///< Whether the data is valid.
} watchdog_manager_noinit_state_t;

/*******************************************************************************
 *****************************   LOCAL DATA   **********************************
 ******************************************************************************/

/// Magic number to validate no-init data.
#define WATCHDOG_MANAGER_MAGIC  0x574D4752u  // "WMGR".

/// Watchdog manager state.
static watchdog_manager_state_t manager_state;

/// No-init state for reset cause tracking (preserved across resets).
#if defined(__ICCARM__)
__no_init static watchdog_manager_noinit_state_t noinit_state @ ".noinit";
#else
static watchdog_manager_noinit_state_t noinit_state SL_ATTRIBUTE_SECTION(".noinit");
#endif

/*******************************************************************************
 **************************   LOCAL FUNCTIONS   ********************************
 ******************************************************************************/

/***************************************************************************//**
 * @brief Find first available handle slot.
 *
 * @return Handle for the new watchdog (0-31), or UINT32_MAX if none available.
 ******************************************************************************/
static sl_watchdog_handle_t find_available_handle(void)
{
  for (uint32_t i = 0; i < SL_WATCHDOG_MANAGER_MAX_SW_WATCHDOGS; i++) {
    if ((manager_state.allocated_mask & (1u << i)) == 0) {
      return i;
    }
  }
  return UINT32_MAX;
}

/***************************************************************************//**
 * @brief Validate a watchdog handle.
 *
 * @param[in] handle Handle to validate (bit position 0-31).
 *
 * @return true if valid, false otherwise.
 ******************************************************************************/
static bool is_valid_handle(sl_watchdog_handle_t handle)
{
  // Check if handle is within valid range (0-31).
  if (handle >= SL_WATCHDOG_MANAGER_MAX_SW_WATCHDOGS) {
    return false;
  }

  // Check if handle is allocated.
  return (manager_state.allocated_mask & (1u << handle)) != 0;
}

/***************************************************************************//**
 * @brief Update hardware watchdog state based on enabled watchdogs.
 *
 * @details
 * Enables the hardware watchdog if any software watchdog is enabled.
 * Disables the hardware watchdog if no software watchdogs are enabled.
 ******************************************************************************/
static void update_hw_watchdog_state(void)
{
  // If any watchdog is enabled, hardware watchdog should be enabled.
  if (manager_state.enabled_mask != 0) {
    // Hardware watchdog needs to be enabled.
    sl_watchdog_manager_start();
  } else {
    // No watchdogs enabled, disable hardware watchdog to save power.
    sl_status_t status = sli_watchdog_manager_hal_disable();
    manager_state.started = false;
    (void)status; // Suppress unused variable warning.
  }
}

/***************************************************************************//**
 * @brief Check if all enabled watchdogs have been fed and feed HW watchdog.
 *
 * @note Caller must hold the atomic section (CORE_ENTER_ATOMIC).
 ******************************************************************************/
static void check_and_feed_hw_watchdog(void)
{
  // Check if any watchdogs are enabled and all of them have been fed.
  if (manager_state.enabled_mask != 0
      && (manager_state.fed_mask & manager_state.enabled_mask)
      == manager_state.enabled_mask) {
    // All enabled watchdogs fed, feed hardware watchdog.
    sli_watchdog_manager_hal_feed();

    // Reset fed mask for next period.
    manager_state.fed_mask = 0;
  } else if (manager_state.enabled_mask != 0) {
    // Record faulty watchdog for post-reset retrieval.
    sli_watchdog_manager_record_state();
  }
}

/***************************************************************************//**
 * @brief Record faulty watchdog for post-reset retrieval.
 ******************************************************************************/
static void record_faulty_watchdog(void)
{
  // Find first unfed enabled watchdog.
  uint32_t unfed_mask = manager_state.enabled_mask & ~manager_state.fed_mask;

  if (unfed_mask != 0) {
    // Find first unfed watchdog (bit position).
    for (uint32_t i = 0; i < SL_WATCHDOG_MANAGER_MAX_SW_WATCHDOGS; i++) {
      if (unfed_mask & (1u << i)) {
        noinit_state.faulty_handle = i;  // Store bit position, not bitmask.
        noinit_state.magic = WATCHDOG_MANAGER_MAGIC;
        noinit_state.valid = true;
        break;
      }
    }
  }
}

/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/

/***************************************************************************//**
 * Initialize watchdog manager.
 ******************************************************************************/
void sl_watchdog_manager_init(void)
{
  // Clear manager state.
  memset(&manager_state, 0, sizeof(manager_state));

  // Initialize HAL.
  sl_status_t status = sli_watchdog_manager_hal_init(SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD);
  EFM_ASSERT(status == SL_STATUS_OK);
  (void)status; // Suppress unused variable warning in release builds.

  manager_state.initialized = true;
}

/***************************************************************************//**
 * Start watchdog manager.
 ******************************************************************************/
void sl_watchdog_manager_start(void)
{
  EFM_ASSERT(manager_state.initialized);

  if (!manager_state.started) {
    sl_status_t status = sli_watchdog_manager_hal_start();
    EFM_ASSERT(status == SL_STATUS_OK);
    (void)status; // Suppress unused variable warning in release builds.

#if SLI_WATCHDOG_MANAGER_USE_EM_TRANSITION_HOOK
    sli_watchdog_manager_power_subscribe_em_transition();
#endif

#if defined(SL_CATALOG_MICRIUMOS_KERNEL_PRESENT)
    sli_watchdog_manager_micrium_install_task_sw_hook();
#endif

    manager_state.started = true;
  }
}

/***************************************************************************//**
 * Create a software watchdog.
 ******************************************************************************/
sl_status_t sl_watchdog_manager_create(sl_watchdog_handle_t *handle,
                                       uint32_t watchdog_uid)
{
  if (handle == NULL) {
    return SL_STATUS_NULL_POINTER;
  }

  if (!manager_state.initialized) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  CORE_DECLARE_IRQ_STATE;
  CORE_ENTER_ATOMIC();

  // Find available handle.
  sl_watchdog_handle_t new_handle = find_available_handle();
  if (new_handle == UINT32_MAX) {
    CORE_EXIT_ATOMIC();
    return SL_STATUS_NO_MORE_RESOURCE;
  }

  EFM_ASSERT(new_handle < SL_WATCHDOG_MANAGER_MAX_SW_WATCHDOGS);

  // Store UID for this slot (for debugging / reset cause).
  manager_state.watchdog_uids[new_handle] = watchdog_uid;

  // Update masks (convert handle to bitmask).
  uint32_t bit = (1u << new_handle);
  manager_state.allocated_mask |= bit;
  manager_state.enabled_mask |= bit;

  // Check if this matches a faulty watchdog from previous reset.
  if (noinit_state.valid
      && noinit_state.magic == WATCHDOG_MANAGER_MAGIC
      && noinit_state.faulty_handle == new_handle) {
    // Log that this watchdog was previously faulty.
    // In a real implementation, this would use the logging system.
    // For now, we just clear the noinit state.
    noinit_state.valid = false;
  }

  *handle = new_handle;

  CORE_EXIT_ATOMIC();

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * Delete a software watchdog.
 ******************************************************************************/
sl_status_t sl_watchdog_manager_delete(sl_watchdog_handle_t *handle)
{
  if (handle == NULL) {
    return SL_STATUS_NULL_POINTER;
  }

  if (!manager_state.initialized) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  if (!is_valid_handle(*handle)) {
    return SL_STATUS_INVALID_HANDLE;
  }

  CORE_DECLARE_IRQ_STATE;
  CORE_ENTER_ATOMIC();

  EFM_ASSERT(is_valid_handle(*handle));

  // Clear UID for this slot.
  manager_state.watchdog_uids[*handle] = 0;

  // Update masks (convert handle to bitmask).
  uint32_t bit = (1u << *handle);
  manager_state.allocated_mask &= ~bit;
  manager_state.enabled_mask &= ~bit;
  manager_state.fed_mask &= ~bit;

  // Update hardware watchdog state based on remaining enabled watchdogs.
  update_hw_watchdog_state();

  // Clear handle.
  *handle = UINT32_MAX;

  // Check if we can now feed HW watchdog.
  check_and_feed_hw_watchdog();

  CORE_EXIT_ATOMIC();

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * Feed a software watchdog.
 ******************************************************************************/
sl_status_t sl_watchdog_manager_feed(sl_watchdog_handle_t *handle)
{
  if (handle == NULL) {
    return SL_STATUS_NULL_POINTER;
  }

  if (!manager_state.initialized) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  if (!is_valid_handle(*handle)) {
    return SL_STATUS_INVALID_HANDLE;
  }

  CORE_DECLARE_IRQ_STATE;
  CORE_ENTER_ATOMIC();

  // Mark this watchdog as fed (convert handle to bitmask).
  manager_state.fed_mask |= (1u << *handle);

  // Check if all watchdogs are fed and feed HW watchdog if so.
  check_and_feed_hw_watchdog();

  CORE_EXIT_ATOMIC();

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * Disable a software watchdog.
 ******************************************************************************/
sl_status_t sl_watchdog_manager_disable(sl_watchdog_handle_t *handle)
{
  if (handle == NULL) {
    return SL_STATUS_NULL_POINTER;
  }

  if (!manager_state.initialized) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  if (!is_valid_handle(*handle)) {
    return SL_STATUS_INVALID_HANDLE;
  }

  CORE_DECLARE_IRQ_STATE;
  CORE_ENTER_ATOMIC();

  EFM_ASSERT(is_valid_handle(*handle));
  manager_state.enabled_mask &= ~(1u << *handle);

  // Update hardware watchdog state based on remaining enabled watchdogs.
  update_hw_watchdog_state();

  // Check if we can now feed HW watchdog.
  check_and_feed_hw_watchdog();

  CORE_EXIT_ATOMIC();

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * Check if a software watchdog is enabled.
 ******************************************************************************/
sl_status_t sl_watchdog_manager_is_enabled(sl_watchdog_handle_t *handle,
                                           bool *is_enabled)
{
  if (handle == NULL || is_enabled == NULL) {
    return SL_STATUS_NULL_POINTER;
  }

  if (!manager_state.initialized) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  if (!is_valid_handle(*handle)) {
    return SL_STATUS_INVALID_HANDLE;
  }

  EFM_ASSERT(is_valid_handle(*handle));
  *is_enabled = (manager_state.enabled_mask & (1u << *handle)) != 0;

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * Enable a software watchdog.
 ******************************************************************************/
sl_status_t sl_watchdog_manager_enable(sl_watchdog_handle_t *handle)
{
  if (handle == NULL) {
    return SL_STATUS_NULL_POINTER;
  }

  if (!manager_state.initialized) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  if (!is_valid_handle(*handle)) {
    return SL_STATUS_INVALID_HANDLE;
  }

  CORE_DECLARE_IRQ_STATE;
  CORE_ENTER_ATOMIC();

  EFM_ASSERT(is_valid_handle(*handle));
  manager_state.enabled_mask |= (1u << *handle);

  // Update hardware watchdog state based on enabled watchdogs.
  update_hw_watchdog_state();

  CORE_EXIT_ATOMIC();

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * Force feed hardware watchdog.
 ******************************************************************************/
sl_status_t sl_watchdog_manager_force_feed(void)
{
  if (!manager_state.initialized) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  CORE_DECLARE_IRQ_STATE;
  CORE_ENTER_ATOMIC();

  sl_status_t status = sli_watchdog_manager_hal_feed();
  // Reset fed mask since we just fed HW watchdog.
  manager_state.fed_mask = 0;

  CORE_EXIT_ATOMIC();

  return status;
}

/***************************************************************************//**
 * Retrieve faulty watchdog from previous reset.
 ******************************************************************************/
sl_status_t sl_watchdog_manager_retrieve_faulty(sl_watchdog_handle_t *handle)
{
  if (handle == NULL) {
    return SL_STATUS_NULL_POINTER;
  }

  // This must be called before init.
  if (manager_state.initialized) {
    return SL_STATUS_INVALID_STATE;
  }

  // Check if we have valid noinit data.
  if (!noinit_state.valid || noinit_state.magic != WATCHDOG_MANAGER_MAGIC) {
    return SL_STATUS_NOT_AVAILABLE;
  }

  // Check if reset was caused by watchdog.
  uint32_t reset_cause = sl_hal_emu_get_reset_cause();
  sl_hal_emu_clear_reset_cause();

  // Check for watchdog reset (bit positions may vary by device).
  // This is a simplified check - actual implementation would need
  // device-specific handling.
  bool is_watchdog_reset = false;
  #if defined(EMU_RSTCAUSE_WDOG1)
  is_watchdog_reset = (reset_cause & (EMU_RSTCAUSE_WDOG0 | EMU_RSTCAUSE_WDOG1)) != 0;
  #elif defined(EMU_RSTCAUSE_WDOG0)
  is_watchdog_reset = (reset_cause & (EMU_RSTCAUSE_WDOG0)) != 0;
  #endif
  if (!is_watchdog_reset) {
    noinit_state.valid = false;
    return SL_STATUS_NOT_AVAILABLE;
  }

  *handle = noinit_state.faulty_handle;

  // Keep noinit_state valid so we can log when the watchdog is recreated.

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * Internal function called before potential watchdog reset to record state.
 * This is called from check_and_feed_hw_watchdog() function.
 * This function is called repeatedly so only the last faulty watchdog handle is stored.
 ******************************************************************************/
void sli_watchdog_manager_record_state(void)
{
  if (manager_state.initialized && manager_state.started) {
    record_faulty_watchdog();
  }
}

/** @} (end addtogroup watchdog_manager) */
