/***************************************************************************//**
 * @file
 * @brief Serial Port Profile example
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
#include <string.h>
#include "sl_main_init.h"
#include "sl_bluetooth.h"

#include "app_log.h"
#include "sl_component_catalog.h"
#include "sl_simple_button_instances.h"

#include "ble_peer_manager_common.h"
#include "ble_peer_manager_central.h"
#include "ble_peer_manager_filter.h"
#include "ble_peer_manager_peripheral.h"
#include "app_config.h"
#include "spp.h"
#include "spp_config.h"
#include "app_display.h"

#define IOSTREAM_READ_BUFFER_SIZE       2048
#define FILTER_BY_UUID16                1
#define FILTER_BY_UUID128               2
static uint8_t iostream_read_buffer[IOSTREAM_READ_BUFFER_SIZE];
static size_t spp_on_data_receive(const uint8_t *data, size_t data_size);

/*******************************************************************************
 * Application initialization.
 ******************************************************************************/
void app_init(void)
{
  app_display_init();
  spp_set_data_receive_callback(spp_on_data_receive);

  /////////////////////////////////////////////////////////////////////////////
  // Put your additional application init code here!                         //
  // This is called once during start-up.                                    //
  /////////////////////////////////////////////////////////////////////////////
}

/*******************************************************************************
 * Application Process Action.
 ******************************************************************************/
void app_process_action(void)
{
  size_t bytes_read = 0;
  sl_status_t sc = sl_iostream_read(SL_IOSTREAM_STDIN,
                                    iostream_read_buffer,
                                    sizeof(iostream_read_buffer),
                                    &bytes_read);

  if (sc == SL_STATUS_OK && bytes_read > 0) {
    // Queue data for SPP transmission
    sc = spp_transmit(iostream_read_buffer, bytes_read);
    if (sc != SL_STATUS_OK) {
      app_log_error("SPP transmit failed. Error = 0x%04lx." APP_LOG_NL, sc);
    }
  }

  /////////////////////////////////////////////////////////////////////////////
  // Put your additional application code here!                              //
  // This is called infinitely.                                              //
  // Do not call blocking functions from here!                               //
  /////////////////////////////////////////////////////////////////////////////
}

/*******************************************************************************
 * Callback for when the SPP connection becomes ready
 ******************************************************************************/
void spp_on_connection_ready(void)
{
  app_log_info("Hello from the SPP %s" APP_LOG_NL, spp_get_role() == SPP_CENTRAL ? "central" : "peripheral");
  app_display_connected(true);
}

/*******************************************************************************
 * Callback for data reception
 *
 * @param[in] data Pointer to the received data
 * @param[in] data_size Length of the received data in bytes
 * @return Number of bytes consumed by the application
 ******************************************************************************/
static size_t spp_on_data_receive(const uint8_t *data, size_t data_size)
{
  static uint8_t data_buf[SPP_DATA_BUFFER_SIZE + 1];
  size_t data_length = data_size;

  // Validate data_size to prevent buffer overflow
  if (data_size > SPP_DATA_BUFFER_SIZE) {
    app_log_error("Received data size exceeds buffer size. Truncating." APP_LOG_NL);
    data_length = SPP_DATA_BUFFER_SIZE;
  }

  memcpy(data_buf, data, data_length);
  data_buf[data_length] = '\0';

  app_log("%s", data_buf);

  return data_length;
}

/*******************************************************************************
 * Enable filtering
 ******************************************************************************/
void app_filter(void)
{
  sl_status_t sc;

#if APP_FILTER_BY_BD_ADDR
  {
    ble_peer_manager_set_filter_bt_address(true);
    bd_addr addr = { .addr = APP_TARGET_BD_ADDR_VALUE };
    sc = ble_peer_manager_add_allowed_bt_address(&addr);
    if (sc != SL_STATUS_OK) {
      app_log_info("Failed to add allowed BT address. Error: 0x%04lx." APP_LOG_NL, sc);
    }
    sc = ble_peer_manager_set_filter_address_type(APP_TARGET_ADDR_TYPE);
    if (sc != SL_STATUS_OK) {
      app_log_info("Failed to set address type filter. Error: 0x0%04lx." APP_LOG_NL, sc);
    }
  }
#endif

#if APP_UUID_TYPE == FILTER_BY_UUID16
  {
    sl_bt_uuid_16_t service_uuid = { .data = APP_SERVICE_UUID16 };
    sc = ble_peer_manager_set_filter_service_uuid16(&service_uuid);
    if (sc != SL_STATUS_OK) {
      app_log_info("Failed to set filter to UUID. Error: 0x0%04lx." APP_LOG_NL, sc);
    }
  }
#endif

#if APP_UUID_TYPE == FILTER_BY_UUID128
  {
    uuid_128 service_uuid = { .data = APP_SERVICE_UUID128 };
    sc = ble_peer_manager_set_filter_service_uuid128(&service_uuid);
    if (sc != SL_STATUS_OK) {
      app_log_info("Failed to set filter to UUID. Error: 0x0%04lx." APP_LOG_NL, sc);
    }
  }
#endif

#if APP_FILTER_BY_NAME
  {
    sc = ble_peer_manager_set_filter_device_name(APP_TARGET_NAME_VALUE,
                                                 strlen(APP_TARGET_NAME_VALUE),
                                                 true);
    if (sc != SL_STATUS_OK) {
      app_log_info("Failed to set device name filter. Error: 0x0%04lx." APP_LOG_NL, sc);
    }
  }
#endif

#if APP_FILTER_BY_SERVICE_DATA
  static const uint8_t app_service_data[] = APP_SERVICE_DATA_VALUE;
  sc = ble_peer_manager_set_filter_service_data(
    (uint8_t*)app_service_data,
    APP_SERVICE_DATA_OFFSET,
    APP_SERVICE_DATA_LEN
    );
  if (sc != SL_STATUS_OK) {
    app_log_info("Failed to set service data filter. Error: 0x0%04lx." APP_LOG_NL, sc);
  }
#endif

#if APP_FILTER_BY_MANUFACTURER_DATA
  static const uint8_t app_manufacturer_data[] = APP_MANUFACTURER_DATA_VALUE;
  sc = ble_peer_manager_set_filter_manufacturer_data(
    (uint8_t*)app_manufacturer_data,
    APP_MANUFACTURER_DATA_OFFSET,
    APP_MANUFACTURER_DATA_LEN
    );
  if (sc != SL_STATUS_OK) {
    app_log_info("Failed to set manufacturer data filter. Error: 0x0%04lx." APP_LOG_NL, sc);
  }
#endif

#if APP_FILTER_BY_RSSI
  sc = ble_peer_manager_set_filter_rssi(APP_TARGET_RSSI);
  if (sc != SL_STATUS_OK) {
    app_log_info("Failed to set RSSI filter. Error: 0x0%04lx." APP_LOG_NL, sc);
  }
#endif
}

/*******************************************************************************
 * Enable peripheral role
 ******************************************************************************/
void app_peripheral_enable(void)
{
  sl_status_t sc = ble_peer_manager_peripheral_start_advertising(SL_BT_INVALID_ADVERTISING_SET_HANDLE);
  if (sc != SL_STATUS_OK) {
    app_log_error("Start advertising failed. Error = 0x%04lx." APP_LOG_NL, sc);
  } else {
    app_log_info("Advertising started..." APP_LOG_NL);
  }
}

/*******************************************************************************
 * Enable central role
 ******************************************************************************/
void app_central_enable(void)
{
  app_filter();
  sl_status_t sc = ble_peer_manager_central_create_connection();
  if (sc != SL_STATUS_OK) {
    app_log_info("Failed to create connection. Error: 0x0%04lx." APP_LOG_NL, sc);
  } else {
    app_log_info("Scanning started..." APP_LOG_NL);
  }
}

/*******************************************************************************
 * Bluetooth stack event handler
 * This overrides the weak implementation
 *
 * @param[in] evt Event coming from the Bluetooth stack
 ******************************************************************************/
void sl_bt_on_event(sl_bt_msg_t *evt)
{
  switch (SL_BT_MSG_ID(evt->header)) {
    // -------------------------------
    // This event indicates the device has started and the radio is ready.
    // Do not call any stack command before receiving this boot event!
    case sl_bt_evt_system_boot_id:
      app_log_info("Bluetooth stack booted: v%d.%d.%d-b%d" APP_LOG_NL,
                   evt->data.evt_system_boot.major,
                   evt->data.evt_system_boot.minor,
                   evt->data.evt_system_boot.patch,
                   evt->data.evt_system_boot.build);

      app_log_info("Silicon Labs SPP" APP_LOG_NL);
      spp_set_role((APP_DEFAULT_SPP_ROLE == 0) ? SPP_CENTRAL : SPP_PERIPHERAL);
      if (sl_button_get_state(&sl_button_btn0) == SL_SIMPLE_BUTTON_PRESSED) {
        spp_set_role(spp_get_role() == SPP_CENTRAL ? SPP_PERIPHERAL : SPP_CENTRAL);
      }

      if (spp_get_role() == SPP_PERIPHERAL) {
        app_log_info("Device role: PERIPHERAL" APP_LOG_NL);
        ble_peer_manager_peripheral_init();
        app_peripheral_enable();
      } else {
        app_log_info("Device role: CENTRAL" APP_LOG_NL);
        ble_peer_manager_central_init();
        ble_peer_manager_filter_init();
        app_central_enable();
      }

      app_display_print_role(spp_get_role());
      break;
    case sl_bt_evt_connection_opened_id:
      app_log_info("Connection opened" APP_LOG_NL);
      break;

    case sl_bt_evt_connection_closed_id:
      app_display_connected(false);
      app_log_info("Connection closed" APP_LOG_NL);
      break;

    // -------------------------------
    // Default event handler
    default:
      break;
  }
}

void app_on_ble_peer_manager_event(ble_peer_manager_evt_type_t *event)
{
  switch (event->evt_id) {
    case BLE_PEER_MANAGER_ON_CONN_OPENED_CENTRAL:
      app_log_info("Connection opened as central from Peer Manager" APP_LOG_NL);
      break;

    case BLE_PEER_MANAGER_ON_CONN_OPENED_PERIPHERAL:
      app_log_info("Connection opened as peripheral from Peer Manager" APP_LOG_NL);
      break;

    case BLE_PEER_MANAGER_ON_CONN_CLOSED:
      app_log_info("Connection closed from Peer Manager" APP_LOG_NL);
      if (spp_get_role() == SPP_PERIPHERAL) {
        app_peripheral_enable();
      } else {
        app_central_enable();
      }
      break;

    case BLE_PEER_MANAGER_ON_ADV_STOPPED:
      app_log_info("Advertisement stopped from Peer Manager" APP_LOG_NL);
      break;

    case BLE_PEER_MANAGER_ERROR:
      app_log_info("Error from Peer Manager" APP_LOG_NL);
      break;

    default:
      app_log_info("Unhandled Peer Manager event" APP_LOG_NL);
      break;
  }
}
