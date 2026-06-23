/***************************************************************************//**
 * @file
 * @brief CS Antenna - configuration header
 *******************************************************************************
 * # License
 * <b>Copyright 2024 Silicon Laboratories Inc. www.silabs.com</b>
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
#ifndef CS_ANTENNA_CONFIG_H
#define CS_ANTENNA_CONFIG_H

// <<< Use Configuration Wizard in Context Menu >>>

// <h> CS Antenna configuration

// <q CS_ANTENNA_CONFIG_SET_ON_BOOT> Apply antenna configuration on Bluetooth boot
// <i> When set to 0 (default), the application is responsible for calling
// <i> cs_antenna_configure() explicitly after the Bluetooth system boot event.
// <i> When set to 1, the CS Antenna component automatically calls
// <i> cs_antenna_configure() on the system_boot event using
// <i> CS_ANTENNA_CONFIG_DEFAULT_ANTENNA_OFFSET.
// <i> Default: 0
#ifndef CS_ANTENNA_CONFIG_SET_ON_BOOT
#define CS_ANTENNA_CONFIG_SET_ON_BOOT             0
#endif

// <o CS_ANTENNA_CONFIG_DEFAULT_ANTENNA_OFFSET> Default antenna offset type
// <0=> Wireless antenna offset
// <1=> Wired antenna offset
// <i> Default: 0
#ifndef CS_ANTENNA_CONFIG_DEFAULT_ANTENNA_OFFSET
#define CS_ANTENNA_CONFIG_DEFAULT_ANTENNA_OFFSET  0
#endif

// </h>

#endif // CS_ANTENNA_CONFIG_H
