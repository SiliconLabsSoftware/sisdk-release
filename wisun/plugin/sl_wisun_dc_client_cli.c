/***************************************************************************//**
 * @file sl_wisun_dc_client_cli.c
 * @brief CLI commands for the Wi-SUN Direct Connect client
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

#include <stdio.h>
#include <string.h>
#include <inttypes.h>

#include "sl_cli.h"
#include "sl_status.h"
#include "sl_wisun_api.h"
#include "sl_wisun_cli_core.h"
#include "sl_wisun_cli_util.h"

#include "app_settings.h"
#include "sl_wisun_dc_client_cli.h"

void app_wisun_start_direct_connect_client(sl_cli_command_arg_t *arguments)
{
  sl_status_t status;
  sl_wisun_phy_config_type_t phy_type;
  sl_wisun_phy_config_t phy_config;

  app_wisun_cli_mutex_lock();

  if (sl_cli_get_argument_count(arguments) > 0) {
    phy_type = (sl_wisun_phy_config_type_t)sl_cli_get_argument_uint32(arguments, 0);
  } else {
    printf("[Failed: missing phy type]\r\n");
    goto cleanup;
  }

  switch (phy_type) {
    case SL_WISUN_PHY_CONFIG_FAN10:
      phy_config.type = SL_WISUN_PHY_CONFIG_FAN10;
      phy_config.config.fan10.reg_domain = app_settings_wisun.regulatory_domain;
      phy_config.config.fan10.op_class = app_settings_wisun.operating_class;
      phy_config.config.fan10.op_mode = app_settings_wisun.operating_mode;
      phy_config.config.fan10.fec = app_settings_wisun.fec;
      break;
    case SL_WISUN_PHY_CONFIG_FAN11:
      phy_config.type = SL_WISUN_PHY_CONFIG_FAN11;
      phy_config.config.fan11.reg_domain = app_settings_wisun.regulatory_domain;
      phy_config.config.fan11.chan_plan_id = app_settings_wisun.chan_plan_id;
      phy_config.config.fan11.phy_mode_id = app_settings_wisun.phy_mode_id;
      break;
    case SL_WISUN_PHY_CONFIG_EXPLICIT:
      phy_config.type = SL_WISUN_PHY_CONFIG_EXPLICIT;
      phy_config.config.explicit_plan.ch0_frequency_khz = app_settings_wisun.ch0_frequency;
      phy_config.config.explicit_plan.number_of_channels = app_settings_wisun.number_of_channels;
      break;
    default:
      printf("[Failed: unsupported phy type: %u]\r\n", phy_type);
      goto cleanup;
  }

  status = sl_wisun_start_direct_connect_client(&phy_config);
  if (status != SL_STATUS_OK) {
    printf("[Failed: unable to start Direct Connect client: %"PRIu32"]\r\n", status);
    goto cleanup;
  }

  printf("[Direct Connect client has started]\r\n");

cleanup:
  app_wisun_cli_mutex_unlock();
}

void app_wisun_stop_direct_connect_client(sl_cli_command_arg_t *arguments)
{
  sl_status_t status;
  (void)arguments;

  app_wisun_cli_mutex_lock();

  status = sl_wisun_stop_direct_connect_client();
  if (status != SL_STATUS_OK) {
    printf("[Failed: unable to stop Direct Connect client: %"PRIu32"]\r\n", status);
    goto cleanup;
  }

  printf("[Direct Connect client has stopped]\r\n");

cleanup:
  app_wisun_cli_mutex_unlock();
}

void app_wisun_direct_connect_scan(sl_cli_command_arg_t *arguments)
{
  sl_status_t status;
  uint8_t max_solicits_count = 0;
  sl_wisun_dc_id_t dc_id = {0};

  app_wisun_cli_mutex_lock();

  if (sl_cli_get_argument_count(arguments) == 2) {
    strncpy((char *)dc_id.id, sl_cli_get_argument_string(arguments, 0), SL_WISUN_DC_ID_LEN - 1);
    max_solicits_count = sl_cli_get_argument_uint8(arguments, 1);
  } else {
    printf("[Failed: missing parameters]\r\n");
    goto cleanup;
  }

  status = sl_wisun_start_direct_connect_scan(&dc_id, max_solicits_count);
  if (status != SL_STATUS_OK) {
    printf("[Failed: unable to start Direct Connect client scanning: %"PRIu32"]\r\n", status);
    goto cleanup;
  }

  printf("[Direct Connect client is scanning using DC_ID: %s]\r\n", (char *) dc_id.id);

cleanup:
  app_wisun_cli_mutex_unlock();
}

void app_wisun_stop_direct_connect_scan(sl_cli_command_arg_t *arguments)
{
  sl_status_t status;
  (void)arguments;

  app_wisun_cli_mutex_lock();

  status = sl_wisun_stop_direct_connect_scan();
  if (status != SL_STATUS_OK) {
    printf("[Failed: unable to stop Direct Connect client scanning: %"PRIu32"]\r\n", status);
    goto cleanup;
  }

  printf("[Direct Connect client has stopped scanning]\r\n");

cleanup:
  app_wisun_cli_mutex_unlock();
}

void app_wisun_connect_to_direct_connect_server(sl_cli_command_arg_t *arguments)
{
  uint32_t ret = 0;
  sl_status_t status = SL_STATUS_OK;
  uint8_t max_solicits_count = 0;
  sl_wisun_mac_address_t mac_address = {0};
  char mac_str[24];

  app_wisun_cli_mutex_lock();

  if (sl_cli_get_argument_count(arguments) == 2) {
    ret = app_util_get_mac_address(&mac_address, sl_cli_get_argument_string(arguments, 0));
    if (ret != SL_STATUS_OK) {
      printf("[Failed: invalid MAC address: %s]\r\n", sl_cli_get_argument_string(arguments, 0));
      goto cleanup;
    }
    max_solicits_count = sl_cli_get_argument_uint8(arguments, 1);
  } else {
    printf("[Failed: missing parameters]\r\n");
    goto cleanup;
  }

  status = app_import_direct_connect_pmk();
  if (status != SL_STATUS_OK) {
    goto cleanup;
  }

  status = sl_wisun_connect_to_direct_connect_server(&mac_address, app_direct_connect_pmk_key_id, max_solicits_count);
  if (status != SL_STATUS_OK) {
    printf("[Failed: unable to connect to Direct Connect server: %"PRIu32"]\r\n", status);
    goto cleanup;
  }

  app_util_get_mac_address_string(mac_str, &mac_address);
  printf("[Connecting to Direct Connect server %s]\r\n", mac_str);

cleanup:
  app_wisun_cli_mutex_unlock();
}
