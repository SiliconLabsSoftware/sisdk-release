/***************************************************************************//**
 * @file
 * @brief LEDSINK bare-metal example
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

#include "em_device.h"
#include "sl_hal_ledsink.h"
#include "sl_clock_manager.h"
#include "sl_device_clock.h"
#include "sl_sleeptimer.h"
#include "sl_power_manager.h"
#include "sl_simple_button_instances.h"
#include "ledsink_baremetal.h"

/*******************************************************************************
 *******************************   DEFINES   ***********************************
 ******************************************************************************/

#define LEDSINK_INST        LEDSINK0
#define NUM_CH              4U

// Mode 0 / Mode 2 clock: ULFRCO ~1 kHz.
// cycles_per_bit=500 → 1 bit-slot = 500 ms at 1 kHz.
#define PATTERN_CYCLES_PER_SEC    1000UL
#define PATTERN_CYCLES_PER_BIT    500U

// Mode 1 clock: FSRCO / 50 = 400 kHz.
// PWM frequency = 400 kHz / 16 = 25 kHz (above audible range).
// PRESC=49 → divide-by-50.
#define PWM_CLOCK_PRESC           49UL
#define PWM_CYCLES_PER_SEC        40UL
// cycles_per_bit=8 → 2 ms per bit-slot at 400 kHz.
#define PWM_CYCLES_PER_BIT        8U

// Each mode runs for 5 seconds before advancing.
#define MODE_DURATION_MS    5000U
// SW counter updates every 300 ms.
#define SW_TICK_MS          300U

#define REPEAT_COUNT        10U

// Mode 0 / Mode 2 — per-channel analog current.
// I(mA) = (step+1) × 0.5; uniform 6 mA/ch (step=11) so the unique
// (2/4/7/10 mA) made CH0 too dim to spot at 2 mA.  Total 24 mA <= 30 mA limit.
static const uint8_t ch_current[NUM_CH] = { 11U, 11U, 11U, 11U };

// Mode 0 — NON-PWM unique 8-bit patterns per channel (LSB = bit played first).
//   CH0 0x0F : 2s-ON/2s-OFF
//   CH1 0x33 : 1s-ON/1s-OFF (x2)
//   CH2 0x55 : 500 ms alternating
//   CH3 0x09 : double-flash every 4 s
static const uint32_t ch_pattern[NUM_CH]  = { 0x0FUL, 0x33UL, 0x55UL, 0x09UL };
static const uint8_t  ch_patlen[NUM_CH]   = { 8U, 8U, 8U, 8U     };

// Mode 1 — PWM all channels: pattern 0xFF (always ON); PWM duty varies brightness.
// Uniform current (step=9, 5 mA/ch, 20 mA total) so only duty differs.
// Duty N → (N+1)/16 × 100%; range 6.25% to 100% in 6.25% steps.
#define PWM_CURRENT_STEP    9U
static const uint8_t ch_duty[NUM_CH] = { 0U, 4U, 9U, 15U };

// EM2 HW-pattern test (BTN0): how long the device stays in EM2.  Picked so
#define EM2_TEST_SLEEP_MS         5000U
// Pattern played before/after EM2 sleep so the pause is visible to the eye.
// Repeat count high enough that the pattern cannot finish during the test.
#define EM2_TEST_REPEAT_COUNT     200U
// Per-channel current for the EM2 test (~3.5 mA/ch, 14 mA total).
#define EM2_TEST_CURRENT_STEP     6U
// LED pattern are both visible before the auto-cycle resumes.
#define EM2_TEST_BLINK_MS         2000U

/*******************************************************************************
 ***************************  LOCAL VARIABLES   ********************************
 ******************************************************************************/

typedef enum {
  MODE_HW_PATTERN = 0,
  MODE_PWM_BRIGHT = 1,
  MODE_SW_COUNTER = 2,
  MODE_COUNT      = 3
} ledsink_mode_t;

static ledsink_mode_t               current_mode     = MODE_HW_PATTERN;
static volatile bool                mode_advance     = false;
static volatile bool                counter_tick     = false;
static uint8_t                      sw_counter       = 0;
static sl_sleeptimer_timer_handle_t mode_timer;
static sl_sleeptimer_timer_handle_t sw_tick_timer;

// EM2 HW-pattern test (BTN0).
// State machine for the BTN0-triggered test:
//   IDLE              -> not running, BTN0 will arm it.
//   ARMED             -> requested but not yet started; main loop will start it.
//   SLEEPING          -> EM2 entered (pattern halted, LEDs off).
//   WOKEN             -> wake-up timer fired, main loop will retrigger pattern.
typedef enum {
  EM2_TEST_IDLE = 0,
  EM2_TEST_ARMED,
  EM2_TEST_SLEEPING,
  EM2_TEST_WOKEN,
} em2_test_state_t;

static volatile em2_test_state_t       em2_test_state = EM2_TEST_IDLE;
static volatile bool                   em2_test_ok_to_sleep = false;
static volatile sl_power_manager_on_isr_exit_t em2_isr_action = SL_POWER_MANAGER_IGNORE;
// Cumulative number of EM2 transitions ever observed since boot.  Drives
// the "EM2 entries should make this counter grow.
static volatile uint32_t               em2_entry_count;
// Snapshot of em2_entry_count taken just before requesting sleep, used
// solely to decide whether THIS test reached EM2 (counter advanced) or
// not (counter unchanged -> FAIL).
static uint32_t                        em2_entry_count_pre_sleep;
static sl_sleeptimer_timer_handle_t    em2_test_timer;
static sl_power_manager_em_transition_event_handle_t em2_event_handle;

/*******************************************************************************
 *********************   LOCAL FUNCTION PROTOTYPES   ***************************
 ******************************************************************************/

static void ledsink_clock_1khz(void);
static void ledsink_clock_400khz(void);
static void ledsink_hw_common_init(uint32_t cycles_per_sec, uint16_t cycles_per_bit,
                                   const uint8_t *current_steps);
static void ledsink_stop_all(void);
static void ledsink_start_all(void);
static void mode_hw_pattern_start(void);
static void mode_pwm_bright_start(void);
static void mode_sw_counter_start(void);
static void mode_sw_counter_stop(void);
static void mode_sw_counter_update(void);
static void advance_mode(void);
static void on_mode_timer(sl_sleeptimer_timer_handle_t *handle, void *data);
static void on_sw_tick(sl_sleeptimer_timer_handle_t *handle, void *data);
static void em2_test_arm(void);
static void em2_test_enter(void);
static void em2_test_resume(void);
static void on_em2_test_wake(sl_sleeptimer_timer_handle_t *handle, void *data);
static void on_em_transition(sl_power_manager_em_t from, sl_power_manager_em_t to);

/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/

/***************************************************************************//**
 * Initialize LEDSINK demo.
 ******************************************************************************/
void ledsink_init(void)
{
  static const sl_power_manager_em_transition_event_info_t em_event_info = {
    .event_mask = SL_POWER_MANAGER_EVENT_TRANSITION_ENTERING_EM2,
    .on_event   = on_em_transition,
  };

  sl_clock_manager_enable_bus_clock(SL_BUS_CLOCK_LEDSINK0);

  // Subscribe so the BTN0 EM2 test can confirm the chip actually reached EM2.
  // (Counter is incremented in on_em_transition.)
  sl_power_manager_subscribe_em_transition_event(&em2_event_handle, &em_event_info);

  // BTN0-triggered EM2 test reaches EM2.  Status is conveyed
  // entirely by the LEDs (and by em2_entry_count for debugger
  // inspection).
  mode_hw_pattern_start();

  sl_sleeptimer_start_periodic_timer_ms(&mode_timer, MODE_DURATION_MS,
                                        on_mode_timer, NULL, 0,
                                        SL_SLEEPTIMER_NO_HIGH_PRECISION_HF_CLOCKS_REQUIRED_FLAG);
}

/***************************************************************************//**
 * LEDSINK ticking function.
 ******************************************************************************/
void ledsink_process_action(void)
{
  if (counter_tick) {
    counter_tick = false;
    mode_sw_counter_update();
  }

  if (mode_advance) {
    mode_advance = false;
    advance_mode();
  }

  // EM2 test state machine
  // Driven entirely from the main loop so the actual sleep call happens in
  // sl_main's idle path (via app_is_ok_to_sleep / sl_power_manager_sleep).
  switch (em2_test_state) {
    case EM2_TEST_ARMED:
      em2_test_enter();
      break;
    case EM2_TEST_WOKEN:
      em2_test_resume();
      break;
    default:
      break;
  }
}

/***************************************************************************//**
 * Power-manager hook: app_is_ok_to_sleep().
 *
 * Returns true only while the BTN0-triggered EM2 test is active.  In every
 * other state the demo runs in EM0 (the periodic timer flag drives polling),
 * so this hook prevents the system from sleeping when it should not.
 ******************************************************************************/
bool app_is_ok_to_sleep(void)
{
  return em2_test_ok_to_sleep;
}

/***************************************************************************//**
 * Power-manager hook: app_sleep_on_isr_exit().
 ******************************************************************************/
sl_power_manager_on_isr_exit_t app_sleep_on_isr_exit(void)
{
  return em2_isr_action;
}

/***************************************************************************//**
 * Simple-button callback.  BTN0 arms the EM2 HW-pattern test.
 *
 * Called from ISR context: do nothing more than set a flag.  The real work
 * happens in ledsink_process_action() on the main loop.
 ******************************************************************************/
void sl_button_on_change(const sl_button_t *handle)
{
  if (sl_button_get_state(handle) != SL_SIMPLE_BUTTON_PRESSED) {
    return;
  }

  if (handle == &sl_button_btn0) {
    em2_test_arm();
  }
}

/*******************************************************************************
 **************************   LOCAL FUNCTIONS   ********************************
 ******************************************************************************/

/***************************************************************************//**
 * Periodic 5 s timer callback — sets mode_advance flag.
 ******************************************************************************/
static void on_mode_timer(sl_sleeptimer_timer_handle_t *handle, void *data)
{
  (void)handle;
  (void)data;
  mode_advance = true;
}

/***************************************************************************//**
 * 300 ms counter tick callback — sets counter_tick flag.
 ******************************************************************************/
static void on_sw_tick(sl_sleeptimer_timer_handle_t *handle, void *data)
{
  (void)handle;
  (void)data;
  counter_tick = true;
}

/***************************************************************************//**
 * Switch LEDSINK clock to ULFRCO ~1 kHz (pattern and SW-drive modes).
 ******************************************************************************/
static void ledsink_clock_1khz(void)
{
  CMU->LEDSINK0CLKCTRL = (_CMU_LEDSINK0CLKCTRL_CLKSEL_ULFRCO
                          << _CMU_LEDSINK0CLKCTRL_CLKSEL_SHIFT);
}

/***************************************************************************//**
 * Switch LEDSINK clock to FSRCO/50 = 400 kHz (PWM mode).
 * PWM frequency = 400 kHz / 16 = 25 kHz (above audible range).
 ******************************************************************************/
static void ledsink_clock_400khz(void)
{
  CMU->LEDSINK0CLKCTRL = ((_CMU_LEDSINK0CLKCTRL_CLKSEL_FSRCO
                           << _CMU_LEDSINK0CLKCTRL_CLKSEL_SHIFT)
                          | (PWM_CLOCK_PRESC << _CMU_LEDSINK0CLKCTRL_PRESC_SHIFT));
}

/***************************************************************************//**
 * Common hardware-mode setup (drive mode, triggers, currents).
 * Clock must be selected by the caller before calling this function.
 ******************************************************************************/
static void ledsink_hw_common_init(uint32_t cycles_per_sec, uint16_t cycles_per_bit,
                                   const uint8_t *current_steps)
{
  sl_hal_ledsink_disable_module(LEDSINK_INST);

  sl_hal_ledsink_configure_auto_failsafe(LEDSINK_INST, true);
  sl_hal_ledsink_set_drive_mode(LEDSINK_INST, SL_HAL_LEDSINK_DRIVE_MODE_PATTERNGEN);
  sl_hal_ledsink_set_trigger_source(LEDSINK_INST,
                                    SL_HAL_LEDSINK_TRIGGER_SOURCE_SW,
                                    SL_HAL_LEDSINK_TRIGGER_SOURCE_SW);
  sl_hal_ledsink_set_cycles_per_sec(LEDSINK_INST, cycles_per_sec);
  sl_hal_ledsink_set_cycles_per_bit(LEDSINK_INST, cycles_per_bit);
  sl_hal_ledsink_set_analog_bias_to_led_delay(LEDSINK_INST, 0U);

  for (uint8_t ch = 0U; ch < NUM_CH; ch++) {
    sl_hal_ledsink_set_channel_current(LEDSINK_INST,
                                       (sl_hal_ledsink_led_channel_t)ch,
                                       current_steps[ch]);
  }
}

/***************************************************************************//**
 * Stop pattern generation on all channels and wait for sync.
 ******************************************************************************/
static void ledsink_stop_all(void)
{
  sl_hal_ledsink_stop_pattern_mask(LEDSINK_INST, SL_HAL_LEDSINK_CHANNEL_MASK);

  uint32_t busy = LEDSINK_SYNCBUSY_SBLED0STOPTRIG
                  | LEDSINK_SYNCBUSY_SBLED1STOPTRIG
                  | LEDSINK_SYNCBUSY_SBLED2STOPTRIG
                  | LEDSINK_SYNCBUSY_SBLED3STOPTRIG;
  while (sl_hal_ledsink_get_sync_busy(LEDSINK_INST) & busy) {
  }
}

/***************************************************************************//**
 * Start all four channels simultaneously and wait for sync.
 ******************************************************************************/
static void ledsink_start_all(void)
{
  sl_hal_ledsink_start_pattern_mask(LEDSINK_INST, SL_HAL_LEDSINK_CHANNEL_MASK);

  uint32_t busy = LEDSINK_SYNCBUSY_SBLED0STARTTRIG
                  | LEDSINK_SYNCBUSY_SBLED1STARTTRIG
                  | LEDSINK_SYNCBUSY_SBLED2STARTTRIG
                  | LEDSINK_SYNCBUSY_SBLED3STARTTRIG;
  while (sl_hal_ledsink_get_sync_busy(LEDSINK_INST) & busy) {
  }
}

/***************************************************************************//**
 * Mode 0: NON-PWM hardware pattern generator with a unique pattern per channel.
 ******************************************************************************/
static void mode_hw_pattern_start(void)
{
  ledsink_clock_1khz();
  // Module is left DISABLED by ledsink_hw_common_init so the per-channel
  // configuration changes below actually take effect.
  ledsink_hw_common_init(PATTERN_CYCLES_PER_SEC, PATTERN_CYCLES_PER_BIT, ch_current);

  sl_hal_ledsink_pwm_config_t pwm_off = {
    .enable       = false,
    .duty_cycle   = 0U,
    .cycle_offset = SL_HAL_LEDSINK_PWM_OFFSET_0_DEG
  };

  for (uint8_t ch = 0U; ch < NUM_CH; ch++) {
    sl_hal_ledsink_configure_pwm(LEDSINK_INST,
                                 (sl_hal_ledsink_led_channel_t)ch, &pwm_off);
    sl_hal_ledsink_set_pattern(LEDSINK_INST,
                               (sl_hal_ledsink_led_channel_t)ch,
                               ch_pattern[ch], 0x00U, ch_patlen[ch]);

    sl_hal_ledsink_set_bit_period(LEDSINK_INST,
                                  (sl_hal_ledsink_led_channel_t)ch, 1U, 1U);
    sl_hal_ledsink_set_repeat(LEDSINK_INST,
                              (sl_hal_ledsink_led_channel_t)ch,
                              REPEAT_COUNT, SL_HAL_LEDSINK_REPEAT_TYPE_NUM);
  }

  // Now that the configuration is programmed, enable module + channels and trigger.
  sl_hal_ledsink_enable_module(LEDSINK_INST);
  sl_hal_ledsink_enable_led_channels(LEDSINK_INST, SL_HAL_LEDSINK_CHANNEL_MASK);

  ledsink_start_all();

  // Mode 0 indication: HW pattern drives LEDs at 500 ms/bit.
  // Visual cue: each channel blinks its own 8-bit pattern (see ch_pattern[]).
}

/***************************************************************************//**
 * Mode 1: PWM hardware pattern generator with four channels at different brightness levels.
 * Uses FSRCO/50 = 400 kHz so PWM runs at 25 kHz (above audible range).
 ******************************************************************************/
static void mode_pwm_bright_start(void)
{
  static const uint8_t pwm_current[NUM_CH] = { PWM_CURRENT_STEP, PWM_CURRENT_STEP,
                                               PWM_CURRENT_STEP, PWM_CURRENT_STEP };
  ledsink_clock_400khz();
  // Module is left DISABLED by ledsink_hw_common_init so the per-channel
  // configuration changes below actually take effect.
  ledsink_hw_common_init(PWM_CYCLES_PER_SEC, PWM_CYCLES_PER_BIT, pwm_current);

  for (uint8_t ch = 0U; ch < NUM_CH; ch++) {
    sl_hal_ledsink_pwm_config_t pwm_cfg = {
      .enable       = true,
      .duty_cycle   = ch_duty[ch],
      .cycle_offset = SL_HAL_LEDSINK_PWM_OFFSET_0_DEG
    };
    sl_hal_ledsink_configure_pwm(LEDSINK_INST,
                                 (sl_hal_ledsink_led_channel_t)ch, &pwm_cfg);

    // Pattern 0xFF (all-1s): LED stays in the ON state continuously so
    // perceived brightness is determined solely by the PWM duty cycle.
    sl_hal_ledsink_set_pattern(LEDSINK_INST,
                               (sl_hal_ledsink_led_channel_t)ch,
                               0xFFFFFFFFUL, 0xFFU, 8U);
    // BITOFFPERIOD must be >= 1 (0 is not a valid bit boundary).
    sl_hal_ledsink_set_bit_period(LEDSINK_INST,
                                  (sl_hal_ledsink_led_channel_t)ch, 1U, 1U);
    sl_hal_ledsink_set_repeat(LEDSINK_INST,
                              (sl_hal_ledsink_led_channel_t)ch,
                              REPEAT_COUNT, SL_HAL_LEDSINK_REPEAT_TYPE_NUM);
  }

  sl_hal_ledsink_enable_module(LEDSINK_INST);
  sl_hal_ledsink_enable_led_channels(LEDSINK_INST, SL_HAL_LEDSINK_CHANNEL_MASK);

  ledsink_start_all();

  // Mode 1 indication: all four LEDs ON simultaneously, each at a
  // different brightness (CH0 dimmest, CH3 brightest -- see ch_duty[]).
}

/***************************************************************************//**
 * Mode 2: software direct-drive — binary counter on four LED channels.
 ******************************************************************************/
static void mode_sw_counter_start(void)
{
  ledsink_clock_1khz();
  sl_hal_ledsink_disable_module(LEDSINK_INST);
  sl_hal_ledsink_set_drive_mode(LEDSINK_INST, SL_HAL_LEDSINK_DRIVE_MODE_SWCONTROL);
  sl_hal_ledsink_enable_module(LEDSINK_INST);
  sl_hal_ledsink_enable_led_channels(LEDSINK_INST, SL_HAL_LEDSINK_CHANNEL_MASK);

  for (uint8_t ch = 0U; ch < NUM_CH; ch++) {
    sl_hal_ledsink_set_channel_current(LEDSINK_INST,
                                       (sl_hal_ledsink_led_channel_t)ch,
                                       ch_current[ch]);
  }

  sl_hal_ledsink_enable_bias_ref(LEDSINK_INST);

  sw_counter = 0U;
  mode_sw_counter_update();

  // 300 ms tick to advance the binary counter display.
  // Mode 2 indication: LEDs count from 0..F in binary (CH0 = LSB, CH3 = MSB).
  sl_sleeptimer_start_periodic_timer_ms(&sw_tick_timer, SW_TICK_MS,
                                        on_sw_tick, NULL, 0,
                                        SL_SLEEPTIMER_NO_HIGH_PRECISION_HF_CLOCKS_REQUIRED_FLAG);
}

/***************************************************************************//**
 * Stop SW direct-drive mode.
 ******************************************************************************/
static void mode_sw_counter_stop(void)
{
  sl_sleeptimer_stop_timer(&sw_tick_timer);

  for (uint8_t ch = 0U; ch < NUM_CH; ch++) {
    sl_hal_ledsink_disable_direct_led(LEDSINK_INST,
                                      (sl_hal_ledsink_led_channel_t)ch);
  }
  sl_hal_ledsink_disable_bias_ref(LEDSINK_INST);
  sl_hal_ledsink_disable_module(LEDSINK_INST);
}

/***************************************************************************//**
 * Display sw_counter as binary on the four LED channels then advance counter.
 ******************************************************************************/
static void mode_sw_counter_update(void)
{
  for (uint8_t ch = 0U; ch < NUM_CH; ch++) {
    if (sw_counter & (1U << ch)) {
      sl_hal_ledsink_enable_direct_led(LEDSINK_INST,
                                       (sl_hal_ledsink_led_channel_t)ch);
    } else {
      sl_hal_ledsink_disable_direct_led(LEDSINK_INST,
                                        (sl_hal_ledsink_led_channel_t)ch);
    }
  }

  sw_counter = (sw_counter + 1U) & 0x0FU;
}

/***************************************************************************//**
 * Advance to the next demo mode.
 ******************************************************************************/
static void advance_mode(void)
{
  switch (current_mode) {
    case MODE_HW_PATTERN:
    case MODE_PWM_BRIGHT:
      ledsink_stop_all();
      break;
    case MODE_SW_COUNTER:
      mode_sw_counter_stop();
      break;
    default:
      break;
  }

  current_mode = (ledsink_mode_t)(((uint8_t)current_mode + 1U)
                                  % (uint8_t)MODE_COUNT);

  switch (current_mode) {
    case MODE_HW_PATTERN: mode_hw_pattern_start(); break;
    case MODE_PWM_BRIGHT: mode_pwm_bright_start(); break;
    case MODE_SW_COUNTER: mode_sw_counter_start(); break;
    default:              break;
  }
}

/*******************************************************************************
 *********************   EM2 HW-PATTERN TEST (BTN0)   **************************
 *
 * Behaviour:
 *   1. BTN0 pressed -> em2_test_arm() sets state = ARMED.
 *   2. Main loop sees ARMED -> em2_test_enter():
 *        - stops auto-cycling, suspends current mode
 *        - configures HW PATTERNGEN (NON-PWM, ULFRCO, long repeat)
 *        - starts the pattern (LEDs blink visibly for ~1 s)
 *        - arms a sleeptimer with the no-HF flag and asks the power manager
 *          to sleep at the lowest reachable EM (EM2)
 *   3. sl_main idle path calls sl_power_manager_sleep() -> EM2.
 *      Then the pattern generator HALTS and LEDs go OFF.
 *   4. Sleeptimer fires -> on_em2_test_wake() releases the sleep flag.
 *   5. Main loop sees WOKEN -> em2_test_resume():
 *        - re-triggers the pattern (LEDs resume visibly)
 *        - prints the result and the EM2 entry count proof
 *        - leaves the test running for ~1 s, then re-arms the auto demo
 ******************************************************************************/

/***************************************************************************//**
 * Power-manager subscriber callback.  Counts EM2 entries so the test can
 * report whether the chip actually reached EM2.
 ******************************************************************************/
static void on_em_transition(sl_power_manager_em_t from,
                             sl_power_manager_em_t to)
{
  (void)from;
  if (to == SL_POWER_MANAGER_EM2) {
    em2_entry_count++;
  }
}

/***************************************************************************//**
 * BTN0 ISR helper: arm the EM2 test if not already running.
 ******************************************************************************/
static void em2_test_arm(void)
{
  if (em2_test_state == EM2_TEST_IDLE) {
    em2_test_state = EM2_TEST_ARMED;
    em2_isr_action = SL_POWER_MANAGER_WAKEUP;
  }
}

/***************************************************************************//**
 * Sleeptimer wake callback: end the EM2 dwell.
 ******************************************************************************/
static void on_em2_test_wake(sl_sleeptimer_timer_handle_t *handle, void *data)
{
  (void)handle;
  (void)data;
  em2_test_ok_to_sleep = false;
  em2_isr_action       = SL_POWER_MANAGER_WAKEUP;
  em2_test_state       = EM2_TEST_WOKEN;
}

/***************************************************************************//**
 * Configure HW pattern, then ask the power manager to sleep into EM2.
 ******************************************************************************/
static void em2_test_enter(void)
{
  static const uint8_t test_current[NUM_CH] = {
    EM2_TEST_CURRENT_STEP, EM2_TEST_CURRENT_STEP,
    EM2_TEST_CURRENT_STEP, EM2_TEST_CURRENT_STEP
  };

  sl_sleeptimer_stop_timer(&mode_timer);

  switch (current_mode) {
    case MODE_HW_PATTERN:
    case MODE_PWM_BRIGHT:
      ledsink_stop_all();
      break;
    case MODE_SW_COUNTER:
      mode_sw_counter_stop();
      break;
    default:
      break;
  }

  ledsink_clock_1khz();
  ledsink_hw_common_init(PATTERN_CYCLES_PER_SEC, PATTERN_CYCLES_PER_BIT,
                         test_current);

  sl_hal_ledsink_pwm_config_t pwm_off = {
    .enable       = false,
    .duty_cycle   = 0U,
    .cycle_offset = SL_HAL_LEDSINK_PWM_OFFSET_0_DEG,
  };

  for (uint8_t ch = 0U; ch < NUM_CH; ch++) {
    sl_hal_ledsink_configure_pwm(LEDSINK_INST,
                                 (sl_hal_ledsink_led_channel_t)ch, &pwm_off);
    sl_hal_ledsink_set_pattern(LEDSINK_INST,
                               (sl_hal_ledsink_led_channel_t)ch,
                               0xAAAAAAAAUL, 0xAAU, 8U);
    sl_hal_ledsink_set_bit_period(LEDSINK_INST,
                                  (sl_hal_ledsink_led_channel_t)ch, 1U, 1U);
    sl_hal_ledsink_set_repeat(LEDSINK_INST,
                              (sl_hal_ledsink_led_channel_t)ch,
                              EM2_TEST_REPEAT_COUNT,
                              SL_HAL_LEDSINK_REPEAT_TYPE_NUM);
  }

  sl_hal_ledsink_enable_module(LEDSINK_INST);
  sl_hal_ledsink_enable_led_channels(LEDSINK_INST, SL_HAL_LEDSINK_CHANNEL_MASK);

  ledsink_start_all();

  // Snapshot the cumulative counter so the wake path can tell whether
  // THIS test actually reached EM2 (counter advanced) or stayed in EM0
  // / EM1 (counter unchanged).  em2_entry_count itself is left
  // cumulative across BTN0 presses for easy debugger inspection.
  em2_entry_count_pre_sleep = em2_entry_count;

  // Arm the sleep request.  Cleared in on_em_transition() / on_em2_test_wake.
  em2_test_state       = EM2_TEST_SLEEPING;
  em2_isr_action       = SL_POWER_MANAGER_SLEEP;
  em2_test_ok_to_sleep = true;

  // Sleeptimer with no-HF flag so it stays armed during EM2.
  sl_sleeptimer_start_timer_ms(&em2_test_timer, EM2_TEST_SLEEP_MS,
                               on_em2_test_wake, NULL, 0,
                               SL_SLEEPTIMER_NO_HIGH_PRECISION_HF_CLOCKS_REQUIRED_FLAG);
}

/***************************************************************************//**
 * Wake-up handler: re-trigger pattern and resume.
 ******************************************************************************/
static void em2_test_resume(void)
{
  // Pattern HALTS on EM2 entry; restart it so users see the LEDs come
  // back to life.  em2_entry_count is cumulative; em2_entry_count_pre_sleep
  // lets the user inspect via debugger whether THIS test reached EM2
  // (em2_entry_count > em2_entry_count_pre_sleep == OK) or stayed in
  // EM0 / EM1 (counters equal == FAIL).
  ledsink_start_all();

  // Brief dwell so the re-triggered LED pattern is visible before the
  // auto-cycle resumes the next mode.
  sl_sleeptimer_delay_millisecond(EM2_TEST_BLINK_MS);

  // Hand control back to the auto demo: stop the test pattern and let the
  // next mode_timer tick start the next mode.
  ledsink_stop_all();
  em2_test_state = EM2_TEST_IDLE;

  // The mode_timer was stopped by em2_test_enter().  Drop any stale
  // advance flag that may have been set just before the test started, then
  // restart the periodic timer so the auto-cycle resumes from "now".
  mode_advance = false;
  sl_sleeptimer_start_periodic_timer_ms(&mode_timer, MODE_DURATION_MS,
                                        on_mode_timer, NULL, 0,
                                        SL_SLEEPTIMER_NO_HIGH_PRECISION_HF_CLOCKS_REQUIRED_FLAG);

  // Restart whichever mode was active before the test, so the demo picks up
  // smoothly without waiting for the next 5 s tick.
  switch (current_mode) {
    case MODE_HW_PATTERN: mode_hw_pattern_start(); break;
    case MODE_PWM_BRIGHT: mode_pwm_bright_start(); break;
    case MODE_SW_COUNTER: mode_sw_counter_start(); break;
    default:              break;
  }
}
