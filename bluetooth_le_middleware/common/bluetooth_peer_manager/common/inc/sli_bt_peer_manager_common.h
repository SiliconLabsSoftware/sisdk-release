/***************************************************************************//**
 * @file
 * @brief Bluetooth Peer Manager - common internal header file
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
#ifndef SLI_BT_PEER_MANAGER_COMMON_H
#define SLI_BT_PEER_MANAGER_COMMON_H

#include "sl_status.h"
#include "sl_bt_api.h"
#include "sl_bt_peer_manager_common_config.h"
#if defined(SL_CATALOG_APP_LOG_PRESENT) && SL_BT_PEER_MANAGER_COMMON_LOG
  #include "app_log.h"
#endif // defined(SL_CATALOG_APP_LOG_PRESENT) && defined(SL_BT_PEER_MANAGER_COMMON_LOG)

// -----------------------------------------------------------------------------
// Defines
#if defined(SL_CATALOG_APP_LOG_PRESENT) && SL_BT_PEER_MANAGER_COMMON_LOG
#define SLI_BT_PM_PREFIX                                      SL_BT_PEER_MANAGER_COMMON_LOG_PREFIX " "
#define sli_bt_peer_manager_log_debug(...)                    app_log_debug(SLI_BT_PM_PREFIX __VA_ARGS__)
#define sli_bt_peer_manager_log_info(...)                     app_log_info(SLI_BT_PM_PREFIX __VA_ARGS__)
#define sli_bt_peer_manager_log_error(...)                    app_log_error(SLI_BT_PM_PREFIX __VA_ARGS__)
#define sli_bt_peer_manager_log_hexdump(p_data, len) \
  do {                                               \
    app_log_append(SLI_BT_PM_PREFIX);                \
    app_log_hexdump_debug(p_data, len);              \
  } while (0);
#else
#define sli_bt_peer_manager_log_debug(...)
#define sli_bt_peer_manager_log_info(...)
#define sli_bt_peer_manager_log_error(...)
#define sli_bt_peer_manager_log_hexdump(p_data, len)
#endif

// -----------------------------------------------------------------------------
// Internal connection types and API

// Struct for the connection array of the Peer Manager
typedef struct sli_bt_peer_manager_connection_s {
  uint8_t conn_handle;
  sl_bt_connection_role_t conn_type;
  bd_addr peer_address;
} sli_bt_peer_manager_connection_t;

/******************************************************************************
 * Set all connection handles to SL_BT_INVALID_CONNECTION_HANDLE.
 *****************************************************************************/
void sli_bt_peer_manager_clear_all_connections(void);

/******************************************************************************
 * Add a connection to the list of managed connections.
 *
 * @param[in] conn_handle Connection handle to add.
 * @param[in] peer_address BT address of the connection.
 * @param[in] role Role of the connection.
 *
 * @retval SL_STATUS_OK if successful
 * @retval SL_STATUS_NO_MORE_RESOURCE if the new connection cannot be added
 *****************************************************************************/
sl_status_t sli_bt_peer_manager_add_connection(uint8_t conn_handle,
                                               bd_addr peer_address,
                                               sl_bt_connection_role_t role);

/******************************************************************************
 * Delete a connection from the connection array.
 *
 * @param[in] conn_handle Connection handle to delete from the array.
 *
 * @retval SL_STATUS_OK if successful
 * @retval SL_STATUS_NOT_FOUND if the connection handle is not found
 *****************************************************************************/
sl_status_t sli_bt_peer_manager_delete_connection(uint8_t conn_handle);

/******************************************************************************
 * Check if a connection handle is in the connection array.
 *
 * @param[in] conn_handle Connection handle to check.
 *
 * @retval true if the connection handle is in the array
 * @retval false if the connection handle is not in the array
 *****************************************************************************/
bool sli_bt_peer_manager_is_conn_handle_in_array(uint8_t conn_handle);

#endif // SLI_BT_PEER_MANAGER_COMMON_H
