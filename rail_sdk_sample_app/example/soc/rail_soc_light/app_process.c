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
#include "printf.h"
#include "sl_component_catalog.h"
#include "sl_rail.h"
#include "app_process.h"
#include "sl_simple_button_instances.h"
#include "sl_rail_sdk_simple_assistance.h"
#include "sl_rail_util_init.h"
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
#define DEVICE_TYPE "Light"
/// Send broadcast message in every second
#define DEMO_LIGHT_STATUS_BROADCAST_INTERVAL    (1000000Ul)

/// this structure contains the Light module's details
typedef struct {
  uint8_t addr[8];
  light_app_state_t state;
  char* modeText[2];
  char modeTextBuf[10];
  bool is_light_on;
} light_t;
// -----------------------------------------------------------------------------
//                          Static Function Declarations
// -----------------------------------------------------------------------------
/**************************************************************************//**
 * Set the User LEDs according to the light state
 *****************************************************************************/
static inline void set_LEDs(void);

/**************************************************************************//**
 * Used for display the module's unique ID
 *****************************************************************************/
static inline void put_unique_ID_to_buffer(void);

/**************************************************************************//**
 * Put the actual light state in the payload, in order to send it wireless
 *
 * @param[out] payload of the transmitting message
 * @param[in] state of the light
 *****************************************************************************/
static inline void set_light_state(uint8_t * payload, bool state);

/**************************************************************************//**
 * Display the protocol, light state, and unique ID
 *****************************************************************************/
static inline void display_all_information(void);

/**************************************************************************//**
 * Callback function for the sl_rail_set_timer API, restart the RAIL timer
 *****************************************************************************/
static inline void broadcast_timer_expired();

/**************************************************************************//**
 * Write to CLI the change of the Light state
 *****************************************************************************/
static void cli_log_state_machine_change(void);

/**************************************************************************//**
 * Write to CLI the change of the Light state
 *****************************************************************************/
static void cli_log_light_side_light_bulb_toggle(void);

/**************************************************************************//**
 * Receive the wireless packet, and save it in a buffer
 *
 * @param[in] rail_handle
 *****************************************************************************/
static void save_received_packet(sl_rail_handle_t rail_handle);

/**************************************************************************//**
 * Set the actual state in the transmit buffer
 *****************************************************************************/
static void set_light_state_in_payload(void);

/**************************************************************************//**
 * Send a wireless pocket
 *
 * @param[in] rail_handle
 *****************************************************************************/
static void transmit_packet(sl_rail_handle_t rail_handle);
/**************************************************************************//**
 * Copy the Light's address to the RX FIFO
 *****************************************************************************/
static void copy_light_addr_to_payload(void);
/**************************************************************************//**
 * Write to CLI the change of the Switch state
 *****************************************************************************/
static void cli_log_switch_side_light_bulb_toggle(void);
// -----------------------------------------------------------------------------
//                                Global Variables
// -----------------------------------------------------------------------------
//app_name used in LCD functions
uint8_t app_name[6] = "Light";

bool light_bulb_toggle_required = false;
bool state_change_required = false;

// -----------------------------------------------------------------------------
//                                Static Variables
// -----------------------------------------------------------------------------
/// Go into transfer mode
static volatile bool light_state_broadcast = false;

/// Contains the last RAIL Rx/Tx error events
static volatile uint64_t current_rail_err = 0;

/// Transmit packet
static uint8_t out_packet[TX_PAYLOAD_LENGTH] = {
  0x0F, 0x16, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66,
  0x77, 0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xFF, 0x00,
};

static light_t light = {
  .addr = { 0 },
  .state = LIGHT_STATE_ADVERTISE,
  .modeText = { "ADVERT", "READY" },
  .modeTextBuf = { 0 },
  .is_light_on = false
};

//Send broadcast message periodically
static bool schedule_broadcast = true;
// Increase value if packet has received, decrease after process it
static volatile bool packet_received = false;
// Hold information about the incoming message
static sl_rail_rx_packet_info_t packet_info;
// Status indicator of the RAIL API calls
static sl_rail_status_t rail_status;
// Start of received payload
static uint8_t *start_of_packet = 0;

static uint8_t rx_buffer[SL_RAIL_SDK_RX_FIFO_SIZE];

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
    switch (light.state) {
      case LIGHT_STATE_READY:
        light.state = LIGHT_STATE_ADVERTISE;
        break;
      case LIGHT_STATE_ADVERTISE:
        light.state = LIGHT_STATE_READY;
        break;
    }
    display_all_information();
    cli_log_state_machine_change();
  }

  switch (light.state) {
    case LIGHT_STATE_ADVERTISE:
      if (packet_received) {
        packet_received = false;
        save_received_packet(rail_handle);
      }
      break;

    case LIGHT_STATE_READY:
      if (packet_received) {
        packet_received = false;
        save_received_packet(rail_handle);
        light.is_light_on = !light.is_light_on;
        display_all_information();
        set_LEDs();
        schedule_broadcast = true;
        cli_log_switch_side_light_bulb_toggle();
      }
      if (light_bulb_toggle_required) {
        light_bulb_toggle_required = false;
        light.is_light_on = !light.is_light_on;
        display_all_information();
        set_LEDs();
        schedule_broadcast = true;
        cli_log_light_side_light_bulb_toggle();
      }
      break;
  }

  // Send broadcast message
  if (schedule_broadcast) {
    schedule_broadcast = false;
    sl_rail_set_timer(rail_handle,
                      DEMO_LIGHT_STATUS_BROADCAST_INTERVAL,
                      SL_RAIL_TIME_DELAY,
                      &broadcast_timer_expired);
    // Send broadcast message
    transmit_packet(rail_handle);
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
 * Copy the Light's address to the TX FIFO
 *****************************************************************************/
void copy_light_addr_to_payload(void)
{
  memcpy((void*)&out_packet[PACKET_HEADER_LEN], (void*)light.addr, sizeof(light.addr));
}

/******************************************************************************
 * Send a wireless pocket
 *****************************************************************************/
void transmit_packet(sl_rail_handle_t rail_handle)
{
  copy_light_addr_to_payload();
  // Set current light state.
  set_role(&out_packet[DEMO_CONTROL_PAYLOAD_BYTE], DEMO_CONTROL_ROLE_LIGHT);
  // Advertisement packet
  if (LIGHT_STATE_ADVERTISE == light.state) {
    set_command_type(&out_packet[DEMO_CONTROL_PAYLOAD_BYTE], CMD_TYPE_LIGHT_ADVERTISE);
  } else {   // Status packet
    set_command_type(&out_packet[DEMO_CONTROL_PAYLOAD_BYTE], CMD_TYPE_LIGHT_BULB_STATE_REPORT);
    set_light_state(&out_packet[DEMO_CONTROL_PAYLOAD_BYTE], light.is_light_on);
  }
  set_light_state_in_payload();
  prepare_packet(rail_handle, out_packet, sizeof(out_packet));
  rail_status = sl_rail_start_tx(rail_handle, get_selected_channel(), SL_RAIL_TX_OPTIONS_DEFAULT, NULL);
  if (rail_status != SL_RAIL_STATUS_NO_ERROR) {
    app_log_warning("sl_rail_start_tx() result: 0x%08" PRIX32 " ", rail_status);
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
  app_log_info("State changing event at Light Node [0x%04" PRIX16 "]. %s",
               (uint16_t)(sys_id & 0x0000FFFF),
               (light.state == LIGHT_STATE_ADVERTISE) ? "Mode: ADVERTISE\n" : "Mode: READY\n");
#if defined(SL_CATALOG_KERNEL_PRESENT)
  app_task_notify();
#endif
}

/******************************************************************************
 * Write to CLI the change of the Switch state
 *****************************************************************************/
static void cli_log_light_side_light_bulb_toggle(void)
{
#if defined(_SILICON_LABS_32B_SERIES_2)
  uint64_t sys_id = SYSTEM_GetUnique();
#else
  uint64_t sys_id = sl_hal_system_get_unique();
#endif
  app_log_info("Led Toggle event at Light Node [0x%04" PRIX16 "]. %s",
               (uint16_t)(sys_id & 0x0000FFFF),
               light.is_light_on ? "Light Bulb is ON\n" : "Light Bulb is OFF\n");
#if defined(SL_CATALOG_KERNEL_PRESENT)
  app_task_notify();
#endif
}

/******************************************************************************
 * Write to CLI the change of the Switch state
 *****************************************************************************/
static void cli_log_switch_side_light_bulb_toggle(void)
{
  app_log_info("Led Toggle event at Switch Node. %s",
               light.is_light_on ? "Light Bulb is ON\n" : "Light Bulb is OFF\n");
#if defined(SL_CATALOG_KERNEL_PRESENT)
  app_task_notify();
#endif
}

/******************************************************************************
 * Receive the wireless packet, and save it in a buffer
 *****************************************************************************/
static void save_received_packet(sl_rail_handle_t rail_handle)
{
  sl_rail_rx_packet_handle_t rx_packet_handle;
  rx_packet_handle = sl_rail_get_rx_packet_info(rail_handle, SL_RAIL_RX_PACKET_HANDLE_OLDEST_COMPLETE, &packet_info);
  while (rx_packet_handle != SL_RAIL_RX_PACKET_HANDLE_INVALID) {
    if (packet_info.packet_bytes <= SL_RAIL_SDK_RX_FIFO_SIZE) {
      uint16_t packet_size = unpack_packet(rail_handle, rx_buffer, &packet_info, &start_of_packet);
      if (packet_size == 0) {
        app_log_warning("Received packet size is :%" PRIu16, packet_size);
      }
    }
    rail_status = sl_rail_release_rx_packet(rail_handle, SL_RAIL_RX_PACKET_HANDLE_OLDEST_COMPLETE);
    if (rail_status != SL_RAIL_STATUS_NO_ERROR) {
      app_log_warning("sl_rail_release_rx_packet() result: 0x%" PRIX32, rail_status);
    }
    rx_packet_handle = sl_rail_get_rx_packet_info(rail_handle, SL_RAIL_RX_PACKET_HANDLE_OLDEST_COMPLETE, &packet_info);
  }
}

/******************************************************************************
 * Set the actual state in the transmit buffer
 *****************************************************************************/
static void set_light_state_in_payload(void)
{
  // Encode the actual state in the outgoing message
  switch (light.state) {
    case LIGHT_STATE_ADVERTISE:
      out_packet[DEVICE_STATUS_PAYLOAD_BYTE] &= ~DEVICE_STATUS_LIGHT_STATE_BIT;
      break;
    case LIGHT_STATE_READY:
      out_packet[DEVICE_STATUS_PAYLOAD_BYTE] |= DEVICE_STATUS_LIGHT_STATE_BIT;
      break;
  }
}

/******************************************************************************
 * Initialize the display at the beginning of the application
 *****************************************************************************/
void init_display(void)
{
  demoUIInit();
  set_EUI(light.addr);
  display_all_information();
}
// -----------------------------------------------------------------------------
//                          Static Function Definitions
// -----------------------------------------------------------------------------

/******************************************************************************
 * Display the app name, light state, and the ID of the connected Light node
 *****************************************************************************/
static void display_all_information(void)
{
  demoUIClearMainScreen((uint8_t *)app_name, true, false);
  demoUIDisplayLight(light.is_light_on);
  demoUIDisplayProtocol(DEMO_UI_PROTOCOL1, false);
  demoUIDisplayId(DEMO_UI_PROTOCOL1, (uint8_t*)light.modeText[light.state]);
  put_unique_ID_to_buffer();
  demoUIDisplayId(DEMO_UI_PROTOCOL2, (uint8_t*)light.modeTextBuf);
}

/******************************************************************************
 * Callback function for the sl_rail_set_timer API
 *****************************************************************************/
static inline void broadcast_timer_expired()
{
  light_state_broadcast = true;
  schedule_broadcast = true;
#if defined(SL_CATALOG_KERNEL_PRESENT)
  app_task_notify();
#endif
}

/******************************************************************************
 * Set the User LEDs according to the light state
 *****************************************************************************/
static inline void set_LEDs(void)
{
  (light.is_light_on == false) \
  ? clear_receive_led() : set_receive_led();
  (light.is_light_on == false) \
  ? clear_send_led() : set_send_led();
}

/******************************************************************************
 * Used for display the module's unique ID
 *****************************************************************************/
static inline void put_unique_ID_to_buffer(void)
{
  snprintf(light.modeTextBuf,
           sizeof(light.modeTextBuf),
           "ID:%" PRIX16, *((uint16_t*)light.addr));
}

/******************************************************************************
 * Put the actual light state in the payload, in order to send it wireless
 *****************************************************************************/
static inline void set_light_state(uint8_t * payload, bool state)
{
  *payload &= ~DEMO_CONTROL_PAYLOAD_CMD_DATA;
  *payload |= state;
}
