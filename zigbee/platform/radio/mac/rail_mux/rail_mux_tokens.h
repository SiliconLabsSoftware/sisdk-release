/***************************************************************************//**
 * @file rail_mux_tokens.h
 * @brief Tokens for RAIL multiplexer runtime configuration.
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * The licensor of this software is Silicon Laboratories Inc. Your use of this
 * software is governed by the terms of Silicon Labs Master Software License
 * Agreement (MSLA) available at
 * www.silabs.com/about-us/legal/master-software-license-agreement. This
 * software is distributed to you in Source Code format and is governed by the
 * sections of the MSLA applicable to Source Code.
 *
 ******************************************************************************/

#include "sl_token_manager_defines.h"

// 0 = Standard/FCS+HDR, 1 = DC/FCS+HDR. Default registered in sli_rail_mux_token_init().
#define COMMON_TOKEN_RAIL_MUX_RXDC_PHY_SELECT \
  SL_TOKEN_GET_DYNAMIC_TOKEN((SL_TOKEN_NVM3_REGION_ZIGBEE | 0x8730), 0)
