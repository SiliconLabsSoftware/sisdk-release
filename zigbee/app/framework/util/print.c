/***************************************************************************//**
 * @file
 * @brief Utilities and command line interface for printing, and enabling/disabling
 * printing to different areas.
 *******************************************************************************
 * # License
 * <b>Copyright 2018 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * The licensor of this software is Silicon Laboratories Inc. Your use of this
 * software is governed by the terms of Silicon Labs Master Software License
 * Agreement (MSLA) available at
 * www.silabs.com/about-us/legal/master-software-license-agreement. This
 * software is distributed to you in Source Code format and is governed by the
 * sections of the MSLA applicable to Source Code.
 *
 ******************************************************************************/

#include <stdint.h>
#include <stddef.h>
#include <stdarg.h>
#include <stdio.h>
#include "app/framework/include/af.h"
#include "app/framework/plugin/debug-print/sl_zigbee_debug_print.h"
#ifdef SL_COMPONENT_CATALOG_PRESENT
#include "sl_component_catalog.h"
#endif
#if defined(SL_COMPONENT_CATALOG_PRESENT) && defined(SL_CATALOG_LOG_COMPONENT_PRESENT)
#include "sl_log_helper.h"
#include <stdio.h>
#endif

#ifndef SLI_ZIGBEE_AF_PRINT_SL_LOG_BUFFER_SIZE
/** Max formatted length for one AF print line before sending to the debug logger. */
#define SLI_ZIGBEE_AF_PRINT_SL_LOG_BUFFER_SIZE 256
#endif
//------------------------------------------------------------------------------
// Globals

// Enable this if you want area names printed. It proved annoying
// so we're disabling it here.
//#define SL_ZIGBEE_AF_PRINT_AREA_NAME

#ifdef SL_ZIGBEE_AF_PRINT_AREA_NAME
static void reallyPrintAreaName(uint16_t area);
  #define printAreaName(area) reallyPrintAreaName(area)
#else
  #define printAreaName(area)
#endif //SL_ZIGBEE_AF_PRINT_AREA_NAME

#ifdef SL_ZIGBEE_AF_PRINT_NAMES
static const char * areaNames[] = SL_ZIGBEE_AF_PRINT_NAMES;
#endif

#ifdef SL_ZIGBEE_AF_PRINT_BITS
static uint8_t enablementBytes[] = SL_ZIGBEE_AF_PRINT_BITS;
#endif

uint16_t sl_zigbee_af_print_active_area = 0;

//------------------------------------------------------------------------------

// In the first stage of Zigbee/UC there is no run-time enabling/disabling of
// debug prints
bool sl_zigbee_af_print_enabled(uint16_t area)
{
  sl_zigbee_af_print_active_area = area;
  return true;
}

static void printEnable(uint16_t area, bool on)
{
#ifdef SL_ZIGBEE_AF_PRINT_BITS
  uint8_t index = (uint8_t)(area >> 8);
  if ( index < sizeof(enablementBytes) ) {
    if ( on ) {
      enablementBytes[index] |= (uint8_t)(area & 0xFF);
    } else {
      enablementBytes[index] &= ~(uint8_t)(area & 0xFF);
    }
  }
#else
  (void) area;
  (void) on;
#endif // SL_ZIGBEE_AF_PRINT_BITS
}

static uint16_t convertUserNumberAreaToInternalArea(uint16_t userNumberedArea)
{
  uint16_t index = userNumberedArea / 8;
  index = (uint16_t)(index << 8)
          + (uint16_t)( ((uint16_t)0x0001) << (userNumberedArea % 8) );
  return index;
}

#if defined SL_ZIGBEE_AF_PRINT_AREA_NAME
static void reallyPrintAreaName(uint16_t area)
{
#ifdef SL_ZIGBEE_AF_PRINT_NAMES
  uint8_t hi, lo, count;
  uint16_t index;

  hi = (uint8_t)(area >> 8);
  lo = (uint8_t)(area & 0xFF);
  count = 0;

  if ( lo != 0 ) {
    while ( !(lo & 0x01) ) {
      lo >>= 1;
      count++;
    }
  }
  index = ((8 * hi) + count);

  if (area != 0xFFFF
      && index < EMBER_AF_PRINT_NAME_NUMBER) {
    sl_zigbee_core_debug_print("%s:", areaNames[index]);
  }
#endif // SL_ZIGBEE_AF_PRINT_NAMES
}
#endif //SL_ZIGBEE_AF_PRINT_AREA_NAME

#if defined(SLI_ZIGBEE_AF_PRINT_USE_SL_LOG)
static void sli_zigbee_af_print_sl_log_string(uint32_t log_level, const char *str)
{
  uint32_t addr = (uint32_t)(uintptr_t)str;
  if (log_level == SLI_ZIGBEE_AF_PRINT_LOG_LEVEL_DEBUG) {
    SL_PRINT_STRING_DEBUG("%s", addr);
  } else if (log_level == SLI_ZIGBEE_AF_PRINT_LOG_LEVEL_WARN) {
    SL_PRINT_STRING_WARN("%s", addr);
  } else if (log_level == SLI_ZIGBEE_AF_PRINT_LOG_LEVEL_ERROR) {
    SL_PRINT_STRING_ERROR("%s", addr);
  } else {
    SL_PRINT_STRING_INFO("%s", addr);
  }
}
#endif

// Prints the trace if trace is enabled
SL_WEAK void sli_zigbee_af_print_internal_var_arg(uint16_t area,
                                                  uint32_t log_level,
                                                  bool newLine,
                                                  const char * formatString,
                                                  va_list ap)
{
  if ( !sl_zigbee_af_print_enabled(area) ) {
    return;
  }
  printAreaName(area);
#if defined(SLI_ZIGBEE_AF_PRINT_USE_SL_LOG)
  {
    char buf[SLI_ZIGBEE_AF_PRINT_SL_LOG_BUFFER_SIZE];
    int n = vsnprintf(buf, sizeof(buf), formatString, ap);
    buf[sizeof(buf) - 1U] = '\0';
    if (n < 0) {
      n = 0;
    }
    size_t len = (size_t)n;
    if (len >= sizeof(buf)) {
      len = sizeof(buf) - 1U;
    }
    if (len > 0U) {
      sli_zigbee_af_print_sl_log_string(log_level, buf);
    }
    if (newLine) {
      sli_zigbee_af_print_sl_log_string(log_level, "\n");
      }
  }
#else
  (void)log_level;
#ifdef SL_CATALOG_ZIGBEE_SIMULATION_PRESENT
  (void) local_vprintf(formatString, ap);
#else
  (void) vprintf(formatString, ap);
#endif // SL_CATALOG_ZIGBEE_SIMULATION_PRESENT
  if (newLine) {
    sl_zigbee_core_debug_println("");
  }
#endif // SLI_ZIGBEE_AF_PRINT_USE_SL_LOG
}

static void sli_zigbee_af_finish_print_var_arg(uint16_t area,
                                               uint32_t log_level,
                                               bool newLine,
                                               const char *formatString,
                                               va_list ap)
{
  sli_zigbee_af_print_internal_var_arg(area, log_level, newLine, formatString, ap);
  sl_zigbee_af_print_active_area = area;
}

void sl_zigbee_af_print_with_log(uint16_t area,
                                 bool print_new_line,
                                 uint32_t log_level,
                                 const char *formatString,
                                 ...)
{
  va_list ap;
  va_start(ap, formatString);
  sli_zigbee_af_finish_print_var_arg(area, log_level, print_new_line, formatString, ap);
  va_end(ap);
}

void sl_zigbee_af_println(uint16_t area, const char * formatString, ...)
{
  va_list ap = { 0 };
  va_start(ap, formatString);
  sli_zigbee_af_finish_print_var_arg(area,
                                     SLI_ZIGBEE_AF_PRINT_DEFAULT_LOG_LEVEL,
                                     true,
                                     formatString,
                                     ap);
  va_end(ap);
}

void sl_zigbee_af_print(uint16_t area, const char * formatString, ...)
{
  va_list ap = { 0 };
  va_start(ap, formatString);
  sli_zigbee_af_finish_print_var_arg(area,
                                     SLI_ZIGBEE_AF_PRINT_DEFAULT_LOG_LEVEL,
                                     false,
                                     formatString,
                                     ap);
  va_end(ap);
}

void sl_zigbee_af_print_status(void)
{
#ifdef SL_ZIGBEE_AF_PRINT_NAMES
  uint8_t i;
  for (i = 0; i < EMBER_AF_PRINT_NAME_NUMBER; i++) {
    sl_zigbee_core_debug_println("[%d] %s : %s",
                                 i,
                                 areaNames[i],
                                 (sl_zigbee_af_print_enabled(
                                    convertUserNumberAreaToInternalArea(i))
                                  ? "YES"
                                  : "no"));
    (void) sli_legacy_serial_wait_send(SL_ZIGBEE_AF_PRINT_OUTPUT);
  }
#endif // SL_ZIGBEE_AF_PRINT_NAMES
}

void sl_zigbee_af_print_all_on(void)
{
#ifdef SL_ZIGBEE_AF_PRINT_BITS
  memset(enablementBytes, 0xFF, sizeof(enablementBytes));
#endif
}

void sl_zigbee_af_print_all_off(void)
{
#ifdef SL_ZIGBEE_AF_PRINT_BITS
  memset(enablementBytes, 0x00, sizeof(enablementBytes));
#endif
}

// These are CLI functions where a user will supply a sequential numbered
// area; as opposed to the bitmask area number that we keep track
// of internally.

void sl_zigbee_af_print_on(uint16_t userArea)
{
  printEnable(convertUserNumberAreaToInternalArea(userArea),
              true);   // enable?
}

void sl_zigbee_af_print_off(uint16_t userArea)
{
  printEnable(convertUserNumberAreaToInternalArea(userArea),
              false);  // enable?
}
