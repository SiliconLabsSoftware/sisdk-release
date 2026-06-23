/***************************************************************************//**
 * @file
 * @brief SPP example configuration
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

#ifndef APP_CONFIG_H
#define APP_CONFIG_H

// <<< Use Configuration Wizard in Context Menu >>>

// <h> SPP Role Configuration

// <o APP_DEFAULT_SPP_ROLE> Default SPP role
// <0=> CENTRAL
// <1=> PERIPHERAL
// <i> Select the default SPP role used at boot.
// <i> Default: CENTRAL
#define APP_DEFAULT_SPP_ROLE                  0

// </h>

// <h> Bluetooth Filters Configuration

// <h> Filter by BD Address
// <e APP_FILTER_BY_BD_ADDR> Enable filtering by BD address
// <i> Default: Off
#define APP_FILTER_BY_BD_ADDR                 0

// <a.6 APP_TARGET_BD_ADDR_VALUE> Target BD address (6 bytes) <0..255> <f.h>
// <i> Default: {0x00,0x00,0x00,0x00,0x00,0x00}
#define APP_TARGET_BD_ADDR_VALUE              { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 }

// <o APP_TARGET_ADDR_TYPE> Address type
// <0=> PUBLIC
// <1=> RANDOM
// <i> Default: PUBLIC
#define APP_TARGET_ADDR_TYPE                  0
// </e>
// </h>

// <h> Filter by UUID
// <o APP_UUID_TYPE> UUID type
// <0=> None
// <1=> 16-bit
// <2=> 128-bit
// <i> Select which UUID type to use for filtering.
// <i> Default: 128-bit
#define APP_UUID_TYPE 2

// <a.2 APP_SERVICE_UUID16> 16-bit service UUID <0..255> <f.h>
// <i> Default: {0x01,0x11}
// <i> Note: 16-bit UUIDs are reserved for Bluetooth SIG assigned numbers only.
// <i> The default value 0x1101 is the SIG-assigned Serial Port Profile UUID
#define APP_SERVICE_UUID16                     { 0x01, 0x11 }
                                            
// <a.16 APP_SERVICE_UUID128> 128-bit service UUID <0..255> <f.h>
// <i> Default: {0xA4,0xA1,0x9E,0xCC,0xE7,0x51,0xA8,0x85,0x9F,0x47,0x7F,0x32,0x46,0xFE,0x92,0x8B}
#define APP_SERVICE_UUID128  { 0xA4, 0xA1, 0x9E, 0xCC, 0xE7, 0x51, 0xA8, 0x85, 0x9F, 0x47, 0x7F, 0x32, 0x46, 0xFE, 0x92, 0x8B }
// </h>

// <h> Filter by Device Name
// <e APP_FILTER_BY_NAME> Enable filtering by device name
// <i> Default : Off
#define APP_FILTER_BY_NAME                     0

// <s.32 APP_TARGET_NAME_VALUE> Device name string
// <i> Default: "SPP"
#define APP_TARGET_NAME_VALUE                  "SPP"
// </e>
// </h>

// <h> Filter by Service Data
// <e APP_FILTER_BY_SERVICE_DATA> Enable filtering by service data
// <i> Default: Off
#define APP_FILTER_BY_SERVICE_DATA             0

// <a.3 APP_SERVICE_DATA_VALUE> Service data bytes initializer <0..255> <f.h>
// <i> Default: {0x00,0x00,0x00}
#define APP_SERVICE_DATA_VALUE                 { 0x00, 0x00, 0x00 }

// <o APP_SERVICE_DATA_OFFSET> Offset within the AD record
// <i> Default: 0
#define APP_SERVICE_DATA_OFFSET                0

// <o APP_SERVICE_DATA_LEN> Length (in bytes)
// <i> Default: 3
#define APP_SERVICE_DATA_LEN                   3
// </e>
// </h>

// <h> Filter by Manufacturer Data
// <e APP_FILTER_BY_MANUFACTURER_DATA> Enable filtering by manufacturer data
// <i> Default: Off
#define APP_FILTER_BY_MANUFACTURER_DATA        0

// <a.4 APP_MANUFACTURER_DATA_VALUE> Manufacturer data initializer <0..255> <f.h>
// <i> Default: {0x00,0x00,0x00,0x00}
#define APP_MANUFACTURER_DATA_VALUE            { 0x00, 0x00, 0x00, 0x00 }

// <o APP_MANUFACTURER_DATA_OFFSET> Offset in the AD record
// <i> Default: 0
#define APP_MANUFACTURER_DATA_OFFSET           0

// <o APP_MANUFACTURER_DATA_LEN> Length (in bytes)
// <i> Default: 4
#define APP_MANUFACTURER_DATA_LEN              4
// </e>
// </h>
// <h> Filter by RSSI
// <e APP_FILTER_BY_RSSI> Enable filtering by RSSI
// <i> Default: Off
#define APP_FILTER_BY_RSSI                     0

// <o APP_TARGET_RSSI> RSSI threshold (signed dBm) <-127..20>
// <i> Default: -3
#define APP_TARGET_RSSI                        -3
// </e>
// </h>

// </h>

// <<< end of configuration section >>>

#endif // APP_CONFIG_H
