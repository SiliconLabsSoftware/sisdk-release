/***************************************************************************//**
 * @file
 * @brief Bluetooth Peer Manager - connections API compatibility header
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
#ifndef BLE_PEER_MANAGER_CONNECTIONS_H
#define BLE_PEER_MANAGER_CONNECTIONS_H

#include "sl_bt_peer_manager_common.h"
#include "sli_bt_peer_manager_common.h"

// ---------------------------------------------------------------------------
// Type alias

typedef sli_bt_peer_manager_connection_t ble_peer_manager_connection_t;

// ---------------------------------------------------------------------------
// Internal function aliases

#define ble_peer_manager_clear_all_connections           sli_bt_peer_manager_clear_all_connections
#define ble_peer_manager_add_connection                  sli_bt_peer_manager_add_connection
#define ble_peer_manager_delete_connection               sli_bt_peer_manager_delete_connection
#define ble_peer_manager_is_conn_handle_in_array         sli_bt_peer_manager_is_conn_handle_in_array

// ---------------------------------------------------------------------------
// Public function aliases

#define ble_peer_manager_get_active_conn_number          sl_bt_peer_manager_get_active_conn_number
#define ble_peer_manager_get_bt_address                  sl_bt_peer_manager_get_bt_address
#define ble_peer_manager_is_bt_address_already_connected sl_bt_peer_manager_is_bt_address_already_connected
#define ble_peer_manager_is_conn_handle_central          sl_bt_peer_manager_is_conn_handle_central

#endif // BLE_PEER_MANAGER_CONNECTIONS_H
