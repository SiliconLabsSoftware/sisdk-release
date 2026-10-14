/***************************************************************************//**
 * @file
 * @brief RF switch compile-time configuration for EFR32xG24.
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * SPDX-License-Identifier: Zlib
 *
 ******************************************************************************/

#ifndef SL_RAIL_UTIL_RF_SWITCH_CONFIG_H
#define SL_RAIL_UTIL_RF_SWITCH_CONFIG_H

#include "sl_gpio.h"

// <<< Use Configuration Wizard in Context Menu >>>

// The antenna-switch control GPIO(s) are configured by the AoX Antenna utility.
// This component configures the antenna-to-pin mapping (polarity / single vs
// dual-pin / custom) plus the optional VDD power-gating pin.
//
// These knobs use plain integer literals so they can be compared in #if
// directives below. The values match the enum numeric values and are cast back
// to the enum type in the plugin source.

// <h> RF Switch Antenna GPIO Pattern
// <o SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE> Antenna-to-GPIO control pattern
// <SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_NONE=> None (natural binary encoding)
// <SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_SINGLE_STANDARD=> Single control pin, standard (antenna 1 = high)
// <SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_SINGLE_INVERTED=> Single control pin, inverted (antenna 1 = low)
// <SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_DUAL_STANDARD=> Dual complementary pins, standard
// <SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_DUAL_INVERTED=> Dual complementary pins, inverted
// <SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_CUSTOM=> Custom pattern array
// <i> Associates a GPIO drive pattern with each antenna id, driving the
// <i> antenna-switch GPIO(s) configured by the AoX Antenna utility. Selects the
// <i> external RF switch polarity, single vs dual-pin complementary control, or
// <i> a fully custom antenna-to-pin mapping.
// <d> SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_NONE
#define SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE    SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_TYPE_NONE

// <a.4 SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_CUSTOM> Custom antenna GPIO pattern (used when type = Custom) <0..3>
// <i> Entry i is the control-pin bit pattern for antenna id i+1: bit0 drives the
// <i> first antenna-switch GPIO, bit1 the second.
// <d> { 0, 1, 2, 3 }
#define SL_RAIL_UTIL_RF_SWITCH_ANTENNA_GPIO_PATTERN_CUSTOM  { 0, 1, 2, 3 }
// </h>

// <h> RF Switch VDD
// <q SL_RAIL_UTIL_RF_SWITCH_VDD_ENABLE> Enable VDD power pin
// <i> VDD follows radio activity. The control pins always follow the same
// <i> radio activity and rest low while the radio is inactive, from boot.
// <i> Default: 0
#define SL_RAIL_UTIL_RF_SWITCH_VDD_ENABLE  0

#if SL_RAIL_UTIL_RF_SWITCH_VDD_ENABLE
// <o SL_RAIL_UTIL_RF_SWITCH_VDD_SETTLE_TIME_US> VDD settle time (us)
// <1-255:1>
// <i> Delay after VDD rises before the Channel Sounding antenna is selected.
// <i> Default: 2
#define SL_RAIL_UTIL_RF_SWITCH_VDD_SETTLE_TIME_US  2

// <o SL_RAIL_UTIL_RF_SWITCH_VDD_PRS_SIGNAL> VDD PRS signal
// <0=> PA enable OR LNA enable
// <1=> TX active OR RX active
// <i> Channel Sounding events always use PA enable OR LNA enable.
// <i> Default: PA enable OR LNA enable
#define SL_RAIL_UTIL_RF_SWITCH_VDD_PRS_SIGNAL  0
#endif // SL_RAIL_UTIL_RF_SWITCH_VDD_ENABLE
// </h>

// <<< end of configuration section >>>

// <<< sl:start pin_tool >>>

#if SL_RAIL_UTIL_RF_SWITCH_VDD_ENABLE
// RF switch VDD power pin
// <gpio> SL_RAIL_UTIL_RF_SWITCH_VDD_PIN
// $[GPIO_SL_RAIL_UTIL_RF_SWITCH_VDD_PIN]
// #define SL_RAIL_UTIL_RF_SWITCH_VDD_PIN_PORT           SL_GPIO_PORT_A
// #define SL_RAIL_UTIL_RF_SWITCH_VDD_PIN_PIN            2
// [GPIO_SL_RAIL_UTIL_RF_SWITCH_VDD_PIN]$
#endif

// <<< sl:end pin_tool >>>

#endif // SL_RAIL_UTIL_RF_SWITCH_CONFIG_H
