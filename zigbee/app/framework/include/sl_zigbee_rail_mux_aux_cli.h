/***************************************************************************//**
 * @file sl_zigbee_rail_mux_aux_cli.h
 * @brief Public CLI command handlers for RAIL multiplexer auxiliary (rail-mux-aux) tests.
 *******************************************************************************
 * # License
 * <b>Copyright 2018 Silicon Laboratories Inc. www.silabs.com</b>
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

#ifndef SL_ZIGBEE_RAIL_MUX_AUX_CLI_H
#define SL_ZIGBEE_RAIL_MUX_AUX_CLI_H

#if defined(SL_CATALOG_CLI_PRESENT)
#include "sl_cli.h"

void sl_zigbee_cli_rail_mux_aux_try_register(sl_cli_command_arg_t *arguments);
void sl_zigbee_cli_rail_mux_aux_unregister_aux(sl_cli_command_arg_t *arguments);
void sl_zigbee_cli_rail_mux_aux_mac_rx_unicast(sl_cli_command_arg_t *arguments);
void sl_zigbee_cli_rail_mux_aux_rx_count(sl_cli_command_arg_t *arguments);
void sl_zigbee_cli_rail_mux_aux_tx_fixed_psdu(sl_cli_command_arg_t *arguments);
void sl_zigbee_cli_rail_mux_aux_raw_rx_off(sl_cli_command_arg_t *arguments);

#endif // SL_CATALOG_CLI_PRESENT

#endif // SL_ZIGBEE_RAIL_MUX_AUX_CLI_H
