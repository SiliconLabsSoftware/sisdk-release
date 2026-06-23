/***************************************************************************//**
 * @file
 * @brief Serial Port Profile component
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
#include <string.h>
#include "spp.h"
#include "spp_config.h"
#include "sl_common.h"
#include "sl_component_catalog.h"
#include "circular_queue.h"
#include "sl_memory_manager.h"
#include "gatt_db.h"
#include "app_timer.h"
#include "app_rta.h"

#ifdef SL_CATALOG_APP_LOG_PRESENT
#include "app_log.h"
#endif // SL_CATALOG_APP_LOG_PRESENT

// -----------------------------------------------------------------------------
// Macros
#define ATT_HEADER_SIZE 3

#define SPP_TIMEOUT 20
#define SPP_CONTROL_OPCODE_BYTES_AVAILABLE 0
#define SPP_CONTROL_OPCODE_BYTES_FREED     1
#define SPP_CONTROL_MESSAGE_LENGTH 3

// Component logging
#if defined(SL_CATALOG_APP_LOG_PRESENT) && SPP_LOG
#define NL                        APP_LOG_NL
#define spp_log_debug(...)        app_log_debug(SPP_LOG_PREFIX __VA_ARGS__)
#define spp_log_info(...)         app_log_info(SPP_LOG_PREFIX __VA_ARGS__)
#define spp_log_warning(...)      app_log_warning(SPP_LOG_PREFIX __VA_ARGS__)
#define spp_log_error(...)        app_log_error(SPP_LOG_PREFIX __VA_ARGS__)
#define spp_log_critical(...)     app_log_critical(SPP_LOG_PREFIX __VA_ARGS__)
#else
#define NL
#define spp_log_debug(...)
#define spp_log_info(...)
#define spp_log_warning(...)
#define spp_log_error(...)
#define spp_log_critical(...)
#endif // defined(SL_CATALOG_APP_LOG_PRESENT) && SPP_LOG

// SPP Service
#define SPP_SERVICE_UUID                     { 0xa4, 0xa1, 0x9e, 0xcc, 0xe7, 0x51, 0xa8, 0x85, \
                                               0x9f, 0x47, 0x7f, 0x32, 0x46, 0xfe, 0x92, 0x8b }

#define SL_BT_INVALID_CHARACTERISTIC_HANDLE  0xFFFF
#define SL_BT_INVALID_SERVICE_HANDLE         0xFFFFFFFF

// -----------------------------------------------------------------------------
// Static function declarations
static void on_bt_evt_connection_opened(sl_bt_evt_connection_opened_t *evt);
static void on_bt_evt_service(sl_bt_evt_gatt_service_t *evt);
static void on_bt_evt_gatt_procedure_completed(void);
static void on_bt_evt_gatt_server_attribute_value(sl_bt_evt_gatt_server_attribute_value_t *evt);
static void on_bt_evt_gatt_characteristic_value(sl_bt_evt_gatt_characteristic_value_t *evt);
static void control_message_received(const uint8_t* data, const size_t data_size);
static void send_initial_buffer_size(void);
static void spp_write_timer_cb(app_timer_t *handle, void *data);
static sl_status_t spp_write(void);
static void spp_send_freed_bytes(const size_t data_size);
static void on_bt_evt_connection_closed(sl_bt_evt_connection_closed_t *evt);
static sl_status_t spp_rta_acquire(void);
static void spp_rta_proceed(void);
static sl_status_t spp_rta_release(void);

// -----------------------------------------------------------------------------
// Static variables

// Current SPP role
static spp_role_t spp_role;
// State of the SPP connection
static spp_state_t spp_state = SPP_UNKNOWN;

// Service UUID
static const uint8_t spp_service_uuid[] = SPP_SERVICE_UUID;
// BLE connection handle
static uint8_t spp_connection_handle = SL_BT_INVALID_CONNECTION_HANDLE;
// Service handle on the remote device
static uint32_t spp_service_handle = SL_BT_INVALID_SERVICE_HANDLE;

// Characteristic handles
// Note: These are initialized with local GATT database values and are used for both
// central and peripheral roles
static uint16_t spp_rx_characteristic_handle = gattdb_spp_rx;
static uint16_t spp_tx_characteristic_handle = gattdb_spp_tx;

// MTU size
static uint16_t mtu_size = 0;
// Data buffers
static Queue_t data_queue;
// Timer
static app_timer_t spp_write_timer;
static bool spp_write_timer_running = false;
static bool spp_timeout_pending = false;
// Remote data buffer
static uint16_t spp_remote_buffer_max_size = SPP_DATA_BUFFER_SIZE;
static uint16_t spp_remote_buffer_size = SPP_DATA_BUFFER_SIZE;

// RTA context
static app_rta_context_t ctx;

// Registered data receive callback
static spp_on_data_receive_t spp_data_receive_cb = NULL;

// -----------------------------------------------------------------------------
// Private function definitions

/*******************************************************************************
 * Connection opened
 *
 * Note: After connection is opened, service discovery is started.
 ******************************************************************************/
static void on_bt_evt_connection_opened(sl_bt_evt_connection_opened_t *evt)
{
  spp_connection_handle = evt->connection;
  sl_status_t sc = sl_bt_gatt_discover_primary_services(evt->connection);
  if (sc != SL_STATUS_OK) {
    spp_log_error("Failed to discover services. Error = 0x%04lx." NL, sc);
  }
  sc = sl_bt_gatt_get_mtu(evt->connection, &mtu_size);
  if (sc != SL_STATUS_OK) {
    spp_log_error("Failed to get MTU size. Error = 0x%04lx." NL, sc);
  }
}

/*******************************************************************************
 * Service discovered
 *
 * Note: Characteristic discovery is not performed here because both central and
 * peripheral devices use the same GATT database structure. The local GATT database
 * handles (gattdb_spp_rx and gattdb_spp_tx) are identical on both devices, so they
 * can be used directly without discovering characteristics on the remote device.
 ******************************************************************************/
static void on_bt_evt_service(sl_bt_evt_gatt_service_t *evt)
{
  if (memcmp(evt->uuid.data, spp_service_uuid, sizeof(spp_service_uuid)) == 0) {
    spp_log_info("SPP GATT service ID discovered" NL);
    spp_service_handle = evt->service;
    spp_state = SPP_ENABLE_TX_NOTIFICATION;
  }
}

/*******************************************************************************
 * Procedure completed (eg. service or characteristic discovery)
 *
 * Note: The characteristic handles used here (spp_tx_characteristic_handle and
 * spp_rx_characteristic_handle) are local GATT database values. This works for
 * both central and peripheral roles because both devices use the same GATT database
 * structure, making the handles identical on both devices.
 ******************************************************************************/
static void on_bt_evt_gatt_procedure_completed(void)
{
  sl_status_t sc;
  switch (spp_state) {
    case SPP_ENABLE_TX_NOTIFICATION:
      sc = sl_bt_gatt_set_characteristic_notification(spp_connection_handle,
                                                      spp_tx_characteristic_handle,
                                                      sl_bt_gatt_notification);

      if (sc == SL_STATUS_OK) {
        spp_log_info("TX characteristic: Subscribed for notification." NL);
      } else {
        spp_log_error("TX characteristic: Couldn't subscribe for notification." NL);
      }
      spp_state = SPP_ENABLE_RX_NOTIFICATION;
      break;
    case SPP_ENABLE_RX_NOTIFICATION:
      if (SPP_FLOW_CONTROL) {
        sc = sl_bt_gatt_set_characteristic_notification(spp_connection_handle,
                                                        spp_rx_characteristic_handle,
                                                        sl_bt_gatt_notification);

        if (sc == SL_STATUS_OK) {
          spp_log_info("RX characteristic: Subscribed for notification." NL);
        } else {
          spp_log_error("RX characteristic: Couldn't subscribe for notification. Error = 0x%04lx" NL, sc);
        }
      }
      spp_state = SPP_SEND_INITIAL_BUFFER;
      break;
    case SPP_SEND_INITIAL_BUFFER:
      if (SPP_FLOW_CONTROL) {
        send_initial_buffer_size();
      }
      spp_on_connection_ready();
      spp_state = SPP_CONNECTED;
      break;
    default:
      spp_log_error("Unknown SPP state" NL);
      break;
  }
}

/*******************************************************************************
 * One of our characteristics has been written
 ******************************************************************************/
static void on_bt_evt_gatt_server_attribute_value(sl_bt_evt_gatt_server_attribute_value_t *evt)
{
  uint16_t attribute_handle = evt->attribute;
  if (attribute_handle == spp_rx_characteristic_handle) {
    spp_log_debug("SPP data received; size='%u' attribute_handle='%u'" NL, evt->value.len, attribute_handle);
    if (spp_data_receive_cb != NULL) {
      size_t consumed = spp_data_receive_cb(evt->value.data, evt->value.len);
      if (consumed > 0) {
        spp_send_freed_bytes(consumed);
      }
    }
  }

  if (attribute_handle == spp_tx_characteristic_handle) {
    control_message_received(evt->value.data, evt->value.len);
  }
}

/*******************************************************************************
 * Notification received
 ******************************************************************************/
static void on_bt_evt_gatt_characteristic_value(sl_bt_evt_gatt_characteristic_value_t *evt)
{
  // SPP TX characteristic notification -> data received
  if (spp_tx_characteristic_handle == evt->characteristic) {
    if (spp_data_receive_cb != NULL) {
      size_t consumed = spp_data_receive_cb(evt->value.data, evt->value.len);
      if (consumed > 0) {
        spp_send_freed_bytes(consumed);
      }
    }
  }

  // SPP RX characteristic notification -> control message received
  if (spp_rx_characteristic_handle == evt->characteristic) {
    control_message_received(evt->value.data, evt->value.len);
  }
}

/*******************************************************************************
 * Handle a received control message.
 ******************************************************************************/
static void control_message_received(const uint8_t* data, const size_t data_size)
{
  if (data_size != SPP_CONTROL_MESSAGE_LENGTH) {
    return;
  }

  uint8_t control_data[SPP_CONTROL_MESSAGE_LENGTH] = { 0 };
  memcpy(control_data, data, data_size);

  switch (control_data[0]) {
    // Byte 0 = opcode
    case SPP_CONTROL_OPCODE_BYTES_AVAILABLE:
      // Received initial buffer size from remote device
      // Parse buffer size: Byte 1 = LSB, Byte 2 = MSB
      spp_remote_buffer_max_size = control_data[1] | (control_data[2] << 8);
      spp_remote_buffer_size = spp_remote_buffer_max_size; // Initialize available space
      spp_log_info("Initial buffer size: %d" NL, spp_remote_buffer_max_size);
      break;

    // Byte 0 = opcode
    case SPP_CONTROL_OPCODE_BYTES_FREED:
      // Remote device has freed up buffer space.
      // Parse freed bytes: Byte 1 = LSB, Byte 2 = MSB
      uint16_t freed_bytes = (control_data[1] | (control_data[2] << 8));
      spp_log_debug("Remote freed %u bytes" NL, freed_bytes);
      // Prevent overflow: don't exceed max buffer size
      if (spp_remote_buffer_size + freed_bytes > spp_remote_buffer_max_size) {
        spp_remote_buffer_size = spp_remote_buffer_max_size;
      } else {
        spp_remote_buffer_size += freed_bytes;
      }
      break;
  }
}

/*******************************************************************************
 * Send the initial buffer size information.
 ******************************************************************************/
static void send_initial_buffer_size(void)
{
  sl_status_t sc;
  // Byte 0: Opcode;
  // Byte 1 and 2 is the maximum buffer size. Byte 1: LSB, Byte 2: MSB.
  uint8_t initial_buffer_size[SPP_CONTROL_MESSAGE_LENGTH] = {
    SPP_CONTROL_OPCODE_BYTES_AVAILABLE,
    (data_queue.size & 0xFF),
    (data_queue.size >> 8) & 0xFF
  };
  if (spp_role == SPP_PERIPHERAL) {
    sc = sl_bt_gatt_server_send_notification(spp_connection_handle,
                                             spp_rx_characteristic_handle,
                                             sizeof(initial_buffer_size),
                                             initial_buffer_size);

    if (sc != SL_STATUS_OK) {
      spp_log_error("Initial buffer notification failed. Error = 0x%04lx" NL, sc);
    }
  } else {
    sc = sl_bt_gatt_write_characteristic_value_without_response(spp_connection_handle,
                                                                spp_tx_characteristic_handle,
                                                                sizeof(initial_buffer_size),
                                                                initial_buffer_size,
                                                                NULL);

    if (sc != SL_STATUS_OK) {
      spp_log_error("Initial buffer write failed. Error = 0x%04lx" NL, sc);
    }
  }
}

/*******************************************************************************
 * Callback for the spp_write_timer
 ******************************************************************************/
static void spp_write_timer_cb(app_timer_t *handle, void *data)
{
  (void)handle;
  (void)data;

  spp_write_timer_running = false;
  spp_timeout_pending = true;

  spp_rta_proceed();
}

/*******************************************************************************
 * Send data through an SPP connection
 ******************************************************************************/
static sl_status_t spp_write(void)
{
  if (mtu_size <= ATT_HEADER_SIZE) {
    spp_log_error("MTU size is invalid or not initialized." NL);
    return SL_STATUS_INVALID_PARAMETER;
  }
  uint16_t mtu_len = mtu_size - ATT_HEADER_SIZE;
  static uint8_t data_buffer[SPP_DATA_BUFFER_SIZE];
  sl_status_t sc;

  sc = spp_rta_acquire();
  if (sc != SL_STATUS_OK) {
    return sc;
  }
  uint16_t data_size = data_queue.count;

  // Flow control: Check if remote buffer has available space
  if (spp_remote_buffer_size == 0) {
    // Remote buffer is full, cannot send data
    sc = SL_STATUS_OK;
    goto exit;
  }

  // data_size should not exceed maximum buffer size
  if (data_size > spp_remote_buffer_max_size) {
    spp_log_error("SPP data dropped, data length is larger than the maximum remote buffer size" NL);
    sc = SL_STATUS_INVALID_PARAMETER;
    goto exit;
  }

  // mtu_len value should be between 0 and available remote buffer size
  if (data_size > 0) {
    // Limit send size to available buffer space
    uint16_t max_send_size = (spp_remote_buffer_size < mtu_len) ? spp_remote_buffer_size : mtu_len;
    mtu_len = (data_size < max_send_size) ? data_size : max_send_size;

    // Only remove up to mtu_len bytes from the queue
    for (uint16_t i = 0; i < mtu_len && !queueIsEmpty(&data_queue); i++) {
      data_buffer[i] = (uint8_t)(uint32_t)queueRemove(&data_queue);
    }

    if (spp_role == SPP_PERIPHERAL) {
      // Peripheral sends data using notifications
      sc = sl_bt_gatt_server_send_notification(spp_connection_handle,
                                               spp_tx_characteristic_handle,
                                               mtu_len,
                                               data_buffer);
    } else {
      // Central sends data using write without response
      sc = sl_bt_gatt_write_characteristic_value_without_response(spp_connection_handle,
                                                                  spp_rx_characteristic_handle,
                                                                  mtu_len,
                                                                  data_buffer,
                                                                  NULL);
    }
    if (sc == SL_STATUS_OK) {
      if (mtu_len <= spp_remote_buffer_size) {
        spp_remote_buffer_size -= mtu_len;
      } else {
        spp_remote_buffer_size = 0;
      }
    } else {
      spp_log_error("Failed to write characteristic value. Error = 0x%04lx." NL, sc);
    }
  }

  exit:
  (void)spp_rta_release();
  spp_rta_proceed();
  return sc;
}

/*******************************************************************************
 * Sends a flow control message indicating the number of bytes freed.
 ******************************************************************************/
static void spp_send_freed_bytes(const size_t data_size)
{
  sl_status_t sc;

  // Clamp to 16-bit, since the flow control message uses 2 bytes
  uint16_t bytes_to_send = (data_size > UINT16_MAX) ? UINT16_MAX : (uint16_t)data_size;

  uint8_t freed_bytes[SPP_CONTROL_MESSAGE_LENGTH] = { SPP_CONTROL_OPCODE_BYTES_FREED, 0, 0 };
  sc = spp_rta_acquire();
  if (sc != SL_STATUS_OK) {
    return;
  }
  freed_bytes[1] = (uint8_t)((bytes_to_send) & 0xFF);
  freed_bytes[2] = (uint8_t)((bytes_to_send >> 8) & 0xFF);

  if (SPP_FLOW_CONTROL) {
    if (spp_role == SPP_PERIPHERAL) {
      // Peripheral specific flow control
      sc = sl_bt_gatt_server_send_notification(spp_connection_handle,
                                               spp_rx_characteristic_handle,
                                               sizeof(freed_bytes),
                                               freed_bytes);
    } else {
      // Central specific flow control
      sc = sl_bt_gatt_write_characteristic_value_without_response(spp_connection_handle,
                                                                  spp_tx_characteristic_handle,
                                                                  sizeof(freed_bytes),
                                                                  freed_bytes,
                                                                  NULL);
    }
    if (sc != SL_STATUS_OK) {
      spp_log_error("Freed bytes write failed. Error = 0x%04lx" NL, sc);
    }
  }
  sc = spp_rta_release();
  if (sc != SL_STATUS_OK) {
    return;
  }
}

/*******************************************************************************
 * Connection closed
 *
 * Note: Reset connection related variables, queue and stop timer.
 ******************************************************************************/
static void on_bt_evt_connection_closed(sl_bt_evt_connection_closed_t *evt)
{
  if (spp_connection_handle == evt->connection) {
    spp_state = SPP_DISCONNECTED;

    // Reset connection related variables
    spp_connection_handle = SL_BT_INVALID_CONNECTION_HANDLE;
    spp_service_handle = SL_BT_INVALID_SERVICE_HANDLE;
    spp_remote_buffer_max_size = SPP_DATA_BUFFER_SIZE;
    spp_remote_buffer_size = SPP_DATA_BUFFER_SIZE;

    // Reset queue
    if (!queueInit(&data_queue, SPP_DATA_BUFFER_SIZE)) {
      spp_log_error("Failed to reinitialize data queue on disconnect" NL);
    }
    // Stop timer
    (void)app_timer_stop(&spp_write_timer);
    spp_write_timer_running = false;
    spp_timeout_pending = false;
  }
}
// -----------------------------------------------------------------------------
// Public function definitions

/*******************************************************************************
 * Set SPP role
 ******************************************************************************/
void spp_set_role(spp_role_t role)
{
  spp_role = role;
}

/*******************************************************************************
 * Get SPP role
 ******************************************************************************/
spp_role_t spp_get_role(void)
{
  return spp_role;
}

/*******************************************************************************
 * Queue outgoing data for transmission
 ******************************************************************************/
sl_status_t spp_transmit(const uint8_t *data, const size_t data_size)
{
  size_t length = data_size;
  sl_status_t sc;
  sc = spp_rta_acquire();
  if (sc != SL_STATUS_OK) {
    return sc;
  }

  if (data == NULL || data_size == 0) {
    sc = SL_STATUS_INVALID_PARAMETER;
    goto exit;
  }

  // Validate that data_size doesn't exceed data_queue.size maximum value
  // This also prevents truncation since data_queue.size is uint16_t
  if (data_size > (size_t)data_queue.size) {
    sc = SL_STATUS_INVALID_PARAMETER;
    goto exit;
  }

  size_t free_space = (size_t)data_queue.size - (size_t)data_queue.count;
  if (free_space >= length) {
    while (length--) {
      queueAdd(&data_queue, (void *)(uint32_t)(*data++));
    }
    sc = SL_STATUS_OK;
  } else {
    sc = SL_STATUS_NO_MORE_RESOURCE;
  }

  exit:
  (void)spp_rta_release();
  spp_rta_proceed();
  return sc;
}

// -----------------------------------------------------------------------------
// Weak function

/******************************************************************************
 * Callback for when the SPP connection becomes ready
 *****************************************************************************/
SL_WEAK void spp_on_connection_ready(void)
{
  // Intentionally left empty
  // Override this function in the application to handle connection-ready events
}

// -----------------------------------------------------------------------------
// Callback function

/******************************************************************************
 * Register a data reception callback
 *****************************************************************************/
void spp_set_data_receive_callback(spp_on_data_receive_t spp_on_data_receive)
{
  spp_data_receive_cb = spp_on_data_receive;
}

// -----------------------------------------------------------------------------
// Internal function definitions

/*******************************************************************************
 * Initialize SPP component
 ******************************************************************************/
void spp_init(void)
{
  if (!queueInit(&data_queue, SPP_DATA_BUFFER_SIZE)) {
    spp_log_error("Failed to initialize data queue" NL);
    return;
  }
}

/*******************************************************************************
 * Process step for SPP
 ******************************************************************************/
void spp_step(void)
{
  // If enough data is available, send immediately
  if (data_queue.count >= SPP_MIN_CHUNK_SIZE) {
    if (spp_write_timer_running) {
      (void)app_timer_stop(&spp_write_timer);
      spp_write_timer_running = false;
    }
    spp_write();
    spp_timeout_pending = false;
    return;
  }

  // On timer timeout, send whatever is left
  if (spp_timeout_pending) {
    spp_timeout_pending = false;
    spp_write();
    return;
  }

  // If the data size is less than the minimum chunk size and timer is not running
  if (data_queue.count > 0 && !spp_write_timer_running) {
    sl_status_t sc = app_timer_start(&spp_write_timer,
                                     SPP_TIMEOUT,
                                     spp_write_timer_cb,
                                     NULL,
                                     0);
    if (sc == SL_STATUS_OK) {
      // Timer started successfully
      spp_write_timer_running = true;
    } else {
      spp_log_info("Failed to start write timer. Error: 0x%04lx." NL, sc);
    }
  }
}
/******************************************************************************
 * Handle run time errors in RTA context
 *****************************************************************************/
static void on_runtime_error(app_rta_error_t error, sl_status_t result)
{
  switch (error) {
    case APP_RTA_ERROR_RUNTIME_INIT_FAILED:
      spp_log_error("RTA runtime init failed: 0x%04lx" NL, result);
      break;

    case APP_RTA_ERROR_ACQUIRE_FAILED:
      spp_log_error("RTA acquire failed: 0x%04lx" NL, result);
      break;

    case APP_RTA_ERROR_RELEASE_FAILED:
      spp_log_error("RTA release failed: 0x%04lx" NL, result);
      break;

    default:
      spp_log_error("RTA generic error: 0x%04lx" NL, result);
      break;
  }
}

/*******************************************************************************
 * Initialize the RTA context of the SPP component
 ******************************************************************************/
void spp_rta_init(void)
{
  app_rta_config_t config = {
    .requirement.runtime = true,
    .requirement.guard   = true,
    .requirement.signal  = true,
    .step                = spp_step,
    .priority            = APP_RTA_PRIORITY_NORMAL,
    .stack_size          = 1024,
    .error               = on_runtime_error,
    .wait_for_guard      = 10
  };
  sl_status_t sc = app_rta_create_context(&config, &ctx);
  if (sc != SL_STATUS_OK) {
    on_runtime_error(APP_RTA_ERROR_RUNTIME_INIT_FAILED, sc);
  }
}

/*******************************************************************************
 * Finalize initialization - called when the RTA is ready
 ******************************************************************************/
void spp_rta_ready(void)
{
  (void)app_rta_proceed(ctx);
}

/*******************************************************************************
 * Acquire access to variables protected by the context
 ******************************************************************************/
static sl_status_t spp_rta_acquire(void)
{
  sl_status_t sc = app_rta_acquire(ctx);
  if (sc != SL_STATUS_OK) {
    on_runtime_error(APP_RTA_ERROR_ACQUIRE_FAILED, sc);
    return sc;
  }
  return SL_STATUS_OK;
}

/*******************************************************************************
 * Finish access to variables protected by the context
 ******************************************************************************/
static sl_status_t spp_rta_release(void)
{
  sl_status_t sc = app_rta_release(ctx);
  if (sc != SL_STATUS_OK) {
    on_runtime_error(APP_RTA_ERROR_RELEASE_FAILED, sc);
    return sc;
  }
  return SL_STATUS_OK;
}

/*******************************************************************************
 * Proceed with execution of runtime context
 ******************************************************************************/
static void spp_rta_proceed(void)
{
  (void)app_rta_proceed(ctx);
}

// -----------------------------------------------------------------------------
// Event / callback definitions

void spp_on_bt_event(sl_bt_msg_t *evt)
{
  sl_status_t sc;
  sc = spp_rta_acquire();
  if (sc != SL_STATUS_OK) {
    return;
  }
  switch (SL_BT_MSG_ID(evt->header)) {
    // Connection opened
    case sl_bt_evt_connection_opened_id:
      on_bt_evt_connection_opened(&evt->data.evt_connection_opened);
      break;
    // Service discovered
    case sl_bt_evt_gatt_service_id:
      on_bt_evt_service(&evt->data.evt_gatt_service);
      break;
    // Procedure completed (eg. service or characteristic discovery)
    case sl_bt_evt_gatt_procedure_completed_id:
      on_bt_evt_gatt_procedure_completed();
      break;
    // One of our characteristics has been written
    case sl_bt_evt_gatt_server_attribute_value_id:
      on_bt_evt_gatt_server_attribute_value(&evt->data.evt_gatt_server_attribute_value);
      break;
    // Notification received
    case sl_bt_evt_gatt_characteristic_value_id:
      on_bt_evt_gatt_characteristic_value(&evt->data.evt_gatt_characteristic_value);
      break;
    // Connection closed
    case sl_bt_evt_connection_closed_id:
      on_bt_evt_connection_closed(&evt->data.evt_connection_closed);
      break;
    // Default event handler
    default:
      break;
  }
  sc = spp_rta_release();
  if (sc != SL_STATUS_OK) {
    return;
  }
}
