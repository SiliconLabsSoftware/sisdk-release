/***************************************************************************//**
 * @file sli_bluetooth_common_init.h
 * @brief Bluetooth Common initialization
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * The licensor of this software is Silicon Laboratories Inc. Your use of this
 * software is governed by the terms of Silicon Labs Master Software License
 * Agreement (MSLA) available at
 * www.silabs.com/about-us/legal/master-software-license-agreement. This
 * software is distributed to you in Source Code format and is governed by the
 * sections of the MSLA applicable to Source Code.
 *
 ******************************************************************************/

#ifndef SLI_BLUETOOTH_COMMON_INIT_H
#define SLI_BLUETOOTH_COMMON_INIT_H

#include <stdint.h>
#include <sl_status.h>

#define SL_BLUETOOTH_COMMON_CONFIG_BUFFER_MEMORY_SIZE_UNUSED (0)

/**
 * @brief Configuration structure for Bluetooth Common initialization.
 */
struct sl_bluetooth_common_config {
  uint32_t buffer_memory_size;
};

/**
 * @brief Initialize Bluetooth Common buffer memory.
 *
 * @param[in] config Pointer to the configuration structure. If NULL, the
 *   default configuration is used. If
 *   @ref sl_bluetooth_common_config::buffer_memory_size is set to
 *   @ref SL_BLUETOOTH_COMMON_CONFIG_BUFFER_MEMORY_SIZE_UNUSED, the default
 *   value from SL_BLUETOOTH_COMMON_BUFFER_MEMORY_SIZE is used.
 *
 * @return SL_STATUS_OK on success, otherwise error
 */
sl_status_t sli_bluetooth_common_init(const struct sl_bluetooth_common_config *config);

/**
 * @brief Deinitialize Bluetooth Common buffer memory.
 *
 * Releases the buffer pool allocated by @ref sli_bluetooth_common_init.
 *
 * @return SL_STATUS_OK on success, otherwise error
 */
sl_status_t sli_bluetooth_common_deinit(void);

#endif /* SLI_BLUETOOTH_COMMON_INIT_H */
