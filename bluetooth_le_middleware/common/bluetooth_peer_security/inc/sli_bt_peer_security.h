/***************************************************************************//**
 * @file
 * @brief Bluetooth Peer Security Internal Header
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
#ifndef SLI_BT_PEER_SECURITY_H
#define SLI_BT_PEER_SECURITY_H

#include <stdbool.h>
#include "sl_status.h"
#include "sl_bt_api.h"
#include "sl_bt_peer_security.h"

/// Passkey confirmation process states
typedef enum {
  SL_BT_PEER_SECURITY_PROCESS_STARTED,
  SL_BT_PEER_SECURITY_PROCESS_IDLE,
} sl_bt_peer_security_process_state_t;

// -----------------------------------------------------------------------------
// Internal function declarations

/******************************************************************************
 * Initialize Bluetooth Peer Security.
 *****************************************************************************/
void sli_bt_peer_security_init(void);

/******************************************************************************
 * Bluetooth event handler for Peer Security.
 * @param[in] evt Event coming from the Bluetooth stack.
 * @return Status of the operation.
 *****************************************************************************/
sl_status_t sli_bt_peer_security_on_bt_event(const sl_bt_msg_t *evt);

/******************************************************************************
 * Initialize Bluetooth Peer Security Runtime.
 *****************************************************************************/
void sli_bt_peer_security_rta_init(void);

/******************************************************************************
 * Bluetooth Peer Security Runtime Ready.
 *****************************************************************************/
void sli_bt_peer_security_rta_ready(void);

#endif // SLI_BT_PEER_SECURITY_H
