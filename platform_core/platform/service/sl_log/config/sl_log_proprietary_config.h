/***************************************************************************/ /**
* @file sl_log_proprietary_config.h
* @brief SL DEBUG LOGGER Proprietary Config.
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

// <<< Use Configuration Wizard in Context Menu >>>

#ifndef SL_LOG_PROPRIETARY_CONFIG_H
#define SL_LOG_PROPRIETARY_CONFIG_H

/** @brief Buffer mode - log messages are stored in internal buffer */
#define SL_LOG_CONFIG_MODE_BUFFER 0
/** @brief Console mode - log messages are sent directly to console/UART */
#define SL_LOG_CONFIG_MODE_CONSOLE 1
/** @brief Host mode - log messages are stored in internal buffer and sent to console when log_flush() is called. */
#define SL_LOG_CONFIG_MODE_HOST 2

// <o SL_LOG_CONFIG_MODE> PROPRIETARY_CONFIG_MODE
// <SL_LOG_CONFIG_MODE_BUFFER => Buffer Mode
// <SL_LOG_CONFIG_MODE_CONSOLE => Console Mode
// <SL_LOG_CONFIG_MODE_HOST => Host Mode
#define SL_LOG_CONFIG_MODE SL_LOG_CONFIG_MODE_HOST

#endif /* SL_LOG_PROPRIETARY_CONFIG_H */

// <<< end of configuration section >>>
