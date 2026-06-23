/***************************************************************************//**
 * @file
 * @brief Platform specific helpers for the logging core
 *******************************************************************************
 * # License
 * <b>Copyright 2025 Silicon Laboratories Inc. www.silabs.com</b>
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
#include "sl_clock_manager.h"
#include "sl_interrupt_manager.h"
#include "sl_log_platform_specific.h"
#include "sl_log_internal.h"
#include "sl_log_common_config.h"
#include "sl_log_platform_core_config.h"
#include "sl_log_helper.h"
#include "em_device.h"
#include "sl_hal_timer.h"
#include "sl_device_peripheral.h"

/*******************************************************************************
*******************************   DEFINES   ***********************************
*******************************************************************************/

// Flag set when the timestamp timer has been initialized.
static volatile bool timer_initialized;

/**
 * @brief Host timestamp timer frequency
 *
 * @note
 *  The underlying timestamp timer operates at a hardware frequency of 10MHz.
 *  However, the count values returned by the timer are always divided by 10
 *  before being provided to the logger service. This effectively reduces the
 *  timer's observable frequency for logging purposes to 1MHz.
 */
#define TIMER_FREQUENCY     1000000
#define TIMER_TOP_VALUE     0xFFFFFFFF
#define TIMESTAMP_RESOLUTION 1000000ULL

#define _CONCAT_TWO_TOKENS(token_1, token_2)                     token_1 ## token_2
#define _CONCAT_THREE_TOKENS(token_1, token_2, token_3)          token_1 ## token_2 ## token_3
#define CONCAT_TWO_TOKENS(token_1, token_2)                      _CONCAT_TWO_TOKENS(token_1, token_2)
#define CONCAT_THREE_TOKENS(token_1, token_2, token_3)           _CONCAT_THREE_TOKENS(token_1, token_2, token_3)

#define TIMER_INSTANCE      TIMER(SL_LOG_CONFIG_TIMER_INSTANCE)
#define TIMER_BUS_CLOCK     CONCAT_TWO_TOKENS(SL_BUS_CLOCK_TIMER, SL_LOG_CONFIG_TIMER_INSTANCE)
#define LOGGER_TIMER_IRQ         CONCAT_THREE_TOKENS(TIMER, SL_LOG_CONFIG_TIMER_INSTANCE, _IRQn)
#define LOGGER_TIMER_IRQHandler  CONCAT_THREE_TOKENS(TIMER, SL_LOG_CONFIG_TIMER_INSTANCE, _IRQHandler)
#define LOGGER_TIMER_PERIPHERAL  CONCAT_TWO_TOKENS(SL_PERIPHERAL_TIMER, SL_LOG_CONFIG_TIMER_INSTANCE)

/*******************************************************************************
**************************   LOCAL VARIABLES   ********************************
*******************************************************************************/
static uint64_t scale_factor;

/* Software offset (microseconds) added to every timestamp returned by
 * sl_log_hal_get_timestamp_count(). The offset is grown on every wake-up by
 * the integration layer (see sli_log_platform_add_sleep_offset_us), which
 * measures elapsed sleep time from a low-power-domain time source. The
 * resulting 32-bit µs counter is continuous across EM2/EM3 entries even
 * though the underlying high-frequency timer is gated off during sleep.
 *
 * Single-writer (the wake-side handler runs in the power-manager critical
 * section); readers are sl_log_send_* paths. uint32_t loads/stores are
 * atomic on Cortex-M, so no extra synchronization is needed. */
static volatile uint32_t timestamp_offset_us = 0;

/* HF-TIMER µs reading captured at the most recent pre-sleep entry. Used
 * by the wake-side offset push to figure out how much of the LF-measured
 * sleep window was actually spent with the HF TIMER gated off (EM2)
 * versus running (EM1, e.g. while waiting for HFXO accuracy restore on
 * the way out of EM2). Only the EM2 portion needs to be back-filled into
 * timestamp_offset_us; the EM1 portion was already counted natively
 * by the HF TIMER's CNT advance. */
static volatile uint32_t pre_sleep_hw_us = 0;

/*******************************************************************************
**************************   LOCAL FUNCTIONS   ********************************
*******************************************************************************/

/**
 * @brief Start the platform timestamp counter used by the logging core.
 *
 * Initializes and starts the TIMERn used to provide microsecond
 * resolution timestamps for log events.
 *
 * @return SL_STATUS_OK on success or an sl_status_t error code.
 */
sl_status_t sl_log_hal_platform_core_init(void)
{
  sl_clock_branch_t clock_branch = sl_device_peripheral_get_clock_branch(LOGGER_TIMER_PERIPHERAL);
  sl_hal_timer_config_t init_config = SL_HAL_TIMER_CONFIG_DEFAULT;
  uint32_t log_timer_freq_hz = 0;
  sl_status_t status;

  sl_clock_manager_enable_bus_clock(TIMER_BUS_CLOCK);

  /* With prescaler DIV1 the free-running counter advanced at the full timer branch rate
   * so the 32-bit hardware counter wrapped in a short interval producing
   * confusing early timestamp resets in logs.
   * So we use DIV8 to slow the counter by 8x so the wrap occurs later.
   */
  init_config.prescaler = SL_HAL_TIMER_PRESCALER_DIV8;

  sl_hal_timer_init(TIMER_INSTANCE, &init_config);
  sl_hal_timer_enable(TIMER_INSTANCE);
  sl_hal_timer_set_top(TIMER_INSTANCE, TIMER_TOP_VALUE);
  sl_hal_timer_start(TIMER_INSTANCE);
  sl_hal_timer_clear_interrupts(TIMER_INSTANCE, TIMER_IEN_OF);
  sl_hal_timer_enable_interrupts(TIMER_INSTANCE, TIMER_IEN_OF);

  status = sl_clock_manager_get_clock_branch_frequency(clock_branch, &log_timer_freq_hz);
  if (status) {
      return status;
  }

  /* log_timer_freq_hz is the timer branch clock (before prescaler). With
   * DIV8 the counter ticks at freq/8; multiply by 8 so fixed-point scaling in
   * sl_log_hal_get_timestamp_count() still yields microseconds (TIMESTAMP_RESOLUTION Hz).
   */
  scale_factor = ((TIMESTAMP_RESOLUTION << 32) * 8) / log_timer_freq_hz;

  sl_interrupt_manager_clear_irq_pending(LOGGER_TIMER_IRQ);
  sl_interrupt_manager_enable_irq(LOGGER_TIMER_IRQ);

  timer_initialized = true;
  return SL_STATUS_OK;
}

/**
 * @brief Stop the platform timestamp counter.
 *
 * Stops the TIMERn peripheral.
 *
 * @return SL_STATUS_OK on success or an sl_status_t error code.
 */
sl_status_t sl_log_hal_core_deinit(void)
{
  sl_hal_timer_stop(TIMER_INSTANCE);
  return SL_STATUS_OK;
}

/**
 * @brief Read the HF TIMER's current value in microseconds (no offset).
 *
 * Helper around the same conversion used by @ref sl_log_hal_get_timestamp_count
 * but exposing only the hardware part. Used by the sleep entry/exit path so
 * the wake-side offset push can subtract the µs the HF TIMER ticked during
 * the LF-measured sleep window (e.g. EM1 wait for HFXO accuracy restore)
 * instead of double-counting it. Returns 0 if the timer hasn't been
 * initialized yet.
 */
static uint32_t log_platform_read_hw_us(void)
{
  if (!timer_initialized) {
    return 0U;
  }
  return (uint32_t)(((uint64_t)sl_hal_timer_get_counter(TIMER_INSTANCE)
                     * (uint64_t)scale_factor) >> 32ULL);
}

/**
 * @brief Get the current timestamp count for the specified core.
 *
 * @details
 * Reads the hardware timer counter and converts it to microseconds using a
 * pre-calculated scale factor (computed during platform_core_init), then
 * adds the software offset that accumulates time spent with the HF TIMER
 * gated off (EM2/EM3).
 *
 * @param[in] core_id Core identifier (0 = host, currently unused)
 * @return Current timestamp in microseconds
 */
uint32_t sl_log_hal_get_timestamp_count(uint8_t core_id)
{
  (void)core_id;

  /* Both terms wrap modulo 2^32, so the resulting timestamp behaves like
   * a single free-running 32-bit µs counter. */
  return timestamp_offset_us + log_platform_read_hw_us();
}

/**
 * @brief Get the timestamp timer frequency (Hz) for a core.
 *
 * @param[in] core_id Core identifier (unused)
 * @return Timer frequency in Hz (typically 1,000,000)
 */
uint32_t sl_log_hal_get_timestamp_timer_frequency(uint8_t core_id)
{
  (void)core_id;

  return TIMER_FREQUENCY;
}

/**
 * @brief Push the elapsed time of an LF-measured sleep window into the
 *        platform timestamp offset, compensating for any HF-TIMER advance
 *        that already occurred during the same window.
 *
 * @param[in] delta_us Microseconds elapsed during the most recent sleep,
 *                     measured by the integration layer against a
 *                     low-power-domain time source (e.g. sleeptimer).
 *
 * The HF TIMER is gated while the device is in EM2/EM3 but keeps ticking
 * in EM0/EM1 - including the EM1-while-waiting-for-HFXO-accuracy stretch
 * the power_manager runs after waking from EM2 and before dispatching the
 * LEAVING_EM2 event on the very first sleep of a session. The offset
 * push therefore needs to credit only the *gated* portion of the LF
 * window:
 *
 *     em_gated_us = delta_us - (post_hw_us - pre_hw_us)
 *
 * where @c pre_hw_us was sampled by sl_log_hal_pre_sleep_process at the
 * matching ENTERING_EM2 callback. A clamp at zero protects against the
 * (rare) case where measurement noise makes the HF advance look slightly
 * larger than the LF window.
 *
 * Adding only @c em_gated_us to timestamp_offset_us makes the visible
 * timestamp reflect the real wall-clock elapsed time (= offset push +
 * native HF advance), regardless of how the EM2 wake path internally
 * splits between EM2 and EM1.
 *
 * Caller runs in the power-manager critical section, so the read of the
 * HF TIMER must avoid any SYNCBUSY busy-wait. sl_hal_timer_get_counter
 * is a plain register read with no wait_sync.
 */
void sli_log_platform_add_sleep_offset_us(uint32_t delta_us)
{
  uint32_t post_hw_us  = log_platform_read_hw_us();
  uint32_t hw_advance  = post_hw_us - pre_sleep_hw_us;   /* wrap-safe */
  uint32_t em_gated_us = (delta_us > hw_advance) ? (delta_us - hw_advance) : 0U;
  timestamp_offset_us += em_gated_us;
}

/**
 * @brief Prepare logging subsystem before entering sleep.
 *
 * Marks the logger as suspended (every sl_log_send_* is silently dropped
 * from this point until @ref sl_log_hal_post_sleep_process clears the
 * flag). Pending events already in the ring buffer are NOT flushed: they
 * keep their pre-sleep timestamps and resume transmission after wake.
 *
 * The high-frequency timer is intentionally left running. On Series 2
 * the TIMER's bus-clocked registers (including CNT) are retained across
 * EM2/EM3, and the peripheral simply pauses while its clock branch is
 * gated, then resumes counting on wake. The "lost" sleep duration is
 * accounted for separately by the integration layer pushing a
 * delta-from-LF-RTC value into timestamp_offset_us on wake.
 *
 * Critically, this handler runs inside the power-manager critical
 * section with interrupts masked. It must therefore avoid any TIMER HAL
 * call that includes a SYNCBUSY busy-wait (sl_hal_timer_stop /
 * _set_counter / _start) - a stuck SYNCBUSY across the EM transition
 * would deadlock the wake path with no IRQs available to break out.
 *
 * @param[in] args Unused.
 * @return SL_STATUS_OK on success.
 */
sl_status_t sl_log_hal_pre_sleep_process(void *args)
{
  (void)args;

  /* Snapshot the HF TIMER reading so the wake-side offset push can tell
   * apart the EM2 portion of the sleep window (HF gated) from any EM1
   * portion (HF still ticking, e.g. while the power_manager waits for
   * HFXO accuracy on the way out). See sli_log_platform_add_sleep_offset_us.
   *
   * Reading the timer here is safe even though we run in the
   * power_manager critical section: sl_hal_timer_get_counter is a bare
   * register load with no SYNCBUSY busy-wait. */
  pre_sleep_hw_us = log_platform_read_hw_us();

  sli_log_set_suspended(true);

  return SL_STATUS_OK;
}

/**
 * @brief Restore logging subsystem after wake-up from sleep.
 *
 * Clears the suspension flag and gives the active backend a chance to
 * refresh transport state via its optional @c on_wake hook. The
 * integration layer (sl_log_power_manager.c) has already pushed the
 * elapsed-sleep microseconds into timestamp_offset_us before this runs,
 * so the next call to sl_log_hal_get_timestamp_count() returns a value
 * that advances continuously across the sleep window.
 *
 * The wake hook is deliberately distinct from @c backend_init: the
 * latter is one-shot bring-up (the SystemView backend's init calls
 * SEGGER_SYSVIEW_Conf/Start, which is unsafe to repeat), while @c
 * on_wake is invoked on every EM2/EM3 exit and must therefore be
 * idempotent. Backends that don't need any wake-time action - e.g.
 * SystemView over RTT, or the iostream backends whose UART driver
 * already subscribes to power_manager events directly - leave the
 * pointer NULL and pay no overhead here.
 *
 * Like the pre-sleep handler, this runs inside the PM critical section
 * with interrupts masked, so it must NOT touch the high-frequency TIMER
 * hardware: any wait_sync busy-wait could spin forever if SYNCBUSY is
 * still set from a pre-sleep command that didn't fully sync before EM2
 * gated the clock branch.
 *
 * @param[in] args Unused.
 * @return SL_STATUS_OK, or the backend's @c on_wake error code.
 */
sl_status_t sl_log_hal_post_sleep_process(void *args)
{
  (void)args;

  sl_status_t status = SL_STATUS_OK;

  sl_log_api_backend_t *backend = sl_log_get_api_backend();
  if (backend != NULL && backend->on_wake != NULL) {
    status = backend->on_wake();
  }

  sli_log_set_suspended(false);
  return status;
}

/**
 * @brief Set the platform-specific logging configuration.
 *
 * @param[in] args Pointer to platform config structure
 * @param[in] core_id Core identifier
 * @return SL_STATUS_OK currently always returned
 */
sl_status_t sl_log_hal_set_configuration(void *args, uint8_t core_id)
{
  (void)args;
  (void)core_id;

  return SL_STATUS_OK;
}

/**
 * @brief Get the platform-specific logging configuration.
 *
 * @param[out] args Pointer to a platform config structure to fill
 * @param[in]  core_id Core identifier
 * @return SL_STATUS_OK currently always returned
 */
sl_status_t sl_log_hal_get_configuration(void *args, uint8_t core_id)
{
  (void)args;
  (void)core_id;

  return SL_STATUS_OK;
}

/**
 * @brief   Core API structure.
 *
 */
sl_log_api_core_t sl_log_api_core = { .platform_core_init       = sl_log_hal_platform_core_init,
                                      .platform_core_deinit        = sl_log_hal_core_deinit,
                                      .get_timestamp                 = sl_log_hal_get_timestamp_count,
                                      .get_timestamp_timer_frequency = sl_log_hal_get_timestamp_timer_frequency,
                                      .post_sleep_process            = sl_log_hal_post_sleep_process,
                                      .pre_sleep_process             = sl_log_hal_pre_sleep_process,
                                      .set_configuration             = sl_log_hal_set_configuration,
                                      .get_configuration             = sl_log_hal_get_configuration };

/**
 * @brief Return pointer to the core API structure.
 *
 * Provides the generic logging core APIs
 *
 * @return Pointer to the populated sl_log_api_backend_t structure.
 */
sl_log_api_core_t *sl_log_get_api_core(void)
{
  return &sl_log_api_core;
}

/*******************************************************************************
 * TIMER interrupt handler.
 ******************************************************************************/
void LOGGER_TIMER_IRQHandler(void)
{
  uint32_t irq_flag = sl_hal_timer_get_pending_interrupts(TIMER_INSTANCE);

  if (irq_flag & TIMER_IEN_OF) {
      sl_hal_timer_clear_interrupts(TIMER_INSTANCE, irq_flag & TIMER_IEN_OF);
      /* TODO: Implement logic to store the overflow count in the ring buffer
       * without triggering a log_flush operation.
       */
  }
}