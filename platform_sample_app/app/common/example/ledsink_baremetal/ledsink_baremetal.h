/***************************************************************************//**
 * @file
 * @brief LEDSINK bare-metal example
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

#ifndef LEDSINK_BAREMETAL_H
#define LEDSINK_BAREMETAL_H

/***************************************************************************//**
 * @brief Initialize LEDSINK demo, start Mode 0 (hardware pattern).
 ******************************************************************************/
void ledsink_init(void);

/***************************************************************************//**
 * @brief Poll for button and timer events; call from app_process_action().
 ******************************************************************************/
void ledsink_process_action(void);

#endif // LEDSINK_BAREMETAL_H
