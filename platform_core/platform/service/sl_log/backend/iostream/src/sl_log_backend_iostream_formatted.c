/***************************************************************************//**
 * @file
 * @brief Target-side printf implementation for the formatted I/O Stream log
 *        backend.
 *
 * Provides the formatted-output backend implementation of
 * sl_log_vprint_target_ex(), the va_list primitive that the single variadic
 * wrapper SL_LOG_PRINT_TARGET_EX forwards to. SL_PRINT_FMT_* macros declared
 * in sl_log_helper.h reach this code path. When the formatted-output backend
 * is installed, SL_PRINT_STRING_* are also redirected to SL_PRINT_FMT_*, so
 * every string log goes through this file. Numeric event records
 * (SL_PRINT_EVENT_*) are not supported in this output mode.
 *
 * The text is formatted on target with vsnprintf() and emitted to the
 * recommended console iostream as a single line. The line layout follows the
 * formatted backend convention; the legacy S/E line-type indicator is no
 * longer emitted because event encoding is not supported here.
 *
 * **Optional leading prefix** (see @ref sl_log_formatted_iostream_config.h):
 * - @c SL_LOG_FORMATTED_IOSTREAM_PREFIX_TIMESTAMP: `[TIMESTAMP]` (8 hex
 *   digits) and a space.
 *
 * **Optional core ID** (when @c SL_LOG_FORMATTED_IOSTREAM_APPEND_CORE_ID is
 * set): `[CC]` (2 hex digits) and a space, before the formatted payload.
 *
 * Example (all options): [00005678] [00] count=-1 addr=0x00001000
 *
 * The trailing CR/LF is not appended automatically: callers must include any
 * desired line terminator in the format string (matching the string-log
 * behavior of the previous formatted backend).
 *
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

#include <stdarg.h>
#include <stdint.h>
#include <stdio.h>
#include <stddef.h>

#include "sl_log.h"
#include "sl_log_platform_specific.h"
#include "sl_log_helper.h"
#include "sl_log_formatted_iostream_config.h"
#include "sl_iostream.h"
#include "sl_iostream_handles.h"

#ifndef SL_LOG_FORMATTED_IOSTREAM_PREFIX_TIMESTAMP
#define SL_LOG_FORMATTED_IOSTREAM_PREFIX_TIMESTAMP  0
#endif
#ifndef SL_LOG_FORMATTED_IOSTREAM_APPEND_CORE_ID
#define SL_LOG_FORMATTED_IOSTREAM_APPEND_CORE_ID    0
#endif

/** Maximum size (bytes) of one printf line emitted to iostream, including the
 *  optional leading prefix(es). Lines longer than this are truncated. */
#ifndef SL_LOG_PRINT_LINE_MAX
#define SL_LOG_PRINT_LINE_MAX 200
#endif

#define SL_LOG_FORMATTED_IOSTREAM_HEX8_LEN  8U
#define SL_LOG_FORMATTED_IOSTREAM_HEX2_LEN  2U

/* Worst-case prefix lengths written unchecked into line[] before the bounds
 * test in sl_log_vprint_target_ex(). Keep these in sync with the prefix
 * blocks below: '[' + 8 hex + ']' + ' ' = 11 for the timestamp; '[' + 2 hex
 * + ']' + ' ' = 5 for the core ID. */
#define SL_LOG_FORMATTED_IOSTREAM_TIMESTAMP_PREFIX_LEN \
  (1U + SL_LOG_FORMATTED_IOSTREAM_HEX8_LEN + 1U + 1U)
#define SL_LOG_FORMATTED_IOSTREAM_CORE_ID_PREFIX_LEN   \
  (1U + SL_LOG_FORMATTED_IOSTREAM_HEX2_LEN + 1U + 1U)

#if SL_LOG_FORMATTED_IOSTREAM_PREFIX_TIMESTAMP
#define SL_LOG_FORMATTED_IOSTREAM_TS_LEN_ACTIVE   SL_LOG_FORMATTED_IOSTREAM_TIMESTAMP_PREFIX_LEN
#else
#define SL_LOG_FORMATTED_IOSTREAM_TS_LEN_ACTIVE   0U
#endif

#if SL_LOG_FORMATTED_IOSTREAM_APPEND_CORE_ID
#define SL_LOG_FORMATTED_IOSTREAM_CID_LEN_ACTIVE  SL_LOG_FORMATTED_IOSTREAM_CORE_ID_PREFIX_LEN
#else
#define SL_LOG_FORMATTED_IOSTREAM_CID_LEN_ACTIVE  0U
#endif

#define SL_LOG_FORMATTED_IOSTREAM_PREFIX_MAX_LEN \
  (SL_LOG_FORMATTED_IOSTREAM_TS_LEN_ACTIVE + SL_LOG_FORMATTED_IOSTREAM_CID_LEN_ACTIVE)

/* Refuse to build if the line buffer is too small to even hold the enabled
 * prefix plus at least one payload byte. Without this the prefix writes in
 * sl_log_vprint_target_ex() would overflow the stack-allocated line[]
 * before the post-write bounds check is reached. */
_Static_assert(SL_LOG_PRINT_LINE_MAX > SL_LOG_FORMATTED_IOSTREAM_PREFIX_MAX_LEN,
               "SL_LOG_PRINT_LINE_MAX is too small for the enabled prefix(es). "
               "Increase SL_LOG_PRINT_LINE_MAX or disable "
               "SL_LOG_FORMATTED_IOSTREAM_PREFIX_TIMESTAMP / "
               "SL_LOG_FORMATTED_IOSTREAM_APPEND_CORE_ID.");

/*******************************************************************************
**************************   LOCAL FUNCTIONS   ********************************
*******************************************************************************/

#if SL_LOG_FORMATTED_IOSTREAM_PREFIX_TIMESTAMP || SL_LOG_FORMATTED_IOSTREAM_APPEND_CORE_ID
static const char hex_chars[] = "0123456789ABCDEF";
#endif

#if SL_LOG_FORMATTED_IOSTREAM_PREFIX_TIMESTAMP
static inline char* u32_to_hex8(char *p, uint32_t v)
{
  for (int i = 7; i >= 0; i--) {
    *p++ = hex_chars[(v >> (i * 4)) & 0xF];
  }
  return p;
}
#endif

#if SL_LOG_FORMATTED_IOSTREAM_APPEND_CORE_ID
static inline char* u8_to_hex2(char *p, uint8_t v)
{
  *p++ = hex_chars[(v >> 4) & 0xF];
  *p++ = hex_chars[v & 0xF];
  return p;
}
#endif

/*******************************************************************************
**************************   GLOBAL FUNCTIONS   ********************************
*******************************************************************************/

void sl_log_vprint_target_ex(uint32_t options, const char *fmt, va_list ap)
{
  (void)options;

  char line[SL_LOG_PRINT_LINE_MAX];
  size_t header_len = 0U;
  int body_len;
  size_t total;

  if (fmt == NULL) {
    return;
  }

#if SL_LOG_FORMATTED_IOSTREAM_PREFIX_TIMESTAMP
  {
    uint32_t timestamp = sl_log_get_timestamp_count(SL_LOG_HOST_CORE_ID);
    line[header_len++] = '[';
    char *p = u32_to_hex8(&line[header_len], timestamp);
    header_len = (size_t)(p - line);
    line[header_len++] = ']';
    line[header_len++] = ' ';
  }
#endif

#if SL_LOG_FORMATTED_IOSTREAM_APPEND_CORE_ID
  {
    line[header_len++] = '[';
    char *p = u8_to_hex2(&line[header_len], (uint8_t)SL_LOG_HOST_CORE_ID);
    header_len = (size_t)(p - line);
    line[header_len++] = ']';
    line[header_len++] = ' ';
  }
#endif

  if (header_len >= sizeof(line)) {
    return;
  }

  size_t body_capacity = sizeof(line) - header_len;
  body_len = vsnprintf(line + header_len, body_capacity, fmt, ap);
  if (body_len < 0) {
    return;
  }

  /* vsnprintf returns the would-be length and writes at most body_capacity-1
   * payload bytes plus a NUL at body_capacity-1 on truncation. Clamp so the
   * NUL byte is never transmitted. */
  size_t actual_body;
  if ((size_t)body_len < body_capacity) {
    actual_body = (size_t)body_len;
  } else {
    actual_body = body_capacity - 1U;
  }
  total = header_len + actual_body;

  (void)sl_iostream_write(sl_iostream_recommended_console_stream, line, total);
}

/**
 * @brief Initialize the logging backend.
 *
 * Sets the recommended console iostream as the default for log output.
 *
 * @return SL_STATUS_OK on success, an sl_status_t error code otherwise.
 */
sl_status_t sl_log_hal_backend_init(void)
{
  return sl_iostream_set_default(sl_iostream_recommended_console_stream);
}

/**
 * @brief Write a formatted log event to the backend transport.
 *
 * The formatted-output backend renders all string logs via
 * sl_log_vprint_target_ex(); the ring-buffer-driven event/string write path
 * is not exercised in this output mode (event logging is a no-op and string
 * logging is redirected to SL_PRINT_FMT_*). The function exists to satisfy
 * the @ref sl_log_api_backend_t contract.
 *
 * @return SL_STATUS_NOT_SUPPORTED.
 */
sl_status_t sl_log_hal_backend_write(sl_log_event_t *buffer, uint32_t read_index, uint32_t event_count)
{
  (void)buffer;
  (void)read_index;
  (void)event_count;
  return SL_STATUS_NOT_SUPPORTED;
}

/**
 * @brief Deinitialize the logging backend.
 *
 * @return SL_STATUS_OK.
 */
sl_status_t sl_log_hal_backend_deinit(void)
{
  return SL_STATUS_OK;
}

/**
 * @brief   Logging backend API structure.
 */
sl_log_api_backend_t sl_log_api_backend = { .backend_init   = sl_log_hal_backend_init,
                                            .backend_write  = sl_log_hal_backend_write,
                                            .backend_deinit = sl_log_hal_backend_deinit };

/**
 * @brief Return pointer to the backend API structure.
 *
 * @return Pointer to the populated sl_log_api_backend_t structure.
 */
sl_log_api_backend_t *sl_log_get_api_backend(void)
{
  return &sl_log_api_backend;
}
