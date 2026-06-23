/***************************************************************************//**
 * @file ws_ie_lib_stubs.c
 * @brief Wi-SUN IE stubs
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

 #include "stdbool.h"
 #include "sl_status.h"
 
 typedef struct ws_utt_ie {
   // empty stub
   int dummy;
 } ws_utt_ie_t;
 
 typedef struct sli_dc_client_ctx_t {
   // empty stub
   int dummy;
 } sli_dc_client_ctx_t;

 sl_status_t sl_ws_wh_dc_id_write(uint8_t *data, uint16_t length, const uint8_t *dc_id)
{
  (void)data;
  (void)length;
  (void)dc_id;
  return SL_STATUS_NOT_SUPPORTED;
}

bool sl_ws_wh_dc_id_read(const uint8_t *data, uint16_t length, uint8_t *dc_id)
{
  (void)data;
  (void)length;
  (void)dc_id;
  return false;
}

bool sl_ws_wh_utt_read(const uint8_t *data, uint16_t length, struct ws_utt_ie *sl_utt_ie)
{
  (void)data;
  (void)length;
  (void)sl_utt_ie;
  return false;
}