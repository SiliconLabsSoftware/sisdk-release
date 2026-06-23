/***************************************************************************//**
 * @file app.c
 * @brief Direct Connect Control Interface Unit
 *
 * Direct Connect Control Interface Unit.
 * Single button to start, automatic progression through states.
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 * SPDX-License-Identifier: Zlib
 ******************************************************************************/

// -----------------------------------------------------------------------------
//                                   Includes
// -----------------------------------------------------------------------------

#include <string.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdarg.h>
#include <inttypes.h>

#include "sl_wisun_api.h"
#include "sl_component_catalog.h"
#include "sl_simple_button_instances.h"
#include "sl_board_control.h"
#include "sl_power_manager.h"
#include "sl_sleeptimer.h"
#include "dmd.h"
#include "glib.h"
#include "sys/socket.h"
#include "arpa/inet.h"
#include "netinet/in.h"
#include "cmsis_os2.h"
#include "app_cli.h"

// PSA crypto for PMK handling
#include "psa/crypto.h"
#include "sl_psa_crypto.h"
#include "em_system.h"

// -----------------------------------------------------------------------------
//                              Macros and Typedefs
// -----------------------------------------------------------------------------

/// Message IDs for event queue
#define SL_DC_CIU_MSG_BTN_0              0
#define SL_DC_CIU_MSG_BTN_1              1
#define SL_DC_CIU_MSG_IDLE_TIMEOUT       2

/// Task stack sizes (words)
#define SL_DC_CIU_BTN_TASK_STACK_SIZE    (512U)
#define SL_DC_CIU_UDP_RX_TASK_STACK_SIZE (512U)

/// Message queue size (one slot per message type: BTN_0, BTN_1, IDLE_TIMEOUT)
#define SL_DC_CIU_MSG_QUEUE_SIZE    (3U)

/// DC CIU states - simplified automatic flow
typedef enum {
  STATE_IDLE = 0,       ///< Waiting for BTN0 to start
  STATE_SCANNING,       ///< Scanning for matching DC ID
  STATE_CONNECTING,     ///< Connecting to discovered server
  STATE_CONNECTED,      ///< Connected, inactivity timer active
  STATE_STOPPING,       ///< Stopping DC client before EM4
  STATE_STOPPED         ///< Stopped, about to enter EM4
} dc_ciu_state_t;

/// Reason for entering STOPPING state
typedef enum {
  STOP_REASON_DELIBERATE = 0,  ///< User pressed BTN0
  STOP_REASON_TIMEOUT,         ///< Inactivity timeout
  STOP_REASON_SCAN_FAILED,     ///< Scan API error or no server found
  STOP_REASON_CONNECT_FAILED,  ///< PMK import, connect API, or connection failed
  STOP_REASON_CONNECTION_LOST  ///< Connection lost to server
} stop_reason_t;

// -----------------------------------------------------------------------------
//                                Static Variables
// -----------------------------------------------------------------------------

/// Current state
static dc_ciu_state_t state = STATE_IDLE;

/// Stop reason (logged before EM4 entry)
static stop_reason_t stop_reason = STOP_REASON_DELIBERATE;

/// Idle timer (triggers EM4 after inactivity in any state)
static sl_sleeptimer_timer_handle_t idle_timer;

/// GLIB context
static GLIB_Context_t glib_context;

/// PHY configuration
static sl_wisun_phy_config_t phy_config;

/// Target DC ID we're looking for
static sl_wisun_dc_id_t target_dc_id;

/// Discovered server MAC address
static sl_wisun_mac_address_t server_mac;

/// Server's link-local IPv6 address
static in6_addr_t server_ip;

/// UDP socket for messaging
static int udp_socket = SOCKET_INVALID_ID;

/// Message counter
static uint32_t msg_count = 0;

/// Connection start timestamp (tick count when BTN0 pressed)
static uint32_t connect_start_tick = 0;

/// Connection time in milliseconds (calculated on connect)
static uint32_t connect_time_ms = 0;

/// PMK key ID for Direct Connect authentication
static psa_key_id_t dc_pmk_key_id = MBEDTLS_SVC_KEY_ID_INIT;

/// UDP RX task ID
static osThreadId_t udp_rx_task_id = NULL;

/// Message queue ID
static osMessageQueueId_t msg_queue = NULL;

// -----------------------------------------------------------------------------
//                          Forward Declarations
// -----------------------------------------------------------------------------

static void handle_dc_client_stopped(void);

// -----------------------------------------------------------------------------
//                          Display Functions
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * Draw text on the display.
 *
 * @param line The line number to draw on.
 * @param text The text string to draw.
 ******************************************************************************/
static void draw_text(uint8_t line, const char *text)
{
  GLIB_drawStringOnLine(&glib_context, text, line, GLIB_ALIGN_LEFT, 2, 2, true);
}

/***************************************************************************//**
 * Initialize the display.
 *
 * Initializes the board display and GLIB graphics context.
 ******************************************************************************/
static void init_display(void)
{
  EMSTATUS status;

  sl_board_enable_display();

  status = DMD_init(0);
  if (status != DMD_OK) {
    return;
  }

  status = GLIB_contextInit(&glib_context);
  if (status != GLIB_OK) {
    return;
  }

  glib_context.backgroundColor = White;
  glib_context.foregroundColor = Black;
  GLIB_setFont(&glib_context, (GLIB_Font_t *)&GLIB_FontNarrow6x8);
}

/***************************************************************************//**
 * Refresh the display.
 *
 * Redraws the display with current state information, button hints,
 * and an optional status message.
 *
 * @param fmt Printf-style format string for status message.
 * @param ... Format arguments.
 ******************************************************************************/
static void refresh_display(const char *fmt, ...)
{
  char status_msg[32] = "";
  const char *state_str;
  char time_str[24];
  va_list args;

  va_start(args, fmt);
  vsnprintf(status_msg, sizeof(status_msg), fmt, args);
  va_end(args);

  GLIB_clear(&glib_context);

  draw_text(0, "=== DC CIU ===");

  // Button hints based on state
  switch (state) {
    case STATE_IDLE:
      draw_text(2, "BTN0: Start");
      draw_text(3, "BTN1: -");
      break;

    case STATE_SCANNING:
    case STATE_CONNECTING:
      draw_text(2, "BTN0: Stop");
      draw_text(3, "BTN1: -");
      break;

    case STATE_CONNECTED:
      draw_text(2, "BTN0: Stop");
      draw_text(3, "BTN1: Send msg");
      break;

    case STATE_STOPPING:
      draw_text(2, "BTN0: -");
      draw_text(3, "BTN1: -");
      break;

    case STATE_STOPPED:
      draw_text(2, "BTN0: Wakeup");
      draw_text(3, "BTN1: Wakeup");
      break;

    default:
      break;
  }

  draw_text(5, "----------------");
  draw_text(6, status_msg);

  // State string
  switch (state) {
    case STATE_IDLE:       state_str = "IDLE";       break;
    case STATE_SCANNING:   state_str = "SCANNING";   break;
    case STATE_CONNECTING: state_str = "CONNECTING"; break;
    case STATE_CONNECTED:  state_str = "CONNECTED";  break;
    case STATE_STOPPING:   state_str = "STOPPING";   break;
    case STATE_STOPPED:    state_str = "STOPPED";    break;
    default:               state_str = "UNKNOWN";    break;
  }
  draw_text(8, state_str);

  // Show connection time in CONNECTED state
  if (state == STATE_CONNECTED && connect_time_ms > 0) {
    snprintf(time_str, sizeof(time_str), "T=%lu.%lus",
             (unsigned long)(connect_time_ms / 1000),
             (unsigned long)((connect_time_ms % 1000) / 100));
    draw_text(9, time_str);
  }

  DMD_updateDisplay();
}

// -----------------------------------------------------------------------------
//                          Timer Callbacks
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * Idle timer callback.
 *
 * Fires after idle_timeout_ms without activity.
 * Posts message to event queue for processing in task context.
 *
 * @param handle Pointer to the timer handle (unused).
 * @param data User data pointer (unused).
 ******************************************************************************/
static void idle_timer_callback(sl_sleeptimer_timer_handle_t *handle,
                                void *data)
{
  uint8_t msg = SL_DC_CIU_MSG_IDLE_TIMEOUT;

  (void)handle;
  (void)data;

  // Post message to be handled in task context
  if (msg_queue != NULL) {
    osMessageQueuePut(msg_queue, &msg, 0U, 0U);
  }
}

/***************************************************************************//**
 * Reset the idle timer.
 *
 * Called when there is user activity on CLI commands
 ******************************************************************************/
void app_reset_idle_timer(void)
{
  sl_sleeptimer_restart_timer_ms(&idle_timer,
                                 dc_ciu_settings.idle_timeout_ms,
                                 idle_timer_callback,
                                 NULL, 0, 0);
}

// -----------------------------------------------------------------------------
//                          PMK Import Function
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * Import the Direct Connect PMK into PSA crypto.
 *
 * Imports the pre-shared PMK key for Direct Connect authentication.
 * Uses hardware security features (Vault) when available.
 *
 * @returns SL_STATUS_OK on success, SL_STATUS_FAIL on error.
 ******************************************************************************/
static sl_status_t import_direct_connect_pmk(void)
{
  psa_key_attributes_t pmk_key_attributes = psa_key_attributes_init();
  psa_key_location_t pmk_location = PSA_KEY_LOCATION_LOCAL_STORAGE;
  sl_status_t status = SL_STATUS_OK;
  psa_status_t ret;

#if defined(SEMAILBOX_PRESENT)
  if (SYSTEM_GetSecurityCapability() == securityCapabilityVault) {
    pmk_location = SL_PSA_KEY_LOCATION_WRAPPED;
  }
#endif

  psa_set_key_lifetime(&pmk_key_attributes,
                       PSA_KEY_LIFETIME_FROM_PERSISTENCE_AND_LOCATION(PSA_KEY_LIFETIME_VOLATILE, pmk_location));

  if (dc_pmk_key_id != MBEDTLS_SVC_KEY_ID_INIT) {
    psa_destroy_key(dc_pmk_key_id);
  }

  dc_pmk_key_id = MBEDTLS_SVC_KEY_ID_INIT;

  psa_set_key_usage_flags(&pmk_key_attributes, PSA_KEY_USAGE_SIGN_HASH);
  psa_set_key_type(&pmk_key_attributes, PSA_KEY_TYPE_HMAC);
  psa_set_key_algorithm(&pmk_key_attributes, PSA_ALG_HMAC(PSA_ALG_SHA_1));

  ret = psa_import_key(&pmk_key_attributes,
                       dc_ciu_settings.pmk,
                       SL_WISUN_PMK_LEN,
                       &dc_pmk_key_id);
  if (ret != PSA_SUCCESS) {
    printf("PMK import failed: psa_import_key: %" PRIu32 "\n", (uint32_t)ret);
    status = SL_STATUS_FAIL;
  }

  psa_reset_key_attributes(&pmk_key_attributes);
  return status;
}

// -----------------------------------------------------------------------------
//                          UDP Socket & Messaging
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * Open UDP socket for messaging.
 *
 * Creates and binds a UDP socket for bidirectional communication
 * with the DC server.
 ******************************************************************************/
static void open_udp_socket(void)
{
  sockaddr_in6_t local_addr = { 0 };

  if (udp_socket != SOCKET_INVALID_ID) {
    return;
  }

  udp_socket = socket(AF_INET6, SOCK_DGRAM, IPPROTO_UDP);
  if (udp_socket == SOCKET_INVALID_ID) {
    printf("Socket open failed\n");
  } else {
    local_addr.sin6_family = AF_INET6;
    local_addr.sin6_port = htons(dc_ciu_settings.server_port);
    if (bind(udp_socket,
             (struct sockaddr *)&local_addr,
             sizeof(local_addr)) < 0) {
      printf("Socket bind failed\n");
    }
  }
}

/***************************************************************************//**
 * Close the UDP socket.
 *
 * Closes the UDP socket if it is currently open.
 ******************************************************************************/
static void close_udp_socket(void)
{
  if (udp_socket != SOCKET_INVALID_ID) {
    close(udp_socket);
    udp_socket = SOCKET_INVALID_ID;
  }
}

/***************************************************************************//**
 * Send a message to the DC server.
 *
 * Sends a numbered UDP message to the connected server and updates
 * the display with the result.
 ******************************************************************************/
static void send_message_to_server(void)
{
  ssize_t ret;
  char msg[64];
  sockaddr_in6_t dest_addr;

  if (udp_socket == SOCKET_INVALID_ID) {
    refresh_display("No socket");
    return;
  }

  memset(&dest_addr, 0, sizeof(dest_addr));
  dest_addr.sin6_family = AF_INET6;
  dest_addr.sin6_port = htons(dc_ciu_settings.server_port);
  memcpy(&dest_addr.sin6_addr, &server_ip, sizeof(in6_addr_t));

  msg_count++;
  snprintf(msg, sizeof(msg), "DC CIU msg #%lu", (unsigned long)msg_count);

  ret = sendto(udp_socket, msg, strlen(msg), 0,
               (struct sockaddr *)&dest_addr, sizeof(dest_addr));
  if (ret >= 0) {
    printf("TX: %s\n", msg);
    refresh_display("TX: msg #%lu", (unsigned long)msg_count);
  } else {
    printf("TX failed\n");
    refresh_display("TX: failed");
  }
}

// -----------------------------------------------------------------------------
//                          State Management
// -----------------------------------------------------------------------------

static const char *stop_reason_str(stop_reason_t reason)
{
  switch (reason) {
    case STOP_REASON_DELIBERATE: return "user stop";
    case STOP_REASON_TIMEOUT:    return "idle timeout";
    case STOP_REASON_SCAN_FAILED:     return "scan failed";
    case STOP_REASON_CONNECT_FAILED:  return "connect failed";
    case STOP_REASON_CONNECTION_LOST: return "conn lost";
    default:                     return "unknown";
  }
}

/***************************************************************************//**
 * Stop the DC client.
 *
 * Stops all active operations (timers, sockets, tasks) and initiates
 * DC client shutdown. After client stops, device enters EM4 sleep.
 *
 * @param reason The reason for stopping (deliberate, timeout, or error).
 ******************************************************************************/
static void initiate_stop(stop_reason_t reason)
{
  sl_status_t status;

  if (state == STATE_STOPPING || state == STATE_STOPPED) {
    return;
  }

  sl_sleeptimer_stop_timer(&idle_timer);
  close_udp_socket();

  stop_reason = reason;
  state = STATE_STOPPING;
  refresh_display("Stopping...");

  status = sl_wisun_stop_direct_connect_client();
  if (status != SL_STATUS_OK) {
    // Stop API failed — the client was likely already stopped.
    // Transition directly since we won't receive a STOPPED event.
    handle_dc_client_stopped();
  }
}

/***************************************************************************//**
 * Start scanning for DC server.
 *
 * Initiates a Direct Connect scan for a server with the target DC ID.
 * On success, transitions to SCANNING state. On failure, transitions
 * to STOPPING state with error reason.
 ******************************************************************************/
static void start_scan(void)
{
  sl_status_t status;

  // Get target DC ID from settings
  app_cli_get_dc_id(&target_dc_id);

  status = sl_wisun_start_direct_connect_scan(&target_dc_id,
                                              dc_ciu_settings.max_scan_solicits);
  if (status == SL_STATUS_OK) {
    state = STATE_SCANNING;
    refresh_display("Scanning...");
  } else {
    printf("Scan failed: 0x%04x\n", (unsigned)status);
    initiate_stop(STOP_REASON_SCAN_FAILED);
  }
}

/***************************************************************************//**
 * Start connecting to discovered server.
 *
 * Stops the ongoing scan, imports the PMK, and initiates connection
 * to the previously discovered server. On success, transitions to
 * CONNECTING state. On failure, transitions to STOPPING state.
 ******************************************************************************/
static void start_connect(void)
{
  sl_status_t status;

  sl_wisun_stop_direct_connect_scan();

  status = import_direct_connect_pmk();
  if (status != SL_STATUS_OK) {
    initiate_stop(STOP_REASON_CONNECT_FAILED);
    return;
  }

  status = sl_wisun_connect_to_direct_connect_server(&server_mac,
                                                     dc_pmk_key_id,
                                                     dc_ciu_settings.max_connect_solicits);
  if (status == SL_STATUS_OK) {
    state = STATE_CONNECTING;
    refresh_display("Connecting...");
  } else {
    printf("Connect failed: 0x%04x\n", (unsigned)status);
    initiate_stop(STOP_REASON_CONNECT_FAILED);
  }
}

// -----------------------------------------------------------------------------
//                          RTOS Tasks
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * UDP receive task.
 *
 * Blocks on recvfrom waiting for incoming UDP packets. Resets the
 * inactivity timer when data is received. Exits when socket is closed
 * or state changes from CONNECTED.
 *
 * @param args Task arguments (unused).
 ******************************************************************************/
static void udp_rx_task(void *args)
{
  char buff[128] = { 0 };
  ssize_t ret;

  (void)args;

  while (udp_socket != SOCKET_INVALID_ID && state == STATE_CONNECTED) {
    // Block waiting for UDP packet
    ret = recvfrom(udp_socket, buff, sizeof(buff) - 1, 0, NULL, NULL);
    if (ret > 0) {
      printf("RX: %s\n", buff);

      refresh_display("RX: %.24s", buff);

      sl_sleeptimer_restart_timer_ms(&idle_timer,
                                     dc_ciu_settings.idle_timeout_ms,
                                     idle_timer_callback,
                                     NULL, 0, 0);
    } else if (ret < 0) {
      break;
    }
  }

  udp_rx_task_id = NULL;
  osThreadExit();
}

/***************************************************************************//**
 * Start the UDP receive task.
 *
 * Creates the UDP receive task if not already running.
 ******************************************************************************/
static void start_udp_rx_task(void)
{
  const osThreadAttr_t udp_rx_task_attr = {
    .name        = "DcCiuUdpRxTask",
    .attr_bits   = osThreadDetached,
    .stack_size  = (SL_DC_CIU_UDP_RX_TASK_STACK_SIZE * sizeof(void *)) & 0xFFFFFFF8U,
    .priority    = osPriorityNormal
  };

  if (udp_rx_task_id != NULL) {
    return;  // Already running
  }

  udp_rx_task_id = osThreadNew(udp_rx_task, NULL, &udp_rx_task_attr);
  if (udp_rx_task_id == NULL) {
    printf("ERROR: UDP RX task failed!\n");
  }
}

// -----------------------------------------------------------------------------
//                          DC Client State Change Handlers
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * Handle client stopped.
 *
 * Called when DC client has stopped. Enters EM4 sleep mode.
 ******************************************************************************/
static void handle_dc_client_stopped(void)
{
  if (state != STATE_STOPPING) {
    return;
  }

  msg_count = 0;
  state = STATE_STOPPED;

  printf("Entering EM4 (%s)\n", stop_reason_str(stop_reason));
  refresh_display("EM4: %s", stop_reason_str(stop_reason));
  sl_power_manager_enter_em4();
}

/***************************************************************************//**
 * Handle connection failure.
 *
 * Called when DC client fails to connect to a server.
 ******************************************************************************/
static void handle_dc_client_connection_failed(void)
{
  if (state != STATE_CONNECTING) {
    return;
  }

  printf("Connection failed\n");
  initiate_stop(STOP_REASON_CONNECT_FAILED);
}

/***************************************************************************//**
 * Handle connection lost.
 *
 * Called when DC client loses connection to the server.
 ******************************************************************************/
static void handle_dc_client_connection_lost(void)
{
  if (state != STATE_CONNECTED) {
    return;
  }

  printf("Connection lost\n");
  initiate_stop(STOP_REASON_CONNECTION_LOST);
}

/***************************************************************************//**
 * Handle scan complete (no server found).
 *
 * Called when DC scan completes without finding the target server.
 ******************************************************************************/
static void handle_dc_client_scan_complete(void)
{
  if (state != STATE_SCANNING) {
    return;
  }

  printf("No server found\n");
  initiate_stop(STOP_REASON_SCAN_FAILED);
}

/***************************************************************************//**
 * Handle transition to connected state.
 *
 * Called when DC client successfully connects to a server.
 *
 * @param link_local_ipv6 Pointer to the server's link-local IPv6 address.
 ******************************************************************************/
static void handle_dc_client_connected(const in6_addr_t *link_local_ipv6)
{
  uint32_t elapsed_ticks;

  if (state != STATE_CONNECTING) {
    return;
  }

  state = STATE_CONNECTED;

  // Calculate connection time
  elapsed_ticks = sl_sleeptimer_get_tick_count() - connect_start_tick;
  connect_time_ms = sl_sleeptimer_tick_to_ms(elapsed_ticks);

  memcpy(&server_ip, link_local_ipv6, sizeof(in6_addr_t));

  open_udp_socket();
  start_udp_rx_task();

  sl_sleeptimer_restart_timer_ms(&idle_timer,
                                 dc_ciu_settings.idle_timeout_ms,
                                 idle_timer_callback,
                                 NULL, 0, 0);

  printf("Connected in %.1f s\n", (double)connect_time_ms / 1000.0);
  refresh_display("OK in %lu.%lus",
                  (unsigned long)(connect_time_ms / 1000),
                  (unsigned long)((connect_time_ms % 1000) / 100));
}

/***************************************************************************//**
 * Handle DC client state change event.
 *
 * Dispatches to the appropriate handler based on the new state.
 *
 * @param evt Pointer to the state changed event.
 ******************************************************************************/
static void handle_dc_client_state_changed(
  const sl_wisun_msg_direct_connect_client_state_changed_ind_t *evt)
{
  switch (evt->body.state) {
    case SL_WISUN_DC_CLIENT_STATE_CONNECTED:
      handle_dc_client_connected(&evt->body.link_local_ipv6);
      break;
    case SL_WISUN_DC_CLIENT_STATE_CONNECTION_FAILED:
      handle_dc_client_connection_failed();
      break;
    case SL_WISUN_DC_CLIENT_STATE_CONNECTION_LOST:
      handle_dc_client_connection_lost();
      break;
    case SL_WISUN_DC_CLIENT_STATE_SCAN_COMPLETE:
      handle_dc_client_scan_complete();
      break;
    case SL_WISUN_DC_CLIENT_STATE_STOPPED:
      handle_dc_client_stopped();
      break;
    default:
      break;
  }
}

/***************************************************************************//**
 * Handle DC ID received event.
 *
 * Called when a DC ID is received during scanning. If the ID matches
 * the target, initiates connection to the server.
 *
 * @param dc_id Pointer to the received DC ID.
 * @param mac_address Pointer to the server's MAC address.
 ******************************************************************************/
static void handle_dc_id_received(const sl_wisun_dc_id_t *dc_id,
                                  const sl_wisun_mac_address_t *mac_address)
{
  if (state != STATE_SCANNING) {
    return;
  }

  if (memcmp(dc_id->id, target_dc_id.id, SL_WISUN_DC_ID_LEN) == 0) {
    memcpy(&server_mac, mac_address, sizeof(sl_wisun_mac_address_t));
    start_connect();
  }
}

// -----------------------------------------------------------------------------
//                          Button Action Handlers
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * Handle BTN0 press.
 *
 * Actions depend on current state:
 * - IDLE: Stop idle timer, start DC client.
 * - Other states: Stop DC client, then enter EM4.
 ******************************************************************************/
static void handle_btn0(void)
{
  sl_status_t status;

  switch (state) {
    case STATE_IDLE:
      sl_sleeptimer_stop_timer(&idle_timer);

      // Record start time for connection timing
      connect_start_tick = sl_sleeptimer_get_tick_count();

      app_cli_get_phy_config(&phy_config);

      refresh_display("Starting...");

      status = sl_wisun_start_direct_connect_client(&phy_config);
      if (status == SL_STATUS_OK) {
        start_scan();
      } else {
        printf("Start failed: 0x%04x\n", (unsigned)status);
        refresh_display("Start err: 0x%04x", (unsigned)status);
        sl_sleeptimer_restart_timer_ms(&idle_timer,
                                       dc_ciu_settings.idle_timeout_ms,
                                       idle_timer_callback,
                                       NULL, 0, 0);
      }
      break;

    case STATE_STOPPING:
      // Already stopping, ignore
      break;

    default:
      initiate_stop(STOP_REASON_DELIBERATE);
      break;
  }
}

/***************************************************************************//**
 * Handle BTN1 press.
 *
 * Actions depend on current state:
 * - CONNECTED: Send UDP message to server and reset idle timer.
 * - Other states: Ignored.
 ******************************************************************************/
static void handle_btn1(void)
{
  switch (state) {
    case STATE_CONNECTED:
      send_message_to_server();
      sl_sleeptimer_restart_timer_ms(&idle_timer,
                                     dc_ciu_settings.idle_timeout_ms,
                                     idle_timer_callback,
                                     NULL, 0, 0);
      break;

    default:
      // Ignore in other states
      break;
  }
}

// -----------------------------------------------------------------------------
//                          Event Task
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * Event handler task.
 *
 * Waits for events (button presses, timer timeouts) from the message queue
 * and dispatches to the appropriate handler function.
 *
 * @param args Task arguments (unused).
 ******************************************************************************/
static void event_task(void *args)
{
  osStatus_t status;
  uint8_t msg;

  (void)args;

  while (1) {
    status = osMessageQueueGet(msg_queue, &msg, NULL, osWaitForever);
    if (status == osOK) {
      switch (msg) {
        case SL_DC_CIU_MSG_BTN_0:
          handle_btn0();
          break;

        case SL_DC_CIU_MSG_BTN_1:
          handle_btn1();
          break;

        case SL_DC_CIU_MSG_IDLE_TIMEOUT:
          if (state == STATE_CONNECTED) {
            // Stop client first, then EM4 will be entered in STOPPED handler
            initiate_stop(STOP_REASON_TIMEOUT);
          } else if (state == STATE_IDLE) {
            state = STATE_STOPPED;
            printf("Entering EM4 (idle timeout)\n");
            refresh_display("EM4: idle timeout");
            sl_power_manager_enter_em4();
          }
          break;

        default:
          break;
      }
    }
  }
}

// -----------------------------------------------------------------------------
//                          Public Functions
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * Application init - called after kernel starts
 ******************************************************************************/
void app_init(void)
{
  const osThreadAttr_t event_task_attr = {
    .name        = "DcCiuEventTask",
    .attr_bits   = osThreadDetached,
    .stack_size  = (SL_DC_CIU_BTN_TASK_STACK_SIZE * sizeof(void *)) & 0xFFFFFFF8U,
    .priority    = osPriorityNormal
  };

  const osMessageQueueAttr_t queue_attr = {
    .name      = "DcCiuQueue",
    .attr_bits = 0,
    .cb_mem    = NULL,
    .cb_size   = 0,
    .mq_mem    = NULL,
    .mq_size   = 0
  };

  osThreadId_t event_task_id;

  init_display();

  printf("\n");
  printf("========================================\n");
  printf("               DC CIU\n");
  printf("========================================\n");

  app_cli_init();

  app_cli_get_phy_config(&phy_config);

  state = STATE_IDLE;

  msg_queue = osMessageQueueNew(SL_DC_CIU_MSG_QUEUE_SIZE,
                                sizeof(uint8_t),
                                &queue_attr);
  if (msg_queue == NULL) {
    printf("ERROR: Queue creation failed!\n");
  }

  event_task_id = osThreadNew(event_task, NULL, &event_task_attr);
  if (event_task_id == NULL) {
    printf("ERROR: Event task creation failed!\n");
  }

  refresh_display("Press BTN0");

  // Start idle timer - device will sleep if user doesn't start within timeout
  sl_sleeptimer_start_timer_ms(&idle_timer,
                               dc_ciu_settings.idle_timeout_ms,
                               idle_timer_callback,
                               NULL, 0, 0);
  refresh_display("BTN0 or EM4");

  printf("Ready (EM4 in %lu s)\n",
         (unsigned long)(dc_ciu_settings.idle_timeout_ms / 1000));
}

/***************************************************************************//**
 * Direct Connect event handler.
 *
 * Dispatches Direct Connect events to the appropriate handler.
 *
 * @param evt Pointer to the Direct Connect event structure.
 ******************************************************************************/
void sl_wisun_on_event(sl_wisun_evt_t *evt)
{
  if (evt == NULL) {
    return;
  }

  switch (evt->header.id) {
    case SL_WISUN_MSG_DIRECT_CONNECT_CLIENT_STATE_CHANGED_IND_ID:
      handle_dc_client_state_changed(
        (const sl_wisun_msg_direct_connect_client_state_changed_ind_t *)evt);
      break;

    case SL_WISUN_MSG_DIRECT_CONNECT_ID_RECEIVED_IND_ID: {
      const sl_wisun_msg_direct_connect_id_received_ind_t *id_evt =
        (const sl_wisun_msg_direct_connect_id_received_ind_t *)evt;
      handle_dc_id_received(&id_evt->body.dc_id, &id_evt->body.mac_address);
      break;
    }

    default:
      break;
  }
}

/***************************************************************************//**
 * Button state change callback.
 *
 * Called from ISR context when a button state changes. Posts button ID
 * to the message queue for processing by the button task.
 *
 * @param handle Pointer to the button instance.
 ******************************************************************************/
void sl_button_on_change(const sl_button_t *handle)
{
  uint8_t msg;

  if (sl_button_get_state(handle) != SL_SIMPLE_BUTTON_PRESSED) {
    return;
  }

  if (msg_queue == NULL) {
    return;
  }

  if (handle == &sl_button_btn0) {
    msg = SL_DC_CIU_MSG_BTN_0;
    osMessageQueuePut(msg_queue, &msg, 0U, 0U);
  } else if (handle == &sl_button_btn1) {
    msg = SL_DC_CIU_MSG_BTN_1;
    osMessageQueuePut(msg_queue, &msg, 0U, 0U);
  }
}

// -----------------------------------------------------------------------------
//                          CLI Support Functions
// -----------------------------------------------------------------------------

/***************************************************************************//**
 * Get the current application state.
 *
 * Called by CLI module to retrieve state information.
 *
 * @returns Current state value.
 ******************************************************************************/
int app_get_current_state(void)
{
  return (int)state;
}

/***************************************************************************//**
 * Get state name string.
 *
 * @param state_val State value.
 * @returns State name string.
 ******************************************************************************/
const char *app_get_state_name(int state_val)
{
  switch ((dc_ciu_state_t)state_val) {
    case STATE_IDLE:       return "IDLE";
    case STATE_SCANNING:   return "SCANNING";
    case STATE_CONNECTING: return "CONNECTING";
    case STATE_CONNECTED:  return "CONNECTED";
    case STATE_STOPPING:   return "STOPPING";
    case STATE_STOPPED:    return "STOPPED";
    default:               return "UNKNOWN";
  }
}
