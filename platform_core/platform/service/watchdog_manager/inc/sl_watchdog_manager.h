/***************************************************************************//**
 * @file
 * @brief Watchdog Manager Service API
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

#ifndef SL_WATCHDOG_MANAGER_H
#define SL_WATCHDOG_MANAGER_H

#include "sl_status.h"
#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/***************************************************************************//**
 * @addtogroup watchdog_manager Watchdog Manager
 * @{
 *
 * @brief Watchdog Manager Service
 *
 * @details
 * The Watchdog Manager provides a software watchdog system that allows
 * monitoring multiple periodic code execution streams. It manages a hardware
 * watchdog peripheral (typically WDOG1) and provides multiple virtual software
 * watchdogs that can be created, fed, enabled, and disabled independently.
 *
 * The hardware watchdog is only fed when all enabled software watchdogs have
 * been fed, ensuring that if any monitored code path fails to execute
 * periodically, the system will reset.
 *
 * Key features:
 * - Multiple software watchdogs (up to 32)
 * - Dynamic creation and deletion of software watchdogs
 * - Individual enable/disable control
 * - Stops counting in all sleep modes (EM1/EM2/EM3)
 * - Debug support to identify which watchdog caused a reset
 *
 * Usage:
 * 1. Call sl_watchdog_manager_init() early in initialization
 * 2. Create software watchdogs with sl_watchdog_manager_create()
 * 3. Call sl_watchdog_manager_start() when ready to enable protection
 * 4. Regularly feed each software watchdog with sl_watchdog_manager_feed()
 *
 ******************************************************************************/

/// @brief Handle for software watchdog instances (bit position 0-31, max 32 watchdogs).
/// Valid values: 0 to 31, where each position corresponds to one watchdog instance.
typedef uint32_t sl_watchdog_handle_t;

/// UID reserved for the platform default watchdog (do not use for application watchdogs).
#define SL_WATCHDOG_MANAGER_PLATFORM_DEFAULT_UID  0xFFFFFFFFu

/***************************************************************************//**
 * @brief Initializes watchdog manager.
 *
 * @details
 * This function must be called before any other watchdog manager function.
 * It initializes the internal state and configures the hardware watchdog
 * peripheral, but does not start it yet.
 *
 * @note When returning from this function, the hardware watchdog will not be
 *       started yet. Call sl_watchdog_manager_start() to start it.
 *
 * @note This function is typically called automatically via system
 *       initialization hooks.
 ******************************************************************************/
void sl_watchdog_manager_init(void);

/***************************************************************************//**
 * @brief Starts watchdog manager.
 *
 * @details
 * This function starts the hardware watchdog timer. After calling this
 * function, the software watchdogs must be fed regularly to prevent a system
 * reset.
 *
 * @note Calling this function will start the hardware watchdog. By default,
 *       this is called late in initialization, but can be called earlier to
 *       protect the initialization phase.
 *
 * @note This function is typically called automatically via system
 *       initialization hooks.
 ******************************************************************************/
void sl_watchdog_manager_start(void);

/***************************************************************************//**
 * @brief Creates a software watchdog.
 *
 * @details
 * Creates a new software watchdog instance and returns a handle to it.
 * The watchdog is created in the enabled state and must be fed regularly
 * to prevent a system reset.
 *
 * The watchdog_uid parameter provides a unique identifier for debugging
 * purposes. If a reset occurs due to watchdog expiration, this UID can help
 * identify which watchdog was not fed.
 *
 * @param[out] handle     Pointer to receive the handle to the created software
 *                        watchdog. Must not be NULL.
 * @param[in]  watchdog_uid Software watchdog unique identifier for debugging.
 *                        Use values 256-0xFFFFFFFE for application watchdogs.
 *                        0-255 are reserved for customer use, 0xFFFFFFFF is
 *                        reserved for platform default watchdog.
 *
 * @return SL_STATUS_OK if successful.
 * @return SL_STATUS_NULL_POINTER if handle is NULL.
 * @return SL_STATUS_NO_MORE_RESOURCE if maximum number of watchdogs (32) has
 *         been reached.
 * @return SL_STATUS_NOT_INITIALIZED if sl_watchdog_manager_init() has not
 *         been called.
 ******************************************************************************/
sl_status_t sl_watchdog_manager_create(sl_watchdog_handle_t *handle,
                                       uint32_t watchdog_uid);

/***************************************************************************//**
 * @brief Deletes a software watchdog.
 *
 * @details
 * Deletes a software watchdog instance and frees its handle for reuse.
 * After deletion, the handle is no longer valid and should not be used.
 *
 * @param[in] handle      Pointer to the handle of the software watchdog to
 *                        delete. Must not be NULL. The handle will be set to an
 *                        invalid value (e.g. UINT32_MAX) after deletion.
 *
 * @return SL_STATUS_OK if successful.
 * @return SL_STATUS_NULL_POINTER if handle is NULL.
 * @return SL_STATUS_INVALID_HANDLE if the handle is invalid or already deleted.
 * @return SL_STATUS_NOT_INITIALIZED if sl_watchdog_manager_init() has not
 *         been called.
 ******************************************************************************/
sl_status_t sl_watchdog_manager_delete(sl_watchdog_handle_t *handle);

/***************************************************************************//**
 * @brief Feeds a software watchdog.
 *
 * @details
 * Marks the software watchdog as fed for the current period. When all enabled
 * software watchdogs have been fed, the hardware watchdog is automatically fed.
 *
 * This function should be called periodically from the code path being
 * monitored. The period must be shorter than the configured hardware watchdog
 * timeout.
 *
 * @param[in] handle      Pointer to the handle of the software watchdog to
 *                        feed. Must not be NULL.
 *
 * @return SL_STATUS_OK if successful.
 * @return SL_STATUS_NULL_POINTER if handle is NULL.
 * @return SL_STATUS_INVALID_HANDLE if the handle is invalid.
 * @return SL_STATUS_NOT_INITIALIZED if sl_watchdog_manager_init() has not
 *         been called.
 ******************************************************************************/
sl_status_t sl_watchdog_manager_feed(sl_watchdog_handle_t *handle);

/***************************************************************************//**
 * @brief Disables a software watchdog.
 *
 * @details
 * Disables a software watchdog. A disabled watchdog does not need to be fed
 * to prevent a system reset. The watchdog remains allocated and can be
 * re-enabled later with sl_watchdog_manager_enable().
 *
 * This is useful for temporarily disabling monitoring of a code path, for
 * example during calibration or other long operations.
 *
 * @param[in] handle      Pointer to the handle of the software watchdog to
 *                        disable. Must not be NULL.
 *
 * @return SL_STATUS_OK if successful.
 * @return SL_STATUS_NULL_POINTER if handle is NULL.
 * @return SL_STATUS_INVALID_HANDLE if the handle is invalid.
 * @return SL_STATUS_NOT_INITIALIZED if sl_watchdog_manager_init() has not
 *         been called.
 *
 * @note A disabled software watchdog doesn't need to be fed to prevent a
 *       system reset.
 ******************************************************************************/
sl_status_t sl_watchdog_manager_disable(sl_watchdog_handle_t *handle);

/***************************************************************************//**
 * @brief Checks if a software watchdog is enabled.
 *
 * @details
 * Queries whether a software watchdog is currently enabled or disabled.
 *
 * @param[in]  handle     Pointer to the handle of the software watchdog to
 *                        query. Must not be NULL.
 * @param[out] is_enabled Pointer to variable that will receive the state of
 *                        the software watchdog. True if enabled, false if
 *                        disabled. Must not be NULL.
 *
 * @return SL_STATUS_OK if successful.
 * @return SL_STATUS_NULL_POINTER if handle or is_enabled is NULL.
 * @return SL_STATUS_INVALID_HANDLE if the handle is invalid.
 * @return SL_STATUS_NOT_INITIALIZED if sl_watchdog_manager_init() has not
 *         been called.
 ******************************************************************************/
sl_status_t sl_watchdog_manager_is_enabled(sl_watchdog_handle_t *handle,
                                           bool *is_enabled);

/***************************************************************************//**
 * @brief Enables a software watchdog.
 *
 * @details
 * Enables a previously disabled software watchdog. Once enabled, the watchdog
 * must be fed regularly to prevent a system reset.
 *
 * @param[in] handle      Pointer to the handle of the software watchdog to
 *                        enable. Must not be NULL.
 *
 * @return SL_STATUS_OK if successful.
 * @return SL_STATUS_NULL_POINTER if handle is NULL.
 * @return SL_STATUS_INVALID_HANDLE if the handle is invalid.
 * @return SL_STATUS_NOT_INITIALIZED if sl_watchdog_manager_init() has not
 *         been called.
 ******************************************************************************/
sl_status_t sl_watchdog_manager_enable(sl_watchdog_handle_t *handle);

/***************************************************************************//**
 * @brief Forces a hardware watchdog feed regardless of software watchdogs.
 *
 * @details
 * Forces an immediate feed of the hardware watchdog, bypassing the normal
 * check that all enabled software watchdogs have been fed.
 *
 * This is useful during initialization when software watchdogs may not all be
 * created yet, or during long operations where normal feeding is not possible.
 *
 * @return SL_STATUS_OK if successful.
 * @return SL_STATUS_NOT_INITIALIZED if sl_watchdog_manager_init() has not
 *         been called.
 *
 * @note Force feeding the watchdog can be useful during initialization or
 *       during long operations. Use with caution as it bypasses the normal
 *       watchdog protection mechanism.
 ******************************************************************************/
sl_status_t sl_watchdog_manager_force_feed(void);

/***************************************************************************//**
 * @brief Retrieves the software watchdog that caused a reset.
 *
 * @details
 * After a reset caused by watchdog expiration, this function can be called to
 * retrieve the handle of the first software watchdog that was not fed.
 *
 * This function uses no_init variables to preserve state across resets. It
 * must be called before sl_watchdog_manager_init() to retrieve the information
 * from the previous reset.
 *
 * The function works by comparing the faulty handle from the previous reset
 * with newly created watchdogs. When a match is found during
 * sl_watchdog_manager_create(), a debug message is logged with the watchdog
 * UID.
 *
 * @param[out] handle     Pointer to variable that will receive the handle of
 *                        the first faulty watchdog. Must not be NULL.
 *
 * @return SL_STATUS_OK if successful and a faulty watchdog was found.
 * @return SL_STATUS_NULL_POINTER if handle is NULL.
 * @return SL_STATUS_NOT_AVAILABLE if the reset was not caused by a watchdog.
 * @return SL_STATUS_INVALID_STATE if this function is called after
 *         sl_watchdog_manager_init().
 *
 * @note This function MUST be called before sl_watchdog_manager_init() to
 *       retrieve information from the previous reset.
 *
 * @note Due to dynamic handle allocation, false positives may occur if handles
 *       are reused across resets. This is acceptable for debugging purposes.
 ******************************************************************************/
sl_status_t sl_watchdog_manager_retrieve_faulty(sl_watchdog_handle_t *handle);

#if defined(SL_CATALOG_FREERTOS_KERNEL_PRESENT) || defined(SL_CATALOG_MICRIUMOS_KERNEL_PRESENT)
/***************************************************************************//**
 * @brief Optional application hook invoked after the platform idle feed.
 *
 * @details
 * - **FreeRTOS:** When @c configUSE_IDLE_HOOK is @c 1, @c vApplicationIdleHook()
 *   feeds the platform default watchdog, then calls this user idle hook function.
 * - **Micrium OS:** @c OSIdleEnterHook() feeds the platform default watchdog,
 *   then calls this user idle hook function.
 *
 * To add application-specific idle work, provide a strong implementation of
 * @c sl_watchdog_manager_user_idle_hook() in application code; the
 * linker will replace this weak default implementation with a strong one.

 * @note Do not block. Do not call APIs that might block. Same constraints as
 *       the RTOS idle hook that invokes this callback.
 ******************************************************************************/
void sl_watchdog_manager_user_idle_hook(void);
#endif

/** @} (end addtogroup watchdog_manager) */

#ifdef __cplusplus
}
#endif

#endif /* SL_WATCHDOG_MANAGER_H */
