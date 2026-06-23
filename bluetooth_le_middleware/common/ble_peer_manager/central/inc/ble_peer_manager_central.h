/***************************************************************************//**
 * @file
 * @brief Bluetooth Peer Manager - central API compatibility header
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
#ifndef BLE_PEER_MANAGER_CENTRAL_H
#define BLE_PEER_MANAGER_CENTRAL_H

#include "sl_bt_peer_manager_central.h"

// ---------------------------------------------------------------------------
// Function aliases

#define ble_peer_manager_central_init               sl_bt_peer_manager_central_init
#define ble_peer_manager_central_set_scanner        sl_bt_peer_manager_central_set_scanner
#define ble_peer_manager_central_create_connection  sl_bt_peer_manager_central_create_connection
#define ble_peer_manager_central_open_connection    sl_bt_peer_manager_central_open_connection
#define ble_peer_manager_central_close_connection   sl_bt_peer_manager_central_close_connection

#endif // BLE_PEER_MANAGER_CENTRAL_H
