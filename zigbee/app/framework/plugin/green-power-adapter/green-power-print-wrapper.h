/***************************************************************************//**
 * @file
 * @brief
 *******************************************************************************
 * # License
 * <b>Copyright 2022 Silicon Laboratories Inc. www.silabs.com</b>
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

#ifndef _SILABS_GREEN_POWER_PRINT_WRAPPER_H_
#define _SILABS_GREEN_POWER_PRINT_WRAPPER_H_

#include "zap-command.h"
#include "zap-id.h"
#include "zap-type.h"
#include "zap-enabled-incoming-commands.h"
#if !defined SL_CATALOG_ZIGBEE_ZCL_FRAMEWORK_CORE_PRESENT
#define SL_CATALOG_ZIGBEE_ZCL_FRAMEWORK_CORE_PRESENT
#include "zap-command-structs.h"
#undef SL_CATALOG_ZIGBEE_ZCL_FRAMEWORK_CORE_PRESENT
#endif

#include "sl_service_function.h"

#ifdef SL_COMPONENT_CATALOG_PRESENT
#ifdef SL_COMPONENT_CATALOG_PRESENT
#include "sl_component_catalog.h"
#endif

#ifdef SL_CATALOG_ZIGBEE_ZCL_FRAMEWORK_CORE_PRESENT
#include "zcl-framework-core-config.h"
#endif // SL_CATALOG_ZIGBEE_ZCL_FRAMEWORK_CORE_PRESENT

#include "green-power-adapter-config.h"
#endif // SL_COMPONENT_CATALOG_PRESENT

/***************************************************************************
* Print stub functions
* Customer should define these in their own application code
***************************************************************************/

/* When af.h has already included zcl-debug-print.h, its include guard is set. The #undef
 * block below would strip sl_zigbee_af_* macros and the delegated #include would then be
 * a no-op, leaving e.g. sl_zigbee_af_green_power_cluster_print undefined. Skip the #undef
 * preamble only in that delegate configuration (non-custom print + same zcl visibility as af.h). */
#if !(defined(SLI_ZIGBEE_APP_FRAMEWORK_UTIL_ZCL_DEBUG_PRINT_H) \
      && (SL_ZIGBEE_AF_PLUGIN_GREEN_POWER_ADAPTER_USE_CUSTOM_PRINT_SYSTEM == 0) \
      && defined(SL_CATALOG_ZIGBEE_DEBUG_PRINT_PRESENT) \
      && (defined(SL_CATALOG_ZIGBEE_ZCL_FRAMEWORK_CORE_PRESENT) \
          || (defined(SL_ZIGBEE_AF_NCP) && defined(SL_CATALOG_ZIGBEE_SIMULATION_PRESENT))))

#define SL_ZIGBEE_AF_PRINT_CORE 0x0001

#undef sl_zigbee_af_core_print

#if !defined(SL_CATALOG_ZIGBEE_DEBUG_PRINT_PRESENT)
#undef sl_zigbee_af_print_big_endian_eui64
#endif // !SL_CATALOG_ZIGBEE_DEBUG_PRINT_PRESENT

#undef sl_zigbee_af_core_println
#undef sl_zigbee_af_cli_print
#undef sl_zigbee_af_cli_println
#undef sl_zigbee_af_green_power_cluster_print
#undef sl_zigbee_af_green_power_cluster_println
#undef sl_zigbee_af_green_power_cluster_print_buffer
#undef sl_zigbee_af_green_power_cluster_print_string
#undef sl_zigbee_af_debug_print
#undef sl_zigbee_af_debug_println
#undef sl_zigbee_af_zdo_print
#undef sl_zigbee_af_attributes_print
#undef sl_zigbee_af_service_discovery_print

#undef sl_zigbee_af_print
#undef sl_zigbee_af_app_println
#undef sl_zigbee_af_app_print
#undef sl_zigbee_af_attributes_print_buffer
#undef sl_zigbee_af_app_print_buffer
#undef sl_zigbee_af_debug_print_buffer
#undef sl_zigbee_af_print_buffer
#undef sl_zigbee_af_debug_flush
#define sl_zigbee_af_debug_flush()

#undef sl_zigbee_af_attributes_println
#undef sl_zigbee_af_app_flush
#define sl_zigbee_af_app_flush()

#undef sl_zigbee_af_cli_flush
#define sl_zigbee_af_cli_flush()

#undef sl_zigbee_af_ota_bootload_cluster_println
#undef sl_zigbee_af_zdo_println
#undef sl_zigbee_af_service_discovery_println
#undef sl_zigbee_af_println
#undef sl_zigbee_af_core_flush
#define sl_zigbee_af_core_flush()

#undef sl_zigbee_af_attributes_flush
#define sl_zigbee_af_attributes_flush()

#undef sl_zigbee_af_app_debug_exec
#define sl_zigbee_af_app_debug_exec(x) if ( true ) { x; }

#endif /* skipped #undef preamble when zcl-debug-print.h already included for delegate path */

extern uint16_t sl_zigbee_af_print_active_area;

#if (SL_ZIGBEE_AF_PLUGIN_GREEN_POWER_ADAPTER_USE_CUSTOM_PRINT_SYSTEM == 1)
// Using custom print system - this is the default behavior
// Customers are expected to define these wrapper functions in their own application code
#define sl_zigbee_af_core_print(...) sl_zigbee_af_core_print_wrapper(__VA_ARGS__)
#define sl_zigbee_af_print_big_endian_eui64(...) sl_zigbee_af_print_big_endian_eui64_wrapper(__VA_ARGS__)
#define sl_zigbee_af_core_println(...) sl_zigbee_af_core_println_wrapper(__VA_ARGS__)
#define sl_zigbee_af_cli_print(...) sl_zigbee_af_cli_print_wrapper(__VA_ARGS__)
#define sl_zigbee_af_cli_println(...) sl_zigbee_af_cli_println_wrapper(__VA_ARGS__)
#define sl_zigbee_af_green_power_cluster_print(...) sl_zigbee_af_green_power_cluster_print_wrapper(__VA_ARGS__)
#define sl_zigbee_af_green_power_cluster_println(...) sl_zigbee_af_green_power_cluster_println_wrapper(__VA_ARGS__)
#define sl_zigbee_af_green_power_cluster_print_buffer(buffer, len, withSpace) sl_zigbee_af_green_power_cluster_print_buffer_wrapper(buffer, len, withSpace)
#define sl_zigbee_af_green_power_cluster_print_string(buffer) sl_zigbee_af_green_power_cluster_print_string_wrapper(buffer)
#define sl_zigbee_af_debug_print(...) sl_zigbee_af_debug_print_wrapper(__VA_ARGS__)
#define sl_zigbee_af_debug_println(...) sl_zigbee_af_debug_println_wrapper(__VA_ARGS__)
#define sl_zigbee_af_zdo_print(...) sl_zigbee_af_print(0x00, __VA_ARGS__)
#define sl_zigbee_af_attributes_print(...) sl_zigbee_af_print(0x00, __VA_ARGS__)
#define sl_zigbee_af_service_discovery_print(...) sl_zigbee_af_print(0x00, __VA_ARGS__)
#define sl_zigbee_af_app_println(...) sl_zigbee_af_app_println_wrapper(__VA_ARGS__)
#define sl_zigbee_af_app_print(...) sl_zigbee_af_app_print_wrapper(__VA_ARGS__)
#define sl_zigbee_af_attributes_print_buffer(buffer, len, withSpace) sl_zigbee_af_print_buffer(0x00, (buffer), (len), (withSpace))
#define sl_zigbee_af_app_print_buffer(buffer, len, withSpace)   sl_zigbee_af_print_buffer(0x00, (buffer), (len), (withSpace))
#define sl_zigbee_af_debug_print_buffer(buffer, len, withSpace) sl_zigbee_af_print_buffer(0x00, (buffer), (len), (withSpace))
#define sl_zigbee_af_print_buffer(...) sl_zigbee_af_print_buffer_wrapper(__VA_ARGS__)
#define sl_zigbee_af_attributes_println(...) sl_zigbee_af_println(0x00, __VA_ARGS__)
#define sl_zigbee_af_ota_bootload_cluster_println(...) sl_zigbee_af_println(0x00, __VA_ARGS__)
#define sl_zigbee_af_zdo_println(...) sl_zigbee_af_println(0x00, __VA_ARGS__)
#define sl_zigbee_af_service_discovery_println(...) sl_zigbee_af_println(0x00, __VA_ARGS__)
#define sl_zigbee_af_print(...) sl_zigbee_af_print_wrapper(__VA_ARGS__)
#define sl_zigbee_af_println(...) sl_zigbee_af_println_wrapper(__VA_ARGS__)
/* Framework code uses warn/error macros from zcl-debug-print.h; map them here when
 * only the Green Power adapter print path is used (no ZCL framework core). */
#define sl_zigbee_af_app_warn(...) sl_zigbee_af_app_print_wrapper(__VA_ARGS__)
#define sl_zigbee_af_app_warnln(...) sl_zigbee_af_app_println_wrapper(__VA_ARGS__)
#define sl_zigbee_af_app_error(...) sl_zigbee_af_app_print_wrapper(__VA_ARGS__)
#define sl_zigbee_af_app_errorln(...) sl_zigbee_af_app_println_wrapper(__VA_ARGS__)
#define sl_zigbee_af_core_warn(...) sl_zigbee_af_core_print_wrapper(__VA_ARGS__)
#define sl_zigbee_af_core_warnln(...) sl_zigbee_af_core_println_wrapper(__VA_ARGS__)
#define sl_zigbee_af_core_error(...) sl_zigbee_af_core_print_wrapper(__VA_ARGS__)
#define sl_zigbee_af_core_errorln(...) sl_zigbee_af_core_println_wrapper(__VA_ARGS__)
void sl_zigbee_af_print_wrapper(uint16_t area, const char * formatString, ...);
#if !defined(SL_CATALOG_ZIGBEE_DEBUG_PRINT_PRESENT)
void sl_zigbee_af_print_big_endian_eui64_wrapper(uint8_t * eui, ...);
#endif // !SL_CATALOG_ZIGBEE_DEBUG_PRINT_PRESENT
void sl_zigbee_af_print_buffer_wrapper(uint16_t area, const uint8_t *buffer, uint16_t bufferLen, bool withSpace);
void sl_zigbee_af_print_string_wrapper(uint16_t area, const uint8_t *buffer);
void sl_zigbee_af_core_print_wrapper(const char * formatString, ...);
void sl_zigbee_af_core_println_wrapper(const char * formatString, ...);
void sl_zigbee_af_cli_print_wrapper(const char * formatString, ...);
void sl_zigbee_af_cli_println_wrapper(const char * formatString, ...);
void sl_zigbee_af_app_println_wrapper(const char * formatString, ...);
void sl_zigbee_af_app_print_wrapper(const char * formatString, ...);
void sl_zigbee_af_debug_print_wrapper(const char * formatString, ...);
void sl_zigbee_af_debug_println_wrapper(const char * formatString, ...);
void sl_zigbee_af_green_power_cluster_print_wrapper(const char * formatString, ...);
void sl_zigbee_af_green_power_cluster_println_wrapper(const char * formatString, ...);
void sl_zigbee_af_green_power_cluster_print_buffer_wrapper(const uint8_t *buffer, uint16_t bufferLen, bool withSpace);
void sl_zigbee_af_green_power_cluster_print_string_wrapper(const uint8_t *buffer);
void sl_zigbee_af_debug_flush_wrapper(void);
void sl_zigbee_af_println_wrapper(uint16_t area, const char * formatString, ...);
#else // SL_ZIGBEE_AF_PLUGIN_GREEN_POWER_ADAPTER_USE_CUSTOM_PRINT_SYSTEM == 1
// For testing purposes, we can add zigbee debug print components to the project
// and set SL_ZIGBEE_AF_PLUGIN_GREEN_POWER_ADAPTER_USE_CUSTOM_PRINT_SYSTEM to 0
// We need to redefine af-print macros to use the zigbee debug print ones
#ifdef SL_CATALOG_ZIGBEE_DEBUG_PRINT_PRESENT
// Same visibility as af.h: zcl-debug-print.h is the canonical macro layer when the ZCL
// framework core is present, or on NCP simulation (see af.h). Include it here instead of
// duplicating sl_zigbee_af_* mappings (avoids macro redefinition vs green-power-adapter).
#if (defined(SL_CATALOG_ZIGBEE_ZCL_FRAMEWORK_CORE_PRESENT) \
  || (defined(SL_ZIGBEE_AF_NCP) && defined(SL_CATALOG_ZIGBEE_SIMULATION_PRESENT)))
#include "app/framework/util/zcl-debug-print.h"
#else // !(ZCL framework core || (NCP && simulation))
#include "sl_zigbee_debug_print.h"
#define sl_zigbee_af_core_print(...) sl_zigbee_core_debug_print(__VA_ARGS__)
#define sl_zigbee_af_print_big_endian_eui64(...) sl_zigbee_core_debug_print_string(__VA_ARGS__)
#define sl_zigbee_af_core_println(...) sl_zigbee_core_debug_println(__VA_ARGS__)
#define sl_zigbee_af_cli_print(...) sl_zigbee_core_debug_print(__VA_ARGS__)
#define sl_zigbee_af_cli_println(...) sl_zigbee_core_debug_println(__VA_ARGS__)
#define sl_zigbee_af_green_power_cluster_print(...) sl_zigbee_core_debug_print(__VA_ARGS__)
#define sl_zigbee_af_green_power_cluster_println(...) sl_zigbee_core_debug_println(__VA_ARGS__)
#define sl_zigbee_af_green_power_cluster_print_buffer(buffer, len, withSpace) sl_zigbee_core_debug_print_buffer(buffer, len, withSpace)
#define sl_zigbee_af_green_power_cluster_print_string(buffer) sl_zigbee_core_debug_print_string(buffer)
#define sl_zigbee_af_debug_print(...) sl_zigbee_core_debug_print(__VA_ARGS__)
#define sl_zigbee_af_debug_println(...) sl_zigbee_core_debug_println(__VA_ARGS__)
#define sl_zigbee_af_zdo_print(...) sl_zigbee_core_debug_print( __VA_ARGS__)
#define sl_zigbee_af_attributes_print(...) sl_zigbee_core_debug_print(__VA_ARGS__)
#define sl_zigbee_af_service_discovery_print(...) sl_zigbee_core_debug_print(__VA_ARGS__)
#define sl_zigbee_af_app_println(...) sl_zigbee_core_debug_println(__VA_ARGS__)
#define sl_zigbee_af_app_print(...) sl_zigbee_core_debug_print(__VA_ARGS__)
#define sl_zigbee_af_attributes_print_buffer(buffer, len, withSpace) sl_zigbee_core_debug_print_buffer((buffer), (len), (withSpace))
#define sl_zigbee_af_app_print_buffer(buffer, len, withSpace)   sl_zigbee_core_debug_print_buffer((buffer), (len), (withSpace))
#define sl_zigbee_af_debug_print_buffer(buffer, len, withSpace) sl_zigbee_core_debug_print_buffer((buffer), (len), (withSpace))
#define sl_zigbee_af_print_buffer(area, buffer, bufferLen, withSpace) sl_zigbee_core_debug_print_buffer(buffer, bufferLen, withSpace)
#define sl_zigbee_af_attributes_println(...) sl_zigbee_core_debug_println(__VA_ARGS__)
#define sl_zigbee_af_ota_bootload_cluster_println(...) sl_zigbee_core_debug_println(__VA_ARGS__)
#define sl_zigbee_af_zdo_println(...) sl_zigbee_core_debug_println(__VA_ARGS__)
#define sl_zigbee_af_service_discovery_println(...) sl_zigbee_core_debug_println(__VA_ARGS__)
#define sl_zigbee_af_print(functionality, formatString, ...) sl_zigbee_core_debug_print(formatString, ##__VA_ARGS__)
#define sl_zigbee_af_println(functionality, formatString, ...) sl_zigbee_core_debug_println(formatString, ##__VA_ARGS__)
#define sl_zigbee_af_app_warn(...) sl_zigbee_app_debug_print(__VA_ARGS__)
#define sl_zigbee_af_app_warnln(...) sl_zigbee_app_debug_println(__VA_ARGS__)
#define sl_zigbee_af_app_error(...) sl_zigbee_app_debug_print(__VA_ARGS__)
#define sl_zigbee_af_app_errorln(...) sl_zigbee_app_debug_println(__VA_ARGS__)
#define sl_zigbee_af_core_warn(...) sl_zigbee_core_debug_print(__VA_ARGS__)
#define sl_zigbee_af_core_warnln(...) sl_zigbee_core_debug_println(__VA_ARGS__)
#define sl_zigbee_af_core_error(...) sl_zigbee_core_debug_print(__VA_ARGS__)
#define sl_zigbee_af_core_errorln(...) sl_zigbee_core_debug_println(__VA_ARGS__)
#endif // !(ZCL framework core || (NCP && simulation))
#else
#error "Include zigbee debug component or use the custom print system by setting SL_ZIGBEE_AF_PLUGIN_GREEN_POWER_ADAPTER_USE_CUSTOM_PRINT_SYSTEM to 1"
#endif // SL_CATALOG_ZIGBEE_DEBUG_PRINT_PRESENT
#endif // (SL_ZIGBEE_AF_PLUGIN_GREEN_POWER_ADAPTER_USE_CUSTOM_PRINT_SYSTEM == 1)

#endif //_SILABS_GREEN_POWER_PRINT_WRAPPER_H_
