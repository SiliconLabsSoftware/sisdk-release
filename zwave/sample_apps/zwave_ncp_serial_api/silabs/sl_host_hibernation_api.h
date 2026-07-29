/***************************************************************************//**
 * @file sl_host_hibernation_api.h
 * @brief Public API for the host hibernation module.
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * SPDX-FileCopyrightText: Silicon Laboratories Inc. <https://www.silabs.com/>
 *
 * SPDX-License-Identifier: LicenseRef-MSLA
 *
 * The licensor of this software is Silicon Laboratories Inc. Your use of this
 * software is governed by the terms of Silicon Labs Master Software License
 * Agreement (MSLA) available at
 * www.silabs.com/about-us/legal/master-software-license-agreement. This
 * software is distributed to you in Source Code format and is governed by the
 * sections of the MSLA applicable to Source Code.
 *
 ******************************************************************************/

#ifndef SL_HOST_HIBERNATION_API_H_
#define SL_HOST_HIBERNATION_API_H_

#include <stdbool.h>
#include <stdint.h>
#include <ZW_typedefs.h>

bool is_host_sleeping(void);

/**
 * @brief Set the host state
 * @param sleeping True if host is sleeping, false if the host is awake
 */
void set_host_state(bool sleeping);

/**
 * @brief Initialize the keep-alive timer. Must be called once at startup.
 */
void keep_alive_init(void);

/**
 * @brief Initialize the host-wake GPIO as push-pull, driven HIGH (idle).
 *
 * Requires the @c zw_host_wakeup_gpio component. Pin defaults to PA10;
 * override via @c sl_host_wakeup_gpio_config.h. Without the component,
 * this is a no-op and the 0xFE unsolicited frame fallback is used instead.
 * Call once at startup.
 */
void gpio_wakeup_host_init(void);

/**
 * @brief Assert the host-wake signal to wake the host from hibernation.
 *
 * Drives the GPIO low when @c zw_host_wakeup_gpio is present, otherwise sends
 * an unsolicited SerialAPI frame (0xFE).
 */
void gpio_wakeup_host(void);

/**
 * @brief Update the S2 message count for a given node
 * @param node_id node ID
 * @param payload S2 message payload
 * @return true if the count was updated
 *   can return false if:
 *   - payload is NULL
 *   - payload is not a valid S2 message
 *   - sequence number is a duplicate
 *   - node ID is not found in the important devices list
 */
bool s2_message_update_count(const node_id_t node_id, const uint8_t * const payload);

#endif /* SL_HOST_HIBERNATION_API_H_ */
