/***************************************************************************//**
 * @file
 * @brief LEDSINK FreeRTOS kernel example
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

#ifndef LEDSINK_KERNEL_FREERTOS_H
#define LEDSINK_KERNEL_FREERTOS_H

/***************************************************************************//**
 * @brief Initialize LEDSINK and create the pattern and PWM sweep tasks.
 ******************************************************************************/
void ledsink_init(void);

#endif // LEDSINK_KERNEL_FREERTOS_H
