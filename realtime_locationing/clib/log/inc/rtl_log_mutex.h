#ifndef RTL_LOG_MUTEX_H
#define RTL_LOG_MUTEX_H

#ifdef RTL_EFR_BUILD

#ifdef __cplusplus
extern "C" {
#endif

/** Opaque mutex handle; created by platform stub or CMSIS-OS2 log mutex sources. */
typedef void *logMutex_t;

int logMutexInit(logMutex_t *mtxInOut);
void logMutexLock(logMutex_t *mtxInOut);
void logMutexUnlock(logMutex_t *mtxInOut);
void logMutexDeinit(logMutex_t *mtxInOut);

#ifdef __cplusplus
}
#endif

#elif defined(_POSIX_THREADS) || !defined(_WIN32)
  #include <pthread.h>

typedef pthread_mutex_t logMutex_t;

static inline int logMutexInit(logMutex_t *mtxInOut)
{
  return pthread_mutex_init(mtxInOut, NULL);
}
static inline void logMutexLock(logMutex_t *mtxInOut)
{
  pthread_mutex_lock(mtxInOut);
}
static inline void logMutexUnlock(logMutex_t *mtxInOut)
{
  pthread_mutex_unlock(mtxInOut);
}
static inline void logMutexDeinit(logMutex_t *mtxInOut)
{
  pthread_mutex_destroy(mtxInOut);
}

#else
typedef int logMutex_t;
static inline int  logMutexInit(logMutex_t *mtxInOut)
{
  (void)mtxInOut; return 0;
}
static inline void logMutexLock(logMutex_t *mtxInOut)
{
  (void)mtxInOut;
}
static inline void logMutexUnlock(logMutex_t *mtxInOut)
{
  (void)mtxInOut;
}
static inline void logMutexDeinit(logMutex_t *mtxInOut)
{
  (void)mtxInOut;
}
#endif

#endif // RTL_LOG_MUTEX_H
