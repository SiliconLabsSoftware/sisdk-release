/**
 * @file
 * Handler for Command Class Wake On Critical Message.
 * @copyright 2026 Silicon Laboratories Inc.
 */

/****************************************************************************/
/*                              INCLUDE FILES                               */
/****************************************************************************/
#include <assert.h>
#include <ZW_TransportEndpoint.h>
#include <ZW_TransportMulticast.h>
#include <ZAF_Common_interface.h>
#include "CC_WakeOnCriticalMessage.h"
#include "ZAF_types.h"
#include <CC_Common.h>
#include <ZAF_nvm.h>
#include <ZAF_file_ids.h>
#include <ZW_TransportSecProtocol.h>
#include "association_plus_base.h"

/****************************************************************************/
/*                              PRIVATE DATA                                */
/****************************************************************************/

typedef struct wocm_nvm_t_ {
  uint16_t node_id;
  uint8_t severity;
} wocm_nvm_t;

/****************************************************************************/
/*                              EXPORTED DATA                               */
/****************************************************************************/

/****************************************************************************/
/*                            PRIVATE FUNCTIONS                             */
/****************************************************************************/

/**
 * Retrieve the node ID of the destination configured in the Lifeline
 * association group (group 1).
 *
 * The Wake On Critical Message Notify encapsulation must target the Lifeline
 * destination (the node the device reports to, typically the controller /
 * gateway) rather than whichever node happened to send the Configuration Set.
 *
 * @return Lifeline destination node ID, or 0 if the Lifeline group is empty.
 */
static node_id_t get_lifeline_node_id(void)
{
  destination_info_t *p_node_list = NULL;
  uint8_t list_length = 0;
  NODE_LIST_STATUS status =
    handleAssociationGetnodeList(LIFELINE_GROUP_ID, LIFELINE_ENDPOINT_ALLOWED, &p_node_list, &list_length);
  if (NODE_LIST_STATUS_SUCCESS == status && NULL != p_node_list && list_length > 0) {
    return p_node_list->node.nodeId;
  }
  return 0;
}

static void send_severity_to_protocol_task(const node_id_t node_id, const uint8_t severity_level)
{
  SZwaveCommandPackage cmdPackage = {
    .eCommandType = EZWAVECOMMANDTYPE_SET_SEVERITY_LEVEL,
    .uCommandParams.SetSeverityLevel.nodeID = node_id,
    .uCommandParams.SetSeverityLevel.severity_level = severity_level
  };
  __attribute__((unused)) EQueueNotifyingStatus QueueStatus =
    QueueNotifyingSendToBack(ZAF_getZwCommandQueue(), (uint8_t *)&cmdPackage, 0);
  assert(EQUEUENOTIFYING_STATUS_SUCCESS == QueueStatus);
}

static bool nvm_wocm_data_write(wocm_nvm_t *wocm_nvm)
{
  return ZPAL_STATUS_OK == ZAF_nvm_write(ZAF_FILE_ID_CC_WOCM, wocm_nvm, sizeof(*wocm_nvm));
}

static bool nvm_wocm_data_read(wocm_nvm_t *wocm_nvm)
{
  return ZPAL_STATUS_OK == ZAF_nvm_read(ZAF_FILE_ID_CC_WOCM, wocm_nvm, sizeof(*wocm_nvm));
}

/**
 * Retrieve the severity level from the protocol task via the command queue /
 * command-status queue round-trip.
 *
 * @param[out] severity  Pointer where the retrieved severity level is stored.
 */
static void retrieve_severity_from_protocol_task(uint8_t *severity)
{
  SApplicationHandles *pAppHandles = ZAF_getAppHandle();
  QueueHandle_t statusQueue = pAppHandles->ZwCommandStatusQueue;

  SZwaveCommandPackage cmdPackage = {
    .eCommandType = EZWAVECOMMANDTYPE_GET_SEVERITY_LEVEL,
  };
  __attribute__((unused)) EQueueNotifyingStatus QueueStatus =
    QueueNotifyingSendToBack(ZAF_getZwCommandQueue(), (uint8_t *)&cmdPackage, 0);
  assert(EQUEUENOTIFYING_STATUS_SUCCESS == QueueStatus);

  SZwaveCommandStatusPackage cmdStatus = { 0 };
  while (true) {
    __attribute__((unused)) BaseType_t rxStatus = xQueueReceive(statusQueue, (uint8_t *)&cmdStatus, portMAX_DELAY);
    assert(pdTRUE == rxStatus);
    if (cmdStatus.eStatusType == EZWAVECOMMANDSTATUS_GET_SEVERITY_LEVEL) {
      *severity = cmdStatus.Content.GetSeverityLevelStatus.result;
      return;
    }
    /* Re-insert non-matching message */
    __attribute__((unused)) BaseType_t result = xQueueSendToBack(statusQueue, (uint8_t *)&cmdStatus, 0);
    assert(pdTRUE == result);
  }
}

static received_frame_status_t
CC_WakeOnCriticalMessage_handler(
  cc_handler_input_t * input,
  cc_handler_output_t * output)
{
  if (input->rx_options->securityKey != GetHighestSecureLevel(ZAF_GetSecurityKeys())) {
    return RECEIVED_FRAME_STATUS_NO_SUPPORT;
  }
  switch (input->frame->ZW_Common.cmd) {
    case COMMAND_WAKE_ON_CRITICAL_MESSAGE_CONFIGURATION_SET:
    {
      if (input->length < sizeof(ZW_WAKE_ON_CRITICAL_MESSAGE_CONFIGURATION_SET_FRAME)) {
        return RECEIVED_FRAME_STATUS_FAIL;
      }

      const uint8_t *raw = (const uint8_t *)input->frame;
      uint8_t severity = raw[2] & WAKE_ON_CRITICAL_MESSAGE_SEVERITY_MASK;

      /* Store the Lifeline destination rather than the sender of this frame, so
       * that WoCM Notify encapsulation later targets the node the device
       * actually reports to. */
      node_id_t node_id = get_lifeline_node_id();
      if (0 == node_id) {
        // Fallback to configuring nodeID in case of no Lifeline configured.
        node_id = input->rx_options->sourceNode.nodeId;
      }
      wocm_nvm_t wocm_nvm = {
        .node_id = node_id,
        .severity = severity
      };
      nvm_wocm_data_write(&wocm_nvm);
      send_severity_to_protocol_task(node_id, severity);

      return RECEIVED_FRAME_STATUS_SUCCESS;
    }

    case COMMAND_WAKE_ON_CRITICAL_MESSAGE_CONFIGURATION_GET:
    {
      if (true == Check_not_legal_response_job(input->rx_options)) {
        return RECEIVED_FRAME_STATUS_FAIL;
      }

      uint8_t severity;
      retrieve_severity_from_protocol_task(&severity);

      uint8_t *raw_out = (uint8_t *)output->frame;

      raw_out[0] = COMMAND_CLASS_WAKE_ON_CRITICAL_MESSAGE;
      raw_out[1] = COMMAND_WAKE_ON_CRITICAL_MESSAGE_CONFIGURATION_REPORT;
      raw_out[2] = severity & WAKE_ON_CRITICAL_MESSAGE_SEVERITY_MASK;

      output->length = sizeof(ZW_WAKE_ON_CRITICAL_MESSAGE_CONFIGURATION_REPORT_FRAME);

      return RECEIVED_FRAME_STATUS_SUCCESS;
    }

    default:
      break;
  }

  return RECEIVED_FRAME_STATUS_NO_SUPPORT;
}

static void init(void)
{
  wocm_nvm_t wocm_nvm = {
    .node_id = 0,
    .severity = WAKE_ON_CRITICAL_MESSAGE_SEVERITY_DEFAULT
  };
  if (nvm_wocm_data_read(&wocm_nvm)) {
    wocm_nvm.severity &= WAKE_ON_CRITICAL_MESSAGE_SEVERITY_MASK;
  } else {
    wocm_nvm.node_id = 0;
    wocm_nvm.severity = WAKE_ON_CRITICAL_MESSAGE_SEVERITY_DEFAULT;
  }
  send_severity_to_protocol_task(wocm_nvm.node_id, wocm_nvm.severity);
}

static void reset(void)
{
  wocm_nvm_t wocm_nvm = {
    .node_id = 0,
    .severity = WAKE_ON_CRITICAL_MESSAGE_SEVERITY_DEFAULT
  };
  nvm_wocm_data_write(&wocm_nvm);
  send_severity_to_protocol_task(wocm_nvm.node_id, wocm_nvm.severity);
}

/****************************************************************************/
/*                           EXPORTED FUNCTIONS                             */
/****************************************************************************/

uint8_t CC_WakeOnCriticalMessage_getSeverityThreshold(void)
{
  uint8_t severity;
  retrieve_severity_from_protocol_task(&severity);
  return severity;
}

/**************************************************************************************************
 * Linker magic - Creates a section for an array of registered CCs and mapped CCs to the Basic CC.
 *************************************************************************************************/

REGISTER_CC_V5(COMMAND_CLASS_WAKE_ON_CRITICAL_MESSAGE, COMMAND_CLASS_WAKE_ON_CRITICAL_MESSAGE_VERSION_V1, CC_WakeOnCriticalMessage_handler, NULL, NULL, NULL, 0, init, reset);
