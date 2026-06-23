/***************************************************************************//**
 * @file sl_zigbee_rail_mux_aux_raw_ipc_callback_events.h
 * @brief callback struct and event handlers for sl_zigbee_rail_mux_aux_raw
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
#ifndef SL_ZIGBEE_RAIL_MUX_AUX_RAW_IPC_CALLBACK_EVENTS_H
#define SL_ZIGBEE_RAIL_MUX_AUX_RAW_IPC_CALLBACK_EVENTS_H

#include "stack/internal/inc/sl_zigbee_rail_mux_aux_raw_internal_def.h"

typedef struct {
  sl_rail_handle_t rail_handle;
  sl_rail_events_t events;
  uint8_t psdu[MAX_IPC_VEC_ARG_CAPACITY];
  uint16_t psdu_length;
  uint8_t lqi;
  int8_t rssi_dbm;
  uint32_t packet_time;
} sli_zigbee_stack_rail_mux_aux_event_callback_ipc_event_t;

#endif // SL_ZIGBEE_RAIL_MUX_AUX_RAW_IPC_CALLBACK_EVENTS_H
