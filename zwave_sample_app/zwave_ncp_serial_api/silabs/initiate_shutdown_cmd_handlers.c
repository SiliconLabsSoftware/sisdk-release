/**
 * @file
 * @brief INITIATE_SHUTDOWN (0xD9) Serial API command handler (Silicon Labs targets).
 * @copyright 2026 Silicon Laboratories Inc.
 */

 #include "app.h"

#if SUPPORT_ZW_INITIATE_SHUTDOWN

#include <em_core.h>
#include <nvm3_default.h>
#include <AppTimer.h>
#include <zpal_misc.h>
#include <zpal_watchdog.h>
#include "cmd_handlers.h"
#include "cmds_management.h"
#include "comm_interface.h"
#include "SerialAPI.h"

/*
 * HOST->ZW
 * ZW-HOST 0x01
 */
ZW_ADD_CMD(FUNC_ID_ZW_INITIATE_SHUTDOWN)
{
  AppTimerStopAll();
  if (InitiateShutdown(NULL)) {
    CORE_CRITICAL_SECTION
    (
      nvm3_close(nvm3_defaultHandle);
    )
    zpal_enable_watchdog(false);
    DoRespond(SAPI_COMMAND_STATUS_SUCCESS);
    comm_interface_wait_transmit_done();
    zpal_disable_interrupts();
    while (1) {
    }            // Halt execution after disabling interrupts
  } else {
    DoRespond(SAPI_COMMAND_STATUS_FAILURE);
  }
}

#endif /* SUPPORT_ZW_INITIATE_SHUTDOWN */
