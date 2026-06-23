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
#ifndef APP_DISPLAY_H
#define APP_DISPLAY_H

// -----------------------------------------------------------------------------
// Includes

#include <stdio.h>
#include <string.h>
#include "spp.h"

#ifdef __cplusplus
extern "C"
{
#endif

// -----------------------------------------------------------------------------
// Function declarations

/**************************************************************************//**
 * Initialize the display driver
 *****************************************************************************/
sl_status_t app_display_init(void);

/**************************************************************************//**
 * Print the node role on the screen
 *
 * @param[in] spp_role role of the node
 *****************************************************************************/
void app_display_print_role(const spp_role_t spp_role);

/**************************************************************************//**
 * Print connection status on the screen
 *
 * @param[in] connected represents whether the SPP node is connected or not
 *****************************************************************************/
void app_display_connected(const bool connected);

/******************************************************************************
 * Write string to a specified row.
 *
 * @param[in] str pointer to the text to print
 * @param[in] row row to print the text on
 *****************************************************************************/
void app_display_write_text(const char *str, uint8_t row);

#ifdef __cplusplus
}
#endif

#endif // APP_DISPLAY_H
