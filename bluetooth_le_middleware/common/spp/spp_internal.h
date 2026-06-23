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

#ifndef SPP_INTERNAL_H
#define SPP_INTERNAL_H

/***************************************************************************//**
 * @addtogroup spp
 * @{
 ******************************************************************************/

// -----------------------------------------------------------------------------
// Includes

#include "sl_bt_api.h"

#ifdef __cplusplus
extern "C" {
#endif

// -----------------------------------------------------------------------------
// Internal function declarations

/***************************************************************************//**
 * Initialize SPP component
 ******************************************************************************/
void spp_init(void);

/***************************************************************************//**
 * Process step for SPP
 ******************************************************************************/
void spp_step(void);

/***************************************************************************//**
 * Initialize the RTA context of the SPP component
 ******************************************************************************/
void spp_rta_init(void);

/***************************************************************************//**
 * Finalize initialization - called when the RTA is ready
 ******************************************************************************/
void spp_rta_ready(void);

/***************************************************************************//**
 * Callback for Bluetooth events
 *
 * @param[in] evt event coming from the Bluetooth stack
 ******************************************************************************/
void spp_on_bt_event(sl_bt_msg_t *evt);

#ifdef __cplusplus
}
#endif

/** @} (end addtogroup spp) */
#endif // SPP_INTERNAL_H
