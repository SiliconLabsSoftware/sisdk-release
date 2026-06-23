/***************************************************************************//**
 * @file
 * @brief LED Boost DCDC example functions
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * The licensor of this software is Silicon Laboratories Inc. Your use of this
 * software is governed by the terms of Silicon Labs Master Software License
 * Agreement (MSLA) available at
 * www.silabs.com/about-us/legal/master-software-license-agreement. This
 * software is distributed to you in Source Code format and is governed by the
 * sections of the MSLA applicable to Source Code.
 *
 ******************************************************************************/

#include "ledboost.h"
#include "em_device.h"
#include "sl_clock_manager.h"
#include "sl_hal_emu.h"
#include "sl_power_manager.h"
#include "sl_sleeptimer.h"
#include "sl_status.h"
 
#if defined(SL_HAL_EMU_DCDC_BOOST_PRESENT) && defined(_DCDC_DVDDBBCFG_MASK)
 
/*******************************************************************************
 ***************************   LOCAL DEFINES   *********************************
 ******************************************************************************/
// Busy-wait limit for the LEDVDDRAMPDONE IRQ flag.
#define LEDBOOST_WAIT_LIMIT          2000000U
// LEDVDD settle delay.
#define LEDBOOST_SETTLE_LONG_CYCLES  20000000U
// EM2 duration (ms).
#define LEDBOOST_EM2_MS              5000U
// Delay between actions (ms).
#define LEDBOOST_DEBOUNCE_MS         2000U

/*******************************************************************************
 ***************************  LOCAL VARIABLES   ********************************
 ******************************************************************************/
 
// EM transition tracking.
static sl_power_manager_em_transition_event_handle_t em_event_handle;
static volatile uint32_t em2_entry_count;
static bool em_event_subscribed = false;
 
/*******************************************************************************
 *********************   LOCAL FUNCTION PROTOTYPES   ***************************
 ******************************************************************************/
 
static bool ledboost_wait_if(uint32_t mask, uint32_t want);
static void ledboost_run_ramp_to_3v8(void);
static void ledboost_park_at_1v8_in_em2(void);
static void ledboost_low_power_sleep(uint32_t timeout_ms);
static void ledboost_busy_delay_ms(uint32_t ms);
 
/*******************************************************************************
 ***************************   LOCAL FUNCTIONS   *******************************
 ******************************************************************************/

/***************************************************************************//**
 * Ledboost delay in milliseconds.
 ******************************************************************************/
 static void ledboost_busy_delay_ms(uint32_t ms)
 {
   for (volatile uint32_t i = 0U; i < ms * 6000U; i++) {
   }
 }

/***************************************************************************//**
 * Wait for a DCDC IF flag to assert.
 ******************************************************************************/
static bool ledboost_wait_if(uint32_t mask, uint32_t want)
{
  bool ok = false;

  for (volatile uint32_t i = 0U; i < LEDBOOST_SETTLE_LONG_CYCLES; i++) {
  }

  sl_hal_emu_dcdc_enable_interrupts(mask);
  NVIC_EnableIRQ(DCDC_IRQn);

  for (uint32_t n = 0U; n < LEDBOOST_WAIT_LIMIT; n++) {
    if ((sl_hal_emu_dcdc_get_pending_interrupts() & mask) == want) {
      sl_hal_emu_dcdc_clear_pending_interrupts(mask);
      ok = true;
      break;
    }
  }

  sl_hal_emu_dcdc_disable_interrupts((uint32_t)_DCDC_IEN_MASK);
  NVIC_DisableIRQ(DCDC_IRQn);
  NVIC_ClearPendingIRQ(DCDC_IRQn);

  return ok;
}

/***************************************************************************//**
 * Ramp LEDVDD 1.8 V -> 3.8 V, then power off DCDC. Runs in EM0.
 ******************************************************************************/
static void ledboost_run_ramp_to_3v8(void)
{
  sl_clock_manager_enable_bus_clock(SL_BUS_CLOCK_DCDC);

  sl_hal_emu_dcdc_clear_pending_interrupts((uint32_t)_DCDC_IF_MASK);
  sl_hal_emu_dcdc_disable_interrupts((uint32_t)_DCDC_IEN_MASK);
  NVIC_DisableIRQ(DCDC_IRQn);
  NVIC_ClearPendingIRQ(DCDC_IRQn);

  sl_hal_emu_dcdc_set_regulation_type(SL_HAL_EMU_DCDC_REGULATION_TYPE_REGDVDDDEC);

  sl_hal_emu_dcdc_boost_init_t boost_cfg = SL_HAL_EMU_DCDC_BOOST_INIT_DEFAULT;
  sl_hal_emu_init_dcdc_boost(&boost_cfg);

  sl_hal_emu_dcdc_clear_pending_interrupts(DCDC_IF_LEDVDDRAMPDONE
                                          | DCDC_IF_BOOSTPOSEDG);
  sl_hal_emu_dcdc_sync(_DCDC_SYNCBUSY_MASK);
  sl_hal_emu_set_dcdc_boost_output_voltage(SL_HAL_EMU_DCDC_BOOST_OUTPUT_VOLTAGE_1V8);
  (void)ledboost_wait_if(DCDC_IF_LEDVDDRAMPDONE, DCDC_IF_LEDVDDRAMPDONE);

  sl_hal_emu_dcdc_clear_pending_interrupts(DCDC_IF_LEDVDDRAMPDONE
                                          | DCDC_IF_BOOSTPOSEDG);
  sl_hal_emu_dcdc_sync(_DCDC_SYNCBUSY_MASK);
  sl_hal_emu_set_dcdc_boost_output_voltage(SL_HAL_EMU_DCDC_BOOST_OUTPUT_VOLTAGE_3V8);
  (void)ledboost_wait_if(DCDC_IF_LEDVDDRAMPDONE, DCDC_IF_LEDVDDRAMPDONE);

  sl_hal_emu_dcdc_power_off();

  sl_clock_manager_disable_bus_clock(SL_BUS_CLOCK_DCDC);
}
 
/***************************************************************************//**
 * EM transition callback. Counts EM2 entries.
 ******************************************************************************/
static void ledboost_on_em_transition(sl_power_manager_em_t from,
                                      sl_power_manager_em_t to)
{
  (void)from;
  if (to == SL_POWER_MANAGER_EM2) {
    em2_entry_count++;
  }
}

static const sl_power_manager_em_transition_event_info_t em_event_info = {
  .event_mask = SL_POWER_MANAGER_EVENT_TRANSITION_ENTERING_EM2,
  .on_event   = ledboost_on_em_transition,
};
 
/***************************************************************************//**
 * Sleeptimer wake callback.
 ******************************************************************************/
static void ledboost_wake_cb(sl_sleeptimer_timer_handle_t *handle,
                                  void *data)
{
  (void)handle;
  *(volatile bool *)data = true;
}
 
/***************************************************************************//**
 * Enter EM2 for `timeout_ms`, wake via sleeptimer.
 ******************************************************************************/
static void ledboost_low_power_sleep(uint32_t timeout_ms)
{
  sl_sleeptimer_timer_handle_t wake_timer;
  volatile bool wake_received = false;

#if defined(EMU_CTRL_EM2DBGEN)
  EMU->CTRL_SET = EMU_CTRL_EM2DBGEN;
#endif

  if (!em_event_subscribed) {
    sl_power_manager_subscribe_em_transition_event(&em_event_handle,
                                                  &em_event_info);
    em_event_subscribed = true;
  }
  em2_entry_count = 0U;

  sl_hal_emu_dcdc_disable_interrupts((uint32_t)_DCDC_IEN_MASK);
  NVIC_DisableIRQ(DCDC_IRQn);
  NVIC_ClearPendingIRQ(DCDC_IRQn);

  if (sl_sleeptimer_start_timer_ms(
        &wake_timer,
        timeout_ms,
        ledboost_wake_cb,
        (void *)&wake_received,
        0,
        SL_SLEEPTIMER_NO_HIGH_PRECISION_HF_CLOCKS_REQUIRED_FLAG) != SL_STATUS_OK) {
    return;
  }

  while (!wake_received) {
    sl_power_manager_sleep();
  }

  (void)sl_sleeptimer_stop_timer(&wake_timer);
}
 
/***************************************************************************//**
 * Park LEDVDD at 1.8 V, then dwell in EM2.
 ******************************************************************************/
static void ledboost_park_at_1v8_in_em2(void)
{
  sl_clock_manager_enable_bus_clock(SL_BUS_CLOCK_DCDC);

  sl_hal_emu_dcdc_clear_pending_interrupts((uint32_t)_DCDC_IF_MASK);
  sl_hal_emu_dcdc_disable_interrupts((uint32_t)_DCDC_IEN_MASK);
  NVIC_DisableIRQ(DCDC_IRQn);
  NVIC_ClearPendingIRQ(DCDC_IRQn);

  sl_hal_emu_dcdc_set_regulation_type(SL_HAL_EMU_DCDC_REGULATION_TYPE_REGDVDDDEC);

  sl_hal_emu_dcdc_boost_init_t boost_cfg = SL_HAL_EMU_DCDC_BOOST_INIT_DEFAULT;
  sl_hal_emu_init_dcdc_boost(&boost_cfg);

  sl_hal_emu_dcdc_clear_pending_interrupts(DCDC_IF_LEDVDDRAMPDONE
                                          | DCDC_IF_BOOSTPOSEDG);
  sl_hal_emu_dcdc_sync(_DCDC_SYNCBUSY_MASK);
  sl_hal_emu_set_dcdc_boost_output_voltage(SL_HAL_EMU_DCDC_BOOST_OUTPUT_VOLTAGE_1V8);
  (void)ledboost_wait_if(DCDC_IF_LEDVDDRAMPDONE, DCDC_IF_LEDVDDRAMPDONE);

  // LEDVDD held at 1.8 V; enter EM2.
  ledboost_low_power_sleep(LEDBOOST_EM2_MS);
}
 
/***************************************************************************//**
 * DCDC IRQ Handler.
 ******************************************************************************/
void DCDC_IRQHandler(void)
{
  sl_hal_emu_dcdc_disable_interrupts((uint32_t)_DCDC_IEN_MASK);
  NVIC_DisableIRQ(DCDC_IRQn);
  NVIC_ClearPendingIRQ(DCDC_IRQn);
}
 
/*******************************************************************************
 ***************************   PUBLIC FUNCTIONS   ******************************
 ******************************************************************************/
 
/***************************************************************************//**
 * Initialize LED Boost example.
 ******************************************************************************/
void ledboost_init(void)
{
  if (!em_event_subscribed) {
    sl_power_manager_subscribe_em_transition_event(&em_event_handle,
                                                    &em_event_info);
    em_event_subscribed = true;
  }
}
 
/***************************************************************************//**
 * Alternates two actions on each iteration:
 *   - odd  count -> ramp LEDVDD 1.8 V -> 3.8 V, then power off DCDC.
 *   - even count -> park LEDVDD at 1.8 V and dwell in EM2.
 *
 * A short delay separates each action so the transitions are clearly
 * visible.
 ******************************************************************************/
void ledboost_process_action(void)
{
  uint32_t count = 0U;
  for (;;) {
    ledboost_busy_delay_ms(LEDBOOST_DEBOUNCE_MS);
    count++;
    if ((count & 1U) == 1U) {
      ledboost_run_ramp_to_3v8();    // odd:  ramp 1.8 V -> 3.8 V
    } else {
      ledboost_park_at_1v8_in_em2(); // even: park 1.8 V + EM2 dwell
    }
    ledboost_busy_delay_ms(LEDBOOST_DEBOUNCE_MS);
  }
}

#else /* !(SL_HAL_EMU_DCDC_BOOST_PRESENT && _DCDC_DVDDBBCFG_MASK) */
 
/***************************************************************************//**
 * Initialize LED Boost example (unsupported device: empty).
 ******************************************************************************/
void ledboost_init(void)
{
}
 
/***************************************************************************//**
 * LED Boost process action (unsupported device: empty).
 ******************************************************************************/
void ledboost_process_action(void)
{
}

#endif /* SL_HAL_EMU_DCDC_BOOST_PRESENT && _DCDC_DVDDBBCFG_MASK */
 