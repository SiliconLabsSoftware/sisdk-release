/***************************************************************************//**
 * @file app_cli.c
 * @brief Direct Connect Control Interface Unit CLI settings implementation
 *
 * Implements CLI commands for configuring and controlling the Direct Connect
 * Control Interface Unit application.
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 * SPDX-License-Identifier: Zlib
 ******************************************************************************/

// -----------------------------------------------------------------------------
//                                   Includes
// -----------------------------------------------------------------------------

#include "app_cli.h"
#include "sl_wisun_api.h"
#include "sl_cli.h"
#include "nvm3.h"
#include "nvm3_default.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// -----------------------------------------------------------------------------
//                              Macros and Typedefs
// -----------------------------------------------------------------------------

/// NVM3 key for DC CIU settings
#define DC_CIU_NVM3_KEY_SETTINGS   (NVM3_KEY_MIN)

// -----------------------------------------------------------------------------
//                          Default Settings
// -----------------------------------------------------------------------------

/// Default PHY: FAN1.1, EU, channel plan 33, PHY mode 3
#define DEFAULT_PHY_CONFIG_TYPE       SL_WISUN_PHY_CONFIG_FAN11
#define DEFAULT_REGULATORY_DOMAIN     SL_WISUN_REGULATORY_DOMAIN_EU
#define DEFAULT_CHAN_PLAN_ID          33
#define DEFAULT_PHY_MODE_ID           3

/// Default DC ID
#define DEFAULT_DC_ID                 "DC_ID_DEFAULT"

/// Default PMK (32 bytes)
static const uint8_t default_pmk[SL_WISUN_PMK_LEN] = {
  0x34, 0xba, 0x32, 0x26, 0xa0, 0xb2, 0xad, 0x66,
  0x7c, 0x9f, 0x66, 0x02, 0xe5, 0xdb, 0x75, 0x77,
  0xdd, 0xbd, 0x5d, 0x2b, 0x34, 0x3a, 0x93, 0x06,
  0x2b, 0x90, 0xc0, 0x7b, 0xe2, 0x8e, 0x4e, 0x54
};

/// Default server port
#define DEFAULT_SERVER_PORT           1234

/// Default idle timeout before EM4 (60 seconds)
#define DEFAULT_IDLE_TIMEOUT_MS       60000

/// Default max scan solicitations
#define DEFAULT_MAX_SCAN_SOLICITS     10

/// Default max connect solicitations
#define DEFAULT_MAX_CONNECT_SOLICITS  5

// -----------------------------------------------------------------------------
//                                Global Variables
// -----------------------------------------------------------------------------

/// DC CIU settings instance
dc_ciu_settings_t dc_ciu_settings;

// -----------------------------------------------------------------------------
//                          External Function Declarations
// -----------------------------------------------------------------------------

/// External function to get current state (from app.c)
extern int app_get_current_state(void);

/// External function to get state name string (from app.c)
extern const char *app_get_state_name(int state);

/// External function to reset idle timer on CLI activity (from app.c)
extern void app_reset_idle_timer(void);

// -----------------------------------------------------------------------------
//                          Utility/Helper Functions
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * Print bytes as hex string.
 ******************************************************************************/
static void print_hex_bytes(const uint8_t *data, size_t len)
{
  for (size_t i = 0; i < len; i++) {
    printf("%02x", data[i]);
  }
}

/***************************************************************************//**
 * Get regulatory domain string.
 ******************************************************************************/
static const char *get_reg_domain_str(uint8_t domain)
{
  switch (domain) {
    case SL_WISUN_REGULATORY_DOMAIN_WW: return "WW";
    case SL_WISUN_REGULATORY_DOMAIN_NA: return "NA";
    case SL_WISUN_REGULATORY_DOMAIN_JP: return "JP";
    case SL_WISUN_REGULATORY_DOMAIN_EU: return "EU";
    case SL_WISUN_REGULATORY_DOMAIN_CN: return "CN";
    case SL_WISUN_REGULATORY_DOMAIN_IN: return "IN";
    case SL_WISUN_REGULATORY_DOMAIN_MX: return "MX";
    case SL_WISUN_REGULATORY_DOMAIN_BZ: return "BZ";
    case SL_WISUN_REGULATORY_DOMAIN_AZ: return "AZ";
    case SL_WISUN_REGULATORY_DOMAIN_KR: return "KR";
    case SL_WISUN_REGULATORY_DOMAIN_PH: return "PH";
    case SL_WISUN_REGULATORY_DOMAIN_MY: return "MY";
    case SL_WISUN_REGULATORY_DOMAIN_HK: return "HK";
    case SL_WISUN_REGULATORY_DOMAIN_SG: return "SG";
    case SL_WISUN_REGULATORY_DOMAIN_TH: return "TH";
    case SL_WISUN_REGULATORY_DOMAIN_VN: return "VN";
    default:                            return "??";
  }
}

/***************************************************************************//**
 * Parse regulatory domain string or number.
 *
 * @param str Input string (e.g., "EU", "3", "NA", "1").
 * @returns Domain value on success, -1 on error.
 ******************************************************************************/
static int parse_reg_domain(const char *str)
{
  // Try as number first
  char *endptr;
  long val = strtol(str, &endptr, 10);
  if (*endptr == '\0' && val >= 0 && val <= 15) {
    return (int)val;
  }

  // Try as string
  if (strcmp(str, "WW") == 0) return SL_WISUN_REGULATORY_DOMAIN_WW;
  if (strcmp(str, "NA") == 0) return SL_WISUN_REGULATORY_DOMAIN_NA;
  if (strcmp(str, "JP") == 0) return SL_WISUN_REGULATORY_DOMAIN_JP;
  if (strcmp(str, "EU") == 0) return SL_WISUN_REGULATORY_DOMAIN_EU;
  if (strcmp(str, "CN") == 0) return SL_WISUN_REGULATORY_DOMAIN_CN;
  if (strcmp(str, "IN") == 0) return SL_WISUN_REGULATORY_DOMAIN_IN;
  if (strcmp(str, "MX") == 0) return SL_WISUN_REGULATORY_DOMAIN_MX;
  if (strcmp(str, "BZ") == 0) return SL_WISUN_REGULATORY_DOMAIN_BZ;
  if (strcmp(str, "AZ") == 0) return SL_WISUN_REGULATORY_DOMAIN_AZ;
  if (strcmp(str, "KR") == 0) return SL_WISUN_REGULATORY_DOMAIN_KR;
  if (strcmp(str, "PH") == 0) return SL_WISUN_REGULATORY_DOMAIN_PH;
  if (strcmp(str, "MY") == 0) return SL_WISUN_REGULATORY_DOMAIN_MY;
  if (strcmp(str, "HK") == 0) return SL_WISUN_REGULATORY_DOMAIN_HK;
  if (strcmp(str, "SG") == 0) return SL_WISUN_REGULATORY_DOMAIN_SG;
  if (strcmp(str, "TH") == 0) return SL_WISUN_REGULATORY_DOMAIN_TH;
  if (strcmp(str, "VN") == 0) return SL_WISUN_REGULATORY_DOMAIN_VN;

  return -1;
}

/***************************************************************************//**
 * Parse hex string to bytes.
 *
 * @param hex_str Hex string (e.g., "34ba3226a0b2ad66...").
 * @param out Output buffer.
 * @param len Expected number of bytes.
 * @returns true on success, false on error.
 ******************************************************************************/
static bool parse_hex_string(const char *hex_str, uint8_t *out, size_t len)
{
  size_t str_len = strlen(hex_str);

  // Must be exactly 2*len hex characters
  if (str_len != len * 2) {
    printf("Error: PMK must be %zu hex characters (got %zu)\n",
           len * 2, str_len);
    return false;
  }

  for (size_t i = 0; i < len; i++) {
    char byte_str[3] = { hex_str[i * 2], hex_str[i * 2 + 1], '\0' };
    char *endptr;
    long val = strtol(byte_str, &endptr, 16);
    if (*endptr != '\0') {
      printf("Error: Invalid hex character in PMK\n");
      return false;
    }
    out[i] = (uint8_t)val;
  }

  return true;
}

// -----------------------------------------------------------------------------
//                          Settings Print Functions
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * Print help for available settings.
 ******************************************************************************/
static void print_settings_help(void)
{
  printf("Available settings:\n");
  printf("  regulatory_domain    - Regulatory domain (0-15 or WW/NA/JP/EU/...)\n");
  printf("  chan_plan_id         - FAN1.1 channel plan ID\n");
  printf("  phy_mode_id          - FAN1.1 PHY mode ID\n");
  printf("  dc_id                - Target DC ID string\n");
  printf("  pmk                  - Pre-shared master key (64 hex chars)\n");
  printf("  server_port          - UDP server port\n");
  printf("  idle_timeout_ms      - Idle timeout before EM4 (ms)\n");
  printf("  max_scan_solicits    - Max scan solicitations\n");
  printf("  max_connect_solicits - Max connect solicitations\n");
}

/***************************************************************************//**
 * Print all settings.
 ******************************************************************************/
static void print_all_settings(void)
{
  printf("=====================================\n");
  printf("  DC CIU Settings\n");
  printf("=====================================\n");
  printf("PHY Configuration:\n");
  printf("  regulatory_domain:     %u (%s)\n",
         dc_ciu_settings.regulatory_domain,
         get_reg_domain_str(dc_ciu_settings.regulatory_domain));
  printf("  chan_plan_id:          %u\n", dc_ciu_settings.chan_plan_id);
  printf("  phy_mode_id:           %u\n", dc_ciu_settings.phy_mode_id);
  printf("\nDirect Connect:\n");
  printf("  dc_id:                 %s\n", dc_ciu_settings.dc_id);
  printf("  pmk:                   ");
  print_hex_bytes(dc_ciu_settings.pmk, SL_WISUN_PMK_LEN);
  printf("\n");
  printf("\nNetwork:\n");
  printf("  server_port:           %u\n", dc_ciu_settings.server_port);
  printf("\nTimeout:\n");
  printf("  idle_timeout_ms:       %lu\n",
         (unsigned long)dc_ciu_settings.idle_timeout_ms);
  printf("\nSolicitations:\n");
  printf("  max_scan_solicits:     %u\n", dc_ciu_settings.max_scan_solicits);
  printf("  max_connect_solicits:  %u\n", dc_ciu_settings.max_connect_solicits);
  printf("=====================================\n");
}

/***************************************************************************//**
 * Print a single setting.
 ******************************************************************************/
static void print_setting(const char *name)
{
  if (strcmp(name, "help") == 0 || strcmp(name, "?") == 0) {
    print_settings_help();
  } else if (strcmp(name, "regulatory_domain") == 0) {
    printf("regulatory_domain: %u (%s)\n",
           dc_ciu_settings.regulatory_domain,
           get_reg_domain_str(dc_ciu_settings.regulatory_domain));
  } else if (strcmp(name, "chan_plan_id") == 0) {
    printf("chan_plan_id: %u\n", dc_ciu_settings.chan_plan_id);
  } else if (strcmp(name, "phy_mode_id") == 0) {
    printf("phy_mode_id: %u\n", dc_ciu_settings.phy_mode_id);
  } else if (strcmp(name, "dc_id") == 0) {
    printf("dc_id: %s\n", dc_ciu_settings.dc_id);
  } else if (strcmp(name, "pmk") == 0) {
    printf("pmk: ");
    print_hex_bytes(dc_ciu_settings.pmk, SL_WISUN_PMK_LEN);
    printf("\n");
  } else if (strcmp(name, "server_port") == 0) {
    printf("server_port: %u\n", dc_ciu_settings.server_port);
  } else if (strcmp(name, "idle_timeout_ms") == 0) {
    printf("idle_timeout_ms: %lu\n",
           (unsigned long)dc_ciu_settings.idle_timeout_ms);
  } else if (strcmp(name, "max_scan_solicits") == 0) {
    printf("max_scan_solicits: %u\n", dc_ciu_settings.max_scan_solicits);
  } else if (strcmp(name, "max_connect_solicits") == 0) {
    printf("max_connect_solicits: %u\n", dc_ciu_settings.max_connect_solicits);
  } else {
    printf("Unknown setting: %s\n", name);
    print_settings_help();
  }
}

// -----------------------------------------------------------------------------
//                          Settings Setter
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * Set a setting value.
 *
 * @param name The setting name.
 * @param value The value string.
 * @returns true on success, false on error.
 ******************************************************************************/
static bool set_setting(const char *name, const char *value)
{
  if (strcmp(name, "regulatory_domain") == 0) {
    int domain = parse_reg_domain(value);
    if (domain >= 0) {
      dc_ciu_settings.regulatory_domain = (uint8_t)domain;
      return true;
    }
    return false;
  } else if (strcmp(name, "chan_plan_id") == 0) {
    dc_ciu_settings.chan_plan_id = (uint8_t)atoi(value);
    return true;
  } else if (strcmp(name, "phy_mode_id") == 0) {
    dc_ciu_settings.phy_mode_id = (uint8_t)atoi(value);
    return true;
  } else if (strcmp(name, "dc_id") == 0) {
    memset(dc_ciu_settings.dc_id, 0, sizeof(dc_ciu_settings.dc_id));
    strncpy(dc_ciu_settings.dc_id, value, SL_WISUN_DC_ID_LEN);
    return true;
  } else if (strcmp(name, "pmk") == 0) {
    return parse_hex_string(value, dc_ciu_settings.pmk, SL_WISUN_PMK_LEN);
  } else if (strcmp(name, "server_port") == 0) {
    dc_ciu_settings.server_port = (uint16_t)atoi(value);
    return true;
  } else if (strcmp(name, "idle_timeout_ms") == 0) {
    dc_ciu_settings.idle_timeout_ms = (uint32_t)atol(value);
    return true;
  } else if (strcmp(name, "max_scan_solicits") == 0) {
    dc_ciu_settings.max_scan_solicits = (uint8_t)atoi(value);
    return true;
  } else if (strcmp(name, "max_connect_solicits") == 0) {
    dc_ciu_settings.max_connect_solicits = (uint8_t)atoi(value);
    return true;
  }

  return false;
}

// -----------------------------------------------------------------------------
//                          Public Settings API
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * Reset settings to defaults.
 ******************************************************************************/
void app_cli_reset_settings(void)
{
  dc_ciu_settings.phy_config_type = DEFAULT_PHY_CONFIG_TYPE;
  dc_ciu_settings.regulatory_domain = DEFAULT_REGULATORY_DOMAIN;
  dc_ciu_settings.chan_plan_id = DEFAULT_CHAN_PLAN_ID;
  dc_ciu_settings.phy_mode_id = DEFAULT_PHY_MODE_ID;

  memset(dc_ciu_settings.dc_id, 0, sizeof(dc_ciu_settings.dc_id));
  strncpy(dc_ciu_settings.dc_id, DEFAULT_DC_ID, SL_WISUN_DC_ID_LEN);

  memcpy(dc_ciu_settings.pmk, default_pmk, SL_WISUN_PMK_LEN);

  dc_ciu_settings.server_port = DEFAULT_SERVER_PORT;
  dc_ciu_settings.idle_timeout_ms = DEFAULT_IDLE_TIMEOUT_MS;
  dc_ciu_settings.max_scan_solicits = DEFAULT_MAX_SCAN_SOLICITS;
  dc_ciu_settings.max_connect_solicits = DEFAULT_MAX_CONNECT_SOLICITS;
}

/***************************************************************************//**
 * Initialize the DC CIU settings with defaults.
 ******************************************************************************/
void app_cli_init(void)
{
  Ecode_t ecode;
  uint32_t type;
  size_t len;

  // Try to load from NVM
  ecode = nvm3_getObjectInfo(nvm3_defaultHandle,
                             DC_CIU_NVM3_KEY_SETTINGS,
                             &type,
                             &len);

  if ((ecode == ECODE_NVM3_OK) && (len == sizeof(dc_ciu_settings_t))) {
    ecode = nvm3_readData(nvm3_defaultHandle,
                          DC_CIU_NVM3_KEY_SETTINGS,
                          &dc_ciu_settings,
                          sizeof(dc_ciu_settings_t));
    if (ecode == ECODE_NVM3_OK) {
      printf("[DC CLI] Settings loaded from NVM\n");
      return;
    }
  }

  // Use defaults
  app_cli_reset_settings();
  printf("[DC CLI] Using default settings\n");
}

/***************************************************************************//**
 * Save current settings to NVM.
 ******************************************************************************/
sl_status_t app_cli_save_settings(void)
{
  Ecode_t ecode;

  ecode = nvm3_writeData(nvm3_defaultHandle,
                         DC_CIU_NVM3_KEY_SETTINGS,
                         &dc_ciu_settings,
                         sizeof(dc_ciu_settings_t));

  if (ecode != ECODE_NVM3_OK) {
    return SL_STATUS_FAIL;
  }

  return SL_STATUS_OK;
}

/***************************************************************************//**
 * Get the current PHY configuration based on settings.
 ******************************************************************************/
void app_cli_get_phy_config(sl_wisun_phy_config_t *phy_config)
{
  if (phy_config == NULL) {
    return;
  }

  memset(phy_config, 0, sizeof(sl_wisun_phy_config_t));
  phy_config->type = SL_WISUN_PHY_CONFIG_FAN11;
  phy_config->config.fan11.reg_domain = dc_ciu_settings.regulatory_domain;
  phy_config->config.fan11.chan_plan_id = dc_ciu_settings.chan_plan_id;
  phy_config->config.fan11.phy_mode_id = dc_ciu_settings.phy_mode_id;
}

/***************************************************************************//**
 * Get the target DC ID based on settings.
 ******************************************************************************/
void app_cli_get_dc_id(sl_wisun_dc_id_t *dc_id)
{
  if (dc_id == NULL) {
    return;
  }

  memset(dc_id, 0, sizeof(sl_wisun_dc_id_t));
  strncpy((char *)dc_id->id, dc_ciu_settings.dc_id, SL_WISUN_DC_ID_LEN - 1);
}

/***************************************************************************//**
 * Get the PMK from settings.
 ******************************************************************************/
void app_cli_get_pmk(uint8_t *pmk)
{
  if (pmk == NULL) {
    return;
  }

  memcpy(pmk, dc_ciu_settings.pmk, SL_WISUN_PMK_LEN);
}

// -----------------------------------------------------------------------------
//                          CLI Command Handlers
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * CLI command: dc get [setting]
 ******************************************************************************/
void app_cli_get_cmd(sl_cli_command_arg_t *arguments)
{
  const char *setting = NULL;

  // Reset idle timer on CLI activity
  app_reset_idle_timer();

  if (sl_cli_get_argument_count(arguments) > 0) {
    setting = sl_cli_get_argument_string(arguments, 0);
    print_setting(setting);
  } else {
    print_all_settings();
  }
}

/***************************************************************************//**
 * CLI command: dc set <setting> <value>
 ******************************************************************************/
void app_cli_set_cmd(sl_cli_command_arg_t *arguments)
{
  char *setting = NULL;
  char *value = NULL;
  size_t argc = sl_cli_get_argument_count(arguments);

  // Reset idle timer on CLI activity
  app_reset_idle_timer();

  // No arguments - show available settings
  if (argc == 0) {
    printf("Usage: dc set <setting> <value>\n");
    print_settings_help();
    return;
  }

  setting = (char *) sl_cli_get_argument_string(arguments, 0);
  if (setting == NULL || strcmp(setting, "help") == 0 || strcmp(setting, "?") == 0) {
    print_settings_help();
    return;
  }

  value = (char *) sl_cli_get_argument_string(arguments, 1);
  if (value == NULL) {
    printf("Usage: dc set <setting> <value>\n");
    print_settings_help();
    return;
  }

  if (set_setting(setting, value)) {
    printf("%s = %s\n", setting, value);
    // Refresh idle timer so a new idle_timeout_ms applies immediately.
    app_reset_idle_timer();
  } else {
    printf("Failed to set %s\n", setting);
  }
}

/***************************************************************************//**
 * CLI command: dc save
 ******************************************************************************/
void app_cli_save_cmd(sl_cli_command_arg_t *arguments)
{
  (void)arguments;

  // Reset idle timer on CLI activity
  app_reset_idle_timer();

  if (app_cli_save_settings() == SL_STATUS_OK) {
    printf("[DC] Settings saved to NVM\n");
  } else {
    printf("[DC] Failed to save settings\n");
  }
}

/***************************************************************************//**
 * CLI command: dc reset
 ******************************************************************************/
void app_cli_reset_cmd(sl_cli_command_arg_t *arguments)
{
  (void)arguments;

  // Reset idle timer on CLI activity
  app_reset_idle_timer();

  app_cli_reset_settings();

  // Delete from NVM
  nvm3_deleteObject(nvm3_defaultHandle, DC_CIU_NVM3_KEY_SETTINGS);

  printf("[DC] Settings reset to defaults\n");
}

/***************************************************************************//**
 * CLI command: dc status
 ******************************************************************************/
void app_cli_status_cmd(sl_cli_command_arg_t *arguments)
{
  (void)arguments;

  // Reset idle timer on CLI activity
  app_reset_idle_timer();

  int state = app_get_current_state();
  const char *state_name = app_get_state_name(state);

  printf("=====================================\n");
  printf("  DC CIU Status\n");
  printf("=====================================\n");
  printf("State: %s (%d)\n", state_name, state);
  printf("DC ID: %s\n", dc_ciu_settings.dc_id);
  printf("PHY: %s, ChanPlan=%u, PhyMode=%u\n",
         get_reg_domain_str(dc_ciu_settings.regulatory_domain),
         dc_ciu_settings.chan_plan_id,
         dc_ciu_settings.phy_mode_id);
  printf("=====================================\n");
}
