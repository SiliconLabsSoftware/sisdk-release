#ifndef IO_HEADERFILE
#define IO_HEADERFILE

#include <stddef.h>

#ifndef CFG_REPORT_LVL
#define CFG_REPORT_LVL 1
#endif

void display(const char *msg, int v);
void displaymsg(const char *msg);
size_t readdata(void *dst, size_t sz);
void writedata(const void *src, size_t sz);
void sx_abort(void);

#if (CFG_REPORT_LVL == 0)
#define displaymsg(msg) do {} while(0)
#define display(msg, v) do {} while(0)
#endif

#if CFG_REPORT_LVL > 2
#define REPORT_PROGRESS(msg, v) displaymsg(msg); display((v) ? "FAIL":"OK", (v));
#else
#define REPORT_PROGRESS(msg, v) do {} while(0)
#endif

#define REPORT_SUMMARY(cnt, wrong) display("processed", cnt); display("failures", wrong);
#define DISPLAY_ERROR(msg) displaymsg(msg);

#ifdef NDEBUG
#define assert(expr) do {} while(0)
#else
#define assert(expr) \
    if (!(expr)) { \
        display(__FILE__, __LINE__); \
        displaymsg(" Assertion '" #expr "' failed.\n"); \
        sx_abort(); \
    }
#endif

static inline int sx_atoi(const char *nptr)
{
    int v = 0;

    while (*nptr) {
        if (*nptr > '9' || *nptr < '0')
            return v;
        v = *nptr - '0' + v * 10;
        nptr++;
    }
    return v;
}

#endif
