/***************************************************************************//**
 * @file sl_zigbee_rail_mux_aux_raw.h
 * @brief Public raw RAIL helpers for the Zigbee RAIL multiplexer auxiliary context.
 *
 * Provides register/unregister and TX wrapper APIs that invoke @c sl_rail_start_tx /
 * @c sl_rail_write_tx_fifo on a mux @c sl_rail_handle_t (for example the handle from
 * @ref sl_zigbee_rail_mux_aux_register_protocol).
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

#ifndef SL_ZIGBEE_RAIL_MUX_AUX_RAW_H
#define SL_ZIGBEE_RAIL_MUX_AUX_RAW_H

#include "sl_rail.h"
#include "stack/include/sl_zigbee_types.h"

typedef void (*sl_zigbee_rail_mux_aux_event_callback_t)(sl_rail_handle_t rail_handle,
                                                         sl_rail_events_t events,
                                                         uint8_t *psdu,
                                                         uint16_t psdu_length,
                                                         uint8_t lqi,
                                                         int8_t rssi_dbm,
                                                         uint32_t packet_time);

/**
 * @brief Register the optional third mux client (fixed context index SUPPORTED_PROTOCOL_COUNT-1).
 *
 * Use this when Zigbee (and typically OpenThread) already occupy earlier mux contexts and the
 * application needs the dedicated last-slot aux handle.
 */
sl_rail_status_t sl_zigbee_rail_mux_aux_register_protocol(sl_rail_handle_t *out_rail_handle,
                                                          sl_rail_config_t *rail_config,
                                                          sl_rail_init_complete_callback_t init_complete_callback);

/** @brief Register default aux context and start aux RX listen path. */
sl_rail_status_t sl_zigbee_rail_mux_aux_try_register_and_start_rx(uint16_t aux_pan,
                                                                   uint8_t channel);

/** @brief Tear down the aux mux client and restore 802.15.4 fast channel-switching logical base. */
sl_rail_status_t sl_zigbee_rail_mux_aux_unregister_protocol(void);

/** @brief RAIL handle last registered by the rail-mux-aux path, or NULL. */
sl_rail_handle_t sl_zigbee_rail_mux_aux_get_default_rail_handle(void);

/** @brief Default AUX listen RAIL config used by the rail-mux-aux CLI path. */
sl_rail_config_t *sl_zigbee_rail_mux_aux_get_default_rail_config(void);

/** @brief Number of RX packets drained on the default AUX listen handle. */
uint32_t sl_zigbee_rail_mux_aux_get_default_listen_rx_packet_count(void);

/** @brief Unified AUX event callback invoked from the AUX RAIL event stream.
 * @internal SL_ZIGBEE_IPC_ARGS
 * {# psdu | length: psdu_length | max: MAX_IPC_VEC_ARG_CAPACITY #}
 */
void sl_zigbee_rail_mux_aux_event_callback(sl_rail_handle_t rail_handle,
                                           sl_rail_events_t events,
                                           uint8_t *psdu,
                                           uint16_t psdu_length,
                                           uint8_t lqi,
                                           int8_t rssi_dbm,
                                           uint32_t packet_time);

/** @brief Wrapper for @c sl_rail_write_tx_fifo on @p rail_handle.
 * @internal SL_ZIGBEE_IPC_ARGS
 * {# data_ptr | length: write_length | max: MAX_IPC_VEC_ARG_CAPACITY #}
 */
uint16_t sl_zigbee_rail_mux_aux_write_tx_fifo(sl_rail_handle_t rail_handle,
                                              const uint8_t *data_ptr,
                                              uint16_t write_length,
                                              bool reset);

/** @brief Wrapper for @c sl_rail_start_tx on @p rail_handle. */
sl_rail_status_t sl_zigbee_rail_mux_aux_start_tx(sl_rail_handle_t rail_handle,
                                                 uint8_t channel,
                                                 sl_rail_tx_options_t options,
                                                 const sl_rail_scheduler_info_t *scheduler_info);

/** @brief Wrapper for @c sl_rail_start_cca_csma_tx on @p rail_handle. */
sl_rail_status_t sl_zigbee_rail_mux_aux_start_cca_csma_tx(sl_rail_handle_t rail_handle,
                                                           uint8_t channel,
                                                           sl_rail_tx_options_t options,
                                                           const sl_rail_csma_config_t *csma_config,
                                                           const sl_rail_scheduler_info_t *scheduler_info);

#endif // SL_ZIGBEE_RAIL_MUX_AUX_RAW_H
