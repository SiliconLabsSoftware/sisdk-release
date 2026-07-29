/***************************************************************************//**
 * @file
 * @brief ESL Access Point NCP advertisement report filter configuration.
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

#ifndef ESL_AP_NCP_ADV_FILTER_CONFIG_H
#define ESL_AP_NCP_ADV_FILTER_CONFIG_H

// <<< Use Configuration Wizard in Context Menu >>>

// <h> ESL AP NCP Advertisement Filtering

// <e ESL_AP_NCP_ADV_FILTER_ENABLE> Filter advertisement reports on the NCP
// <i> When enabled, the NCP drops scan reports not containing the ESL
// Service UUID before forwarding them to the host.
// <i> Default: On
#define ESL_AP_NCP_ADV_FILTER_ENABLE                 1

// <q ESL_AP_NCP_ADV_FILTER_NON_CONNECTABLE_ENABLE> Drop non-connectable reports
// <i> Do not report non-connectable advertisements. Checked before
// UUID parsing: reduces UART load cheaply while such reports cannot be used for
// connection initiation anyway.
// Note: any non-connectable report that carries the ESL UUID is also dropped.
// <i> Default: On
#define ESL_AP_NCP_ADV_FILTER_NON_CONNECTABLE_ENABLE  1

// <q ESL_AP_NCP_ADV_FILTER_LEGACY_ENABLE> Filter legacy advertisement reports
// <i> Drop legacy advertisement reports that do not advertise the ESL
// Service UUID  using 16-bit UUID list or 16-bit Service Data.
// <i> Default: On
#define ESL_AP_NCP_ADV_FILTER_LEGACY_ENABLE           1

// <q ESL_AP_NCP_ADV_FILTER_EXTENDED_ENABLE> Filter extended advertisement reports
// <i> Keep reports only when ESL Service UUID is found in a single complete
// extended report as 16-bit UUID list or Service Data AD types.
// <i> Multi-fragment reports (incomplete_more / incomplete_nomore) are dropped
// as each fragment is a separate event with no stack reassembly, so UUID match
// on partial data is unreliable and the full chain is discarded.
// <i> Third-party ESL devices using large fragmented extended PDUs only may
// never reach the host. The Silicon Labs ESL Tag is unaffected by this filter
// since it uses legacy advertising.
// <i> Default: On
#define ESL_AP_NCP_ADV_FILTER_EXTENDED_ENABLE         1

// </e>

// </h>

// <<< end of configuration section >>>

#endif // ESL_AP_NCP_ADV_FILTER_CONFIG_H
