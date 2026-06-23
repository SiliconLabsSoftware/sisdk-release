/**
 * @file
 * @brief Network learn source file
 * @copyright 2019 Silicon Laboratories Inc.
 */

#include "ZAF_network_learn.h"
#include "ZW_application_transport_interface.h"
#include "ZAF_Common_interface.h"
#include "zpal_log.h"

void ZAF_setNetworkLearnMode(E_NETWORK_LEARN_MODE_ACTION bMode)
{
  SApplicationHandles* pAppHandle;

  pAppHandle = ZAF_getAppHandle();

  SZwaveCommandPackage CommandPackage = {
    .eCommandType = EZWAVECOMMANDTYPE_NETWORK_LEARN_MODE_START,
    .uCommandParams.SetSmartStartLearnMode.eLearnMode = bMode
  };
  if (EQUEUENOTIFYING_STATUS_SUCCESS != QueueNotifyingSendToBack(pAppHandle->pZwCommandQueue, (uint8_t*)&CommandPackage, 0)) {
    ZPAL_LOG_ERROR(ZPAL_LOG_ZAF_COMMON, "Network learn mode command could not be queued (mode=%u)", (unsigned)bMode);
  }
}
