/***************************************************************************//**
 * @file
 * @brief RTL Library Log Mutex implementation for CMSIS-RTOS2.
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

/***************************************************************************//**
 * @brief rtl_log callback mutex using CMSIS-RTOS2 (FreeRTOS / Micrium OS).
 ******************************************************************************/
#include <cmsis_os2.h>
#include <stddef.h>
#include "rtl_log_mutex.h"

/* name, attr_bits, cb_mem, cb_size — positional for C++17 / C compatibility */
static const osMutexAttr_t mutexAttr = {
  "rtl_log_cb",
  0u,
  NULL,
  0u,
};

int logMutexInit(logMutex_t *mtxInOut)
{
  if (mtxInOut == NULL) {
    return -1;
  }
  osMutexId_t mutexId = osMutexNew(&mutexAttr);
  *mtxInOut = (logMutex_t)mutexId;
  return (mutexId != NULL) ? 0 : -1;
}

void logMutexLock(logMutex_t *mtxInOut)
{
  if (mtxInOut == NULL || *mtxInOut == NULL) {
    return;
  }
  (void)osMutexAcquire((osMutexId_t)*mtxInOut, osWaitForever);
}

void logMutexUnlock(logMutex_t *mtxInOut)
{
  if (mtxInOut == NULL || *mtxInOut == NULL) {
    return;
  }
  (void)osMutexRelease((osMutexId_t)*mtxInOut);
}

void logMutexDeinit(logMutex_t *mtxInOut)
{
  if (mtxInOut == NULL || *mtxInOut == NULL) {
    return;
  }
  (void)osMutexDelete((osMutexId_t)*mtxInOut);
  *mtxInOut = NULL;
}
