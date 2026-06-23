/***************************************************************************//**
 * @file
 * @brief app_process.c
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
#include "printf.h"
#include "app_log.h"
#include "sl_rail_util_init.h"
#include "sl_simple_led_instances.h"
#include "sl_rail.h"
#include "app_process.h"
#include "sl_simple_button_instances.h"
#include "demo-ui.h"
#include "em_device.h"
#if defined _SILICON_LABS_32B_SERIES_2
#include "em_system.h"
#else
#include "sl_hal_system.h"
#endif
#include "sl_core.h"
#include "sl_rail_sdk_light_switch_support.h"
#include "sl_rail_sdk_packet_assistant.h"
#include "sl_rail_sdk_fifo_size_config.h"
#include "sl_rail_sdk_channel_selector.h"
#include "sl_code_classification.h"

#if defined(SL_CATALOG_KERNEL_PRESENT)
#include "app_task_init.h"
#endif

#include "cmsis_compiler.h"

// -----------------------------------------------------------------------------
//                              Macros and Typedefs
// -----------------------------------------------------------------------------
/// DEVICE_TYPE used in LCD functions
#define DEVICE_TYPE "Switch"

// Variable for keeping the states consistent in both devices
/// this structure contains the Light module's details
typedef struct {
  uint8_t addr[8];
  int8_t rssi_dbm;
  bool is_light_on;
  demo_control_command_type_t last_response_type;
  light_app_state_t state;
} light_t;

/// This structure contains the Switch module's details
typedef struct {
  switch_app_state_t state;
  char *switch_text[2];
  char switch_text_buffer[10];
  bool is_paired;
} switch_t;

// -----------------------------------------------------------------------------
//                          Static Function Declarations
// -----------------------------------------------------------------------------

/**************************************************************************//**
 * Prepare the communication state and the Light's ID in order to display it
 *****************************************************************************/
static void write_ID_to_buffer(void);

/**************************************************************************//**
 * Copy the Light's address to the TX FIFO
 *****************************************************************************/
static void copy_light_address_to_payload(void);

/**************************************************************************//**
 * Check if an advertise message come from the Light device
 * @return the advertisement type came from the Light device
 *****************************************************************************/
static demo_control_command_type_t get_light_response_type(const uint8_t* rx_fifo);

/**************************************************************************//**
 * Get light mode from the rx_fifo
 *
 * @param[out] rx_fifo with the received message
 * @return the light bulb's state: ON / OFF
 *****************************************************************************/
static bool get_light_bulb_state(const uint8_t* rx_fifo);

/**************************************************************************//**
 * Update the RSSI an ID values of the Light module
 *****************************************************************************/
static void update_light_RSSI(void);

/**************************************************************************//**
 * Receive the wireless packet, and save it in a buffer
 *
 * @param[in] rail_handle
 *****************************************************************************/
static void save_received_packet(sl_rail_handle_t rail_handle);

/**************************************************************************//**
 * Set the actual state in the transmit buffer
 *****************************************************************************/
static void set_switch_state_in_payload(void);

/**************************************************************************//**
 * Display the app name, light state, and the ID of the connected Light node
 *****************************************************************************/
static void display_all_information(void);
/**************************************************************************//**
 * Send a wireless pocket
 *
 * @param[in] rail_handle
 *****************************************************************************/
static void transmit_packet(sl_rail_handle_t rail_handle);

/**************************************************************************//**
 * Get the communication state of the Light node, if possible (if it is a new Light)
 *****************************************************************************/
static void get_light_state_from_rx_fifo(void);

/**************************************************************************//**
 * Write to CLI the change of the Light state
 *****************************************************************************/
static void cli_log_state_machine_change(void);

/**************************************************************************//**
 * Write to CLI the change of the Light state
 *****************************************************************************/
static void cli_log_light_side_light_bulb_toggle(void);
/**************************************************************************//**
 * Write to CLI the change of the Switch state
 *****************************************************************************/
static void cli_log_switch_side_light_bulb_toggle(void);

/**************************************************************************//**
 * Check if the Switch and Light nodes are connected
 *****************************************************************************/
static void check_paired_state(void);

// -----------------------------------------------------------------------------
//                                Global Variables
// -----------------------------------------------------------------------------
// Light bulb toggle required from from CLI command
bool light_bulb_toggle_required = false;
//State change in the State machine required from CLI command
bool state_change_required = false;

// -----------------------------------------------------------------------------
//                                Static Variables
// -----------------------------------------------------------------------------
static light_t light_module = {
  .addr = { 0 },
  .rssi_dbm = -128,
  .is_light_on = false,
};

static switch_t switch_module = {
  .state = SWITCH_STATE_SCAN,
  .switch_text = { "SCAN:", "LINK:" },
  .is_paired = false,
};

/// Contains the last RAIL Rx/Tx error events
static volatile uint64_t current_rail_err = 0;

/// Contains the received packet's details
static sl_rail_rx_packet_details_t rxPacketDetails;

/// Transmit packet
static uint8_t out_packet[TX_PAYLOAD_LENGTH] = {
  0x0F, 0x16, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66,
  0x77, 0x88, 0x99, 0xAA, 0xBB, 0xCC, 0x00, 0x00,
};

static uint8_t rx_buffer[SL_RAIL_SDK_RX_FIFO_SIZE];
static uint8_t *start_of_packet = &rx_buffer[0];

/// App_name used in LCD functions
static uint8_t app_name[7] = "Switch";
// Increase value if packet has received, decrease after process it
static volatile bool packet_received = false;
// Indicates a button push on the board
static bool button_was_pushed = false;
// Hold information about the incoming message
static sl_rail_rx_packet_info_t packet_info;
// Status indicator of the RAIL API calls
static sl_rail_status_t rail_status;

// -----------------------------------------------------------------------------
//                          Public Function Definitions
// -----------------------------------------------------------------------------

/******************************************************************************
 * Application state machine, called infinitely
 *****************************************************************************/
void app_process_action(void)
{
  // Get RAIL handle, used later by the application
  sl_rail_handle_t rail_handle = sl_rail_util_get_handle(SL_RAIL_UTIL_HANDLE_INST0);

  if (current_rail_err != 0) {
    app_log_error("RAIL Error occurred\nEvents: 0x%" PRIX64 "\n", current_rail_err);
    current_rail_err = 0;
  }
  if (state_change_required) {
    state_change_required = false;
    switch (switch_module.state) {
      case SWITCH_STATE_LINKED:
        switch_module.state = SWITCH_STATE_SCAN;
        break;
      case SWITCH_STATE_SCAN:
        switch_module.state = SWITCH_STATE_LINKED;
        break;
    }
    cli_log_state_machine_change();
    check_paired_state();
    display_all_information();
  }

  switch (switch_module.state) {
    case SWITCH_STATE_SCAN:
      if (packet_received) {
        packet_received = false;
        save_received_packet(rail_handle);
        // Get the highest Light node based on the  Received Signal Strength Indicator
        update_light_RSSI();
        // Display the data
        display_all_information();
        get_light_state_from_rx_fifo();
      }
      break;

    case SWITCH_STATE_LINKED:
      // If there is any received message, process it
      if (packet_received) {
        packet_received = false;
        save_received_packet(rail_handle);
        get_light_state_from_rx_fifo();
        // If Switch side button push happened
        if (button_was_pushed) {
          button_was_pushed = false;
          light_module.is_light_on = get_light_bulb_state(start_of_packet);
          cli_log_switch_side_light_bulb_toggle();
          // If not, but according to the incoming message,
          // light bulb should toggle
        } else if (light_module.is_light_on != get_light_bulb_state(start_of_packet)) {
          light_module.is_light_on = get_light_bulb_state(start_of_packet);
          cli_log_light_side_light_bulb_toggle();
        }
        display_all_information();
        check_paired_state();
      }
      if (light_bulb_toggle_required) {
        light_bulb_toggle_required = false;
        button_was_pushed = true;
        transmit_packet(rail_handle);
        display_all_information();
      }
      break;
  }
}

/******************************************************************************
 * RAIL callback, called if a RAIL event occurs.
 *****************************************************************************/
SL_CODE_RAM void sl_rail_util_on_event(sl_rail_handle_t rail_handle, sl_rail_events_t events)
{
  // Handle Rx events
  if ( events & SL_RAIL_EVENTS_RX_COMPLETION ) {
    if (events & SL_RAIL_EVENT_RX_PACKET_RECEIVED) {
      // Keep the packet in the radio buffer, download it later at the state machine
      sl_rail_hold_rx_packet(rail_handle);
      packet_received = true;
    } else {
      // Handle Rx error
      current_rail_err |= (events & SL_RAIL_EVENTS_RX_COMPLETION);
    }
  }
  // Handle Tx events
  if ( events & SL_RAIL_EVENTS_TX_COMPLETION) {
    if (!(events & SL_RAIL_EVENT_TX_PACKET_SENT)) {
      // Handle Tx error
      current_rail_err |= (events & SL_RAIL_EVENTS_TX_COMPLETION);
    }
  }
#if defined(SL_CATALOG_KERNEL_PRESENT)
  app_task_notify();
#endif
}

/******************************************************************************
 * Button callback, called if any button is pressed or released.
 *****************************************************************************/
SL_CODE_RAM void sl_button_on_change(const sl_button_t *handle)
{
  // Check if any button was pressed
  if (sl_button_get_state(handle) == SL_SIMPLE_BUTTON_PRESSED) {
    if (&sl_button_btn0 == handle) {
      light_bulb_toggle_required = true;
    }
    if (&sl_button_btn1 == handle) {
      state_change_required = true;
    }
  }
#if defined(SL_CATALOG_KERNEL_PRESENT)
  app_task_notify();
#endif
}

/******************************************************************************
 * Initialize the display at the beginning of the application
 *****************************************************************************/
void init_display(void)
{
  demoUIInit();
  display_all_information();
  set_EUI(&out_packet[PACKET_HEADER_LEN]);
}

// -----------------------------------------------------------------------------
//                          Static Function Definitions
// -----------------------------------------------------------------------------

/******************************************************************************
 * Check if the Switch and Light nodes are connected
 *****************************************************************************/
static void check_paired_state(void)
{
  // If Light node is in READY mode and Switch node is in LINKED mode
  bool light_is_ready =
    (start_of_packet[DEVICE_STATUS_PAYLOAD_BYTE] & DEVICE_STATUS_LIGHT_STATE_BIT);
  bool switch_is_linked = (switch_module.state == SWITCH_STATE_LINKED);
  bool is_paired = light_is_ready && switch_is_linked;

  if (switch_module.is_paired != is_paired) {
    switch_module.is_paired = is_paired;
    app_log_info(
      "NODES ARE IN %s STATE\n",
      (is_paired == true) ? "PAIRED " : "NOT PAIRED "
      );
  }
}
/******************************************************************************
 * Write to CLI the change of the Light state
 *****************************************************************************/
static void cli_log_state_machine_change(void)
{
#if defined(_SILICON_LABS_32B_SERIES_2)
  uint64_t sys_id = SYSTEM_GetUnique();
#else
  uint64_t sys_id = sl_hal_system_get_unique();
#endif
  app_log_info(
    "State changing event at Switch Node [0x%04" PRIX16 "]. %s\n",
    (uint16_t)(sys_id & 0x0000FFFF),
    (switch_module.state == SWITCH_STATE_LINKED) ? "Mode: LINK" : "Mode: SCAN"
    );
#if defined(SL_CATALOG_KERNEL_PRESENT)
  app_task_notify();
#endif
}

/******************************************************************************
 * Write to CLI the change of the Switch state
 *****************************************************************************/
static void cli_log_switch_side_light_bulb_toggle(void)
{
#if defined(_SILICON_LABS_32B_SERIES_2)
  uint64_t sys_id = SYSTEM_GetUnique();
#else
  uint64_t sys_id = sl_hal_system_get_unique();
#endif
  app_log_info(
    "Led Toggle event at Switch Node [0x%04" PRIX16 "]. %s",
    (uint16_t)(sys_id & 0x0000FFFF),
    (light_module.is_light_on ? "Light Bulb is ON\n" : "Light Bulb is OFF\n")
    );
#if defined(SL_CATALOG_KERNEL_PRESENT)
  app_task_notify();
#endif
}

/******************************************************************************
 * Write to CLI the change of the Light state
 *****************************************************************************/
static void cli_log_light_side_light_bulb_toggle(void)
{
  app_log_info(
    "Led Toggle event at Light Node [0x%04" PRIX16 "]. %s",
    *((uint16_t*)light_module.addr),
    (light_module.is_light_on ? "Light Bulb is ON\n" : "Light Bulb is OFF\n")
    );
#if defined(SL_CATALOG_KERNEL_PRESENT)
  app_task_notify();
#endif
}

/******************************************************************************
 * Send a wireless pocket
 *****************************************************************************/
static void transmit_packet(sl_rail_handle_t rail_handle)
{
  // Encode the control role in the message
  set_role(&out_packet[DEMO_CONTROL_PAYLOAD_BYTE], DEMO_CONTROL_ROLE_SWITCH);
  copy_light_address_to_payload();
  // Send out a light bulb toggle command
  set_command_type(&out_packet[DEMO_CONTROL_PAYLOAD_BYTE], CMD_TYPE_LIGHT_TOGGLE);
  set_switch_state_in_payload();
  prepare_packet(rail_handle, out_packet, sizeof(out_packet));
  rail_status = sl_rail_start_tx(rail_handle, get_selected_channel(), SL_RAIL_TX_OPTIONS_DEFAULT, NULL);
  if (rail_status != SL_RAIL_STATUS_NO_ERROR) {
    app_log_warning("sl_rail_start_tx() result: 0x%08" PRIX32 "\n ", rail_status);
  }
}

/******************************************************************************
 * Receive the wireless packet, and save it in a buffer
 *****************************************************************************/
static void save_received_packet(sl_rail_handle_t rail_handle)
{
  sl_rail_rx_packet_handle_t rx_packet_handle;
  rx_packet_handle = sl_rail_get_rx_packet_info(rail_handle, SL_RAIL_RX_PACKET_HANDLE_OLDEST_COMPLETE, &packet_info);
  while (rx_packet_handle != SL_RAIL_RX_PACKET_HANDLE_INVALID) {
    sl_rail_get_rx_packet_details(rail_handle, SL_RAIL_RX_PACKET_HANDLE_OLDEST_COMPLETE, &rxPacketDetails);
    if (packet_info.packet_bytes <= SL_RAIL_SDK_RX_FIFO_SIZE) {
      uint16_t packet_size = unpack_packet(rail_handle, rx_buffer, &packet_info, &start_of_packet);
      if (packet_size == 0) {
        app_log_warning("Packet size is: %" PRIu16, packet_size);
      }
    }
    rail_status = sl_rail_release_rx_packet(rail_handle, SL_RAIL_RX_PACKET_HANDLE_OLDEST_COMPLETE);
    if (rail_status != SL_RAIL_STATUS_NO_ERROR) {
      app_log_warning("sl_rail_release_rx_packet() result: 0x%08" PRIX32 "\n", rail_status);
    }
    if (packet_info.packet_bytes <= SL_RAIL_SDK_RX_FIFO_SIZE) {
      light_module.last_response_type = get_light_response_type(start_of_packet);
    }
    rx_packet_handle = sl_rail_get_rx_packet_info(rail_handle, SL_RAIL_RX_PACKET_HANDLE_OLDEST_COMPLETE, &packet_info);
  }
}

/******************************************************************************
 * Set the actual state in the transmit buffer
 *****************************************************************************/
static void set_switch_state_in_payload(void)
{
  // Encode the actual state in the outgoing message
  switch (switch_module.state) {
    case SWITCH_STATE_SCAN:
      out_packet[DEVICE_STATUS_PAYLOAD_BYTE] &= ~DEVICE_STATUS_SWITCH_STATE_BIT;
      break;
    case SWITCH_STATE_LINKED:
      out_packet[DEVICE_STATUS_PAYLOAD_BYTE] |= DEVICE_STATUS_SWITCH_STATE_BIT;
      break;
  }
}

/******************************************************************************
 * Get the communication state of the Light node, if possible (if it is a new Light)
 *****************************************************************************/
static void get_light_state_from_rx_fifo(void)
{
  light_app_state_t light_state =
    (start_of_packet[DEVICE_STATUS_PAYLOAD_BYTE] & DEVICE_STATUS_LIGHT_STATE_BIT)
    ? LIGHT_STATE_READY : LIGHT_STATE_ADVERTISE;

  // If the light changed its state
  if (light_module.state != light_state) {
    light_module.state = light_state;
    app_log_info(
      "State changing event at Light Node [0x%04" PRIX16 "]. %s\n",
      *(uint16_t*)light_module.addr,
      (light_module.state == LIGHT_STATE_ADVERTISE) ? "Mode: ADVERTISE" : "Mode: READY"
      );
  }
}

/******************************************************************************
 * Display the app name, light state, and the ID of the connected Light node
 *****************************************************************************/
static void display_all_information(void)
{
  demoUIClearMainScreen((uint8_t *)app_name, true, false);
  demoUIDisplayLight(light_module.is_light_on);
  demoUIDisplayProtocol(DEMO_UI_PROTOCOL1, false);
  write_ID_to_buffer();
  demoUIDisplayId(DEMO_UI_PROTOCOL1, (uint8_t*)switch_module.switch_text_buffer);
}

/******************************************************************************
 * Update the RSSI and ID values
 *****************************************************************************/
static void update_light_RSSI(void)
{
  // Same Light, update RSSI value
  if (!memcmp((void*)light_module.addr, (void*)&start_of_packet[2], sizeof(light_module.addr))) {
    light_module.rssi_dbm = rxPacketDetails.rssi_dbm;
  } else {
    // Other Light with stronger signal: save ID and RSSI
    if (rxPacketDetails.rssi_dbm > light_module.rssi_dbm) {
      memcpy((void*)light_module.addr, (void*)&start_of_packet[2], sizeof(light_module.addr));
      light_module.rssi_dbm = rxPacketDetails.rssi_dbm;
    }
  }
}

/******************************************************************************
 * Put the communication state and the Light device's ID into a buffer in order to display it
 *****************************************************************************/
static void write_ID_to_buffer(void)
{
  uint8_t blankAddr[8] = { 0 };
  int ID_not_null = memcmp((void*)light_module.addr, blankAddr, sizeof(light_module.addr));
  if (ID_not_null) {
    snprintf(switch_module.switch_text_buffer, sizeof(switch_module.switch_text_buffer), \
             "%s%04" PRIX16, switch_module.switch_text[switch_module.state], *((uint16_t*)light_module.addr));
  } else {
    snprintf(switch_module.switch_text_buffer, sizeof(switch_module.switch_text_buffer), \
             "%s", switch_module.switch_text[switch_module.state]);
  }
}
/******************************************************************************
 * Copy the Light's address to the RX FIFO
 *****************************************************************************/
static void copy_light_address_to_payload(void)
{
  memcpy((void*)&out_packet[PACKET_HEADER_LEN], (void*)light_module.addr, sizeof(light_module.addr));
}

/******************************************************************************
 * Check if an advertise message come from the Light device
 *****************************************************************************/
static demo_control_command_type_t get_light_response_type(const uint8_t* rx_fifo)
{
  return (demo_control_command_type_t)(((rx_fifo[DEMO_CONTROL_PAYLOAD_BYTE]) & DEMO_CONTROL_PAYLOAD_CMD_MASK) >> DEMO_CONTROL_PAYLOAD_CMD_MASK_SHIFT);
}

/******************************************************************************
 * Get light mode from the rx_fifo
 *****************************************************************************/
static bool get_light_bulb_state(const uint8_t* rx_fifo)
{
  return (bool)(rx_fifo[DEMO_CONTROL_PAYLOAD_BYTE] & DEMO_CONTROL_PAYLOAD_CMD_DATA);
}
