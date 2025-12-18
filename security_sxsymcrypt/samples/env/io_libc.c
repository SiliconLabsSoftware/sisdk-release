#include <stdio.h>
#include <stdlib.h>

void displaymsg(const char *msg)
{
    fprintf(stderr, "%s", msg);
}

void display(const char *msg, int v)
{
    fprintf(stderr, "%s %d\n", msg, v);
}

size_t readdata(void *dst, size_t sz)
{
    return fread(dst, 1, sz, stdin);
}

void writedata(const void *src, size_t sz)
{
    fwrite(src, 1, sz, stdout);
}

void sx_abort(void)
{
    abort();
}
