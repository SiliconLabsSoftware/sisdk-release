/***************************************************************************//**
 * @file sli_wisun_task_direct_connect_client_stubs.c
 * @brief Wi-SUN Direct Connect Client stubs
 *******************************************************************************
 * # License
 * <b>Copyright 2021 Silicon Laboratories Inc. www.silabs.com</b>
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

#include "sl_status.h"
#include "sl_wisun_types.h"
#include "sl_wisun_msg_api.h"

// ----------------------------------------------------------------------------------------------------------------------
// REQUESTS - Stubs when DC client library is not linked

void sli_wisun_task_req_start_direct_connect_client(const sl_wisun_msg_start_direct_connect_client_req_t *req,
                                                    sl_wisun_msg_start_direct_connect_client_cnf_t *cnf)
{
  (void)req;

  if (cnf) {
    cnf->header.id = SL_WISUN_MSG_START_DIRECT_CONNECT_CLIENT_CNF_ID;
    cnf->header.length = sizeof(sl_wisun_msg_start_direct_connect_client_cnf_t);
    cnf->body.status = SL_STATUS_NOT_SUPPORTED;
  }
}

void sli_wisun_task_req_start_direct_connect_scan(const sl_wisun_msg_start_direct_connect_scan_req_t *req, 
                                             sl_wisun_msg_start_direct_connect_scan_cnf_t *cnf)
{
  (void)req;
  if (cnf) {
    cnf->header.id = SL_WISUN_MSG_START_DIRECT_CONNECT_SCAN_CNF_ID;
    cnf->header.length = sizeof(sl_wisun_msg_start_direct_connect_scan_cnf_t);
    cnf->body.status = SL_STATUS_NOT_SUPPORTED;
  }
}

void sli_wisun_task_req_stop_direct_connect_scan(const sl_wisun_msg_stop_direct_connect_scan_req_t *req, 
                                                  sl_wisun_msg_stop_direct_connect_scan_cnf_t *cnf)
{
  (void)req;
  if (cnf) {
    cnf->header.id = SL_WISUN_MSG_STOP_DIRECT_CONNECT_SCAN_CNF_ID;
    cnf->header.length = sizeof(sl_wisun_msg_stop_direct_connect_scan_cnf_t);
    cnf->body.status = SL_STATUS_NOT_SUPPORTED;
  }
}

void sli_wisun_task_req_connect_to_direct_connect_server(const sl_wisun_msg_connect_to_direct_connect_server_req_t *req, 
                                                          sl_wisun_msg_connect_to_direct_connect_server_cnf_t *cnf)
{
  (void)req;
  if (cnf) {
    cnf->header.id = SL_WISUN_MSG_CONNECT_TO_DIRECT_CONNECT_SERVER_CNF_ID;
    cnf->header.length = sizeof(sl_wisun_msg_connect_to_direct_connect_server_cnf_t);
    cnf->body.status = SL_STATUS_NOT_SUPPORTED;
  }
}

void sli_wisun_task_req_stop_direct_connect_client(const sl_wisun_msg_stop_direct_connect_client_req_t *req, 
                                                    sl_wisun_msg_stop_direct_connect_client_cnf_t *cnf)
{
  (void)req;
  if (cnf) {
    cnf->header.id = SL_WISUN_MSG_STOP_DIRECT_CONNECT_CLIENT_CNF_ID;
    cnf->header.length = sizeof(sl_wisun_msg_stop_direct_connect_client_cnf_t);
    cnf->body.status = SL_STATUS_NOT_SUPPORTED;
  }
}

// ----------------------------------------------------------------------------------------------------------------------
// INDICATIONS - Stubs when DC client library is not linked

void sli_wisun_task_ind_direct_connect_id_received(const uint8_t *server_eui64, const uint8_t *dc_id)
{
  (void)server_eui64;
  (void)dc_id;
}

void sli_wisun_task_ind_direct_connect_client_state_changed(sl_wisun_dc_client_state_t state, const in6_addr_t *link_local_ipv6)
{
  (void)state;
  (void)link_local_ipv6;
}