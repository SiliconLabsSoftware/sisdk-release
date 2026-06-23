/***************************************************************************//**
 * @file sl_zigbee_rail_mux_aux_raw_ipc_command_messages.c
 * @brief internal wrappers for 'sl_zigbee_rail_mux_aux_raw' ipc commands
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
#include "stack/internal/src/ipc/sl_zigbee_rail_mux_aux_raw_ipc_command_messages.h"
#include "stack/internal/src/ipc/zigbee_ipc_command_messages.h"

// ipc command dispatch

void sli_zigbee_stack_rail_mux_aux_get_default_listen_rx_packet_count_process_ipc_command(sli_zigbee_ipc_cmd_t *msg)
{
  msg->data.rail_mux_aux_get_default_listen_rx_packet_count.response.result = sli_zigbee_stack_rail_mux_aux_get_default_listen_rx_packet_count();
}

void sli_zigbee_stack_rail_mux_aux_get_default_rail_config_process_ipc_command(sli_zigbee_ipc_cmd_t *msg)
{
  msg->data.rail_mux_aux_get_default_rail_config.response.result = sli_zigbee_stack_rail_mux_aux_get_default_rail_config();
}

void sli_zigbee_stack_rail_mux_aux_get_default_rail_handle_process_ipc_command(sli_zigbee_ipc_cmd_t *msg)
{
  msg->data.rail_mux_aux_get_default_rail_handle.response.result = sli_zigbee_stack_rail_mux_aux_get_default_rail_handle();
}

void sli_zigbee_stack_rail_mux_aux_register_protocol_process_ipc_command(sli_zigbee_ipc_cmd_t *msg)
{
  msg->data.rail_mux_aux_register_protocol.response.result = sli_zigbee_stack_rail_mux_aux_register_protocol(&msg->data.rail_mux_aux_register_protocol.request.out_rail_handle,
                                                                                                             &msg->data.rail_mux_aux_register_protocol.request.rail_config,
                                                                                                             msg->data.rail_mux_aux_register_protocol.request.init_complete_callback);
}

void sli_zigbee_stack_rail_mux_aux_start_cca_csma_tx_process_ipc_command(sli_zigbee_ipc_cmd_t *msg)
{
  msg->data.rail_mux_aux_start_cca_csma_tx.response.result = sli_zigbee_stack_rail_mux_aux_start_cca_csma_tx(msg->data.rail_mux_aux_start_cca_csma_tx.request.rail_handle,
                                                                                                             msg->data.rail_mux_aux_start_cca_csma_tx.request.channel,
                                                                                                             msg->data.rail_mux_aux_start_cca_csma_tx.request.options,
                                                                                                             &msg->data.rail_mux_aux_start_cca_csma_tx.request.csma_config,
                                                                                                             &msg->data.rail_mux_aux_start_cca_csma_tx.request.scheduler_info);
}

void sli_zigbee_stack_rail_mux_aux_start_tx_process_ipc_command(sli_zigbee_ipc_cmd_t *msg)
{
  msg->data.rail_mux_aux_start_tx.response.result = sli_zigbee_stack_rail_mux_aux_start_tx(msg->data.rail_mux_aux_start_tx.request.rail_handle,
                                                                                           msg->data.rail_mux_aux_start_tx.request.channel,
                                                                                           msg->data.rail_mux_aux_start_tx.request.options,
                                                                                           &msg->data.rail_mux_aux_start_tx.request.scheduler_info);
}

void sli_zigbee_stack_rail_mux_aux_try_register_and_start_rx_process_ipc_command(sli_zigbee_ipc_cmd_t *msg)
{
  msg->data.rail_mux_aux_try_register_and_start_rx.response.result = sli_zigbee_stack_rail_mux_aux_try_register_and_start_rx(msg->data.rail_mux_aux_try_register_and_start_rx.request.aux_pan,
                                                                                                                             msg->data.rail_mux_aux_try_register_and_start_rx.request.channel);
}

void sli_zigbee_stack_rail_mux_aux_unregister_protocol_process_ipc_command(sli_zigbee_ipc_cmd_t *msg)
{
  msg->data.rail_mux_aux_unregister_protocol.response.result = sli_zigbee_stack_rail_mux_aux_unregister_protocol();
}

void sli_zigbee_stack_rail_mux_aux_write_tx_fifo_process_ipc_command(sli_zigbee_ipc_cmd_t *msg)
{
  msg->data.rail_mux_aux_write_tx_fifo.response.result = sli_zigbee_stack_rail_mux_aux_write_tx_fifo(msg->data.rail_mux_aux_write_tx_fifo.request.rail_handle,
                                                                                                     msg->data.rail_mux_aux_write_tx_fifo.request.data_ptr,
                                                                                                     msg->data.rail_mux_aux_write_tx_fifo.request.write_length,
                                                                                                     msg->data.rail_mux_aux_write_tx_fifo.request.reset);
}

// public entrypoints

uint32_t sl_zigbee_rail_mux_aux_get_default_listen_rx_packet_count(void)
{
  sli_zigbee_ipc_cmd_t msg = { 0, };

  sli_zigbee_send_ipc_cmd(sli_zigbee_stack_rail_mux_aux_get_default_listen_rx_packet_count_process_ipc_command, &msg);

  return msg.data.rail_mux_aux_get_default_listen_rx_packet_count.response.result;
}

sl_rail_config_t * sl_zigbee_rail_mux_aux_get_default_rail_config(void)
{
  sli_zigbee_ipc_cmd_t msg = { 0, };

  sli_zigbee_send_ipc_cmd(sli_zigbee_stack_rail_mux_aux_get_default_rail_config_process_ipc_command, &msg);

  return msg.data.rail_mux_aux_get_default_rail_config.response.result;
}

sl_rail_handle_t sl_zigbee_rail_mux_aux_get_default_rail_handle(void)
{
  sli_zigbee_ipc_cmd_t msg = { 0, };

  sli_zigbee_send_ipc_cmd(sli_zigbee_stack_rail_mux_aux_get_default_rail_handle_process_ipc_command, &msg);

  return msg.data.rail_mux_aux_get_default_rail_handle.response.result;
}

sl_rail_status_t sl_zigbee_rail_mux_aux_register_protocol(sl_rail_handle_t *out_rail_handle,
                                                          sl_rail_config_t *rail_config,
                                                          sl_rail_init_complete_callback_t init_complete_callback)
{
  sli_zigbee_ipc_cmd_t msg = { 0, };

  if (out_rail_handle != NULL) {
    msg.data.rail_mux_aux_register_protocol.request.out_rail_handle = *out_rail_handle;
  }

  if (rail_config != NULL) {
    msg.data.rail_mux_aux_register_protocol.request.rail_config = *rail_config;
  }

  msg.data.rail_mux_aux_register_protocol.request.init_complete_callback = init_complete_callback;
  sli_zigbee_send_ipc_cmd(sli_zigbee_stack_rail_mux_aux_register_protocol_process_ipc_command, &msg);

  if (out_rail_handle != NULL) {
    *out_rail_handle = msg.data.rail_mux_aux_register_protocol.request.out_rail_handle;
  }

  if (rail_config != NULL) {
    *rail_config = msg.data.rail_mux_aux_register_protocol.request.rail_config;
  }

  return msg.data.rail_mux_aux_register_protocol.response.result;
}

sl_rail_status_t sl_zigbee_rail_mux_aux_start_cca_csma_tx(sl_rail_handle_t rail_handle,
                                                          uint8_t channel,
                                                          sl_rail_tx_options_t options,
                                                          const sl_rail_csma_config_t *csma_config,
                                                          const sl_rail_scheduler_info_t *scheduler_info)
{
  sli_zigbee_ipc_cmd_t msg = { 0, };
  msg.data.rail_mux_aux_start_cca_csma_tx.request.rail_handle = rail_handle;
  msg.data.rail_mux_aux_start_cca_csma_tx.request.channel = channel;
  msg.data.rail_mux_aux_start_cca_csma_tx.request.options = options;

  if (csma_config != NULL) {
    msg.data.rail_mux_aux_start_cca_csma_tx.request.csma_config = *csma_config;
  }

  if (scheduler_info != NULL) {
    msg.data.rail_mux_aux_start_cca_csma_tx.request.scheduler_info = *scheduler_info;
  }

  sli_zigbee_send_ipc_cmd(sli_zigbee_stack_rail_mux_aux_start_cca_csma_tx_process_ipc_command, &msg);

  return msg.data.rail_mux_aux_start_cca_csma_tx.response.result;
}

sl_rail_status_t sl_zigbee_rail_mux_aux_start_tx(sl_rail_handle_t rail_handle,
                                                 uint8_t channel,
                                                 sl_rail_tx_options_t options,
                                                 const sl_rail_scheduler_info_t *scheduler_info)
{
  sli_zigbee_ipc_cmd_t msg = { 0, };
  msg.data.rail_mux_aux_start_tx.request.rail_handle = rail_handle;
  msg.data.rail_mux_aux_start_tx.request.channel = channel;
  msg.data.rail_mux_aux_start_tx.request.options = options;

  if (scheduler_info != NULL) {
    msg.data.rail_mux_aux_start_tx.request.scheduler_info = *scheduler_info;
  }

  sli_zigbee_send_ipc_cmd(sli_zigbee_stack_rail_mux_aux_start_tx_process_ipc_command, &msg);

  return msg.data.rail_mux_aux_start_tx.response.result;
}

sl_rail_status_t sl_zigbee_rail_mux_aux_try_register_and_start_rx(uint16_t aux_pan,
                                                                  uint8_t channel)
{
  sli_zigbee_ipc_cmd_t msg = { 0, };
  msg.data.rail_mux_aux_try_register_and_start_rx.request.aux_pan = aux_pan;
  msg.data.rail_mux_aux_try_register_and_start_rx.request.channel = channel;
  sli_zigbee_send_ipc_cmd(sli_zigbee_stack_rail_mux_aux_try_register_and_start_rx_process_ipc_command, &msg);

  return msg.data.rail_mux_aux_try_register_and_start_rx.response.result;
}

sl_rail_status_t sl_zigbee_rail_mux_aux_unregister_protocol(void)
{
  sli_zigbee_ipc_cmd_t msg = { 0, };

  sli_zigbee_send_ipc_cmd(sli_zigbee_stack_rail_mux_aux_unregister_protocol_process_ipc_command, &msg);

  return msg.data.rail_mux_aux_unregister_protocol.response.result;
}

uint16_t sl_zigbee_rail_mux_aux_write_tx_fifo(sl_rail_handle_t rail_handle,
                                              const uint8_t *data_ptr,
                                              uint16_t write_length,
                                              bool reset)
{
  sli_zigbee_ipc_cmd_t msg = { 0, };
  msg.data.rail_mux_aux_write_tx_fifo.request.rail_handle = rail_handle;

  if (write_length > MAX_IPC_VEC_ARG_CAPACITY) {
    assert(false); // "vector data_ptr length exceeds expected maximum
    return msg.data.rail_mux_aux_write_tx_fifo.response.result;
  }

  memmove(msg.data.rail_mux_aux_write_tx_fifo.request.data_ptr, data_ptr, sizeof(uint8_t) * write_length);
  msg.data.rail_mux_aux_write_tx_fifo.request.write_length = write_length;
  msg.data.rail_mux_aux_write_tx_fifo.request.reset = reset;
  sli_zigbee_send_ipc_cmd(sli_zigbee_stack_rail_mux_aux_write_tx_fifo_process_ipc_command, &msg);

  return msg.data.rail_mux_aux_write_tx_fifo.response.result;
}
