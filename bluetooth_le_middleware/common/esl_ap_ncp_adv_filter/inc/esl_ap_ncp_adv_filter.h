/***************************************************************************//**
 * @file
 * @brief ESL Access Point NCP advertisement report filter.
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

#ifndef ESL_AP_NCP_ADV_FILTER_H
#define ESL_AP_NCP_ADV_FILTER_H

#include "sl_bt_api.h"

#ifdef __cplusplus
extern "C" {
#endif

/**************************************************************************//**
 * NCP local event handler for legacy and extended advertisement filtering.
 *
 * @return true to forward the event to the host, false to drop it locally.
 *****************************************************************************/
bool esl_ap_ncp_adv_filter_on_event(sl_bt_msg_t *evt);

#ifdef __cplusplus
}
#endif

#endif // ESL_AP_NCP_ADV_FILTER_H
