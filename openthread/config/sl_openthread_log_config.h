/*******************************************************************************
 * @file
 * @brief OpenThread log configuration file.
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

#ifndef _SL_OPENTHREAD_LOG_CONFIG_H
#define _SL_OPENTHREAD_LOG_CONFIG_H

//-------- <<< Use Configuration Wizard in Context Menu >>> -----------------
// <h>  Logging
// <o   OPENTHREAD_CONFIG_LOG_OUTPUT> LOG_OUTPUT
//      <OPENTHREAD_CONFIG_LOG_OUTPUT_NONE             => NONE
//      <OPENTHREAD_CONFIG_LOG_OUTPUT_APP              => APP
//      <OPENTHREAD_CONFIG_LOG_OUTPUT_PLATFORM_DEFINED => PLATFORM_DEFINED
// <i>  Default: OPENTHREAD_CONFIG_LOG_OUTPUT_APP
// <d>  OPENTHREAD_CONFIG_LOG_OUTPUT_APP
#ifndef OPENTHREAD_CONFIG_LOG_OUTPUT
#define OPENTHREAD_CONFIG_LOG_OUTPUT OPENTHREAD_CONFIG_LOG_OUTPUT_APP
#endif

// <q>  DYNAMIC_LOG_LEVEL
#ifndef OPENTHREAD_CONFIG_LOG_LEVEL_DYNAMIC_ENABLE
#define OPENTHREAD_CONFIG_LOG_LEVEL_DYNAMIC_ENABLE  0
#endif

// <e>  Enable Logging
#define OPENTHREAD_FULL_LOGS_ENABLE                 0
#if     OPENTHREAD_FULL_LOGS_ENABLE
// <h>  Note: Enabling higher log levels, which include logging packet details, can cause delays which may result in join failures.
// <o   OPENTHREAD_CONFIG_LOG_LEVEL> LOG_LEVEL
//      <OT_LOG_LEVEL_NONE       => NONE
//      <OT_LOG_LEVEL_CRIT       => CRIT
//      <OT_LOG_LEVEL_WARN       => WARN
//      <OT_LOG_LEVEL_NOTE       => NOTE
//      <OT_LOG_LEVEL_INFO       => INFO
//      <OT_LOG_LEVEL_DEBG       => DEBG
// <i>  Default: OT_LOG_LEVEL_DEBG
// <d>  OT_LOG_LEVEL_DEBG
#ifndef OPENTHREAD_CONFIG_LOG_LEVEL
#define OPENTHREAD_CONFIG_LOG_LEVEL OT_LOG_LEVEL_DEBG
#endif
// <q>  CLI
#ifndef OPENTHREAD_CONFIG_LOG_CLI
#define OPENTHREAD_CONFIG_LOG_CLI                   1
#endif
// <q>  PKT_DUMP
#ifndef OPENTHREAD_CONFIG_LOG_PKT_DUMP
#define OPENTHREAD_CONFIG_LOG_PKT_DUMP              1
#endif
// <q>  PLATFORM
#ifndef OPENTHREAD_CONFIG_LOG_PLATFORM
#define OPENTHREAD_CONFIG_LOG_PLATFORM              1
#endif
// <q>  PREPEND_LEVEL
#ifndef OPENTHREAD_CONFIG_LOG_PREPEND_LEVEL
#define OPENTHREAD_CONFIG_LOG_PREPEND_LEVEL         1
#endif
// </h>
#endif // OPENTHREAD_FULL_LOGS_ENABLE
// </e>
// </h>
// <<< end of configuration section >>>
#endif // _SL_OPENTHREAD_LOG_CONFIG_H