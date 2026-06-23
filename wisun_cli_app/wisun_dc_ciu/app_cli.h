/***************************************************************************//**
 * @file app_cli.h
 * @brief Direct Connect Control Interface Unit CLI settings header
 *
 * Defines the configuration structure and CLI command handlers for the
 * Direct Connect Control Interface Unit application.
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 * SPDX-License-Identifier: Zlib
 ******************************************************************************/

#ifndef APP_CLI_H
#define APP_CLI_H

// -----------------------------------------------------------------------------
//                                   Includes
// -----------------------------------------------------------------------------

#include <stdint.h>
#include <stdbool.h>
#include "sl_wisun_api.h"
#include "sl_cli.h"

// -----------------------------------------------------------------------------
//                              Macros and Typedefs
// -----------------------------------------------------------------------------

/// DC CIU configuration settings structure
typedef struct {
  /// PHY configuration type (always FAN1.1 for DC)
  uint8_t phy_config_type;
  /// Regulatory domain (EU=3, NA=1, etc.)
  uint8_t regulatory_domain;
  /// Channel plan ID
  uint8_t chan_plan_id;
  /// PHY mode ID
  uint8_t phy_mode_id;
  /// Target DC ID string
  char dc_id[SL_WISUN_DC_ID_LEN];
  /// Pre-shared master key (PMK)
  uint8_t pmk[SL_WISUN_PMK_LEN];
  /// Server UDP port
  uint16_t server_port;
  /// Idle timeout before EM4 in milliseconds (applies to all states)
  uint32_t idle_timeout_ms;
  /// Max scan solicitations
  uint8_t max_scan_solicits;
  /// Max connect solicitations
  uint8_t max_connect_solicits;
} dc_ciu_settings_t;

// -----------------------------------------------------------------------------
//                          Public Variable Declarations
// -----------------------------------------------------------------------------

/// DC CIU configuration settings (global instance)
extern dc_ciu_settings_t dc_ciu_settings;

// -----------------------------------------------------------------------------
//                          Public Function Declarations
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * Initialize the DC CIU settings with defaults.
 *
 * Loads settings from NVM if available, otherwise uses compile-time defaults.
 ******************************************************************************/
void app_cli_init(void);

/***************************************************************************//**
 * Get the current PHY configuration based on settings.
 *
 * @param phy_config Pointer to PHY config structure to populate.
 ******************************************************************************/
void app_cli_get_phy_config(sl_wisun_phy_config_t *phy_config);

/***************************************************************************//**
 * Get the target DC ID based on settings.
 *
 * @param dc_id Pointer to DC ID structure to populate.
 ******************************************************************************/
void app_cli_get_dc_id(sl_wisun_dc_id_t *dc_id);

/***************************************************************************//**
 * Get the PMK from settings.
 *
 * @param pmk Pointer to buffer to copy PMK (must be SL_WISUN_PMK_LEN bytes).
 ******************************************************************************/
void app_cli_get_pmk(uint8_t *pmk);

/***************************************************************************//**
 * Save current settings to NVM.
 *
 * @returns SL_STATUS_OK on success, error code on failure.
 ******************************************************************************/
sl_status_t app_cli_save_settings(void);

/***************************************************************************//**
 * Reset settings to defaults.
 ******************************************************************************/
void app_cli_reset_settings(void);

// -----------------------------------------------------------------------------
//                          CLI Command Handlers
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * CLI command: dc get [setting]
 *
 * Get one or all DC CIU settings.
 *
 * @param arguments CLI argument array.
 ******************************************************************************/
void app_cli_get_cmd(sl_cli_command_arg_t *arguments);

/***************************************************************************//**
 * CLI command: dc set <setting> <value>
 *
 * Set a DC CIU setting.
 *
 * @param arguments CLI argument array.
 ******************************************************************************/
void app_cli_set_cmd(sl_cli_command_arg_t *arguments);

/***************************************************************************//**
 * CLI command: dc save
 *
 * Save current settings to NVM.
 *
 * @param arguments CLI argument array (unused).
 ******************************************************************************/
void app_cli_save_cmd(sl_cli_command_arg_t *arguments);

/***************************************************************************//**
 * CLI command: dc reset
 *
 * Reset settings to defaults.
 *
 * @param arguments CLI argument array (unused).
 ******************************************************************************/
void app_cli_reset_cmd(sl_cli_command_arg_t *arguments);

/***************************************************************************//**
 * CLI command: dc status
 *
 * Print current application status.
 *
 * @param arguments CLI argument array (unused).
 ******************************************************************************/
void app_cli_status_cmd(sl_cli_command_arg_t *arguments);

#endif  // APP_CLI_H
