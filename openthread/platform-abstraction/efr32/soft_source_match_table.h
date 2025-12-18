/*
 *  Copyright (c) 2023, The OpenThread Authors.
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
 * @file
 * @brief
 *   This file defines the software source match table interfaces used by
 *   soft_source_match_table.c.
 */

#ifndef SOFT_SOURCE_MATCH_TABLE_H
#define SOFT_SOURCE_MATCH_TABLE_H

#include "openthread-core-config.h"
#include <openthread/platform/radio.h>

#include <stdint.h>

// Include config file that defines RADIO_CONFIG_MAX_SRC_MATCH_ENTRIES
// This ensures the macro is defined before it's used below
// First check if it was already included via openthread-core-config.h
#ifndef _SL_OPENTHREAD_FEATURES_CONFIG_H
// If not included yet, try to include via the macro mechanism (same as openthread-core-config.h)
// This is the preferred method as it matches how openthread-core-config.h includes it
#ifdef SL_OPENTHREAD_STACK_FEATURES_CONFIG_FILE
#include SL_OPENTHREAD_STACK_FEATURES_CONFIG_FILE
#else
// Fallback: try direct include if macro isn't defined
// Use __has_include if available to check for file existence before including
#if defined(__has_include)
#if __has_include("sl_openthread_features_config.h")
#include "sl_openthread_features_config.h"
#elif __has_include(<sl_openthread_features_config.h>)
#include <sl_openthread_features_config.h>
#endif
#else
// If __has_include is not available (older compilers), try direct include
// This will cause a compilation error if the file doesn't exist, which is expected
// for configurations that require the config file
#include "sl_openthread_features_config.h"
#endif
#endif
#endif

// If RADIO_CONFIG_MAX_SRC_MATCH_ENTRIES is still not defined, provide a default
// This can happen if the config file wasn't included or doesn't define it
#ifndef RADIO_CONFIG_MAX_SRC_MATCH_ENTRIES
#define RADIO_CONFIG_MAX_SRC_MATCH_ENTRIES OPENTHREAD_CONFIG_MLE_MAX_CHILDREN
#endif

#ifdef __cplusplus
extern "C" {
#endif

#ifndef RADIO_CONFIG_SRC_MATCH_SHORT_ENTRY_NUM
#define RADIO_CONFIG_SRC_MATCH_SHORT_ENTRY_NUM RADIO_CONFIG_MAX_SRC_MATCH_ENTRIES
#endif

#ifndef RADIO_CONFIG_SRC_MATCH_EXT_ENTRY_NUM
#define RADIO_CONFIG_SRC_MATCH_EXT_ENTRY_NUM RADIO_CONFIG_MAX_SRC_MATCH_ENTRIES
#endif

#ifndef RADIO_CONFIG_SRC_MATCH_PANID_NUM
#define RADIO_CONFIG_SRC_MATCH_PANID_NUM RADIO_INTERFACE_COUNT
#endif

#if RADIO_CONFIG_SRC_MATCH_SHORT_ENTRY_NUM || RADIO_CONFIG_SRC_MATCH_EXT_ENTRY_NUM
void utilsSoftSrcMatchSetPanId(otInstance *aInstance, uint16_t aPanId);
#endif // RADIO_CONFIG_SRC_MATCH_SHORT_ENTRY_NUM || RADIO_CONFIG_SRC_MATCH_EXT_ENTRY_NUM

#if RADIO_CONFIG_SRC_MATCH_SHORT_ENTRY_NUM
int16_t utilsSoftSrcMatchShortFindEntry(otInstance *aInstance, uint16_t aShortAddress);
#endif // RADIO_CONFIG_SRC_MATCH_SHORT_ENTRY_NUM

#if RADIO_CONFIG_SRC_MATCH_EXT_ENTRY_NUM
int16_t utilsSoftSrcMatchExtFindEntry(otInstance *aInstance, const otExtAddress *aExtAddress);
#endif // RADIO_CONFIG_SRC_MATCH_EXT_ENTRY_NUM

#ifdef __cplusplus
} // extern "C"
#endif

#endif // SOFT_SOURCE_MATCH_TABLE_H
