/*
 *  Copyright (c) 2026, The OpenThread Authors.
 *  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions are met:
 *  1. Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *  2. Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *  3. Neither the name of the copyright holder nor the
 *     names of its contributors may be used to endorse or promote products
 *     derived from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 *  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 *  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 *  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 *  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 *  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 *  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 *  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */

/**
 * @file logging_sl_debug.c
 *  This file implements the OpenThread platform abstraction for logging using
 *  Silicon Labs sl_log interface (SL_PRINT_STRING_*).
 *
 *  SL_PRINT_STRING_* is used (not SL_PRINT_EVENT). Format strings remain in
 *  OpenThread; we pass a pre-formatted buffer via "%s" to minimize sl_log
 *  flash usage.
 *
 */

#include <stdarg.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#include <openthread-core-config.h>
#include <openthread/config.h>
#include <openthread/platform/logging.h>

#ifdef SL_COMPONENT_CATALOG_PRESENT
#include "sl_component_catalog.h"
#endif // SL_COMPONENT_CATALOG_PRESENT

#ifdef SL_CATALOG_OT_SL_LOG_PRESENT

#include "sl_log.h"
#include "sl_log_helper.h"

#if (OPENTHREAD_CONFIG_LOG_OUTPUT == OPENTHREAD_CONFIG_LOG_OUTPUT_PLATFORM_DEFINED)
static bool sLogInitialized = false;

void efr32LogInit(void)
{
    sLogInitialized = true;
}

void efr32LogDeinit(void)
{
    sLogInitialized = false;
}

/* sl_log does not provide a va_list variant; format with vsnprintf and pass as string */
static void utilsLogSlOutput(otLogLevel aLogLevel, otLogRegion aLogRegion, const char *aFormat, va_list ap)
{
    OT_UNUSED_VARIABLE(aLogRegion);

    if (!sLogInitialized)
    {
        return;
    }

    char buffer[OPENTHREAD_CONFIG_LOG_MAX_SIZE + 1];
    int  charsWritten = vsnprintf(buffer, sizeof(buffer), aFormat, ap);
    if (charsWritten < 0)
    {
        return;
    }
    switch (aLogLevel)
    {
    case OT_LOG_LEVEL_CRIT:
        SL_PRINT_STRING_ERROR("%s", (uint32_t)(uintptr_t)buffer);
        break;
    case OT_LOG_LEVEL_WARN:
        SL_PRINT_STRING_WARN("%s", (uint32_t)(uintptr_t)buffer);
        break;
    case OT_LOG_LEVEL_NOTE:
    case OT_LOG_LEVEL_INFO:
        SL_PRINT_STRING_INFO("%s", (uint32_t)(uintptr_t)buffer);
        break;
    case OT_LOG_LEVEL_DEBG:
        SL_PRINT_STRING_DEBUG("%s", (uint32_t)(uintptr_t)buffer);
        break;
    case OT_LOG_LEVEL_NONE:
    default:
        return;
    }
}

void otPlatLog(otLogLevel aLogLevel, otLogRegion aLogRegion, const char *aFormat, ...)
{
    va_list ap;

    va_start(ap, aFormat);

    utilsLogSlOutput(aLogLevel, aLogRegion, aFormat, ap);

    va_end(ap);
}

// Instance-aware logging hook
#if OPENTHREAD_CONFIG_LOG_INSTANCE_AWARE_API_ENABLE
void otPlatLogOutput(otInstance *aInstance, otLogLevel aLogLevel, const char *aLogLine)
{
    uint8_t instanceIndex = 0;

    if (aInstance != NULL)
    {
        instanceIndex = otInstanceGetIndex(aInstance);
    }

    otPlatLog(aLogLevel, OT_LOG_REGION_CORE, "[%u] %s", instanceIndex, aLogLine);
}
#endif
#endif

#endif // SL_CATALOG_OT_SL_LOG_PRESENT
