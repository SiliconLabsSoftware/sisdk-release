/***************************************************************************//**
 * # License
 * <b> Copyright 2026 Silicon Laboratories Inc. www.silabs.com </b>
 *******************************************************************************
 *
 * The licensor of this software is Silicon Laboratories Inc. Your use of this
 * software is governed by the terms of the Silicon Labs Master Software License
 * Agreement (MSLA) available at
 * https://www.silabs.com/about-us/legal/master-software-license-agreement
 * By installing, copying or otherwise using this software, you agree to the
 * terms of the MSLA.
 *
 ******************************************************************************/

#ifndef _ZW_DTPA_CONFIG_H_
#define _ZW_DTPA_CONFIG_H_

// <<< Use Configuration Wizard in Context Menu >>>

// <h> Configuration of the DTPA (Dynamic Transmit Power Algorithm).

// <o ZWAVE_DTPA_NOISE_MARGIN_DBM> Noise margin in dBm <0..12:1> <f.d>
// <i> The DTPA algorithm will adjust the transmit power level to have the RSSI level at least this many dBm above the noise floor. Both noise floor and RSSI are measured by the packet receiver, and sent back to the transmitter through the acknowledge.
// <i> Default: 6
#define ZWAVE_DTPA_NOISE_MARGIN_DBM  6

// </h>

// <<< end of configuration section >>>

#endif /* _ZW_DTPA_CONFIG_H_ */
