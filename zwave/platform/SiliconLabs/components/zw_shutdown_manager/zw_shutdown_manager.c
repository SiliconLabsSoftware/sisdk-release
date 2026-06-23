/*******************************************************************************
 * @file zw_shutdown_manager.c
 * @brief This file contains application specific power manager IDs and abstraction
 *******************************************************************************
 * # License
 * <b> Copyright 2026 Silicon Laboratories Inc. www.silabs.com </b>
 *******************************************************************************
 *
 * The licensor of this software is Silicon Laboratories Inc. Your use of this
 * software is governed by the terms of the Silicon Labs Master Software License
 * Agreement (MSLA) available at
 * https://www.silabs.com/about-us/legal/master-software-license-agreement
 * By installing, copying or otherwise using this software, you agree to the
 * terms of the MSLA.
 *
 ******************************************************************************/

/* standard includes */
#include <assert.h>
#include <stdint.h>

/* platform includes */
#include "sl_component_catalog.h"
#include "sl_power_manager.h"
#include "sl_sleeptimer.h"
#include "sl_dcdc.h"
#include "sl_status.h"
#include "em_burtc.h"
#include "sl_clock_manager.h"
#include "sl_interrupt_manager.h"
#include "em_device.h"

/* zpal includes */
#include "system_startup.h"
#include "zpal_retention_register_private.h"
#include "zpal_misc.h"
#include "zpal_radio.h"
#include "zpal_log.h"

/* z-wave includes */
#include "zw_shutdown_manager.h"
#include "ZW_basis_api.h"

/* zaf/app includes */
#ifdef SL_CATALOG_ZW_APP_TIMER_DEEP_SLEEP_PRESENT
#include "AppTimer.h"
#endif

// protection for double initialization of the module
static bool zw_shutdown_manager_inited = false;
// used for handling timeout of temporary locks
static sl_sleeptimer_timer_handle_t em4_sleeptimer_handle;
// global counter of em4 locks
static volatile uint8_t em4_locks_counter = 0;
static bool temporary_lock_active = false;

// satisfy compiler with forward declarations
void zw_shutdown_manager_callback(sl_power_manager_em_t from, sl_power_manager_em_t to);
static void temporary_lock_revoke_callback(__attribute__((unused)) sl_sleeptimer_timer_handle_t *handle, __attribute__((unused)) void *contextData);

static zpal_status_t zw_shutdown_manager_sleeptimer_ticks_to_burtc_ticks(uint32_t sleeptimer_ticks, uint32_t *burtc_ticks)
{
  if (burtc_ticks == NULL || sleeptimer_ticks == 0U) {
    return ZPAL_STATUS_INVALID_ARGUMENT;
  }

  uint32_t sleeptimer_freq = sl_sleeptimer_get_timer_frequency();
  uint32_t burtc_freq = zpal_get_burtc_counter_frequency_hz();

  if (sleeptimer_freq == 0U || burtc_freq == 0U) {
    return ZPAL_STATUS_FAIL;
  }

  if (sleeptimer_freq == burtc_freq) {
    *burtc_ticks = sleeptimer_ticks;
    return ZPAL_STATUS_OK;
  }

  *burtc_ticks = (uint32_t)(((uint64_t)sleeptimer_ticks * (uint64_t)burtc_freq) / (uint64_t)sleeptimer_freq);
  return ZPAL_STATUS_OK;
}

/* Define the events we want to be notified about from power manager module
 * here our interest is about EM2 transition entry/leaving
 * we will hijack to EM4 if no shutdown locks are present.
 */
static sl_power_manager_em_transition_event_handle_t pm_event_handle = { 0 };
static const sl_power_manager_em_transition_event_info_t pm_event_info =
{
  .event_mask = SL_POWER_MANAGER_EVENT_TRANSITION_LEAVING_EM2
                | SL_POWER_MANAGER_EVENT_TRANSITION_ENTERING_EM2,
  .on_event = zw_shutdown_manager_callback
};

/* @brief callback function for power manager em transition event
 * @param from The power level the device is transitioning from
 * @param to The power level the device is transitioning to
 * @note em transition levels can be configured above through pm_event_info.event_mask
 */
void zw_shutdown_manager_callback(sl_power_manager_em_t from, sl_power_manager_em_t to)
{
  if (SL_POWER_MANAGER_EM2 == from) {
    // wake up from EM2
    sl_dcdc_exit_em2();
  }

  // handle sleep entry
  if (SL_POWER_MANAGER_EM2 == to) {
    if (0 != em4_locks_counter || ZPAL_RADIO_STATUS_OFF != zpal_radio_get_wakeup_status()) {
      sl_dcdc_setup_em2();
      // there are active locks, stay in EM2/EM1P
      return;
    }

    uint32_t sleeptimer_ticks_remaining = UINT32_MAX;
    if (SL_STATUS_OK != sl_sleeptimer_get_remaining_time_of_first_timer(SL_SLEEPTIMER_ANY_FLAG, &sleeptimer_ticks_remaining)) {
      sl_dcdc_setup_em2();
      // failed to acquire remaining time of platform timer
      assert(0);
      return;
    }
    if (sl_sleeptimer_ms_to_tick(1000) > sleeptimer_ticks_remaining) {
      ZPAL_LOG_DEBUG(ZPAL_LOG_SHUTDOWN_MANAGER, "Timer expiring soon: %u ticks remaining\n", sleeptimer_ticks_remaining);
      sl_dcdc_setup_em2();
      // timer expiring soon, stay in EM2/EM1P
      return;
    }

    // core shutoff completly and abort ongoing debug session, prevent em4 if in debug mode
#ifndef NDEBUG
    ZPAL_LOG_DEBUG(ZPAL_LOG_SHUTDOWN_MANAGER, "Going to EM4 (not effective in debug)\n");
    return;
#endif

    // before entering critical EM4 path, validate the tick conversion is correct
    uint32_t burtc_ticks_probe = 0U;
    if (zw_shutdown_manager_sleeptimer_ticks_to_burtc_ticks(sleeptimer_ticks_remaining, &burtc_ticks_probe) != ZPAL_STATUS_OK) {
      assert(0);
      sl_dcdc_setup_em2();
      return;
    }

    // from this point, we will be going to EM4, so shutdown the Z-Wave stack
    ZW_stack_shutdown();

#ifdef SL_CATALOG_ZW_APP_TIMER_DEEP_SLEEP_PRESENT
    // save all persistent timer data to memory
    AppTimerDeepSleepPersistentSaveAll();
#endif

    // prepare BURTC peripheral for EM4 wakeup
    CORE_DECLARE_IRQ_STATE;
    CORE_ENTER_CRITICAL();
    // get remaining time of earliest platform timer
    (void) sl_sleeptimer_get_remaining_time_of_first_timer(SL_SLEEPTIMER_ANY_FLAG, &sleeptimer_ticks_remaining);
    uint32_t counter = BURTC_CounterGet();
    uint32_t burtc_ticks_remaining = 0U;
    if (zw_shutdown_manager_sleeptimer_ticks_to_burtc_ticks(sleeptimer_ticks_remaining, &burtc_ticks_remaining) != ZPAL_STATUS_OK) {
      CORE_EXIT_CRITICAL();
      assert(0);
      sl_dcdc_setup_em2();
      return;
    }
    // set the compare value for next wakeup tick (BURTC counter domain)
    BURTC_CompareSet(0, counter + burtc_ticks_remaining);
    // enable compare and overflow interrupts
    BURTC_IntClear(BURTC_IF_COMP | BURTC_IF_OF);
    BURTC_IntEnable(BURTC_IF_COMP | BURTC_IF_OF); // enable BURTC interrupt level (already enabled at NVIC level in init function)
    CORE_EXIT_CRITICAL();

    ZPAL_LOG_DEBUG(ZPAL_LOG_SHUTDOWN_MANAGER, "Reprogrammed BURTC compare %lu BURTC ticks (sleeptimer %lu ticks, %lu ms)\n", burtc_ticks_remaining, sleeptimer_ticks_remaining, sl_sleeptimer_tick_to_ms(sleeptimer_ticks_remaining));
    ZPAL_LOG_DEBUG(ZPAL_LOG_SHUTDOWN_MANAGER, "BURTC actual count=%d\n", counter);

    // store the current BURTC count in retention register to compute sleep duration at wakeup time (system_startup_core() in system_startup.c)
    zpal_retention_register_write_private(ZPAL_RETENTION_REGISTER_PRIVATE_DEEP_SLEEP_TICK, counter);

    BURTC_Start(); // start BURTC count
    BURTC_SyncWait(); // important wait for cmd execution before entering EM4!

    sl_dcdc_setup_em4h();
    // no return from here until next wake up.
    sl_power_manager_enter_em4();
  }
}

/* @brief callback function to protect em4 entry if radio is active
 * @param state The new radio status from zpal_radio driver
 * @note this is called from zpal_radio driver on state changes.
 * @warning do not touch this implementation if you are not sure about the consequences!
 */
static void zpal_radio_status_callback(const zpal_radio_status_t state)
{
  static bool zpal_radio_shutdown_lock_state = false;
  switch (state) {
    // radio is off, release the lock
    case ZPAL_RADIO_STATUS_OFF:
      if (zpal_radio_shutdown_lock_state) {
        zw_shutdown_manager_release_lock();
        zpal_radio_shutdown_lock_state = false;
      }
      break;
    // radio is either in normal operating mode or in FLiRS mode, add a lock
    case ZPAL_RADIO_STATUS_ON:
    case ZPAL_RADIO_STATUS_FLIRS:
      if (!zpal_radio_shutdown_lock_state) {
        zw_shutdown_manager_add_lock();
        zpal_radio_shutdown_lock_state = true;
      }
      break;
    default:
      break;
  }
}

zpal_status_t zw_shutdown_manager_init(void)
{
  if (zw_shutdown_manager_inited) {
    return ZPAL_STATUS_OK;
  }

  BURTC_Init_TypeDef burtc_init_cfg = BURTC_INIT_DEFAULT;

  // Enable BURTC bus clock
  sl_status_t ret = sl_clock_manager_enable_bus_clock(SL_BUS_CLOCK_BURTC);
  if (ret != SL_STATUS_OK) {
    return ZPAL_STATUS_FAIL;
  }

  // Configure BURTC settings for EM4 wakeup operation
  burtc_init_cfg.clkDiv = 1;                           // Default frequency f=32768
  burtc_init_cfg.em4comp = true;                       // Enable compare match events for EM4 wakeup
  burtc_init_cfg.em4overflow = true;                   // Enable overflow events for EM4 wakeup
  burtc_init_cfg.compare0Top = false;                  // Reset counter to 0 on compare match for periodic timing
  burtc_init_cfg.debugRun = false;                     // Halt counter during debug to prevent interference
  burtc_init_cfg.start = false;                        // Do not start (after init) BURTC counter yet

  // Apply BURTC configuration (writes CFG and EM4WUEN registers)
  BURTC_Init(&burtc_init_cfg);
  BURTC_IntDisable(_BURTC_IEN_MASK);
  BURTC_IntClear(_BURTC_IF_MASK);

  BURTC_Start();
  BURTC_SyncWait();

  sl_interrupt_manager_clear_irq_pending(BURTC_IRQn);
  sl_interrupt_manager_enable_irq(BURTC_IRQn);

  // Initialize and register power management transition callback
  sl_power_manager_subscribe_em_transition_event(&pm_event_handle, &pm_event_info);
  (void) zpal_radio_set_status_callback(zpal_radio_status_callback);

  zw_shutdown_manager_inited = true;

  return ZPAL_STATUS_OK;
}

/* @brief add a lock to the shutdown manager
 * Increments the internal lock count, preventing the shutdown process from proceeding until all locks have been released.
 */
void zw_shutdown_manager_add_lock(void)
{
  em4_locks_counter++;
}

/* @brief release a lock from the shutdown manager
 * Decrements the internal lock count, allowing the shutdown process to proceed if no locks are present.
 */
void zw_shutdown_manager_release_lock(void)
{
  if (em4_locks_counter > 0) {
    em4_locks_counter--;
  }
}

/* @brief take a temporary lock to the shutdown manager
 * @param duration The duration (in milliseconds) for which the temporary lock should be held.
 * @note this function is used to take a temporary lock to the shutdown manager
 */
void zw_shutdown_manager_take_temporary_lock(uint32_t duration)
{
  // If a temporary lock is already active, just restart the timer and return early
  if (temporary_lock_active) {
    sl_sleeptimer_restart_timer_ms(&em4_sleeptimer_handle, duration, temporary_lock_revoke_callback, NULL, 0, 0);
    return;
  }

  // First time: acquire the lock
  zw_shutdown_manager_add_lock();
  temporary_lock_active = true;
  __attribute__((unused)) sl_status_t status = sl_sleeptimer_start_timer_ms(&em4_sleeptimer_handle, duration, temporary_lock_revoke_callback, NULL, 0, 0);
  assert(status == SL_STATUS_OK);  // Verify timer started successfully
}

/* @brief callback function to revoke a temporary lock
 * @param handle The handle of the timer that expired
 * @param contextData Additional data for the timeout handler (NULL in this case)
 * @note this function is used to revoke a temporary lock after the timeout period has elapsed
 */
static void temporary_lock_revoke_callback(__attribute__((unused)) sl_sleeptimer_timer_handle_t *handle, __attribute__((unused)) void *contextData)
{
  // Only release the lock if it's actually active to prevent double-release
  if (temporary_lock_active) {
    zw_shutdown_manager_release_lock();
    temporary_lock_active = false;
  }
}

void zw_shutdown_manager_reset(void)
{
  em4_locks_counter = 0;
  temporary_lock_active = false;
  zw_shutdown_manager_inited = false;
}
