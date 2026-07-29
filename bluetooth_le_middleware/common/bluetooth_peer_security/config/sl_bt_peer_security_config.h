/***************************************************************************//**
 * @file
 * @brief Bluetooth Peer Security - config
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
#ifndef SL_BT_PEER_SECURITY_CONFIG_H
#define SL_BT_PEER_SECURITY_CONFIG_H

/***********************************************************************************************//**
 * @addtogroup sl_bt_peer_security
 * @{
 **************************************************************************************************/

// <<< Use Configuration Wizard in Context Menu >>>

// <e SL_BT_PEER_SECURITY_LOG> Log
// <i> Enable or disable logging for this module.
// <i> Default: 0
#define SL_BT_PEER_SECURITY_LOG                              0

// <s SL_BT_PEER_SECURITY_LOG_PREFIX> Log prefix
// <i> Default: "[SEC] "
#define SL_BT_PEER_SECURITY_LOG_PREFIX                       "[SEC]"

// </e>

// <o SL_BT_PEER_SECURITY_IO_CAPABILITY> I/O Capability
// <sl_bt_sm_io_capability_noinputnooutput=> No Input, No Output (Just Works)
// <sl_bt_sm_io_capability_displayonly=> Display Only
// <sl_bt_sm_io_capability_displayyesno=> Display Yes/No
// <sl_bt_sm_io_capability_keyboardonly=> Keyboard Only
// <sl_bt_sm_io_capability_keyboarddisplay=> Keyboard + Display
// <i> Default: sl_bt_sm_io_capability_noinputnooutput
#define SL_BT_PEER_SECURITY_IO_CAPABILITY                    sl_bt_sm_io_capability_noinputnooutput

// <q SL_BT_PEER_SECURITY_BONDING_ENABLED> Allow Bonding
// <i> Enable or disable bonding. When disabled, the bonding database is cleared on init.
// <i> Default: 1
#define SL_BT_PEER_SECURITY_BONDING_ENABLED                  1

// <o SL_BT_PEER_SECURITY_MAX_BONDINGS> Maximum number of bondings <1..32>
// <i> Default: 8
#define SL_BT_PEER_SECURITY_MAX_BONDINGS                     8

// <q SL_BT_PEER_SECURITY_MITM_REQUIRED> Require MITM protection
// <i> When enabled, unauthenticated pairing is rejected.
// <i> Default: 0
#define SL_BT_PEER_SECURITY_MITM_REQUIRED                    0

// <q SL_BT_PEER_SECURITY_BONDED_DEVICES_ONLY> Accept connections from bonded devices only
// <i> When enabled, connections from non-bonded devices are rejected.
// <i> Default: 0
#define SL_BT_PEER_SECURITY_BONDED_DEVICES_ONLY              0

// <q SL_BT_PEER_SECURITY_REJECT_DEBUG_KEYS> Reject debug keys
// <i> When enabled, connections using debug keys (known BT spec keys) are rejected.
// <i> Default: 1
#define SL_BT_PEER_SECURITY_REJECT_DEBUG_KEYS                1

// <q SL_BT_PEER_SECURITY_REQUEST_DEBUG_KEYS> Request debug keys
// <i> Enable to request debug keys by enabling Debug mode of Security Manager.
// <i> Default: 0
#define SL_BT_PEER_SECURITY_REQUEST_DEBUG_KEYS               0

// <q SL_BT_PEER_SECURITY_DELETE_BONDINGS_ON_INIT> Delete all bondings on initialization
// <i> When enabled, all bondings are erased at startup.
// <i> Default: 0
#define SL_BT_PEER_SECURITY_DELETE_BONDINGS_ON_INIT          0

// <o SL_BT_PEER_SECURITY_DEFAULT_PASSKEY> Default passkey <0..999999>
// <i> Passkey used when I/O capability requires it.
// <i> Default: 0
#define SL_BT_PEER_SECURITY_DEFAULT_PASSKEY                  1234

// <q SL_BT_PEER_SECURITY_AUTO_ALLOW_CONFIRMATION> Automatically allow confirmation
// <i> When enabled, the passkey confirmation is automatically allowed.
// <i> Default: 1
#define SL_BT_PEER_SECURITY_AUTO_ALLOW_CONFIRMATION          1

// <<< end of configuration section >>>

/** @} (end addtogroup sl_bt_peer_security) */
#endif // SL_BT_PEER_SECURITY_CONFIG_H
