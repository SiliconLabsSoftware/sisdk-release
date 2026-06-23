/***************************************************************************//**
 * @file
 * @brief Bluetooth Peer Manager - filter API compatibility header
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
#ifndef BLE_PEER_MANAGER_FILTER_H
#define BLE_PEER_MANAGER_FILTER_H

#include "sl_bt_peer_manager_filter.h"

// ---------------------------------------------------------------------------
// Function aliases

#define ble_peer_manager_filter_init                         sl_bt_peer_manager_filter_init
#define ble_peer_manager_set_filter_bt_address               sl_bt_peer_manager_set_filter_bt_address
#define ble_peer_manager_add_allowed_bt_address              sl_bt_peer_manager_add_allowed_bt_address
#define ble_peer_manager_remove_allowed_bt_address           sl_bt_peer_manager_remove_allowed_bt_address
#define ble_peer_manager_set_filter_address_type             sl_bt_peer_manager_set_filter_address_type
#define ble_peer_manager_set_filter_device_name              sl_bt_peer_manager_set_filter_device_name
#define ble_peer_manager_set_filter_service_uuid16           sl_bt_peer_manager_set_filter_service_uuid16
#define ble_peer_manager_set_filter_service_uuid128          sl_bt_peer_manager_set_filter_service_uuid128
#define ble_peer_manager_set_filter_service_data             sl_bt_peer_manager_set_filter_service_data
#define ble_peer_manager_set_filter_manufacturer_data        sl_bt_peer_manager_set_filter_manufacturer_data
#define ble_peer_manager_set_filter_rssi                     sl_bt_peer_manager_set_filter_rssi
#define ble_peer_manager_is_filter_set                       sl_bt_peer_manager_is_filter_set
#define ble_peer_manager_reset_filter                        sl_bt_peer_manager_reset_filter
#define ble_peer_manager_find_match                          sl_bt_peer_manager_find_match
#define ble_peer_manager_is_filter_set_allowed               sl_bt_peer_manager_is_filter_set_allowed
#define ble_peer_manager_str_to_address                      sl_bt_peer_manager_str_to_address

#endif // BLE_PEER_MANAGER_FILTER_H
