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

#ifndef _ZW_JAMMING_DETECTION_CONFIG_H_
#define _ZW_JAMMING_DETECTION_CONFIG_H_

// <<< Use Configuration Wizard in Context Menu >>>

// <h> Z-Wave NCP jamming detection (RSSI window and default report interval)

// <o SL_JAMMING_DETECTION_BUFFER_SIZE> Number of RSSI samples kept per channel in the jamming detection window <150..255:1> <f.d>
// <i> Each sample is taken every 100 ms; e.g. 150 samples span 15 seconds of history. Per-channel critical sample counts must not exceed this value.
// <i> Default: 150
#define SL_JAMMING_DETECTION_BUFFER_SIZE  150

// <o SL_JAMMING_DEFAULT_DETECTION_EVALUATION_DELAY_SEC> Default interval in seconds between periodic jamming reports when initialized via defaults <0..20:1> <f.d>
// <i> Used as the default report_interval_sec in sl_jamming_detection_default_config(). Valid runtime values are 1–20 seconds; 0 disables periodic reporting.
// <i> Default: 5
#define SL_JAMMING_DEFAULT_DETECTION_EVALUATION_DELAY_SEC  5

// </h>

// <<< end of configuration section >>>

#endif /* _ZW_JAMMING_DETECTION_CONFIG_H_ */
