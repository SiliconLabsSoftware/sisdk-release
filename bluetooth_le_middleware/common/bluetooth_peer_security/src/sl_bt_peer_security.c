/***************************************************************************//**
 * @file
 * @brief Bluetooth Peer Security
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
#include "sl_bt_peer_security.h"
#include "sl_bt_peer_security_config.h"
#include "sli_bt_peer_security.h"
#include "app_rta.h"
#include "sl_common.h"

#define NL_SEC                         "\n"
#if defined(SL_CATALOG_APP_LOG_PRESENT) && SL_BT_PEER_SECURITY_LOG
  #include "app_log.h"
  #define peer_security_log_info(...)    app_log_info(SL_BT_PEER_SECURITY_LOG_PREFIX " " __VA_ARGS__)
  #define peer_security_log_warning(...) app_log_warning(SL_BT_PEER_SECURITY_LOG_PREFIX " " __VA_ARGS__)
  #define peer_security_log_error(...)   app_log_error(SL_BT_PEER_SECURITY_LOG_PREFIX " " __VA_ARGS__)
#else
  #define peer_security_log_info(...)
  #define peer_security_log_warning(...)
  #define peer_security_log_error(...)
#endif

// -----------------------------------------------------------------------------
// Private function declarations
static sl_status_t send_confirmation(bool confirm);
static void configure_sm(void);
static uint8_t build_sm_flags(void);
static void on_runtime_error(app_rta_error_t error, sl_status_t result);

// -----------------------------------------------------------------------------
// Static variables
static sl_bt_peer_security_process_state_t confirm_process_state = SL_BT_PEER_SECURITY_PROCESS_IDLE;
static uint8_t confirm_conn_handle = SL_BT_INVALID_CONNECTION_HANDLE;
static app_rta_context_t ctx;

// -----------------------------------------------------------------------------
// Callback weak implementation
SL_WEAK void sl_bt_peer_security_on_event(uint8_t handle)
{
  (void)handle;
}

// -----------------------------------------------------------------------------
// Public functions

sl_status_t sl_bt_peer_security_send_confirmation(bool confirm)
{
  sl_status_t sc;
  sc = app_rta_acquire(ctx);
  if (sc != SL_STATUS_OK) {
    peer_security_log_error("Failed to acquire RTA context for sending confirmation, sc=0x%lx" NL_SEC, sc);
    return sc;
  }

  sc = send_confirmation(confirm);

  (void)app_rta_release(ctx);
  return sc;
}

// -----------------------------------------------------------------------------
// Private functions

void sli_bt_peer_security_init(void)
{
  confirm_process_state = SL_BT_PEER_SECURITY_PROCESS_IDLE;
  confirm_conn_handle = SL_BT_INVALID_CONNECTION_HANDLE;
}

sl_status_t sli_bt_peer_security_on_bt_event(const sl_bt_msg_t *evt)
{
  sl_status_t sc = SL_STATUS_OK;

  switch (SL_BT_MSG_ID(evt->header)) {
    case sl_bt_evt_system_boot_id:
      sc = app_rta_acquire(ctx);
      if (sc != SL_STATUS_OK) {
        peer_security_log_error("Failed to acquire RTA context, sc=0x%lx" NL_SEC, sc);
        break;
      }
      sli_bt_peer_security_init();
      configure_sm();
      (void)app_rta_release(ctx);
      break;

    case sl_bt_evt_sm_bonded_id:
      peer_security_log_info("Bonded (handle=%u, bonding=%u)." NL_SEC,
                             evt->data.evt_sm_bonded.connection,
                             evt->data.evt_sm_bonded.bonding);
      break;

    case sl_bt_evt_sm_bonding_failed_id:
      peer_security_log_warning(
        "Bonding failed (handle=%u, reason=0x%lx)." NL_SEC,
        evt->data.evt_sm_bonding_failed.connection,
        (unsigned long)evt->data.evt_sm_bonding_failed.reason);
      if ((evt->data.evt_sm_bonding_failed.reason
           == SL_STATUS_BT_SMP_PAIRING_NOT_SUPPORTED)
          || (evt->data.evt_sm_bonding_failed.reason
              == SL_STATUS_BT_CTRL_PIN_OR_KEY_MISSING)) {
        bd_addr address;
        uint8_t address_type;
        uint32_t bonding_handle;
        uint8_t security_mode;
        uint8_t key_size;

        sc = sl_bt_connection_get_remote_address(evt->data.evt_sm_bonding_failed.connection,
                                                 &address,
                                                 &address_type);
        if (sc != SL_STATUS_OK) {
          peer_security_log_error("Failed to get remote address, sc=0x%lx" NL_SEC, sc);
          break;
        }
        sc = sl_bt_sm_find_bonding_by_address(address, &bonding_handle, &security_mode, &key_size);
        if (sc != SL_STATUS_OK) {
          peer_security_log_error("Bonding not found for address, sc=0x%lx" NL_SEC, sc);
          break;
        }
        sc = sl_bt_sm_delete_bonding((uint8_t)bonding_handle);
        if (sc != SL_STATUS_OK) {
          peer_security_log_error("Failed to delete bonding, sc=0x%lx" NL_SEC, sc);
        } else {
          peer_security_log_info("Stale bonding deleted." NL_SEC);
        }
      }
      break;

    case sl_bt_evt_sm_passkey_display_id:
      peer_security_log_info("Display passkey: %06lu" NL_SEC,
                             (unsigned long)evt->data.evt_sm_passkey_display.passkey);
      break;

    case sl_bt_evt_sm_passkey_request_id:
      peer_security_log_info("Passkey requested (handle=%u)." NL_SEC,
                             evt->data.evt_sm_passkey_request.connection);
      sc = sl_bt_sm_enter_passkey(evt->data.evt_sm_passkey_request.connection,
                                  SL_BT_PEER_SECURITY_DEFAULT_PASSKEY);
      if (sc != SL_STATUS_OK) {
        peer_security_log_error("Failed to enter passkey, sc=0x%lx" NL_SEC, sc);
      }
      break;

    case sl_bt_evt_sm_confirm_passkey_id:
      sc = app_rta_acquire(ctx);
      if (sc != SL_STATUS_OK) {
        peer_security_log_error("Failed to acquire RTA context, sc=0x%lx" NL_SEC, sc);
        break;
      }
      peer_security_log_info("Passkey confirmation required: %06lu" NL_SEC,
                             (unsigned long)evt->data.evt_sm_confirm_passkey.passkey);
      confirm_conn_handle = evt->data.evt_sm_confirm_passkey.connection;
      confirm_process_state = SL_BT_PEER_SECURITY_PROCESS_STARTED;
      sl_bt_peer_security_on_event(confirm_conn_handle);
#if (SL_BT_PEER_SECURITY_AUTO_ALLOW_CONFIRMATION == 1)
      sc = send_confirmation(true);
      if (sc != SL_STATUS_OK) {
        peer_security_log_error("Failed to send confirmation, sc=0x%lx" NL_SEC, sc);
      }
#endif
      (void)app_rta_release(ctx);
      break;
    default:
      break;
  }
  return sc;
}

static sl_status_t send_confirmation(bool confirm)
{
  if (confirm_process_state != SL_BT_PEER_SECURITY_PROCESS_STARTED) {
    return SL_STATUS_INVALID_STATE;
  }

  uint8_t accept = (true == confirm) ? 1u : 0u;
  sl_status_t sc = sl_bt_sm_passkey_confirm(confirm_conn_handle, accept);
  if (sc != SL_STATUS_OK) {
    peer_security_log_error("Failed to confirm passkey, sc=0x%lx" NL_SEC, sc);
  } else {
    peer_security_log_info("Passkey %s." NL_SEC, accept ? "confirmed" : "denied");
  }

  confirm_conn_handle = SL_BT_INVALID_CONNECTION_HANDLE;
  confirm_process_state = SL_BT_PEER_SECURITY_PROCESS_IDLE;
  return sc;
}

void sli_bt_peer_security_rta_init(void)
{
  sl_status_t sc;
  app_rta_config_t config = { .requirement.runtime = false,
                              .requirement.guard = true,
                              .requirement.signal = false,
                              .step = NULL,
                              .priority = 0,
                              .stack_size = 0,
                              .error = on_runtime_error,
                              .wait_for_guard = 10 };
  sc = app_rta_create_context(&config, &ctx);
  if (sc != SL_STATUS_OK) {
    peer_security_log_error("Failed to create context, sc=0x%lx" NL_SEC, sc);
  }
}

void sli_bt_peer_security_rta_ready(void)
{
  (void)app_rta_proceed(ctx);
}

static void on_runtime_error(app_rta_error_t error, sl_status_t result)
{
  (void)result;
  switch (error) {
    case APP_RTA_ERROR_RUNTIME_INIT_FAILED:
      peer_security_log_error("RTA runtime init failed, sc=0x%lx" NL_SEC, result);
      break;
    case APP_RTA_ERROR_ACQUIRE_FAILED:
      peer_security_log_error("RTA acquire failed, sc=0x%lx" NL_SEC, result);
      break;
    case APP_RTA_ERROR_RELEASE_FAILED:
      peer_security_log_error("RTA release failed, sc=0x%lx" NL_SEC, result);
      break;
    default:
      peer_security_log_error("RTA generic error, sc=0x%lx" NL_SEC, result);
      break;
  }
}

static void configure_sm(void)
{
  sl_status_t sc;

#if SL_BT_PEER_SECURITY_DELETE_BONDINGS_ON_INIT
  sc = sl_bt_sm_delete_bondings();
  if (sc != SL_STATUS_OK) {
    peer_security_log_error("Failed to delete bondings on init, sc=0x%lx" NL_SEC, sc);
  } else {
    peer_security_log_info("All bondings deleted on init." NL_SEC);
  }
#endif

  sc = sl_bt_sm_store_bonding_configuration(SL_BT_PEER_SECURITY_MAX_BONDINGS, 0);
  if (sc != SL_STATUS_OK) {
    peer_security_log_error("Failed to set bonding configuration, sc=0x%lx" NL_SEC, sc);
  }

  uint8_t sm_flags = build_sm_flags();

  sc = sl_bt_sm_configure(sm_flags, SL_BT_PEER_SECURITY_IO_CAPABILITY);
  if (sc != SL_STATUS_OK) {
    peer_security_log_error("Failed to configure SM, sc=0x%lx" NL_SEC, sc);
    return;
  }

#if SL_BT_PEER_SECURITY_BONDING_ENABLED
  sc = sl_bt_sm_set_bondable_mode(1);
#else
  sc = sl_bt_sm_set_bondable_mode(0);
  (void)sl_bt_sm_delete_bondings();
#endif
  if (sc != SL_STATUS_OK) {
    peer_security_log_error("Failed to set bondable mode, sc=0x%lx" NL_SEC, sc);
    return;
  }

#if (SL_BT_PEER_SECURITY_IO_CAPABILITY != sl_bt_sm_io_capability_noinputnooutput) \
  && (SL_BT_PEER_SECURITY_DEFAULT_PASSKEY != 0)
  sc = sl_bt_sm_set_passkey(SL_BT_PEER_SECURITY_DEFAULT_PASSKEY);
  if (sc != SL_STATUS_OK) {
    peer_security_log_error("Failed to set passkey, sc=0x%lx" NL_SEC, sc);
    return;
  }
#endif

  peer_security_log_info("SM configured." NL_SEC);
}

static uint8_t build_sm_flags(void)
{
  uint8_t flags = 0u;

#if SL_BT_PEER_SECURITY_MITM_REQUIRED
  flags |= SL_BT_SM_CONFIGURATION_MITM_REQUIRED;
#endif

#if SL_BT_PEER_SECURITY_BONDED_DEVICES_ONLY
  flags |= SL_BT_SM_CONFIGURATION_CONNECTIONS_FROM_BONDED_DEVICES_ONLY;
#endif

#if SL_BT_PEER_SECURITY_REJECT_DEBUG_KEYS
  flags |= SL_BT_SM_CONFIGURATION_REJECT_DEBUG_KEYS;
#endif

  return flags;
}
