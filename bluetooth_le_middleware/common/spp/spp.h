/***************************************************************************//**
 * @file
 * @brief Serial Port Profile component
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

#ifndef SPP_H
#define SPP_H

/***************************************************************************//**
 * @addtogroup spp
 * @{
 ******************************************************************************/

// -----------------------------------------------------------------------------
// Includes

#include <stdint.h>
#include "spp_internal.h"
#include "sl_bt_api.h"
#include "sl_component_catalog.h"

#ifdef __cplusplus
extern "C" {
#endif

// -----------------------------------------------------------------------------
// Enums

/// @enum spp_role_t
///
/// This enumeration specifies whether the device operates as a central
/// or peripheral in an SPP Bluetooth connection.
typedef enum {
  SPP_CENTRAL = 0,
  SPP_PERIPHERAL,
} spp_role_t;

/// @brief Enumeration of SPP (Serial Port Profile) connection states.
///
/// This enumeration defines the various states that an SPP connection
/// can be in during its lifecycle, from unknown/disconnected state
/// through the connection establishment process to ready state.
typedef enum {
  SPP_UNKNOWN = 0,
  SPP_DISCONNECTED,
  SPP_ENABLE_TX_NOTIFICATION,
  SPP_ENABLE_RX_NOTIFICATION,
  SPP_SEND_INITIAL_BUFFER,
  SPP_CONNECTED
} spp_state_t;

// -----------------------------------------------------------------------------
// Callback typedefs

/// Callback type for data reception
///
/// @param[in] data Pointer to the received data
/// @param[in] data_size Length of the received data in bytes
/// @return Number of bytes consumed by the application
typedef size_t (*spp_on_data_receive_t)(const uint8_t *data, size_t data_size);

// -----------------------------------------------------------------------------
// Public function declarations

/***************************************************************************//**
 * Set SPP role
 *
 * @param[in] role Role to assign (central or peripheral)
 ******************************************************************************/
void spp_set_role(spp_role_t role);

/***************************************************************************//**
 * Get SPP role
 *
 * @return current role of the node
 * @retval See @ref spp_role_t for possible values
 ******************************************************************************/
spp_role_t spp_get_role(void);

/***************************************************************************//**
 * Queue data for transmitting
 *
 * @param[in] data Pointer to the data to be transmitted
 * @param[in] data_size Length of the data in bytes
 * @return SL_STATUS_OK on success, or an error code otherwise
 ******************************************************************************/
sl_status_t spp_transmit(const uint8_t *data, const size_t data_size);

/***************************************************************************//**
 * Callback for when the SPP connection becomes ready
 *
 * The user can override it in their application
 * to perform custom actions when the SPP connection is established.
 ******************************************************************************/
void spp_on_connection_ready(void);

/***************************************************************************//**
 * Register a data reception callback
 *
 * @param[in] spp_on_data_receive Callback invoked when data is received
 ******************************************************************************/
void spp_set_data_receive_callback(spp_on_data_receive_t spp_on_data_receive);

#ifdef __cplusplus
}
#endif

/** @} (end addtogroup spp) */
#endif // SPP_H
