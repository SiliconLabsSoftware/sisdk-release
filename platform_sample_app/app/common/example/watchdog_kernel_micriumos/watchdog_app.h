/***************************************************************************//**
 * @file
 * @brief WatchDog examples functions with Micrium OS kernel
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

#ifndef WATCHDOG_APP_H
#define WATCHDOG_APP_H

/***************************************************************************//**
 * Initialize example (create tasks).
 ******************************************************************************/
void sample_init(void);

/***************************************************************************//**
 * Retrieve faulty watchdog information from the previous reset.
 ******************************************************************************/
void watchdog_retrieve_faulty(void);

#endif /* WATCHDOG_APP_H */
