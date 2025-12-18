/***************************************************************************//**
 * @file
 * @brief Tests for buffer management.
 *******************************************************************************
 * # License
 * <b>Copyright 2023 Silicon Laboratories Inc. www.silabs.com</b>
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

#include <stdlib.h>
#include "core/sl_zigbee_stack.h"

// Normally static values that we use for checking.
extern uint16_t *emHeapBase;
extern uint16_t *heapPointer;
extern sli_buffer_manager_buffer_t phyToMacQueue;

//Stubs to build test from zigbee
uint8_t sl_zigbee_endpoint_count = 0;
sl_zigbee_endpoint_t sl_zigbee_endpoints[] = {};

// A representation of an object in the heap.  The first four values
// are specified by the test.

typedef struct {
  int size;     // number of bytes
  int root;     // location in the array of roots, or -1 if not a root
  int link0;    // index of the TestObject for the first link, or -1
  int link1;    // index of the TestObject for the second link, or -1
  sli_buffer_manager_buffer_t object;            // the actual allocated object
  sli_buffer_manager_buffer_t newLocation;       // new location after compaction
} TestObject;

#define ROOT_COUNT 16
#define PHY_TO_MAC_QUEUE_ROOT ROOT_COUNT
static sli_buffer_manager_buffer_t roots[ROOT_COUNT];
static bool amalgamate = false;

static void markRoots(void)
{
  uint16_t i;
  if (amalgamate) {
    sli_legacy_buffer_manager_mark_amalgamate_queue(roots);
  } else {
    sli_legacy_buffer_manager_mark_buffer(roots);
  }

  for (i = 1; i < ROOT_COUNT; i++) {
    sli_legacy_buffer_manager_mark_buffer(roots + i);
  }
}

static BufferMarker const markers[] = {
  markRoots,
  NULL
};

static void reclaimUnusedBuffers(void)
{
  sli_legacy_buffer_manager_reclaim_unused_buffers(markers);
}

static void clearRoots(void)
{
  memset(roots, 0, sizeof(roots));
}

static void testGCDualPhy(void)
{
  sli_legacy_buffer_manager_initialize_buffers();
  assert(heapPointer == emHeapBase);
  reclaimUnusedBuffers();
  clearRoots();
}
//----------------------------------------------------------------

int main(int argc, char **argv)
{
  printf("[Testing dual phy buffer-gc ");
  testGCDualPhy();
  printf(" ... done]\n");
  return 0;
}
