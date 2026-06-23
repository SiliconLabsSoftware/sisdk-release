/***************************************************************************/ /**
* @file sl_log.c
* @brief Implementation of the Silicon Labs Debug Logger
* @version 1.0.0
*******************************************************************************
* # License
* <b>Copyright 2025 Silicon Laboratories Inc. www.silabs.com</b>
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

#include "sl_log.h"
#include "sl_log_internal.h"
#include "sl_log_platform_specific.h"
#include "sl_log_common_config.h"
#include "sl_component_catalog.h"
#ifdef SL_CATALOG_LOG_BACKEND_PROPRIETARY_PRESENT
#ifndef SL_CATALOG_LOG_FORMATTED_OUTPUT_PRESENT
#include "sl_log_proprietary_config.h"
#endif
#endif
#if defined (__clang__)
#include "cmsis_clang.h"
#elif defined (__GNUC__)
#include "cmsis_gcc.h"
#elif defined(__ICCARM__)
#include "cmsis_iccarm.h"
#endif
#include <stddef.h>
#include <stdbool.h>
#include "sl_log_helper.h"
// ARM architecture specific includes for CoreDebug and __BKPT intrinsic
#if defined(__ARM_ARCH) || defined(__CORTEX_M)
#include "em_device.h"  // Provides CoreDebug and CoreDebug_DHCSR_C_DEBUGEN_Msk
#endif
/*******************************************************************************
 ***************************  DEFINE MACROS ********************************
 ******************************************************************************/
#define SL_LOG_FLAGS_POS 1  // Position of the log level in the event structure

#define SL_LOG_OVERFLOW_EVENT_ID 0xFFFFFFFF // Event ID for overflow events

#define SL_LOG_FLAGS_LEVEL_MASK 0x7

/* Ring buffer size for console mode and SystemView.
 * Used to buffer events logged prior to sl_log_init_stage2
 * Uses reduced size during early logging in console mode and SystemView.
 * HOST mode uses SL_LOG_NUMBER_OF_EVENTS */
#define EARLY_LOG_BUFFER_SIZE 20

#define EVENT_COUNT_DEFAULT 1

#define READ_INDEX_DEFAULT 0

#define MAYBE_UNUSED(x) ((void)(x))

/*******************************************************************************
 ***************************  GLOBAL VARIABLES   ********************************
 ******************************************************************************/

#ifdef SL_CATALOG_LOG_BACKEND_SYSTEMVIEW_PRESENT
/* External global timestamp variable (temporary workaround) */
extern uint32_t timestamp_global;
#endif

/* Global backend status variable to track the backend transfer status */
 sl_log_backend_status_t sl_log_backend_status;

/*
 * Global instance of the ring buffer that manages the circular storage
 * of log events. Initialized with zero indices and points to the static
 * storage array for actual event data.
 */
static sl_log_ring_buffer_t ring_buffer;

/*******************************************************************************
 ***************************  LOCAL VARIABLES   ********************************
 ******************************************************************************/

static sl_log_level_t current_log_level;

/* When true every sl_log_send_* call is silently dropped. Set by integration
 * code (e.g. the power-manager glue) on entry to a sleep mode that gates the
 * timestamp timer or the backend transport, and cleared once both are usable
 * again. The user-configured runtime level is preserved across the cycle. */
static volatile bool log_suspended = false;

void sli_log_set_suspended(bool suspended)
{
  log_suspended = suspended;
}

/* Returns true when an event with the given flags byte should be produced.
 * Combines the suspension gate (cheap volatile read, short-circuited first)
 * with the existing runtime severity filter. */
static inline bool log_should_send(uint8_t flags)
{
  return !log_suspended
         && (((flags >> SL_LOG_FLAGS_POS) & SL_LOG_FLAGS_LEVEL_MASK)
             >= current_log_level);
}

// Sets after sl_log_init_stage2 and used to determine the early logs
bool sli_log_init_stage2_done;

#if (defined(SL_LOG_CONFIG_MODE) \
  && (SL_LOG_CONFIG_MODE != SL_LOG_CONFIG_MODE_CONSOLE) \
  && !defined(SL_CATALOG_LOG_DEFAULT_RING_BUFFER_PRESENT) \
  )

/*
 * In HOST mode, Pre-allocated array that provides the actual storage space for log events
 * in the ring buffer.
 */
static sl_log_event_t buffer[SL_LOG_NUMBER_OF_EVENTS];

static sl_log_event_t overflow_event;

/*******************************************************************************
 ***************************   LOCAL FUNCTIONS   *******************************
 ******************************************************************************/

/**
 * @brief Update the overflow event
 * 
 * Updates the overflow event with the current timestamp, core ID, flags,
 * argument count, event ID, and version.
 * 
 * @param[in] overflow_count The number of overflow events
 */
static inline void update_over_flow_event(uint32_t overflow_count)
{
  sl_log_event_t overflow_event_local;

  overflow_event_local.timestamp = sl_log_get_api_core()->get_timestamp(SL_LOG_HOST_CORE_ID);
  overflow_event_local.core_id = 0;
  overflow_event_local.flags = (SL_LOG_CONFIG_LEVEL_WARN<<1)|1;
  overflow_event_local.arg_count = 1;
  overflow_event_local.event_id = SL_LOG_OVERFLOW_EVENT_ID;
  overflow_event_local.args[0] = overflow_count;
  overflow_event_local.version = 1;
  overflow_event=overflow_event_local;
}

/**
 * @brief atomic check of the backend transfer status
 * 
 * Checks the backend transfer status atomically by disabling interrupts
 * and checking the backend transfer status.
 * 
 * @return bool True if the backend transfer is done, false otherwise
 */
static inline bool log_is_backend_flush_done(void)
{
  bool is_done = false;
  __disable_irq();
  if (sl_log_backend_status.backend_transfer_done) {
    sl_log_backend_status.backend_transfer_done = 0;  // claim
    is_done = true;
  }
  __enable_irq();
  return is_done;
}
#else
/**
 * Ring buffer is only used for early logs in console mode and SystemView
 * a reduced buffer size is used to save memory.
 */
static sl_log_event_t buffer[EARLY_LOG_BUFFER_SIZE];
#endif
/**
 * @brief Write a log event to the ring buffer
 *
 * Internal function that handles the actual insertion of log events into
 * the circular ring buffer. Manages buffer wraparound, automatic flushing
 * when threshold is reached, and ensures thread safety through interrupt
 * disable/enable around critical sections.
 *
 * This function implements the producer side of the ring buffer, updating
 * write indices and event counts atomically to prevent corruption in
 * interrupt-driven logging scenarios.
 *
 * @param[in] buffer Pointer to the log event to be written
 * @param[in] buffer_size Size of the log event (for consistency, typically
 * ignored)
 * @return sl_status_t Status code indicating the result:
 *         - SL_STATUS_OK: Event successfully written to ring buffer
 *
 * @note This function disables interrupts briefly to ensure atomic updates
 *       of ring buffer control variables.
 * @note Automatic flushing occurs when buffer reaches SL_LOG_THRESHOLD
 * capacity.
 */
static inline sl_status_t log_write_to_ring_buffer(sl_log_event_t *event_buffer,
                                                      uint32_t event_size)
{
  (void)event_size;
#if defined(SL_LOG_CONFIG_MODE) && (SL_LOG_CONFIG_MODE != SL_LOG_CONFIG_MODE_CONSOLE)
    uint32_t buffer_capacity = SL_LOG_NUMBER_OF_EVENTS;
#else
    uint32_t buffer_capacity = EARLY_LOG_BUFFER_SIZE;
#endif
  sl_log_ring_buffer_t *ring_buffer_ptr = &ring_buffer;
  __disable_irq();
  ring_buffer_ptr->available_event_slots--;
  if (ring_buffer_ptr->available_event_slots<0 &&
      sl_log_backend_status.backend_transfer_done==0) {
      __enable_irq();
      return SL_STATUS_NOT_AVAILABLE;
  }
  uint32_t write_index = ring_buffer_ptr->write_index;
  ring_buffer_ptr->write_index =
      (write_index + 1u >= buffer_capacity) ? 0u : (write_index + 1u);
  __enable_irq();

  ring_buffer_ptr->buffer[write_index] = *event_buffer;

  __disable_irq();
  if (++ring_buffer_ptr->event_count > buffer_capacity) {
    ring_buffer_ptr->event_count = buffer_capacity;
    if (++ring_buffer_ptr->read_index == buffer_capacity) {
      ring_buffer_ptr->read_index = 0;
    }
  }
  __enable_irq();

  return SL_STATUS_OK;
}

/**
 * @brief Flush early events stored in the ring buffer to the respective backend.
 *
 * @param[in] read_index Start index in the ring buffer.
 * @param[in] event_count Number of events to flush.
 * @return void
 */
static void flush_early_logs_to_backend(uint32_t read_index, uint32_t event_count)
{
#if defined(SL_LOG_CONFIG_MODE) && (SL_LOG_CONFIG_MODE != SL_LOG_CONFIG_MODE_CONSOLE)
  uint32_t buffer_capacity = SL_LOG_NUMBER_OF_EVENTS;
#else
  uint32_t buffer_capacity = EARLY_LOG_BUFFER_SIZE;
#endif

  for (uint32_t i = 0; i < event_count; i++) {
    uint32_t idx = read_index + i;
    if (idx >= buffer_capacity) {
      idx -= buffer_capacity;
    }
    // SystemView: printf-style logs use PrintElf (ELF string address); numeric events use RecordU32xN.
#ifdef SL_CATALOG_LOG_BACKEND_SYSTEMVIEW_PRESENT
    {
      uint32_t opt = (uint32_t)(ring_buffer.buffer[idx].flags & 1u);
      if ((ring_buffer.buffer[idx].flags & 1u) == 0u) {
        /* event_id is format string address — must use PrintElf*, not RecordVoid (see SEGGER SYSVIEW_EVTID_EX_PRINT_ELF). */
        switch (ring_buffer.buffer[idx].arg_count) {
          case 0:
            SEGGER_SYSVIEW__PrintElf((unsigned int)ring_buffer.buffer[idx].event_id, opt);
            break;
          case 1:
            SEGGER_SYSVIEW__PrintElf_U32((unsigned int)ring_buffer.buffer[idx].event_id, opt,
                                           ring_buffer.buffer[idx].args[0]);
            break;
          case 2:
            SEGGER_SYSVIEW__PrintElf_U32x2((unsigned int)ring_buffer.buffer[idx].event_id, opt,
                                           ring_buffer.buffer[idx].args[0],
                                           ring_buffer.buffer[idx].args[1]);
            break;
          case 3:
            SEGGER_SYSVIEW__PrintElf_U32x3((unsigned int)ring_buffer.buffer[idx].event_id, opt,
                                           ring_buffer.buffer[idx].args[0],
                                           ring_buffer.buffer[idx].args[1],
                                           ring_buffer.buffer[idx].args[2]);
            break;
#if (SL_LOG_CONFIG_ARG >= 4)
          case 4:
            SEGGER_SYSVIEW__PrintElf_U32x4((unsigned int)ring_buffer.buffer[idx].event_id, opt,
                                           ring_buffer.buffer[idx].args[0],
                                           ring_buffer.buffer[idx].args[1],
                                           ring_buffer.buffer[idx].args[2],
                                           ring_buffer.buffer[idx].args[3]);
            break;
#endif
#if (SL_LOG_CONFIG_ARG >= 5)
          case 5:
            SEGGER_SYSVIEW__PrintElf_U32x5((unsigned int)ring_buffer.buffer[idx].event_id, opt,
                                           ring_buffer.buffer[idx].args[0],
                                           ring_buffer.buffer[idx].args[1],
                                           ring_buffer.buffer[idx].args[2],
                                           ring_buffer.buffer[idx].args[3],
                                           ring_buffer.buffer[idx].args[4]);
            break;
#endif
#if (SL_LOG_CONFIG_ARG >= 6)
          case 6:
            SEGGER_SYSVIEW__PrintElf_U32x6((unsigned int)ring_buffer.buffer[idx].event_id, opt,
                                           ring_buffer.buffer[idx].args[0],
                                           ring_buffer.buffer[idx].args[1],
                                           ring_buffer.buffer[idx].args[2],
                                           ring_buffer.buffer[idx].args[3],
                                           ring_buffer.buffer[idx].args[4],
                                           ring_buffer.buffer[idx].args[5]);
            break;
#endif
#if (SL_LOG_CONFIG_ARG >= 7)
          case 7:
            SEGGER_SYSVIEW__PrintElf_U32x7((unsigned int)ring_buffer.buffer[idx].event_id, opt,
                                           ring_buffer.buffer[idx].args[0],
                                           ring_buffer.buffer[idx].args[1],
                                           ring_buffer.buffer[idx].args[2],
                                           ring_buffer.buffer[idx].args[3],
                                           ring_buffer.buffer[idx].args[4],
                                           ring_buffer.buffer[idx].args[5],
                                           ring_buffer.buffer[idx].args[6]);
            break;
#endif
#if (SL_LOG_CONFIG_ARG >= 8)
          case 8:
            SEGGER_SYSVIEW__PrintElf_U32x8((unsigned int)ring_buffer.buffer[idx].event_id, opt,
                                           ring_buffer.buffer[idx].args[0],
                                           ring_buffer.buffer[idx].args[1],
                                           ring_buffer.buffer[idx].args[2],
                                           ring_buffer.buffer[idx].args[3],
                                           ring_buffer.buffer[idx].args[4],
                                           ring_buffer.buffer[idx].args[5],
                                           ring_buffer.buffer[idx].args[6],
                                           ring_buffer.buffer[idx].args[7]);
            break;
#endif
#if (SL_LOG_CONFIG_ARG >= 9)
          case 9:
            SEGGER_SYSVIEW__PrintElf_U32x9((unsigned int)ring_buffer.buffer[idx].event_id, opt,
                                           ring_buffer.buffer[idx].args[0],
                                           ring_buffer.buffer[idx].args[1],
                                           ring_buffer.buffer[idx].args[2],
                                           ring_buffer.buffer[idx].args[3],
                                           ring_buffer.buffer[idx].args[4],
                                           ring_buffer.buffer[idx].args[5],
                                           ring_buffer.buffer[idx].args[6],
                                           ring_buffer.buffer[idx].args[7],
                                           ring_buffer.buffer[idx].args[8]);
            break;
#endif
#if (SL_LOG_CONFIG_ARG >= 10)
          case 10:
            SEGGER_SYSVIEW__PrintElf_U32x10((unsigned int)ring_buffer.buffer[idx].event_id, opt,
                                            ring_buffer.buffer[idx].args[0],
                                            ring_buffer.buffer[idx].args[1],
                                            ring_buffer.buffer[idx].args[2],
                                            ring_buffer.buffer[idx].args[3],
                                            ring_buffer.buffer[idx].args[4],
                                            ring_buffer.buffer[idx].args[5],
                                            ring_buffer.buffer[idx].args[6],
                                            ring_buffer.buffer[idx].args[7],
                                            ring_buffer.buffer[idx].args[8],
                                            ring_buffer.buffer[idx].args[9]);
            break;
#endif
          default:
            break;
        }
      } else {
        switch (ring_buffer.buffer[idx].arg_count) {
          case 0:
            SEGGER_SYSVIEW_RecordVoid(ring_buffer.buffer[idx].event_id);
            break;
          case 1:
            SEGGER_SYSVIEW_RecordU32(ring_buffer.buffer[idx].event_id,
                                       ring_buffer.buffer[idx].args[0]);
            break;
          case 2:
            SEGGER_SYSVIEW_RecordU32x2(ring_buffer.buffer[idx].event_id,
                                       ring_buffer.buffer[idx].args[0],
                                       ring_buffer.buffer[idx].args[1]);
            break;
          case 3:
            SEGGER_SYSVIEW_RecordU32x3(ring_buffer.buffer[idx].event_id,
                                       ring_buffer.buffer[idx].args[0],
                                       ring_buffer.buffer[idx].args[1],
                                       ring_buffer.buffer[idx].args[2]);
            break;
#if (SL_LOG_CONFIG_ARG >= 4)
      case 4:
        SEGGER_SYSVIEW_RecordU32x4(ring_buffer.buffer[idx].event_id,
                                    ring_buffer.buffer[idx].args[0],
                                    ring_buffer.buffer[idx].args[1],
                                    ring_buffer.buffer[idx].args[2],
                                    ring_buffer.buffer[idx].args[3]);
        break;
#endif
#if (SL_LOG_CONFIG_ARG >= 5)
      case 5:
        SEGGER_SYSVIEW_RecordU32x5(ring_buffer.buffer[idx].event_id,
                                    ring_buffer.buffer[idx].args[0],
                                    ring_buffer.buffer[idx].args[1],
                                    ring_buffer.buffer[idx].args[2],
                                    ring_buffer.buffer[idx].args[3],
                                    ring_buffer.buffer[idx].args[4]);
        break;
#endif
#if (SL_LOG_CONFIG_ARG >= 6)
      case 6:
        SEGGER_SYSVIEW_RecordU32x6(ring_buffer.buffer[idx].event_id,
                                    ring_buffer.buffer[idx].args[0],
                                    ring_buffer.buffer[idx].args[1],
                                    ring_buffer.buffer[idx].args[2],
                                    ring_buffer.buffer[idx].args[3],
                                    ring_buffer.buffer[idx].args[4],
                                    ring_buffer.buffer[idx].args[5]);
        break;
#endif
#if (SL_LOG_CONFIG_ARG >= 7)
      case 7:
        SEGGER_SYSVIEW_RecordU32x7(ring_buffer.buffer[idx].event_id,
                                    ring_buffer.buffer[idx].args[0],
                                    ring_buffer.buffer[idx].args[1],
                                    ring_buffer.buffer[idx].args[2],
                                    ring_buffer.buffer[idx].args[3],
                                    ring_buffer.buffer[idx].args[4],
                                    ring_buffer.buffer[idx].args[5],
                                    ring_buffer.buffer[idx].args[6]);
        break;
#endif
#if (SL_LOG_CONFIG_ARG >= 8)
      case 8:
        SEGGER_SYSVIEW_RecordU32x8(ring_buffer.buffer[idx].event_id,
                                    ring_buffer.buffer[idx].args[0],
                                    ring_buffer.buffer[idx].args[1],
                                    ring_buffer.buffer[idx].args[2],
                                    ring_buffer.buffer[idx].args[3],
                                    ring_buffer.buffer[idx].args[4],
                                    ring_buffer.buffer[idx].args[5],
                                    ring_buffer.buffer[idx].args[6],
                                    ring_buffer.buffer[idx].args[7]);
        break;
#endif
#if (SL_LOG_CONFIG_ARG >= 9)
      case 9:
        SEGGER_SYSVIEW_RecordU32x9(ring_buffer.buffer[idx].event_id,
                                    ring_buffer.buffer[idx].args[0],
                                    ring_buffer.buffer[idx].args[1],
                                    ring_buffer.buffer[idx].args[2],
                                    ring_buffer.buffer[idx].args[3],
                                    ring_buffer.buffer[idx].args[4],
                                    ring_buffer.buffer[idx].args[5],
                                    ring_buffer.buffer[idx].args[6],
                                    ring_buffer.buffer[idx].args[7],
                                    ring_buffer.buffer[idx].args[8]);
        break;
#endif
#if (SL_LOG_CONFIG_ARG >= 10)
      case 10:
        SEGGER_SYSVIEW_RecordU32x10(ring_buffer.buffer[idx].event_id,
                                     ring_buffer.buffer[idx].args[0],
                                     ring_buffer.buffer[idx].args[1],
                                     ring_buffer.buffer[idx].args[2],
                                     ring_buffer.buffer[idx].args[3],
                                     ring_buffer.buffer[idx].args[4],
                                     ring_buffer.buffer[idx].args[5],
                                     ring_buffer.buffer[idx].args[6],
                                     ring_buffer.buffer[idx].args[7],
                                     ring_buffer.buffer[idx].args[8],
                                     ring_buffer.buffer[idx].args[9]);
        break;
#endif
          default:
            break;
        }
      }
    }
#else
    //Host or console mode: write each event to the backend.
    sl_log_backend_write(&ring_buffer.buffer[idx], 0, 1);
#endif
  }

  ring_buffer.read_index = 0;
  ring_buffer.write_index = 0;
  ring_buffer.event_count = 0;
  ring_buffer.available_event_slots = buffer_capacity;
}

/*
 *  Append timestamps to early events
 *  flush them to the respective backend.
 */
static void flush_early_logs(void)
{
#ifndef SL_CATALOG_LOG_BACKEND_SYSTEMVIEW_PRESENT
  /* Timestamps are only appended for host and console mode. SystemView does not use them.
   * Assign in sequential order (oldest = smallest timestamp, newest = largest) so older packets can be identified
   * current time and offsets preserve order including after overflow. */
  if (ring_buffer.event_count > 0) {

    // buffer_capacity used for ring-buffer wrap
#if defined(SL_LOG_CONFIG_MODE) && (SL_LOG_CONFIG_MODE != SL_LOG_CONFIG_MODE_CONSOLE)
    // Host mode uses full ring buffer capacity
    uint32_t buffer_capacity = SL_LOG_NUMBER_OF_EVENTS;
#else
    // Console mode uses reduced early buffer capacity
    uint32_t buffer_capacity = EARLY_LOG_BUFFER_SIZE;
#endif
    uint32_t current_timestamp = sl_log_get_api_core()->get_timestamp(SL_LOG_HOST_CORE_ID);
    for (uint32_t i = 0; i < ring_buffer.event_count; i++) {
      // Ring buffer is circular where ring_buffer.read_index+i may wrap and get array index.
      uint32_t event_slot_index = ring_buffer.read_index + i;
      if (event_slot_index >= buffer_capacity) {
        event_slot_index -= buffer_capacity;
      }
      ring_buffer.buffer[event_slot_index].timestamp = current_timestamp - (ring_buffer.event_count - 1 - i);
    }
  }
#endif

  flush_early_logs_to_backend(ring_buffer.read_index, ring_buffer.event_count);
}

/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/

/**
* Initializes the ring buffer, invoked during sl_main_init.
* Configures the buffer slot count for the corresponding backend, 
* enabling early log capture before full system initialization.
*/
void sl_log_init_stage1(void) {

  ring_buffer.buffer = buffer;
  sl_log_backend_status.backend_transfer_done = 1;
  // set event slots count by mode to save memory during early logging.
#if defined(SL_LOG_CONFIG_MODE) && ((SL_LOG_CONFIG_MODE != SL_LOG_CONFIG_MODE_CONSOLE))
  ring_buffer.available_event_slots = SL_LOG_NUMBER_OF_EVENTS;
#else
  // Console and SystemView modes do not use the ring buffer so use reduced size buffer.
  ring_buffer.available_event_slots = EARLY_LOG_BUFFER_SIZE;
#endif
  current_log_level = (sl_log_level_t)SL_LOG_CONFIG_LEVEL_COMPILE_TIME;
}

/**
 * @brief log_init stage 2: platform/backend init
 * flush early logs stored in the ring buffer to the respective backend.
 */
sl_status_t  sl_log_init_stage2(void) {

  if (sl_log_get_api_core() == NULL) {
    return SL_STATUS_NOT_INITIALIZED;
  }
  sl_log_platform_core_init();
  sl_log_backend_init();

  // Flush the early event logs stored in the ring buffer to the respective backend.
  flush_early_logs();
  sli_log_init_stage2_done = true;

  return SL_STATUS_OK;
}

/**
 * @brief Send a log event with no arguments
 *
 * Creates and logs an event containing only an event ID and metadata.
 * This is the most efficient logging function as it minimizes memory
 * usage and processing overhead.
 *
 * The function:
 * - Captures current timestamp from host API
 * - Sets core ID to 0 (host core)
 * - Packages event data into log structure
 * - Writes to ring buffer for transmission
 *
 * @param[in] event_id Unique event identifier (format string pointer or numeric
 * ID)
 * @param[in] flags Combined log level and event type flags:
 *                  - Bits 1-7: Log level (DEBUG, INFO, WARN, ERROR, etc.)
 *                  - Bit 0: Event type (0=format string, 1=numeric event)
 *
 * @note This function is typically called by higher-level logging macros
 *       rather than directly by application code.
 * @note Function does not return status - logging is fire-and-forget for
 * performance.
 */
void sl_log_send_no_args(uint32_t event_id, uint8_t flags)
{
  if(log_should_send(flags)){
    sl_log_event_t event;

    event.timestamp = sl_log_get_api_core()->get_timestamp(SL_LOG_HOST_CORE_ID);
    event.core_id = 0;
    event.flags = flags;
    event.arg_count = 0;
    event.event_id = event_id;
    event.args[0] = 0;
    event.args[1] = 0;
    event.args[2] = 0;
    event.version = 1;
    if (!sli_log_init_stage2_done) {
      // Early logging into the ring buffer before stage2 init is complete
      log_write_to_ring_buffer(&event, sizeof(event));
    } else {
#if ((defined(SL_LOG_CONFIG_MODE) && (SL_LOG_CONFIG_MODE==SL_LOG_CONFIG_MODE_CONSOLE)) \
  || defined(SL_CATALOG_LOG_DEFAULT_RING_BUFFER_PRESENT))
    sl_log_backend_write(&event,READ_INDEX_DEFAULT,EVENT_COUNT_DEFAULT);
#else
    log_write_to_ring_buffer(&event, sizeof(event));
#endif
    }
  }
}

/**
 * @brief Send a log event with one argument
 *
 * Creates and logs an event with a single 32-bit argument. Suitable for
 * logging simple values like integers, pointers, status codes, or other
 * data that fits in a 32-bit value.
 *
 * The function follows the same pattern as sl_log_send_no_args() but
 * additionally stores one argument value in the event structure.
 *
 * @param[in] event_id Unique event identifier (format string pointer or numeric
 * ID)
 * @param[in] flags Combined log level and event type flags
 * @param[in] arg1 First argument value to be logged
 *
 * @note Arguments are stored as 32-bit values. Larger data types should
 *       be cast appropriately or split across multiple arguments.
 */
void sl_log_send_arg1(uint32_t event_id, uint8_t flags, uint32_t arg1)
{
  if(log_should_send(flags)){
    sl_log_event_t event;

    event.timestamp = sl_log_get_api_core()->get_timestamp(SL_LOG_HOST_CORE_ID);
    event.core_id = 0;
    event.flags = flags;
    event.arg_count = 1;
    event.event_id = event_id;
    event.args[0] = arg1; 
    event.version = 1;

    if (!sli_log_init_stage2_done) {
      // Early logging into the ring buffer before stage2 init is complete
      log_write_to_ring_buffer(&event, sizeof(event));
    } else {
#if ((defined(SL_LOG_CONFIG_MODE) && (SL_LOG_CONFIG_MODE==SL_LOG_CONFIG_MODE_CONSOLE)) \
  || defined(SL_CATALOG_LOG_DEFAULT_RING_BUFFER_PRESENT))
    sl_log_backend_write(&event,READ_INDEX_DEFAULT,EVENT_COUNT_DEFAULT);
#else
    log_write_to_ring_buffer(&event, sizeof(event));
#endif
    }
  }
}

/**
 * @brief Send a log event with two arguments
 *
 * Creates and logs an event with two 32-bit arguments. Useful for logging
 * pairs of related values, coordinates, before/after states, or more
 * complex data structures that require two parameters.
 *
 * @param[in] event_id Unique event identifier (format string pointer or numeric
 * ID)
 * @param[in] flags Combined log level and event type flags
 * @param[in] arg1 First argument value to be logged
 * @param[in] arg2 Second argument value to be logged
 *
 * @note Both arguments are stored as 32-bit values in the args[] array.
 */
void sl_log_send_arg2(uint32_t event_id, uint8_t flags, uint32_t arg1,
                      uint32_t arg2)
{
  if(log_should_send(flags)){
    sl_log_event_t event;

    event.timestamp = sl_log_get_api_core()->get_timestamp(SL_LOG_HOST_CORE_ID);
    event.core_id = 0;
    event.flags = flags;
    event.arg_count = 2;
    event.event_id = event_id;
    event.args[0] = arg1;
    event.args[1] = arg2;
    event.version = 1;

    if (!sli_log_init_stage2_done) {
      // Early logging into the ring buffer before stage2 init is complete
      log_write_to_ring_buffer(&event, sizeof(event));
    } else {
#if ((defined(SL_LOG_CONFIG_MODE) && (SL_LOG_CONFIG_MODE==SL_LOG_CONFIG_MODE_CONSOLE)) \
  || defined(SL_CATALOG_LOG_DEFAULT_RING_BUFFER_PRESENT))
    sl_log_backend_write(&event,READ_INDEX_DEFAULT,EVENT_COUNT_DEFAULT);
#else
    log_write_to_ring_buffer(&event, sizeof(event));
#endif
    }
  }
}

/**
 * @brief Send a log event with three arguments
 *
 * Creates and logs an event with three 32-bit arguments. This provides
 * the maximum argument capacity supported by the system for optimal
 * memory efficiency while still allowing complex data logging.
 *
 * Suitable for logging RGB values, 3D coordinates, complex state
 * information, or any data requiring three related parameters.
 *
 * @param[in] event_id Unique event identifier (format string pointer or numeric
 * ID)
 * @param[in] flags Combined log level and event type flags
 * @param[in] arg1 First argument value to be logged
 * @param[in] arg2 Second argument value to be logged
 * @param[in] arg3 Third argument value to be logged
 *
 * @note For more than 3 arguments use sl_log_send_arg4 through sl_log_send_arg10
 *       when SL_LOG_CONFIG_ARG is configured accordingly.
 */
void sl_log_send_arg3(uint32_t event_id, uint8_t flags, uint32_t arg1,
                      uint32_t arg2, uint32_t arg3)
{
  if(log_should_send(flags)){
    sl_log_event_t event;

    event.timestamp = sl_log_get_api_core()->get_timestamp(SL_LOG_HOST_CORE_ID);
    event.core_id = 0;
    event.flags = flags;
    event.arg_count = 3;
    event.event_id = event_id;
    event.args[0] = arg1;
    event.args[1] = arg2;
    event.args[2] = arg3;
    event.version = 1;

    if (!sli_log_init_stage2_done) {
      // Early logging into the ring buffer before stage2 init is complete
      log_write_to_ring_buffer(&event, sizeof(event));
    } else {
#if ((defined(SL_LOG_CONFIG_MODE) && (SL_LOG_CONFIG_MODE==SL_LOG_CONFIG_MODE_CONSOLE)) \
  || defined(SL_CATALOG_LOG_DEFAULT_RING_BUFFER_PRESENT))
    sl_log_backend_write(&event,READ_INDEX_DEFAULT,EVENT_COUNT_DEFAULT);
#else
    log_write_to_ring_buffer(&event, sizeof(event));
#endif
    }
  }
}

#if (SL_LOG_CONFIG_ARG >= 4)
void sl_log_send_arg4(uint32_t event_id, uint8_t flags, uint32_t arg1,
                      uint32_t arg2, uint32_t arg3, uint32_t arg4)
{
  if(log_should_send(flags)){
    sl_log_event_t event;

    event.timestamp = sl_log_get_api_core()->get_timestamp(SL_LOG_HOST_CORE_ID);
    event.core_id = 0;
    event.flags = flags;
    event.arg_count = 4;
    event.event_id = event_id;
    event.args[0] = arg1;
    event.args[1] = arg2;
    event.args[2] = arg3;
    event.args[3] = arg4;    
    event.version = 1;

    if (!sli_log_init_stage2_done) {
      // Early logging into the ring buffer before stage2 init is complete
      log_write_to_ring_buffer(&event, sizeof(event));
    } else {
#if ((defined(SL_LOG_CONFIG_MODE) && (SL_LOG_CONFIG_MODE==SL_LOG_CONFIG_MODE_CONSOLE)) \
  || defined(SL_CATALOG_LOG_DEFAULT_RING_BUFFER_PRESENT))
    sl_log_backend_write(&event,READ_INDEX_DEFAULT,EVENT_COUNT_DEFAULT);
#else
    log_write_to_ring_buffer(&event, sizeof(event));
#endif
    }
  }
}
#endif

#if (SL_LOG_CONFIG_ARG >= 5)
void sl_log_send_arg5(uint32_t event_id, uint8_t flags, uint32_t arg1,
                      uint32_t arg2, uint32_t arg3, uint32_t arg4,
                      uint32_t arg5)
{
  if(log_should_send(flags)){
    sl_log_event_t event;

    event.timestamp = sl_log_get_api_core()->get_timestamp(SL_LOG_HOST_CORE_ID);
    event.core_id = 0;
    event.flags = flags;
    event.arg_count = 5;
    event.event_id = event_id;
    event.args[0] = arg1;
    event.args[1] = arg2;
    event.args[2] = arg3;
    event.args[3] = arg4;
    event.args[4] = arg5;    
    event.version = 1;

    if (!sli_log_init_stage2_done) {
      // Early logging into the ring buffer before stage2 init is complete
      log_write_to_ring_buffer(&event, sizeof(event));
    } else {
#if ((defined(SL_LOG_CONFIG_MODE) && (SL_LOG_CONFIG_MODE==SL_LOG_CONFIG_MODE_CONSOLE)) \
  || defined(SL_CATALOG_LOG_DEFAULT_RING_BUFFER_PRESENT))
    sl_log_backend_write(&event,READ_INDEX_DEFAULT,EVENT_COUNT_DEFAULT);
#else
    log_write_to_ring_buffer(&event, sizeof(event));
#endif
    }
  }
}
#endif

#if (SL_LOG_CONFIG_ARG >= 6)
void sl_log_send_arg6(uint32_t event_id, uint8_t flags, uint32_t arg1,
                      uint32_t arg2, uint32_t arg3, uint32_t arg4,
                      uint32_t arg5, uint32_t arg6)
{
  if(log_should_send(flags)){
    sl_log_event_t event;

    event.timestamp = sl_log_get_api_core()->get_timestamp(SL_LOG_HOST_CORE_ID);
    event.core_id = 0;
    event.flags = flags;
    event.arg_count = 6;
    event.event_id = event_id;
    event.args[0] = arg1;
    event.args[1] = arg2;
    event.args[2] = arg3;
    event.args[3] = arg4;
    event.args[4] = arg5;
    event.args[5] = arg6;   
    event.version = 1;

    if (!sli_log_init_stage2_done) {
      // Early logging into the ring buffer before stage2 init is complete
      log_write_to_ring_buffer(&event, sizeof(event));
    } else {
#if ((defined(SL_LOG_CONFIG_MODE) && (SL_LOG_CONFIG_MODE==SL_LOG_CONFIG_MODE_CONSOLE)) \
  || defined(SL_CATALOG_LOG_DEFAULT_RING_BUFFER_PRESENT))
    sl_log_backend_write(&event,READ_INDEX_DEFAULT,EVENT_COUNT_DEFAULT);
#else
    log_write_to_ring_buffer(&event, sizeof(event));
#endif
    }
  }
}
#endif

#if (SL_LOG_CONFIG_ARG >= 7)
void sl_log_send_arg7(uint32_t event_id, uint8_t flags, uint32_t arg1,
                      uint32_t arg2, uint32_t arg3, uint32_t arg4,
                      uint32_t arg5, uint32_t arg6, uint32_t arg7)
{
  if(log_should_send(flags)){
    sl_log_event_t event;

    event.timestamp = sl_log_get_api_core()->get_timestamp(SL_LOG_HOST_CORE_ID);
    event.core_id = 0;
    event.flags = flags;
    event.arg_count = 7;
    event.event_id = event_id;
    event.args[0] = arg1;
    event.args[1] = arg2;
    event.args[2] = arg3;
    event.args[3] = arg4;
    event.args[4] = arg5;
    event.args[5] = arg6;
    event.args[6] = arg7;    
    event.version = 1;

    if (!sli_log_init_stage2_done) {
      // Early logging into the ring buffer before stage2 init is complete
      log_write_to_ring_buffer(&event, sizeof(event));
    } else {
#if ((defined(SL_LOG_CONFIG_MODE) && (SL_LOG_CONFIG_MODE==SL_LOG_CONFIG_MODE_CONSOLE)) \
  || defined(SL_CATALOG_LOG_DEFAULT_RING_BUFFER_PRESENT))
    sl_log_backend_write(&event,READ_INDEX_DEFAULT,EVENT_COUNT_DEFAULT);
#else
    log_write_to_ring_buffer(&event, sizeof(event));
#endif
    }
  }
}
#endif

#if (SL_LOG_CONFIG_ARG >= 8)
void sl_log_send_arg8(uint32_t event_id, uint8_t flags, uint32_t arg1,
                      uint32_t arg2, uint32_t arg3, uint32_t arg4,
                      uint32_t arg5, uint32_t arg6, uint32_t arg7,
                      uint32_t arg8)
{
  if(log_should_send(flags)){
    sl_log_event_t event;

    event.timestamp = sl_log_get_api_core()->get_timestamp(SL_LOG_HOST_CORE_ID);
    event.core_id = 0;
    event.flags = flags;
    event.arg_count = 8;
    event.event_id = event_id;
    event.args[0] = arg1;
    event.args[1] = arg2;
    event.args[2] = arg3;
    event.args[3] = arg4;
    event.args[4] = arg5;
    event.args[5] = arg6;
    event.args[6] = arg7;
    event.args[7] = arg8;    
    event.version = 1;

    if (!sli_log_init_stage2_done) {
      // Early logging into the ring buffer before stage2 init is complete
      log_write_to_ring_buffer(&event, sizeof(event));
    } else {
#if ((defined(SL_LOG_CONFIG_MODE) && (SL_LOG_CONFIG_MODE==SL_LOG_CONFIG_MODE_CONSOLE)) \
  || defined(SL_CATALOG_LOG_DEFAULT_RING_BUFFER_PRESENT))
    sl_log_backend_write(&event,READ_INDEX_DEFAULT,EVENT_COUNT_DEFAULT);
#else
    log_write_to_ring_buffer(&event, sizeof(event));
#endif
    }
  }
}
#endif

#if (SL_LOG_CONFIG_ARG >= 9)
void sl_log_send_arg9(uint32_t event_id, uint8_t flags, uint32_t arg1,
                      uint32_t arg2, uint32_t arg3, uint32_t arg4,
                      uint32_t arg5, uint32_t arg6, uint32_t arg7,
                      uint32_t arg8, uint32_t arg9)
{
  if(log_should_send(flags)){
    sl_log_event_t event;

    event.timestamp = sl_log_get_api_core()->get_timestamp(SL_LOG_HOST_CORE_ID);
    event.core_id = 0;
    event.flags = flags;
    event.arg_count = 9;
    event.event_id = event_id;
    event.args[0] = arg1;
    event.args[1] = arg2;
    event.args[2] = arg3;
    event.args[3] = arg4;
    event.args[4] = arg5;
    event.args[5] = arg6;
    event.args[6] = arg7;
    event.args[7] = arg8;
    event.args[8] = arg9;    
    event.version = 1;

    if (!sli_log_init_stage2_done) {
      // Early logging into the ring buffer before stage2 init is complete
      log_write_to_ring_buffer(&event, sizeof(event));
    } else {
#if ((defined(SL_LOG_CONFIG_MODE) && (SL_LOG_CONFIG_MODE==SL_LOG_CONFIG_MODE_CONSOLE)) \
  || defined(SL_CATALOG_LOG_DEFAULT_RING_BUFFER_PRESENT))
    sl_log_backend_write(&event,READ_INDEX_DEFAULT,EVENT_COUNT_DEFAULT);
#else
    log_write_to_ring_buffer(&event, sizeof(event));
#endif
    }
  }
}
#endif

#if (SL_LOG_CONFIG_ARG >= 10)
void sl_log_send_arg10(uint32_t event_id, uint8_t flags, uint32_t arg1,
                       uint32_t arg2, uint32_t arg3, uint32_t arg4,
                       uint32_t arg5, uint32_t arg6, uint32_t arg7,
                       uint32_t arg8, uint32_t arg9, uint32_t arg10)
{
  if(log_should_send(flags)){
    sl_log_event_t event;

    event.timestamp = sl_log_get_api_core()->get_timestamp(SL_LOG_HOST_CORE_ID);
    event.core_id = 0;
    event.flags = flags;
    event.arg_count = 10;
    event.event_id = event_id;
    event.args[0] = arg1;
    event.args[1] = arg2;
    event.args[2] = arg3;
    event.args[3] = arg4;
    event.args[4] = arg5;
    event.args[5] = arg6;
    event.args[6] = arg7;
    event.args[7] = arg8;
    event.args[8] = arg9;
    event.args[9] = arg10;
    event.version = 1;

    if (!sli_log_init_stage2_done) {
      // Early logging into the ring buffer before stage2 init is complete
      log_write_to_ring_buffer(&event, sizeof(event));
    } else {
#if ((defined(SL_LOG_CONFIG_MODE) && (SL_LOG_CONFIG_MODE==SL_LOG_CONFIG_MODE_CONSOLE)) \
  || defined(SL_CATALOG_LOG_DEFAULT_RING_BUFFER_PRESENT))
    sl_log_backend_write(&event,READ_INDEX_DEFAULT,EVENT_COUNT_DEFAULT);
#else
    log_write_to_ring_buffer(&event, sizeof(event));
#endif
    }
  }
}
#endif

/**
 * @brief Flush all pending log events to the backend
 *
 * Forces immediate transmission of all events currently stored in the ring
 * buffer to the configured backend interface. This function handles:
 * - Empty buffer detection and early return
 * - Bulk transmission of all pending events
 * - Ring buffer index management and wraparound
 * - Consumer-side buffer state updates
 *
 * The function calculates the number of events to send and delegates
 * the actual transmission to sl_log_backend_write(), which handles
 * backend-specific formatting and transmission protocols.
 *
 * After successful transmission, the ring buffer read index is updated
 * to reflect that all events have been consumed, effectively emptying
 * the buffer for new events.
 *
 * @return sl_status_t Flush operation result:
 *         - SL_STATUS_OK: All events flushed successfully
 *         - SL_STATUS_EMPTY: No events to flush (buffer was empty)
 *
 * @note This function should be called from the lowest priority task to
 *       avoid blocking time-critical operations.
 * @note Automatic flushing occurs at SL_LOG_THRESHOLD, but this function
 *       can be called manually for immediate transmission.
 */
sl_status_t sl_log_flush(void)
{
#if defined(SL_LOG_CONFIG_MODE) && (SL_LOG_CONFIG_MODE==SL_LOG_CONFIG_MODE_HOST)
  if (log_is_backend_flush_done()) {
    uint32_t new_read_index = 0;

    __disable_irq();
    if (sl_log_is_ring_buffer_empty(&ring_buffer)) {
      sl_log_backend_status.backend_transfer_done = 1;
      __enable_irq();
      return SL_STATUS_EMPTY;
    }

    uint32_t read_index = ring_buffer.read_index;
    uint32_t event_count = ring_buffer.event_count;
    __enable_irq();

    sl_log_backend_write(ring_buffer.buffer, read_index,
                         event_count);
    new_read_index = event_count + read_index;
    if (new_read_index >= SL_LOG_NUMBER_OF_EVENTS) {
      new_read_index -= SL_LOG_NUMBER_OF_EVENTS;
    }

    __disable_irq();
    ring_buffer.read_index = new_read_index;
    ring_buffer.event_count -= event_count;

    int available_event_slots = ring_buffer.available_event_slots;
    if (ring_buffer.available_event_slots < 0) {
      ring_buffer.available_event_slots = 0;
    }
    ring_buffer.available_event_slots += event_count;
    __enable_irq();

    if (available_event_slots < 0) {
      update_over_flow_event(-available_event_slots);
      sl_log_backend_write(&overflow_event, READ_INDEX_DEFAULT, EVENT_COUNT_DEFAULT);
    }

    __disable_irq();
    sl_log_backend_status.backend_transfer_done = 1;
    __enable_irq();
  } else {
    return SL_STATUS_BUSY;
  }
#endif
  return SL_STATUS_OK;
}
/**
 * @brief Set the runtime log level filter
 *
 * Updates the current log level filter that determines which log messages
 * are processed at runtime. Only messages at the specified level or higher
 * priority will be logged. This provides runtime control over logging
 * verbosity without requiring recompilation.
 *
 * The log level hierarchy (from lowest to highest priority):
 * - SL_LOG_ENUM_CONFIG_DEBUG: Most verbose, includes all messages
 * - SL_LOG_ENUM_CONFIG_INFO: Informational messages and above
 * - SL_LOG_ENUM_CONFIG_WARN: Warning messages and above
 * - SL_LOG_ENUM_CONFIG_ERROR: Error messages and above
 * - SL_LOG_ENUM_CONFIG_CRASH: Only crash-level messages
 * - SL_LOG_ENUM_CONFIG_NONE: No logging
 *
 * @param[in] level The new log level to set (must be valid enum value)
 * @return sl_status_t Operation result:
 *         - SL_STATUS_OK: Log level updated successfully
 *         - SL_STATUS_INVALID_PARAMETER: Invalid log level provided
 *
 * @note Changes take effect immediately for new log messages.
 * @note This setting works in conjunction with compile-time level filtering.
 */
sl_status_t sl_log_set_loglevel(sl_log_level_t level)
{
  if (level >= SL_LOG_ENUM_CONFIG_INVALID) {
    return SL_STATUS_INVALID_PARAMETER; // Invalid log level parameter
  }

  current_log_level = level;
  return SL_STATUS_OK;
}
/**
 * @brief Get the current runtime log level
 *
 * Retrieves the currently active log level filter that determines
 * which messages are being processed. This can be used by applications
 * to check logging configuration or implement conditional logging logic.
 *
 * @return sl_log_level_t Current active log level filter
 *
 * @note The returned value reflects the runtime setting, which may differ
 *       from compile-time settings if modified via sl_log_set_loglevel().
 */
sl_log_level_t sl_log_get_loglevel(void)
{
  return current_log_level;
}

/**
 * @brief Get the current multi-core timestamp delta
 *
 * Returns the calculated timestamp offset used for synchronizing timestamps
 * between the host core and captive cores in multi-core systems. This delta
 * compensates for timing differences between different processor cores.
 *
 * @return int Current timestamp delta in system timer units
 *
 * @note This value is used internally for multi-core timestamp alignment.
 * @note A delta of 0 indicates no correction is being applied.
 */
int sl_log_get_timestamp_delta(void)
{
  return 0;
}

/**
 * @brief Initializes the core platform logging infrastructure.
 *
 * This function sets up any platform-specific resources required by
 * the logging system (e.g., timers). It is intended to be called once during system
 * startup before any other logging APIs are used.
 *
 *
 * @return SL_STATUS_OK on successful initialization.
 *       any other platform specific error codes on failure.
 *
 */
sl_status_t sl_log_platform_core_init(void)
{
  if (sl_log_get_api_core() == NULL) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  return sl_log_get_api_core()->platform_core_init();
}

/**
 * @brief Get current timestamp counter value for specified core
 *
 * Retrieves the current timestamp value from either the host core or
 * a captive core, depending on the core_id parameter. This function
 * handles multi-core timestamp coordination and includes a temporary
 * workaround for global timestamp integration.
 *
 * The function implements the following logic:
 * 1. Check for temporary global timestamp override (SystemView integration)
 * 2. Route to host API for core_id 0 (host core)
 * 3. Route to captive core API for core_id > 0
 *
 * @param[in] core_id Core identifier:
 *                    - 0: Host core timestamp
 *                    - >0: Captive core timestamp
 * @return uint32_t Current timestamp value in system timer units
 *         - Returns 0 if core_id is invalid or API call fails
 *
 * @note The global timestamp_global variable is a temporary workaround
 *       and will be removed when SystemView API integration is complete.
 * @note Timestamp resolution and range depend on platform-specific
 * implementation.
 */
uint32_t sl_log_get_timestamp_count(uint8_t core_id)
{
#ifdef SL_CATALOG_LOG_BACKEND_SYSTEMVIEW_PRESENT
  //@TODO remove global timestamp variable after getting api from systemview
  if (timestamp_global != 0) {
    volatile uint32_t timestamp_val = timestamp_global;
    timestamp_global = 0;
    return timestamp_val;
  }
#endif  
  if (sl_log_get_api_core() == NULL) {
    return 0;
  }

  return sl_log_get_api_core()->get_timestamp(core_id);
}
/**
 * @brief De-initializes the core platform logging infrastructure.
 *
 * This function deinitializes any platform-specific resources allocated by
 * sl_log_platform_core_init().
 *
 * @return SL_STATUS_OK on successful de-initialization.
 *       any other platform specific error codes on failure.
 *
 */
sl_status_t sl_log_platform_core_deinit(void)
{
  if (sl_log_get_api_core() == NULL) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  return sl_log_get_api_core()->platform_core_deinit();
}
/**
 * @brief Initialize the specified logging backend interface
 *
 * Performs backend-specific initialization based on the selected interface
 * type. Each backend may have different initialization requirements, hardware
 * setup needs, and configuration parameters.
 *
 * Supported backends:
 * - SL_LOG_BACKEND_PROPRIETARY: Platform-specific interface (typically
 * UART-based)
 * - SL_LOG_BACKEND_SYSTEMVIEW: SEGGER SystemView real-time analysis integration
 *
 * The function uses conditional compilation to include only the backends
 * that are configured at compile time, reducing code size and complexity.
 *
 * @param[in] interface The backend interface type to initialize
 * @return sl_status_t Initialization result:
 *         - SL_STATUS_OK: Backend initialized successfully
 *         - SL_STATUS_INVALID_PARAMETER: Unsupported interface type
 *         - Other codes: Backend-specific initialization errors
 *
 * @note This function is called automatically during sl_log_init_stage2().
 * @note Backend availability depends on compile-time configuration macros.
 * @note Some backends may require additional hardware or software setup.
 */
sl_status_t sl_log_backend_init(void)
{
  sl_log_api_backend_t * sl_log_backend_api=sl_log_get_api_backend();
  return sl_log_backend_api ? sl_log_backend_api->backend_init(): SL_STATUS_NOT_INITIALIZED;
}

/**
 * @brief Prepare logging system for sleep mode entry
 *
 * Performs necessary preparation steps before the system enters sleep mode
 * to ensure log data integrity and proper system behavior. This typically
 * includes flushing pending events, configuring wake-up sources, and
 * preparing hardware for low-power operation.
 *
 * The function delegates to the platform-specific host API implementation
 * which knows the appropriate steps for the target hardware and power
 * management requirements.
 *
 * Common preparation activities may include:
 * - Flushing all pending log events to prevent data loss
 * - Stopping or configuring timestamp counters for sleep mode
 * - Preparing backend interfaces for power-down
 * - Saving critical state information
 *
 * @param[in] args void pointer for any platform-specific arguments
 * @return sl_status_t Preparation result:
 *         - SL_STATUS_OK: Sleep preparation completed successfully
 *         - Other codes: Platform-specific preparation errors
 *
 * @note This function should be called before entering any sleep mode.
 * @note Must be paired with sl_log_post_sleep_process() after wake-up.
 */
sl_status_t sl_log_pre_sleep_process(void * args)
{
  if(sl_log_get_api_core() == NULL) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  return sl_log_get_api_core()->pre_sleep_process(args);
}
/**
 * @brief Reinitialize logging system after sleep mode wake-up
 *
 * Restores the logging system to full operational state after waking from
 * sleep mode. This includes reinitializing hardware, restoring configuration,
 * and resuming normal logging operations.
 *
 * The function delegates to the platform-specific host API implementation
 * which handles the hardware-specific restoration procedures required
 * after power management events.
 *
 * Common restoration activities may include:
 * - Restarting timestamp counters with proper synchronization
 * - Reinitializing backend interface hardware
 * - Restoring saved configuration state
 * - Verifying system clock and timing references
 *
 * @param[in] args void pointer for any platform-specific arguments
 * @return sl_status_t Restoration result:
 *         - SL_STATUS_OK: Wake-up restoration completed successfully
 *         - Other codes: Platform-specific restoration errors
 *
 * @note This function should be called immediately after waking from sleep.
 * @note Must be paired with sl_log_pre_sleep_process() before sleep entry.
 * @note Logging functionality may be impaired until this function completes.
 */
sl_status_t sl_log_post_sleep_process(void * args)
{
  if(sl_log_get_api_core() == NULL) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  return sl_log_get_api_core()->post_sleep_process(args);
}
/**
 * @brief Set the logger configurations for host or captive core.
 *
 * @param args Pointer to the platform specific configuration arguments.
 * @param core_id The core ID (0 for host, non-zero for captive core).
 * @return sl_status_t SL_STATUS_OK if successful, or an error code if
 * initialization fails.
 */
sl_status_t sl_log_set_configurations(void *args, uint8_t core_id)
{
  if(sl_log_get_api_core() == NULL) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  return sl_log_get_api_core()->set_configuration(args, core_id);
}

/**
 * @brief Get the logger configurations for host or captive core.
 *
 * @param args Pointer to the platform specific configuration arguments.
 * @param core_id The core ID (0 for host, non-zero for captive core).
 * @return sl_status_t SL_STATUS_OK if successful, or an error code if
 * initialization fails.
 */
sl_status_t sl_log_get_configurations(void *args, uint8_t core_id)
{
  if(sl_log_get_api_core() == NULL){
    return SL_STATUS_NOT_INITIALIZED;
  }

  return sl_log_get_api_core()->get_configuration(args, core_id);
}

/**
 * @brief Write log events to the configured backend interface
 *
 * Transmits log events from the ring buffer to the currently selected
 * backend interface. This function handles different backend types and
 * manages ring buffer wraparound conditions during transmission.
 *
 * Backend-specific handling:
 * - SL_LOG_BACKEND_PROPRIETARY: Bulk transmission via proprietary protocol
 * - SL_LOG_BACKEND_SYSTEMVIEW: Individual event transmission to SystemView
 *
 * For ring buffer wraparound (when events span the buffer boundary),
 * the proprietary backend handles this by splitting the transmission
 * into two parts: from read_index to buffer end, then from buffer
 * start to the remaining events.
 *
 * The SystemView backend processes events individually in sequence,
 * automatically handling index wraparound during iteration.
 *
 * @param[in] buffer Pointer to the ring buffer array containing events
 * @param[in] read_index Starting index for reading events from buffer
 * @param[in] event_count Number of events to transmit
 * @return sl_status_t Transmission result:
 *         - SL_STATUS_OK: Events transmitted successfully
 *         - SL_STATUS_INVALID_PARAMETER: Invalid backend interface
 *         - Other codes: Backend-specific transmission errors
 *
 * @note This function is called by sl_log_flush() to transmit pending events.
 * @note Ring buffer event_count is reset to 0 for proprietary backend after
 * transmission.
 * @note SystemView backend processes events individually for real-time
 * analysis.
 */
sl_status_t sl_log_backend_write(sl_log_event_t *buffer, uint32_t read_index,
                                 uint32_t event_count)
{
  sl_log_api_backend_t * sl_log_backend_api=sl_log_get_api_backend();

  if (buffer == NULL || sl_log_backend_api == NULL) {
    return SL_STATUS_NULL_POINTER; // Invalid parameters
  }
  if(read_index >= SL_LOG_NUMBER_OF_EVENTS || event_count > SL_LOG_NUMBER_OF_EVENTS) {
    return SL_STATUS_INVALID_PARAMETER;
  }

  return sl_log_backend_api->backend_write(buffer,read_index,event_count);
}

/**
 * @brief Get timestamp timer frequency
 *
 * Returns the frequency in Hz of the timestamp timer used for the specified
 * core. This frequency value can be used to convert raw timestamp values
 * to actual time units (seconds, milliseconds, etc.).
 *
 * @param[in] core_id Core identifier (0 = host core, >0 = captive cores)
 * @return uint32_t Frequency of the timestamp timer in Hz
 *
 * @note The returned frequency depends on the underlying timer/counter
 *       hardware configuration and may vary between different cores
 *       in a multi-core system.
 */
 
uint32_t sl_log_get_timestamp_timer_frequency(uint8_t core_id)
{
  if(sl_log_get_api_core() == NULL) {
    return 0;
  }

  return sl_log_get_api_core()->get_timestamp_timer_frequency(core_id);
}

/**
 * @brief Synchronize timestamps between host and captive cores
 *
 * Performs timestamp synchronization between the host core and specified
 * captive core to ensure coherent timing across multi-core log events.
 * This is essential for accurate event correlation and timing analysis
 * in multi-core systems.
 *
 * The function delegates to the platform-specific timer synchronization
 * implementation through the logging API, which handles the low-level
 * details of inter-core timing coordination.
 *
 * Synchronization may involve:
 * - Measuring and compensating for clock drift between cores
 * - Establishing common time reference points
 * - Calibrating timing offsets for different processor speeds
 * - Updating timestamp delta values for correction
 *
 * @param[in] core_id Target core identifier for synchronization
 * @param[in] args Platform-specific synchronization parameters
 * @return sl_status_t Synchronization result:
 *         - SL_STATUS_OK: Timestamp synchronization successful
 *         - SL_STATUS_FAIL: Synchronization operation failed
 *         - SL_STATUS_INVALID_PARAMETER: Invalid core ID or parameters
 *         - Other codes: Platform-specific synchronization errors
 *
 * @note This function is critical for accurate multi-core event correlation.
 * @note Should be called periodically to maintain synchronization accuracy.
 * @note Platform-specific implementation determines synchronization method.
 */
sl_status_t sl_log_sync_timestamp(uint8_t core_id, void *args)
{
  if(sl_log_get_api_core() == NULL) {
    return SL_STATUS_NOT_INITIALIZED;
  }

  return sl_log_get_api_core()->time_sync(args,core_id);
}

sl_log_ring_buffer_t *sl_log_get_ring_buffer_config(void)
{
#if (defined(SL_LOG_CONFIG_MODE) \
  && (SL_LOG_CONFIG_MODE != SL_LOG_CONFIG_MODE_CONSOLE) \
  && !defined(SL_CATALOG_LOG_DEFAULT_RING_BUFFER_PRESENT) \
  )
  return &ring_buffer;
#else
  return NULL;
#endif
}

/***************************************************************************//**
 * @brief Variadic capture for @ref SL_LOG_PRINT_TARGET_EX.
 *
 * Ellipsis is required here; @c va_start is only valid inside a variadic
 * function (not a macro).
 ******************************************************************************/
void sli_log_print_target_ex(uint32_t options, const char *fmt, ...) /* NOSONAR */
{
  va_list ap;

  if (!fmt) {
    return;
  }
  va_start(ap, fmt);
  sl_log_vprint_target_ex(options, fmt, ap);
  va_end(ap);
}

/***************************************************************************//**
 * @brief Assert handler implementation - triggers breakpoint in debug mode
 * if debugger is attached
 * @param[in] string_value Formatted error string with file:line - condition
 ******************************************************************************/
 void sli_log_assert_implementation(const char* string_value)
{
  MAYBE_UNUSED(string_value);
#ifdef SL_CATALOG_LOG_FORMATTED_OUTPUT_PRESENT
  if (ring_buffer.buffer != NULL) {
    SL_PRINT_STRING_ERROR("ASSERT: %s", (uintptr_t)string_value);
  }
#elif defined(SL_CATALOG_LOG_BACKEND_SYSTEMVIEW_PRESENT)
  // Assert message appears in SystemView.
  SL_PRINT_FMT_ERROR("ASSERT: %s", string_value);
#endif

#if (defined(SL_LOG_CONFIG_MODE) \
  && (SL_LOG_CONFIG_MODE != SL_LOG_CONFIG_MODE_CONSOLE) \
  && !defined(SL_CATALOG_LOG_DEFAULT_RING_BUFFER_PRESENT) \
  )
  // Non-console + ring-buffer path: flush so the assert message leaves the ring buffer
  sl_log_flush();
#endif

#if defined(__ARM_ARCH) || defined(__CORTEX_M)
   // Check if there's an active debug session by reading DHCSR register
   // CoreDebug_DHCSR_C_DEBUGEN_Msk indicates debugger is connected
   if ((CoreDebug->DHCSR & CoreDebug_DHCSR_C_DEBUGEN_Msk) != 0x0)
   {
     // Debugger is attached - trigger a software breakpoint
     // This allows the developer to inspect the call stack and variables
     __BKPT(1);
   }
   else
 #endif
   {
     // No debugger attached - enter infinite loop for watchdog reset
     while (true) {
     }
   }
 }


