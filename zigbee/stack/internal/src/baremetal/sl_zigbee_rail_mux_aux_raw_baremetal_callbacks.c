/***************************************************************************//**
 * @file sl_zigbee_rail_mux_aux_raw_baremetal_callbacks.c
 * @brief internal dispatch for 'sl_zigbee_rail_mux_aux_raw' callbacks as a thin-wrapper
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
#include "app/framework/include/sl_zigbee_rail_mux_aux_raw.h"
#include "stack/internal/inc/sl_zigbee_rail_mux_aux_raw_internal_def.h"

void sli_zigbee_stack_rail_mux_aux_event_callback(sl_rail_handle_t rail_handle,
                                                  sl_rail_events_t events,
                                                  uint8_t *psdu,
                                                  uint16_t psdu_length,
                                                  uint8_t lqi,
                                                  int8_t rssi_dbm,
                                                  uint32_t packet_time)
{
  sl_zigbee_rail_mux_aux_event_callback(rail_handle,
                                        events,
                                        psdu,
                                        psdu_length,
                                        lqi,
                                        rssi_dbm,
                                        packet_time);
}
