/***************************************************************************//**
 * @file
 * @brief Bluetooth Peer Security
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
#ifndef SL_BT_PEER_SECURITY_H
#define SL_BT_PEER_SECURITY_H

/***********************************************************************************************//**
 * @addtogroup sl_bt_peer_security
 * @{
 **************************************************************************************************/

#include <stdbool.h>
#include "sl_status.h"

// -----------------------------------------------------------------------------
// Enums

// -----------------------------------------------------------------------------
// Public function declarations

/**************************************************************************//**
 * Set the passkey confirmation decision and send it to the stack.
 *
 * Should be called after receiving a passkey confirmation request
 * (SL_BT_PEER_SECURITY_CONFIRM_IN_PROGRESS state).
 *
 * @param[in] confirm true to confirm, false to reject.
 * @note Must not be called from interrupt context.
 * @return SL_STATUS_OK on success, or an error code on failure.
 *****************************************************************************/
sl_status_t sl_bt_peer_security_send_confirmation(bool confirm);

/**************************************************************************//**
 * Connection callback for Peer Security.
 * This callback is called when a passkey confirmation request is received.
 *
 * @param[in] handle The connection handle.
 * @note To be implemented in user code.
 *****************************************************************************/
void sl_bt_peer_security_on_event(uint8_t handle);

/** @} (end addtogroup sl_bt_peer_security) */
#endif // SL_BT_PEER_SECURITY_H
