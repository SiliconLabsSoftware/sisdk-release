/***************************************************************************//**
 * @file
 * @brief app_process.h
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
#ifndef APP_PROCESS_H
#define APP_PROCESS_H

// -----------------------------------------------------------------------------
//                                   Includes
// -----------------------------------------------------------------------------
#include <stdint.h>
#include <stdbool.h>

// -----------------------------------------------------------------------------
//                              Macros and Typedefs
// -----------------------------------------------------------------------------

/// State machine of Switch
typedef enum {
  SWITCH_STATE_SCAN,
  SWITCH_STATE_LINKED,
} switch_app_state_t;

/// The state of the Light's state machine
typedef enum {
  LIGHT_STATE_ADVERTISE,
  LIGHT_STATE_READY,
} light_app_state_t;

/// Indicates the control role of the device
typedef enum {
  DEMO_CONTROL_ROLE_LIGHT,
  DEMO_CONTROL_ROLE_SWITCH,
} demo_control_role_t;

/// Indicates the command
typedef enum {
  CMD_TYPE_LIGHT_ADVERTISE = 0,
  CMD_TYPE_LIGHT_TOGGLE = 1,
  CMD_TYPE_LIGHT_BULB_STATE_REPORT = 2,
  CMD_TYPE_LIGHT_BULB_STATE_GET = 3,
} demo_control_command_type_t;
// -----------------------------------------------------------------------------
//                                Global Variables
// -----------------------------------------------------------------------------
extern bool light_bulb_toggle_required;
extern bool state_change_required;
// -----------------------------------------------------------------------------
//                          Public Function Declarations
// -----------------------------------------------------------------------------

/*******************************************************************************
 * Application state machine, called infinitely
 ******************************************************************************/
void app_process_action(void);

/**************************************************************************//**
 * Initialize the LCD Display at the beginning of the application
 *****************************************************************************/
void init_display(void);

#endif // APP_PROCESS_H
