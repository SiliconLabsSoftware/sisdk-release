/***************************************************************************//**
 * @file
 * @brief Serial Port Profile example - display functions
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

// -----------------------------------------------------------------------------
// Includes

#include <stdio.h>
#include <string.h>

#include "glib.h"
#include "dmd/dmd.h"

#include "app_log.h"
#include "app_display.h"

// -----------------------------------------------------------------------------
// Macros

#define APP_DISPLAY_LINE_LENGTH                15

#define APP_DISPLAY_TITLE_VENDOR_TEXT          "Silicon Labs"
#define APP_DISPLAY_TITLE_CENTRAL_TEXT         "SPP Central"
#define APP_DISPLAY_TITLE_PERIPHERAL_TEXT      "SPP Peripheral"

#define APP_DISPLAY_CONNECTED_TEXT             "Connected"
#define APP_DISPLAY_DISCONNECTED_TEXT          "Disconnected"

// -----------------------------------------------------------------------------
// Enums, structs, typedefs

// Enum type for UI rows
typedef enum {
  ROW_VENDOR = 0,
  ROW_ROLE,
  ROW_STATE
} display_row;

// -----------------------------------------------------------------------------
// Static function declarations

static void app_display_clear_row(const uint8_t row);

// -----------------------------------------------------------------------------
// Static variables

static GLIB_Context_t glib_context;

// -----------------------------------------------------------------------------
// Private function definitions

/******************************************************************************
 * Clear the specified row on the display
 *
 * @param[in] row row to clear
 *****************************************************************************/
static void app_display_clear_row(const uint8_t row)
{
  const char empty[] = "                    ";
  GLIB_drawStringOnLine(&glib_context,
                        empty,
                        row,
                        GLIB_ALIGN_LEFT,
                        0,
                        0,
                        true);
  DMD_updateDisplay();
}

// -----------------------------------------------------------------------------
// Public function definitions

/******************************************************************************
 * Initialize the display driver
 *****************************************************************************/
sl_status_t app_display_init(void)
{
  EMSTATUS status;

  status = DMD_init(0);
  if (status != DMD_OK) {
    app_log_error("DMD_init failed! [E:0x%lx]" APP_LOG_NL, status);
    return SL_STATUS_INITIALIZATION;
  }

  status = GLIB_contextInit(&glib_context);
  if (status != GLIB_OK) {
    app_log_error("GLIB_contextInit failed! [E:0x%lx]" APP_LOG_NL, status);
    return SL_STATUS_INITIALIZATION;
  }

  glib_context.backgroundColor = White;
  glib_context.foregroundColor = Black;

  status = GLIB_clear(&glib_context);
  if (status != GLIB_OK) {
    app_log_error("Failed to clear display. [E:0x%lx]" APP_LOG_NL, status);
  }

  status = GLIB_setFont(&glib_context, (GLIB_Font_t *)&GLIB_FontNormal8x8);
  if (status != GLIB_OK) {
    app_log_error("Failed to set font. [E:0x%lx]" APP_LOG_NL, status);
  }

  app_display_write_text(APP_DISPLAY_TITLE_VENDOR_TEXT, ROW_VENDOR);

  DMD_updateDisplay();

  return status;
}

/******************************************************************************
 * Print the node role on the screen
 *
 * @param[in] spp_role role of the node
 *****************************************************************************/
void app_display_print_role(const spp_role_t spp_role)
{
  if (spp_role == SPP_PERIPHERAL) {
    app_display_write_text(APP_DISPLAY_TITLE_PERIPHERAL_TEXT, ROW_ROLE);
  } else {
    app_display_write_text(APP_DISPLAY_TITLE_CENTRAL_TEXT, ROW_ROLE);
  }

  DMD_updateDisplay();
}

/******************************************************************************
 * Print connection status on the screen
 *
 * @param[in] connected represents whether the SPP node is connected or not
 *****************************************************************************/
void app_display_connected(const bool connected)
{
  if (connected) {
    app_display_write_text(APP_DISPLAY_CONNECTED_TEXT, ROW_STATE);
  } else {
    app_display_write_text(APP_DISPLAY_DISCONNECTED_TEXT, ROW_STATE);
  }

  DMD_updateDisplay();
}

/******************************************************************************
 * Write string to a specified row.
 *****************************************************************************/
void app_display_write_text(const char *str, uint8_t row)
{
  if (strlen(str) == 0) {
    return;
  }
  app_display_clear_row(row);
  GLIB_drawStringOnLine(&glib_context,
                        str,
                        row,
                        GLIB_ALIGN_LEFT,
                        0,
                        0,
                        true);
}
