/***************************************************************************//**
 * @file
 * @brief Logger - Power Manager integration.
 *
 *   Subscribes to the power_manager EM transition events. On entry into
 *   EM2 (or EM3 - same notification path on Series 2 / Series 3) the
 *   logger is suspended and a tick count is snapshotted from sleeptimer;
 *   on the matching wake the elapsed sleeptimer ticks are converted to
 *   microseconds and pushed into the platform timestamp accumulator
 *   before the logger is resumed.
 *
 *   Sleeptimer abstracts the actual low-frequency hardware timer
 *   (RTCC / SYSRTC / BURTC / PRORTC) and is guaranteed to be running
 *   from a clock domain that survives EM2 / EM3 in any project that
 *   already uses sleep + wake. Going through its API rather than
 *   touching SoC-specific RTC registers directly avoids hard-faulting
 *   on devices where the chip's CMSIS *_PRESENT macros suggest a
 *   peripheral that the project's actual sleeptimer config didn't
 *   bring up (e.g. xG24, where SYSRTC_PRESENT is set but a build can
 *   still end up using BURTC).
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * SPDX-License-Identifier: Zlib
 *
 ******************************************************************************/

#include "sl_log.h"
#include "sl_log_internal.h"
#include "sl_log_power_manager.h"
#include "sl_power_manager.h"
#include "sl_sleeptimer.h"
#include "sl_status.h"

#include <stdbool.h>
#include <stdint.h>

/*******************************************************************************
 ***************************   LOCAL VARIABLES   ******************************
 ******************************************************************************/

/* Sleeptimer tick count sampled at the last sleep entry. The wake side
 * computes (now - this) modulo 2^32; at the typical 32768 Hz tick rate
 * that's wrap-safe for any plausible sleep duration (~36 hours). */
static uint32_t pre_sleep_ticks;

/* Subscribe-once guard. */
static bool subscribed;

/* Power-manager subscription handle and the event info that drives it.
 * The event_info struct must outlive the subscription, so it is kept
 * static. */
static sl_power_manager_em_transition_event_handle_t s_pm_handle;

static void sli_log_pm_em_transition_cb(sl_power_manager_em_t from,
                                        sl_power_manager_em_t to);

static const sl_power_manager_em_transition_event_info_t s_pm_event_info = {
  .event_mask = SL_POWER_MANAGER_EVENT_TRANSITION_ENTERING_EM2
                | SL_POWER_MANAGER_EVENT_TRANSITION_LEAVING_EM2,
  .on_event   = sli_log_pm_em_transition_cb,
};

/*******************************************************************************
 ***************************   LOCAL FUNCTIONS   ******************************
 ******************************************************************************/

/**
 * @brief Power-manager EM transition callback.
 *
 * Runs inside the power-manager critical section (interrupts masked), so
 * it must stay short and non-blocking. Two relevant transitions exist:
 *  - EM0/EM1 -> EM2 : entering deep sleep. Snapshot tick count, suspend logger.
 *  - EM2 -> EM0/EM1 : leaving deep sleep. Compute elapsed time, resume.
 *
 * EM3 follows the same EM2 notification path on the supported SoCs (the
 * power_manager only emits ENTERING_EM2 / LEAVING_EM2 bits regardless of
 * whether the SoC actually settles in EM2 or EM3).
 */
static void sli_log_pm_em_transition_cb(sl_power_manager_em_t from,
                                        sl_power_manager_em_t to)
{
  if ((from <= SL_POWER_MANAGER_EM1) && (to >= SL_POWER_MANAGER_EM2)) {
    /* Entering deep sleep: sample the sleeptimer tick count, then ask
     * the platform layer to suspend the logger. The suspended flag
     * prevents any further sl_log_send_* from running between this
     * point and the matching wake-side callback. */
    pre_sleep_ticks = sl_sleeptimer_get_tick_count();
    (void)sl_log_pre_sleep_process(NULL);
  } else if ((from >= SL_POWER_MANAGER_EM2) && (to <= SL_POWER_MANAGER_EM1)) {
    /* Leaving deep sleep: convert the elapsed sleeptimer ticks to
     * microseconds via the wrap-safe helper (see the overflow analysis
     * in the sli_log_pm_lf_ticks_to_us doxygen in sl_log_internal.h),
     * push the result into the platform offset, then resume logging. */
    uint32_t now_ticks = sl_sleeptimer_get_tick_count();
    uint32_t delta_us  = sli_log_pm_lf_ticks_to_us(
      pre_sleep_ticks,
      now_ticks,
      sl_sleeptimer_get_timer_frequency());

    sli_log_platform_add_sleep_offset_us(delta_us);
    (void)sl_log_post_sleep_process(NULL);
  }
}

/*******************************************************************************
 ***************************   GLOBAL FUNCTIONS   *****************************
 ******************************************************************************/

uint32_t sli_log_pm_lf_ticks_to_us(uint32_t pre_ticks,
                                   uint32_t now_ticks,
                                   uint32_t freq_hz)
{
  if (freq_hz == 0U) {
    return 0U;
  }

  /* uint32_t modular subtraction - correct across any single wrap of
   * the LF counter. The widening to uint64_t keeps the *1e6 product
   * from overflowing; the final cast back to uint32_t intentionally
   * truncates modulo 2^32 us so the result composes with the visible
   * 32-bit timestamp's natural wrap. */
  uint32_t delta_ticks = now_ticks - pre_ticks;
  return (uint32_t)(((uint64_t)delta_ticks * 1000000ULL) / (uint64_t)freq_hz);
}

void sli_log_pm_subscribe(void)
{
  if (subscribed) {
    return;
  }

  /* Sleeptimer is required at the SLCC level whenever this file is
   * compiled (see log_platform_specific.slcc), so its tick source is
   * already up by the time any sleep cycle reaches us. */
  (void)sl_power_manager_subscribe_em_transition_event(&s_pm_handle,
                                                       &s_pm_event_info);
  subscribed = true;
}
