/***************************************************************************//**
 * @file sl_host_hibernation_cmd_handlers.h
 * @brief Host hibernation and important devices list command handlers.
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

#ifndef SL_HOST_HIBERNATION_CMD_HANDLERS_H_
#define SL_HOST_HIBERNATION_CMD_HANDLERS_H_

#include <stdint.h>
#include <stdbool.h>
#include "ZW_application_transport_interface.h"
#include "app.h"
#include "sl_host_hibernation_api.h"
#include "zw_host_hibernation_config.h"

#include "SerialAPI.h"

#define FUNC_ID_HOST_SLEEP FUNC_ID_PROPRIETARY_0  /* 0xF0 - Host Hibernation commands */

#define ZW_MAX_IMPORTANT_DEVICES SL_HOST_HIBERNATION_DEVICE_TABLE_SIZE

/** Each frame can contains up to 173 bytes of payload (RECEIVE_BUFFER_SIZE - 8)
 * | SOF | LEN | TYPE | CMD ID | TOTAL_FRAME_COUNT | FRAME_INDEX | LIST_LENGTH | ... | CHECKSUM |
 * each node need 2 bytes for node_id and 2 bytes for keep_alive_min
 * so each frame can contains up to (RECEIVE_BUFFER_SIZE - 8) / 4 nodes
 * so the max frame count is ZW_MAX_IMPORTANT_DEVICES / ((RECEIVE_BUFFER_SIZE - 8) / 4)
 */
#define MAX_DEVICE_COUNT_PER_FRAME ((RECEIVE_BUFFER_SIZE - 8) / 4)
/**
 * Max entries per response frame: 3 bytes overhead (subcommand + length + more_to_follow),
 * each entry is 4 bytes (NodeID MSB, NodeID LSB, S2 Message Count, Last Sequence Number).
 */
 #define S2_MSG_COUNT_ENTRIES_PER_FRAME ((BUF_SIZE_TX - 3) / 4)

#define HOST_SLEEP_SUBCOMMAND_LIST_IMPORTANT_DEVICES              0x00
#define HOST_SLEEP_SUBCOMMAND_CLEAR_IMPORTANT_DEVICES_LIST        0x01
#define HOST_SLEEP_SUBCOMMAND_NOTIFY_HOST_STATE                   0x02
#define HOST_SLEEP_SUBCOMMAND_ZW_MODULE_CAPABILITIES_REPORT       0x03
#define HOST_SLEEP_SUBCOMMAND_REQUEST_WAKEUP_REPORT               0x04
#define HOST_SLEEP_SUBCOMMAND_DEVICE_LOST_REPORT                  0x05
#define HOST_SLEEP_SUBCOMMAND_REQUEST_S2_MESSAGE_COUNT            0x06
#define HOST_SLEEP_SUBCOMMAND_UNKNOWN                             0xFF

#define NOTIFY_HOST_STATE_AWAKE 0x00
#define NOTIFY_HOST_STATE_SLEEPING 0x01

#define IMPORTANT_DEVICES_LIST_DEVICE_SIZE 4 // 2 bytes for node_id and 2 bytes for keep_alive_min
#define IMPORTANT_DEVICES_LIST_HEADER_SIZE 4 // 1 byte for total_frame_count, 1 byte for frame_index, 1 byte for list_length

typedef enum {
  IMPORTANT_DEVICES_LIST_SUCCESS = 0,
  IMPORTANT_DEVICES_LIST_UNKNOWN_NODE_ID = 1,
  IMPORTANT_DEVICES_LIST_NODE_ID_ALREADY_EXISTS = 2,
  IMPORTANT_DEVICES_LIST_NOT_ENOUGH_DEVICES = 3,
  IMPORTANT_DEVICES_LIST_WRONG_FRAME_INDEX = 4,
  IMPORTANT_DEVICES_LIST_WRONG_TOTAL_FRAME_COUNT = 5,
  IMPORTANT_DEVICES_LIST_TOO_MANY_DEVICES = 6,
} important_devices_list_error_t;

typedef struct {
  node_id_t node_id; ///< 0 for empty
  uint16_t keep_alive_min; ///< Keep Alive in minutes
  uint16_t elapsed_min; ///< elapsed time in minutes
  uint8_t s2_message_count; ///< number of S2 messages received from the device
  uint8_t s2_last_seqno; ///< last sequence number received from the device
} important_device_t;

typedef struct {
  uint8_t total_frame_count; ///< frame count from last received frame
  uint8_t frame_index; ///< index from the last received frame, used to check we are not missing a frame
  uint8_t total_nodes_count; ///< node count in the important_devices list
  bool host_sleeping;
  bool has_pending_wakeup_frame;
  bool has_lost_devices;
  important_device_t important_devices[ZW_MAX_IMPORTANT_DEVICES]; ///< this list must be packed. (first empty row must be the end of the list)
  SZwaveReceivePackage wakeup_frame_package;
} host_sleep_context_t;

#endif /* SL_HOST_HIBERNATION_CMD_HANDLERS_H_ */
