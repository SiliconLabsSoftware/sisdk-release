/***************************************************************************//**
 * @file
 * @brief Watchdog Manager default platform integration (bare-metal and RTOS)
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

#include "sl_watchdog_manager.h"
#include "sli_watchdog_manager.h"
#include "sl_status.h"
#include "sl_common.h"
#if defined(SL_CATALOG_FREERTOS_KERNEL_PRESENT)
#include "FreeRTOS.h"
#endif
#if defined(SL_CATALOG_MICRIUMOS_KERNEL_PRESENT)
#include "os.h"
#endif

/***************************************************************************//**
 * @addtogroup watchdog_manager
 * @{
 ******************************************************************************/

/*******************************************************************************
 *****************************   LOCAL DATA   **********************************
 ******************************************************************************/

/// Platform default watchdog handle.
static sl_watchdog_handle_t platform_watchdog_handle = 0;

/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/

/***************************************************************************//**
 * Initialize platform default watchdog.
 *
 * @note This function is called automatically during system initialization.
 ******************************************************************************/
void sli_watchdog_manager_platform_init(void)
{
  sl_status_t status;

  // Create platform default watchdog with reserved UID.
  status = sl_watchdog_manager_create(&platform_watchdog_handle,
                                      SL_WATCHDOG_MANAGER_PLATFORM_DEFAULT_UID);
  (void)status; // Suppress unused variable warning in release builds.
}

/***************************************************************************//**
 * Feed platform default watchdog.
 *
 * @note This function should be called from the main loop in baremetal
 *       applications, or from the idle task in RTOS applications.
 ******************************************************************************/
void sli_watchdog_manager_platform_feed(void)
{
  sl_watchdog_manager_feed(&platform_watchdog_handle);
}

#if ((defined(SL_CATALOG_FREERTOS_KERNEL_PRESENT) && (configUSE_IDLE_HOOK == 1)) \
  || defined(SL_CATALOG_MICRIUMOS_KERNEL_PRESENT))
/***************************************************************************//**
 * Optional application hook invoked after the platform idle feed.
 ******************************************************************************/
SL_WEAK void sl_watchdog_manager_user_idle_hook(void)
{
}
#endif

#if defined(SL_CATALOG_FREERTOS_KERNEL_PRESENT)
#if (configUSE_IDLE_HOOK == 1)
/***************************************************************************//**
 * FreeRTOS idle hook: feed the platform default software watchdog.
 *
 * @details
 * When Watchdog Manager is used with an RTOS, FreeRTOSConfig.h may set
 * configUSE_IDLE_HOOK. This complements feeding from portTASK_SWITCH_HOOK
 * (task switch) so the platform handle is also exercised while the idle task runs.
 *
 * @note Keep this hook minimal; do not block or call non–ISR-safe APIs here.
 * @note Calls @ref sl_watchdog_manager_user_idle_hook after feeding.
 ******************************************************************************/
void vApplicationIdleHook(void)
{
  sli_watchdog_manager_platform_feed();
  sl_watchdog_manager_user_idle_hook();
}
#endif /* configUSE_IDLE_HOOK == 1 */
#endif /* SL_CATALOG_FREERTOS_KERNEL_PRESENT */

#if defined(SL_CATALOG_MICRIUMOS_KERNEL_PRESENT)
/***************************************************************************//**
 * Micrium OS idle enter hook: feed the platform default software watchdog.
 *
 * @details
 * The kernel calls this weak hook from @ref OSSched when the highest ready
 * priority is idle (see @c OSIdleEnterHook in @c os_core.c). This mirrors the
 * FreeRTOS idle-hook path when the CPU spends time in the idle state without
 * frequent context switches. Task-switch feeding is installed separately via
 * @ref sli_watchdog_manager_micrium_install_task_sw_hook when
 * @c OS_CFG_APP_HOOKS_EN is enabled.
 *
 * @note Keep this hook minimal; do not block or call non–ISR-safe APIs here.
 * @note Calls @ref sl_watchdog_manager_user_idle_hook after feeding.
 ******************************************************************************/
void OSIdleEnterHook(void)
{
  sli_watchdog_manager_platform_feed();
  sl_watchdog_manager_user_idle_hook();
}

/***************************************************************************//**
 * Register Micrium @c OS_AppTaskSwHookPtr to feed on context switches (when
 * @c OS_CFG_APP_HOOKS_EN is enabled). Called from @ref sl_watchdog_manager_start().
 ******************************************************************************/
void sli_watchdog_manager_micrium_install_task_sw_hook(void)
{
#if (OS_CFG_APP_HOOKS_EN == DEF_ENABLED)
  OS_AppTaskSwHookPtr = sli_watchdog_manager_platform_feed;
#else
  (void)0;
#endif
}
#endif /* SL_CATALOG_MICRIUMOS_KERNEL_PRESENT */

/** @} (end addtogroup watchdog_manager) */
