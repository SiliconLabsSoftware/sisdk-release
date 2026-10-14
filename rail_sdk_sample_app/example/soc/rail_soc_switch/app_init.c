/***************************************************************************//**
 * @file
 * @brief app_init.c
 *******************************************************************************
 * # License
 * <b>Copyright 2018 Silicon Laboratories Inc. www.silabs.com</b>
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

// -----------------------------------------------------------------------------
//                                   Includes
// -----------------------------------------------------------------------------
#include <stdint.h>
#include <inttypes.h>
#include "sl_component_catalog.h"
#include "sl_common.h"
#include "sl_rail.h"
#include "rail_config.h"
#include "sl_rail_util_init.h"
#include "app_process.h"
#include "sl_rail_sdk_simple_assistance.h"
#include "sl_rail_sdk_channel_selector.h"
#include "sl_clock_manager_oscillator_config.h"

#if defined(SL_CATALOG_KERNEL_PRESENT)
#include "app_task_init.h"
#endif

#if defined(SL_CATALOG_APP_LOG_PRESENT)
#include "app_log.h"
#endif

// -----------------------------------------------------------------------------
//                              Macros and Typedefs
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//                          Static Function Declarations
// -----------------------------------------------------------------------------
/******************************************************************************
 * Checks that HFXO and radio config crystal frequencies match when both are present.
 *****************************************************************************/
static void xtal_frequency_validation_check(void);

// -----------------------------------------------------------------------------
//                                Global Variables
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//                                Static Variables
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//                          Public Function Definitions
// -----------------------------------------------------------------------------

/******************************************************************************
 * Print sample app name
 *****************************************************************************/
SL_WEAK void print_sample_app_name(const char* app_name)
{
#ifdef SL_CATALOG_APP_LOG_PRESENT
  app_log_info("%s\n", app_name);
#endif
  // Avoid unused parameter warning
  (void)app_name;
}

/******************************************************************************
 * The function is used for some basic initialization related to the app.
 *****************************************************************************/
void rail_app_init(void)
{
  xtal_frequency_validation_check();

  // Get RAIL handle, used later by the application
  sl_rail_handle_t rail_handle = sl_rail_util_get_handle(SL_RAIL_UTIL_HANDLE_INST0);

  // Turn OFF LEDs
  clear_receive_led();
  clear_send_led();
  init_display();

  // CLI info message
  print_sample_app_name("Switch");

  // Start reception
  sl_rail_status_t status = sl_rail_start_rx(rail_handle, get_selected_channel(), NULL);
  if (status != SL_RAIL_STATUS_NO_ERROR) {
    app_log_warning("After initialization sl_rail_start_rx() result: 0x%08" PRIX32 "\n ", status);
  }
}

void app_init(void)
{
#if !defined(SL_CATALOG_KERNEL_PRESENT)
  rail_app_init();
#else
  app_task_init();
#endif
}

// -----------------------------------------------------------------------------
//                          Static Function Definitions
// -----------------------------------------------------------------------------
/******************************************************************************
 * Checks that HFXO and radio config crystal frequencies match when both are present.
 *****************************************************************************/
static void xtal_frequency_validation_check(void)
{
#if defined(SL_CLOCK_MANAGER_HFXO_FREQ) && defined(RADIO_CONFIG_XTAL_FREQUENCY)
  _Static_assert(SL_CLOCK_MANAGER_HFXO_FREQ == RADIO_CONFIG_XTAL_FREQUENCY,
                 "SL_CLOCK_MANAGER_HFXO_FREQ must match RADIO_CONFIG_XTAL_FREQUENCY.");
#endif
}
