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

// <<< Use Configuration Wizard in Context Menu >>>

// The antenna-switch control GPIO(s) are configured by the AoX Antenna utility.
// This component configures the antenna-to-pin mapping (polarity / single vs
// dual-pin / custom) plus the optional VDD power-gating pin and idle-low
// behavior.
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

// <h> RF Switch VDD / Idle
// <q SL_RAIL_UTIL_RF_SWITCH_IDLE_CONTROL_PINS_LOW> Drive control pins low when radio inactive
// <i> When enabled, the control pins rest low between radio activity so the
// <i> external switch is not left powered through a control line at idle. Both
// <i> control pins are parked low directly by the antenna-switch LDMA, so this
// <i> consumes no additional PRS channels.
// <i> Default: 0
#define SL_RAIL_UTIL_RF_SWITCH_IDLE_CONTROL_PINS_LOW  0

// <q SL_RAIL_UTIL_RF_SWITCH_VDD_ENABLE> Enable VDD power pin
// <i> Default: 0
#define SL_RAIL_UTIL_RF_SWITCH_VDD_ENABLE  0

#if SL_RAIL_UTIL_RF_SWITCH_VDD_ENABLE
// <o SL_RAIL_UTIL_RF_SWITCH_VDD_SETTLE_TIME_US> VDD settle time (us)
// <1-255:1>
// <i> Default: 2
#define SL_RAIL_UTIL_RF_SWITCH_VDD_SETTLE_TIME_US  2

// <o SL_RAIL_UTIL_RF_SWITCH_VDD_PRS_SIGNAL> VDD PRS signal
// <0=> PA enable OR LNA enable
// <1=> TX active OR RX active
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
// #define SL_RAIL_UTIL_RF_SWITCH_VDD_PIN_PORT           gpioPortA
// #define SL_RAIL_UTIL_RF_SWITCH_VDD_PIN_PIN               4
// [GPIO_SL_RAIL_UTIL_RF_SWITCH_VDD_PIN]$
#endif

// <<< sl:end pin_tool >>>

#endif // SL_RAIL_UTIL_RF_SWITCH_CONFIG_H
