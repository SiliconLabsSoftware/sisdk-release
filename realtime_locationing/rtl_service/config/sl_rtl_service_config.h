/***************************************************************************//**
 * @file
 * @brief Real-Time Locationing Service configuration
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

#ifndef SL_RTL_SERVICE_CONFIG_H
#define SL_RTL_SERVICE_CONFIG_H

// <<< Use Configuration Wizard in Context Menu >>>

// <h> RTL Service Configuration

// <o SL_RTL_SERVICE_CS_MAX_INSTANCES> Max RTL library instances per context <1..16>
// <i> Default: 4
// <i> Each instance owns one sl_rtl_cs_libitem; bounds the internal instance pool.
#ifndef SL_RTL_SERVICE_CS_MAX_INSTANCES
#define SL_RTL_SERVICE_CS_MAX_INSTANCES           (4)
#endif

// <o SL_RTL_SERVICE_CS_GUARD_WAIT> RTA guard wait timeout (ms)
// <i> Default: 0xFFFF (effectively forever for RTA)
// <i> Passed to app_rta_config_t.wait_for_guard (must be non-zero when guard is enabled).
#ifndef SL_RTL_SERVICE_CS_GUARD_WAIT
#define SL_RTL_SERVICE_CS_GUARD_WAIT              (0xFFFFu)
#endif

// <o SL_RTL_SERVICE_CS_TASK_NAME> RTL task name (RTOS; informational)
// <i> Default: "RTL task"
#ifndef SL_RTL_SERVICE_CS_TASK_NAME
#define SL_RTL_SERVICE_CS_TASK_NAME          "RTL task"
#endif

// <o SL_RTL_SERVICE_CS_TASK_STACK_SIZE> RTL / RTA task stack size (bytes)
// <i> Default: 2800
#ifndef SL_RTL_SERVICE_CS_TASK_STACK_SIZE
#define SL_RTL_SERVICE_CS_TASK_STACK_SIZE    (2800)
#endif

// <o SL_RTL_SERVICE_CS_TASK_PRIO> RTL / RTA task priority (app_rta_priority_t)
// <i> Default: 3 (APP_RTA_PRIORITY_ABOVE_NORMAL)
#ifndef SL_RTL_SERVICE_CS_TASK_PRIO
#define SL_RTL_SERVICE_CS_TASK_PRIO          (3)
#endif

// <<< end of configuration section >>>

#endif // SL_RTL_SERVICE_CONFIG_H
