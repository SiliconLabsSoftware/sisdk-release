/***************************************************************************//**
 * @file
 * @brief Bluetooth Peer Manager - central config compatibility bridge
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
#ifndef BLE_PEER_MANAGER_CENTRAL_CONFIG_COMPAT_H
#define BLE_PEER_MANAGER_CENTRAL_CONFIG_COMPAT_H

#include "ble_peer_manager_central_config.h"

#ifndef SL_BT_PEER_MANAGER_CENTRAL_CONFIG_DEFAULT_SCANNING_PHY
  #define SL_BT_PEER_MANAGER_CENTRAL_CONFIG_DEFAULT_SCANNING_PHY \
          BLE_PEER_MANAGER_CENTRAL_CONFIG_DEFAULT_SCANNING_PHY
#endif

#ifndef SL_BT_PEER_MANAGER_CENTRAL_CONFIG_DEFAULT_SCAN_DISCOVERY_MODE
  #define SL_BT_PEER_MANAGER_CENTRAL_CONFIG_DEFAULT_SCAN_DISCOVERY_MODE \
          BLE_PEER_MANAGER_CENTRAL_CONFIG_DEFAULT_SCAN_DISCOVERY_MODE
#endif

#ifndef SL_BT_PEER_MANAGER_CENTRAL_CONFIG_DEFAULT_SCAN_MODE
  #define SL_BT_PEER_MANAGER_CENTRAL_CONFIG_DEFAULT_SCAN_MODE \
          BLE_PEER_MANAGER_CENTRAL_CONFIG_DEFAULT_SCAN_MODE
#endif

#ifndef SL_BT_PEER_MANAGER_CENTRAL_CONFIG_DEFAULT_SCAN_INTERVAL
  #define SL_BT_PEER_MANAGER_CENTRAL_CONFIG_DEFAULT_SCAN_INTERVAL \
          BLE_PEER_MANAGER_CENTRAL_CONFIG_DEFAULT_SCAN_INTERVAL
#endif

#ifndef SL_BT_PEER_MANAGER_CENTRAL_CONFIG_DEFAULT_SCAN_WINDOW
  #define SL_BT_PEER_MANAGER_CENTRAL_CONFIG_DEFAULT_SCAN_WINDOW \
          BLE_PEER_MANAGER_CENTRAL_CONFIG_DEFAULT_SCAN_WINDOW
#endif

#endif // BLE_PEER_MANAGER_CENTRAL_CONFIG_COMPAT_H
