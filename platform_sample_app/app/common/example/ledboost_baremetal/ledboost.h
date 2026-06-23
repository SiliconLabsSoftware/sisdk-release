/***************************************************************************//**
 * @file
 * @brief LED Boost DCDC example functions
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * The licensor of this software is Silicon Laboratories Inc. Your use of this
 * software is governed by the terms of Silicon Labs Master Software License
 * Agreement (MSLA) available at
 * www.silabs.com/about-us/legal/master-software-license-agreement. This
 * software is distributed to you in Source Code format and is governed by the
 * sections of the MSLA applicable to Source Code.
 *
 ******************************************************************************/

#ifndef LEDBOOST_H
#define LEDBOOST_H

/***************************************************************************//**
 * Initialize LED Boost example.
 ******************************************************************************/
void ledboost_init(void);

/***************************************************************************//**
 * LED Boost ticking function.
 ******************************************************************************/
void ledboost_process_action(void);

#endif  // LEDBOOST_H
