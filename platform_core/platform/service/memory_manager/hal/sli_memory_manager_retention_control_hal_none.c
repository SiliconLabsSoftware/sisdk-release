/***************************************************************************//**
 * @file
 * @brief Memory Manager Retention Control Empty HAL.
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

#include <stddef.h>
#include <stdint.h>
#include "sli_memory_manager.h"
#include "sli_memory_manager_retention_control.h"
#include "sli_code_classification.h"
#include "em_device.h"
#include "sl_assert.h"

#if !defined(DMEM_MEM_BASE)
#define DMEM_MEM_BASE  SRAM_BASE
#endif

#if !defined(DMEM_NUM_BANKS)
// On XG21 DMEM_NUM_BANKS is named DMEM_NUM_BANK
#if defined(DMEM_NUM_BANK)
#define DMEM_NUM_BANKS DMEM_NUM_BANK
// On XG26 DMEM_NUM_BANKS is named DMEM0_NUM_BANKS
#elif defined(DMEM0_NUM_BANKS)
#define DMEM_NUM_BANKS DMEM0_NUM_BANKS
#define DMEM_BANK0_SIZE DMEM0_BANK0_SIZE
#elif defined(HOSTDMEM_NUM_BANKS)
#define DMEM_NUM_BANKS HOSTDMEM_NUM_BANKS
#define DMEM_BANK0_SIZE HOSTDMEM_BANK0_SIZE
#endif
#endif

static uint32_t memory_manager_dmem_get_bank_id(void *addr);
static uintptr_t memory_manager_dmem_get_bank_start_address_by_id(uint32_t bank_id);
static void memory_manager_dmem_enable_retention(uint32_t bank_id);
static void memory_manager_dmem_disable_retention(uint32_t bank_id);
static sli_bank_coverage_t memory_manager_dmem_get_block_bank_coverage(void *start_addr,
                                                                       uint32_t block_size);

// Banks allocation counters for DMEM.
static uint16_t dmem_banks_counter[DMEM_NUM_BANKS] SLI_MEMORY_MANAGER_GLOBAL_VARIABLE_ATTRIBUTES = { 0 };

// DMEM RAM type.
static sli_retention_control_t retention_control_dmem SLI_MEMORY_MANAGER_GLOBAL_VARIABLE_ATTRIBUTES = {
  .bank_size = DMEM_BANK0_SIZE,
  .banks_counter = dmem_banks_counter,
  .get_bank_id = memory_manager_dmem_get_bank_id,
  .get_bank_start_address_by_id = memory_manager_dmem_get_bank_start_address_by_id,
  .enable_retention = memory_manager_dmem_enable_retention,
  .disable_retention = memory_manager_dmem_disable_retention,
  .get_block_bank_coverage = memory_manager_dmem_get_block_bank_coverage,
};

/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/

/***************************************************************************//**
 * Initialize Memory Manager related hardware.
 ******************************************************************************/
void sli_memory_manager_hal_init(void)
{
  // No hardware initialization needed.
}

/***************************************************************************//**
 * Initialize Memory Manager HAL for the given heap.
 ******************************************************************************/
void sli_memory_manager_hal_heap_init(sl_memory_heap_t *heap)
{
  heap->retention_control = &retention_control_dmem;
}

/***************************************************************************//**
 * Gets RAM bank ID from address.
 ******************************************************************************/
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_MEMORY_MANAGER, SL_CODE_CLASS_TIME_CRITICAL)
uint32_t sli_memory_manager_get_bank_id_by_addr(const sl_memory_heap_t *heap,
                                                void *addr)
{
  // Validate given address.
  EFM_ASSERT((addr >= heap->base_addr) && (addr <= (void *)((uint8_t *)heap->base_addr + heap->size)));
  uint32_t bank_id;
  sli_retention_control_t *retention_control = (sli_retention_control_t *)heap->retention_control;

  // Get the bank ID as if all banks were of the same size being the smallest
  // bank size for the given heap.
  bank_id = retention_control->get_bank_id(addr);

  return bank_id;
}

/***************************************************************************//**
 * Gets the address of the start of a RAM bank.
 ******************************************************************************/
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_MEMORY_MANAGER, SL_CODE_CLASS_TIME_CRITICAL)
uintptr_t sli_memory_manager_get_bank_start_address_by_id(const sl_memory_heap_t *heap,
                                                          uint32_t bank_id)
{
  sli_retention_control_t *retention_control =
    (sli_retention_control_t *)heap->retention_control;

  EFM_ASSERT(retention_control != NULL);
  return retention_control->get_bank_start_address_by_id(bank_id);
}

/***************************************************************************//**
 * Increments Bank Counters between a start bank ID and an end bank ID.
 ******************************************************************************/
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_MEMORY_MANAGER, SL_CODE_CLASS_TIME_CRITICAL)
void sli_memory_manager_increment_bank_counter(sl_memory_heap_t *heap,
                                               uint32_t start_id,
                                               uint32_t end_id)
{
  EFM_ASSERT(start_id <= end_id);
  sli_retention_control_t *retention_control = (sli_retention_control_t *)heap->retention_control;

  for (uint32_t id = start_id; id <= end_id; id++) {
    retention_control->banks_counter[id]++;
    retention_control->enable_retention(id);
  }
}

/***************************************************************************//**
 * Decrements Bank Counters between a start bank ID and an end bank ID.
 ******************************************************************************/
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_MEMORY_MANAGER, SL_CODE_CLASS_TIME_CRITICAL)
void sli_memory_manager_decrement_bank_counter(sl_memory_heap_t *heap,
                                               uint32_t start_id,
                                               uint32_t end_id)
{
  EFM_ASSERT(start_id <= end_id);
  sli_retention_control_t *retention_control = (sli_retention_control_t *)heap->retention_control;

  for (uint32_t id = start_id; id <= end_id; id++) {
    retention_control->banks_counter[id]--;
    if (!retention_control->banks_counter[id]) {
      retention_control->disable_retention(id);
    }
  }
}

/***************************************************************************//**
 * Adds size_bytes to retained_size (retention statistics). No-op when disabled.
 ******************************************************************************/
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_MEMORY_MANAGER, SL_CODE_CLASS_TIME_CRITICAL)
void sli_memory_manager_retention_add_size(sl_memory_heap_t *heap,
                                           size_t size_bytes)
{
  (void)heap;
  (void)size_bytes;
}

/***************************************************************************//**
 * Subtracts size_bytes from retained_size (retention statistics). No-op when disabled.
 ******************************************************************************/
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_MEMORY_MANAGER, SL_CODE_CLASS_TIME_CRITICAL)
void sli_memory_manager_retention_subtract_size(sl_memory_heap_t *heap,
                                                size_t size_bytes)
{
  (void)heap;
  (void)size_bytes;
}

/***************************************************************************//**
 * Updates the retained high watermark from the current retained_size. No-op when disabled.
 ******************************************************************************/
void sli_memory_manager_retention_update_high_watermark(const sl_memory_heap_t *heap)
{
  (void)heap;
}

/*******************************************************************************
 **************************   LOCAL FUNCTIONS   *******************************
 ******************************************************************************/

/***************************************************************************//**
 * Get DMEM bank ID.
 *
 * @param[in]  addr  Address.
 *
 * @return  DMEM bank ID.
 ******************************************************************************/
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_MEMORY_MANAGER, SL_CODE_CLASS_TIME_CRITICAL)
static uint32_t memory_manager_dmem_get_bank_id(void *addr)
{
  return ((size_t)((uint8_t *)addr - DMEM_MEM_BASE) / DMEM_BANK0_SIZE);
}

/***************************************************************************//**
 * Get DMEM bank start address from bank ID.
 ******************************************************************************/
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_MEMORY_MANAGER, SL_CODE_CLASS_TIME_CRITICAL)
static uintptr_t memory_manager_dmem_get_bank_start_address_by_id(uint32_t bank_id)
{
  return (uintptr_t)DMEM_MEM_BASE + (uintptr_t)bank_id * (uintptr_t)DMEM_BANK0_SIZE;
}

/***************************************************************************//**
 * Enable the retention for a given DMEM bank ID.
 *
 * @param[in]  bank_id  Bank ID.
 ******************************************************************************/
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_MEMORY_MANAGER, SL_CODE_CLASS_TIME_CRITICAL)
static void memory_manager_dmem_enable_retention(uint32_t bank_id)
{
  (void)bank_id;
}

/***************************************************************************//**
 * Disable the retention for a given DMEM bank ID.
 *
 * @param[in]  bank_id  Bank ID.
 ******************************************************************************/
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_MEMORY_MANAGER, SL_CODE_CLASS_TIME_CRITICAL)
static void memory_manager_dmem_disable_retention(uint32_t bank_id)
{
  (void)bank_id;
}

/***************************************************************************//**
 * Get the bank coverage of a pool block in DMEM.
 * The block may span multiple banks.
 *
 * @param[in]  start_addr   Pointer to the start address of the block.
 * @param[in]  block_size  Size of the block.
 *
 * @return     The bank coverage of the block.
 ******************************************************************************/
SL_CODE_CLASSIFY(SL_CODE_COMPONENT_MEMORY_MANAGER, SL_CODE_CLASS_TIME_CRITICAL)
static sli_bank_coverage_t memory_manager_dmem_get_block_bank_coverage(void *start_addr,
                                                                       uint32_t block_size)
{
  sli_bank_coverage_t block_coverage;

  // Assumes consistent bank sizes.
  block_coverage.start = ((uintptr_t)start_addr - (uintptr_t)DMEM_MEM_BASE) / DMEM_BANK0_SIZE;
  block_coverage.end = (((uintptr_t)start_addr + block_size - 1) - (uintptr_t)DMEM_MEM_BASE) / DMEM_BANK0_SIZE;

  return block_coverage;
}
