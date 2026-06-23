/***************************************************************************//**
 * @file
 * @brief Macros for functional area and per-cluster debug printing
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

#ifndef __AF_DEBUG_PRINT__
#define __AF_DEBUG_PRINT__

#include <stdint.h>

#ifdef SL_COMPONENT_CATALOG_PRESENT
#include "sl_component_catalog.h"
#endif

/** When set, AF prints use the Silicon Labs logger (@ref sl_log). @ref sl_zigbee_af_core_println maps to ERROR
 *  severity in zcl-debug-print.h so core call sites need not #if between println and errorln.
 *  @ref SLI_ZIGBEE_DEBUG_USE_SL_LOG is additionally gated on the sl_log compile-time level being
 *  non-NONE: when logging is fully disabled at compile time, zigbee stack debug prints fall back
 *  to the legacy local_vprintf path instead of feeding into a no-op logger. */
#if defined(SL_COMPONENT_CATALOG_PRESENT) && defined(SL_CATALOG_LOG_COMPONENT_PRESENT)
#include "sl_log_common_config.h"
#if (SL_LOG_CONFIG_LEVEL_COMPILE_TIME != SL_LOG_CONFIG_LEVEL_NONE)
#define SLI_ZIGBEE_AF_PRINT_USE_SL_LOG 1
#define SLI_ZIGBEE_DEBUG_USE_SL_LOG 1
#endif
#endif

/** @brief Log levels for AF framework printing (uint32_t so host builds avoid sl_log_level_t).
 *  Values match @ref SL_LOG_CONFIG_LEVEL_DEBUG and siblings when the Silicon Labs logger is used.
 */
#define SLI_ZIGBEE_AF_PRINT_LOG_LEVEL_DEBUG ((uint32_t)1)
#define SLI_ZIGBEE_AF_PRINT_LOG_LEVEL_INFO  ((uint32_t)2)
#define SLI_ZIGBEE_AF_PRINT_LOG_LEVEL_WARN  ((uint32_t)3)
#define SLI_ZIGBEE_AF_PRINT_LOG_LEVEL_ERROR ((uint32_t)4)
#define SLI_ZIGBEE_AF_PRINT_LOG_LEVEL_CRASH ((uint32_t)5)
#define SLI_ZIGBEE_AF_PRINT_LOG_LEVEL_NONE  ((uint32_t)6)

/** Default sl_log severity for @ref sl_zigbee_af_print / @ref sl_zigbee_af_println (matches @ref SL_LOG_CONFIG_LEVEL_* numeric values). */
#if defined(SL_COMPONENT_CATALOG_PRESENT) && defined(SL_CATALOG_LOG_COMPONENT_PRESENT)
#if (SL_LOG_CONFIG_LEVEL_COMPILE_TIME == SL_LOG_CONFIG_LEVEL_NONE)
#define SLI_ZIGBEE_AF_PRINT_DEFAULT_LOG_LEVEL SLI_ZIGBEE_AF_PRINT_LOG_LEVEL_NONE
#elif (SL_LOG_CONFIG_LEVEL_COMPILE_TIME == SL_LOG_CONFIG_LEVEL_CRASH)
#define SLI_ZIGBEE_AF_PRINT_DEFAULT_LOG_LEVEL SLI_ZIGBEE_AF_PRINT_LOG_LEVEL_ERROR
#elif (SL_LOG_CONFIG_LEVEL_COMPILE_TIME == SL_LOG_CONFIG_LEVEL_ERROR)
#define SLI_ZIGBEE_AF_PRINT_DEFAULT_LOG_LEVEL SLI_ZIGBEE_AF_PRINT_LOG_LEVEL_ERROR
#elif (SL_LOG_CONFIG_LEVEL_COMPILE_TIME == SL_LOG_CONFIG_LEVEL_WARN)
#define SLI_ZIGBEE_AF_PRINT_DEFAULT_LOG_LEVEL SLI_ZIGBEE_AF_PRINT_LOG_LEVEL_WARN
#elif (SL_LOG_CONFIG_LEVEL_COMPILE_TIME == SL_LOG_CONFIG_LEVEL_INFO)
#define SLI_ZIGBEE_AF_PRINT_DEFAULT_LOG_LEVEL SLI_ZIGBEE_AF_PRINT_LOG_LEVEL_INFO
#elif (SL_LOG_CONFIG_LEVEL_COMPILE_TIME == SL_LOG_CONFIG_LEVEL_DEBUG)
#define SLI_ZIGBEE_AF_PRINT_DEFAULT_LOG_LEVEL SLI_ZIGBEE_AF_PRINT_LOG_LEVEL_DEBUG
#else
#define SLI_ZIGBEE_AF_PRINT_DEFAULT_LOG_LEVEL SLI_ZIGBEE_AF_PRINT_LOG_LEVEL_INFO
#endif
#else
#define SLI_ZIGBEE_AF_PRINT_DEFAULT_LOG_LEVEL SLI_ZIGBEE_AF_PRINT_LOG_LEVEL_INFO
#endif

#if !defined(SL_ZIGBEE_AF_PRINT_OUTPUT) && defined(APP_SERIAL)
  #define SL_ZIGBEE_AF_PRINT_OUTPUT APP_SERIAL
#endif

#include "zcl-debug-print.h"
#include "mac-types.h" // for sl_802154_long_addr_t

extern uint16_t sl_zigbee_af_print_active_area;

/** @name Printing */
// @{

// Guaranteed print
/**
 * @brief Print that can't be turned off.
 *
 */
#define sl_zigbee_af_guaranteed_print(...)   sl_zigbee_af_print(0xFFFF, __VA_ARGS__)

/**
 * @brief Println that can't be turned off.
 */
#define sl_zigbee_af_guaranteed_println(...) sl_zigbee_af_println(0xFFFF, __VA_ARGS__)

/**
 * @brief Buffer print that can't be turned off.
 */
#define sl_zigbee_af_guaranteed_print_buffer(buffer, len, withSpace) sl_zigbee_af_print_buffer(0xFFFF, (buffer), (len), (withSpace))

/**
 * @brief String print that can't be turned off.
 */
#define sl_zigbee_af_guaranteed_print_string(buffer) sl_zigbee_af_print_string(0xFFFF, (buffer))

/**
 * @brief Long string print that can't be turned off.
 */
#define sl_zigbee_af_guaranteed_print_long_string(buffer) sl_zigbee_af_print_long_string(0xFFFF, (buffer))

/**
 * @brief returns true if certain debug area is enabled.
 */
bool sl_zigbee_af_print_enabled(uint16_t functionality);

/**
 * @brief Useful function to print a buffer
 */
void sl_zigbee_af_print_buffer(uint16_t area, const uint8_t *buffer, uint16_t bufferLen, bool withSpaces);

/**
 * @brief Useful function to print character strings.  The first byte of the
 * buffer specifies the length of the string.
 */
void sl_zigbee_af_print_string(uint16_t area, const uint8_t *buffer);

/**
 * @brief Useful function to print long character strings.  The first two bytes
 * of the buffer specify the length of the string.
 */
void sl_zigbee_af_print_long_string(uint16_t area, const uint8_t *buffer);

/**
 * @brief prints the specified text if certain debug are is enabled
 * @param functionality: one of the EMBER_AF_PRINT_xxx macros as defined by AppBuilder
 * @param formatString: formatString for varargs
 */
void sl_zigbee_af_print(uint16_t functionality, const char * formatString, ...);

/**
 * @brief prints the specified text if certain debug are is enabled.
 * Print-out will include the newline character at the end.
 * @param functionality: one of the EMBER_AF_PRINT_xxx macros as defined by AppBuilder
 * @param formatString: formatString for varargs
 */
void sl_zigbee_af_println(uint16_t functionality, const char * formatString, ...);

/**
 * @brief Print with explicit log level and optional trailing newline.
 * @param functionality Print area (same as @ref sl_zigbee_af_print).
 * @param print_new_line If true, append newline after the formatted text (like @ref sl_zigbee_af_println).
 * @param log_level One of @ref SLI_ZIGBEE_AF_PRINT_LOG_LEVEL_DEBUG through @ref SLI_ZIGBEE_AF_PRINT_LOG_LEVEL_ERROR (uint32_t for host builds).
 */
void sl_zigbee_af_print_with_log(uint16_t functionality,
                                 bool print_new_line,
                                 uint32_t log_level,
                                 const char *formatString,
                                 ...);

/**
 * @brief turns on debugging for certain functional area
 */
void sl_zigbee_af_print_on(uint16_t functionality);

/**
 * @brief turns off debugging for certain functional area
 */
void sl_zigbee_af_print_off(uint16_t functionality);

#if !defined(SL_ZIGBEE_AF_GENERATE_CLI)
/** @brief turns on debugging for all functional areas
 */
void sl_zigbee_af_print_all_on(void);

/**
 * @brief turns off debugging for all functional areas
 */
void sl_zigbee_af_print_all_off(void);

/**
 * @brief prints current status of functional areas
 */
void sl_zigbee_af_print_status(void);
#endif

#if defined(SL_CATALOG_ZIGBEE_DEBUG_PRINT_PRESENT)
/**
 * @brief prints eui64 stored in little endian format
 */
void sl_zigbee_af_print_little_endian_eui64(const sl_802154_long_addr_t eui64);

/**
 * @brief prints eui64 stored in big endian format
 */
void sl_zigbee_af_print_big_endian_eui64(const sl_802154_long_addr_t eui64);

/**
 * @brief prints all message data in message format
 */
void sl_zigbee_af_print_message_data(uint8_t* data, uint16_t length);

/** @} END Printing */

extern void printZigbeeKey(const uint8_t* key);
extern void printCert(const uint8_t* cert);
extern void printKey(bool publicKey, const uint8_t* key);
extern void printKey283k1(bool publicKey, const uint8_t* key);
extern void printCert283k1(const uint8_t* cert);
extern void printIeeeLine(const sl_802154_long_addr_t ieee);
extern void printTextLine(const char * text);
// These print functions are required by the CBKE crypto engine.
#define sl_zigbee_af_print_zigbee_key printZigbeeKey
#define sl_zigbee_af_print_cert      printCert
#define sl_zigbee_af_print_key       printKey
#define sl_zigbee_af_print_ieee_line  printIeeeLine
#define sl_zigbee_af_print_text_line  printTextLine
#define sl_zigbee_af_print_public_key(key)  printKey(true, key)
#define sl_zigbee_af_print_private_key(key) printKey(false, key)
#define sl_zigbee_af_print_key_283k1 printKey283k1
#define sl_zigbee_af_print_cert_283k1  printCert283k1

void sl_zigbee_af_print8_byte_blocks(uint8_t numBlocks,
                                     const uint8_t *block,
                                     bool crBetweenBlocks);
void sl_zigbee_af_print_issuer(const uint8_t *issuer);

void sl_zigbee_af_print_channel_list_from_mask(uint32_t channelMask);

void sli_zigbee_af_print_status(const char * task,
                                sl_status_t status);
#else

#define sl_zigbee_af_print_little_endian_eui64(...)

/**
 * @brief prints eui64 stored in big endian format
 */
#define sl_zigbee_af_print_big_endian_eui64(...)

/**
 * @brief prints all message data in message format
 */
#define sl_zigbee_af_print_message_data(...)

/** @} END Printing */

#define sl_zigbee_af_print_zigbee_key(...)
#define sl_zigbee_af_print_cert(...)
#define sl_zigbee_af_print_cert_283k1(...)
#define sl_zigbee_af_print_key(...)
#define sl_zigbee_af_print_key_283k1(...)
#define sl_zigbee_af_print_ieee_line(...)
#define sl_zigbee_af_print_text_line(...)

#define sl_zigbee_af_print8_byte_blocks(...)
#define sl_zigbee_af_print_issuer(...)
#define sl_zigbee_af_print_channel_list_from_mask(...)
#define sli_zigbee_af_print_status(...)

#endif // SL_CATALOG_ZIGBEE_DEBUG_PRINT_PRESENT
#endif // __AF_DEBUG_PRINT__
