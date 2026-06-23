/***************************************************************************//**
 * @brief Adaptation layer between host application and BGAPI Service
 *******************************************************************************
 * # License
 * <b>Copyright 2025 Silicon Laboratories Inc. www.silabs.com</b>
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

#include "sl_bgapi_service_api.h"
#include "sl_bt_ncp_host.h"
#include "sl_status.h"

static sl_bgapi_msg_t _sli_bgapi_cmd_msg;
static sl_bgapi_msg_t _sli_bgapi_rsp_msg;
sl_bgapi_msg_t *sl_bgapi_cmd_msg = &_sli_bgapi_cmd_msg;
sl_bgapi_msg_t *sl_bgapi_rsp_msg = &_sli_bgapi_rsp_msg;

void sl_bgapi_host_handle_command()
{
  // Output the packet that has been filled in sl_bgapi_cmd_msg
  sl_bt_api_output(SL_BGAPI_MSG_HEADER_LEN + SL_BGAPI_MSG_LEN(sl_bgapi_cmd_msg->header), (uint8_t*)sl_bgapi_cmd_msg);

  // Synchronously wait for a response. We have received a response if a
  // non-NULL pointer is returned.
  while (1) {
    sl_bgapi_msg_t* p = (sl_bgapi_msg_t*)sli_wait_for_bgapi_message((sl_bt_msg_t*)sl_bgapi_rsp_msg);
    if (p) {
      return;
    }
  }
}

void sl_bgapi_host_handle_command_noresponse()
{
  // Output the packet that has been filled in sl_bgapi_cmd_msg
  sl_bt_api_output(SL_BGAPI_MSG_HEADER_LEN + SL_BGAPI_MSG_LEN(sl_bgapi_cmd_msg->header), (uint8_t*)sl_bgapi_cmd_msg);
}
