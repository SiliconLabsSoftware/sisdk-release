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

#define SL_RAIL_PA_TABLE_0_NUM_VALUES  (52U)
#define SL_RAIL_PA_TABLE_0_STEP_DDBM   (10U)
#define SL_RAIL_PA_TABLE_0_MAX_POWER_DDBM     (-67)
#define SL_RAIL_PA_TABLE_0_MIN_POWER_DDBM     (-434)

#define SL_RAIL_PA_TABLE_0                           \
  {                                                  \
    0xc000 /* est_deci-dBm:-434 act_deci-dBm:-434*/, \
    0xc000 /* est_deci-dBm:-424 act_deci-dBm:-434*/, \
    0xc002 /* est_deci-dBm:-414 act_deci-dBm:-422*/, \
    0xc003 /* est_deci-dBm:-404 act_deci-dBm:-412*/, \
    0xc004 /* est_deci-dBm:-394 act_deci-dBm:-395*/, \
    0xc005 /* est_deci-dBm:-384 act_deci-dBm:-387*/, \
    0xc006 /* est_deci-dBm:-374 act_deci-dBm:-376*/, \
    0xc007 /* est_deci-dBm:-364 act_deci-dBm:-369*/, \
    0xc007 /* est_deci-dBm:-354 act_deci-dBm:-369*/, \
    0xc009 /* est_deci-dBm:-344 act_deci-dBm:-346*/, \
    0xc00b /* est_deci-dBm:-334 act_deci-dBm:-334*/, \
    0xc00c /* est_deci-dBm:-324 act_deci-dBm:-326*/, \
    0xc00e /* est_deci-dBm:-314 act_deci-dBm:-316*/, \
    0xc00f /* est_deci-dBm:-304 act_deci-dBm:-312*/, \
    0xc011 /* est_deci-dBm:-294 act_deci-dBm:-295*/, \
    0xc014 /* est_deci-dBm:-284 act_deci-dBm:-284*/, \
    0xc017 /* est_deci-dBm:-274 act_deci-dBm:-275*/, \
    0xc019 /* est_deci-dBm:-264 act_deci-dBm:-266*/, \
    0xc01d /* est_deci-dBm:-254 act_deci-dBm:-255*/, \
    0xc020 /* est_deci-dBm:-244 act_deci-dBm:-244*/, \
    0xc025 /* est_deci-dBm:-234 act_deci-dBm:-234*/, \
    0xc02a /* est_deci-dBm:-224 act_deci-dBm:-224*/, \
    0xc02f /* est_deci-dBm:-214 act_deci-dBm:-215*/, \
    0xc035 /* est_deci-dBm:-204 act_deci-dBm:-204*/, \
    0xc03c /* est_deci-dBm:-194 act_deci-dBm:-194*/, \
    0xc043 /* est_deci-dBm:-184 act_deci-dBm:-184*/, \
    0xc04a /* est_deci-dBm:-174 act_deci-dBm:-175*/, \
    0xc054 /* est_deci-dBm:-164 act_deci-dBm:-164*/, \
    0xc05f /* est_deci-dBm:-154 act_deci-dBm:-154*/, \
    0xc069 /* est_deci-dBm:-144 act_deci-dBm:-144*/, \
    0xc077 /* est_deci-dBm:-134 act_deci-dBm:-134*/, \
    0xc084 /* est_deci-dBm:-124 act_deci-dBm:-124*/, \
    0xc095 /* est_deci-dBm:-114 act_deci-dBm:-114*/, \
    0xc0a6 /* est_deci-dBm:-104 act_deci-dBm:-104*/, \
    0xc0bb /* est_deci-dBm:-94 act_deci-dBm:-94*/,   \
    0xc0d1 /* est_deci-dBm:-84 act_deci-dBm:-84*/,   \
    0xc0e4 /* est_deci-dBm:-74 act_deci-dBm:-74*/,   \
    0xc0ed /* est_deci-dBm:-64 act_deci-dBm:-68*/,   \
    0xc0ed /* est_deci-dBm:-54 act_deci-dBm:-68*/,   \
    0xc0ed /* est_deci-dBm:-44 act_deci-dBm:-68*/,   \
    0xc0ed /* est_deci-dBm:-34 act_deci-dBm:-68*/,   \
    0xc0ed /* est_deci-dBm:-24 act_deci-dBm:-68*/,   \
    0xc0ed /* est_deci-dBm:-14 act_deci-dBm:-68*/,   \
    0xc0ed /* est_deci-dBm:-4 act_deci-dBm:-68*/,    \
    0xc0ed /* est_deci-dBm:6 act_deci-dBm:-68*/,     \
    0xc0ed /* est_deci-dBm:16 act_deci-dBm:-68*/,    \
    0xc0ed /* est_deci-dBm:26 act_deci-dBm:-68*/,    \
    0xc0ed /* est_deci-dBm:36 act_deci-dBm:-68*/,    \
    0xc0ed /* est_deci-dBm:46 act_deci-dBm:-68*/,    \
    0xc0ed /* est_deci-dBm:56 act_deci-dBm:-68*/,    \
    0xc0ed /* est_deci-dBm:66 act_deci-dBm:-68*/,    \
    0xc0ed /* est_deci-dBm:67 act_deci-dBm:-68*/,    \
  }

#ifdef __cplusplus
}
#endif

#endif
