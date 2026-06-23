/***************************************************************************//**
 * @file
 * @brief Bluetooth Peer Manager - common API compatibility header
 *
 * This file provides backward-compatible aliases for the old ble_peer_manager_*
 * API. Include this file only through the ble_peer_manager_common compatibility
 * SLCC component; do not include it directly in new code.
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
#ifndef BLE_PEER_MANAGER_COMMON_H
#define BLE_PEER_MANAGER_COMMON_H

#include "sl_bt_peer_manager_common.h"

// ---------------------------------------------------------------------------
// Type aliases

typedef sl_bt_peer_manager_evt_id         ble_peer_manager_evt_id;
typedef sl_bt_peer_manager_evt_type_t     ble_peer_manager_evt_type_t;

// ---------------------------------------------------------------------------
// Enum value aliases

#define BLE_PEER_MANAGER_ON_CONN_OPENED_CENTRAL    SL_BT_PEER_MANAGER_ON_CONN_OPENED_CENTRAL
#define BLE_PEER_MANAGER_ON_CONN_OPENED_PERIPHERAL SL_BT_PEER_MANAGER_ON_CONN_OPENED_PERIPHERAL
#define BLE_PEER_MANAGER_ON_CONN_CLOSED            SL_BT_PEER_MANAGER_ON_CONN_CLOSED
#define BLE_PEER_MANAGER_ON_ADV_STOPPED            SL_BT_PEER_MANAGER_ON_ADV_STOPPED
#define BLE_PEER_MANAGER_ERROR                     SL_BT_PEER_MANAGER_ERROR

#endif // BLE_PEER_MANAGER_COMMON_H
