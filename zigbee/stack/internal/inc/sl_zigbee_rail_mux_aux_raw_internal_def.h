/***************************************************************************//**
 * @file sl_zigbee_rail_mux_aux_raw_internal_def.h
 * @brief internal names for 'sl_zigbee_rail_mux_aux_raw' declarations
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
// automatically generated from sl_zigbee_rail_mux_aux_raw.h.  Do not manually edit
#ifndef SL_ZIGBEE_RAIL_MUX_AUX_RAW_INTERNAL_DEF_H
#define SL_ZIGBEE_RAIL_MUX_AUX_RAW_INTERNAL_DEF_H

#include "app/framework/include/sl_zigbee_rail_mux_aux_raw.h"

// Command Indirection

uint32_t sli_zigbee_stack_rail_mux_aux_get_default_listen_rx_packet_count(void);

sl_rail_config_t * sli_zigbee_stack_rail_mux_aux_get_default_rail_config(void);

sl_rail_handle_t sli_zigbee_stack_rail_mux_aux_get_default_rail_handle(void);

sl_rail_status_t sli_zigbee_stack_rail_mux_aux_register_protocol(sl_rail_handle_t *out_rail_handle,
                                                                 sl_rail_config_t *rail_config,
                                                                 sl_rail_init_complete_callback_t init_complete_callback);

sl_rail_status_t sli_zigbee_stack_rail_mux_aux_start_cca_csma_tx(sl_rail_handle_t rail_handle,
                                                                 uint8_t channel,
                                                                 sl_rail_tx_options_t options,
                                                                 const sl_rail_csma_config_t *csma_config,
                                                                 const sl_rail_scheduler_info_t *scheduler_info);

sl_rail_status_t sli_zigbee_stack_rail_mux_aux_start_tx(sl_rail_handle_t rail_handle,
                                                        uint8_t channel,
                                                        sl_rail_tx_options_t options,
                                                        const sl_rail_scheduler_info_t *scheduler_info);

sl_rail_status_t sli_zigbee_stack_rail_mux_aux_try_register_and_start_rx(uint16_t aux_pan,
                                                                         uint8_t channel);

sl_rail_status_t sli_zigbee_stack_rail_mux_aux_unregister_protocol(void);

uint16_t sli_zigbee_stack_rail_mux_aux_write_tx_fifo(sl_rail_handle_t rail_handle,
                                                     const uint8_t *data_ptr,
                                                     uint16_t write_length,
                                                     bool reset);

// Callback Indirection

void sli_zigbee_stack_rail_mux_aux_event_callback(sl_rail_handle_t rail_handle,
                                                  sl_rail_events_t events,
                                                  uint8_t *psdu,
                                                  uint16_t psdu_length,
                                                  uint8_t lqi,
                                                  int8_t rssi_dbm,
                                                  uint32_t packet_time);

#endif // SL_ZIGBEE_RAIL_MUX_AUX_RAW_INTERNAL_DEF_H
