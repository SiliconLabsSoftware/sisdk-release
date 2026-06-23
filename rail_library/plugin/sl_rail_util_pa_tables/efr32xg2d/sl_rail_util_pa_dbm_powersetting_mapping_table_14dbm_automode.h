/***************************************************************************//**
 * @file
 * @brief PA power conversion curves used by Silicon Labs PA power conversion
 *   functions.
 * @details This file contains the curves needed convert PA power levels to
 *   dBm powers.
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

#ifndef __PA_DBM_POWERSETTING_MAPPING_EFR32XG23_H_
#define __PA_DBM_POWERSETTING_MAPPING_EFR32XG23_H_

#ifdef __cplusplus
extern "C" {
#endif

#define SL_RAIL_PA_TABLE_0_MIN_POWER_DDBM -380
#define SL_RAIL_PA_TABLE_0_MAX_POWER_DDBM  144
#define SL_RAIL_PA_TABLE_0_STEP_DDBM        10
#define SL_RAIL_PA_TABLE_0_NUM_VALUES       54U

#define SL_RAIL_PA_TABLE_0                            \
  {                               /* round:lowest */  \
    /* LLP from min to -10 dBm */                     \
    0xc000 /* est_deci-dBm:-380 act_deci-dBm:-379 */, \
    0xc003 /* est_deci-dBm:-370 act_deci-dBm:-376 */, \
    0xc005 /* est_deci-dBm:-360 act_deci-dBm:-363 */, \
    0xc007 /* est_deci-dBm:-350 act_deci-dBm:-350 */, \
    0xc007 /* est_deci-dBm:-340 act_deci-dBm:-350 */, \
    0xc009 /* est_deci-dBm:-330 act_deci-dBm:-332 */, \
    0xc00b /* est_deci-dBm:-320 act_deci-dBm:-321 */, \
    0xc00c /* est_deci-dBm:-310 act_deci-dBm:-311 */, \
    0xc00e /* est_deci-dBm:-300 act_deci-dBm:-301 */, \
    0xc00f /* est_deci-dBm:-290 act_deci-dBm:-297 */, \
    0xc011 /* est_deci-dBm:-280 act_deci-dBm:-283 */, \
    0xc014 /* est_deci-dBm:-270 act_deci-dBm:-270 */, \
    0xc016 /* est_deci-dBm:-260 act_deci-dBm:-262 */, \
    0xc019 /* est_deci-dBm:-250 act_deci-dBm:-250 */, \
    0xc01c /* est_deci-dBm:-240 act_deci-dBm:-240 */, \
    0xc01f /* est_deci-dBm:-230 act_deci-dBm:-233 */, \
    0xc024 /* est_deci-dBm:-220 act_deci-dBm:-220 */, \
    0xc028 /* est_deci-dBm:-210 act_deci-dBm:-211 */, \
    0xc02e /* est_deci-dBm:-200 act_deci-dBm:-200 */, \
    0xc033 /* est_deci-dBm:-190 act_deci-dBm:-190 */, \
    0xc038 /* est_deci-dBm:-180 act_deci-dBm:-181 */, \
    0xc03f /* est_deci-dBm:-170 act_deci-dBm:-171 */, \
    0xc047 /* est_deci-dBm:-160 act_deci-dBm:-161 */, \
    0xc050 /* est_deci-dBm:-150 act_deci-dBm:-150 */, \
    0xc05a /* est_deci-dBm:-140 act_deci-dBm:-140 */, \
    0xc066 /* est_deci-dBm:-130 act_deci-dBm:-130 */, \
    0xc071 /* est_deci-dBm:-120 act_deci-dBm:-120 */, \
    0xc07f /* est_deci-dBm:-110 act_deci-dBm:-110 */, \
    0xc090 /* est_deci-dBm:-100 act_deci-dBm:-100 */, \
    /* MP from -9 to -2 dBm */                        \
    0x4011 /* est_deci-dBm: -90 act_deci-dBm: -90 */, \
    0x4013 /* est_deci-dBm: -80 act_deci-dBm: -82 */, \
    0x4015 /* est_deci-dBm: -70 act_deci-dBm: -74 */, \
    0x4018 /* est_deci-dBm: -60 act_deci-dBm: -61 */, \
    0x401b /* est_deci-dBm: -50 act_deci-dBm: -52 */, \
    0x401f /* est_deci-dBm: -40 act_deci-dBm: -41 */, \
    0x4023 /* est_deci-dBm: -30 act_deci-dBm: -32 */, \
    0x4028 /* est_deci-dBm: -20 act_deci-dBm: -20 */, \
    /* HP from -1 dBm to max */                       \
    0x000d /* est_deci-dBm: -10 act_deci-dBm: -10 */, \
    0x000e /* est_deci-dBm:   0 act_deci-dBm:  -4 */, \
    0x0011 /* est_deci-dBm:  10 act_deci-dBm:  10 */, \
    0x0013 /* est_deci-dBm:  20 act_deci-dBm:  18 */, \
    0x0016 /* est_deci-dBm:  30 act_deci-dBm:  29 */, \
    0x001a /* est_deci-dBm:  40 act_deci-dBm:  40 */, \
    0x001e /* est_deci-dBm:  50 act_deci-dBm:  50 */, \
    0x0021 /* est_deci-dBm:  60 act_deci-dBm:  58 */, \
    0x0027 /* est_deci-dBm:  70 act_deci-dBm:  70 */, \
    0x002d /* est_deci-dBm:  80 act_deci-dBm:  80 */, \
    0x0035 /* est_deci-dBm:  90 act_deci-dBm:  90 */, \
    0x003f /* est_deci-dBm: 100 act_deci-dBm: 100 */, \
    0x004c /* est_deci-dBm: 110 act_deci-dBm: 110 */, \
    0x005f /* est_deci-dBm: 120 act_deci-dBm: 120 */, \
    0x007e /* est_deci-dBm: 130 act_deci-dBm: 130 */, \
    0x00be /* est_deci-dBm: 140 act_deci-dBm: 140 */, \
    0x00e8 /* est_deci-dBm: 144 act_deci-dBm: 144 */, \
  }

#ifdef __cplusplus
}
#endif

#endif
