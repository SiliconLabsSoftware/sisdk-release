/*****************************************************************************/
/**
 * Copyright 2021 Silicon Laboratories, Inc.
 *
 *****************************************************************************/
//
// *** Generated file. Do not edit! ***
//
// Description: Handlers for the EZSP frames that directly correspond to Ember
// API calls.

#include PLATFORM_HEADER
#include "stack/include/sl_zigbee_types.h"
#include "stack/internal/inc/internal-defs-patch.h"
#include "ezsp-enum.h"
#include "app/em260/command-context.h"
#include "stack/include/cbke-crypto-engine.h"
#include "stack/include/zigbee-security-manager.h"
#include "stack/internal/inc/mfglib_internal_def.h"
#include "stack/include/binding-table.h"
#include "stack/include/message.h"
#include "stack/include/mac-layer.h"
#include "app/util/ezsp/ezsp-frame-utilities.h"
#include "app/em260/command-handlers-cbke.h"
#include "app/em260/command-handlers-binding.h"
#include "app/em260/command-handlers-mfglib.h"
#include "app/em260/command-handlers-security.h"
#include "app/em260/command-handlers-zll.h"
#include "app/em260/command-handlers-zigbee-pro.h"
#include "child.h"
#include "message.h"
#include "zll-api.h"
#include "security.h"
#include "stack-info.h"
#include "network-formation.h"
#include "zigbee-device-stack.h"
#include "sl_zigbee_duty_cycle.h"
#include "multi-phy.h"
#include "stack/include/gp-sink-table.h"
#include "stack/include/gp-proxy-table.h"
#include "stack/include/source-route.h"
#include "stack/include/multi-network.h"
#include "stack/include/sl_zigbee_dhc.h"
#include "app/framework/plugin/dhc/dhc-ncp.h"

bool sli_zigbee_af_process_ezsp_command_configuration(uint16_t commandId)
{
  switch (commandId) {
//------------------------------------------------------------------------------

    case SL_ZIGBEE_EZSP_SET_PENDING_NETWORK_UPDATE_PAN_ID: {
      uint16_t panId;
      panId = fetchInt16u();
      sli_zigbee_stack_set_pending_network_update_pan_id(panId);
      break;
    }

    case SL_ZIGBEE_EZSP_SET_PENDING_NETWORK_UPDATE_CHANNEL: {
      uint8_t channel;
      channel = fetchInt8u();
      sli_zigbee_stack_set_pending_network_update_channel(channel);
      break;
    }

    case SL_ZIGBEE_EZSP_GET_ENDPOINT: {
      uint8_t endpoint;
      uint8_t index;
      index = fetchInt8u();
      endpoint = sli_zigbee_stack_get_endpoint(index);
      appendInt8u(endpoint);
      break;
    }

    case SL_ZIGBEE_EZSP_GET_ENDPOINT_COUNT: {
      uint8_t count;
      count = sli_zigbee_stack_get_endpoint_count();
      appendInt8u(count);
      break;
    }

    case SL_ZIGBEE_EZSP_GET_ENDPOINT_DESCRIPTION: {
      bool success;
      uint8_t endpoint;
      sl_zigbee_endpoint_description_t result;
      endpoint = fetchInt8u();
      success = sli_zigbee_stack_get_endpoint_description(endpoint, &result);
      appendInt8u(success);
      append_sl_zigbee_endpoint_description_t(&result);
      break;
    }

    case SL_ZIGBEE_EZSP_GET_ENDPOINT_CLUSTER: {
      uint16_t endpoint_cluster;
      uint8_t endpoint;
      uint8_t listId;
      uint8_t listIndex;
      endpoint = fetchInt8u();
      listId = fetchInt8u();
      listIndex = fetchInt8u();
      endpoint_cluster = sli_zigbee_stack_get_endpoint_cluster(endpoint, listId, listIndex);
      appendInt16u(endpoint_cluster);
      break;
    }

//------------------------------------------------------------------------------

    default: {
      return false;
    }
  }

  return true;
}
