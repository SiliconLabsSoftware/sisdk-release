/***************************************************************************//**
 * @file
 * @brief Logger - Power Manager integration glue.
 *
 *   Subscribes to power-manager EM transition events so that logging is
 *   suspended across EM2/EM3 sleep and the µs timestamp counter is
 *   back-filled with the elapsed sleep time read via sleeptimer
 *   (sleeptimer abstracts whichever low-frequency RTC the SoC uses).
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * SPDX-License-Identifier: Zlib
 *
 ******************************************************************************/

#ifndef SL_LOG_POWER_MANAGER_H
#define SL_LOG_POWER_MANAGER_H

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Register the logger as a power-manager EM transition subscriber.
 *
 * Wired in by the @c log_platform_specific component as a @c service_init
 * template contribution when the @c power_manager service is present in
 * the project. Idempotent: subsequent calls have no effect.
 */
void sli_log_pm_subscribe(void);

#ifdef __cplusplus
}
#endif

#endif // SL_LOG_POWER_MANAGER_H
