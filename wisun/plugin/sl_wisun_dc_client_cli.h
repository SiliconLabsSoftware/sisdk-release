/***************************************************************************//**
 * @file sl_wisun_dc_client_cli.h
 * @brief CLI helpers shared with the Wi-SUN Direct Connect client CLI plugin
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

#ifndef SL_WISUN_DC_CLIENT_CLI_H
#define SL_WISUN_DC_CLIENT_CLI_H

#include <stdint.h>
#include "sl_status.h"

/**
 * PSA key ID holding the Direct Connect PMK currently installed in the PSA
 * key store by app_import_direct_connect_pmk(). Set to MBEDTLS_SVC_KEY_ID_INIT
 * when no PMK has been imported yet (or the most recent import failed).
 *
 * Owned by the Wi-SUN CLI app (defined in app/wisun_soc_cli/app_cli.c) and
 * shared with the Direct Connect client CLI plugin. Callers must not modify
 * this value directly; use app_import_direct_connect_pmk() to refresh it.
 */
extern uint32_t app_direct_connect_pmk_key_id;

/**
 * (Re-)import the Direct Connect PMK from app_settings_wisun.direct_connect_pmk
 * into the PSA key store and install it in the stack via
 * sl_wisun_set_direct_connect_pmk(). Destroys any previously-imported PMK
 * first and updates app_direct_connect_pmk_key_id. Prints diagnostics on
 * failure; intended for CLI command handlers (Wi-SUN CLI mutex held).
 *
 * @return SL_STATUS_OK on success, an error status otherwise.
 */
sl_status_t app_import_direct_connect_pmk(void);

#endif /* SL_WISUN_DC_CLIENT_CLI_H */
