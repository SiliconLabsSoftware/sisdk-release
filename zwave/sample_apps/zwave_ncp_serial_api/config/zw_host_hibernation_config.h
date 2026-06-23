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

#ifndef _ZW_HOST_HIBERNATION_CONFIG_H_
#define _ZW_HOST_HIBERNATION_CONFIG_H_

// <<< Use Configuration Wizard in Context Menu >>>

// <h> Host Hibernation Configuration

// <o SL_HOST_HIBERNATION_DEVICE_TABLE_SIZE> Device Table Size <1..128:1> <f.d>
// <i> The number of devices that can be tracked in the important-devices table.
// <i> Default: 128
#define SL_HOST_HIBERNATION_DEVICE_TABLE_SIZE  128

// <o SL_HOST_HIBERNATION_KEEP_ALIVE_CHECK_PERIOD_MS> Keep-Alive Check Period (ms) <1..60000:1> <f.d>
// <i> The period in milliseconds between keep-alive checks for important devices.
// <i> Default: 60000
#define SL_HOST_HIBERNATION_KEEP_ALIVE_CHECK_PERIOD_MS  60000

// </h>

// <<< end of configuration section >>>

#endif /* _ZW_HOST_HIBERNATION_CONFIG_H_ */
