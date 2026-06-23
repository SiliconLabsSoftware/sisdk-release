/***************************************************************************//**
 * @file
 * @brief Watchdog Manager Power Manager Integration
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * SPDX-License-Identifier: Zlib
 *
 * The licensor of this software is Silicon Laboratories Inc.
 *
 * This software is provided 'as-is', without any express or implied
 * warranty. In no event will the authors be held liable for any damages
 * arising from the use of this software.
 *
 * Permission is granted to anyone to use this software for any purpose,
 * including commercial applications, and to alter it and redistribute it
 * freely, subject to the following restrictions:
 *
 * 1. The origin of this software must not be misrepresented; you must not
 *    claim that you wrote the original software. If you use this software
 *    in a product, an acknowledgment in the product documentation would be
 *    appreciated but is not required.
 * 2. Altered source versions must be plainly marked as such, and must not be
 *    misrepresented as being the original software.
 * 3. This notice may not be removed or altered from any source distribution.
 *
 ******************************************************************************/

#include "sli_watchdog_manager_hal.h"

#if SLI_WATCHDOG_MANAGER_USE_EM_TRANSITION_HOOK
#include "sl_power_manager.h"

/***************************************************************************//**
 * @addtogroup watchdog_manager
 * @{
 ******************************************************************************/

/*******************************************************************************
 **************************   LOCAL DATA   ************************************
 ******************************************************************************/

static sl_power_manager_em_transition_event_handle_t em_transition_handle;
static void watchdog_em_transition_callback(sl_power_manager_em_t from,
                                           sl_power_manager_em_t to);

static const sl_power_manager_em_transition_event_info_t em_transition_info = {
  .event_mask = SL_POWER_MANAGER_EVENT_TRANSITION_ENTERING_EM0
                | SL_POWER_MANAGER_EVENT_TRANSITION_LEAVING_EM0,
  .on_event = watchdog_em_transition_callback,
};

/*******************************************************************************
 **************************   LOCAL FUNCTIONS   ********************************
 ******************************************************************************/

static void watchdog_em_transition_callback(sl_power_manager_em_t from,
                                            sl_power_manager_em_t to)
{
  sli_watchdog_manager_hal_on_em_transition((uint8_t)from, (uint8_t)to);
}

/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/

/***************************************************************************//**
 * Subscribe to power manager EM transition events for disable/enable of
 * hardware watchdog when EM1/2/3 run is not all supported. Called once from
 * sl_watchdog_manager_start().
 ******************************************************************************/
void sli_watchdog_manager_power_subscribe_em_transition(void)
{
  static bool subscribed = false;

  if (subscribed) {
    return;
  }

  sl_power_manager_subscribe_em_transition_event(&em_transition_handle, &em_transition_info);
  subscribed = true;
}
/** @} (end addtogroup watchdog_manager) */
#endif /* SLI_WATCHDOG_MANAGER_USE_EM_TRANSITION_HOOK */
