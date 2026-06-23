/***************************************************************************//**
 * @file
 * @brief Bluetooth Peer Manager - peripheral API compatibility header
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
#ifndef BLE_PEER_MANAGER_PERIPHERAL_H
#define BLE_PEER_MANAGER_PERIPHERAL_H

#include "sl_bt_peer_manager_peripheral.h"

// ---------------------------------------------------------------------------
// Function aliases

#define ble_peer_manager_peripheral_init                             sl_bt_peer_manager_peripheral_init
#define ble_peer_manager_peripheral_set_advertiser_discovery_mode    sl_bt_peer_manager_peripheral_set_advertiser_discovery_mode
#define ble_peer_manager_peripheral_set_advertiser_phy               sl_bt_peer_manager_peripheral_set_advertiser_phy
#define ble_peer_manager_peripheral_create_connection                sl_bt_peer_manager_peripheral_create_connection
#define ble_peer_manager_peripheral_start_advertising                sl_bt_peer_manager_peripheral_start_advertising
#define ble_peer_manager_peripheral_stop_advertising                 sl_bt_peer_manager_peripheral_stop_advertising
#define ble_peer_manager_peripheral_close_connection                 sl_bt_peer_manager_peripheral_close_connection

#endif // BLE_PEER_MANAGER_PERIPHERAL_H
