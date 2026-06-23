/***************************************************************************//**
 * @file
 * @brief Bluetooth Peer Manager - common
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
#ifndef SL_BT_PEER_MANAGER_COMMON_H
#define SL_BT_PEER_MANAGER_COMMON_H

/***********************************************************************************************//**
 * @addtogroup sl_bt_peer_manager_common
 * @{
 **************************************************************************************************/

#include <stdbool.h>
#include <stdint.h>
#include "sl_bt_api.h"

typedef enum {
  SL_BT_PEER_MANAGER_ON_CONN_OPENED_CENTRAL = 0,
  SL_BT_PEER_MANAGER_ON_CONN_OPENED_PERIPHERAL,
  SL_BT_PEER_MANAGER_ON_CONN_CLOSED,
  SL_BT_PEER_MANAGER_ON_ADV_STOPPED,
  SL_BT_PEER_MANAGER_ERROR,
} sl_bt_peer_manager_evt_id;

typedef struct sl_bt_peer_manager_evt_type_s {
  sl_bt_peer_manager_evt_id evt_id;
  uint8_t connection_id;
} sl_bt_peer_manager_evt_type_t;

void sl_bt_peer_manager_on_event(sl_bt_peer_manager_evt_type_t *event);

// -----------------------------------------------------------------------------
// Public connection API

/******************************************************************************
 * Get the number of active connections.
 *
 * @return Number of active connections
 *****************************************************************************/
uint8_t sl_bt_peer_manager_get_active_conn_number(void);

/******************************************************************************
 * Get the BT address of a connection.
 *
 * @param[in] conn_handle Connection handle to get the BT address for.
 *
 * @return Pointer to the BT address, or NULL if not found
 *****************************************************************************/
bd_addr *sl_bt_peer_manager_get_bt_address(uint8_t conn_handle);

/******************************************************************************
 * Check if a device with a given BT address is already connected.
 *
 * @param[in] bt_address BT address to check.
 *
 * @return true if the BT address is already connected, false otherwise
 *****************************************************************************/
bool sl_bt_peer_manager_is_bt_address_already_connected(bd_addr *bt_address);

/******************************************************************************
 * Check if a connection handle is a central connection.
 *
 * @param[in] conn_handle Connection handle to check.
 *
 * @retval true if the connection handle is a central connection
 * @retval false if the connection handle is not a central connection
 *****************************************************************************/
bool sl_bt_peer_manager_is_conn_handle_central(uint8_t conn_handle);

/** @} (end addtogroup sl_bt_peer_manager_common) */
#endif // SL_BT_PEER_MANAGER_COMMON_H
