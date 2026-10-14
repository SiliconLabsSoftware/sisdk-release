/***************************************************************************/ /**
 @file sl_log.h
* @brief Silicon Labs Debug Logger API
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

#ifndef SL_LOG_H
#define SL_LOG_H

#ifdef __cplusplus
extern "C" {
#endif

#include "sl_log_common_config.h"
#include "sl_status.h"
#include "sl_compiler.h"
#include <stdarg.h>
#include <stdbool.h>
/** @addtogroup sl_log Silicon Labs Debug Logger
 * @brief Comprehensive logging system with multiple backends and efficient
 * event handling
 *
 * The Silicon Labs Debug Logger provides a flexible, efficient logging system
 * that supports multiple backends including proprietary interfaces and SEGGER
 * SystemView. It offers both printf-style and event-based logging with
 * compile-time and runtime filtering capabilities.
 *
 * Key features:
 * - Multiple log levels (INFO, DEBUG, WARN, ERROR, CRASH)
 * - Multiple backend support (Proprietary, SystemView)
 * - Efficient ring buffer implementation
 * - Multi-core timestamp synchronization
 * - Compile-time optimization for reduced overhead
 * - Power management integration
 *
 * @{
 */

/**
 * @defgroup sl_log_constants Constants and Limits
 * @brief Constants defining system limits and capabilities
 * @{
 */

/** @brief Maximum number of events that can be configured in the system */
#define SL_LOG_MAX_NO_OF_EVENTS 255

/** @brief Core ID of Host*/
#define SL_LOG_HOST_CORE_ID 0

/**
 * @defgroup sl_log_print_options Backend-Agnostic Print Options
 * @brief Message-type / option flags accepted by @ref SL_LOG_PRINT_TARGET_EX.
 *
 * These values are forwarded to the active backend:
 *   - SystemView backend: forwarded directly to SEGGER_SYSVIEW_VPrintfTargetEx()
 *     (numerically identical to SEGGER_SYSVIEW_LOG / WARNING / ERROR).
 *   - I/O Stream (proprietary) backend: used to pick the level prefix in the
 *     emitted text line.
 * @{
 */

/** @brief Informational / generic log message. */
#define SL_LOG_PRINT_OPT_LOG     (0u)
/** @brief Warning message. */
#define SL_LOG_PRINT_OPT_WARN    (1u)
/** @brief Error message. */
#define SL_LOG_PRINT_OPT_ERROR   (2u)
/** @brief Append to previous line instead of starting a new one
 *         (honoured by SystemView; ignored by other backends). */
#define SL_LOG_PRINT_OPT_APPEND  (1u << 6)

/** @} (end addtogroup sl_log_print_options) */

/** @} (end addtogroup sl_log_constants) */

/**
 * @defgroup sl_log_types Type Definitions
 * @brief Core type definitions for the logging system
 * @{
 */

/**
 * @brief Log level enumeration
 *
 * Defines the various log levels available in the system, from no logging
 * to crash-level events. Higher numeric values indicate more critical events.
 *
 * The log levels are hierarchical - enabling a higher level automatically
 * includes all lower-numbered (more critical) levels.
 */
typedef enum {
  /** @brief Debug level - detailed debugging information */
  SL_LOG_ENUM_CONFIG_DEBUG = SL_LOG_CONFIG_LEVEL_DEBUG,
  /** @brief Information level - general informational messages */
  SL_LOG_ENUM_CONFIG_INFO = SL_LOG_CONFIG_LEVEL_INFO,
  /** @brief Warning level - warning conditions that should be noted */
  SL_LOG_ENUM_CONFIG_WARN = SL_LOG_CONFIG_LEVEL_WARN,
  /** @brief Error level - error conditions that affect functionality */
  SL_LOG_ENUM_CONFIG_ERROR = SL_LOG_CONFIG_LEVEL_ERROR,
  /** @brief Crash level - critical system failures */
  SL_LOG_ENUM_CONFIG_CRASH = SL_LOG_CONFIG_LEVEL_CRASH,
  /** @brief No logging - all log messages are disabled */
  SL_LOG_ENUM_CONFIG_NONE = SL_LOG_CONFIG_LEVEL_NONE,  
  /** @brief Invalid level - used for validation purposes */
  SL_LOG_ENUM_CONFIG_INVALID,
} sl_log_level_t;

/**
 * @brief Maximum log arguments enumeration
 *
 * Defines the maximum number of arguments that can be passed to log functions.
 * This setting affects memory usage and performance - higher values provide
 * more flexibility but consume more resources.
 */
typedef enum {
  /** @brief No arguments supported - string-only logging */
  SL_LOG_ENUM_CONFIG_ARG0 = SL_LOG_CONFIG_ARG0,
  /** @brief Up to 1 argument supported */
  SL_LOG_ENUM_CONFIG_ARG1,
  /** @brief Up to 2 arguments supported */
  SL_LOG_ENUM_CONFIG_ARG2,
  /** @brief Up to 3 arguments supported */
  SL_LOG_ENUM_CONFIG_ARG3,
  /** @brief Up to 4 arguments supported */
  SL_LOG_ENUM_CONFIG_ARG4,
  /** @brief Up to 5 arguments supported */
  SL_LOG_ENUM_CONFIG_ARG5,
  /** @brief Up to 6 arguments supported */
  SL_LOG_ENUM_CONFIG_ARG6,
  /** @brief Up to 7 arguments supported */
  SL_LOG_ENUM_CONFIG_ARG7,
  /** @brief Up to 8 arguments supported */
  SL_LOG_ENUM_CONFIG_ARG8,
  /** @brief Up to 9 arguments supported */
  SL_LOG_ENUM_CONFIG_ARG9,
  /** @brief Up to 10 arguments supported */
  SL_LOG_ENUM_CONFIG_ARG10,
  /** @brief Invalid argument count - used for validation */
  SL_LOG_ENUM_CONFIG_ARG_INVALID,
} sl_log_args_t;

/**
 * @brief Log system configuration structure
 *
 * Contains all configuration parameters for the logging system. This structure
 * is used to configure the logger's behavior at runtime and defines the
 * system's capabilities and limits.
 */
typedef struct {
  /** @brief Maximum number of events that can be stored in the ring buffer */
  uint32_t no_of_events;
  /** @brief Current log level filter - only messages at this level or higher
   * are processed */
  sl_log_level_t log_level;
  /** @brief Maximum number of arguments supported in log messages */
  sl_log_args_t max_no_args;
} sl_log_config_t;

/**
 * @brief Structure representing a single log event
 *
 * This structure contains all information for a single log event, including
 * timing information, event identification, arguments, and metadata. Events
 * are stored in a ring buffer and transmitted to the selected backend.
 *
 * @note The total size of this structure affects memory usage and should be
 *       kept as compact as possible for embedded systems.
 */
typedef __PACKED_STRUCT {
  /** @brief Timestamp when the event was logged (in system timer units) */
  uint32_t timestamp;
  /** @brief Unique event identifier (pointer to format string or numeric ID) */
  uint32_t event_id;
  /** @brief Array of arguments associated with the event (up to
   * SL_LOG_CONFIG_ARG items) */
  uint32_t args[SL_LOG_CONFIG_ARG];
  /** @brief Number of valid arguments in the args array (0 to
   * SL_LOG_CONFIG_ARG) */
  uint8_t arg_count;
  /** @brief Core identifier that generated the event (0 = host core) */
  uint8_t core_id;
  /** @brief Event flags - bits 1-7: log level, bit 0: event type (0=format
   * string, 1=numeric) */
  uint8_t flags;
  /** @brief Version of the logging component that generated this event */
  uint8_t version;
} sl_log_event_t;

/**
 * @brief Ring buffer control structure
 *
 * Manages a circular buffer of log events. The ring buffer provides efficient
 * storage for log events with automatic wraparound when full. Newer events
 * overwrite older ones when the buffer capacity is exceeded.
 *
 * @note This structure is designed for single-producer, single-consumer access
 *       patterns typical in logging systems.
 */
typedef struct {
  /** @brief Index where the next event will be written (0 to no_of_events-1) */
  uint32_t write_index;
  /** @brief Index of the oldest unread event (0 to no_of_events-1) */
  uint32_t read_index;
  /** @brief Current number of events stored in buffer (0 to no_of_events) */
  uint32_t event_count;
  /** @brief Number of available event slots left in the buffer */
  int32_t available_event_slots;
  /** @brief Pointer to the actual ring buffer storage array */
  sl_log_event_t *buffer;
} sl_log_ring_buffer_t;

/** @} (end addtogroup sl_log_types) */

/**
 * @defgroup sl_log_api_common Common API Functions
 * @brief Common logging API functions available to all users
 *
 * These functions provide the main interface for initializing, configuring,
 * and using the logging system. They are designed to work across all
 * supported platforms and backends.
 *
 * @{
 */

/**
 * @brief Pre-initializes the log component.
 * Called before the backend and timestamp timer are ready.
 * Initializes the ring buffer configuration.
 */
void sl_log_init_stage1(void);

/**
 * @brief Starts the timestamp timer, initializes the backend
 * Appends timestamp to early logs and flushes them to the backend
 *
 * @return sl_status_t Status code indicating the result of the operation.
 *         - SL_STATUS_OK: Initialization successful.
 *         - SL_STATUS_NOT_INITIALIZED: Logger not properly initialized.
 *         - SL_STATUS_FAIL: Initialization failed.
 */
sl_status_t sl_log_init_stage2(void);

/**
 * @brief Set true when @ref sl_log_init_stage2() completes (backend ready).
 *
 * Used by logging helpers to defer output that has no early buffer (for example
 * @ref SL_LOG_PRINT_TARGET_EX / @c SL_PRINT_FMT_*). Do not write from
 * application code.
 */
extern bool sli_log_init_stage2_done;

/**
 * @brief Set the log level for the logger.
 *
 * @param[in] level Log level to be set.
 * @return sl_status_t Status code indicating the result of the operation.
 *         - SL_STATUS_OK: Log level set successfully.
 *         - SL_STATUS_INVALID_PARAMETER: Invalid log level parameter.
 */
sl_status_t sl_log_set_loglevel(sl_log_level_t level);

/**
 * @brief Get the current log level of the logger.
 *
 * @return sl_log_level_t Current log level.
 */
sl_log_level_t sl_log_get_loglevel(void);

/**
 * @brief Synchronize the timestamp between the host and captive core.
 *
 * @param[in] core_id Core identifier.
 * @param[in] args Pointer to additional arguments if needed.
 * @return sl_status_t Status code indicating the result of the operation.
 *         - SL_STATUS_OK: Synchronization successful.
 *         - SL_STATUS_FAIL: Synchronization failed.
 *         - SL_STATUS_INVALID_PARAMETER: Invalid parameters provided.
 *         - any other error codes as defined by the underlying implementation.
 */
sl_status_t sl_log_sync_timestamp(uint8_t core_id, void *args);

/**
 * @brief Send a log event with no arguments
 *
 * Logs an event containing only an event ID and level information.
 * This is the most efficient logging function as it requires minimal
 * memory and processing overhead.
 *
 * @param[in] event_id Event identifier (format string pointer or numeric ID)
 * @param[in] log_level Log level combined with event type flags
 *
 * @note This function is typically called by higher-level logging macros
 *       rather than directly by application code.
 */
void sl_log_send_no_args(uint32_t event_id, uint8_t log_level);

/**
 * @brief Send a log event with one argument
 *
 * Logs an event with a single 32-bit argument. Suitable for logging
 * simple values like integers, pointers, or status codes.
 *
 * @param[in] event_id Event identifier (format string pointer or numeric ID)
 * @param[in] log_level Log level combined with event type flags
 * @param[in] arg1 First argument for the log event
 *
 * @note Arguments are stored as 32-bit values. Larger data types should
 *       be cast or split across multiple arguments.
 */
void sl_log_send_arg1(uint32_t event_id, uint8_t log_level, uint32_t arg1);

/**
 * @brief Send a log event with two arguments
 *
 * Logs an event with two 32-bit arguments. Useful for logging pairs
 * of related values or more complex data structures.
 *
 * @param[in] event_id Event identifier (format string pointer or numeric ID)
 * @param[in] log_level Log level combined with event type flags
 * @param[in] arg1 First argument for the log event
 * @param[in] arg2 Second argument for the log event
 */
void sl_log_send_arg2(uint32_t event_id, uint8_t log_level, uint32_t arg1,
                      uint32_t arg2);

/**
 * @brief Send a log event with three arguments
 *
 * Logs an event with three 32-bit arguments. Use sl_log_send_arg4 through
 * sl_log_send_arg10 for more arguments (when SL_LOG_CONFIG_ARG is configured
 * accordingly).
 *
 * @param[in] event_id Event identifier (format string pointer or numeric ID)
 * @param[in] log_level Log level combined with event type flags
 * @param[in] arg1 First argument for the log event
 * @param[in] arg2 Second argument for the log event
 * @param[in] arg3 Third argument for the log event
 */
void sl_log_send_arg3(uint32_t event_id, uint8_t log_level, uint32_t arg1,
                      uint32_t arg2, uint32_t arg3);

#if (SL_LOG_CONFIG_ARG >= 4)
/**
 * @brief Send a log event with four arguments
 *
 * @param[in] event_id Event identifier (format string pointer or numeric ID)
 * @param[in] log_level Log level combined with event type flags
 * @param[in] arg1...arg4 Event arguments (in order).
 */
void sl_log_send_arg4(uint32_t event_id, uint8_t log_level, uint32_t arg1,
                      uint32_t arg2, uint32_t arg3, uint32_t arg4);
#endif

#if (SL_LOG_CONFIG_ARG >= 5)
/**
 * @brief Send a log event with four arguments
 *
 * @param[in] event_id Event identifier (format string pointer or numeric ID)
 * @param[in] log_level Log level combined with event type flags
 * @param[in] arg1...arg5 Event arguments (in order).
 */
void sl_log_send_arg5(uint32_t event_id, uint8_t log_level, uint32_t arg1,
                      uint32_t arg2, uint32_t arg3, uint32_t arg4,
                      uint32_t arg5);
#endif

#if (SL_LOG_CONFIG_ARG >= 6)
/**
 * @brief Send a log event with four arguments
 *
 * @param[in] event_id Event identifier (format string pointer or numeric ID)
 * @param[in] log_level Log level combined with event type flags
 * @param[in] arg1...arg6 Event arguments (in order).
 */
void sl_log_send_arg6(uint32_t event_id, uint8_t log_level, uint32_t arg1,
                      uint32_t arg2, uint32_t arg3, uint32_t arg4,
                      uint32_t arg5, uint32_t arg6);
#endif

#if (SL_LOG_CONFIG_ARG >= 7)
/**
 * @brief Send a log event with four arguments
 *
 * @param[in] event_id Event identifier (format string pointer or numeric ID)
 * @param[in] log_level Log level combined with event type flags
 * @param[in] arg1...arg7 Event arguments (in order).
 */
void sl_log_send_arg7(uint32_t event_id, uint8_t log_level, uint32_t arg1,
                      uint32_t arg2, uint32_t arg3, uint32_t arg4,
                      uint32_t arg5, uint32_t arg6, uint32_t arg7);
#endif

#if (SL_LOG_CONFIG_ARG >= 8)
/**
 * @brief Send a log event with four arguments
 *
 * @param[in] event_id Event identifier (format string pointer or numeric ID)
 * @param[in] log_level Log level combined with event type flags
 * @param[in] arg1...arg8 Event arguments (in order).
 */
void sl_log_send_arg8(uint32_t event_id, uint8_t log_level, uint32_t arg1,
                      uint32_t arg2, uint32_t arg3, uint32_t arg4,
                      uint32_t arg5, uint32_t arg6, uint32_t arg7,
                      uint32_t arg8);
#endif

#if (SL_LOG_CONFIG_ARG >= 9)
/**
 * @brief Send a log event with four arguments
 *
 * @param[in] event_id Event identifier (format string pointer or numeric ID)
 * @param[in] log_level Log level combined with event type flags
 * @param[in] arg1...arg9 Event arguments (in order).
 */
void sl_log_send_arg9(uint32_t event_id, uint8_t log_level, uint32_t arg1,
                      uint32_t arg2, uint32_t arg3, uint32_t arg4,
                      uint32_t arg5, uint32_t arg6, uint32_t arg7,
                      uint32_t arg8, uint32_t arg9);
#endif

#if (SL_LOG_CONFIG_ARG >= 10)
/**
 * @brief Send a log event with four arguments
 *
 * @param[in] event_id Event identifier (format string pointer or numeric ID)
 * @param[in] log_level Log level combined with event type flags
 * @param[in] arg1...arg10 Event arguments (in order).
 */
void sl_log_send_arg10(uint32_t event_id, uint8_t log_level, uint32_t arg1,
                       uint32_t arg2, uint32_t arg3, uint32_t arg4,
                       uint32_t arg5, uint32_t arg6, uint32_t arg7,
                       uint32_t arg8, uint32_t arg9, uint32_t arg10);
#endif

/**
 * @brief Print a formatted string directly to the active log backend.
 *
 * Backend implementation for the SL_PRINT_FMT_* macros. Formats @p fmt with
 * the supplied variadic arguments on target and forwards the result to the
 * currently selected log backend:
 *   - SystemView backend: emits a SystemView text packet via
 *     SEGGER_SYSVIEW_VPrintfTargetEx().
 *   - I/O Stream (proprietary) backend: writes a `[L|F] formatted-text\\r\\n`
 *     line to the recommended console iostream.
 *   - log_none / no backend: linked against a weak no-op (message discarded).
 *
 * Unlike the event-based SL_PRINT_STRING_* path, the text is fully formatted
 * on target before transmission - no host-side description / lookup file is
 * required, and the format string may be runtime-built. The trade-off is
 * higher CPU and bandwidth than the event-based path.
 *
 * @param[in] options Message-type flag (see @ref sl_log_print_options):
 *                    SL_LOG_PRINT_OPT_LOG / WARN / ERROR, optionally OR'ed
 *                    with SL_LOG_PRINT_OPT_APPEND.
 * @param[in] fmt     printf-style format string. NULL is treated as a no-op.
 * @param[in] ...     Variadic arguments matching @p fmt.
 *
 * @note Output may be suppressed until the backend has been initialised
 *       (sl_log_init_stage2()).
 *
 * @note Forwards to @ref sli_log_print_target_ex, which captures variadic
 *       arguments into a @c va_list and calls @ref sl_log_vprint_target_ex.
 *       Backend implementations override the @c va_list form.
 */
void sli_log_print_target_ex(uint32_t options, const char *fmt, ...);

#define SL_LOG_PRINT_TARGET_EX(options, fmt, ...)                              \
  sli_log_print_target_ex((options), (fmt), ##__VA_ARGS__)

/**
 * @brief @c va_list variant of @ref SL_LOG_PRINT_TARGET_EX.
 *
 * Backend implementations override this function; @ref sli_log_print_target_ex
 * forwards to it after @c va_start. Callers that already hold a @c va_list
 * (e.g. when implementing their own printf-style helpers) should call this
 * directly.
 *
 * @param[in] options Message-type flag (see @ref sl_log_print_options).
 * @param[in] fmt     printf-style format string. NULL is treated as a no-op.
 * @param[in] ap      Variadic argument list previously initialised by the
 *                    caller via @c va_start. The callee consumes @p ap;
 *                    use @c va_copy if the caller needs to reuse it.
 *
 * @note Output may be suppressed until the backend has been initialised
 *       (sl_log_init_stage2()).
 */
void sl_log_vprint_target_ex(uint32_t options, const char *fmt, va_list ap);

/**
 * @brief Flush the logger buffer
 *
 * Forces immediate transmission of all pending log events in the ring buffer
 * to the selected backend. This function blocks until all events are sent
 * or an error occurs.
 *
 * @return sl_status_t Status code indicating the result of the operation.
 *         - SL_STATUS_OK: All events flushed successfully
 *         - SL_STATUS_FAIL: Flush operation failed
 *         - SL_STATUS_INVALID_STATE: Logger not properly initialized
 *
 * @note This function is useful before entering sleep mode or at critical
 *       points where log data must be preserved.
 */
sl_status_t sl_log_flush(void);

/** @} (end addtogroup sl_log_api_common) */

/**
 * @defgroup sl_log_api_internal Internal API Functions
 * @brief Internal functions used by the logging system implementation
 *
 * These functions are primarily for internal use by the logging system
 * and platform-specific implementations. They provide access to low-level
 * functionality and system state information.
 *
 * @{
 */

/**
 * @brief Calculate timestamp delta between cores
 *
 * Computes the timestamp difference between captive cores and the host
 * timestamp reference. This is used for timestamp synchronization in
 * multi-core logging scenarios.
 *
 * @return int Timestamp delta value in system timer units
 *
 * @note This function is primarily used internally for multi-core
 *       timestamp alignment and synchronization.
 */
int sl_log_get_timestamp_delta(void);

/**
 * @brief Retrieve current logging configuration
 *
 * Returns a snapshot of the current logging system configuration,
 * including log level, backend interface, and buffer settings.
 *
 * @return sl_log_config_t Copy of current logging configuration
 *
 * @note This function returns a copy of the configuration structure,
 *       so modifications to the returned value do not affect the
 *       actual system configuration.
 */
sl_log_config_t sl_log_get_config(void);

/**
 * @brief Check if ring buffer is empty
 *
 * Efficiently determines whether the ring buffer contains any log events.
 * This inline function provides optimal performance for frequent buffer
 * status checks.
 *
 * @param[in] ring_buffer Pointer to the ring buffer control structure
 * @return uint8_t Non-zero if buffer is empty, zero if it contains events
 *
 * @note This function should only be called with a valid ring_buffer pointer.
 */
static inline uint8_t
sl_log_is_ring_buffer_empty(sl_log_ring_buffer_t *ring_buffer) {
  return (ring_buffer->event_count == 0);
}

/**
 * @brief Check if ring buffer is full
 *
 * Efficiently determines whether the ring buffer has reached its maximum
 * capacity. When full, new events will overwrite the oldest events.
 *
 * @param[in] ring_buffer Pointer to the ring buffer control structure
 * @return uint8_t Non-zero if buffer is full, zero if space is available
 *
 * @note This function should only be called with a valid ring_buffer pointer.
 */
static inline uint8_t
sl_log_is_ring_buffer_full(sl_log_ring_buffer_t *ring_buffer) {
  return ((ring_buffer->event_count == SL_LOG_NUMBER_OF_EVENTS));
}


/***************************************************************************//**
* @brief
*    Assert implementation function
* @param[in] string_value - Formatted error string containing file:line - condition
* @details
*    This function should:
*    1. Log the error string using SL_PRINT_ERR or similar logging API
*    2. Check if debugger is attached (CoreDebug->DHCSR)
*    3. If debugger attached: trigger breakpoint (__BKPT(1))
*    4. If no debugger: enter infinite loop for watchdog reset
*
******************************************************************************/
void sli_log_assert_implementation(const char* string_value);

/** @} (end addtogroup sl_log_api_internal) */

/**
 * @defgroup sl_log_api_platform Platform-Specific API Functions
 * @brief Platform-specific functions for logging system integration
 *
 * These functions provide platform-specific functionality for power management,
 * backend initialization, and hardware-specific operations. Implementations
 * are provided by the platform-specific code.
 *
 * @{
 */

/**
 * @brief Prepare logger for sleep mode
 *
 * Configures the logging system before entering sleep mode. This typically
 * involves flushing pending events, configuring wake-up sources, and
 * preparing hardware for low-power operation.
 *
 * @param[in] args void pointer for any platform-specific arguments
 * @return sl_status_t Status code indicating the result of the operation.
 *         - SL_STATUS_OK: Sleep preparation successful
 *         - SL_STATUS_FAIL: Sleep preparation failed
 *         - SL_STATUS_NULL_POINTER: Invalid config pointer
 *
 * @note This function should be called before entering any sleep mode
 *       to ensure log data integrity and proper system behavior.
 */
sl_status_t sl_log_pre_sleep_process(void * args);

/**
 * @brief Initialize logger after wake-up
 *
 * Reinitializes the logging system after waking from sleep mode. This
 * includes restoring hardware state, reinitializing timers, and resuming
 * normal logging operations.
 *
 * @param[in] args void pointer for any platform-specific arguments
 * @return sl_status_t Status code indicating the result of the operation.
 *         - SL_STATUS_OK: Wake-up initialization successful
 *         - SL_STATUS_FAIL: Wake-up initialization failed
 *         - SL_STATUS_NULL_POINTER: Invalid config pointer
 *
 * @note This function should be called immediately after waking from
 *       sleep mode to restore full logging functionality.
 */
sl_status_t sl_log_post_sleep_process(void * args);

/**
 * @brief Initialize the selected logging backend
 *
 * Initializes the specified backend interface for log output. This function
 * sets up the necessary hardware, communication channels, and data structures
 * required by the selected backend.
 *
 * @return sl_status_t Status code indicating the result of the operation.
 *         - SL_STATUS_OK: Backend initialized successfully
 *         - SL_STATUS_INVALID_PARAMETER: Invalid interface parameter
 *         - SL_STATUS_FAIL: Backend initialization failed
 *
 * @note This function must be called before using any backend-specific
 *       logging functionality. Different backends may have different
 *       initialization requirements and capabilities.
 */
sl_status_t sl_log_backend_init(void);

/**
 * @brief Write log events to backend interface
 *
 * Transmits log events from the ring buffer to the selected backend interface.
 * This function handles ring buffer wraparound and ensures reliable
 * transmission of all requested events to the backend.
 *
 * @param[in] buffer Pointer to the ring buffer containing log events
 * @param[in] read_index Starting index in the buffer for reading events
 * @param[in] event_count Number of events to transmit from the buffer
 * @return sl_status_t Status code indicating the result of the operation.
 *         - SL_STATUS_OK: All events written successfully
 *         - SL_STATUS_INVALID_PARAMETER: Invalid buffer pointer or indices
 *         - SL_STATUS_FAIL: Backend write operation failed
 *
 * @note This function may be called multiple times for large event counts
 *       to handle ring buffer wraparound conditions efficiently.
 */
sl_status_t sl_log_backend_write(sl_log_event_t *buffer, uint32_t read_index,
                                 uint32_t event_count);


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
sl_status_t sl_log_platform_core_init(void);
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
sl_status_t sl_log_platform_core_deinit(void);

/**
 * @brief Get current timestamp counter value
 *
 * Retrieves the current value from the timestamp counter for the specified
 * core. This function provides access to the raw timestamp value used for
 * logging operations.
 *
 * @param[in] core_id Core identifier (0 = host core, >0 = captive cores)
 * @return uint32_t Current timestamp counter value in system timer units
 *
 * @note The timestamp resolution and range depend on the underlying
 *       hardware timer configuration. Use
 * sl_log_get_timestamp_timer_frequency() to convert to actual time units.
 */
uint32_t sl_log_get_timestamp_count(uint8_t core_id);

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
uint32_t sl_log_get_timestamp_timer_frequency(uint8_t core_id);

/**
 * @brief Set core-specific logger configurations
 *
 * Configures logging parameters for either the host core or a specific
 * captive core. The function automatically delegates to the appropriate
 * API (host or captive core) based on the core ID.
 *
 * @param[in] args Pointer to core-specific configuration arguments
 * @param[in] core_id Core identifier (0 = host core, >0 = captive core)
 * @return sl_status_t Status code indicating the result of the operation.
 *         - SL_STATUS_OK: Configuration applied successfully
 *         - SL_STATUS_INVALID_PARAMETER: Invalid arguments or core ID
 *         - SL_STATUS_NULL_POINTER: NULL args pointer provided
 *
 * @note The format and content of the args parameter depends on the
 *       specific core type and its configuration requirements.
 */
sl_status_t sl_log_set_configurations(void *args, uint8_t core_id);

/**
 * @brief Get core-specific logger configurations
 *
 * Retrieves current logging configuration parameters for either the host
 * core or a specific captive core. The function automatically delegates
 * to the appropriate API based on the core ID.
 *
 * @param[out] args Pointer to buffer for storing configuration arguments
 * @param[in] core_id Core identifier (0 = host core, >0 = captive core)
 * @return sl_status_t Status code indicating the result of the operation.
 *         - SL_STATUS_OK: Configuration retrieved successfully
 *         - SL_STATUS_INVALID_PARAMETER: Invalid core ID provided
 *         - SL_STATUS_NULL_POINTER: NULL args pointer provided
 *
 * @note The caller must provide a sufficiently large buffer in args to
 *       hold the core-specific configuration data.
 */
sl_status_t sl_log_get_configurations(void *args, uint8_t core_id);

/**
 * @brief Retrieve the logging ring buffer configuration instance.
 *
 * Provides access to the global (singleton) ring buffer configuration used by
 * the logging subsystem. This structure typically contains buffer size,
 * write/read indices, pointer to ring buffer and any state needed to manage in-memory log storage.
 *
 * The returned pointer refers to an internally managed object; callers MUST NOT
 * free or modify ownership-related aspects of the structure. If mutation of
 * fields is allowed by design, ensure proper synchronization (see Thread Safety).
 *
 * @return Pointer to the logging ring buffer configuration. Returns nullptr if
 *         the configuration has not been initialized or an internal error occurred.
 *
 * @thread_safety
 * - If the logging system initializes the ring buffer during startup and only
 *   mutates it through its own synchronized APIs, read-only access through this
 *   pointer is typically safe.
 * - If callers intend to modify the structure directly, they must ensure
 *   external synchronization to avoid data races.
 *
 */
sl_log_ring_buffer_t *sl_log_get_ring_buffer_config(void);

/** @} (end addtogroup sl_log_api_platform) */

/** @} (end addtogroup sl_log) */

#ifdef __cplusplus
}
#endif

/* *INDENT-OFF* */
/* THE REST OF THE FILE IS DOCUMENTATION ONLY! */
/**************************************************************************//**
* @addtogroup sl_log Silicon Labs Debug Logger
* @{
* @details The Silicon Labs Debug Logger (sl_log) is the unified, platform-level
* logging service. Its main purpose is to give application, driver, and stack
* code a single, standardized logging API that replaces ad-hoc `printf` /
* `DEBUGOUT` paths with predictable Flash/RAM cost, runtime-tunable verbosity,
* and a clean zero-overhead build for shipping firmware. Log messages are
* generated using lightweight `SL_PRINT_*` macros, categorized by severity
* (DEBUG, INFO, WARN, ERROR, and CRASH for asserts), and routed to a single
* selectable backend: I/O Stream (UART/VCOM or SEGGER RTT) in either formatted
* or compact form, or SEGGER SystemView. Logging behavior - default log level,
* ring-buffer depth, maximum argument count, selected backend, and message
* formatting - is configured through the Simplicity Studio Project Configurator
* (Universal Configurator, UC).
*
* @note Only **one** backend may be installed at a time. Adding a second backend
*       component triggers a Simplicity Studio conflict dialog offering
*       **Replace** or **Keep**.
*
* @details
* ## Initialization
*
*   SL Log must be initialized before any `SL_PRINT_*` macro produces output.
*   When `sl_main` or `sl_system_init` is used, initialization is part of the
*   startup sequence and @ref sl_log_init_stage1() / @ref sl_log_init_stage2()
*   are invoked automatically - **do not call them from application code**.
*   Initialization is split into two stages so that code running before the
*   timestamp timer and backend are ready can still log:
*   - @ref sl_log_init_stage1() sets up the ring buffer and the initial runtime
*     level. Early `SL_PRINT_*` calls that use the ring path are buffered;
*     final timestamps are applied at stage2 (see Early logs below).
*   - @ref sl_log_init_stage2() starts the timestamp timer, initializes the
*     backend, back-fills timestamps on the early logs, and flushes them. It is
*     wired in as a Service-Init event (priority 9999).
*
* ## Selecting and configuring a backend
*
*   In Simplicity Studio (**Software Components** view), install **exactly one**
*   backend. SL Log components ship with `quality: evaluation`, so they appear
*   in the Software Components list when Evaluation quality is enabled.
*   The core (`log`), platform integration (`log_platform_specific`), and no-op
*   (`log_none`) components are hidden and are pulled in automatically by the
*   backend; never install them by hand. If the backend uses I/O Stream, also
*   add and configure the transport (UART/VCOM or RTT).
*
*   | Goal | Components to install |
*   |------|-----------------------|
*   | Formatted (console/RTT) | `log_backend_iostream` + `log_backend_iostream_formatted` |
*   | Compact binary (host decode tool)  | `log_backend_iostream` + `log_backend_iostream_compact` |
*   | Trace correlation with SystemView  | `log_backend_systemview` |
*   | No output (buildable, zero output) | `log_none` (or set `LOG_LEVEL = NONE`) |
*
*   - **I/O Stream - Formatted** (`log_backend_iostream_formatted`): produces
*     human-readable text lines, expanded on target for **host-core** logs.
*     Viewable directly in a serial terminal (UART/VCOM) or RTT viewer with no
*     host decoder. Host string logs are written directly to the transport
*     (they do not enqueue through the compact ring-buffer drain /
*     @ref sl_log_flush path). Captive-core logs are not formatted on target.
*     Best for bench debugging and log analysis.
*   - **I/O Stream - Compact** (`log_backend_iostream_compact`): streams the
*     packed @ref sl_log_event_t record as a binary wire format (one struct per
*     event) to minimize bandwidth and RAM. Requires a host-side decoder and the
*     application ELF `.log_fmt` section to resolve format strings. Best for
*     performance-sensitive or resource-constrained builds.
*   - **SEGGER SystemView** (`log_backend_systemview`): forwards events into
*     SEGGER SystemView for trace correlation alongside FreeRTOS task and
*     interrupt timelines. Requires the SystemView host application and the
*     application ELF `.log_fmt` section for string resolution.
*
* ## Event record layout (`sl_log_event_t`)
*
*   @ref sl_log_event_t is the packed ring-buffer element used by all backends.
*   It is not compact-only: formatted and SystemView paths also enqueue this
*   record in RAM. Only the compact backend reuses the same packed layout as its
*   on-wire binary stream (`sizeof(sl_log_event_t)` bytes per event).
*
*   | Field | Type | Role |
*   |-------|------|------|
*   | `timestamp` | `uint32_t` | Raw counter ticks (wraps at 2^32) |
*   | `event_id` | `uint32_t` | Format-string pointer or numeric event ID |
*   | `args[]` | `uint32_t[SL_LOG_CONFIG_ARG]` | Argument slots (UC `CONFIG_MAX_ARGS`) |
*   | `arg_count` | `uint8_t` | Number of valid entries in `args` |
*   | `core_id` | `uint8_t` | Producing core (`0` = host) |
*   | `flags` | `uint8_t` | Bit 0: type (0 = format string, 1 = numeric); bits 1-7: log level |
*   | `version` | `uint8_t` | Logger layout / component version |
*
*   Packed field order: `timestamp`, `event_id`, `args[]`, then the four
*   trailing `uint8_t` fields. Raising `CONFIG_MAX_ARGS` enlarges every
*   ring-buffer slot and every compact wire record by four bytes per added
*   argument.
*
* ## UC configuration options
*
*   All UC settings map one-to-one to C macros in the config headers under
*   `platform/service/sl_log/config/`.
*
*   **Common settings** (`sl_log_common_config.h`, always present):
*
*   | UC field | Macro | Allowed values | Default |
*   |----------|-------|----------------|---------|
*   | LOG_LEVEL | `SL_LOG_CONFIG_LEVEL_COMPILE_TIME` | NONE / DEBUG / INFO / WARN / ERROR | ERROR |
*   | CONFIG_MAX_ARGS | `SL_LOG_CONFIG_ARG` | ARG0..ARG10 (0..10) | 3 |
*   | No of Logs | `SL_LOG_NUMBER_OF_EVENTS` | 1..255 | 128 |
*   | Enable Debug Assertions | `SL_LOG_DEBUG_ASSERT_ENABLE` | 0 / 1 | 0 |
*
*   `LOG_LEVEL` is the compile-time ceiling: severities below it are stripped
*   from the binary and cannot be recovered without a rebuild. `NONE` removes
*   all log calls. `CONFIG_MAX_ARGS` sets the maximum arguments per call (each
*   extra argument adds 4 bytes per event); calls that exceed it fail to build
*   with a `_Static_assert`.
*
*   **Timer** (`sl_log_platform_core_config.h`):
*
*   | UC field | Macro | Allowed values | Default |
*   |----------|-------|----------------|---------|
*   | TIMER Instance Used for timestamp counter | `SL_LOG_CONFIG_TIMER_INSTANCE` | 0..6 | 0 |
*
*   Select a 32-bit timer instance for the logger timestamp counter. Make sure
*   the chosen TIMER instance is 32 bits (see the device datasheet).
*
*   **Compact output** (`sl_log_proprietary_config.h`, compact backend only):
*
*   | UC field | Macro | Allowed values | Default |
*   |----------|-------|----------------|---------|
*   | PROPRIETARY_CONFIG_MODE | `SL_LOG_CONFIG_MODE` | Buffer / Console / Host | Host |
*
*   **Host** mode buffers events and drains them with @ref sl_log_flush()
*   (recommended). **Console** writes each event directly with no flush
*   plumbing. **Buffer** captures events in RAM only and does not stream them
*   live.
*
*   **Formatted output** (`sl_log_formatted_iostream_config.h`, formatted
*   backend only):
*
*   | UC field | Macro | Allowed values | Default |
*   |----------|-------|----------------|---------|
*   | Formatted iostream: prefix timestamp | `SL_LOG_FORMATTED_IOSTREAM_PREFIX_TIMESTAMP` | 0 / 1 | 0 |
*   | Formatted iostream: emit core ID | `SL_LOG_FORMATTED_IOSTREAM_APPEND_CORE_ID` | 0 / 1 | 0 |
*
*   When enabled, the timestamp prefix emits `[TTTTTTTT]` (32-bit `timestamp` as
*   8 hex digits) before the formatted payload. The core-ID prefix emits `[CC]`
*   (2 hex digits).
*
*   Example (both options enabled): `[00005678] [00] App started`
*
* ## Host vs captive-core formatted output
*
*   On-target printf-style expansion (`SL_PRINT_STRING_*` with the formatted
*   I/O Stream backend) is supported for **host-core** logs only. Captive-core
*   (secondary core) logs do not support formatted strings on target; they are
*   emitted in encoded form and require a host-side decoder for interpretation.
*
* ## Using the SL_PRINT macros
*
*   Include `sl_log_helper.h` in your source files. Prefer the `SL_PRINT_STRING_*`
*   and `SL_PRINT_EVENT_*` families; they are the supported application API.
*
*   Printf-style string logging:
* @code{.c}
* SL_PRINT_STRING_DEBUG("Debug message");
* SL_PRINT_STRING_INFO("Sensor value: %u", (uint32_t)reading);
* SL_PRINT_STRING_WARN("Retry %u of %u", (uint32_t)attempt, (uint32_t)max_attempts);
* SL_PRINT_STRING_ERROR("Init failed: %d", (int)status);
* SL_PRINT_STRING_CRASH("Fatal path: %lu", (unsigned long)code);
* @endcode
*
*   Event-style numeric logging (best for hot paths and machine-parsed traces):
* @code{.c}
* SL_PRINT_EVENT_DEBUG(EVT_STATE_CHANGE, (uint32_t)old_state, (uint32_t)new_state);
* SL_PRINT_EVENT_INFO(MY_EVENT_ID, (uint32_t)arg1, (uint32_t)arg2);
* SL_PRINT_EVENT_WARN(EVT_RETRY, (uint32_t)attempt, (uint32_t)max_attempts);
* SL_PRINT_EVENT_ERROR(EVT_RADIO_TX_FAIL, (uint32_t)channel, (uint32_t)status);
* SL_PRINT_EVENT_CRASH(EVT_FATAL, (uint32_t)reason, (uint32_t)pc);
* @endcode
*
*   Guidance on which style to use:
*   - **Formatted backend** - use `SL_PRINT_STRING_*` with `%` format
*     specifiers. On this backend those macros expand on target (via the
*     `SL_PRINT_FMT_*` path). Prefer `SL_PRINT_STRING_*` in application code.
*   - **Compact backend** - use `SL_PRINT_STRING_*` or `SL_PRINT_EVENT_*`; cast
*     every numeric argument to `(uint32_t)` (`%lu` recommended).
*   - **SystemView** - either style; view in SystemView.
*
*   Argument storage is `uint32_t` through the log ABI. The formatted backend
*   accepts native C types for most integer/pointer/string specifiers; the
*   compact and event paths require explicit `(uint32_t)` / `(uintptr_t)` casts.
*   Avoid `%f` - it is not supported by the compact / event encoding.
*
* ### `SL_PRINT_FMT_*` (formatted backend path)
*
*   When the formatted I/O Stream backend is installed, `SL_PRINT_STRING_*`
*   maps to `SL_PRINT_FMT_*` (`INFO` / `DEBUG` / `WARN` / `ERROR` /
*   `CRASH`). In this configuration, the line is formatted on target and written
*   to the console stream; it does not enqueue a compact ring-buffer event. Prefer
*   `SL_PRINT_STRING_*` in application code; the `SL_PRINT_FMT_*` names are the
*   underlying formatted-backend implementation.
*
*   Requirements and limits:
*   - Active only with the formatted I/O Stream backend. Without it, direct
*     `SL_PRINT_FMT_*` calls are silent; `SL_PRINT_STRING_*` still uses the
*     compact / ring-buffer path when that backend is selected.
*   - Requires @ref sl_log_init_stage2() to have completed. Early prints before
*     stage 2 are discarded (not buffered) on this path.
*   - Host-core only for on-target expansion (see Host vs captive-core
*     formatted output).
*
* Preferred application API:
* @code{.c}
* SL_PRINT_STRING_DEBUG("Probe: value=%u", (unsigned)7);
* SL_PRINT_STRING_INFO("App started, build=%u", (unsigned)42);
* SL_PRINT_STRING_WARN("Retry %u of %u", (unsigned)1, (unsigned)3);
* SL_PRINT_STRING_ERROR("Init failed: status=%d", (int)-1);
* @endcode
*
* Same effect under the formatted backend (implementation path):
* @code{.c}
* SL_PRINT_FMT_DEBUG("Probe: value=%u", (unsigned)7);
* SL_PRINT_FMT_INFO("App started, build=%u", (unsigned)42);
* SL_PRINT_FMT_WARN("Retry %u of %u", (unsigned)1, (unsigned)3);
* SL_PRINT_FMT_ERROR("Init failed: status=%d", (int)-1);
* @endcode
*
*   Example host console line (optional UC timestamp / core-ID prefixes on):
* @code
* [00005678] [00] App started, build=42
* @endcode
*
* ## Log levels
*
*   Severity increases from DEBUG to CRASH. A message is emitted only if its
*   level is at or above **both** the compile-time ceiling and the current
*   runtime threshold. Setting the filter to level N passes N and all
*   higher-severity levels (for example, `INFO` passes INFO, WARN, ERROR, CRASH).
*
*   | Level | Producer macro | Use for |
*   |-------|----------------|---------|
*   | DEBUG | `SL_PRINT_STRING_DEBUG` / `SL_PRINT_EVENT_DEBUG` | Verbose dev trace (temp) |
*   | INFO | `SL_PRINT_STRING_INFO` / `SL_PRINT_EVENT_INFO` | Normal progress (temp) |
*   | WARN | `SL_PRINT_STRING_WARN` / `SL_PRINT_EVENT_WARN` | Recoverable anomalies |
*   | ERROR | `SL_PRINT_STRING_ERROR` / `SL_PRINT_EVENT_ERROR` | Needs attention (default) |
*   | CRASH | `SL_PRINT_STRING_CRASH` / `SL_PRINT_EVENT_CRASH`, asserts | Fatal / assert paths |
*
*   `ERROR` / `WARN` are the intended working levels for production and
*   day-to-day development; `INFO` / `DEBUG` are temporary and should not be
*   left enabled in shipping firmware. Set the compile-time `LOG_LEVEL` to
*   `NONE` to strip all logging from the build.
*
* ## Runtime log level
*
*   The `LOG_LEVEL` UC setting is the compile-time upper bound. Within that
*   ceiling, the runtime threshold can be changed at any time without a rebuild
*   using @ref sl_log_set_loglevel() and @ref sl_log_get_loglevel(). The initial
*   runtime level is seeded from the compile-time setting during
*   @ref sl_log_init_stage1(). Logs below the runtime threshold are suppressed
*   at runtime, but they remain in the binary and can be re-enabled later if they
*   are within the compile-time `LOG_LEVEL` limit.
*
*   The example below reads the current threshold, widens it to INFO while the
*   issue is reproduced and the trace is captured, then restores the previous
*   value on exit.
*
* @code{.c}
* sl_log_level_t prev = sl_log_get_loglevel();
*
* sl_log_set_loglevel(SL_LOG_ENUM_CONFIG_INFO);
*
* sl_log_set_loglevel(prev);
* @endcode
*
* ## Early logs and stage2 re-stamping
*
*   Before @ref sl_log_init_stage2(), `SL_PRINT_*` events that use the ring
*   buffer are queued without a final timestamp. At stage2 the logger assigns
*   ordered tick values (oldest to newest relative to the then-current count),
*   initializes the backend, and flushes those early events. Formatted
*   on-target prints that require the backend wait until stage2 completes.
*
* ## Ring-buffer overflow
*
*   When the ring buffer is full, newer events overwrite the oldest. The logger
*   also tracks drops and may emit a synthetic WARN overflow event so host tools
*   can see that records were lost. Size the UC **No of Logs**
*   (`SL_LOG_NUMBER_OF_EVENTS`) for your peak rate, and call @ref sl_log_flush()
*   often enough in compact Host mode.
*
* ## Draining the buffer with sl_log_flush()
*
*   In compact **Host** mode (default), events accumulate in the ring buffer and
*   must be drained by @ref sl_log_flush(). The call is blocking: it writes the
*   pending events through the backend transport and returns when that write
*   completes (`SL_STATUS_OK` = flushed, `SL_STATUS_EMPTY` = nothing to send,
*   `SL_STATUS_BUSY` = previous transfer still in progress).
*   @ref sl_log_flush() is not required for the formatted backend or compact
*   **Console** mode. With the formatted backend, host string output is rendered
*   on target and written straight to the console stream; it does not use the
*   compact ring-buffer enqueue / flush path.
*
* @note Call @ref sl_log_flush() from the super-loop (baremetal) or a dedicated
*       low-priority task (RTOS) - never from a high-priority ISR. Call it before
*       sleeping to ensure buffered logs reach the host.
*
* ## Usage Example
*
*   @ref sl_log_init_stage1() and @ref sl_log_init_stage2() are invoked
*   automatically by `sl_main` / `sl_system_init`; do not call them from
*   application code. Only the optional runtime level override below is needed,
*   and it stays within the compile-time ceiling.
*
* @code{.c}
* #include "sl_log_helper.h"
*
* void app_init(void)
* {
*   sl_log_set_loglevel(SL_LOG_ENUM_CONFIG_INFO);
*
*   SL_PRINT_STRING_INFO("App started");
*   SL_PRINT_STRING_WARN("Sensor sample = %d", (int)42);
*   SL_PRINT_STRING_ERROR("Boot OK");
* }
* @endcode
*
*   `SL_PRINT_STRING_ERROR()` is always emitted at the default level.
*
* ## Assert macros
*
*   | Macro | When active | Behavior |
*   |-------|-------------|----------|
*   | `SL_LOG_CRASH_ASSERT(cond)` | Always | See note below. |
*   | `SL_LOG_DEBUG_ASSERT(cond)` | UC debug asserts on | Development checks. |
*
*   `SL_LOG_CRASH_ASSERT` logs `"file:line - Assertion failed: <expr>"` on failure,
*   then `__BKPT(1)` if a debugger is attached, otherwise spins for watchdog reset.
*
* @code{.c}
* SL_LOG_CRASH_ASSERT(ptr != NULL);
* SL_LOG_DEBUG_ASSERT(count < MAX_COUNT);
* @endcode
*
* ## Power management integration
*
*   To keep timestamps monotonic across low-power transitions, call
*   @ref sl_log_pre_sleep_process() before entering sleep and
*   @ref sl_log_post_sleep_process() immediately after wake-up. When the
*   platform power_manager service is present, these hooks are wired
*   automatically. Otherwise, pair them symmetrically around every sleep
*   entry; timestamps become non-monotonic if they are not. While suspended
*   between the two calls, `SL_PRINT_*` calls are silently dropped because
*   the transport is gated. The RTT and SystemView backends keep the system
*   in the lowest operable state while a debugger is connected.
*
* ## Multi-core timestamp synchronization
*
*   On multi-core systems, @ref sl_log_sync_timestamp() aligns secondary-core
*   (captive) timestamps to the host-core reference so lines from all cores
*   correlate in a single stream. Call it periodically if precise correlation
*   is required. Formatted on-target string expansion remains host-core only;
*   captive-core traffic stays encoded for host decode.
*
*
* ## `.log_fmt` and viewing output
*
*   Compact and SystemView string logs store each format string in a dedicated
*   ELF section so host tools can map `event_id` (an address) back to text.
*   Placement is automatic: the `SL_PRINT_STRING_*` helpers put the literal in
*   that section (GCC/Clang: `.log_fmt`; IAR: `log_fmt`). Installing a compact
*   or SystemView backend automatically enables the corresponding linker input,
*   which retains this section in the final image. Applications do not need to
*   add these strings manually.
*
*   Always archive the application ELF with any release that produces those
*   streams; offline decoders need it (and the `timestamp` field on compact
*   records).
*
*   | Backend + transport | Host tool |
*   |---------------------|-----------|
*   | Formatted + RTT | SEGGER RTT Viewer / J-Link RTT terminal |
*   | Formatted + UART/VCOM | Serial terminal at the configured baud |
*   | Compact + RTT/UART | Host decoder + application ELF (`.log_fmt`); decode `timestamp` |
*   | SystemView | SEGGER SystemView; map messages using ELF `.log_fmt` |
*
* @} (end addtogroup sl_log)
******************************************************************************/

#endif // SL_LOG_H
