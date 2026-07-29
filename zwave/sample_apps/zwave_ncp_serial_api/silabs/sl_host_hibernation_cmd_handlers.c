/***************************************************************************//**
 * @file sl_host_hibernation_cmd_handlers.c
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

#include <assert.h>
#include <string.h>
#include <stdbool.h>

#include "AppTimer.h"
#include "app.h"
#include "cmd_handlers.h"
#include "cmds_management.h"
#include "comm_interface.h"
#include "NodeMask.h"
#include "SerialAPI.h"

#include "sl_host_hibernation_cmd_handlers.h"

#ifdef SL_CATALOG_ZW_HOST_WAKEUP_GPIO_PRESENT
#include "sl_gpio.h"
#include "sl_host_wakeup_gpio_config.h"

static const sl_gpio_t host_wake_gpio = {
  .port = SL_HOST_WAKEUP_GPIO_PORT,
  .pin  = SL_HOST_WAKEUP_GPIO_PIN
};
#endif

#include "SwTimer.h"
#include "utils.h"
#include "ZAF_Common_interface.h"
#include "ZW_transport_api.h"
#include "ZW_application_transport_interface.h"

void gpio_wakeup_host_init(void)
{
#ifdef SL_CATALOG_ZW_HOST_WAKEUP_GPIO_PRESENT
  (void)sl_gpio_set_pin_mode(&host_wake_gpio, SL_GPIO_MODE_PUSH_PULL, 1);
  (void)sl_gpio_set_pin(&host_wake_gpio);
#endif
}

void gpio_wakeup_host(void)
{
#ifdef SL_CATALOG_ZW_HOST_WAKEUP_GPIO_PRESENT
  (void)sl_gpio_clear_pin(&host_wake_gpio);
#else
  compl_workbuf[0] = 0xFE;
  RequestUnsolicited(0xFE, compl_workbuf, 1);
#endif
}

static void gpio_wakeup_host_clear(void)
{
#ifdef SL_CATALOG_ZW_HOST_WAKEUP_GPIO_PRESENT
  (void)sl_gpio_set_pin(&host_wake_gpio);
#endif
}

static SSwTimer keep_alive_timer;

static void urgent_wakeup_callback(const SZwaveReceivePackage *pRxPackage);
static void host_sleep_subcommand_request_wakeup_report(void);
static void host_sleep_subcommand_device_lost_report(void);
static void keep_alive_timer_cb(SSwTimer *pTimer);
static void keep_alive_check_timeouts(void);
static bool keep_alive_update_node(const node_id_t node_id);

/**
 * Host sleeping diagram
 *
 * Host --> Controller: List of important devices
 * Host --> Controller: Notify Host State Sleeping
 * Host: Goes to sleep
 * Important Device -[URGENT, S2]-> Controller: wakeup host
 * Host --> Controller: Notify Host State Awake
 * Host --> Controller: Important Device list clear
 * Host --> Controller: Request Wakeup Report
 * Controller --> Host: [URGENT] S2 frame
 */

static host_sleep_context_t host_sleep_context = {
  .total_frame_count = 0,
  .frame_index = 0,
  .total_nodes_count = 0,
  .host_sleeping = false,
  .has_pending_wakeup_frame = false,
  .has_lost_devices = false,
  .important_devices = { { 0 } },
  .wakeup_frame_package = { 0 },
#ifdef SL_CATALOG_ZW_JAMMING_DETECTION_PRESENT
  .has_pending_jamming_report = false,
  .jamming_report = { 0 },
#endif
};

#ifdef SL_CATALOG_ZW_JAMMING_DETECTION_PRESENT
void store_jamming_report(const sl_jamming_detection_statistics_t *report)
{
  memcpy(&host_sleep_context.jamming_report, report, sizeof(sl_jamming_detection_statistics_t));
  host_sleep_context.has_pending_jamming_report = true;
}
#endif

static bool is_important_device(const node_id_t node_id)
{
  if (node_id == 0) {
    return false;
  }

  for (uint8_t i = 0; i < ZW_MAX_IMPORTANT_DEVICES; i++) {
    if (host_sleep_context.important_devices[i].node_id == 0) {
      break;
    }
    if (host_sleep_context.important_devices[i].node_id == node_id) {
      return true;
    }
  }
  return false;
}

void set_host_state(bool sleeping)
{
  host_sleep_context.host_sleeping = sleeping;
}

bool is_host_sleeping(void)
{
  return host_sleep_context.host_sleeping;
}

void keep_alive_init(void)
{
  AppTimerRegister(&keep_alive_timer, true, keep_alive_timer_cb);
}

static void keep_alive_start_tracking(void)
{
  SZwaveCommandPackage cmdPackage = {
    .eCommandType = EZWAVECOMMANDTYPE_SET_KEEP_ALIVE_TRACKING,
    .uCommandParams.SetKeepAliveTracking.value = true
  };
  // Put the package on queue (and dont wait for it)
  __attribute__((unused)) EQueueNotifyingStatus QueueStatus = QueueNotifyingSendToBack(ZAF_getZwCommandQueue(), (uint8_t *)&cmdPackage, 0);
  assert(EQUEUENOTIFYING_STATUS_SUCCESS == QueueStatus);

  for (uint8_t i = 0; i < host_sleep_context.total_nodes_count; i++) {
    host_sleep_context.important_devices[i].elapsed_min = 0;
  }
  TimerStart(&keep_alive_timer, SL_HOST_HIBERNATION_KEEP_ALIVE_CHECK_PERIOD_MS);
}

static void keep_alive_stop_tracking(void)
{
  SZwaveCommandPackage cmdPackage = {
    .eCommandType = EZWAVECOMMANDTYPE_SET_KEEP_ALIVE_TRACKING,
    .uCommandParams.SetKeepAliveTracking.value = false
  };
  // Put the package on queue (and dont wait for it)
  __attribute__((unused)) EQueueNotifyingStatus QueueStatus = QueueNotifyingSendToBack(ZAF_getZwCommandQueue(), (uint8_t *)&cmdPackage, 0);
  assert(EQUEUENOTIFYING_STATUS_SUCCESS == QueueStatus);
  TimerStop(&keep_alive_timer);
}

static bool keep_alive_update_node(const node_id_t node_id)
{
  if (node_id == 0 || !host_sleep_context.host_sleeping) {
    return false;
  }

  for (uint8_t i = 0; i < host_sleep_context.total_nodes_count; i++) {
    if (host_sleep_context.important_devices[i].node_id == node_id
        && host_sleep_context.important_devices[i].keep_alive_min > 0) {
      host_sleep_context.important_devices[i].elapsed_min = 0;
      return true;
    }
  }
  return false;
}

static void keep_alive_check_timeouts(void)
{
  for (uint8_t i = 0; i < host_sleep_context.total_nodes_count; i++) {
    important_device_t *dev = &host_sleep_context.important_devices[i];
    if (dev->keep_alive_min == 0 || dev->elapsed_min >= dev->keep_alive_min) {
      continue;
    }
    dev->elapsed_min++;
    if (dev->elapsed_min >= dev->keep_alive_min) {
      host_sleep_context.has_lost_devices = true;
    }
  }
  if (host_sleep_context.has_lost_devices) {
    gpio_wakeup_host();
  }
}

static void keep_alive_timer_cb(__attribute__((unused)) SSwTimer *pTimer)
{
  keep_alive_check_timeouts();
}

static void important_devices_list_response(const uint8_t total_nodes_count,
                                            const important_devices_list_error_t error)
{
  compl_workbuf[0] = HOST_SLEEP_SUBCOMMAND_LIST_IMPORTANT_DEVICES;
  compl_workbuf[1] = total_nodes_count;
  compl_workbuf[2] = error;
  if (error != IMPORTANT_DEVICES_LIST_SUCCESS) {
    memset(&host_sleep_context, 0, sizeof(host_sleep_context));
  }
  DoRespond_workbuf(3);
}

static important_devices_list_error_t verify_device(const node_id_t node_id)
{
  important_devices_list_error_t status = IMPORTANT_DEVICES_LIST_SUCCESS;
  if (node_id == 0) {
    // List should be packed
    status = IMPORTANT_DEVICES_LIST_UNKNOWN_NODE_ID;
  }
  /* Check if node is in the included nodes: classic or LR mask */
  else if (node_id <= ZW_MAX_NODES) {
    NODE_MASK_TYPE classic_node_mask;
    Get_included_nodes(classic_node_mask);
    if (!ZW_NodeMaskNodeIn(classic_node_mask, node_id)) {
      status = IMPORTANT_DEVICES_LIST_UNKNOWN_NODE_ID;
    }
  } else if (node_id >= LOWEST_LONG_RANGE_NODE_ID && node_id <= HIGHEST_LONG_RANGE_NODE_ID) {
    LR_NODE_MASK_TYPE lr_node_mask;
    Get_included_lr_nodes(lr_node_mask);
    if (!ZW_NodeMaskNodeIn(lr_node_mask, node_id)) {
      status = IMPORTANT_DEVICES_LIST_UNKNOWN_NODE_ID;
    }
  } else {
    /* Node ID is out of valid range (classic 1-232, LR 256-1279) */
    status = IMPORTANT_DEVICES_LIST_UNKNOWN_NODE_ID;
  }
  // Check for duplicated node id
  if (true == is_important_device(node_id)) {
    status = IMPORTANT_DEVICES_LIST_NODE_ID_ALREADY_EXISTS;
  }
  return status;
}

static void host_sleep_subcommand_list_important_devices(const comm_interface_frame_ptr frame)
{
  /** HOST->ZW: subcommand 0x00 | total_frame_count | frame_index |list_length | node_id[0] MSB | node_id[0] LSB |
   *   keep_alive_min[0] MSB | keep_alive_min[0] LSB |  ... | node_id[N] MSB | node_id[N] LSB |
   *   keep_alive_min[N] MSB | keep_alive_min[N] LSB */
  const uint8_t expected_frame_index = host_sleep_context.frame_index + 1;
  host_sleep_context.total_frame_count = frame->payload[1];
  if (host_sleep_context.total_frame_count == 0) {
    important_devices_list_response(host_sleep_context.total_nodes_count,
                                    IMPORTANT_DEVICES_LIST_WRONG_TOTAL_FRAME_COUNT);
    return;
  }

  if (frame->payload[2] != expected_frame_index) {
    important_devices_list_response(host_sleep_context.total_nodes_count, IMPORTANT_DEVICES_LIST_WRONG_FRAME_INDEX);
    return;
  }

  host_sleep_context.frame_index = frame->payload[2];
  const uint8_t frame_node_count = frame->payload[3];

  if (frame_node_count == 0) {
    important_devices_list_response(host_sleep_context.total_nodes_count, IMPORTANT_DEVICES_LIST_NOT_ENOUGH_DEVICES);
    return;
  }

  if (frame->len < (IMPORTANT_DEVICES_LIST_HEADER_SIZE + frame_node_count * IMPORTANT_DEVICES_LIST_DEVICE_SIZE)) {
    important_devices_list_response(host_sleep_context.total_nodes_count, IMPORTANT_DEVICES_LIST_NOT_ENOUGH_DEVICES);
    return;
  }

  uint8_t offset = 4;  /* Start after the length byte */
  for (uint8_t i = 0; i < frame_node_count; i++) {
    if (host_sleep_context.total_nodes_count >= ZW_MAX_IMPORTANT_DEVICES) {
      important_devices_list_response(host_sleep_context.total_nodes_count, IMPORTANT_DEVICES_LIST_TOO_MANY_DEVICES);
      return;
    }

    node_id_t node_id = (uint16_t) GET_16BIT_VALUE(&frame->payload[offset]);
    offset += 2;
    important_devices_list_error_t status = verify_device(node_id);
    if (status != IMPORTANT_DEVICES_LIST_SUCCESS) {
      /* We expect host to clear list on error and send new list, no need to continue here */
      important_devices_list_response(host_sleep_context.total_nodes_count, status);
      return;
    }

    host_sleep_context.important_devices[host_sleep_context.total_nodes_count].keep_alive_min
      = (uint16_t)GET_16BIT_VALUE(&frame->payload[offset]);
    offset += 2;
    host_sleep_context.important_devices[host_sleep_context.total_nodes_count].node_id
      = node_id;
    host_sleep_context.total_nodes_count++;
  }

  if (host_sleep_context.total_frame_count == host_sleep_context.frame_index) {
    host_sleep_context.frame_index = 0;
  }
  important_devices_list_response(host_sleep_context.total_nodes_count, IMPORTANT_DEVICES_LIST_SUCCESS);
}

static void host_sleep_subcommand_clear_important_devices_list(__attribute__((unused)) const comm_interface_frame_ptr frame)
{
  /** HOST->ZW: subcommand 0x01 */
  memset(&host_sleep_context, 0, sizeof(host_sleep_context));
  compl_workbuf[0] = HOST_SLEEP_SUBCOMMAND_CLEAR_IMPORTANT_DEVICES_LIST;
  compl_workbuf[1] = SAPI_COMMAND_STATUS_SUCCESS;
  DoRespond_workbuf(2);
}

static void app_set_controller_severity_level(const uint8_t severity_level)
{
  SZwaveCommandPackage cmdPackage = {
    .eCommandType = EZWAVECOMMANDTYPE_SET_SEVERITY_LEVEL,
    .uCommandParams.SetSeverityLevel.severity_level = severity_level
  };
  // Put the package on queue (and dont wait for it)
  __attribute__((unused)) EQueueNotifyingStatus QueueStatus = QueueNotifyingSendToBack(ZAF_getZwCommandQueue(), (uint8_t *)&cmdPackage, 0);
  assert(EQUEUENOTIFYING_STATUS_SUCCESS == QueueStatus);
}

static void host_sleep_subcommand_notify_host_state(const comm_interface_frame_ptr frame)
{
  /** HOST->ZW: subcommand 0x02 | host_state */
  const uint8_t host_state = frame->payload[1];
  const uint8_t severity_level = frame->payload[2] & 0x0F; // Severity level is 0-15
  compl_workbuf[0] = HOST_SLEEP_SUBCOMMAND_NOTIFY_HOST_STATE;
  compl_workbuf[1] = SAPI_COMMAND_STATUS_SUCCESS;
  compl_workbuf[2] = severity_level & 0x0F;
  switch (host_state) {
    case NOTIFY_HOST_STATE_AWAKE:
      keep_alive_stop_tracking();
      set_host_state(false);
      set_urgent_app_callback(NULL);
      set_keep_alive_callback(NULL);
      gpio_wakeup_host_clear();
      compl_workbuf[1] = SAPI_COMMAND_STATUS_SUCCESS;
      break;
    case NOTIFY_HOST_STATE_SLEEPING:
      app_set_controller_severity_level(severity_level); // If SLEEPING, byte 3 is the severity level, ignored if host state is AWAKE
      host_sleep_context.has_pending_wakeup_frame = false;
      host_sleep_context.has_lost_devices = false;
#ifdef SL_CATALOG_ZW_JAMMING_DETECTION_PRESENT
      host_sleep_context.has_pending_jamming_report = false;
#endif
      set_host_state(true);
      set_urgent_app_callback(urgent_wakeup_callback);
      set_keep_alive_callback(keep_alive_update_node);
      keep_alive_start_tracking();
      compl_workbuf[1] = SAPI_COMMAND_STATUS_SUCCESS;
      break;
    default:
      compl_workbuf[1] = SAPI_COMMAND_STATUS_FAILURE;
      break;
  }
  DoRespond_workbuf(3);
}

static void host_sleep_subcommand_zw_module_capabilities_report(__attribute__((unused)) const comm_interface_frame_ptr frame)
{
  /** HOST->ZW: subcommand 0x03 */
  compl_workbuf[0] = HOST_SLEEP_SUBCOMMAND_ZW_MODULE_CAPABILITIES_REPORT;
  compl_workbuf[1] = ZW_MAX_IMPORTANT_DEVICES;
  compl_workbuf[2] = MAX_DEVICE_COUNT_PER_FRAME;
  DoRespond_workbuf(3);
}

#ifdef SL_CATALOG_ZW_JAMMING_DETECTION_PRESENT
static void host_sleep_subcommand_jamming_report(void)
{
  struct __attribute__((packed)) {
    uint8_t sub_command;
    sl_jamming_detection_statistics_t payload;
  } jamming_packet = {
    .sub_command   = FUNC_ID_PROP_JAMMING_SUBCOMMAND_REPORT,
    .payload = host_sleep_context.jamming_report
  };

  RequestUnsolicited(FUNC_ID_PROP_JAMMING_DETECTION_COMMAND, (uint8_t *)&jamming_packet, sizeof(jamming_packet));
}
#endif

static void host_sleep_subcommand_request_wakeup_report(void)
{
  if (host_sleep_context.has_pending_wakeup_frame) {
#ifndef ZW_CONTROLLER_BRIDGE
    ApplicationCommandHandler(NULL, &host_sleep_context.wakeup_frame_package);
#else
    ApplicationCommandHandler_Bridge(&host_sleep_context.wakeup_frame_package.uReceiveParams.RxMulti);
#endif
    host_sleep_context.has_pending_wakeup_frame = false;
  }

  if (host_sleep_context.has_lost_devices) {
    host_sleep_subcommand_device_lost_report();
    host_sleep_context.has_lost_devices = false;
  }

#ifdef SL_CATALOG_ZW_JAMMING_DETECTION_PRESENT
  if (host_sleep_context.has_pending_jamming_report) {
    host_sleep_context.has_pending_jamming_report = false;
    host_sleep_subcommand_jamming_report();
  }
#endif
}

/**
 * ZW->HOST: subcommand 0x05 | lost_device_count | node_id[0] MSB | node_id[0] LSB | ... | node_id[N] MSB | node_id[N] LSB
 *
 * Scans the important devices list for any device whose elapsed time has
 * reached its keep-alive threshold and sends an unsolicited report.
 * Resets elapsed_min after reporting. Does nothing if no devices are lost.
 */
static void host_sleep_subcommand_device_lost_report(void)
{
  uint8_t lost_count = 0;
  uint8_t offset = 2;

  compl_workbuf[0] = HOST_SLEEP_SUBCOMMAND_DEVICE_LOST_REPORT;

  for (uint8_t i = 0; i < host_sleep_context.total_nodes_count; i++) {
    important_device_t *dev = &host_sleep_context.important_devices[i];
    if (dev->keep_alive_min == 0 || dev->elapsed_min < dev->keep_alive_min) {
      continue;
    }
    compl_workbuf[offset++] = (uint8_t)(dev->node_id >> 8);
    compl_workbuf[offset++] = (uint8_t)(dev->node_id & 0xFF);
    compl_workbuf[offset++] = (uint8_t)(dev->elapsed_min >> 8);
    compl_workbuf[offset++] = (uint8_t)(dev->elapsed_min & 0xFF);
    lost_count++;
    if (lost_count >= MAX_DEVICE_COUNT_PER_FRAME) {
      break;
    }
  }

  if (lost_count == 0) {
    return;
  }

  compl_workbuf[1] = lost_count;
  RequestUnsolicited(FUNC_ID_HOST_SLEEP, compl_workbuf, offset);
  host_sleep_context.has_lost_devices = false;
}

static inline void send_s2_message_count_full_list(void)
{
  uint8_t sent = 0;

  // we should never send more than 4 frames with max list length set to 128
  // so this will be send as 1 response frame + 3 unsolicited frames
  // unsolicited queue is limited to 8 slots so it will be ok with this implementation
  while (sent < host_sleep_context.total_nodes_count) {
    uint8_t remaining = host_sleep_context.total_nodes_count - sent;
    uint8_t count = (remaining > S2_MSG_COUNT_ENTRIES_PER_FRAME)
                    ? S2_MSG_COUNT_ENTRIES_PER_FRAME : remaining;
    uint8_t more_to_follow = (sent + count < host_sleep_context.total_nodes_count) ? 0x01 : 0x00;

    compl_workbuf[0] = HOST_SLEEP_SUBCOMMAND_REQUEST_S2_MESSAGE_COUNT;
    compl_workbuf[1] = count;
    uint8_t offset = 2;
    for (uint8_t i = 0; i < count; i++) {
      important_device_t *dev = &host_sleep_context.important_devices[sent + i];
      compl_workbuf[offset++] = (uint8_t)(dev->node_id >> 8);
      compl_workbuf[offset++] = (uint8_t)(dev->node_id & 0xFF);
      compl_workbuf[offset++] = dev->s2_message_count;
      compl_workbuf[offset++] = dev->s2_last_seqno;
    }
    compl_workbuf[offset++] = more_to_follow;

    if (sent == 0) {
      DoRespond_workbuf(offset);
    } else {
      RequestUnsolicited(FUNC_ID_HOST_SLEEP, compl_workbuf, offset);
    }
    sent += count;
  }

  if (host_sleep_context.total_nodes_count == 0) {
    compl_workbuf[0] = HOST_SLEEP_SUBCOMMAND_REQUEST_S2_MESSAGE_COUNT;
    compl_workbuf[1] = 0;
    DoRespond_workbuf(2);
  }
}

static void host_sleep_subcommand_request_s2_message_count(const comm_interface_frame_ptr frame)
{
  /** HOST->ZW: subcommand 0x06 | node_id[0] MSB | node_id[0] LSB */
  const node_id_t node_id = (uint16_t) GET_16BIT_VALUE(&frame->payload[1]);

  if (node_id == 0) {
    // We need to send the full list
    send_s2_message_count_full_list();
    return;
  }

  compl_workbuf[0] = HOST_SLEEP_SUBCOMMAND_REQUEST_S2_MESSAGE_COUNT;
  for (uint8_t i = 0; i < host_sleep_context.total_nodes_count; i++) {
    if (host_sleep_context.important_devices[i].node_id == node_id) {
      important_device_t *dev = &host_sleep_context.important_devices[i];
      compl_workbuf[1] = 1;
      compl_workbuf[2] = (uint8_t)(dev->node_id >> 8);
      compl_workbuf[3] = (uint8_t)(dev->node_id & 0xFF);
      compl_workbuf[4] = dev->s2_message_count;
      compl_workbuf[5] = dev->s2_last_seqno;
      compl_workbuf[6] = 0x00; // more_to_follow
      DoRespond_workbuf(7);
      return;
    }
  }
  compl_workbuf[1] = 0;
  DoRespond_workbuf(2);
}

ZW_ADD_CMD(FUNC_ID_HOST_SLEEP)
{
  switch (frame->payload[0]) { // Subcommand
    case HOST_SLEEP_SUBCOMMAND_LIST_IMPORTANT_DEVICES:
      host_sleep_subcommand_list_important_devices(frame);
      break;
    case HOST_SLEEP_SUBCOMMAND_CLEAR_IMPORTANT_DEVICES_LIST:
      host_sleep_subcommand_clear_important_devices_list(frame);
      break;
    case HOST_SLEEP_SUBCOMMAND_NOTIFY_HOST_STATE:
      host_sleep_subcommand_notify_host_state(frame);
      break;
    case HOST_SLEEP_SUBCOMMAND_ZW_MODULE_CAPABILITIES_REPORT:
      host_sleep_subcommand_zw_module_capabilities_report(frame);
      break;
    case HOST_SLEEP_SUBCOMMAND_REQUEST_WAKEUP_REPORT:
      set_state_and_notify(stateIdle);
      host_sleep_subcommand_request_wakeup_report();
      break;
    case HOST_SLEEP_SUBCOMMAND_REQUEST_S2_MESSAGE_COUNT:
      host_sleep_subcommand_request_s2_message_count(frame);
      break;
    default:
      compl_workbuf[0] = HOST_SLEEP_SUBCOMMAND_UNKNOWN;
      DoRespond_workbuf(1);
      break;
  }
}

static void urgent_wakeup_callback(const SZwaveReceivePackage *pRxPackage)
{
  if (!is_host_sleeping()) {
    return;
  }

#ifndef ZW_CONTROLLER_BRIDGE
  const node_id_t node_id = pRxPackage->uReceiveParams.Rx.RxOptions.sourceNode;
  const uint8_t * const payload = (uint8_t*) &pRxPackage->uReceiveParams.Rx.Payload;
#else
  const node_id_t node_id = pRxPackage->uReceiveParams.RxMulti.RxOptions.sourceNode;
  const uint8_t * const payload = (uint8_t*) &pRxPackage->uReceiveParams.RxMulti.Payload;
#endif

  s2_message_update_count(node_id, payload);
  if (NULL != pRxPackage && is_important_device(node_id) && !host_sleep_context.has_pending_wakeup_frame) {
    host_sleep_context.wakeup_frame_package = *pRxPackage;
    host_sleep_context.has_pending_wakeup_frame = true;
    gpio_wakeup_host();
  }
}

bool s2_message_update_count(const node_id_t node_id, const uint8_t * const payload)
{
  if (payload == NULL || payload[0] != COMMAND_CLASS_SECURITY_2_V2 || payload[1] != SECURITY_2_MESSAGE_ENCAPSULATION_V2) {
    return false;
  }

  uint8_t seqno = payload[2];

  for (uint8_t i = 0; i < host_sleep_context.total_nodes_count; i++) {
    if (host_sleep_context.important_devices[i].node_id == node_id) {
      if (host_sleep_context.important_devices[i].s2_last_seqno == seqno) {
        // duplicate sequence number
        return false;
      }
      host_sleep_context.important_devices[i].s2_message_count++;
      host_sleep_context.important_devices[i].s2_last_seqno = seqno;
      return true;
    }
    if (host_sleep_context.important_devices[i].node_id == 0) {
      // we've reached the end of the list
      break;
    }
  }
  return false;
}
