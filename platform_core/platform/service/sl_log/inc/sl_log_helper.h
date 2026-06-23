
/***************************************************************************/ /**
* @file sl_log_helper.h
* @brief SL Log Helper Macros and Utilities
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

#ifndef SL_LOG_HELPER_H
#define SL_LOG_HELPER_H

#ifdef __cplusplus
extern "C" {
#endif
#if defined(SL_COMPONENT_CATALOG_PRESENT)
#include "sl_component_catalog.h"
#endif
#include "sl_log.h"
#include "sl_log_common_config.h"
#include "sl_common.h"
#ifdef SL_CATALOG_LOG_BACKEND_SYSTEMVIEW_PRESENT
#include "SEGGER_SYSVIEW.h"
#include "sl_log_systemview_helper.h"
#endif
#define SL_STRINGIFY(x) STRINGIZE(x)

/** @addtogroup sl_log_helper SL Log Helper Functions
 * @brief Helper macros and utilities for the Silicon Labs logging system
 *
 * This module provides the core helper macros that user can use to log messages and
 * events with various log levels and argument counts. It includes compile-time validation
 * to ensure correct usage and efficient logging implementations.
 *
 * @{
 */

/**
 * @defgroup sl_log_disabled_macros Disabled Logging Macros
 * @brief Macros that disable logging when compile-time level is set to NONE
 *
 * When SL_LOG_CONFIG_LEVEL_COMPILE_TIME is set to SL_LOG_CONFIG_LEVEL_NONE,
 * all logging macros are replaced with void operations to completely eliminate
 * logging overhead at compile time.
 *
 * @{
 */


/**
 * @defgroup sl_log_memory_sections Memory Section Definitions
 * @brief Linker section attributes for log string placement
 * @{
 */

/**
 * @defgroup sl_log_compiler_support Compiler-Specific Support
 * @brief Compiler-specific definitions for string section placement
 * @{
 */
#if defined(__GNUC__)
/**
 * @brief Linker section attribute for log format strings
 *
 * This attribute places log format strings in a dedicated memory section
 * for optimized memory layout and potential compression or removal.
 */
#define SL_COMPACT_STRINGS_SECTION __attribute__((section(".log_fmt")))

#elif defined(__ICCARM__)
/**
 * @brief Compiler-specific string section placement for IAR
 *
 * IAR-specific pragma for placing log format strings in a dedicated section.
 */
#define SL_COMPACT_STRINGS_SECTION @"log_fmt"

#else
/**
 * @brief Default definition (no special section)
 *
 * For compilers that don't support custom section placement.
 */
#define SL_COMPACT_STRINGS_SECTION
#endif

/** @} (end addtogroup sl_log_memory_sections) */

/** @} (end addtogroup sl_log_compiler_support) */




#define SL_PRINT_VOID_ARG0_DBG(EVENT, EVENT_TYPE)                           do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); } while (0)
#define SL_PRINT_VOID_ARG0_ERR(EVENT, EVENT_TYPE)                           do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); } while (0)
#define SL_PRINT_VOID_ARG0_WRN(EVENT, EVENT_TYPE)                           do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); } while (0)
#define SL_PRINT_VOID_ARG0_INFO(EVENT, EVENT_TYPE)                          do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); } while (0)
#define SL_PRINT_VOID_ARG0_CRASH(EVENT, EVENT_TYPE)                         do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); } while (0)

#define SL_PRINT_VOID_ARG1_DBG(EVENT, EVENT_TYPE, ARG1)                     do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); } while (0)
#define SL_PRINT_VOID_ARG1_ERR(EVENT, EVENT_TYPE, ARG1)                     do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); } while (0)
#define SL_PRINT_VOID_ARG1_WRN(EVENT, EVENT_TYPE, ARG1)                     do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); } while (0)
#define SL_PRINT_VOID_ARG1_INFO(EVENT, EVENT_TYPE, ARG1)                    do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); } while (0)
#define SL_PRINT_VOID_ARG1_CRASH(EVENT, EVENT_TYPE, ARG1)                   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); } while (0)

#define SL_PRINT_VOID_ARG2_DBG(EVENT, EVENT_TYPE, ARG1, ARG2)               do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); } while (0)
#define SL_PRINT_VOID_ARG2_ERR(EVENT, EVENT_TYPE, ARG1, ARG2)               do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); } while (0)
#define SL_PRINT_VOID_ARG2_WRN(EVENT, EVENT_TYPE, ARG1, ARG2)               do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); } while (0)
#define SL_PRINT_VOID_ARG2_INFO(EVENT, EVENT_TYPE, ARG1, ARG2)              do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); } while (0)
#define SL_PRINT_VOID_ARG2_CRASH(EVENT, EVENT_TYPE, ARG1, ARG2)             do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); } while (0)

#define SL_PRINT_VOID_ARG3_DBG(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3)         do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); } while (0)
#define SL_PRINT_VOID_ARG3_ERR(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3)         do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); } while (0)
#define SL_PRINT_VOID_ARG3_WRN(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3)         do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); } while (0)
#define SL_PRINT_VOID_ARG3_INFO(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3)        do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); } while (0)
#define SL_PRINT_VOID_ARG3_CRASH(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3)       do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); } while (0)

#define SL_PRINT_VOID_ARG4_DBG(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); } while (0)
#define SL_PRINT_VOID_ARG4_ERR(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); } while (0)
#define SL_PRINT_VOID_ARG4_WRN(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); } while (0)
#define SL_PRINT_VOID_ARG4_INFO(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4)  do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); } while (0)
#define SL_PRINT_VOID_ARG4_CRASH(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4)  do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); } while (0)

#define SL_PRINT_VOID_ARG5_DBG(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); } while (0)
#define SL_PRINT_VOID_ARG5_ERR(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); } while (0)
#define SL_PRINT_VOID_ARG5_WRN(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); } while (0)
#define SL_PRINT_VOID_ARG5_INFO(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5)  do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); } while (0)
#define SL_PRINT_VOID_ARG5_CRASH(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5)  do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); } while (0)

#define SL_PRINT_VOID_ARG6_DBG(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); } while (0)
#define SL_PRINT_VOID_ARG6_ERR(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); } while (0)
#define SL_PRINT_VOID_ARG6_WRN(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); } while (0)
#define SL_PRINT_VOID_ARG6_INFO(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6)  do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); } while (0)
#define SL_PRINT_VOID_ARG6_CRASH(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6)  do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); } while (0)

#define SL_PRINT_VOID_ARG7_DBG(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); } while (0)
#define SL_PRINT_VOID_ARG7_ERR(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); } while (0)
#define SL_PRINT_VOID_ARG7_WRN(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); } while (0)
#define SL_PRINT_VOID_ARG7_INFO(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7)  do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); } while (0)
#define SL_PRINT_VOID_ARG7_CRASH(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7)  do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); } while (0)

#define SL_PRINT_VOID_ARG8_DBG(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); (void)sizeof(ARG8); } while (0)
#define SL_PRINT_VOID_ARG8_ERR(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); (void)sizeof(ARG8); } while (0)
#define SL_PRINT_VOID_ARG8_WRN(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); (void)sizeof(ARG8); } while (0)
#define SL_PRINT_VOID_ARG8_INFO(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8)  do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); (void)sizeof(ARG8); } while (0)
#define SL_PRINT_VOID_ARG8_CRASH(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8)  do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); (void)sizeof(ARG8); } while (0)

#define SL_PRINT_VOID_ARG9_DBG(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); (void)sizeof(ARG8); (void)sizeof(ARG9); } while (0)
#define SL_PRINT_VOID_ARG9_ERR(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); (void)sizeof(ARG8); (void)sizeof(ARG9); } while (0)
#define SL_PRINT_VOID_ARG9_WRN(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); (void)sizeof(ARG8); (void)sizeof(ARG9); } while (0)
#define SL_PRINT_VOID_ARG9_INFO(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9)  do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); (void)sizeof(ARG8); (void)sizeof(ARG9); } while (0)
#define SL_PRINT_VOID_ARG9_CRASH(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9)  do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); (void)sizeof(ARG8); (void)sizeof(ARG9); } while (0)

#define SL_PRINT_VOID_ARG10_DBG(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); (void)sizeof(ARG8); (void)sizeof(ARG9); (void)sizeof(ARG10); } while (0)
#define SL_PRINT_VOID_ARG10_ERR(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); (void)sizeof(ARG8); (void)sizeof(ARG9); (void)sizeof(ARG10); } while (0)
#define SL_PRINT_VOID_ARG10_WRN(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10)   do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); (void)sizeof(ARG8); (void)sizeof(ARG9); (void)sizeof(ARG10); } while (0)
#define SL_PRINT_VOID_ARG10_INFO(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10)  do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); (void)sizeof(ARG8); (void)sizeof(ARG9); (void)sizeof(ARG10); } while (0)
#define SL_PRINT_VOID_ARG10_CRASH(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10)  do { (void)sizeof(EVENT); (void)sizeof(EVENT_TYPE); (void)sizeof(ARG1); (void)sizeof(ARG2); (void)sizeof(ARG3); (void)sizeof(ARG4); (void)sizeof(ARG5); (void)sizeof(ARG6); (void)sizeof(ARG7); (void)sizeof(ARG8); (void)sizeof(ARG9); (void)sizeof(ARG10); } while (0)

/** @} (end addtogroup sl_log_disabled_macros) */

/**
 * @defgroup sl_log_backend_functions Backend Function Declarations
 * @brief External function declarations for log backend implementations
 *
 * These functions are provided by the selected backend implementation
 * (proprietary or SystemView) and handle the actual transmission of
 * log messages with various argument counts.
 *
 * @{
 */

/**
 * @defgroup sl_log_active_macros Active Logging Macros
 * @brief Macros that perform actual logging when enabled
 *
 * These macros are used when logging is enabled (compile-time level is not
 * NONE). They call the appropriate backend functions with formatted log level
 * information.
 *
 * @{
 */

#if !defined(SL_CATALOG_LOG_BACKEND_SYSTEMVIEW_PRESENT)

/** @brief Send debug log message with no arguments */
#define SL_PRINT_ARG0_DBG(EVENT, EVENT_TYPE)                                   \
  sl_log_send_no_args(EVENT, SL_LOG_CONFIG_LEVEL_DEBUG << 1 | EVENT_TYPE)

/** @brief Send error log message with no arguments */
#define SL_PRINT_ARG0_ERR(EVENT, EVENT_TYPE)                                   \
  sl_log_send_no_args(EVENT, SL_LOG_CONFIG_LEVEL_ERROR << 1 | EVENT_TYPE)

/** @brief Send crash log message with no arguments */
#define SL_PRINT_ARG0_CRASH(EVENT, EVENT_TYPE)                                 \
  sl_log_send_no_args(EVENT, SL_LOG_CONFIG_LEVEL_CRASH << 1 | EVENT_TYPE)

/** @brief Send warning log message with no arguments */
#define SL_PRINT_ARG0_WRN(EVENT, EVENT_TYPE)                                   \
  sl_log_send_no_args(EVENT, SL_LOG_CONFIG_LEVEL_WARN << 1 | EVENT_TYPE)

/** @brief Send info log message with no arguments */
#define SL_PRINT_ARG0_INFO(EVENT, EVENT_TYPE)                                  \
  sl_log_send_no_args(EVENT, SL_LOG_CONFIG_LEVEL_INFO << 1 | EVENT_TYPE)

/** @brief Send debug log message with 1 argument */
#define SL_PRINT_ARG1_DBG(EVENT, EVENT_TYPE, ARG1)                             \
  sl_log_send_arg1(EVENT, SL_LOG_CONFIG_LEVEL_DEBUG << 1 | EVENT_TYPE, ARG1)

/** @brief Send error log message with 1 argument */
#define SL_PRINT_ARG1_ERR(EVENT, EVENT_TYPE, ARG1)                             \
  sl_log_send_arg1(EVENT, SL_LOG_CONFIG_LEVEL_ERROR << 1 | EVENT_TYPE, ARG1)

/** @brief Send crash log message with 1 argument */
#define SL_PRINT_ARG1_CRASH(EVENT, EVENT_TYPE, ARG1)                           \
  sl_log_send_arg1(EVENT, SL_LOG_CONFIG_LEVEL_CRASH << 1 | EVENT_TYPE, ARG1)

/** @brief Send warning log message with 1 argument */
#define SL_PRINT_ARG1_WRN(EVENT, EVENT_TYPE, ARG1)                             \
  sl_log_send_arg1(EVENT, SL_LOG_CONFIG_LEVEL_WARN << 1 | EVENT_TYPE, ARG1)

/** @brief Send info log message with 1 argument */
#define SL_PRINT_ARG1_INFO(EVENT, EVENT_TYPE, ARG1)                            \
  sl_log_send_arg1(EVENT, SL_LOG_CONFIG_LEVEL_INFO << 1 | EVENT_TYPE, ARG1)

/** @brief Send debug log message with 2 arguments */
#define SL_PRINT_ARG2_DBG(EVENT, EVENT_TYPE, ARG1, ARG2)                       \
  sl_log_send_arg2(EVENT, SL_LOG_CONFIG_LEVEL_DEBUG << 1 | EVENT_TYPE, ARG1,   \
                   ARG2)

/** @brief Send error log message with 2 arguments */
#define SL_PRINT_ARG2_ERR(EVENT, EVENT_TYPE, ARG1, ARG2)                       \
  sl_log_send_arg2(EVENT, SL_LOG_CONFIG_LEVEL_ERROR << 1 | EVENT_TYPE, ARG1,   \
                   ARG2)

/** @brief Send crash log message with 2 arguments */
#define SL_PRINT_ARG2_CRASH(EVENT, EVENT_TYPE, ARG1, ARG2)                      \
  sl_log_send_arg2(EVENT, SL_LOG_CONFIG_LEVEL_CRASH << 1 | EVENT_TYPE, ARG1,   \
                   ARG2)

/** @brief Send warning log message with 2 arguments */
#define SL_PRINT_ARG2_WRN(EVENT, EVENT_TYPE, ARG1, ARG2)                       \
  sl_log_send_arg2(EVENT, SL_LOG_CONFIG_LEVEL_WARN << 1 | EVENT_TYPE, ARG1,    \
                   ARG2)

/** @brief Send info log message with 2 arguments */
#define SL_PRINT_ARG2_INFO(EVENT, EVENT_TYPE, ARG1, ARG2)                      \
  sl_log_send_arg2(EVENT, SL_LOG_CONFIG_LEVEL_INFO << 1 | EVENT_TYPE, ARG1,    \
                   ARG2)

/** @brief Send debug log message with 3 arguments */
#define SL_PRINT_ARG3_DBG(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3)                 \
  sl_log_send_arg3(EVENT, SL_LOG_CONFIG_LEVEL_DEBUG << 1 | EVENT_TYPE, ARG1,   \
                   ARG2, ARG3)

/** @brief Send error log message with 3 arguments */
#define SL_PRINT_ARG3_ERR(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3)                 \
  sl_log_send_arg3(EVENT, SL_LOG_CONFIG_LEVEL_ERROR << 1 | EVENT_TYPE, ARG1,   \
                   ARG2, ARG3)

/** @brief Send crash log message with 3 arguments */
#define SL_PRINT_ARG3_CRASH(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3)               \
  sl_log_send_arg3(EVENT, SL_LOG_CONFIG_LEVEL_CRASH << 1 | EVENT_TYPE, ARG1,   \
                   ARG2, ARG3)

/** @brief Send warning log message with 3 arguments */
#define SL_PRINT_ARG3_WRN(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3)                 \
  sl_log_send_arg3(EVENT, SL_LOG_CONFIG_LEVEL_WARN << 1 | EVENT_TYPE, ARG1,    \
                   ARG2, ARG3)

/** @brief Send info log message with 3 arguments */
#define SL_PRINT_ARG3_INFO(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3)                \
  sl_log_send_arg3(EVENT, SL_LOG_CONFIG_LEVEL_INFO << 1 | EVENT_TYPE, ARG1,    \
                   ARG2, ARG3)

#if (SL_LOG_CONFIG_ARG >= 4)
/** @brief Send debug log message with 4 arguments */
#define SL_PRINT_ARG4_DBG(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4)          \
  sl_log_send_arg4(EVENT, SL_LOG_CONFIG_LEVEL_DEBUG << 1 | EVENT_TYPE, ARG1,  \
                   ARG2, ARG3, ARG4)
/** @brief Send error log message with 4 arguments */
#define SL_PRINT_ARG4_ERR(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4)          \
  sl_log_send_arg4(EVENT, SL_LOG_CONFIG_LEVEL_ERROR << 1 | EVENT_TYPE, ARG1,   \
                   ARG2, ARG3, ARG4)
/** @brief Send crash log message with 4 arguments */
#define SL_PRINT_ARG4_CRASH(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4)         \
  sl_log_send_arg4(EVENT, SL_LOG_CONFIG_LEVEL_CRASH << 1 | EVENT_TYPE, ARG1,   \
                   ARG2, ARG3, ARG4)
/** @brief Send warning log message with 4 arguments */
#define SL_PRINT_ARG4_WRN(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4)          \
  sl_log_send_arg4(EVENT, SL_LOG_CONFIG_LEVEL_WARN << 1 | EVENT_TYPE, ARG1,    \
                   ARG2, ARG3, ARG4)
/** @brief Send info log message with 4 arguments */
#define SL_PRINT_ARG4_INFO(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4)          \
  sl_log_send_arg4(EVENT, SL_LOG_CONFIG_LEVEL_INFO << 1 | EVENT_TYPE, ARG1,   \
                   ARG2, ARG3, ARG4)
#endif

#if (SL_LOG_CONFIG_ARG >= 5)
#define SL_PRINT_ARG5_DBG(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5)     \
  sl_log_send_arg5(EVENT, SL_LOG_CONFIG_LEVEL_DEBUG << 1 | EVENT_TYPE, ARG1,   \
                   ARG2, ARG3, ARG4, ARG5)
#define SL_PRINT_ARG5_ERR(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5)     \
  sl_log_send_arg5(EVENT, SL_LOG_CONFIG_LEVEL_ERROR << 1 | EVENT_TYPE, ARG1,   \
                   ARG2, ARG3, ARG4, ARG5)
#define SL_PRINT_ARG5_CRASH(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5)   \
  sl_log_send_arg5(EVENT, SL_LOG_CONFIG_LEVEL_CRASH << 1 | EVENT_TYPE, ARG1,   \
                   ARG2, ARG3, ARG4, ARG5)
#define SL_PRINT_ARG5_WRN(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5)     \
  sl_log_send_arg5(EVENT, SL_LOG_CONFIG_LEVEL_WARN << 1 | EVENT_TYPE, ARG1,    \
                   ARG2, ARG3, ARG4, ARG5)
#define SL_PRINT_ARG5_INFO(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5)    \
  sl_log_send_arg5(EVENT, SL_LOG_CONFIG_LEVEL_INFO << 1 | EVENT_TYPE, ARG1,    \
                   ARG2, ARG3, ARG4, ARG5)
#endif

#if (SL_LOG_CONFIG_ARG >= 6)
#define SL_PRINT_ARG6_DBG(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6) \
  sl_log_send_arg6(EVENT, SL_LOG_CONFIG_LEVEL_DEBUG << 1 | EVENT_TYPE, ARG1,   \
                   ARG2, ARG3, ARG4, ARG5, ARG6)
#define SL_PRINT_ARG6_ERR(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6) \
  sl_log_send_arg6(EVENT, SL_LOG_CONFIG_LEVEL_ERROR << 1 | EVENT_TYPE, ARG1,  \
                   ARG2, ARG3, ARG4, ARG5, ARG6)
#define SL_PRINT_ARG6_CRASH(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6) \
  sl_log_send_arg6(EVENT, SL_LOG_CONFIG_LEVEL_CRASH << 1 | EVENT_TYPE, ARG1,  \
                   ARG2, ARG3, ARG4, ARG5, ARG6)
#define SL_PRINT_ARG6_WRN(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6) \
  sl_log_send_arg6(EVENT, SL_LOG_CONFIG_LEVEL_WARN << 1 | EVENT_TYPE, ARG1,    \
                   ARG2, ARG3, ARG4, ARG5, ARG6)
#define SL_PRINT_ARG6_INFO(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6) \
  sl_log_send_arg6(EVENT, SL_LOG_CONFIG_LEVEL_INFO << 1 | EVENT_TYPE, ARG1,    \
                   ARG2, ARG3, ARG4, ARG5, ARG6)
#endif

#if (SL_LOG_CONFIG_ARG >= 7)
#define SL_PRINT_ARG7_DBG(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7) \
  sl_log_send_arg7(EVENT, SL_LOG_CONFIG_LEVEL_DEBUG << 1 | EVENT_TYPE, ARG1,  \
                   ARG2, ARG3, ARG4, ARG5, ARG6, ARG7)
#define SL_PRINT_ARG7_ERR(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7) \
  sl_log_send_arg7(EVENT, SL_LOG_CONFIG_LEVEL_ERROR << 1 | EVENT_TYPE, ARG1,  \
                   ARG2, ARG3, ARG4, ARG5, ARG6, ARG7)
#define SL_PRINT_ARG7_CRASH(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7) \
  sl_log_send_arg7(EVENT, SL_LOG_CONFIG_LEVEL_CRASH << 1 | EVENT_TYPE, ARG1,  \
                   ARG2, ARG3, ARG4, ARG5, ARG6, ARG7)
#define SL_PRINT_ARG7_WRN(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7) \
  sl_log_send_arg7(EVENT, SL_LOG_CONFIG_LEVEL_WARN << 1 | EVENT_TYPE, ARG1,    \
                   ARG2, ARG3, ARG4, ARG5, ARG6, ARG7)
#define SL_PRINT_ARG7_INFO(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7) \
  sl_log_send_arg7(EVENT, SL_LOG_CONFIG_LEVEL_INFO << 1 | EVENT_TYPE, ARG1,   \
                   ARG2, ARG3, ARG4, ARG5, ARG6, ARG7)
#endif

#if (SL_LOG_CONFIG_ARG >= 8)
#define SL_PRINT_ARG8_DBG(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8) \
  sl_log_send_arg8(EVENT, SL_LOG_CONFIG_LEVEL_DEBUG << 1 | EVENT_TYPE, ARG1,  \
                   ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8)
#define SL_PRINT_ARG8_ERR(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8) \
  sl_log_send_arg8(EVENT, SL_LOG_CONFIG_LEVEL_ERROR << 1 | EVENT_TYPE, ARG1,  \
                   ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8)
#define SL_PRINT_ARG8_CRASH(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8) \
  sl_log_send_arg8(EVENT, SL_LOG_CONFIG_LEVEL_CRASH << 1 | EVENT_TYPE, ARG1,  \
                   ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8)
#define SL_PRINT_ARG8_WRN(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8) \
  sl_log_send_arg8(EVENT, SL_LOG_CONFIG_LEVEL_WARN << 1 | EVENT_TYPE, ARG1,    \
                   ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8)
#define SL_PRINT_ARG8_INFO(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8) \
  sl_log_send_arg8(EVENT, SL_LOG_CONFIG_LEVEL_INFO << 1 | EVENT_TYPE, ARG1,   \
                   ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8)
#endif

#if (SL_LOG_CONFIG_ARG >= 9)
#define SL_PRINT_ARG9_DBG(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9) \
  sl_log_send_arg9(EVENT, SL_LOG_CONFIG_LEVEL_DEBUG << 1 | EVENT_TYPE, ARG1,  \
                   ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9)
#define SL_PRINT_ARG9_ERR(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9) \
  sl_log_send_arg9(EVENT, SL_LOG_CONFIG_LEVEL_ERROR << 1 | EVENT_TYPE, ARG1,  \
                   ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9)
#define SL_PRINT_ARG9_CRASH(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9) \
  sl_log_send_arg9(EVENT, SL_LOG_CONFIG_LEVEL_CRASH << 1 | EVENT_TYPE, ARG1,  \
                   ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9)
#define SL_PRINT_ARG9_WRN(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9) \
  sl_log_send_arg9(EVENT, SL_LOG_CONFIG_LEVEL_WARN << 1 | EVENT_TYPE, ARG1,    \
                   ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9)
#define SL_PRINT_ARG9_INFO(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9) \
  sl_log_send_arg9(EVENT, SL_LOG_CONFIG_LEVEL_INFO << 1 | EVENT_TYPE, ARG1,   \
                   ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9)
#endif

#if (SL_LOG_CONFIG_ARG >= 10)
#define SL_PRINT_ARG10_DBG(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10) \
  sl_log_send_arg10(EVENT, SL_LOG_CONFIG_LEVEL_DEBUG << 1 | EVENT_TYPE, ARG1,  \
                    ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10)
#define SL_PRINT_ARG10_ERR(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10) \
  sl_log_send_arg10(EVENT, SL_LOG_CONFIG_LEVEL_ERROR << 1 | EVENT_TYPE, ARG1,  \
                    ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10)
#define SL_PRINT_ARG10_CRASH(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10) \
  sl_log_send_arg10(EVENT, SL_LOG_CONFIG_LEVEL_CRASH << 1 | EVENT_TYPE, ARG1,  \
                    ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10)
#define SL_PRINT_ARG10_WRN(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10) \
  sl_log_send_arg10(EVENT, SL_LOG_CONFIG_LEVEL_WARN << 1 | EVENT_TYPE, ARG1,    \
                    ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10)
#define SL_PRINT_ARG10_INFO(EVENT, EVENT_TYPE, ARG1, ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10) \
  sl_log_send_arg10(EVENT, SL_LOG_CONFIG_LEVEL_INFO << 1 | EVENT_TYPE, ARG1,   \
                    ARG2, ARG3, ARG4, ARG5, ARG6, ARG7, ARG8, ARG9, ARG10)
#endif

#endif /* !defined(SL_CATALOG_LOG_BACKEND_SYSTEMVIEW_PRESENT) */

/** @} (end addtogroup sl_log_active_macros) */


/**
 * @defgroup sl_log_level_checks Log Level Check Macros
 * @brief Macros for checking if a log level should be processed
 *
 * These macros provide efficient level checking to determine if a log
 * message should be processed based on the current log level configuration.
 *
 * @{
 */

/** @brief Check if debug level logging is enabled for the given level */
#define SL_LOG_LVL_DEBUG_CHECK(level) (level <= SL_LOG_CONFIG_LEVEL_DEBUG)

/** @brief Check if info level logging is enabled for the given level */
#define SL_LOG_LVL_INFO_CHECK(level) (level <= SL_LOG_CONFIG_LEVEL_INFO)

/** @brief Check if error level logging is enabled for the given level */
#define SL_LOG_LVL_ERROR_CHECK(level) (level <= SL_LOG_CONFIG_LEVEL_ERROR)

/** @brief Check if crash level logging is enabled for the given level */
#define SL_LOG_LVL_CRASH_CHECK(level) (level <= SL_LOG_CONFIG_LEVEL_CRASH)

/** @brief Check if warning level logging is enabled for the given level */
#define SL_LOG_LVL_WARN_CHECK(level) (level <= SL_LOG_CONFIG_LEVEL_WARN)

/** @} (end addtogroup sl_log_level_checks) */

/**
 * @defgroup sl_log_macro_helpers Macro Processing Helpers
 * @brief Helper macros for token concatenation and argument processing
 *
 * These macros provide the foundation for the variadic logging system,
 * enabling automatic selection of appropriate logging functions based
 * on argument count and generating unique identifiers.
 *
 * @{
 */

/* Token concatenation is provided by sl_common.h:
 *   _SL_CONCAT_2(a, b)       - concatenates without expanding macro arguments
 *   SL_CONCAT_PASTER_2(a, b) - expands macro arguments before concatenating
 */

/** @brief Generate unique name based on line number */
#define SLI_LOG_UNIQUE_NAME(base) SL_CONCAT_PASTER_2(base, SL_CONCAT_PASTER_2(__LINE__, 0))

/** @brief Implementation macro for counting variadic arguments (up to 10) */
#define SLI_LOG_COUNT_ARGS_IMPL(_0, _1, _2, _3, _4, _5, _6, _7, _8, _9, _10, N, ...) N

/** @brief Count the number of variadic arguments (up to 10) */
#define SLI_LOG_COUNT_ARGS(fmt, ...) SLI_LOG_COUNT_ARGS_IMPL(_, ##__VA_ARGS__, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0)

/** @brief Helper for choosing logging macro based on argument count */
#define SLI_LOG_MACRO_CHOOSER2(count) SL_CONCAT_PASTER_2(SL_PRINT_ARG, count##_)

/** @brief Macro dispatcher for selecting appropriate logging function */
#define SLI_LOG_VOID_MACRO_CHOOSER2(count) SL_CONCAT_PASTER_2(SL_PRINT_VOID_ARG, count##_)

/** @brief Macro dispatcher for selecting appropriate logging function */
#define SLI_LOG_VOID_MACRO_CHOOSER1(count) SLI_LOG_VOID_MACRO_CHOOSER2(count)

/** @brief Macro dispatcher for selecting appropriate logging function */
#define SLI_LOG_MACRO_CHOOSER1(count) SLI_LOG_MACRO_CHOOSER2(count)

/** @brief Chooser for SL_PRINT_EVENT_* -> SEGGER_SYSVIEW_RecordU32 / RecordU32xN */
#define SLI_LOG_EVENT_MACRO_CHOOSER2(count) SL_CONCAT_PASTER_2(SL_EVENT_PRINT_ARG, count##_)

/** @brief Chooser for SL_PRINT_EVENT_* -> SEGGER_SYSVIEW_RecordU32 / RecordU32xN */
#define SLI_LOG_EVENT_MACRO_CHOOSER1(count) SLI_LOG_EVENT_MACRO_CHOOSER2(count)

/** @} (end addtogroup sl_log_macro_helpers) */

/**
 * @defgroup sl_log_common_macros Common Logging Macros
 * @brief Core macros for printf-style and event-based logging
 *
 * These macros provide the foundation for both printf-style string logging
 * and numeric event-based logging with compile-time argument validation.
 *
 * @{
 */

/**
 * @brief Common printf-style logging macro
 *
 * Creates a static format string in the log section and calls the appropriate
 * logging function based on argument count. Includes compile-time validation
 * to ensure no more than SL_LOG_CONFIG_ARG arguments are provided.
 *
 * @param level Log level suffix (INFO, DBG, ERR, WRN, CRASH)
 * @param fmt Format string
 * @param ... Variable arguments (up to 10)
 */
#define sl_printf_common(level, fmt, ...)                                      \
  static const char SLI_LOG_UNIQUE_NAME(logstr_)[] SL_COMPACT_STRINGS_SECTION = fmt;               \
  _Static_assert(SLI_LOG_COUNT_ARGS(fmt, ##__VA_ARGS__) <= SL_LOG_CONFIG_ARG, "Too many arguments!");  \
  SL_CONCAT_PASTER_2(SLI_LOG_MACRO_CHOOSER1(SLI_LOG_COUNT_ARGS(fmt, ##__VA_ARGS__)), level)     \
  ((uintptr_t)SLI_LOG_UNIQUE_NAME(logstr_), 0, ##__VA_ARGS__)

/**
 * @brief Common event-based logging macro
 *
 * Logs a numeric event ID with optional arguments. Includes compile-time
 * validation to ensure no more than SL_LOG_CONFIG_ARG arguments are provided.
 *
 * @param level Log level suffix (INFO, DBG, ERR, WRN, CRASH)
 * @param event_id Numeric event identifier
 * @param ... Variable arguments (up to 10)
 */
#if defined(SL_CATALOG_LOG_BACKEND_SYSTEMVIEW_PRESENT)
#define sl_event_common(level, event_id, ...)                                  \
  _Static_assert(SLI_LOG_COUNT_ARGS(event_id, ##__VA_ARGS__) <= SL_LOG_CONFIG_ARG, "Too many arguments!");  \
  SL_CONCAT_PASTER_2(SLI_LOG_EVENT_MACRO_CHOOSER1(SLI_LOG_COUNT_ARGS(event_id, ##__VA_ARGS__)), level)     \
  (event_id, 1, ##__VA_ARGS__)
#else
#define sl_event_common(level, event_id, ...)                                  \
  _Static_assert(SLI_LOG_COUNT_ARGS(event_id, ##__VA_ARGS__) <= SL_LOG_CONFIG_ARG, "Too many arguments!");  \
  SL_CONCAT_PASTER_2(SLI_LOG_MACRO_CHOOSER1(SLI_LOG_COUNT_ARGS(event_id, ##__VA_ARGS__)), level)     \
  (event_id, 1, ##__VA_ARGS__)
#endif

/** @} (end addtogroup sl_log_common_macros) */

/***************************************************************************//**
 * @addtogroup assert ASSERT - Assert
 * @brief Enhanced assert/error checking module with detailed logging
 * @details
 * This implementation provides comprehensive assert handling with:
 * - File name, line number, and expression logging
 * - Debug session detection and breakpoint triggering
 * - Conditional debug asserts via SL_LOG_DEBUG_ASSERT_ENABLE flag
 *
 * Assert Macros:
 * - SL_LOG_CRASH_ASSERT: Always active, triggers assert handler
 * - SL_LOG_DEBUG_ASSERT: Active only when SL_LOG_DEBUG_ASSERT_ENABLE is defined
 * - assert: Core assert implementation with detailed logging
 * @{
 ******************************************************************************/

/***************************************************************************//**
 * @brief
 *    Core assert implementation with file, line, and expression logging
 * @details
 *    If the condition is false, constructs a detailed error string and
 *    passes it to sli_assert_implementation for handling.
 ******************************************************************************/
#define debug_assert(__e) \
    ((__e) \
        ? (void)0 \
        : sli_log_assert_implementation( \
            __FILE__ ":" SL_STRINGIFY(__LINE__) " - Assertion failed: " #__e) \
)


/***************************************************************************//**
* @brief
*    Crash assert - always enabled regardless of SL_LOG_DEBUG_ASSERT_ENABLE configuration
******************************************************************************/

#define SL_LOG_CRASH_ASSERT(condition) debug_assert(condition)

/***************************************************************************//**
* @brief
*    Debug assert - enabled only when SL_LOG_DEBUG_ASSERT_ENABLE is defined
* @details
*    In debug builds, maps to SL_LOG_CRASH_ASSERT for full error handling.
*    In release builds, this macro is disabled (no-op) to save code space.
******************************************************************************/

#if SL_LOG_DEBUG_ASSERT_ENABLE
#define SL_LOG_DEBUG_ASSERT(condition) SL_LOG_CRASH_ASSERT(condition) // If SL_LOG_DEBUG is non-zero, enable debug asserts
#else
#define SL_LOG_DEBUG_ASSERT(condition) ((void)0) // If SL_LOG_DEBUG is 0, compile out the assert (no-op)
#endif


/** @} (end addtogroup SL_DEBUG_ASSERT) */

#if (defined(LIBRARY_BUILD) || defined(SL_CATALOG_LOG_COMPONENT_PRESENT)) && (SL_LOG_CONFIG_LEVEL_COMPILE_TIME != SL_LOG_CONFIG_LEVEL_NONE)

/**
 * @defgroup sl_log_printf_api Printf-Style Logging API
 * @brief High-level printf-style logging macros with level filtering
 *
 * These macros provide the main user-facing API for printf-style logging.
 * They include both compile-time and runtime level filtering for optimal
 * performance and flexibility.
 *
 * @note When @c SL_CATALOG_LOG_FORMATTED_OUTPUT_PRESENT is defined,
 *       SL_PRINT_STRING_INFO/DEBUG/WARN/ERROR/CRASH are redirected to the
 *       SL_PRINT_FMT_* path (including SL_PRINT_FMT_CRASH) and
 *       SL_PRINT_EVENT_* become no-ops. Early logging (before
 *       @ref sl_log_init_stage2() completes) is not supported in this
 *       mode: messages emitted before stage 2 are discarded rather than
 *       buffered.
 *
 * @note The SL_PRINT_FMT_* path (and therefore the redirect above) is
 *       implemented only by the @c log_backend_iostream_formatted backend.
 *       In compact-output builds, @c log_none, or builds with no backend
 *       installed, @ref sl_log_vprint_target_ex resolves to the weak no-op
 *       in sl_log_weak.c — direct SL_PRINT_FMT_* calls in those modes are
 *       intentionally silent. SL_PRINT_STRING_* without the formatted
 *       catalog still flows through the legacy ring-buffer path
 *       (@c sl_printf_common) and is unaffected.
 *
 * @{
 */

/**
 * @brief Print info-level message with printf-style formatting
 *
 * Logs a message at INFO level if either compile-time or runtime
 * configuration allows info-level logging.
 *
 * @param fmt Printf-style format string
 * @param ... Variable arguments for format string (up to 10)
 */
#if defined(SL_CATALOG_LOG_FORMATTED_OUTPUT_PRESENT)
#define SL_PRINT_STRING_INFO(fmt, ...) SL_PRINT_FMT_INFO(fmt, ##__VA_ARGS__)
#else
#define SL_PRINT_STRING_INFO(fmt, ...) do{sl_printf_common(INFO, fmt, ##__VA_ARGS__); }while(0)
#endif


/**
 * @brief Print debug-level message with printf-style formatting
 *
 * Logs a message at DEBUG level if either compile-time or runtime
 * configuration allows debug-level logging.
 *
 * @param fmt Printf-style format string
 * @param ... Variable arguments for format string (up to 10)
 */
#if defined(SL_CATALOG_LOG_FORMATTED_OUTPUT_PRESENT)
#define SL_PRINT_STRING_DEBUG(fmt, ...) SL_PRINT_FMT_DEBUG(fmt, ##__VA_ARGS__)
#else
#define SL_PRINT_STRING_DEBUG(fmt, ...) do{sl_printf_common(DBG, fmt, ##__VA_ARGS__); }while(0)
#endif


/**
 * @brief Print warning-level message with printf-style formatting
 *
 * Logs a message at WARNING level if either compile-time or runtime
 * configuration allows warning-level logging.
 *
 * @param fmt Printf-style format string
 * @param ... Variable arguments for format string (up to 10)
 */

#if defined(SL_CATALOG_LOG_FORMATTED_OUTPUT_PRESENT)
#define SL_PRINT_STRING_WARN(fmt, ...) SL_PRINT_FMT_WARN(fmt, ##__VA_ARGS__)
#else
#define SL_PRINT_STRING_WARN(fmt, ...) do{sl_printf_common(WRN, fmt, ##__VA_ARGS__); }while(0)
#endif


/**
 * @brief Print error-level message with printf-style formatting
 *
 * Logs a message at ERROR level if either compile-time or runtime
 * configuration allows error-level logging.
 *
 * @param fmt Printf-style format string
 * @param ... Variable arguments for format string (up to 10)
 */
#if defined(SL_CATALOG_LOG_FORMATTED_OUTPUT_PRESENT)
#define SL_PRINT_STRING_ERROR(fmt, ...) SL_PRINT_FMT_ERROR(fmt, ##__VA_ARGS__)
#else
#define SL_PRINT_STRING_ERROR(fmt, ...) do{sl_printf_common(ERR, fmt, ##__VA_ARGS__); }while(0)
#endif

/**
 * @brief Print crash-level message with printf-style formatting
 *
 * Logs a message at CRASH level if either compile-time or runtime
 * configuration allows crash-level logging.
 *
 * @param fmt Printf-style format string
 * @param ... Variable arguments for format string (up to 10)
 */
#if defined(SL_CATALOG_LOG_FORMATTED_OUTPUT_PRESENT)
#define SL_PRINT_STRING_CRASH(fmt, ...) SL_PRINT_FMT_CRASH(fmt, ##__VA_ARGS__)
#elif (SL_LOG_CONFIG_LEVEL_COMPILE_TIME == SL_LOG_CONFIG_LEVEL_NONE)
#define SL_PRINT_STRING_CRASH(fmt, ...) do{ }while(0)
#else
#define SL_PRINT_STRING_CRASH(fmt, ...) do{sl_printf_common(CRASH, fmt, ##__VA_ARGS__); }while(0)
#endif

/** @} (end addtogroup sl_log_printf_api) */

/**
 * @defgroup sl_log_event_api Event-Based Logging API
 * @brief High-level event-based logging macros with level filtering
 *
 * These macros provide the main user-facing API for event-based logging
 * using numeric event IDs. They include both compile-time and runtime
 * level filtering for optimal performance and flexibility.
 *
 * @{
 */

/**
 * @brief Log info-level event with optional arguments
 *
 * Logs an event at INFO level if either compile-time or runtime
 * configuration allows info-level logging.
 *
 * @param event_id Numeric event identifier
 * @param ... Variable arguments for the event (up to 10)
 */
#if defined(SL_CATALOG_LOG_FORMATTED_OUTPUT_PRESENT)
#define SL_PRINT_EVENT_INFO(event_id, ...) do { (void)sizeof(event_id); } while(0)
#else
#define SL_PRINT_EVENT_INFO(event_id, ...) do{sl_event_common(INFO, event_id, ##__VA_ARGS__); }while(0)
#endif

/**
 * @brief Log debug-level event with optional arguments
 *
 * Logs an event at DEBUG level if either compile-time or runtime
 * configuration allows debug-level logging.
 *
 * @param event_id Numeric event identifier
 * @param ... Variable arguments for the event (up to 10)
 */
#if defined(SL_CATALOG_LOG_FORMATTED_OUTPUT_PRESENT)
#define SL_PRINT_EVENT_DEBUG(event_id, ...) do { (void)sizeof(event_id); } while(0)
#else
#define SL_PRINT_EVENT_DEBUG(event_id, ...) do{sl_event_common(DBG, event_id, ##__VA_ARGS__); }while(0)
#endif
/**
 * @brief Log warning-level event with optional arguments
 *
 * Logs an event at WARNING level if either compile-time or runtime
 * configuration allows warning-level logging.
 *
 * @param event_id Numeric event identifier
 * @param ... Variable arguments for the event (up to 10)
 */
#if defined(SL_CATALOG_LOG_FORMATTED_OUTPUT_PRESENT)
#define SL_PRINT_EVENT_WARN(event_id, ...) do { (void)sizeof(event_id); } while(0)
#else
#define SL_PRINT_EVENT_WARN(event_id, ...) do{sl_event_common(WRN, event_id, ##__VA_ARGS__); }while(0)
#endif
/**
 * @brief Log error-level event with optional arguments
 *
 * Logs an event at ERROR level if either compile-time or runtime
 * configuration allows error-level logging.
 *
 * @param event_id Numeric event identifier
 * @param ... Variable arguments for the event (up to 10)
 */

#if defined(SL_CATALOG_LOG_FORMATTED_OUTPUT_PRESENT)
#define SL_PRINT_EVENT_ERROR(event_id, ...) do { (void)sizeof(event_id); } while(0)
#else
#define SL_PRINT_EVENT_ERROR(event_id, ...) do{sl_event_common(ERR, event_id, ##__VA_ARGS__); }while(0)
#endif

/**
 * @brief Log crash-level event with optional arguments
 *
 * Logs an event at CRASH level if either compile-time or runtime
 * configuration allows crash-level logging.
 *
 * @param event_id Numeric event identifier
 * @param ... Variable arguments for the event (up to 10)
 */
#if defined(SL_CATALOG_LOG_FORMATTED_OUTPUT_PRESENT)
#define SL_PRINT_EVENT_CRASH(event_id, ...) do { (void)sizeof(event_id); } while(0)
#elif (SL_LOG_CONFIG_LEVEL_COMPILE_TIME == SL_LOG_CONFIG_LEVEL_NONE)
#define SL_PRINT_EVENT_CRASH(event_id, ...) do{ }while(0)
#else
#define SL_PRINT_EVENT_CRASH(event_id, ...) do{sl_event_common(CRASH, event_id, ##__VA_ARGS__); }while(0)
#endif

/** @} (end addtogroup sl_log_event_api) */

/**
 * @defgroup sl_log_fmt_api Target-Side Formatted Logging API
 * @brief printf-style logging that formats on the target before transmission.
 *
 * Unlike SL_PRINT_STRING_*, which encodes only the format-string pointer plus
 * numeric arguments (the host renders the message from a description file),
 * the SL_PRINT_FMT_* macros call @ref SL_LOG_PRINT_TARGET_EX so the format
 * string is fully expanded on target and the resulting text is forwarded to
 * the active backend:
 *
 *   - SystemView backend: emitted as a SystemView text packet via
 *     SEGGER_SYSVIEW_VPrintfTargetEx().
 *   - I/O Stream **formatted** backend (component
 *     @c log_backend_iostream_formatted): the format string is rendered on
 *     target with vsnprintf() and emitted to the recommended console
 *     iostream as `[TIMESTAMP] [CC] <text>` (each prefix optional, see
 *     sl_log_formatted_iostream_config.h). No trailing CR/LF is appended.
 *   - All other backends (I/O Stream **compact**, @c log_none, or no
 *     backend installed): no strong implementation of
 *     @ref sl_log_vprint_target_ex is linked, so calls fall through to the
 *     weak no-op in sl_log_weak.c and the message is silently discarded.
 *
 * @warning SL_PRINT_FMT_* (and the SL_PRINT_STRING_* redirects below) only
 *          render under the formatted-output backend. They are intentionally
 *          inert in compact-output builds; do not rely on them to produce
 *          output there.
 *
 * Use these when:
 *   - A host-side description / lookup file for the format strings is not
 *     available, or
 *   - The format string is not a string literal pointer (e.g. composed at
 *     runtime), or
 *   - You want the same call site to work across all log backends without
 *     extra glue.
 *
 * Trade-off: higher CPU and bandwidth than SL_PRINT_STRING_*.
 *
 * Each macro is compile-time gated by SL_LOG_CONFIG_LEVEL_COMPILE_TIME
 * (severities above the build-time level collapse to a (void)sizeof() no-op),
 * consistent with SL_PRINT_STRING_* and SL_PRINT_EVENT_*.
 * At runtime, @ref SL_LOG_PRINT_TARGET_EX is invoked only when the macro's
 * level passes @ref sl_log_get_loglevel() (same ordering rule as @c sl_log_send_*)
 * and when @c sli_log_init_stage2_done is true (set when @ref sl_log_init_stage2()
 * finishes). Unlike @c sl_log_send_*, this path does not buffer early output
 * in the ring buffer, so nothing is emitted before stage 2 completes.
 * If SL_LOG_CONFIG_LEVEL_COMPILE_TIME is SL_LOG_CONFIG_LEVEL_NONE, all five
 * macros (INFO/DEBUG/WARN/ERROR/CRASH) are stripped entirely at compile time.
 *
 * @{
 */
#if (SL_LOG_CONFIG_LEVEL_COMPILE_TIME != SL_LOG_CONFIG_LEVEL_NONE)

/* Outer #if on each SL_PRINT_FMT_*: compile-time strip (no code). Inner if:
 * runtime threshold via sl_log_set_loglevel / sl_log_get_loglevel (same rule
 * as sl_log_send_*) and @c sli_log_init_stage2_done (backend ready). */

/** @brief Print info-level message via the active backend's target-side printf. */
#if (SL_LOG_CONFIG_LEVEL_COMPILE_TIME <= SL_LOG_CONFIG_LEVEL_INFO)
#define SL_PRINT_FMT_INFO(fmt, ...)                                            \
  do {                                                                         \
    if ((sl_log_level_t)SL_LOG_CONFIG_LEVEL_INFO >= sl_log_get_loglevel()      \
        && sli_log_init_stage2_done) {                                          \
      SL_LOG_PRINT_TARGET_EX(SL_LOG_PRINT_OPT_LOG, (fmt), ##__VA_ARGS__);      \
    }                                                                          \
  } while (0)
#else
#define SL_PRINT_FMT_INFO(fmt, ...)  do { sl_printf_common(INFO, fmt, ##__VA_ARGS__); } while (0)
#endif

/** @brief Print debug-level message via the active backend's target-side printf. */
#if (SL_LOG_CONFIG_LEVEL_COMPILE_TIME <= SL_LOG_CONFIG_LEVEL_DEBUG)
#define SL_PRINT_FMT_DEBUG(fmt, ...)                                           \
  do {                                                                         \
    if ((sl_log_level_t)SL_LOG_CONFIG_LEVEL_DEBUG >= sl_log_get_loglevel()     \
        && sli_log_init_stage2_done) {                                          \
      SL_LOG_PRINT_TARGET_EX(SL_LOG_PRINT_OPT_LOG, (fmt), ##__VA_ARGS__);      \
    }                                                                          \
  } while (0)
#else
#define SL_PRINT_FMT_DEBUG(fmt, ...) do { sl_printf_common(DBG, fmt, ##__VA_ARGS__); } while (0)
#endif

/** @brief Print warning-level message via the active backend's target-side printf. */
#if (SL_LOG_CONFIG_LEVEL_COMPILE_TIME <= SL_LOG_CONFIG_LEVEL_WARN)
#define SL_PRINT_FMT_WARN(fmt, ...)                                            \
  do {                                                                         \
    if ((sl_log_level_t)SL_LOG_CONFIG_LEVEL_WARN >= sl_log_get_loglevel()      \
        && sli_log_init_stage2_done) {                                          \
      SL_LOG_PRINT_TARGET_EX(SL_LOG_PRINT_OPT_WARN, (fmt), ##__VA_ARGS__);     \
    }                                                                          \
  } while (0)
#else
#define SL_PRINT_FMT_WARN(fmt, ...)  do { sl_printf_common(WRN, fmt, ##__VA_ARGS__); } while (0)
#endif

/** @brief Print error-level message via the active backend's target-side printf. */
#if (SL_LOG_CONFIG_LEVEL_COMPILE_TIME <= SL_LOG_CONFIG_LEVEL_ERROR)
#define SL_PRINT_FMT_ERROR(fmt, ...)                                           \
  do {                                                                         \
    if ((sl_log_level_t)SL_LOG_CONFIG_LEVEL_ERROR >= sl_log_get_loglevel()      \
        && sli_log_init_stage2_done) {                                          \
      SL_LOG_PRINT_TARGET_EX(SL_LOG_PRINT_OPT_ERROR, (fmt), ##__VA_ARGS__);    \
    }                                                                          \
  } while (0)
#else
#define SL_PRINT_FMT_ERROR(fmt, ...) do { sl_printf_common(ERR, fmt, ##__VA_ARGS__); } while (0)
#endif

/** @brief Print crash-level message via the active backend's target-side printf.
 *
 * CRASH is the highest severity, so any compile-time level other than NONE
 * accepts it. There is no dedicated SL_LOG_PRINT_OPT_CRASH option, so the
 * call is forwarded with SL_LOG_PRINT_OPT_ERROR (the formatted backend
 * ignores the level field; only the payload is rendered). */
#define SL_PRINT_FMT_CRASH(fmt, ...)                                           \
  do {                                                                         \
    if ((sl_log_level_t)SL_LOG_CONFIG_LEVEL_CRASH >= sl_log_get_loglevel()      \
        && sli_log_init_stage2_done) {                                          \
      SL_LOG_PRINT_TARGET_EX(SL_LOG_PRINT_OPT_ERROR, (fmt), ##__VA_ARGS__);    \
    }                                                                          \
  } while (0)

#else /* compile-time level == NONE */

#define SL_PRINT_FMT_INFO(fmt, ...)  do { (void)sizeof(fmt); } while (0)
#define SL_PRINT_FMT_DEBUG(fmt, ...) do { (void)sizeof(fmt); } while (0)
#define SL_PRINT_FMT_WARN(fmt, ...)  do { (void)sizeof(fmt); } while (0)
#define SL_PRINT_FMT_ERROR(fmt, ...) do { (void)sizeof(fmt); } while (0)
#define SL_PRINT_FMT_CRASH(fmt, ...) do { (void)sizeof(fmt); } while (0)

#endif

/** @} (end addtogroup sl_log_fmt_api) */


#else // LIBRARY_BUILD
/**
 * @defgroup sl_log_common_macros Common Logging Macros
 * @brief Core macros for printf-style and event-based logging
 *
 * These macros provide the foundation for both printf-style string logging
 * and numeric event-based logging with compile-time argument validation.
 *
 * @{
 */

/**
 * @brief Common printf-style logging macro
 *
 * This apis discards the string provided by the user and and send empty string address magic word
 *
 * @param level Log level suffix (INFO, DBG, ERR, WRN)
 * @param fmt Format string
 * @param ... Variable arguments (up to 10)
 */

#define sl_log_common_void(level, event_id, ...)                                  \
 _Static_assert(SLI_LOG_COUNT_ARGS(event_id, ##__VA_ARGS__) <= SL_LOG_CONFIG_ARG, "Too many arguments!");  \
  SL_CONCAT_PASTER_2(SLI_LOG_VOID_MACRO_CHOOSER1(SLI_LOG_COUNT_ARGS(event_id, ##__VA_ARGS__)), level)     \
  (event_id, 1, ##__VA_ARGS__)

/* Compile-time–controlled PRINTF-style macros */


#define SL_PRINT_STRING_INFO(fmt, ...)   do { sl_log_common_void(INFO, fmt, ##__VA_ARGS__); } while(0)
#define SL_PRINT_STRING_DEBUG(fmt, ...)  do { sl_log_common_void(DBG, fmt, ##__VA_ARGS__); } while(0)
#define SL_PRINT_STRING_WARN(fmt, ...)   do { sl_log_common_void(WRN, fmt, ##__VA_ARGS__); } while(0)
#define SL_PRINT_STRING_ERROR(fmt, ...)  do { sl_log_common_void(ERR, fmt, ##__VA_ARGS__); } while(0)
#define SL_PRINT_STRING_CRASH(fmt, ...)  do { sl_log_common_void(CRASH, fmt, ##__VA_ARGS__); } while(0)

/* Compile-time–controlled EVENT-style macros */
#define SL_PRINT_EVENT_INFO(event_id, ...)   do { sl_log_common_void(INFO, event_id, ##__VA_ARGS__); } while(0)
#define SL_PRINT_EVENT_DEBUG(event_id, ...)  do { sl_log_common_void(DBG, event_id, ##__VA_ARGS__); } while(0)
#define SL_PRINT_EVENT_WARN(event_id, ...)   do { sl_log_common_void(WRN, event_id, ##__VA_ARGS__); } while(0)
#define SL_PRINT_EVENT_ERROR(event_id, ...)  do { sl_log_common_void(ERR, event_id, ##__VA_ARGS__); } while(0)
#define SL_PRINT_EVENT_CRASH(event_id, ...)  do { sl_log_common_void(CRASH, event_id, ##__VA_ARGS__); } while(0)

/* In LIBRARY_BUILD, SL_PRINT_FMT_* expand to no-ops but link the
 * to SL_LOG_PRINT_TARGET_EX implementation. */
#define SL_PRINT_FMT_INFO(fmt, ...)  do { (void)sizeof(fmt); } while (0)
#define SL_PRINT_FMT_DEBUG(fmt, ...) do { (void)sizeof(fmt); } while (0)
#define SL_PRINT_FMT_WARN(fmt, ...)  do { (void)sizeof(fmt); } while (0)
#define SL_PRINT_FMT_ERROR(fmt, ...) do { (void)sizeof(fmt); } while (0)
#define SL_PRINT_FMT_CRASH(fmt, ...) do { (void)sizeof(fmt); } while (0)

#endif // LIBRARY_BUILD

#ifdef __cplusplus
}
#endif

#endif // SL_LOG_HELPER_H
