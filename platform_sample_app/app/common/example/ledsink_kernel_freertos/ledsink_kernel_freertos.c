/***************************************************************************//**
 * @file
 * @brief LEDSINK FreeRTOS kernel example
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
#include "sl_power_manager.h"
#include "sl_simple_button_instances.h"
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"
#include "ledsink_kernel_freertos.h"

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

// Each mode runs for 5 seconds before the task advances to the next.
#define MODE_DURATION_MS    5000U
// SW counter advances every 300 ms.
#define SW_TICK_MS          300U

#define REPEAT_COUNT        10U

#ifndef LEDSINK_TASK_STACK_SIZE
#define LEDSINK_TASK_STACK_SIZE   512U
#endif

#ifndef LEDSINK_TASK_PRIO
#define LEDSINK_TASK_PRIO         (tskIDLE_PRIORITY + 1)
#endif

#ifndef EXAMPLE_USE_STATIC_ALLOCATION
#define EXAMPLE_USE_STATIC_ALLOCATION   1
#endif

// Mode 0 / Mode 2 — per-channel analog current.
// I(mA) = (step+1) × 0.5; uniform 6 mA/ch (step=11) so the unique
// blink patterns in Mode 0 are clearly visible -- the previous staircase
// (2/4/7/10 mA) made CH0 too dim to spot at 2 mA.  Total 24 mA <= 30 mA limit.
static const uint8_t ch_current[NUM_CH] = { 11U, 11U, 11U, 11U };

// Mode 0 — unique 8-bit patterns per channel (LSB = bit played first).
//   CH0 0x0F : 2s-ON/2s-OFF
//   CH1 0x33 : 1s-ON/1s-OFF (x2)
//   CH2 0x55 : 500 ms alternating
//   CH3 0x09 : double-flash every 4 s
static const uint32_t ch_pattern[NUM_CH]  = { 0x0FUL, 0x33UL, 0x55UL, 0x09UL };
static const uint8_t  ch_patlen[NUM_CH]   = { 8U, 8U, 8U, 8U     };

// Mode 1 — all channels: pattern 0xFF (always ON); PWM duty varies brightness.
// Uniform current (step=9, 5 mA/ch, 20 mA total) so only duty differs.
// Duty N → (N+1)/16 × 100%; range 6.25% to 100% in 6.25% steps.
#define PWM_CURRENT_STEP    9U
static const uint8_t ch_duty[NUM_CH] = { 0U, 4U, 9U, 15U };

// EM2 HW-pattern test (BTN0): how long the device stays in EM2.  Picked so
// the pause is visible to the eye and the test completes quickly.
#define EM2_TEST_SLEEP_MS         5000U
// Pre-/post-sleep visible blink window.
#define EM2_TEST_BLINK_MS         1000U
// Long repeat so the pattern cannot finish during the test window.
#define EM2_TEST_REPEAT_COUNT     200U
// Per-channel current for the EM2 test (~3.5 mA/ch, 14 mA total).
#define EM2_TEST_CURRENT_STEP     6U

#ifndef EM2_TEST_TASK_STACK_SIZE
#define EM2_TEST_TASK_STACK_SIZE  384U
#endif

#ifndef EM2_TEST_TASK_PRIO
// One above the demo task so it preempts and runs immediately on BTN0.
#define EM2_TEST_TASK_PRIO        (tskIDLE_PRIORITY + 2)
#endif

/*******************************************************************************
 *********************   LOCAL FUNCTION PROTOTYPES   ***************************
 ******************************************************************************/

static void ledsink_task(void *arg);
static void ledsink_clock_1khz(void);
static void ledsink_clock_400khz(void);
static void ledsink_hw_common_init(uint32_t cycles_per_sec, uint16_t cycles_per_bit,
                                   const uint8_t *current_steps);
static void ledsink_stop_all(void);
static void ledsink_start_all(void);
static void mode_hw_pattern_start(void);
static void mode_pwm_bright_start(void);
static void mode_sw_counter_run(void);
static void em2_test_task(void *arg);
static void on_em_transition(sl_power_manager_em_t from,
                             sl_power_manager_em_t to);

/*******************************************************************************
 ***************************  LOCAL STATE   ************************************
 ******************************************************************************/

// Semaphore signalled from BTN0 ISR; the EM2 test task blocks on it.
static SemaphoreHandle_t em2_test_sem;
// Cumulative number of EM2 transitions ever observed since boot
// (incremented in on_em_transition).  Inspect in the debugger to confirm
// how many BTN0 presses successfully reached EM2.
static volatile uint32_t em2_entry_count;
// Snapshot of em2_entry_count taken just before the most recent sleep
// request, used solely so the user can tell from the debugger whether
// THIS test reached EM2 (em2_entry_count > em2_entry_count_pre_sleep)
// or stayed in EM0 / EM1 (counters equal -> FAIL).
static uint32_t em2_entry_count_pre_sleep;
static sl_power_manager_em_transition_event_handle_t em2_event_handle;

/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/

/***************************************************************************//**
 * Initialize LEDSINK and create the demo + EM2-test tasks.
 ******************************************************************************/
void ledsink_init(void)
{
  static const sl_power_manager_em_transition_event_info_t em_event_info = {
    .event_mask = SL_POWER_MANAGER_EVENT_TRANSITION_ENTERING_EM2,
    .on_event   = on_em_transition,
  };

  TaskHandle_t handle = NULL;
  TaskHandle_t em2_handle = NULL;

  // Subscribe so the EM2 test can confirm it actually reached EM2.
  sl_power_manager_subscribe_em_transition_event(&em2_event_handle,
                                                 &em_event_info);

  // Hold an EM1 floor for the demo task.  Without this, FreeRTOS tickless
  // idle would drop the chip to EM2 during every vTaskDelay() in the demo
  // -- the LEDSINK PATTERNGEN engine halts on EM2 entry and the
  // LEDs would go OFF for the whole 5-second mode window.  Holding EM1
  // keeps the pattern engine ticking so the LEDs visibly blink, the
  // same way baremetal's app_is_ok_to_sleep() returning false keeps the
  // bare-metal idle loop in EM0.  The BTN0 EM2 test removes this
  // requirement just before its sleep and re-adds it after wake.
  sl_power_manager_add_em_requirement(SL_POWER_MANAGER_EM1);

#if (EXAMPLE_USE_STATIC_ALLOCATION == 1)
  static StaticSemaphore_t em2_sem_buf;
  em2_test_sem = xSemaphoreCreateBinaryStatic(&em2_sem_buf);
#else
  em2_test_sem = xSemaphoreCreateBinary();
#endif
  EFM_ASSERT(em2_test_sem != NULL);

#if (EXAMPLE_USE_STATIC_ALLOCATION == 1)
  static StaticTask_t task_buf;
  static StackType_t  task_stack[LEDSINK_TASK_STACK_SIZE];

  handle = xTaskCreateStatic(ledsink_task, "ledsink",
                             LEDSINK_TASK_STACK_SIZE, NULL,
                             LEDSINK_TASK_PRIO,
                             task_stack, &task_buf);
  EFM_ASSERT(handle != NULL);

  static StaticTask_t em2_task_buf;
  static StackType_t  em2_task_stack[EM2_TEST_TASK_STACK_SIZE];

  em2_handle = xTaskCreateStatic(em2_test_task, "ledsink_em2",
                                 EM2_TEST_TASK_STACK_SIZE, NULL,
                                 EM2_TEST_TASK_PRIO,
                                 em2_task_stack, &em2_task_buf);
  EFM_ASSERT(em2_handle != NULL);
#else
  BaseType_t ret = xTaskCreate(ledsink_task, "ledsink",
                               LEDSINK_TASK_STACK_SIZE, NULL,
                               LEDSINK_TASK_PRIO, &handle);
  EFM_ASSERT(ret == pdPASS);

  ret = xTaskCreate(em2_test_task, "ledsink_em2",
                    EM2_TEST_TASK_STACK_SIZE, NULL,
                    EM2_TEST_TASK_PRIO, &em2_handle);
  EFM_ASSERT(ret == pdPASS);
#endif
}

/***************************************************************************//**
 * Simple-button callback (ISR context).  BTN0 signals the EM2 test task.
 ******************************************************************************/
void sl_button_on_change(const sl_button_t *handle)
{
  if (sl_button_get_state(handle) != SL_SIMPLE_BUTTON_PRESSED) {
    return;
  }

  if (handle == &sl_button_btn0) {
    BaseType_t higher_prio = pdFALSE;
    if (em2_test_sem != NULL) {
      xSemaphoreGiveFromISR(em2_test_sem, &higher_prio);
      portYIELD_FROM_ISR(higher_prio);
    }
  }
}

/*******************************************************************************
 **************************   LOCAL FUNCTIONS   ********************************
 ******************************************************************************/

/***************************************************************************//**
 * LEDSINK demo task.
 * Cycles through three modes every MODE_DURATION_MS milliseconds using
 * vTaskDelay — the CPU is released to the OS scheduler during each wait.
 ******************************************************************************/
static void ledsink_task(void *arg)
{
  (void)arg;

  sl_clock_manager_enable_bus_clock(SL_BUS_CLOCK_LEDSINK0);

  // Status is conveyed entirely by the LEDs (and by em2_entry_count for
  // debugger inspection).  An EM1 power-manager requirement is held in
  // ledsink_init() so vTaskDelay() below stays at EM1 -- the LEDSINK
  // PATTERNGEN engine keeps ticking and the LEDs visibly blink, instead
  // of halting on an EM2 drop.

  while (1) {
    // Mode 0 — hardware pattern generator with NON-PWM.
    mode_hw_pattern_start();
    vTaskDelay(pdMS_TO_TICKS(MODE_DURATION_MS));
    ledsink_stop_all();

    // Mode 1 — hardware pattern generator with PWM.
    mode_pwm_bright_start();
    vTaskDelay(pdMS_TO_TICKS(MODE_DURATION_MS));
    ledsink_stop_all();

    // Mode 2 — SW direct drive binary counter.
    mode_sw_counter_run();
  }
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
 * Common hardware-mode setup (drive mode, triggers, current, module enable).
 * Clock must be selected by the caller before calling this function.
 ******************************************************************************/
static void ledsink_hw_common_init(uint32_t cycles_per_sec, uint16_t cycles_per_bit,
                                   const uint8_t *current_steps)
{
  // The caller must re-enable the module + channels AFTER programming the per-channel pattern / bit_period / repeat.
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
 * Mode 2: software direct-drive — binary counter for MODE_DURATION_MS total.
 * Uses vTaskDelay between counter steps instead of a sleeptimer callback.
 ******************************************************************************/
static void mode_sw_counter_run(void)
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

  // Mode 2 indication: LEDs count from 0..F in binary (CH0 = LSB, CH3 = MSB).

  // Run the counter for the same 5-second window.
  // MODE_DURATION_MS / SW_TICK_MS = 5000 / 300 ≈ 16 steps.
  const uint8_t steps = (uint8_t)(MODE_DURATION_MS / SW_TICK_MS);
  for (uint8_t i = 0U; i < steps; i++) {
    uint8_t counter = i & 0x0FU;

    for (uint8_t ch = 0U; ch < NUM_CH; ch++) {
      if (counter & (1U << ch)) {
        sl_hal_ledsink_enable_direct_led(LEDSINK_INST,
                                         (sl_hal_ledsink_led_channel_t)ch);
      } else {
        sl_hal_ledsink_disable_direct_led(LEDSINK_INST,
                                          (sl_hal_ledsink_led_channel_t)ch);
      }
    }

    // vTaskDelay releases the CPU — other tasks can run during this wait.
    vTaskDelay(pdMS_TO_TICKS(SW_TICK_MS));
  }

  for (uint8_t ch = 0U; ch < NUM_CH; ch++) {
    sl_hal_ledsink_disable_direct_led(LEDSINK_INST,
                                      (sl_hal_ledsink_led_channel_t)ch);
  }
  sl_hal_ledsink_disable_bias_ref(LEDSINK_INST);
  sl_hal_ledsink_disable_module(LEDSINK_INST);
}

/*******************************************************************************
 *********************   EM2 HW-PATTERN TEST (BTN0)   **************************
 *
 * Behaviour:
 *   1. BTN0 pressed -> sl_button_on_change() gives the binary semaphore.
 *   2. em2_test_task wakes, configures HW PATTERNGEN (NON-PWM, ULFRCO,
 *      long repeat) and starts it (LEDs blink visibly).
 *   3. The task drops the demo's EM1 power-manager floor and vTaskDelays
 *      for EM2_TEST_SLEEP_MS; tickless idle takes the chip into EM2.
 *      The pattern HALTS on EM2 entry and LEDs go OFF.
 *   4. After the delay the task reinstates the EM1 floor, re-triggers
 *      the pattern (LEDs resume blinking visibly), then hands control
 *      back to the demo task.
 ******************************************************************************/

/***************************************************************************//**
 * Power-manager subscriber callback: counts EM2 entries.
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
 * Configure HW pattern (NON-PWM, ULFRCO, long repeat) and start it.
 ******************************************************************************/
static void em2_test_configure_pattern(void)
{
  static const uint8_t test_current[NUM_CH] = {
    EM2_TEST_CURRENT_STEP, EM2_TEST_CURRENT_STEP,
    EM2_TEST_CURRENT_STEP, EM2_TEST_CURRENT_STEP
  };

  ledsink_clock_1khz();
  ledsink_hw_common_init(PATTERN_CYCLES_PER_SEC, PATTERN_CYCLES_PER_BIT,
                         test_current);

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
                               0xAAAAAAAAUL, 0xAAU, 8U);
    // BITOFFPERIOD must be >= 1 (0 is not a valid bit boundary).
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
}

/***************************************************************************//**
 * EM2 HW-pattern test task.  Blocks on the BTN0 semaphore; runs one test
 * per press.
 ******************************************************************************/
static void em2_test_task(void *arg)
{
  (void)arg;

  while (1) {
    // Block forever until BTN0 fires the semaphore from ISR context.
    if (xSemaphoreTake(em2_test_sem, portMAX_DELAY) != pdTRUE) {
      continue;
    }

    em2_test_configure_pattern();

    // Snapshot the cumulative counter so the user can tell from the
    // debugger whether THIS test reached EM2 (counter advanced) or
    // stayed in EM0 / EM1 (counter unchanged).  em2_entry_count itself
    // is left cumulative across BTN0 presses for easy inspection.
    em2_entry_count_pre_sleep = em2_entry_count;

    // Drop the demo's EM1 floor for the dwell so tickless idle is allowed
    // to take the chip down to EM2.  The LEDSINK PATTERNGEN engine halts
    // on EM2 entry -- that is exactly what we want here, since it
    // makes the LED-OFF window during the test a visible cue and produces
    // the ~2 µA dip on AEM.
    sl_power_manager_remove_em_requirement(SL_POWER_MANAGER_EM1);
    vTaskDelay(pdMS_TO_TICKS(EM2_TEST_SLEEP_MS));
    // Reinstate the EM1 floor so the demo's LED pattern keeps running
    // through the post-wake blink window and after the test returns.
    sl_power_manager_add_em_requirement(SL_POWER_MANAGER_EM1);

    // Pattern halted on EM2 entry; restart it so users see the LEDs
    // come back to life.  Pass / fail of THIS test:
    //   em2_entry_count > em2_entry_count_pre_sleep -> reached EM2 (OK)
    //   em2_entry_count == em2_entry_count_pre_sleep -> stayed EM0/EM1 (FAIL)
    ledsink_start_all();

    // Visible blink window after wake before handing back to the demo task.
    vTaskDelay(pdMS_TO_TICKS(EM2_TEST_BLINK_MS));

    ledsink_stop_all();
    sl_hal_ledsink_disable_module(LEDSINK_INST);
  }
}
