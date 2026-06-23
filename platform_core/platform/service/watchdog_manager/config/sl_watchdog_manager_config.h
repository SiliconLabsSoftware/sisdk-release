/***************************************************************************//**
 * @file
 * @brief Watchdog Manager Configuration
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

#ifndef SL_WATCHDOG_MANAGER_CONFIG_H
#define SL_WATCHDOG_MANAGER_CONFIG_H

// <<< Use Configuration Wizard in Context Menu >>>

// Timeout period enum values
#define SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_9K      0
#define SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_17K     1
#define SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_33K     2
#define SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_65K     3
#define SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_129K    4
#define SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_257K    5
#define SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_513K    6
#define SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_1M      7
#define SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_2M      8
#define SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_4M      9
#define SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_8M      10
#define SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_16M     11
#define SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_32M     12
#define SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_64M     13
#define SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_128M    14
#define SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_256M    15

// <h> Watchdog Manager Configuration

// <o SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD> Timeout period
// <i> The timeout period is specified in number of CPU cycles (HCLK/1024).
// <i> The hardware watchdog will reset the system if not fed within this period.
// <i> All enabled software watchdogs must be fed to feed the hardware watchdog.
// <i> Choose a period that is longer than the longest expected interval between
// <i> feeds from any software watchdog.
// <i> Note: The actual timeout in seconds depends on the CPU frequency and the
// <i> HCLK prescaler configured by the clock manager. For example, at 38.4 MHz
// <i> CPU frequency with prescaler 1, 256M cycles equals approximately 6.8 seconds.
// <i> Default: SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_256M (longest timeout)
// <SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_9K=> 9K CPU Cycles (~0.24 ms @ 38.4 MHz)
// <SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_17K=> 17K CPU Cycles (~0.45 ms @ 38.4 MHz)
// <SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_33K=> 33K CPU Cycles (~0.88 ms @ 38.4 MHz)
// <SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_65K=> 65K CPU Cycles (~1.7 ms @ 38.4 MHz)
// <SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_129K=> 129K CPU Cycles (~3.4 ms @ 38.4 MHz)
// <SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_257K=> 257K CPU Cycles (~6.9 ms @ 38.4 MHz)
// <SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_513K=> 513K CPU Cycles (~13.7 ms @ 38.4 MHz)
// <SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_1M=> 1M CPU Cycles (~26.7 ms @ 38.4 MHz)
// <SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_2M=> 2M CPU Cycles (~53.5 ms @ 38.4 MHz)
// <SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_4M=> 4M CPU Cycles (~107 ms @ 38.4 MHz)
// <SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_8M=> 8M CPU Cycles (~214 ms @ 38.4 MHz)
// <SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_16M=> 16M CPU Cycles (~427 ms @ 38.4 MHz)
// <SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_32M=> 32M CPU Cycles (~854 ms @ 38.4 MHz)
// <SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_64M=> 64M CPU Cycles (~1.7 s @ 38.4 MHz)
// <SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_128M=> 128M CPU Cycles (~3.4 s @ 38.4 MHz)
// <SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_256M=> 256M CPU Cycles (~6.8 s @ 38.4 MHz)
#define SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD SL_WATCHDOG_MANAGER_TIMEOUT_PERIOD_256M

// <o SL_WATCHDOG_MANAGER_MAX_SW_WATCHDOGS> Maximum number of software watchdogs
// <i> Defines the maximum number of concurrent software watchdog instances.
// <i> Each watchdog consumes memory for the entry structure.
// <i> Reduce to save memory if fewer watchdogs are needed.
// <i> Default: 32 (supports all 32 bit positions)
// <1-32>
// <d> 32
#define SL_WATCHDOG_MANAGER_MAX_SW_WATCHDOGS 32u

// <q SL_WATCHDOG_MANAGER_DEBUG_RUN> WDOG runs during debug halt
// <i> When enabled (1), the hardware watchdog counter keeps running when the CPU
// <i> is halted in a debugger. When disabled (0, default), the counter stops
// <i> during debug halt so the device does not reset while stepping code.
// <i> Enable for testing watchdog behavior in debug; disable for normal debugging.
// <d> 0
#define SL_WATCHDOG_MANAGER_DEBUG_RUN 0

// <q SL_WATCHDOG_MANAGER_EM4_BLOCK> Block entry to EM4 while WDOG is enabled
// <i> When enabled (1), the system cannot enter EM4 while the watchdog
// <i> is running, avoiding unrecoverable sleep with an active watchdog.
// <i> When disabled (0, default), EM4 can be entered (use only if WDOG is disabled in deep sleep).
// <d> 0
#define SL_WATCHDOG_MANAGER_EM4_BLOCK 0

// <q SL_WATCHDOG_MANAGER_LOCK> Lock WDOG configuration after init
// <i> When enabled (1), software cannot change WDOG settings after init; a reset
// <i> is required to reconfigure. Use for production hardening.
// <i> When disabled (0, default), configuration remains modifiable.
// <d> 0
#define SL_WATCHDOG_MANAGER_LOCK 0

// <q SL_WATCHDOG_MANAGER_RESET_DISABLE> Disable WDOG reset output
// <i> When enabled (1), the watchdog counts but does not assert reset (useful
// <i> for debug or when using warning/interrupt only). When disabled (0, default),
// <i> timeout triggers a system reset.
// <d> 0
#define SL_WATCHDOG_MANAGER_RESET_DISABLE 0

// <q SL_WATCHDOG_MANAGER_EM1_RUN> WDOG runs in EM1
// <i> When enabled (1), the watchdog counter keeps running in EM1 sleep.
// <i> When disabled (0, default), the counter stops in EM1. On parts without
// <i> EM1RUN support, the manager disables WDOG on sleep and re-enables on wake.
// <d> 0
#define SL_WATCHDOG_MANAGER_EM1_RUN 0

// <q SL_WATCHDOG_MANAGER_EM2_RUN> WDOG runs in EM2
// <i> When enabled (1), the watchdog counter keeps running in EM2 sleep.
// <i> When disabled (0, default), the counter stops in EM2. On parts without
// <i> EM2RUN support, the manager disables WDOG on sleep and re-enables on wake.
// <d> 0
#define SL_WATCHDOG_MANAGER_EM2_RUN 0

// <q SL_WATCHDOG_MANAGER_EM3_RUN> WDOG runs in EM3
// <i> When enabled (1), the watchdog counter keeps running in EM3 sleep.
// <i> When disabled (0, default), the counter stops in EM3. On parts without
// <i> EM3RUN support, the manager disables WDOG on sleep and re-enables on wake.
// <d> 0
#define SL_WATCHDOG_MANAGER_EM3_RUN 0

// </h>

#endif /* SL_WATCHDOG_MANAGER_CONFIG_H */

// <<< end of configuration section >>>
