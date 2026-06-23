/***************************************************************************//**
 * @file
 * @brief Bluetooth RTOS configuration for series 2 devices
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * SPDX-License-Identifier: Zlib
 *
 * The licensor of this software is Silicon Laboratories Inc.
 *
 * This software is provided 'as-is', without any express or implied warranty.
 * In no event will the authors be held liable for any damages arising from the
 * use of this software.
 *
 * Permission is granted to anyone to use this software for any purpose,
 * including commercial applications, and to alter it and redistribute it
 * freely, subject to the following restrictions:
 *
 * 1. The origin of this software must not be misrepresented; you must not
 *    claim that you wrote the original software. If you use this software in a
 *    product, an acknowledgment in the product documentation would be
 *    appreciated but is not required.
 * 2. Altered source versions must be plainly marked as such, and must not be
 *    misrepresented as being the original software.
 * 3. This notice may not be removed or altered from any source distribution.
 *
 ******************************************************************************/

#ifndef SL_BTCTRL_RTOS_CONFIG_S2_H
#define SL_BTCTRL_RTOS_CONFIG_S2_H

// <<< Use Configuration Wizard in Context Menu >>>

// <h> Priority Configuration for Bluetooth RTOS Tasks

// <o SL_BTCTRL_RTOS_LINK_LAYER_TASK_PRIORITY> Bluetooth link layer task priority
// <i> Default: 52 (CMSIS-RTOS2 osPriorityRealtime4)
// <i> Define the priority of the Bluetooth link layer task. This must be a valid
// <i> priority value from CMSIS-RTOS2 osPriority_t definition.
#define SL_BTCTRL_RTOS_LINK_LAYER_TASK_PRIORITY     (52)

// <o SL_BTCTRL_RTOS_LINK_LAYER_TASK_STACK_SIZE> Bluetooth link layer task stack size in bytes
// <i> Default: 1000
// <i> Define the stack size of the Bluetooth link layer task. The value is in bytes
// <i> and will be word aligned when it is applied at the task creation.
#define SL_BTCTRL_RTOS_LINK_LAYER_TASK_STACK_SIZE   (1000)

// </h> End Priority Configuration for Bluetooth RTOS Tasks

// <<< end of configuration section >>>

#endif // SL_BTCTRL_RTOS_CONFIG_S2_H
