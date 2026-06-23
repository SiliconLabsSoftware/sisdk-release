/***************************************************************************//**
 * @file
 * @brief Bluetooth Peer Manager - common config compatibility bridge
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
#ifndef BLE_PEER_MANAGER_COMMON_CONFIG_COMPAT_H
#define BLE_PEER_MANAGER_COMMON_CONFIG_COMPAT_H

// Pull in the original config so any user-customised BLE_PEER_MANAGER_*
// overrides are applied before we map them to the new SL_BT_PEER_MANAGER_* names.
#include "ble_peer_manager_common_config.h"

#ifndef SL_BT_PEER_MANAGER_COMMON_LOG
  #define SL_BT_PEER_MANAGER_COMMON_LOG             BLE_PEER_MANAGER_COMMON_LOG
#endif

#ifndef SL_BT_PEER_MANAGER_COMMON_LOG_PREFIX
  #define SL_BT_PEER_MANAGER_COMMON_LOG_PREFIX      BLE_PEER_MANAGER_COMMON_LOG_PREFIX
#endif

#ifndef SL_BT_PEER_MANAGER_COMMON_MAX_ALLOWED_CONN_COUNT
  #define SL_BT_PEER_MANAGER_COMMON_MAX_ALLOWED_CONN_COUNT \
          BLE_PEER_MANAGER_COMMON_MAX_ALLOWED_CONN_COUNT
#endif

#ifndef SL_BT_PEER_MANAGER_COMMON_TIMEOUT_GATT_MS
  #define SL_BT_PEER_MANAGER_COMMON_TIMEOUT_GATT_MS BLE_PEER_MANAGER_COMMON_TIMEOUT_GATT_MS
#endif

#endif // BLE_PEER_MANAGER_COMMON_CONFIG_COMPAT_H
