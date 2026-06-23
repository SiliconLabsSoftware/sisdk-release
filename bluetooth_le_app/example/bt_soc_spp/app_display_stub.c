/***************************************************************************//**
 * @file
 * @brief Serial Port Profile example - display stub functions
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
#include "app_display.h"

// -----------------------------------------------------------------------------
// Public function definitions

/**************************************************************************//**
 * Initialize the display driver
 *****************************************************************************/
sl_status_t app_display_init(void)
{
  return SL_STATUS_OK;
}

/**************************************************************************//**
 * Print the node role on the screen
 *
 * @param[in] spp_role role of the node
 *****************************************************************************/
void app_display_print_role(const spp_role_t spp_role)
{
  (void)spp_role;
}

/**************************************************************************//**
 * Print SPP connection status on the screen
 *
 * @param[in] connected represents whether the SPP node is connected or not
 *****************************************************************************/
void app_display_connected(const bool connected)
{
  (void)connected;
}

/******************************************************************************
 * Write string to a specified row.
 *****************************************************************************/
void app_display_write_text(const char *str, uint8_t row)
{
  (void)str;
  (void)row;
}
