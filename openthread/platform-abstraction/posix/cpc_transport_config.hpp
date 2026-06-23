/*******************************************************************************
 * @file
 * @brief Compile-time defaults for `CpcTransport` (override before including `cpc_transport.hpp`).
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

#ifndef CPC_TRANSPORT_CONFIG_HPP
#define CPC_TRANSPORT_CONFIG_HPP

#ifndef CPC_TRANSPORT_CONFIG_INSTANCE_NAME_MAX_LEN
#define CPC_TRANSPORT_CONFIG_INSTANCE_NAME_MAX_LEN 32
#endif

/** `usleep` interval (microseconds) between `cpc_restart` / `cpc_open_endpoint` retries. */
#ifndef CPC_TRANSPORT_CONFIG_MAX_SLEEP_DURATION_US
#define CPC_TRANSPORT_CONFIG_MAX_SLEEP_DURATION_US 100000
#endif

/** Maximum attempts per reconnect phase (`cpc_restart` loop, then endpoint open loop). */
#ifndef CPC_TRANSPORT_CONFIG_MAX_RESTART_ATTEMPTS
#define CPC_TRANSPORT_CONFIG_MAX_RESTART_ATTEMPTS 300
#endif

#endif // CPC_TRANSPORT_CONFIG_HPP
