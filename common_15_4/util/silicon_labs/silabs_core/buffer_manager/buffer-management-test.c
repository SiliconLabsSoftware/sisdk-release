/***************************************************************************//**
 * @file
 * @brief Tests for buffer management.
 *******************************************************************************
 * # License
 * <b>Copyright 2018 Silicon Laboratories Inc. www.silabs.com</b>
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
#include "buffer-management.h"
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

// All of the test objects.
static TestObject testObjects[100];
static int testObjectsCount = 0;

//----------------------------------------------------------------
// Forward declarations
static void simpleCompactionTest(uint8_t rootIndex);
static void test(int size, ...);
static void runTest(bool forward, bool addJunk);
static void allocateTestObjects(bool forward, bool addJunk);
static void runCompaction(bool isFirst);
static void checkContents(uint8_t *contents,
                          uint16_t count,
                          uint16_t seed,
                          bool check);
static void checkBuffer(sli_buffer_manager_buffer_t buffer,
                        uint16_t count,
                        uint16_t seed,
                        bool check);
static bool checkLink(int linkIndex, sli_buffer_manager_buffer_t linkObject);

//----------------------------------------------------------------
// A value of "102" for example, adds one buffer to the PHY -> MAC queue
// on the first call and two on the third.

static char *interruptAllocations = "";

#define ISR_OBJECT_SIZE 5

static bool useIndirect = false;

static sli_buffer_manager_buffer_t reallyAllocate(uint8_t index)
{
  TestObject *testObject = testObjects + index;
  sli_buffer_manager_buffer_t buffer;
  bool indirect = useIndirect && (index & 1);

  if (indirect) {
    uint8_t *contents = (uint8_t *) malloc(testObject->size);
    checkContents(contents,
                  testObject->size,
                  index | (testObject->size << 8),
                  false);
    buffer = sli_legacy_buffer_manager_allocate_indirect_buffer(contents, NULL, testObject->size);
  } else {
    buffer = sli_legacy_buffer_manager_allocate_buffer(testObject->size);
  }

  assert(buffer != NULL_BUFFER);
  assert(sli_legacy_buffer_manager_get_buffer_length(buffer) == testObject->size);

  checkBuffer(buffer,
              testObject->size,
              index | (testObject->size << 8),
              indirect);

  testObject->object = buffer;
  testObject->newLocation = NULL_BUFFER;

  return buffer;
}

static sli_buffer_manager_buffer_t allocate(uint8_t index)
{
  return reallyAllocate(index);
}

// Each object in the heap is specified using four values:
//    size root link0 link1
// A size of -1 terminates the list of objects.  A -1 for
// the root or a link means that the object is not a root or
// has no link.

static void testCompaction(void)
{
  sli_legacy_buffer_manager_initialize_buffers();

  assert(heapPointer == emHeapBase);
  memset(roots, 0, sizeof(roots));
  reclaimUnusedBuffers();
  assert(heapPointer == emHeapBase);

  simpleCompactionTest(0);
  simpleCompactionTest(2);
  simpleCompactionTest(ROOT_COUNT - 1);
  simpleCompactionTest(PHY_TO_MAC_QUEUE_ROOT);

  test(80, PHY_TO_MAC_QUEUE_ROOT, 1, -1,        // a queue with two elements
       80, -1, 0, -1,
       -1);

  interruptAllocations = "21";
  test(80, PHY_TO_MAC_QUEUE_ROOT, 1, -1,        // a queue with two elements
       80, -1, 0, -1,
       -1);

  interruptAllocations = "1111";
  test(80, PHY_TO_MAC_QUEUE_ROOT, 1, -1,        // a queue with two elements
       80, -1, 0, -1,
       -1);

  // Same as the simple test, but with two roots
  test(101, 2, 1, -1,
       101, 3, -1, -1,
       -1);

  test(101, 2, -1, 1,
       101, 3, -1, -1,
       -1);

  test(101, 2, 1, 1,
       101, 3, -1, -1,
       -1);

  // A loop
  test(101, 2, -1, 1,
       101, -1, 0, -1,
       -1);

  // A small tree
  test(10, 2, 1, 2,
       10, -1, 3, 4,
       10, -1, 5, 6,
       10, -1, -1, -1,
       10, -1, -1, -1,
       10, -1, -1, -1,
       10, -1, -1, -1,
       -1);

  // A larger tree
  test(10, 2, 1, 2,
       11, -1, 3, 4,
       12, -1, 5, 6,
       13, -1, 7, 8,
       14, -1, 9, 10,
       15, -1, 11, 12,
       16, -1, 13, 14,
       17, -1, 15, 16,
       18, -1, 17, 18,
       19, -1, 19, 20,
       20, -1, 21, 22,
       21, -1, 23, 24,
       22, -1, 25, 26,
       23, -1, 27, 28,
       24, -1, 29, 30,
       25, -1, 31, 32,
       26, -1, -1, -1,
       27, -1, -1, -1,
       28, -1, -1, -1,
       29, -1, -1, -1,
       30, -1, -1, -1,
       31, -1, -1, -1,
       32, -1, -1, -1,
       33, -1, -1, -1,
       34, -1, -1, -1,
       35, -1, -1, -1,
       36, -1, -1, -1,
       37, -1, -1, -1,
       38, -1, -1, -1,
       40, -1, -1, -1,
       41, -1, -1, -1,
       42, -1, -1, -1,
       43, -1, -1, -1,
       -1);

  // Ditto, with some additional roots
  test(10, 2, 1, 2,
       11, -1, 3, 4,
       12, -1, 5, 6,
       13, -1, 7, 8,
       14, -1, 9, 10,
       15, -1, 11, 12,
       16, 7, 13, 14,
       17, -1, 15, 16,
       18, -1, 17, 18,
       19, -1, 19, 20,
       20, -1, 21, 22,
       21, -1, 23, 24,
       22, -1, 25, 26,
       23, 5, 27, 28,
       24, -1, 29, 30,
       25, -1, 31, 32,
       26, -1, -1, -1,
       27, -1, -1, -1,
       28, -1, -1, -1,
       29, -1, -1, -1,
       30, -1, -1, -1,
       31, -1, -1, -1,
       32, -1, -1, -1,
       33, -1, -1, -1,
       34, -1, -1, -1,
       35, 6, -1, -1,
       36, 8, -1, -1,
       37, -1, -1, -1,
       38, -1, -1, -1,
       40, -1, -1, -1,
       41, -1, -1, -1,
       42, -1, -1, -1,
       43, -1, -1, -1,
       -1);

  // A long chain through the second link in order to fill the GC stack.
  // We have to zigzag a bit at the start to get by the initial root
  // scans.
  test(10, 2, -1, 1,
       10, -1, 2, -1,
       10, -1, -1, 3,
       10, -1, 4, 5,
       10, -1, -1, -1,
       10, -1, 6, 7,
       10, -1, -1, -1,
       10, -1, 8, 9,
       10, -1, -1, -1,
       10, -1, 10, 11,
       10, -1, -1, -1,
       10, -1, 12, 13,
       10, -1, -1, -1,
       10, -1, 14, 15,
       10, -1, -1, -1,
       10, -1, 16, 17,
       10, -1, -1, -1,
       10, -1, 18, 19,
       10, -1, -1, -1,
       10, -1, 20, 21,
       10, -1, -1, -1,
       10, -1, 22, 23,
       10, -1, -1, -1,
       10, -1, 24, 25,
       10, -1, -1, -1,
       10, -1, 26, 27,
       10, -1, -1, -1,
       10, -1, 28, 29,
       10, -1, -1, -1,
       10, -1, 30, 31,
       10, -1, -1, -1,
       10, -1, 32, 33,
       10, -1, -1, -1,
       10, -1, 34, 35,
       10, -1, -1, -1,
       10, -1, 36, 37,
       10, -1, -1, -1,
       10, -1, 38, 39,
       10, -1, -1, -1,
       10, -1, 40, 31,
       10, -1, -1, -1,
       10, -1, -1, -1,
       -1);
}

static void simpleCompactionTest(uint8_t rootIndex)
{
  test(100, rootIndex, -1, -1,
       -1);

  test(101, rootIndex, -1, -1,
       -1);

  // Two objects, one of which is a root.
  test(101, rootIndex, -1, -1,
       101, -1, -1, -1,
       -1);

  // Two objects, one linked to the other through either or both links.
  test(101, rootIndex, 1, -1,
       101, -1, -1, -1,
       -1);

  test(101, rootIndex, -1, 1,
       101, -1, -1, -1,
       -1);

  test(101, rootIndex, 1, 1,
       101, -1, -1, -1,
       -1);
}

static void testSetBufferLength(void)
{
  int direction;
  int i;
  TestObject *theObject = testObjects;

  sli_legacy_buffer_manager_initialize_buffers();

  testObjectsCount = 2;

  theObject->root = 1;
  theObject->link0 = -1;
  theObject->link1 = -1;

  testObjects[1].size = 10;
  testObjects[1].root = 2;
  testObjects[1].link0 = -1;
  testObjects[1].link1 = -1;
  for (direction = 0; direction < 2; direction++) {
    for (i = 0; i < 20; i++) {
      theObject->size = 20;
      // Incrementing direction toggles between false then true.
      allocateTestObjects(((bool)direction), false);

      theObject->size = i;
      sli_legacy_buffer_manager_set_buffer_length(theObject->object, i);
      checkBuffer(theObject->object,
                  i,
                  0 | (i << 8),
                  false);

      runCompaction(true);
      runCompaction(false);
    }
  }
}

// Read in the test object data and then run the four test variants.

static void test(int size, ...)
{
  char *savedInterruptAllocations = interruptAllocations;

  va_list argPointer;

  va_start(argPointer, size);
  testObjectsCount = 0;

  while (size != -1) {
    TestObject *testObject = testObjects + testObjectsCount;

    assert(0 < size && size <= 256);

    testObject->size = size;
    testObject->root = va_arg(argPointer, int);
    testObject->link0 = va_arg(argPointer, int);
    testObject->link1 = va_arg(argPointer, int);

    testObjectsCount += 1;
    size = va_arg(argPointer, int);
  }

  va_end(argPointer);

  runTest(true, false);
  interruptAllocations = savedInterruptAllocations;
  runTest(false, false);
  interruptAllocations = savedInterruptAllocations;
  runTest(true, true);
  interruptAllocations = savedInterruptAllocations;
  runTest(false, true);

  printf(".");
}

// 'forward' controls the order in which the objects are created
// in the heap.  true allocates them in the order given, false
// does in the reverse order.
//
// If 'addJunk' is true some additional, unrooted objects are
// added to the heap.

static void runTest(bool forward, bool addJunk)
{
  int i;

  for (i = 0; i < ROOT_COUNT; i++) {
    roots[i] = NULL_BUFFER;
  }

  allocateTestObjects(forward, addJunk);

  // Actually run the GC

  runCompaction(true);
  runCompaction(false);

  // Clear the roots.

  for (i = 0; i < testObjectsCount; i++) {
    TestObject *testObject = testObjects + i;
    if (testObject->root == PHY_TO_MAC_QUEUE_ROOT) {
      phyToMacQueue = NULL_BUFFER;
    } else if (testObject->root != -1) {
      roots[testObject->root] = NULL_BUFFER;
    }
  }

  // Collect everything

  reclaimUnusedBuffers();
  assert(heapPointer == emHeapBase);
}

static void allocateTestObjects(bool forward, bool addJunk)
{
  int i;

  // Create the objects

  for (i = 0; i < testObjectsCount; i++) {
    int index = (forward
                 ? i
                 : testObjectsCount - i - 1);
    TestObject *testObject = testObjects + index;
    sli_buffer_manager_buffer_t object = allocate(index);

    if (testObject->root == PHY_TO_MAC_QUEUE_ROOT) {
      phyToMacQueue = object;
    } else if (testObject->root != -1) {
      roots[testObject->root] = object;
    }

    if (addJunk && (index % 3) == 0) {
      object = sli_legacy_buffer_manager_allocate_buffer(index + 3);
//      fprintf(stderr, "[junk %04X]\n", object);
      assert(object != NULL_BUFFER);
      assert(sli_legacy_buffer_manager_get_buffer_length(object) == index + 3);
    }
  }

  // Set the link values.

  for (i = 0; i < testObjectsCount; i++) {
    TestObject *testObject = testObjects + i;

    if (testObject->link0 != -1) {
      sli_legacy_buffer_manager_set_buffer_link(testObject->object,
                                                0,
                                                testObjects[testObject->link0].object);
    }

    if (testObject->link1 != -1) {
      sli_legacy_buffer_manager_set_buffer_link(testObject->object,
                                                1,
                                                testObjects[testObject->link1].object);
    }
  }
}

// Run the GC and verify that everything is still as it should be.

static void runCompaction(bool isFirst)
{
  int i;
  bool gcDone;
  int oldSize = heapPointer - emHeapBase;

  reclaimUnusedBuffers();

  // Subsequent GCs should leave the size of the heap unchanged.
  if (!isFirst) {
    assert(heapPointer - emHeapBase == oldSize);
  }

  // Get the new locations for the roots.

  for (i = 0; i < testObjectsCount; i++) {
    TestObject *testObject = testObjects + i;

    if (testObject->root == -1) {
      testObject->newLocation = NULL_BUFFER;
    } else {
      if (testObject->root == PHY_TO_MAC_QUEUE_ROOT) {
        testObject->newLocation = phyToMacQueue;
      } else {
        testObject->newLocation = roots[testObject->root];
      }
      assert(testObject->newLocation != NULL_BUFFER);
    }
  }

  // Get the new locations for the links.

  do {
    gcDone = true;

    for (i = 0; i < testObjectsCount; i++) {
      TestObject *testObject = testObjects + i;

      if (testObject->newLocation != NULL_BUFFER) {
        if (!checkLink(testObject->link0,
                       sli_legacy_buffer_manager_get_buffer_link(testObject->newLocation, 0))) {
          gcDone = false;
        }

        if (!checkLink(testObject->link1,
                       sli_legacy_buffer_manager_get_buffer_link(testObject->newLocation, 1))) {
          gcDone = false;
        }
      }
    }
  } while (!gcDone);

  // Check that root objects are still present and correct.

  for (i = 0; i < testObjectsCount; i++) {
    TestObject *testObject = testObjects + i;

    if (testObject->newLocation != NULL_BUFFER) {
      if (!isFirst) {
        assert(testObject->newLocation == testObject->object);
      }
      assert(sli_legacy_buffer_manager_get_buffer_length(testObject->newLocation) == testObject->size);
      checkBuffer(testObject->newLocation,
                  testObject->size,
                  i | (testObject->size << 8),
                  true);
      testObject->object = testObject->newLocation;
    }
  }
}

// Either fill 'buffer' with pseudorandom data or check that it
// contains the correct pseudorandom data.

static void checkContents(uint8_t *contents,
                          uint16_t count,
                          uint16_t seed,
                          bool check)
{
  uint32_t randomValue = seed;
  uint16_t i;

  // fprintf(stderr, "[%d %d %d ", count, seed, check);

  for (i = 0; i < count; i++) {
    randomValue = ((randomValue * 1103515245 + 12345) / 65536) % 32768;
    if (check) {
      if (!(0
            && i < sizeof(sli_buffer_manager_buffer_t *))) {
        // fprintf(stderr, "%c%02X", i == 0 ? '[' : ' ', contents[i]);
        assert(contents[i] == (randomValue & 0xFF));
      }
    } else {
      contents[i] = randomValue & 0xFF;
      // fprintf(stderr, "%c%02X", i == 0 ? '[' : ' ', contents[i]);
    }
  }
  // fprintf(stderr, "]]\n");
}

static void checkBuffer(sli_buffer_manager_buffer_t buffer,
                        uint16_t count,
                        uint16_t seed,
                        bool check)
{
  checkContents(sli_legacy_buffer_manager_get_buffer_pointer(buffer),
                count,
                seed,
                check);
}

// Check that a link field has the correct value.  If this is
// the first reference to the linked object we record its new
// location.
//
// Returns true if this is the first reference to the linked
// object.

static bool checkLink(int linkIndex, sli_buffer_manager_buffer_t linkObject)
{
  if (linkIndex == -1) {
    assert(linkObject == NULL_BUFFER);
    return true;
  } else {
    sli_buffer_manager_buffer_t *newLocation = &testObjects[linkIndex].newLocation;

    assert(linkObject != NULL_BUFFER);

    if (*newLocation == NULL_BUFFER) {
      *newLocation = linkObject;
      return false;
    } else {
      assert(*newLocation == linkObject);
      return true;
    }
  }
}

//----------------------------------------------------------------
// Testing queues

// Utility functions for checking buffer queues.  These use strings
// to represent the contents of a queue.  "ABC" is a queue with buffer 0
// as the head, buffer 1 next, and then buffer 2 as the tail.

#define elementCount 8

static sli_buffer_manager_buffer_t elements[elementCount];

static void fillQueue(sli_buffer_manager_buffer_t *queue, char *contents)
{
  *queue = NULL_BUFFER;
  assert(sli_legacy_buffer_manager_buffer_queue_is_empty(queue));
  assert(sli_legacy_buffer_manager_buffer_queue_byte_length(queue) == 0);

  for (; *contents; contents++) {
    sli_legacy_buffer_manager_buffer_queue_add(queue, elements[*contents - 'A']);
  }
}

static void checkQueue(sli_buffer_manager_buffer_t *queue, char *contents)
{
  sli_buffer_manager_buffer_t finger = sli_legacy_buffer_manager_buffer_queue_head(queue);
  while (finger != NULL_BUFFER) {
    assert(finger == elements[*contents - 'A']);
    contents += 1;
    finger = sli_legacy_buffer_manager_buffer_queue_next(queue, finger);
  }
  assert(!*contents);
}

static void removeBuffers(sli_buffer_manager_buffer_t *queue, char *contents)
{
  for (; *contents; contents++) {
    sli_legacy_buffer_manager_buffer_queue_remove(queue, elements[*contents - 'A']);
  }
}

// Put the 'start' buffers in queue, remove the ones in 'remove', and
// then check that the queue looks like 'result'.

static void removeBufferTest(char *start, char *myRemove, char *result)
{
  sli_buffer_manager_buffer_t queue;
  fillQueue(&queue, start);
  removeBuffers(&queue, myRemove);
  checkQueue(&queue, result);
}

static void testBufferQueues(void)
{
  uint8_t i;
  uint16_t n = 0;
  uint8_t queueLength;
  sli_buffer_manager_buffer_t queue = NULL_BUFFER;

  sli_legacy_buffer_manager_initialize_buffers();

  for (i = 0; i < elementCount; i++) {
    sli_buffer_manager_buffer_t element = sli_legacy_buffer_manager_allocate_buffer(i + 1);
    uint8_t j;
    assert(element != NULL_BUFFER);
    for (j = 0; j < i + 1; j++) {
      sli_legacy_buffer_manager_get_buffer_pointer(element)[j] = n++;
    }
    elements[i] = element;
  }

  printf(".");

  for (queueLength = 0; queueLength <= elementCount; queueLength++) {
    assert(sli_legacy_buffer_manager_buffer_queue_is_empty(&queue));
    //fprintf(stderr, "adding: ");
    for (i = 0; i < queueLength; i++) {
      sli_legacy_buffer_manager_buffer_queue_add(&queue, elements[i]);
      //fprintf(stderr, "%d ", i);
    }
    assert(sli_legacy_buffer_manager_buffer_queue_byte_length(&queue)
           == (queueLength * (queueLength + 1)) / 2);

    if (queueLength == elementCount) {
      uint8_t temp[1000];
      for (i = 0; i < n; i++) {
        uint16_t j;
        memset(temp, 0xFF, sizeof(temp));
        sli_legacy_buffer_manager_copy_from_buffer_queue(&queue, i, temp);
        for (j = 0; j < i; j++) {
          assert(temp[j] == j);
        }
        for (j = i; j < sizeof(temp); j++) {
          assert(temp[j] == 0xFF);
        }
      }
    }

    //fprintf(stderr, "\nremoving: ");
    for (i = 0; i < queueLength; i++) {
      sli_buffer_manager_buffer_t head = sli_legacy_buffer_manager_buffer_queue_remove_head(&queue);
      assert(head != NULL_BUFFER);
      assert(head == elements[i]);
      //fprintf(stderr, "%d ", i);
    }
    assert(sli_legacy_buffer_manager_buffer_queue_remove_head(&queue) == NULL_BUFFER);
    assert(sli_legacy_buffer_manager_buffer_queue_is_empty(&queue));
    //fprintf(stderr, "\nempty\n");
  }

  removeBufferTest("", "", "");
  removeBufferTest("", "A", "");

  removeBufferTest("A", "", "A");
  removeBufferTest("A", "B", "A");
  removeBufferTest("A", "A", "");

  removeBufferTest("BC", "", "BC");
  removeBufferTest("BC", "D", "BC");
  removeBufferTest("BC", "B", "C");
  removeBufferTest("BC", "C", "B");

  removeBufferTest("BCD", "", "BCD");
  removeBufferTest("BCD", "E", "BCD");
  removeBufferTest("BCD", "B", "CD");
  removeBufferTest("BCD", "C", "BD");
  removeBufferTest("BCD", "D", "BC");

  printf(".");

  // Test interactions between queues and sli_legacy_buffer_manager_reclaim_unused_buffers().
  {
    uint16_t remaining;
    clearRoots();
    sli_legacy_buffer_manager_buffer_queue_add(&roots[1], elements[0]);
    sli_legacy_buffer_manager_buffer_queue_add(&roots[1], elements[1]);
    roots[0] = sli_legacy_buffer_manager_buffer_queue_remove_head(&roots[1]);
    reclaimUnusedBuffers();
    // 2 buffers are in use. roots[0] is a single buffer (not a queue).
    // roots[1] is a queue containing one buffer.
    remaining = sli_legacy_buffer_manager_buffer_bytes_remaining();
    sli_legacy_buffer_manager_buffer_queue_remove_head(&roots[1]);
    reclaimUnusedBuffers();
    // 1 buffer is in use. roots[0] is a single buffer. roots[1] is an
    // empty queue.
    assert(sli_legacy_buffer_manager_buffer_bytes_remaining() > remaining);
    remaining = sli_legacy_buffer_manager_buffer_bytes_remaining();
    roots[0] = NULL_BUFFER;
    reclaimUnusedBuffers();
    // 0 buffers are in use.
    assert(sli_legacy_buffer_manager_buffer_bytes_remaining() > remaining);
    assert(heapPointer == emHeapBase);
  }
}

#if 0
static void printHeap(void)
{
  uint16_t *finger = emHeapBase;
  while (finger < heapPointer) {
    uint16_t size = 4 + (((finger[1] & 0x1FFF) + 1) >> 1);
    sli_buffer_manager_buffer_t b = (finger - emHeapBase) + 1;
    printf("%04X:\n", b);
    uint16_t i;
    for (i = 0; i < size; i++) {
      printf("  %04x\n", finger[i]);
    }
    printf("  new loc = %04X\n", finger[0]);
    printf("  size    = %u\n", finger[1]);
    printf("  link 0  = %04X\n", finger[2]);
    printf("  link 1  = %04X\n", finger[3]);
    printf("  contents = '%.*s'\n",
           sli_legacy_buffer_manager_get_buffer_length(b), sli_legacy_buffer_manager_get_buffer_pointer(b));
    finger += size;
  }
}
#endif

static void heapToString(char *result)
{
  char *output = result;
  *output = 0;
  uint16_t *finger = emHeapBase;
  while (finger < heapPointer) {
    // This has to duplicate the header overhead (the 4) and the alignment
    // (the (((... + 3) >> 2) < 1) ) that the buffer management code uses.
    // Having our own code for this makes the testing more independent.
    uint16_t size = 4 + ((((finger[1] & 0x1FFF) + 3) >> 2) << 1);
    sli_buffer_manager_buffer_t b = (finger - emHeapBase) + 1;
    uint16_t length = sli_legacy_buffer_manager_get_buffer_length(b);
    memcpy(output, sli_legacy_buffer_manager_get_buffer_pointer(b), length);
    output += length;
    *output++ = ' ';
    finger += size;
  }
  if (output > result) {
    output--;
    *output = 0;
  }
}

static int getBufferNumber(sli_buffer_manager_buffer_t b)
{
  char contents[50];
  uint16_t length = sli_legacy_buffer_manager_get_buffer_length(b);
  assert(length < sizeof(contents));
  memcpy(contents, sli_legacy_buffer_manager_get_buffer_pointer(b), length);
  contents[length] = 0;
  return atoi(contents + 1);
}

static void addInOrder(sli_buffer_manager_buffer_t *queue, sli_buffer_manager_buffer_t b)
{
  int n = getBufferNumber(b);
  sli_buffer_manager_buffer_t temp = *queue;
  *queue = NULL_BUFFER;
  while (!sli_legacy_buffer_manager_buffer_queue_is_empty(&temp)) {
    sli_buffer_manager_buffer_t next = sli_legacy_buffer_manager_buffer_queue_remove_head(&temp);
    if (n > 0 && getBufferNumber(next) > n) {
      sli_legacy_buffer_manager_buffer_queue_add(queue, b);
      n = -1;
    }
    sli_legacy_buffer_manager_buffer_queue_add(queue, next);
  }
  if (n > 0) {
    sli_legacy_buffer_manager_buffer_queue_add(queue, b);
  }
}

static void testAmalgamate(char *before, char *after)
{
  sli_legacy_buffer_manager_initialize_buffers();
  clearRoots();
  while (true) {
    uint8_t length = 0;
    while (before[length] != ' ' && before[length] != 0) {
      length++;
    }
    sli_buffer_manager_buffer_t b = sli_legacy_buffer_manager_fill_buffer((uint8_t*)before, length);
    switch (before[0]) {
      case 'A':
        addInOrder(&roots[0], b);
        break;
      case 'B':
        addInOrder(&roots[1], b);
        break;
      case 'C':
        roots[2] = b;
        break;
    }
    before += length;
    if (before[0] == ' ') {
      before++;
    } else {
      assert(before[0] == 0);
      break;
    }
  }
  uint8_t scratchpad[30];
  amalgamate = true;
  sli_legacy_buffer_manager_reclaim_unused_buffers_and_amalgamate(markers, scratchpad, sizeof(scratchpad));
  amalgamate = false;
  char heapString[1000];
  heapToString(heapString);
  if (strcmp(after, heapString) != 0) {
    printf("Expected '%s', got '%s'\n", after, heapString);
    assert(false);
  }
  //printHeap();
}

//----------------------------------------------------------------

int main(int argc, char **argv)
{
  printf("[Testing buffer-gc ");

  testCompaction();
  testSetBufferLength();

  useIndirect = true;
  testCompaction();
  testSetBufferLength();

  testBufferQueues();
  testAmalgamate("A1 A2 A3", "A1A2 A3");
  testAmalgamate("A1 B1 B2 A2 B3 Z0 B4", "A1A2 B1 B2 B3 B4");
  testAmalgamate("A3 A2 B1 B2 A1 B3 Z0 B4", "A3 B1 B2 A1A2 B3 B4");
  testAmalgamate("A3 B1 B2 A1A2 B3 B4", "B1 B2 A1A2A3 B3 B4");
  testAmalgamate("A1 B1 A2", "A1A2 B1");
  testAmalgamate("Z00 B1 Z A1 B2 Z A02 Z00 B3", "B1 A1A02 B2 B3");

  // Test that copying forward over the final, non-live buffer doesn't
  // break anything.  The \x escapes are needed to get the high bit set
  // so that the copied data looks like a live object ('live' flag is
  // bit 0x8000).
  testAmalgamate("A1 C\xFF\xFF\xFF\xFF A2000", "A1A2000 C\xFF\xFF\xFF\xFF");

  printf(" done]\n");

  return 0;
}
