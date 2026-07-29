/*******************************************************************************
 * @file
 * @brief Silicon Labs POSIX compile-time configuration for OpenThread Border Router (OTBR) builds.
 *
 *   This file overrides OpenThread configuration constants with values recommended
 *   for Silicon Labs certifiable OTBR deployments. Review all settings before use —
 *   some may need adjustment for your specific scenario.
 *
 *   Before running the bootstrap and setup scripts below, copy this file into the
 *   OpenThread source tree:
 *
 *   sudo cp $SDK_DIR/openthread/platform-abstraction/posix/openthread-core-silabs-posix-config.h \
 *           $SDK_DIR/openthread_stack/util/third_party/openthread/src/posix/platform/
 *
 *   where $SDK_DIR is the root of your Silicon Labs Simplicity SDK checkout.
 *   For full build instructions and environment variable definitions, refer to the
 *   Silicon Labs OpenThread documentation.
 *******************************************************************************
 * # License
 * <b>Copyright 2024 Silicon Laboratories Inc. www.silabs.com</b>
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

#ifndef OPENTHREAD_CORE_SILABS_POSIX_CONFIG_H_
#define OPENTHREAD_CORE_SILABS_POSIX_CONFIG_H_

/* clang-format off */
/******************************************************************************
 * Reference build strings for Silicon Labs OTBR
 *
 * Set the following environment variables before running the scripts:
 *
 *   export SDK_DIR=<absolute path to SDK checkout>
 *   export THREAD_DIR=$SDK_DIR/openthread        // OpenThread PAL (contains platform-abstraction/)
 *   export CPCD_DIR=<absolute path to cpc-daemon checkout>  // CPC builds only
 *
 * Pass OTBR_MDNS, OTBR_DHCP6_PD_CLIENT, and NAT64_SERVICE explicitly to both
 * bootstrap and setup. The values below are what Silicon Labs tests and certifies
 * against. Alternate values are supported.
 *
 * OTBR_MDNS=avahi is deprecated and not recommended.
 *
 *   Variable              | RCP default       | NCP default
 *   ----------------------|-------------------|------------------
 *   OTBR_MDNS             | openthread        | mDNSResponder
 *   OTBR_DHCP6_PD_CLIENT  | dhcpcd            | dhcpcd
 *   NAT64_SERVICE         | openthread        | tayga
 *
 *****************************************************************************/

/****************************
 * Default OTBR — RCP
 ****************************/

/*

sudo OTBR_MDNS=openthread OTBR_DHCP6_PD_CLIENT=dhcpcd NAT64=1 NAT64_SERVICE=openthread \
     ./script/bootstrap

sudo INFRA_IF_NAME=eth0 \
     OTBR_MDNS=openthread OTBR_DHCP6_PD_CLIENT=dhcpcd NAT64=1 NAT64_SERVICE=openthread \
     OTBR_OPTIONS="-DOT_THREAD_VERSION=1.4 \
                   -DOT_PLATFORM_CONFIG=openthread-core-silabs-posix-config.h \
                   -DOTBR_DUA_ROUTING=ON \
                   -DOTBR_DHCP6_PD=ON \
                   -DOTBR_NAME=SL-OPENTHREAD-BR -DOTBR_VERSION=3.1.1.0_GitHub-717abf0dc -DOT_PACKAGE_NAME=SL-OPENTHREAD -DOT_PACKAGE_VERSION=3.1.1.0_GitHub-fb274efe6" \
     ./script/setup

*/

/****************************
 * Default OTBR — NCP
 ****************************/

/*

sudo OTBR_MDNS=mDNSResponder OTBR_DHCP6_PD_CLIENT=dhcpcd NAT64=1 NAT64_SERVICE=tayga \
     ./script/bootstrap

sudo INFRA_IF_NAME=eth0 \
     OTBR_MDNS=mDNSResponder OTBR_DHCP6_PD_CLIENT=dhcpcd NAT64=1 NAT64_SERVICE=tayga \
     OTBR_OPTIONS="-DOT_THREAD_VERSION=1.4 \
                   -DOT_PLATFORM_CONFIG=openthread-core-silabs-posix-config.h \
                   -DOTBR_DUA_ROUTING=ON \
                   -DOTBR_DHCP6_PD=ON \
                   -DOTBR_DNS_UPSTREAM_QUERY=OFF \
                   -DOTBR_NCP_DNS_UPSTREAM=ON \
                   -DOTBR_NCP_DNS_UPSTREAM_BIND_TO_INFRA=ON \
                   -DOTBR_NAME=SL-OPENTHREAD-BR -DOTBR_VERSION=3.1.1.0_GitHub-717abf0dc -DOT_PACKAGE_NAME=SL-OPENTHREAD -DOT_PACKAGE_VERSION=3.1.1.0_GitHub-fb274efe6" \
     ./script/setup

*/

/****************************
 * CPC OTBR — RCP
 ****************************/

/*

sudo OTBR_MDNS=openthread OTBR_DHCP6_PD_CLIENT=dhcpcd NAT64=1 NAT64_SERVICE=openthread \
     ./script/bootstrap

sudo INFRA_IF_NAME=eth0 \
     OTBR_MDNS=openthread OTBR_DHCP6_PD_CLIENT=dhcpcd NAT64=1 NAT64_SERVICE=openthread \
     OTBR_OPTIONS="-DOT_THREAD_VERSION=1.4 \
                   -DOT_MULTIPAN_RCP=ON \
                   -DCPCD_SOURCE_DIR=$CPCD_DIR \
                   -DOT_POSIX_RCP_HDLC_BUS=ON \
                   -DOT_POSIX_RCP_SPI_BUS=ON \
                   -DOT_POSIX_RCP_VENDOR_BUS=ON \
                   -DOT_POSIX_CONFIG_RCP_VENDOR_DEPS_PACKAGE=$THREAD_DIR/platform-abstraction/posix/posix_vendor_rcp.cmake \
                   -DOT_POSIX_CONFIG_RCP_VENDOR_INTERFACE=$THREAD_DIR/platform-abstraction/posix/cpc_interface.cpp \
                   -DOT_CLI_VENDOR_EXTENSION=$THREAD_DIR/platform-abstraction/posix/posix_vendor_cli.cmake \
                   -DOT_PLATFORM_CONFIG=openthread-core-silabs-posix-config.h \
                   -DOTBR_DUA_ROUTING=ON \
                   -DOTBR_DHCP6_PD=ON \
                   -DOTBR_NAME=SL-OPENTHREAD-BR -DOTBR_VERSION=3.1.1.0_GitHub-717abf0dc -DOT_PACKAGE_NAME=SL-OPENTHREAD -DOT_PACKAGE_VERSION=3.1.1.0_GitHub-fb274efe6" \
     ./script/setup

*/

/****************************
 * CPC OTBR — NCP
 ****************************/

/*

sudo OTBR_MDNS=mDNSResponder OTBR_DHCP6_PD_CLIENT=dhcpcd NAT64=1 NAT64_SERVICE=tayga \
     ./script/bootstrap

sudo INFRA_IF_NAME=eth0 \
     OTBR_MDNS=mDNSResponder OTBR_DHCP6_PD_CLIENT=dhcpcd NAT64=1 NAT64_SERVICE=tayga \
     OTBR_OPTIONS="-DOT_THREAD_VERSION=1.4 \
                   -DOT_MULTIPAN_RCP=ON \
                   -DCPCD_SOURCE_DIR=$CPCD_DIR \
                   -DOT_POSIX_RCP_HDLC_BUS=ON \
                   -DOT_POSIX_RCP_SPI_BUS=ON \
                   -DOT_POSIX_RCP_VENDOR_BUS=ON \
                   -DOT_POSIX_CONFIG_RCP_VENDOR_DEPS_PACKAGE=$THREAD_DIR/platform-abstraction/posix/posix_vendor_rcp.cmake \
                   -DOT_POSIX_CONFIG_RCP_VENDOR_INTERFACE=$THREAD_DIR/platform-abstraction/posix/cpc_interface.cpp \
                   -DOT_CLI_VENDOR_EXTENSION=$THREAD_DIR/platform-abstraction/posix/posix_vendor_cli.cmake \
                   -DOT_PLATFORM_CONFIG=openthread-core-silabs-posix-config.h \
                   -DOTBR_DUA_ROUTING=ON \
                   -DOTBR_DHCP6_PD=ON \
                   -DOTBR_DNS_UPSTREAM_QUERY=OFF \
                   -DOTBR_NCP_DNS_UPSTREAM=ON \
                   -DOTBR_NCP_DNS_UPSTREAM_BIND_TO_INFRA=ON \
                   -DOTBR_NAME=SL-OPENTHREAD-BR -DOTBR_VERSION=3.1.0.0_GitHub-717abf0dc -DOT_PACKAGE_NAME=SL-OPENTHREAD -DOT_PACKAGE_VERSION=3.1.0.0_GitHub-fb274efe6" \
     ./script/setup

*/

/* clang-format on */
/******************************************************************************
 * Vendor defaults
 *****************************************************************************/

/**
 * OPENTHREAD_POSIX_CONFIG_SPINEL_VENDOR_INTERFACE_URL_PROTOCOL_NAME
 *
 * Define the URL protocol name of our vendor Spinel interface, which is CPC
 *
 */
#ifndef OPENTHREAD_POSIX_CONFIG_SPINEL_VENDOR_INTERFACE_URL_PROTOCOL_NAME
#define OPENTHREAD_POSIX_CONFIG_SPINEL_VENDOR_INTERFACE_URL_PROTOCOL_NAME "spinel+cpc"
#endif

/**
 * Provide radio url help message for vendor RCP bus configuration
 *
 * This supports Multipan/CPC configurations:
 * (OPENTHREAD_CONFIG_MULTIPAN_RCP_ENABLE &&
 *  OPENTHREAD_POSIX_CONFIG_SPINEL_VENDOR_INTERFACE_ENABLE)
 *
 * Unfortunately this file is included prior to OPENTHREAD_POSIX_CONFIG_SPINEL_VENDOR_INTERFACE_ENABLE
 * being defined so we can't check here.
 */
#define OT_VENDOR_RADIO_URL_HELP_BUS                                                               \
    "Protocol=[spinel+cpc*]            Specify the Spinel interface as the Spinel CPC interface\n" \
    "    spinel+cpc://cpcd_0?${Parameters} for connecting to cpcd\n"                               \
    "Parameters:\n"                                                                                \
    "    cpc-bus-speed[=speed]         CPC bus speed used for communicating with RCP.\n"

/******************************************************************************
 * Stack / MAC defaults for OTBR
 *****************************************************************************/

#undef OPENTHREAD_CONFIG_THREAD_VERSION
#define OPENTHREAD_CONFIG_THREAD_VERSION OT_THREAD_VERSION_1_4

/**
 * OPENTHREAD_CONFIG_REFERENCE_DEVICE_ENABLE
 *
 * Define to 1 to enable Thread Test Harness reference device support.
 */
#undef OPENTHREAD_CONFIG_REFERENCE_DEVICE_ENABLE
#define OPENTHREAD_CONFIG_REFERENCE_DEVICE_ENABLE 0

/**
 * OPENTHREAD_CONFIG_DUA_ENABLE
 *
 * Define as 1 to support Thread 1.2 Domain Unicast Address feature.
 *
 */
#undef OPENTHREAD_CONFIG_DUA_ENABLE
#define OPENTHREAD_CONFIG_DUA_ENABLE (OPENTHREAD_CONFIG_THREAD_VERSION >= OT_THREAD_VERSION_1_2)

/**
 * OPENTHREAD_CONFIG_MLR_ENABLE
 *
 * Define as 1 to support Thread 1.2 Multicast Listener Registration feature.
 *
 */
#undef OPENTHREAD_CONFIG_MLR_ENABLE
#define OPENTHREAD_CONFIG_MLR_ENABLE (OPENTHREAD_CONFIG_THREAD_VERSION >= OT_THREAD_VERSION_1_2)

/**
 * OPENTHREAD_CONFIG_BORDER_ROUTING_ENABLE
 *
 * Define to 1 to enable Border Routing Manager feature.
 *
 */
#undef OPENTHREAD_CONFIG_BORDER_ROUTING_ENABLE
#define OPENTHREAD_CONFIG_BORDER_ROUTING_ENABLE \
    (OPENTHREAD_FTD && OPENTHREAD_CONFIG_THREAD_VERSION >= OT_THREAD_VERSION_1_3)

/**
 * OPENTHREAD_CONFIG_DHCP6_CLIENT_ENABLE
 *
 * Define to 1 to enable DHCPv6 Client support.
 *
 */
#undef OPENTHREAD_CONFIG_DHCP6_CLIENT_ENABLE
#define OPENTHREAD_CONFIG_DHCP6_CLIENT_ENABLE (OPENTHREAD_CONFIG_THREAD_VERSION >= OT_THREAD_VERSION_1_3)

/**
 * OPENTHREAD_CONFIG_DHCP6_SERVER_ENABLE
 *
 * Define to 1 to enable DHCPv6 Server support.
 *
 */
#undef OPENTHREAD_CONFIG_DHCP6_SERVER_ENABLE
#define OPENTHREAD_CONFIG_DHCP6_SERVER_ENABLE \
    (OPENTHREAD_FTD && OPENTHREAD_CONFIG_THREAD_VERSION >= OT_THREAD_VERSION_1_3)

/**
 * OPENTHREAD_CONFIG_SRP_CLIENT_ENABLE
 *
 * Define to 1 to enable SRP Client support.
 *
 */
#undef OPENTHREAD_CONFIG_SRP_CLIENT_ENABLE
#define OPENTHREAD_CONFIG_SRP_CLIENT_ENABLE (OPENTHREAD_CONFIG_THREAD_VERSION >= OT_THREAD_VERSION_1_3)

/**
 * OPENTHREAD_CONFIG_RADIO_LINK_TREL_ENABLE
 *
 * Set to 1 to enable support for Thread Radio Encapsulation Link (TREL).
 *
 */
#undef OPENTHREAD_CONFIG_RADIO_LINK_TREL_ENABLE
#define OPENTHREAD_CONFIG_RADIO_LINK_TREL_ENABLE \
    (OPENTHREAD_FTD && OPENTHREAD_CONFIG_THREAD_VERSION >= OT_THREAD_VERSION_1_3)

/**
 * OPENTHREAD_CONFIG_TCP_ENABLE
 *
 * Set to 1 to enable TCP.
 *
 */
#undef OPENTHREAD_CONFIG_TCP_ENABLE
#define OPENTHREAD_CONFIG_TCP_ENABLE (OPENTHREAD_CONFIG_THREAD_VERSION >= OT_THREAD_VERSION_1_3)

/**
 * OPENTHREAD_CONFIG_DNS_CLIENT_OVER_TCP_ENABLE
 *
 * Set to 1 to enable support for sending DNS Queries over TCP.
 *
 */
#undef OPENTHREAD_CONFIG_DNS_CLIENT_OVER_TCP_ENABLE
#define OPENTHREAD_CONFIG_DNS_CLIENT_OVER_TCP_ENABLE (OPENTHREAD_CONFIG_THREAD_VERSION >= OT_THREAD_VERSION_1_3)

/**
 * OPENTHREAD_CONFIG_BORDER_ROUTING_DHCP6_PD_ENABLE
 *
 * Define to 1 to enable the Border Routing Manager's DHCPv6 Prefix Delegation feature.
 *
 */
#undef OPENTHREAD_CONFIG_BORDER_ROUTING_DHCP6_PD_ENABLE
#define OPENTHREAD_CONFIG_BORDER_ROUTING_DHCP6_PD_ENABLE \
    (OPENTHREAD_FTD && OPENTHREAD_CONFIG_THREAD_VERSION >= OT_THREAD_VERSION_1_3)

/**
 * OPENTHREAD_CONFIG_BORDER_ROUTING_DHCP6_PD_CLIENT_ENABLE
 *
 * Define to 1 to enable the Border Router's built-in OpenThread DHCPv6 Prefix Delegation (PD) client feature.
 *
 * This should work in theory, but there are some certification flows that are yet to be fixed with this
 * implementation.
 *
 */
#undef OPENTHREAD_CONFIG_BORDER_ROUTING_DHCP6_PD_CLIENT_ENABLE
#define OPENTHREAD_CONFIG_BORDER_ROUTING_DHCP6_PD_CLIENT_ENABLE 0

/**
 * @def OPENTHREAD_CONFIG_NET_DIAG_VENDOR_NAME
 *
 * Set to a non-empty default to satisfy certification features, but can be changed at run time.
 * See `OPENTHREAD_CONFIG_NET_DIAG_VENDOR_INFO_SET_API_ENABLE`
 */
#undef OPENTHREAD_CONFIG_NET_DIAG_VENDOR_NAME
#if OPENTHREAD_CONFIG_REFERENCE_DEVICE_ENABLE
#define OPENTHREAD_CONFIG_NET_DIAG_VENDOR_NAME "RD:Silicon Labs"
#else
#define OPENTHREAD_CONFIG_NET_DIAG_VENDOR_NAME "Silicon Labs"
#endif

/**
 * @def OPENTHREAD_CONFIG_NET_DIAG_VENDOR_MODEL
 *
 * Set to a non-empty default to satisfy certification features, but can be changed at run time.
 * See `OPENTHREAD_CONFIG_NET_DIAG_VENDOR_INFO_SET_API_ENABLE`
 */
#undef OPENTHREAD_CONFIG_NET_DIAG_VENDOR_MODEL
#define OPENTHREAD_CONFIG_NET_DIAG_VENDOR_MODEL "Sample"

/**
 * @def OPENTHREAD_CONFIG_NET_DIAG_VENDOR_SW_VERSION
 *
 * Set to a non-empty default to satisfy certification features, but can be changed at run time.
 * See `OPENTHREAD_CONFIG_NET_DIAG_VENDOR_INFO_SET_API_ENABLE`
 */
#undef OPENTHREAD_CONFIG_NET_DIAG_VENDOR_SW_VERSION
#define OPENTHREAD_CONFIG_NET_DIAG_VENDOR_SW_VERSION "3.1.1.0"

/**
 * @def OPENTHREAD_CONFIG_NET_DIAG_VENDOR_APP_URL
 *
 * Set to a non-empty default to satisfy certification features, but can be changed at run time.
 * See `OPENTHREAD_CONFIG_NET_DIAG_VENDOR_INFO_SET_API_ENABLE`
 */
#undef OPENTHREAD_CONFIG_NET_DIAG_VENDOR_APP_URL
#define OPENTHREAD_CONFIG_NET_DIAG_VENDOR_APP_URL "www.silabs.com"

/**
 * @def OPENTHREAD_CONFIG_NET_DIAG_VENDOR_INFO_SET_API_ENABLE
 *
 * Set to 1 to add APIs to allow Vendor Name, Model, SW Version to change at run-time.
 *
 */
#undef OPENTHREAD_CONFIG_NET_DIAG_VENDOR_INFO_SET_API_ENABLE
#define OPENTHREAD_CONFIG_NET_DIAG_VENDOR_INFO_SET_API_ENABLE \
    (OPENTHREAD_CONFIG_THREAD_VERSION >= OT_THREAD_VERSION_1_3)

/**
 * OPENTHREAD_CONFIG_MAC_CSL_REQUEST_AHEAD_US
 *
 * Define how many microseconds ahead should MAC deliver CSL frame to SubMac.
 *
 * This value is a higher on the OTBR than the stack default.
 *
 * Security processing is delegated to the RCP. For Series-3, we need to account for more ahead time;
 * even though the EnhAck path is entirely in RAM, LPWCRYPTO executes from flash,
 * adding non-deterministic latency on the critical path from MAC timer fire to RAIL scheduled TX submission.
 * NOTE: This increased ahead time configuration on the host is compatible with both Series-2
 * and Series-3 RCPs because this config only controls when the MAC timer fires.
 * The actual on-air TX time is anchored to an absolute radio timestamp targeting the child's CSL receive window.
 * A Series-2 RCP simply receives the frame with more lead time than it needs.
 */
#undef OPENTHREAD_CONFIG_MAC_CSL_REQUEST_AHEAD_US
#define OPENTHREAD_CONFIG_MAC_CSL_REQUEST_AHEAD_US 18000

/**
 * OPENTHREAD_CONFIG_CSL_TRANSMIT_TIME_AHEAD
 *
 * Transmission scheduling and ramp up time needed for the CSL transmitter
 * to be ready, in units of microseconds. This time must include at least
 * the radio's turnaround time between end of CCA and start of preamble
 * transmission. To avoid early CSL transmission it also must not be configured
 * higher than the actual scheduling and ramp up time.
 *
 * Same as stack default, but can change if needed for OTBR as CSL transmitter.
 */
#undef OPENTHREAD_CONFIG_CSL_TRANSMIT_TIME_AHEAD
#define OPENTHREAD_CONFIG_CSL_TRANSMIT_TIME_AHEAD 40

/******************************************************************************
 * MultiPan RCP (CPC) defaults
 *****************************************************************************/

/**
 * Define to 1 to enable multipan RCP support.
 */
#ifndef OPENTHREAD_CONFIG_MULTIPAN_RCP_ENABLE
#define OPENTHREAD_CONFIG_MULTIPAN_RCP_ENABLE 0
#endif

#if OPENTHREAD_CONFIG_MULTIPAN_RCP_ENABLE

/**
 * Force disable max power table support.
 *
 */
#undef OPENTHREAD_POSIX_CONFIG_MAX_POWER_TABLE_ENABLE
#define OPENTHREAD_POSIX_CONFIG_MAX_POWER_TABLE_ENABLE 0

/**
 * Force disable Channel Manager support.
 *
 */
#undef OPENTHREAD_CONFIG_CHANNEL_MANAGER_ENABLE
#define OPENTHREAD_CONFIG_CHANNEL_MANAGER_ENABLE 0

/**
 * Force diable Channel Monitor support.
 *
 */
#undef OPENTHREAD_CONFIG_CHANNEL_MONITOR_ENABLE
#define OPENTHREAD_CONFIG_CHANNEL_MONITOR_ENABLE 0

#endif // OPENTHREAD_CONFIG_MULTIPAN_RCP_ENABLE

/******************************************************************************
 * Proprietary SubGhz defaults
 *****************************************************************************/

/**
 * Define to 1 if you want to enable proprietary radio support as defined by platform.
 *
 * @note If this setting is set to 1, the channel range is defined by the platform. Choosing this option requires
 * the following configuration options to be defined by Platform:
 * OPENTHREAD_CONFIG_PLATFORM_RADIO_PROPRIETARY_CHANNEL_PAGE,
 * OPENTHREAD_CONFIG_PLATFORM_RADIO_PROPRIETARY_CHANNEL_MIN,
 * OPENTHREAD_CONFIG_PLATFORM_RADIO_PROPRIETARY_CHANNEL_MAX and,
 * OPENTHREAD_CONFIG_PLATFORM_RADIO_PROPRIETARY_CHANNEL_MASK.
 *
 */
#ifndef OPENTHREAD_CONFIG_PLATFORM_RADIO_PROPRIETARY_SUPPORT
#ifndef OPENTHREAD_CONFIG_RADIO_915MHZ_OQPSK_SUPPORT
#ifndef OPENTHREAD_CONFIG_RADIO_2P4GHZ_OQPSK_SUPPORT
#define OPENTHREAD_CONFIG_PLATFORM_RADIO_PROPRIETARY_SUPPORT 0
#define OPENTHREAD_CONFIG_RADIO_915MHZ_OQPSK_SUPPORT 0
#define OPENTHREAD_CONFIG_RADIO_2P4GHZ_OQPSK_SUPPORT 1
#endif
#endif
#endif

#if OPENTHREAD_CONFIG_PLATFORM_RADIO_PROPRIETARY_SUPPORT

#undef OPENTHREAD_CONFIG_PLATFORM_RADIO_PROPRIETARY_CHANNEL_PAGE
#define OPENTHREAD_CONFIG_PLATFORM_RADIO_PROPRIETARY_CHANNEL_PAGE 23

#undef OPENTHREAD_CONFIG_PLATFORM_RADIO_PROPRIETARY_CHANNEL_MIN
#define OPENTHREAD_CONFIG_PLATFORM_RADIO_PROPRIETARY_CHANNEL_MIN 0

#undef OPENTHREAD_CONFIG_PLATFORM_RADIO_PROPRIETARY_CHANNEL_MAX
#define OPENTHREAD_CONFIG_PLATFORM_RADIO_PROPRIETARY_CHANNEL_MAX 24

#undef OPENTHREAD_CONFIG_DEFAULT_CHANNEL
#define OPENTHREAD_CONFIG_DEFAULT_CHANNEL OPENTHREAD_CONFIG_PLATFORM_RADIO_PROPRIETARY_CHANNEL_MIN

#undef OPENTHREAD_CONFIG_PLATFORM_RADIO_PROPRIETARY_CHANNEL_MASK
#define OPENTHREAD_CONFIG_PLATFORM_RADIO_PROPRIETARY_CHANNEL_MASK 0x1ffffff

/**
 * Force disable OQPSK modulation in 915MHz frequency band. The physical layer parameters are defined in
 * section 6 of IEEE802.15.4-2006.
 *
 */
#undef OPENTHREAD_CONFIG_RADIO_915MHZ_OQPSK_SUPPORT
#define OPENTHREAD_CONFIG_RADIO_915MHZ_OQPSK_SUPPORT 0

/**
 * Force disable OQPSK modulation in 2.4GHz frequency band. The physical layer parameters are defined in
 * section 6 of IEEE802.15.4-2006.
 *
 */
#undef OPENTHREAD_CONFIG_RADIO_2P4GHZ_OQPSK_SUPPORT
#define OPENTHREAD_CONFIG_RADIO_2P4GHZ_OQPSK_SUPPORT 0

/**
 * Define to enable platform logging and `otLog{Level}Plat()` OT functions.
 *
 */
#undef OPENTHREAD_CONFIG_LOG_PLATFORM
#define OPENTHREAD_CONFIG_LOG_PLATFORM 1

#endif // OPENTHREAD_CONFIG_PLATFORM_RADIO_PROPRIETARY_SUPPORT

/******************************************************************************
 * Project defaults
 *
 * See also ot-br-posix/third_party/openthread/CMakeLists.txt for other defaults
 *****************************************************************************/

/**
 * Define to 1 to enable Factory Diagnostics support.
 *
 */
#undef OPENTHREAD_CONFIG_DIAG_ENABLE
#define OPENTHREAD_CONFIG_DIAG_ENABLE 1

/**
 * The log level (used at compile time). If `OPENTHREAD_CONFIG_LOG_LEVEL_DYNAMIC_ENABLE` is set, this defines the most
 * verbose log level possible. See `OPENTHREAD_CONFIG_LOG_LEVEL_INIT` to set the initial log level.
 *
 */
#undef OPENTHREAD_CONFIG_LOG_LEVEL
#define OPENTHREAD_CONFIG_LOG_LEVEL OT_LOG_LEVEL_DEBG

/**
 * Define to prepend the log level to all log messages.
 *
 */
#undef OPENTHREAD_CONFIG_LOG_PREPEND_LEVEL
#define OPENTHREAD_CONFIG_LOG_PREPEND_LEVEL 1

/**
 * Defines the max count of RCP failures allowed to be recovered.
 * 0 means to disable RCP failure recovering.
 *
 */
#undef OPENTHREAD_SPINEL_CONFIG_RCP_RESTORATION_MAX_COUNT
#define OPENTHREAD_SPINEL_CONFIG_RCP_RESTORATION_MAX_COUNT 100

/**
 * Define to enable CLI logging and `otLogCli()` OT function.
 *
 */
#undef OPENTHREAD_CONFIG_LOG_CLI
#define OPENTHREAD_CONFIG_LOG_CLI 0

/**
 * Define to 1 if you want to enable radio coexistence implemented in platform.
 *
 */
#undef OPENTHREAD_CONFIG_PLATFORM_RADIO_COEX_ENABLE
#define OPENTHREAD_CONFIG_PLATFORM_RADIO_COEX_ENABLE 1

/******************************************************************************
 * Include OpenThread project's POSIX defaults
 *****************************************************************************/
#include "openthread-core-posix-config.h"

#endif // OPENTHREAD_CORE_SILABS_POSIX_CONFIG_H_
