/***************************************************************************//**
 * @file
 * @brief Serial Port Profile component configuration
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

#ifndef SPP_CONFIG_H
#define SPP_CONFIG_H

/***************************************************************************//**
 * @addtogroup spp
 * @{
 ******************************************************************************/

// <<< Use Configuration Wizard in Context Menu >>>

// <h> SPP Configuration

// <e SPP_LOG> Log
// <i> Default: On
#define SPP_LOG                    1

// <s SPP_LOG_PREFIX> Log prefix
// <i> Default: "[SPP] "
#define SPP_LOG_PREFIX             "[SPP] "

// </e>

// <o SPP_DATA_BUFFER_SIZE> Data buffer size (bytes) <0-512>
// <i> Define the size of the data buffer in bytes.
// <i> Default: 512
#define SPP_DATA_BUFFER_SIZE    (512)

// <o SPP_MIN_CHUNK_SIZE> Minimum chunk size <1-255>
// <i> Define the minimum chunk size.
// <i> Default: 200
#define SPP_MIN_CHUNK_SIZE      (200)

// <q SPP_FLOW_CONTROL> Fast-Ack flow control
// <i> Default: On
#define SPP_FLOW_CONTROL        1

// </h>

// <<< end of configuration section >>>

/** @} (end addtogroup spp) */
#endif // SPP_CONFIG_H
