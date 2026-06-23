/***************************************************************************//**
 * @file dc_bootstrap_stubs.c
 * @brief Wi-SUN Direct Connect bootstrap / configuration stubs
 *
 * Provided by the wisun_dc_client_stubs SLC component. These strong no-op
 * definitions satisfy references from the base Wi-SUN stack (ws_bootstrap.c,
 * protocol_6lowpan.c) to Direct Connect helpers when no DC implementation
 * component (wisun_dc_client_plugin) is present.
 *
 * When a DC implementation component is selected, SLC links its real
 * library instead of this stubs file, so the strong symbols below are
 * replaced by the real implementations. Only one provider of
 * wisun_dc_client_implementation may be linked at a time.
 *
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

#include <stdint.h>

#include "sl_status.h"
#include "sl_wisun_connection_params_api.h" /* public: defines sl_wisun_connection_params_t */

/*
 * Opaque forward declarations.
 */
struct protocol_interface_info_entry;
struct mcps_data_ind_s;
struct mcps_data_ie_list;

/* wisun_dc_configuration_api.h -------------------------------------- */

void ws_dc_config_init(void)
{
}

int ws_dc_config_store(const sl_wisun_connection_params_t *params)
{
    (void)params;
    return -1;
}

int ws_dc_config_apply(struct protocol_interface_info_entry *cur)
{
    (void)cur;
    return -1;
}

/* dc_bootstrap_fsm.h ------------------------------------------------- */

sl_status_t dc_bootstrap_fsm_init(struct protocol_interface_info_entry *cur)
{
    (void)cur;
    return SL_STATUS_NOT_SUPPORTED;
}

/* dc_bootstrap.h ----------------------------------------------------- */

void dc_bootstrap_pan_control_ind(struct protocol_interface_info_entry *cur,
                                  const struct mcps_data_ind_s *data,
                                  const struct mcps_data_ie_list *ie_ext,
                                  uint8_t message_type)
{
    (void)cur;
    (void)data;
    (void)ie_ext;
    (void)message_type;
}

void dc_bootstrap_pan_control_confirm(struct protocol_interface_info_entry *interface,
                                      uint8_t pan_control_message)
{
    (void)interface;
    (void)pan_control_message;
}
