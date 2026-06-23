/***************************************************************************//**
 * @file
 * @brief PA power conversion curves used by Silicon Labs PA power conversion
 *   functions.
 * @details This file contains the curves needed convert PA power levels to
 *   dBm powers.
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

#ifndef __PA_DBM_POWERSETTING_MAPPING_EFR32XG2D_H_
#define __PA_DBM_POWERSETTING_MAPPING_EFR32XG2D_H_

#ifdef __cplusplus
extern "C" {
#endif

#define SL_RAIL_PA_TABLE_0_NUM_VALUES  (36U)
#define SL_RAIL_PA_TABLE_0_STEP_DDBM   (10U)
#define SL_RAIL_PA_TABLE_0_MAX_POWER_DDBM     (200U)
#define SL_RAIL_PA_TABLE_0_MIN_POWER_DDBM     (-145)

#define SL_RAIL_PA_TABLE_0                        \
  {                                               \
    0x0 /* est_deci-dBm:-145 act_deci-dBm:-146*/, \
    0x0 /* est_deci-dBm:-135 act_deci-dBm:-146*/, \
    0x0 /* est_deci-dBm:-125 act_deci-dBm:-146*/, \
    0x0 /* est_deci-dBm:-115 act_deci-dBm:-146*/, \
    0x2 /* est_deci-dBm:-105 act_deci-dBm:-112*/, \
    0x2 /* est_deci-dBm:-95 act_deci-dBm:-112*/,  \
    0x3 /* est_deci-dBm:-85 act_deci-dBm:-87*/,   \
    0x3 /* est_deci-dBm:-75 act_deci-dBm:-87*/,   \
    0x4 /* est_deci-dBm:-65 act_deci-dBm:-69*/,   \
    0x4 /* est_deci-dBm:-55 act_deci-dBm:-69*/,   \
    0x5 /* est_deci-dBm:-45 act_deci-dBm:-53*/,   \
    0x6 /* est_deci-dBm:-35 act_deci-dBm:-40*/,   \
    0x7 /* est_deci-dBm:-25 act_deci-dBm:-29*/,   \
    0x8 /* est_deci-dBm:-15 act_deci-dBm:-19*/,   \
    0x9 /* est_deci-dBm:-5 act_deci-dBm:-10*/,    \
    0xb /* est_deci-dBm:5 act_deci-dBm:5*/,       \
    0xc /* est_deci-dBm:15 act_deci-dBm:11*/,     \
    0xe /* est_deci-dBm:25 act_deci-dBm:22*/,     \
    0x10 /* est_deci-dBm:35 act_deci-dBm:33*/,    \
    0x13 /* est_deci-dBm:45 act_deci-dBm:45*/,    \
    0x15 /* est_deci-dBm:55 act_deci-dBm:53*/,    \
    0x18 /* est_deci-dBm:65 act_deci-dBm:64*/,    \
    0x1c /* est_deci-dBm:75 act_deci-dBm:75*/,    \
    0x1f /* est_deci-dBm:85 act_deci-dBm:83*/,    \
    0x24 /* est_deci-dBm:95 act_deci-dBm:95*/,    \
    0x29 /* est_deci-dBm:105 act_deci-dBm:105*/,  \
    0x2f /* est_deci-dBm:115 act_deci-dBm:115*/,  \
    0x36 /* est_deci-dBm:125 act_deci-dBm:125*/,  \
    0x3f /* est_deci-dBm:135 act_deci-dBm:135*/,  \
    0x49 /* est_deci-dBm:145 act_deci-dBm:145*/,  \
    0x56 /* est_deci-dBm:155 act_deci-dBm:155*/,  \
    0x66 /* est_deci-dBm:165 act_deci-dBm:165*/,  \
    0x7e /* est_deci-dBm:175 act_deci-dBm:175*/,  \
    0xa0 /* est_deci-dBm:185 act_deci-dBm:185*/,  \
    0xd3 /* est_deci-dBm:195 act_deci-dBm:195*/,  \
    0xec /* est_deci-dBm:200 act_deci-dBm:200*/,  \
  }

#ifdef __cplusplus
}
#endif

#endif
