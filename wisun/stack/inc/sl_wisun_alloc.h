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

#ifndef SL_WISUN_ALLOC_H
#define SL_WISUN_ALLOC_H

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

void *sl_wisun_calloc(size_t nmemb, size_t size);
void *sl_wisun_realloc(void *ptr, size_t size);
void sl_wisun_free(void *ptr);
bool sl_wisun_is_heap_block(void *ptr);
void sl_wisun_heap_get_stats(uint32_t *used_size, uint32_t *high_watermark);

#endif // SL_WISUN_ALLOC_H
