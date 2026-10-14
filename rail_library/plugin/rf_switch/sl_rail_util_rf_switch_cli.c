/***************************************************************************//**
 * @file
 * @brief RAIL Test CLI for external RF switch configuration.
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * SPDX-License-Identifier: Zlib
 *
 ******************************************************************************/

#include "sl_cli.h"
#include "response_print.h"
#include "sl_rail.h"
#include "sl_rail_ble.h"
#include "sl_rail_util_rf_switch.h"

static sl_rail_rf_switch_config_t cliRfSwitchConfig;

void CI_setCsAntGpioPattern(sl_cli_command_arg_t *args)
{
#if SL_RAIL_SUPPORTS_RF_SWITCH
  if (!sl_rail_util_rf_switch_config_allowed()) {
    responsePrintError(sl_cli_get_command_string(args, 0), 0x01, "CS must be deinited first.");
    return;
  }

  uint8_t count = (uint8_t)sl_cli_get_argument_count(args);
  if (count > SL_RAIL_BLE_CS_MAX_ANTENNAS) {
    responsePrintError(sl_cli_get_command_string(args, 0), 0x01, "Too many pattern entries.");
    return;
  }
  for (uint8_t i = 0U; i < count; i++) {
    uint8_t pattern = sl_cli_get_argument_uint8(args, i);
    // bit0 drives the first control pin, bit1 the second: only two pins.
    if (pattern > 0x3U) {
      responsePrintError(sl_cli_get_command_string(args, 0), 0x01, "Pattern entry out of range (0-3).");
      return;
    }
    cliRfSwitchConfig.antenna_gpio_pattern[i] = pattern;
  }
  // Default any unspecified antennas to the natural binary encoding.
  for (uint8_t i = count; i < SL_RAIL_BLE_CS_MAX_ANTENNAS; i++) {
    cliRfSwitchConfig.antenna_gpio_pattern[i] = i;
  }
  cliRfSwitchConfig.use_antenna_gpio_pattern = true;

  // Apply the (accumulated) RF switch config; preserves any VDD set via
  // setCsRfSwitch.
  sl_rail_status_t status = sl_rail_config_rf_switch(SL_RAIL_EFR32_HANDLE,
                                                     &cliRfSwitchConfig);
  if (status != SL_RAIL_STATUS_NO_ERROR) {
    responsePrintError(sl_cli_get_command_string(args, 0), 0x01, "Unable to configure RF switch antenna pattern.");
    return;
  }
  responsePrint(sl_cli_get_command_string(args, 0), "Status:Success");
#else
  responsePrintError(sl_cli_get_command_string(args, 0), 0x01, "RF switch not supported.");
#endif
}

void CI_setCsRfSwitch(sl_cli_command_arg_t *args)
{
#if SL_RAIL_SUPPORTS_RF_SWITCH
  if (!sl_rail_util_rf_switch_config_allowed()) {
    responsePrintError(sl_cli_get_command_string(args, 0), 0x01, "CS must be deinited first.");
    return;
  }

  // Update VDD in the persistent config, preserving any antenna pattern
  // previously set via setCsAntGpioPattern.
  cliRfSwitchConfig.vdd_enable =
    (sl_cli_get_argument_uint8(args, 0) != 0U);
  cliRfSwitchConfig.vdd_pin.gpio_port = 0U;
  cliRfSwitchConfig.vdd_pin.gpio_pin = 0U;
  cliRfSwitchConfig.vdd_settle_time_us =
    SL_RAIL_RF_SWITCH_VDD_SETTLE_TIME_US_DEFAULT;
  cliRfSwitchConfig.vdd_prs_signal =
    SL_RAIL_RF_SWITCH_VDD_PRS_SIGNAL_PAEN_OR_LNAEN;

  if (cliRfSwitchConfig.vdd_enable) {
    if (sl_cli_get_argument_count(args) < 4) {
      responsePrintError(sl_cli_get_command_string(args, 0), 0x01, "VDD requires port, pin, and settle time.");
      return;
    }
    cliRfSwitchConfig.vdd_pin.gpio_port = sl_cli_get_argument_uint8(args, 1);
    cliRfSwitchConfig.vdd_pin.gpio_pin = sl_cli_get_argument_uint8(args, 2);
    if (cliRfSwitchConfig.vdd_pin.gpio_pin > 15U) {
      responsePrintError(sl_cli_get_command_string(args, 0), 0x01, "Invalid VDD GPIO pin.");
      return;
    }
    cliRfSwitchConfig.vdd_settle_time_us = sl_cli_get_argument_uint8(args, 3);
    if (sl_cli_get_argument_count(args) > 4) {
      uint8_t vddPrsSignal = sl_cli_get_argument_uint8(args, 4);
      if (vddPrsSignal > (uint8_t)SL_RAIL_RF_SWITCH_VDD_PRS_SIGNAL_TX_OR_RX_ACTIVE) {
        responsePrintError(sl_cli_get_command_string(args, 0), 0x01, "Invalid VDD PRS signal.");
        return;
      }
      cliRfSwitchConfig.vdd_prs_signal =
        (sl_rail_rf_switch_vdd_prs_signal_t)vddPrsSignal;
    }
  }

  sl_rail_status_t status = sl_rail_config_rf_switch(SL_RAIL_EFR32_HANDLE,
                                                     &cliRfSwitchConfig);
  if (status != SL_RAIL_STATUS_NO_ERROR) {
    responsePrintError(sl_cli_get_command_string(args, 0), 0x01, "Unable to configure RF switch.");
    return;
  }

  responsePrint(sl_cli_get_command_string(args, 0), "Status:Success");
#else
  responsePrintError(sl_cli_get_command_string(args, 0), 0x01, "RF switch not supported.");
#endif
}
