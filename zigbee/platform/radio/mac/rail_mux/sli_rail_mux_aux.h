/***************************************************************************//**
 * @file sli_rail_mux_aux.h
 * @brief RAIL multiplexer aux (try-register): RX FIFO drain API and declarations
 *        shared with the Zigbee stack rail-mux-aux implementation.
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

#ifndef SLI_RAIL_MUX_AUX_H
#define SLI_RAIL_MUX_AUX_H

#include "sl_rail.h"

typedef void (*sli_rail_mux_aux_rx_packet_callback_t)(uint8_t *psdu,
                                                       uint16_t psdu_length,
                                                       uint8_t lqi,
                                                       int8_t rssi_dbm,
                                                       uint32_t packet_time);

/** Drain RAIL RX for this mux handle; returns count of packets copied+released (SUCCESS). */
uint32_t sli_rail_mux_aux_rx_on_event(sl_rail_handle_t rail_handle);

/**
 * @brief Same drain path as @ref sli_rail_mux_aux_rx_on_event, but invokes @p callback
 *        for each READY_SUCCESS / READY_CRC_ERROR packet (PSDU in scratch buffer; valid only
 *        for the duration of the callback). If @p callback is NULL, only counts drained packets.
 */
uint32_t sli_rail_mux_aux_rx_on_event_with_packet_callback(sl_rail_handle_t rail_handle,
                                                              sli_rail_mux_aux_rx_packet_callback_t callback);

void sli_rail_mux_aux_on_register_success(sl_rail_handle_t rail_handle);
void sli_rail_mux_aux_on_unregister_success(void);

#endif // SLI_RAIL_MUX_AUX_H
