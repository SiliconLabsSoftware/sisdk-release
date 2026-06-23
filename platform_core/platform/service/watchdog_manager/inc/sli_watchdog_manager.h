/***************************************************************************//**
 * @file
 * @brief Watchdog Manager Internal API
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

#ifndef SLI_WATCHDOG_MANAGER_H
#define SLI_WATCHDOG_MANAGER_H

#include "sli_watchdog_manager_hal.h"
#include "sl_component_catalog.h"

#if SLI_WATCHDOG_MANAGER_USE_EM_TRANSITION_HOOK
#include "sl_power_manager.h"
#endif

#ifdef __cplusplus
extern "C" {
#endif

/*******************************************************************************
 *****************************   PROTOTYPES   **********************************
 ******************************************************************************/

/***************************************************************************//**
 * Initialize platform default watchdog.
 *
 * @note FOR INTERNAL USE ONLY.
 ******************************************************************************/
void sli_watchdog_manager_platform_init(void);

/***************************************************************************//**
 * Feed platform default watchdog.
 ******************************************************************************/
void sli_watchdog_manager_platform_feed(void);

#if defined(SL_CATALOG_MICRIUMOS_KERNEL_PRESENT)
/***************************************************************************//**
 * Register Micrium @c OS_AppTaskSwHookPtr to feed on context switches (when
 * @c OS_CFG_APP_HOOKS_EN is enabled). Called from @ref sl_watchdog_manager_start().
 ******************************************************************************/
void sli_watchdog_manager_micrium_install_task_sw_hook(void);
#endif

/***************************************************************************//**
 * Record which software watchdog was not fed, for post-reset retrieval.
 *
 * @details
 * Stores the first unfed enabled watchdog handle in no-init state so that
 * after a watchdog-triggered reset, sl_watchdog_manager_retrieve_faulty() can
 * report which watchdog caused the reset. Called internally when the manager
 * detects that not all enabled watchdogs have been fed in time.
 ******************************************************************************/
void sli_watchdog_manager_record_state(void);

#if SLI_WATCHDOG_MANAGER_USE_EM_TRANSITION_HOOK
/***************************************************************************//**
 * Subscribe to power manager EM transition events for watchdog disable/enable
 * when EM1/2/3 run is not all supported. Called from sl_watchdog_manager_start().
 ******************************************************************************/
void sli_watchdog_manager_power_subscribe_em_transition(void);
#endif
#ifdef __cplusplus
}
#endif

#endif /* SLI_WATCHDOG_MANAGER_H */
