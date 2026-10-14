/*
 * SPDX-License-Identifier: LicenseRef-MSLA
 * Copyright (c) 2024 Silicon Laboratories Inc. (www.silabs.com)
 *
 * The licensor of this software is Silicon Laboratories Inc. Your use of this
 * software is governed by the terms of the Silicon Labs Master Software License
 * Agreement (MSLA) available at [1].  This software is distributed to you in
 * Object Code format and/or Source Code format and is governed by the sections
 * of the MSLA applicable to Object Code, Source Code and Modified Open Source
 * Code. By using this software, you agree to the terms of the MSLA.
 *
 * [1]: https://www.silabs.com/about-us/legal/master-software-license-agreement
 */

#include <string.h>
#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#include <inttypes.h>
#include "sl_core.h"
#include "sli_memory_manager.h"
#include "sl_wisun_trace_api.h"
#include "sl_wisun_alloc.h"
#include "sl_wisun_alloc_config.h"
#include "sl_wisun_common.h"

SL_ALIGN(8) static uint8_t sli_wisun_heap[SL_WISUN_ALLOC_HEAP_SIZE] SL_ATTRIBUTE_ALIGN(8);
static sl_memory_heap_t sli_wisun_heap_handle = { 0 };

static void sli_wisun_heap_init(void)
{
    sl_memory_heap_t *h = &sli_general_purpose_heap;

    if (sli_wisun_heap_handle.base_addr) {
        return;
    }
    sli_memory_create_heap(sli_wisun_heap, SL_WISUN_ALLOC_HEAP_SIZE, SL_MEMORY_HEAP_ALLOC_CPU_RAM, &sli_wisun_heap_handle);

    // Link the new heap after the general purpose one so sli_memory_get_heap_handle can find it
    while (h->next_handle != NULL && h->next_handle != &sli_wisun_heap_handle) {
        h = h->next_handle;
    }
    if (h->next_handle != &sli_wisun_heap_handle) {
        h->next_handle = &sli_wisun_heap_handle;
    }
}

static uint32_t sli_wisun_get_block_length(void *ptr)
{
    if (!sl_wisun_is_heap_block(ptr)) {
        return 0;
    }
    sli_block_metadata_t *block = (sli_block_metadata_t *)((uint8_t *)ptr - SLI_BLOCK_METADATA_SIZE_BYTE);
    return SLI_BLOCK_LEN_DWORD_TO_BYTE(sli_block_len_dword_decode(block));
}

/*****************************************************************************/
// Public APIs
// These APIs are used by the security components to allocate and free memory
/*****************************************************************************/

void *sl_wisun_calloc(size_t nmemb, size_t size)
{
    void *ptr = NULL;

    sli_wisun_heap_init();

    sl_memory_heap_calloc(&sli_wisun_heap_handle, nmemb, size, BLOCK_TYPE_SHORT_TERM, &ptr);
    if (!ptr) {
        sl_wisun_trace_debug("wisun_alloc(%"PRIu32"): fallback", (uint32_t)(nmemb * size));
        ptr = sl_calloc(nmemb, size);
    }
    return ptr;
}

void *sl_wisun_realloc(void *ptr, size_t size)
{
    void *new_ptr = NULL;

    sli_wisun_heap_init();

    if (ptr == NULL) {
        return sl_wisun_calloc(1, size);
    }
    if (size == 0) {
        sl_wisun_free(ptr);
        return NULL;
    }
    if (!sl_wisun_is_heap_block(ptr)) {
        return sl_realloc(ptr, size);
    }

    sl_memory_heap_realloc(&sli_wisun_heap_handle, ptr, (uint32_t)size, &new_ptr);
    if (!new_ptr) {
        sl_wisun_trace_debug("wisun_realloc(%"PRIu32"): fallback", (uint32_t)size);
        new_ptr = sl_malloc(size);
        if (new_ptr) {
            memcpy(new_ptr, ptr, MIN(sli_wisun_get_block_length(ptr), size));
            sl_wisun_free(ptr);
        }
    }
    return new_ptr;
}

void sl_wisun_free(void *ptr)
{
    if (!ptr) {
        return;
    }
    if (!sl_wisun_is_heap_block(ptr)) {
        sl_free(ptr);
    } else {
        sl_memory_heap_free(&sli_wisun_heap_handle, ptr);
    }
}

bool sl_wisun_is_heap_block(void *ptr)
{
    if (sli_wisun_heap_handle.base_addr
        && sli_memory_get_heap_handle(ptr) == &sli_wisun_heap_handle) {
        return true;
    }
    return false;
}

void sl_wisun_heap_get_stats(uint32_t *used_size, uint32_t *high_watermark)
{
    if (used_size) {
        *used_size = sl_memory_heap_get_used_size(&sli_wisun_heap_handle);
    }
    if (high_watermark) {
        *high_watermark = sl_memory_heap_get_high_watermark(&sli_wisun_heap_handle);
    }
}
