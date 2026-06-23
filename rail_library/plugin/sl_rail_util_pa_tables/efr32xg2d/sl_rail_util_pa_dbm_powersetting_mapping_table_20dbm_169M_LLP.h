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

#define SL_RAIL_PA_TABLE_0_NUM_VALUES  (50U)
#define SL_RAIL_PA_TABLE_0_STEP_DDBM   (10U)
#define SL_RAIL_PA_TABLE_0_MAX_POWER_DDBM     (-57)
#define SL_RAIL_PA_TABLE_0_MIN_POWER_DDBM     (-540)

#define SL_RAIL_PA_TABLE_0                           \
  {                                                  \
    0xc000 /* est_deci-dBm:-540 act_deci-dBm:-534*/, \
    0xc000 /* est_deci-dBm:-530 act_deci-dBm:-534*/, \
    0xc000 /* est_deci-dBm:-520 act_deci-dBm:-534*/, \
    0xc000 /* est_deci-dBm:-510 act_deci-dBm:-534*/, \
    0xc000 /* est_deci-dBm:-500 act_deci-dBm:-534*/, \
    0xc002 /* est_deci-dBm:-490 act_deci-dBm:-494*/, \
    0xc002 /* est_deci-dBm:-480 act_deci-dBm:-494*/, \
    0xc002 /* est_deci-dBm:-470 act_deci-dBm:-494*/, \
    0xc003 /* est_deci-dBm:-460 act_deci-dBm:-469*/, \
    0xc003 /* est_deci-dBm:-450 act_deci-dBm:-469*/, \
    0xc003 /* est_deci-dBm:-440 act_deci-dBm:-469*/, \
    0xc004 /* est_deci-dBm:-430 act_deci-dBm:-433*/, \
    0xc004 /* est_deci-dBm:-420 act_deci-dBm:-433*/, \
    0xc005 /* est_deci-dBm:-410 act_deci-dBm:-419*/, \
    0xc006 /* est_deci-dBm:-400 act_deci-dBm:-403*/, \
    0xc007 /* est_deci-dBm:-390 act_deci-dBm:-393*/, \
    0xc007 /* est_deci-dBm:-380 act_deci-dBm:-393*/, \
    0xc007 /* est_deci-dBm:-370 act_deci-dBm:-393*/, \
    0xc008 /* est_deci-dBm:-360 act_deci-dBm:-362*/, \
    0xc009 /* est_deci-dBm:-350 act_deci-dBm:-356*/, \
    0xc00b /* est_deci-dBm:-340 act_deci-dBm:-343*/, \
    0xc00c /* est_deci-dBm:-330 act_deci-dBm:-332*/, \
    0xc00e /* est_deci-dBm:-320 act_deci-dBm:-321*/, \
    0xc00f /* est_deci-dBm:-310 act_deci-dBm:-317*/, \
    0xc00f /* est_deci-dBm:-300 act_deci-dBm:-317*/, \
    0xc011 /* est_deci-dBm:-290 act_deci-dBm:-291*/, \
    0xc013 /* est_deci-dBm:-280 act_deci-dBm:-284*/, \
    0xc017 /* est_deci-dBm:-270 act_deci-dBm:-270*/, \
    0xc018 /* est_deci-dBm:-260 act_deci-dBm:-261*/, \
    0xc01c /* est_deci-dBm:-250 act_deci-dBm:-250*/, \
    0xc021 /* est_deci-dBm:-240 act_deci-dBm:-240*/, \
    0xc025 /* est_deci-dBm:-230 act_deci-dBm:-231*/, \
    0xc02a /* est_deci-dBm:-220 act_deci-dBm:-220*/, \
    0xc02f /* est_deci-dBm:-210 act_deci-dBm:-210*/, \
    0xc033 /* est_deci-dBm:-200 act_deci-dBm:-200*/, \
    0xc039 /* est_deci-dBm:-190 act_deci-dBm:-190*/, \
    0xc041 /* est_deci-dBm:-180 act_deci-dBm:-180*/, \
    0xc049 /* est_deci-dBm:-170 act_deci-dBm:-170*/, \
    0xc050 /* est_deci-dBm:-160 act_deci-dBm:-160*/, \
    0xc059 /* est_deci-dBm:-150 act_deci-dBm:-150*/, \
    0xc065 /* est_deci-dBm:-140 act_deci-dBm:-140*/, \
    0xc070 /* est_deci-dBm:-130 act_deci-dBm:-130*/, \
    0xc07d /* est_deci-dBm:-120 act_deci-dBm:-120*/, \
    0xc08d /* est_deci-dBm:-110 act_deci-dBm:-110*/, \
    0xc09c /* est_deci-dBm:-100 act_deci-dBm:-100*/, \
    0xc0af /* est_deci-dBm:-90 act_deci-dBm:-90*/,   \
    0xc0c5 /* est_deci-dBm:-80 act_deci-dBm:-80*/,   \
    0xc0db /* est_deci-dBm:-70 act_deci-dBm:-70*/,   \
    0xc0ea /* est_deci-dBm:-60 act_deci-dBm:-60*/,   \
    0xc0ee /* est_deci-dBm:-57 act_deci-dBm:-57*/,   \
  }

#ifdef __cplusplus
}
#endif

#endif
