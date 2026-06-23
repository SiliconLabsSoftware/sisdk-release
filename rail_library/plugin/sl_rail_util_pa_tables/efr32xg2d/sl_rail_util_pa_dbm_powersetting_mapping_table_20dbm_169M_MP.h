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

#define SL_RAIL_PA_TABLE_0_NUM_VALUES  (45U)
#define SL_RAIL_PA_TABLE_0_STEP_DDBM   (10U)
#define SL_RAIL_PA_TABLE_0_MAX_POWER_DDBM     (126U)
#define SL_RAIL_PA_TABLE_0_MIN_POWER_DDBM     (-310)

#define SL_RAIL_PA_TABLE_0                           \
  {                                                  \
    0x4000 /* est_deci-dBm:-310 act_deci-dBm:-314*/, \
    0x4000 /* est_deci-dBm:-300 act_deci-dBm:-314*/, \
    0x4000 /* est_deci-dBm:-290 act_deci-dBm:-314*/, \
    0x4000 /* est_deci-dBm:-280 act_deci-dBm:-314*/, \
    0x4002 /* est_deci-dBm:-270 act_deci-dBm:-274*/, \
    0x4002 /* est_deci-dBm:-260 act_deci-dBm:-274*/, \
    0x4002 /* est_deci-dBm:-250 act_deci-dBm:-274*/, \
    0x4003 /* est_deci-dBm:-240 act_deci-dBm:-249*/, \
    0x4003 /* est_deci-dBm:-230 act_deci-dBm:-249*/, \
    0x4003 /* est_deci-dBm:-220 act_deci-dBm:-249*/, \
    0x4004 /* est_deci-dBm:-210 act_deci-dBm:-219*/, \
    0x4005 /* est_deci-dBm:-200 act_deci-dBm:-205*/, \
    0x4006 /* est_deci-dBm:-190 act_deci-dBm:-190*/, \
    0x4007 /* est_deci-dBm:-180 act_deci-dBm:-180*/, \
    0x4007 /* est_deci-dBm:-170 act_deci-dBm:-180*/, \
    0x4007 /* est_deci-dBm:-160 act_deci-dBm:-180*/, \
    0x4009 /* est_deci-dBm:-150 act_deci-dBm:-150*/, \
    0x400a /* est_deci-dBm:-140 act_deci-dBm:-143*/, \
    0x400b /* est_deci-dBm:-130 act_deci-dBm:-137*/, \
    0x400d /* est_deci-dBm:-120 act_deci-dBm:-122*/, \
    0x400f /* est_deci-dBm:-110 act_deci-dBm:-111*/, \
    0x400f /* est_deci-dBm:-100 act_deci-dBm:-111*/, \
    0x4011 /* est_deci-dBm:-90 act_deci-dBm:-93*/,   \
    0x4014 /* est_deci-dBm:-80 act_deci-dBm:-81*/,   \
    0x4017 /* est_deci-dBm:-70 act_deci-dBm:-71*/,   \
    0x4019 /* est_deci-dBm:-60 act_deci-dBm:-61*/,   \
    0x401d /* est_deci-dBm:-50 act_deci-dBm:-50*/,   \
    0x4021 /* est_deci-dBm:-40 act_deci-dBm:-41*/,   \
    0x4026 /* est_deci-dBm:-30 act_deci-dBm:-30*/,   \
    0x402b /* est_deci-dBm:-20 act_deci-dBm:-20*/,   \
    0x402f /* est_deci-dBm:-10 act_deci-dBm:-13*/,   \
    0x4035 /* est_deci-dBm:0 act_deci-dBm:-1*/,      \
    0x403c /* est_deci-dBm:10 act_deci-dBm:10*/,     \
    0x4045 /* est_deci-dBm:20 act_deci-dBm:20*/,     \
    0x404d /* est_deci-dBm:30 act_deci-dBm:30*/,     \
    0x4056 /* est_deci-dBm:40 act_deci-dBm:40*/,     \
    0x4061 /* est_deci-dBm:50 act_deci-dBm:50*/,     \
    0x406e /* est_deci-dBm:60 act_deci-dBm:60*/,     \
    0x407b /* est_deci-dBm:70 act_deci-dBm:70*/,     \
    0x408b /* est_deci-dBm:80 act_deci-dBm:80*/,     \
    0x409d /* est_deci-dBm:90 act_deci-dBm:90*/,     \
    0x40b2 /* est_deci-dBm:100 act_deci-dBm:100*/,   \
    0x40cb /* est_deci-dBm:110 act_deci-dBm:110*/,   \
    0x40e3 /* est_deci-dBm:120 act_deci-dBm:120*/,   \
    0x40ed /* est_deci-dBm:126 act_deci-dBm:126*/,   \
  }
#ifdef __cplusplus
}
#endif

#endif
