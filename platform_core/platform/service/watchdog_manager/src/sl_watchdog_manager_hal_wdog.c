/***************************************************************************//**
 * @file
 * @brief Watchdog Manager HAL Implementation for WDOG peripheral
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

#include "sli_watchdog_manager_hal.h"
#include "sl_hal_wdog.h"
#include "sl_clock_manager.h"
#include "sl_core.h"
#include "sl_assert.h"
#include "sl_watchdog_manager_config.h"
#if SLI_WATCHDOG_MANAGER_USE_EM_TRANSITION_HOOK
#include "sl_power_manager.h"
#endif
/***************************************************************************//**
 * @addtogroup watchdog_manager_hal
 * @{
 ******************************************************************************/

/*******************************************************************************
 *******************************   DEFINES   ***********************************
 ******************************************************************************/

// Determine which WDOG instance to use.
// Priority: WDOG1 > WDOG0.
#if defined(WDOG_PRESENT) && (WDOG_COUNT > 1)
  #define WATCHDOG_PERIPHERAL     WDOG1
  #define WATCHDOG_BUS_CLOCK      SL_BUS_CLOCK_WDOG1
#elif defined(WDOG_PRESENT) && (WDOG_COUNT == 1)
  #define WATCHDOG_PERIPHERAL     WDOG0
  #define WATCHDOG_BUS_CLOCK      SL_BUS_CLOCK_WDOG0
#else
  #warning "No WDOG peripheral available"
#endif

/*******************************************************************************
 *****************************   LOCAL DATA   **********************************
 ******************************************************************************/

/// Flag indicating if watchdog has been initialized.
static bool hal_initialized = false;

#if SLI_WATCHDOG_MANAGER_USE_EM_TRANSITION_HOOK
/// True if we disabled WDOG when leaving EM0; re-enable only when entering EM0 if set.
static bool wdog_disabled_for_sleep = false;
#endif
/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/

/***************************************************************************//**
 * Initialize the hardware watchdog.
 ******************************************************************************/
sl_status_t sli_watchdog_manager_hal_init(uint8_t timeout_period)
{
  if (timeout_period > 15) {
    return SL_STATUS_INVALID_PARAMETER;
  }

  // Enable clock to watchdog.
  sl_clock_manager_enable_bus_clock(WATCHDOG_BUS_CLOCK);

  // Initialize WDOG structure.
  sl_hal_wdog_init_t init = SL_HAL_WDOG_INIT_DEFAULT;

  // Set timeout period.
  init.period_select = (sl_hal_wdog_period_select_t)timeout_period;

  // Debug run: counter runs during debug halt when set (from config).
#if defined(_WDOG_CFG_DEBUGRUN_MASK)
  init.debug_run = (SL_WATCHDOG_MANAGER_DEBUG_RUN != 0);
#endif

  // Block EM4 when WDOG is enabled (from config).
  init.em4_block = (SL_WATCHDOG_MANAGER_EM4_BLOCK != 0);

  // Lock configuration after init (from config).
  init.lock = (SL_WATCHDOG_MANAGER_LOCK != 0);

  // Disable reset output when set (from config).
  init.reset_disable = (SL_WATCHDOG_MANAGER_RESET_DISABLE != 0);

  // EM1/EM2/EM3 run: counter runs in sleep when set (from config).
#if defined(_WDOG_CFG_EM1RUN_MASK)
  init.em1_run = (SL_WATCHDOG_MANAGER_EM1_RUN != 0);
#endif
#if defined(_WDOG_CFG_EM2RUN_MASK)
  init.em2_run = (SL_WATCHDOG_MANAGER_EM2_RUN != 0);
#endif
#if defined(_WDOG_CFG_EM3RUN_MASK)
  init.em3_run = (SL_WATCHDOG_MANAGER_EM3_RUN != 0);
#endif

  // Disable warning interrupt.
  init.warning_time_select = SL_WDOG_WARNING_DISABLE;

  // Disable window interrupt.
  init.window_time_select = SL_WDOG_ILLEGAL_WINDOW_DISABLE;

  // Initialize watchdog.
  sl_hal_wdog_init(WATCHDOG_PERIPHERAL, &init);

  hal_initialized = true;

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * Start the hardware watchdog.
 ******************************************************************************/
sl_status_t sli_watchdog_manager_hal_start(void)
{
  if (!hal_initialized) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  // Enable watchdog.
  sl_hal_wdog_enable(WATCHDOG_PERIPHERAL);

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * Feed the hardware watchdog.
 ******************************************************************************/
sl_status_t sli_watchdog_manager_hal_feed(void)
{
  if (!hal_initialized) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  // Feed the watchdog.
  sl_hal_wdog_feed(WATCHDOG_PERIPHERAL);
  // Wait for feed operation to complete.
  sl_hal_wdog_wait_sync(WATCHDOG_PERIPHERAL);

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * Disable the hardware watchdog.
 ******************************************************************************/
sl_status_t sli_watchdog_manager_hal_disable(void)
{
  if (!hal_initialized) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  // Disable Hardware watchdog.
  sl_hal_wdog_disable(WATCHDOG_PERIPHERAL);
  // Wait for disable operation to complete.
  sl_hal_wdog_wait_ready(WATCHDOG_PERIPHERAL);

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * Enable the hardware watchdog.
 ******************************************************************************/
sl_status_t sli_watchdog_manager_hal_enable(void)
{
  if (!hal_initialized) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  // Enable Hardware watchdog.
  sl_hal_wdog_enable(WATCHDOG_PERIPHERAL);

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * Check if hardware watchdog has EM1RUN capability.
 ******************************************************************************/
bool sli_watchdog_manager_hal_has_em1run(void)
{
  return (SLI_WATCHDOG_MANAGER_HAS_EM1RUN != 0);
}

/***************************************************************************//**
 * Notify HAL of an energy mode transition (disable when leaving EM0, re-enable when entering EM0).
 * When leaving EM0: software-disable WDOG unless config EMx_RUN is set or the part has
 * EMxRUN HW (then EM behavior is handled by WDOG init, not by disable here).
 ******************************************************************************/
#if SLI_WATCHDOG_MANAGER_USE_EM_TRANSITION_HOOK
void sli_watchdog_manager_hal_on_em_transition(uint8_t from, uint8_t to)
{
  if (!hal_initialized) {
    return;
  }

  // SL_POWER_MANAGER_EM0 = 0, EM1 = 1, EM2 = 2, EM3 = 3
  if (from == SL_POWER_MANAGER_EM0) {
    // Leaving EM0: skip disable if EMx_RUN requested or HW has EMxRUN (init sets EM behavior).
    wdog_disabled_for_sleep = true;
    if (to == SL_POWER_MANAGER_EM1) {
      if ((SL_WATCHDOG_MANAGER_EM1_RUN != 0) || (SLI_WATCHDOG_MANAGER_HAS_EM1RUN != 0)) {
        wdog_disabled_for_sleep = false;
      }
    } else if (to == SL_POWER_MANAGER_EM2) {
      if ((SL_WATCHDOG_MANAGER_EM2_RUN != 0) || (SLI_WATCHDOG_MANAGER_HAS_EM2RUN != 0)) {
        wdog_disabled_for_sleep = false;
      }
    } else if (to == SL_POWER_MANAGER_EM3) {
      if ((SL_WATCHDOG_MANAGER_EM3_RUN != 0) || (SLI_WATCHDOG_MANAGER_HAS_EM3RUN != 0)) {
        wdog_disabled_for_sleep = false;
      }
    }
    if (wdog_disabled_for_sleep) {
      sl_hal_wdog_disable(WATCHDOG_PERIPHERAL);
      sl_hal_wdog_wait_ready(WATCHDOG_PERIPHERAL);
    }
  } else if (to == SL_POWER_MANAGER_EM0) {
    // Entering EM0: re-enable watchdog only if we had disabled it when leaving EM0.
    if (wdog_disabled_for_sleep) {
      sl_hal_wdog_enable(WATCHDOG_PERIPHERAL);
      wdog_disabled_for_sleep = false;
    }
  }
}
#endif
/** @} (end addtogroup watchdog_manager_hal) */
