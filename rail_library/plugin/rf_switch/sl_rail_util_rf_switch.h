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

#ifndef SL_RAIL_UTIL_RF_SWITCH_H
#define SL_RAIL_UTIL_RF_SWITCH_H

#include <stdbool.h>

// Antenna-id -> control-pin GPIO pattern presets. These associate a GPIO drive
// pattern with each antenna id for an external RF switch driven from the
// antenna-switch GPIO(s) (configured via the AoX Antenna utility). bit0 drives
// the first control pin, bit1 the second.
/** No custom pattern; use the natural binary encoding (antenna id - 1). */
#define SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_NONE            0
/** Single control pin, standard polarity (antenna 1 = pin high). */
#define SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_SINGLE_STANDARD 1
/** Single control pin, inverted polarity (antenna 1 = pin low). */
#define SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_SINGLE_INVERTED 2
/** Dual complementary control pins, standard polarity (ant 1 = V1 high/V2 low). */
#define SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_DUAL_STANDARD   3
/** Dual complementary control pins, inverted polarity (ant 1 = V1 low/V2 high). */
#define SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_DUAL_INVERTED   4
/** Fully custom per-antenna pattern array. */
#define SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_CUSTOM          5

/**
 * Configure the external RF switch from compile-time settings.
 */
void sl_rail_util_rf_switch_init(void);

/**
 * @return True if RF switch settings may be changed.
 */
bool sl_rail_util_rf_switch_config_allowed(void);

#endif // SL_RAIL_UTIL_RF_SWITCH_H
