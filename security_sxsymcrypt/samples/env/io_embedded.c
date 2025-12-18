
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "../rawpatterns.c"

void displaymsg(const char *msg)
{
    /* Due to particularities of the test bench, the fprintf is needed.
     * It should be removed in custom builds. */
    fprintf(stderr, "%s", msg);
}


void display(const char *msg, int v)
{
    /* Due to particularities of the test bench, the fprintf is needed.
     * It should be removed in custom builds. */
    fprintf(stderr, "%s %d\n", msg, v);
}

size_t readdata(void *dst, size_t sz)
{
    static size_t current_processed_sz = 0;
    static size_t rawpatterns_sz = sizeof(rawpatterns) - 1;
    size_t processed_sz = sz;

    if (current_processed_sz + sz > rawpatterns_sz)
        processed_sz = rawpatterns_sz - current_processed_sz;

    memcpy(dst, &rawpatterns[current_processed_sz], processed_sz);
    current_processed_sz += processed_sz;

    return processed_sz;
}

void writedata(const void *src, size_t sz)
{
    (void)src;
    (void)sz;
}


void sx_abort(void)
{
    while(1) {
    }
}
