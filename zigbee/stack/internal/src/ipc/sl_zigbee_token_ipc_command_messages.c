/***************************************************************************//**
 * @file sl_zigbee_token_ipc_command_messages.c
 * @brief internal wrappers for 'sl_zigbee_token' ipc commands
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
// automatically generated from sl_zigbee_token.h.  Do not manually edit
#include "stack/include/sl_zigbee_token.h"
#include "stack/internal/inc/sl_zigbee_token_internal_def.h"
#include "stack/internal/src/ipc/sl_zigbee_token_ipc_command_messages.h"
#include "stack/internal/src/ipc/zigbee_ipc_command_messages.h"

// ipc command dispatch

void sli_zigbee_stack_get_token_count_process_ipc_command(sli_zigbee_ipc_cmd_t *msg)
{
  msg->data.get_token_count.response.result = sli_zigbee_stack_get_token_count();
}

void sli_zigbee_stack_get_token_data_process_ipc_command(sli_zigbee_ipc_cmd_t *msg)
{
  msg->data.get_token_data.response.result = sli_zigbee_stack_get_token_data(msg->data.get_token_data.request.token,
                                                                             msg->data.get_token_data.request.index,
                                                                             &msg->data.get_token_data.request.tokenData);
}

void sli_zigbee_stack_get_token_default_process_ipc_command(sli_zigbee_ipc_cmd_t *msg)
{
  msg->data.get_token_default.response.result = sli_zigbee_stack_get_token_default(msg->data.get_token_default.request.token,
                                                                                   msg->data.get_token_default.request.default_token_value);
}

void sli_zigbee_stack_get_token_info_process_ipc_command(sli_zigbee_ipc_cmd_t *msg)
{
  msg->data.get_token_info.response.result = sli_zigbee_stack_get_token_info(msg->data.get_token_info.request.index,
                                                                             &msg->data.get_token_info.request.tokenInfo);
}

void sli_zigbee_stack_initialize_basic_token_process_ipc_command(sli_zigbee_ipc_cmd_t *msg)
{
  msg->data.initialize_basic_token.response.result = sli_zigbee_stack_initialize_basic_token(msg->data.initialize_basic_token.request.token,
                                                                                             msg->data.initialize_basic_token.request.default_token_value,
                                                                                             msg->data.initialize_basic_token.request.token_size);
}

void sli_zigbee_stack_initialize_counter_token_process_ipc_command(sli_zigbee_ipc_cmd_t *msg)
{
  msg->data.initialize_counter_token.response.result = sli_zigbee_stack_initialize_counter_token(msg->data.initialize_counter_token.request.token,
                                                                                                 msg->data.initialize_counter_token.request.default_token_value,
                                                                                                 msg->data.initialize_counter_token.request.token_size);
}

void sli_zigbee_stack_initialize_index_token_process_ipc_command(sli_zigbee_ipc_cmd_t *msg)
{
  msg->data.initialize_index_token.response.result = sli_zigbee_stack_initialize_index_token(msg->data.initialize_index_token.request.token_base,
                                                                                             msg->data.initialize_index_token.request.default_token_value,
                                                                                             msg->data.initialize_index_token.request.token_size,
                                                                                             msg->data.initialize_index_token.request.token_index_size);
}

void sli_zigbee_stack_set_token_data_process_ipc_command(sli_zigbee_ipc_cmd_t *msg)
{
  msg->data.set_token_data.response.result = sli_zigbee_stack_set_token_data(msg->data.set_token_data.request.token,
                                                                             msg->data.set_token_data.request.index,
                                                                             &msg->data.set_token_data.request.tokenData);
}

void slxi_zigbee_stack_token_manager_get_data_process_ipc_command(sli_zigbee_ipc_cmd_t *msg)
{
  msg->data.token_manager_get_data.response.result = slxi_zigbee_stack_token_manager_get_data(msg->data.token_manager_get_data.request.token,
                                                                                              msg->data.token_manager_get_data.request.data,
                                                                                              msg->data.token_manager_get_data.request.length);
}

// public entrypoints

uint32_t sl_zigbee_get_token_count(void)
{
  sli_zigbee_ipc_cmd_t msg = { 0, };

  sli_zigbee_send_ipc_cmd(sli_zigbee_stack_get_token_count_process_ipc_command, &msg);

  return msg.data.get_token_count.response.result;
}

sl_status_t sl_zigbee_get_token_data(uint32_t token,
                                     uint32_t index,
                                     sl_zigbee_token_data_t *tokenData)
{
  sli_zigbee_ipc_cmd_t msg = { 0, };
  msg.data.get_token_data.request.token = token;
  msg.data.get_token_data.request.index = index;

  if (tokenData != NULL) {
    msg.data.get_token_data.request.tokenData = *tokenData;
  }

  sli_zigbee_send_ipc_cmd(sli_zigbee_stack_get_token_data_process_ipc_command, &msg);

  if (tokenData != NULL) {
    *tokenData = msg.data.get_token_data.request.tokenData;
  }

  return msg.data.get_token_data.response.result;
}

sl_status_t sl_zigbee_get_token_default(uint32_t token,
                                        uint8_t *default_token_value)
{
  sli_zigbee_ipc_cmd_t msg = { 0, };
  msg.data.get_token_default.request.token = token;

  if (default_token_value != NULL) {
    memmove(msg.data.get_token_default.request.default_token_value, default_token_value, sizeof(uint8_t) * MAX_IPC_VEC_ARG_CAPACITY);
  }

  sli_zigbee_send_ipc_cmd(sli_zigbee_stack_get_token_default_process_ipc_command, &msg);

  if (default_token_value != NULL) {
    memmove(default_token_value, msg.data.get_token_default.request.default_token_value, sizeof(uint8_t) * MAX_IPC_VEC_ARG_CAPACITY);
  }

  return msg.data.get_token_default.response.result;
}

sl_status_t sl_zigbee_get_token_info(uint8_t index,
                                     sl_zigbee_token_info_t *tokenInfo)
{
  sli_zigbee_ipc_cmd_t msg = { 0, };
  msg.data.get_token_info.request.index = index;

  if (tokenInfo != NULL) {
    msg.data.get_token_info.request.tokenInfo = *tokenInfo;
  }

  sli_zigbee_send_ipc_cmd(sli_zigbee_stack_get_token_info_process_ipc_command, &msg);

  if (tokenInfo != NULL) {
    *tokenInfo = msg.data.get_token_info.request.tokenInfo;
  }

  return msg.data.get_token_info.response.result;
}

sl_status_t sl_zigbee_initialize_basic_token(uint32_t token,
                                             void *default_token_value,
                                             uint32_t token_size)
{
  sli_zigbee_ipc_cmd_t msg = { 0, };
  msg.data.initialize_basic_token.request.token = token;

  if (token_size > MAX_IPC_VEC_ARG_CAPACITY) {
    assert(false); // "vector default_token_value length exceeds expected maximum
    return msg.data.initialize_basic_token.response.result;
  }

  memmove(msg.data.initialize_basic_token.request.default_token_value, default_token_value, sizeof(uint8_t) * token_size);
  msg.data.initialize_basic_token.request.token_size = token_size;
  sli_zigbee_send_ipc_cmd(sli_zigbee_stack_initialize_basic_token_process_ipc_command, &msg);

  if (token_size > MAX_IPC_VEC_ARG_CAPACITY) {
    assert(false); // "vector default_token_value length exceeds expected maximum
    return msg.data.initialize_basic_token.response.result;
  }

  memmove(default_token_value, msg.data.initialize_basic_token.request.default_token_value, sizeof(uint8_t) * token_size);
  return msg.data.initialize_basic_token.response.result;
}

sl_status_t sl_zigbee_initialize_counter_token(uint32_t token,
                                               void *default_token_value,
                                               uint32_t token_size)
{
  sli_zigbee_ipc_cmd_t msg = { 0, };
  msg.data.initialize_counter_token.request.token = token;

  if (token_size > MAX_IPC_VEC_ARG_CAPACITY) {
    assert(false); // "vector default_token_value length exceeds expected maximum
    return msg.data.initialize_counter_token.response.result;
  }

  memmove(msg.data.initialize_counter_token.request.default_token_value, default_token_value, sizeof(uint8_t) * token_size);
  msg.data.initialize_counter_token.request.token_size = token_size;
  sli_zigbee_send_ipc_cmd(sli_zigbee_stack_initialize_counter_token_process_ipc_command, &msg);

  if (token_size > MAX_IPC_VEC_ARG_CAPACITY) {
    assert(false); // "vector default_token_value length exceeds expected maximum
    return msg.data.initialize_counter_token.response.result;
  }

  memmove(default_token_value, msg.data.initialize_counter_token.request.default_token_value, sizeof(uint8_t) * token_size);
  return msg.data.initialize_counter_token.response.result;
}

sl_status_t sl_zigbee_initialize_index_token(uint32_t token_base,
                                             void *default_token_value,
                                             uint32_t token_size,
                                             uint8_t token_index_size)
{
  sli_zigbee_ipc_cmd_t msg = { 0, };
  msg.data.initialize_index_token.request.token_base = token_base;

  if (token_size > MAX_IPC_VEC_ARG_CAPACITY) {
    assert(false); // "vector default_token_value length exceeds expected maximum
    return msg.data.initialize_index_token.response.result;
  }

  memmove(msg.data.initialize_index_token.request.default_token_value, default_token_value, sizeof(uint8_t) * token_size);
  msg.data.initialize_index_token.request.token_size = token_size;
  msg.data.initialize_index_token.request.token_index_size = token_index_size;
  sli_zigbee_send_ipc_cmd(sli_zigbee_stack_initialize_index_token_process_ipc_command, &msg);

  if (token_size > MAX_IPC_VEC_ARG_CAPACITY) {
    assert(false); // "vector default_token_value length exceeds expected maximum
    return msg.data.initialize_index_token.response.result;
  }

  memmove(default_token_value, msg.data.initialize_index_token.request.default_token_value, sizeof(uint8_t) * token_size);
  return msg.data.initialize_index_token.response.result;
}

sl_status_t sl_zigbee_set_token_data(uint32_t token,
                                     uint32_t index,
                                     sl_zigbee_token_data_t *tokenData)
{
  sli_zigbee_ipc_cmd_t msg = { 0, };
  msg.data.set_token_data.request.token = token;
  msg.data.set_token_data.request.index = index;

  if (tokenData != NULL) {
    msg.data.set_token_data.request.tokenData = *tokenData;
  }

  sli_zigbee_send_ipc_cmd(sli_zigbee_stack_set_token_data_process_ipc_command, &msg);

  if (tokenData != NULL) {
    *tokenData = msg.data.set_token_data.request.tokenData;
  }

  return msg.data.set_token_data.response.result;
}

sl_status_t slx_zigbee_token_manager_get_data(uint32_t token,
                                              void *data,
                                              uint32_t length)
{
  sli_zigbee_ipc_cmd_t msg = { 0, };
  msg.data.token_manager_get_data.request.token = token;

  if (length > MAX_IPC_TOKEN_MANAGER_DATA_LENGTH_ARG_CAPACITY) {
    assert(false); // "vector data length exceeds expected maximum
    return msg.data.token_manager_get_data.response.result;
  }

  memmove(msg.data.token_manager_get_data.request.data, data, sizeof(uint8_t) * length);
  msg.data.token_manager_get_data.request.length = length;
  sli_zigbee_send_ipc_cmd(slxi_zigbee_stack_token_manager_get_data_process_ipc_command, &msg);

  if (length > MAX_IPC_TOKEN_MANAGER_DATA_LENGTH_ARG_CAPACITY) {
    assert(false); // "vector data length exceeds expected maximum
    return msg.data.token_manager_get_data.response.result;
  }

  memmove(data, msg.data.token_manager_get_data.request.data, sizeof(uint8_t) * length);
  return msg.data.token_manager_get_data.response.result;
}
