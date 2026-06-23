/***************************************************************************//**
 * @file sl_zigbee_token_ipc_command_messages.h
 * @brief defines structured format for 'sl_zigbee_token' ipc messages
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
#ifndef SL_ZIGBEE_TOKEN_IPC_COMMAND_MESSAGES_H
#define SL_ZIGBEE_TOKEN_IPC_COMMAND_MESSAGES_H

#include "stack/include/sl_zigbee_token.h"
#include "stack/internal/inc/sl_zigbee_token_internal_def.h"

typedef struct {
  uint32_t result;
} sli_zigbee_stack_get_token_count_ipc_rsp_t;

typedef struct {
  sli_zigbee_stack_get_token_count_ipc_rsp_t response;
} sli_zigbee_stack_get_token_count_ipc_msg_t;

typedef struct {
  uint32_t token;
  uint32_t index;
  sl_zigbee_token_data_t tokenData;
} sli_zigbee_stack_get_token_data_ipc_req_t;

typedef struct {
  sl_status_t result;
} sli_zigbee_stack_get_token_data_ipc_rsp_t;

typedef struct {
  sli_zigbee_stack_get_token_data_ipc_req_t request;
  sli_zigbee_stack_get_token_data_ipc_rsp_t response;
} sli_zigbee_stack_get_token_data_ipc_msg_t;

typedef struct {
  uint32_t token;
  uint8_t default_token_value[MAX_IPC_VEC_ARG_CAPACITY];
} sli_zigbee_stack_get_token_default_ipc_req_t;

typedef struct {
  sl_status_t result;
} sli_zigbee_stack_get_token_default_ipc_rsp_t;

typedef struct {
  sli_zigbee_stack_get_token_default_ipc_req_t request;
  sli_zigbee_stack_get_token_default_ipc_rsp_t response;
} sli_zigbee_stack_get_token_default_ipc_msg_t;

typedef struct {
  uint8_t index;
  sl_zigbee_token_info_t tokenInfo;
} sli_zigbee_stack_get_token_info_ipc_req_t;

typedef struct {
  sl_status_t result;
} sli_zigbee_stack_get_token_info_ipc_rsp_t;

typedef struct {
  sli_zigbee_stack_get_token_info_ipc_req_t request;
  sli_zigbee_stack_get_token_info_ipc_rsp_t response;
} sli_zigbee_stack_get_token_info_ipc_msg_t;

typedef struct {
  uint32_t token;
  uint8_t default_token_value[MAX_IPC_VEC_ARG_CAPACITY];
  uint32_t token_size;
} sli_zigbee_stack_initialize_basic_token_ipc_req_t;

typedef struct {
  sl_status_t result;
} sli_zigbee_stack_initialize_basic_token_ipc_rsp_t;

typedef struct {
  sli_zigbee_stack_initialize_basic_token_ipc_req_t request;
  sli_zigbee_stack_initialize_basic_token_ipc_rsp_t response;
} sli_zigbee_stack_initialize_basic_token_ipc_msg_t;

typedef struct {
  uint32_t token;
  uint8_t default_token_value[MAX_IPC_VEC_ARG_CAPACITY];
  uint32_t token_size;
} sli_zigbee_stack_initialize_counter_token_ipc_req_t;

typedef struct {
  sl_status_t result;
} sli_zigbee_stack_initialize_counter_token_ipc_rsp_t;

typedef struct {
  sli_zigbee_stack_initialize_counter_token_ipc_req_t request;
  sli_zigbee_stack_initialize_counter_token_ipc_rsp_t response;
} sli_zigbee_stack_initialize_counter_token_ipc_msg_t;

typedef struct {
  uint32_t token_base;
  uint8_t default_token_value[MAX_IPC_VEC_ARG_CAPACITY];
  uint32_t token_size;
  uint8_t token_index_size;
} sli_zigbee_stack_initialize_index_token_ipc_req_t;

typedef struct {
  sl_status_t result;
} sli_zigbee_stack_initialize_index_token_ipc_rsp_t;

typedef struct {
  sli_zigbee_stack_initialize_index_token_ipc_req_t request;
  sli_zigbee_stack_initialize_index_token_ipc_rsp_t response;
} sli_zigbee_stack_initialize_index_token_ipc_msg_t;

typedef struct {
  uint32_t token;
  uint32_t index;
  sl_zigbee_token_data_t tokenData;
} sli_zigbee_stack_set_token_data_ipc_req_t;

typedef struct {
  sl_status_t result;
} sli_zigbee_stack_set_token_data_ipc_rsp_t;

typedef struct {
  sli_zigbee_stack_set_token_data_ipc_req_t request;
  sli_zigbee_stack_set_token_data_ipc_rsp_t response;
} sli_zigbee_stack_set_token_data_ipc_msg_t;

typedef struct {
  uint32_t token;
  uint8_t data[MAX_IPC_TOKEN_MANAGER_DATA_LENGTH_ARG_CAPACITY];
  uint32_t length;
} slxi_zigbee_stack_token_manager_get_data_ipc_req_t;

typedef struct {
  sl_status_t result;
} slxi_zigbee_stack_token_manager_get_data_ipc_rsp_t;

typedef struct {
  slxi_zigbee_stack_token_manager_get_data_ipc_req_t request;
  slxi_zigbee_stack_token_manager_get_data_ipc_rsp_t response;
} slxi_zigbee_stack_token_manager_get_data_ipc_msg_t;

#endif // SL_ZIGBEE_TOKEN_IPC_COMMAND_MESSAGES_H
