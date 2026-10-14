/***************************************************************************//**
 * @file
 * @brief RAIL utility for external RF switch configuration (antenna-to-pin
 *   mapping, VDD power-gating, and idle behavior).
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * SPDX-License-Identifier: Zlib
 *
 ******************************************************************************/

#include "sl_rail.h"
#include "sl_rail_util_rf_switch.h"
#include "sl_rail_util_rf_switch_config.h"
#include "em_common.h"

bool sl_rail_util_rf_switch_config_allowed(void)
{
  return sl_rail_rf_switch_can_reconfigure(SL_RAIL_EFR32_HANDLE);
}

// A custom antenna-to-pin pattern is requested when the type is not NONE.
#if (SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE \
     != SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_NONE)
#define SL_RAIL_UTIL_RF_SWITCH_HAS_ANTENNA_GPIO_PATTERN  1
#endif

// The antenna-switch control GPIO(s) come from the AoX Antenna utility. This
// component layers the antenna-to-pin mapping and optional VDD power-gating on
// top by calling sl_rail_config_rf_switch(). It is always called, so the
// control pins rest low from boot even with neither a pattern nor VDD.
void sl_rail_util_rf_switch_init(void)
{
  sl_rail_rf_switch_config_t rf_switch_config = {
#ifdef SL_RAIL_UTIL_RF_SWITCH_HAS_ANTENNA_GPIO_PATTERN
    .use_antenna_gpio_pattern = true,
    // Entry i is the control-pin bit pattern for antenna id i+1. Presets cover
    // the common single/dual-pin SPDT cases; CUSTOM uses the supplied array.
    .antenna_gpio_pattern =
#if SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE == SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_SINGLE_STANDARD
    { 0x1U, 0x0U, 0x2U, 0x3U },
#elif SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE == SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_SINGLE_INVERTED
    { 0x0U, 0x1U, 0x2U, 0x3U },
#elif SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE == SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_DUAL_STANDARD
    { 0x1U, 0x2U, 0x2U, 0x3U },
#elif SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE == SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_DUAL_INVERTED
    { 0x2U, 0x1U, 0x2U, 0x3U },
#else // SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_CUSTOM
      SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_CUSTOM,
#endif
#else
    .use_antenna_gpio_pattern = false,
    .antenna_gpio_pattern = { 0U, 1U, 2U, 3U },
#endif // SL_RAIL_UTIL_RF_SWITCH_HAS_ANTENNA_GPIO_PATTERN
    .vdd_enable = (SL_RAIL_UTIL_RF_SWITCH_VDD_ENABLE != 0),
#if SL_RAIL_UTIL_RF_SWITCH_VDD_ENABLE
    .vdd_pin = {
      .gpio_port = (uint8_t)SL_RAIL_UTIL_RF_SWITCH_VDD_PIN_PORT,
      .gpio_pin = SL_RAIL_UTIL_RF_SWITCH_VDD_PIN_PIN,
    },
    .vdd_settle_time_us = SL_RAIL_UTIL_RF_SWITCH_VDD_SETTLE_TIME_US,
    .vdd_prs_signal =
      (sl_rail_rf_switch_vdd_prs_signal_t)SL_RAIL_UTIL_RF_SWITCH_VDD_PRS_SIGNAL,
#else
    .vdd_pin = { 0U, 0U },
    .vdd_settle_time_us = SL_RAIL_RF_SWITCH_VDD_SETTLE_TIME_US_DEFAULT,
    .vdd_prs_signal = SL_RAIL_RF_SWITCH_VDD_PRS_SIGNAL_PAEN_OR_LNAEN,
#endif
  };

  sl_rail_status_t status =
    sl_rail_config_rf_switch(SL_RAIL_EFR32_HANDLE, &rf_switch_config);
  // Without a pattern or VDD this only idles the control pins, so it may fail
  // (e.g. GPIO is a secure TrustZone peripheral) without breaking the app.
#if defined(SL_RAIL_UTIL_RF_SWITCH_HAS_ANTENNA_GPIO_PATTERN) \
  || (SL_RAIL_UTIL_RF_SWITCH_VDD_ENABLE != 0)
  EFM_ASSERT(status == SL_RAIL_STATUS_NO_ERROR);
#endif
  (void) status;
}
