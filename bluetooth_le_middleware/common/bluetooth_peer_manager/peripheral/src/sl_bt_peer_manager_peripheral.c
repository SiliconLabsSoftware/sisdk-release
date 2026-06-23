/***************************************************************************//**
 * @file
 * @brief Bluetooth Peer Manager - peripheral
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
#include "sl_component_catalog.h"
#include "sl_bt_peer_manager_common.h"
#include "sl_bt_peer_manager_common_config.h"
#include "sli_bt_peer_manager_common.h"
#include "sl_bt_peer_manager_peripheral.h"
#include "sli_bt_peer_manager_peripheral.h"
#include "sl_bt_peer_manager_peripheral_config.h"

// -----------------------------------------------------------------------------
// Macros and Typedefs
typedef struct sl_bt_peer_manager_advertiser_s {
  uint8_t advertising_handle;
  uint8_t adv_discovery_mode;
  sl_bt_gap_phy_t adv_phy;
} sl_bt_peer_manager_advertiser_t;

typedef enum {
  SL_BT_PEER_MANAGER_STATE_IDLE = 0u,
  SL_BT_PEER_MANAGER_STATE_CLOSING,
  SL_BT_PEER_MANAGER_ADVERTISING,
} sl_bt_peer_manager_state_id;

// -----------------------------------------------------------------------------
// Forward declaration of private functions
static sl_bt_peer_manager_state_id get_state(void);
static void set_state(sl_bt_peer_manager_state_id new_state);

// -----------------------------------------------------------------------------
// Static variables
static sl_bt_peer_manager_advertiser_t advertiser;
static sl_bt_peer_manager_state_id state;

// -----------------------------------------------------------------------------
// Public functions
void sl_bt_peer_manager_peripheral_init(void)
{
  // Set default values
  advertiser.advertising_handle = SL_BT_INVALID_ADVERTISING_SET_HANDLE;
  advertiser.adv_discovery_mode = SL_BT_PEER_MANAGER_PERIPHERAL_CONFIG_DEFAULT_ADV_DISCOVERY_MODE;
  advertiser.adv_phy = SL_BT_PEER_MANAGER_PERIPHERAL_CONFIG_ADV_PHY;
  sli_bt_peer_manager_clear_all_connections();
  set_state(SL_BT_PEER_MANAGER_STATE_IDLE);
}

void sli_bt_peer_manager_peripheral_on_bt_event(sl_bt_msg_t *evt)
{
  sl_status_t sc;
  sl_bt_peer_manager_evt_type_t peer_evt;

  switch (SL_BT_MSG_ID(evt->header)) {
    case sl_bt_evt_system_boot_id:
    {
      sl_bt_peer_manager_peripheral_init();
      break;
    }
    case sl_bt_evt_advertiser_timeout_id:
      // Received when the number of advertising events command is done
      if (evt->data.evt_advertiser_timeout.handle == advertiser.advertising_handle) {
        peer_evt.evt_id = SL_BT_PEER_MANAGER_ON_ADV_STOPPED;
        peer_evt.connection_id = SL_BT_INVALID_CONNECTION_HANDLE;
        set_state(SL_BT_PEER_MANAGER_STATE_IDLE);
        sl_bt_peer_manager_on_event(&peer_evt);
      }
      break;

    case sl_bt_evt_connection_opened_id:
      if (evt->data.evt_connection_opened.advertiser == advertiser.advertising_handle
          && evt->data.evt_connection_opened.role == sl_bt_connection_role_peripheral) {
        sli_bt_peer_manager_add_connection(evt->data.evt_connection_opened.connection,
                                           evt->data.evt_connection_opened.address,
                                           sl_bt_connection_role_peripheral);
        sli_bt_peer_manager_log_info("Connection opened as peripheral with '%02x:%02x:%02x:%02x:%02x:%02x'" APP_LOG_NL,
                                     evt->data.evt_connection_opened.address.addr[5],
                                     evt->data.evt_connection_opened.address.addr[4],
                                     evt->data.evt_connection_opened.address.addr[3],
                                     evt->data.evt_connection_opened.address.addr[2],
                                     evt->data.evt_connection_opened.address.addr[1],
                                     evt->data.evt_connection_opened.address.addr[0]);
        peer_evt.evt_id = SL_BT_PEER_MANAGER_ON_CONN_OPENED_PERIPHERAL;
        peer_evt.connection_id = evt->data.evt_connection_opened.connection;
        set_state(SL_BT_PEER_MANAGER_STATE_IDLE);
        sl_bt_peer_manager_on_event(&peer_evt);
      }
      break;

    case sl_bt_evt_connection_closed_id:
      if (sli_bt_peer_manager_is_conn_handle_in_array(evt->data.evt_connection_closed.connection)
          && !(sl_bt_peer_manager_is_conn_handle_central(evt->data.evt_connection_closed.connection))) {
        sli_bt_peer_manager_log_info("Peripheral device connection closed, reason 0x%x" APP_LOG_NL,
                                     evt->data.evt_connection_closed.reason);
        sc = sli_bt_peer_manager_delete_connection(evt->data.evt_connection_closed.connection);
        if (sc != SL_STATUS_OK) {
          peer_evt.evt_id = SL_BT_PEER_MANAGER_ERROR;
          peer_evt.connection_id = SL_BT_INVALID_CONNECTION_HANDLE;
        } else {
          peer_evt.evt_id = SL_BT_PEER_MANAGER_ON_CONN_CLOSED;
          peer_evt.connection_id = evt->data.evt_connection_closed.connection;
        }
        sl_bt_peer_manager_on_event(&peer_evt);
      }
      break;
  }
}

sl_status_t sl_bt_peer_manager_peripheral_set_advertiser_discovery_mode(sl_bt_advertiser_discovery_mode_t adv_discovery_mode)
{
  if (get_state() == SL_BT_PEER_MANAGER_ADVERTISING) {
    sli_bt_peer_manager_log_info("Already advertising. \
                                 New settings will take effect the next time advertising is started." APP_LOG_NL);
  }
  advertiser.adv_discovery_mode = adv_discovery_mode;
  return SL_STATUS_OK;
}

sl_status_t sl_bt_peer_manager_peripheral_set_advertiser_phy(sl_bt_gap_phy_t adv_phy)
{
  if (adv_phy != sl_bt_gap_phy_1m
      && adv_phy != sl_bt_gap_phy_2m
      && adv_phy != sl_bt_gap_phy_coded
      && adv_phy != sl_bt_gap_phy_any) {
    return SL_STATUS_INVALID_PARAMETER;
  }
  if (get_state() == SL_BT_PEER_MANAGER_ADVERTISING) {
    sli_bt_peer_manager_log_info("Already advertising. \
                                 New settings will take effect the next time advertising is started." APP_LOG_NL);
  }
  advertiser.adv_phy = adv_phy;
  return SL_STATUS_OK;
}

sl_status_t sl_bt_peer_manager_peripheral_create_connection(void)
{
  if (get_state() == SL_BT_PEER_MANAGER_ADVERTISING) {
    sli_bt_peer_manager_log_error("Already advertising" APP_LOG_NL);
    return SL_STATUS_INVALID_STATE;
  }
  // Start advertising
  sl_status_t sc = sl_bt_peer_manager_peripheral_start_advertising(advertiser.advertising_handle);
  if (sc == SL_STATUS_OK) {
    set_state(SL_BT_PEER_MANAGER_ADVERTISING);
  }
  return sc;
}

sl_status_t sl_bt_peer_manager_peripheral_start_advertising(uint8_t advertising_handle)
{
  sl_status_t sc;
  // Stop running advertising
  if (get_state() == SL_BT_PEER_MANAGER_ADVERTISING) {
    sc = sl_bt_advertiser_stop(advertiser.advertising_handle);
    if (sc != SL_STATUS_OK) {
      return sc;
    }
  }
  if (advertising_handle != SL_BT_INVALID_ADVERTISING_SET_HANDLE) {
    advertiser.advertising_handle = advertising_handle;
  } else {
    // If we already have an existing set, delete it
    if (advertiser.advertising_handle != SL_BT_INVALID_ADVERTISING_SET_HANDLE) {
      sc = sl_bt_advertiser_delete_set(advertiser.advertising_handle);
      if (sc != SL_STATUS_OK) {
        return sc;
      }
    }

    // Create new advertiser set
    sc = sl_bt_advertiser_create_set(&advertiser.advertising_handle);
    if (sc != SL_STATUS_OK) {
      return sc;
    }
  }
  // Set advertising interval
  sc = sl_bt_advertiser_set_timing(
    advertiser.advertising_handle,
    SL_BT_PEER_MANAGER_PERIPHERAL_CONFIG_ADV_TIMING_INTERVAL_MIN,
    SL_BT_PEER_MANAGER_PERIPHERAL_CONFIG_ADV_TIMING_INTERVAL_MAX,
    SL_BT_PEER_MANAGER_PERIPHERAL_CONFIG_ADV_TIMING_DURATION,
    SL_BT_PEER_MANAGER_PERIPHERAL_CONFIG_ADV_TIMING_MAX_EVENTS);
  if (sc != SL_STATUS_OK) {
    return sc;
  }

  if (advertiser.adv_phy == sl_bt_gap_phy_1m
      || advertiser.adv_phy == sl_bt_gap_phy_any) {
    // Generate data for legacy advertiser using phy_1m
    sc = sl_bt_legacy_advertiser_generate_data(advertiser.advertising_handle,
                                               advertiser.adv_discovery_mode);
    if (sc != SL_STATUS_OK) {
      sli_bt_peer_manager_log_info("Legacy advertiser generate data failed..." APP_LOG_NL);
      return sc;
    }
    sc = sl_bt_legacy_advertiser_start(advertiser.advertising_handle,
                                       SL_BT_PEER_MANAGER_PERIPHERAL_CONFIG_DEFAULT_ADV_CONNECTION_MODE);
    if (sc != SL_STATUS_OK) {
      sli_bt_peer_manager_log_info("Legacy advertiser start failed..." APP_LOG_NL);
      return sc;
    }
  } else {
    // Generate data for extended advertiser
    sc = sl_bt_extended_advertiser_generate_data(advertiser.advertising_handle,
                                                 advertiser.adv_discovery_mode);
    if (sc != SL_STATUS_OK) {
      sli_bt_peer_manager_log_info("Extended advertiser generate data failed..." APP_LOG_NL);
      return sc;
    }
    if (advertiser.adv_phy == sl_bt_gap_phy_coded) {
      sc = sl_bt_extended_advertiser_set_phy(advertiser.advertising_handle,
                                             sl_bt_gap_phy_1m,
                                             sl_bt_gap_phy_coded);
      if (sc != SL_STATUS_OK) {
        sli_bt_peer_manager_log_info("Extended advertiser set coded phy failed..." APP_LOG_NL);
        return sc;
      }
    } else {
      sc = sl_bt_extended_advertiser_set_phy(advertiser.advertising_handle,
                                             sl_bt_gap_phy_1m,
                                             sl_bt_gap_phy_2m);
      if (sc != SL_STATUS_OK) {
        sli_bt_peer_manager_log_info("Extended advertiser set 2M phy failed..." APP_LOG_NL);
        return sc;
      }
    }

    sc = sl_bt_extended_advertiser_start(advertiser.advertising_handle,
                                         sl_bt_extended_advertiser_connectable,
                                         0);
    if (sc != SL_STATUS_OK) {
      sli_bt_peer_manager_log_info("Extended advertiser start failed..." APP_LOG_NL);
      return sc;
    }
  }

  sli_bt_peer_manager_log_info("Started advertising..." APP_LOG_NL);
  return sc;
}

sl_status_t sl_bt_peer_manager_peripheral_stop_advertising(uint8_t advertising_handle)
{
  sl_status_t sc;
  if (advertising_handle != SL_BT_INVALID_ADVERTISING_SET_HANDLE) {
    advertiser.advertising_handle = advertising_handle;
  }
  // Delete advertiser set - the deletion stops the advertising
  sc = sl_bt_advertiser_delete_set(advertiser.advertising_handle);
  if (sc == SL_STATUS_OK) {
    advertiser.advertising_handle = SL_BT_INVALID_ADVERTISING_SET_HANDLE;
  } else if (sc == SL_STATUS_INVALID_PARAMETER) {
    // Don't return error if the advertising set has already been deleted
    sc = SL_STATUS_OK;
    advertiser.advertising_handle = SL_BT_INVALID_ADVERTISING_SET_HANDLE;
  }
  return sc;
}

sl_status_t sl_bt_peer_manager_peripheral_close_connection(uint8_t conn_handle)
{
  sl_status_t sc = SL_STATUS_OK;
  if (sli_bt_peer_manager_is_conn_handle_in_array(conn_handle)
      && !(sl_bt_peer_manager_is_conn_handle_central(conn_handle))) {
    sli_bt_peer_manager_log_info("Closing connection." APP_LOG_NL);
    sc = sl_bt_connection_close(conn_handle);
    set_state(SL_BT_PEER_MANAGER_STATE_CLOSING);
    if (sc != SL_STATUS_OK) {
      return sc;
    }
  } else {
    sli_bt_peer_manager_log_error("Connection handle not found." APP_LOG_NL);
    return SL_STATUS_NOT_FOUND;
  }
  return sc;
}

// -----------------------------------------------------------------------------
// Private functions
static sl_bt_peer_manager_state_id get_state(void)
{
  return state;
}

static void set_state(sl_bt_peer_manager_state_id new_state)
{
  state = new_state;
}
