/***************************************************************************//**
 * @file
 * @brief Bluetooth Peer Manager - filter config
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
#ifndef SL_BT_PEER_MANAGER_FILTER_CONFIG_H
#define SL_BT_PEER_MANAGER_FILTER_CONFIG_H

/***********************************************************************************************//**
 * @addtogroup sl_bt_peer_manager_filter
 * @{
 **************************************************************************************************/

#if defined(SL_CATALOG_BLE_PEER_MANAGER_FILTER_PRESENT)
#include "ble_peer_manager_filter_config_compat.h"
#endif

// <<< Use Configuration Wizard in Context Menu >>>

// <q SL_BT_PEER_MANAGER_FILTER_LOG> Log
// <i> Should the module log or not.
// <i> Default: 0
#ifndef SL_BT_PEER_MANAGER_FILTER_LOG
#define SL_BT_PEER_MANAGER_FILTER_LOG                          0
#endif

// <<< end of configuration section >>>

/** @} (end addtogroup sl_bt_peer_manager_filter) */
#endif // SL_BT_PEER_MANAGER_FILTER_CONFIG_H
