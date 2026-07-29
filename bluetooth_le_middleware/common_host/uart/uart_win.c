/***************************************************************************//**
 * @file
 * @brief UART implementation for Windows platform
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
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

#include <windows.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "uart.h"

#if _WIN32 != 1 && __CYGWIN__ != 1
#error "**** Unsupported OS! This UART driver works on Windows and Cygwin only! ****"
#endif // _WIN32 != 1 && __CYGWIN__ != 1

#ifndef CBR_230400
  #define CBR_230400 230400
#endif // CBR_230400

#ifndef CBR_460800
  #define CBR_460800 460800
#endif // CBR_460800

#ifndef CBR_921600
  #define CBR_921600 921600
#endif // CBR_921600

// Brief wait after asserting RTS so a blocked target can finish boot-event TX.
#define UART_BRINGUP_SETTLE_MS  5

// -----------------------------------------------------------------------------
// Local Variables
// Internal handle structure
typedef struct uart_handle_s uart_handle_t;

struct uart_handle_s {
  HANDLE hComm;
  HANDLE hRxEvent;
  HANDLE hStopEvent;
  HANDLE hThread;
  uart_rx_callback_t cb;
  void *cb_user;
  int32_t timeout_ms;
  uint32_t baud_rate;
  uint32_t rts_cts;
};

typedef enum {
  UART_LINE_RUNTIME,
  UART_LINE_BRINGUP,
} uart_line_mode_t;

static int uart_configure_port(HANDLE hComm,
                               uint32_t baudRate,
                               uint32_t rtsCts,
                               int32_t timeout_ms,
                               uart_line_mode_t line_mode);

void *uartHandleAlloc(void)
{
  return malloc(sizeof(uart_handle_t));
}

// -----------------------------------------------------------------------------
// Public Function Definitions
void uartHandleFree(void *handle)
{
  free(handle);
}

// Internal worker thread: waits for RX events
static DWORD WINAPI uart_worker_thread(LPVOID param)
{
  uart_handle_t *uh = (uart_handle_t*)param;

  HANDLE waitHandles[2];
  waitHandles[0] = uh->hStopEvent;
  waitHandles[1] = uh->hRxEvent;

  DWORD mask = 0;
  OVERLAPPED ov;
  memset(&ov, 0, sizeof(ov));
  ov.hEvent = uh->hRxEvent;

  // Enable RXCHAR events
  if (!SetCommMask(uh->hComm, EV_RXCHAR)) {
    return 1;
  }

  while (1) {
    mask = 0;
    ResetEvent(uh->hRxEvent);

    BOOL overlapped_pending = FALSE;
    if (!WaitCommEvent(uh->hComm, &mask, &ov)) {
      DWORD err = GetLastError();
      if (err != ERROR_IO_PENDING) {
        break;
      }
      overlapped_pending = TRUE;
    }

    if (overlapped_pending) {
      DWORD w = WaitForMultipleObjects(2, waitHandles, FALSE, INFINITE);
      if (w == WAIT_OBJECT_0) {
        // Stop: cancel this WaitCommEvent, then reap so the next WaitCommEvent is legal.
        (void)CancelIoEx(uh->hComm, &ov);
        DWORD unused = 0;
        (void)GetOverlappedResult(uh->hComm, &ov, &unused, TRUE);
        break;
      } else if (w != WAIT_OBJECT_0 + 1) {
        break;
      }
      DWORD unused = 0;
      if (!GetOverlappedResult(uh->hComm, &ov, &unused, FALSE)) {
        break;
      }
    }
    // Synchronous WaitCommEvent, or overlapped completed; mask is valid.
    if (uh->cb) {
      uh->cb(uh, uh->cb_user);
    }
  }

  return 0;
}

// Map baud rate to Windows constant
static DWORD uart_baud_to_cbr(uint32_t baud)
{
  switch (baud) {
    case 300: return CBR_300;
    case 1200: return CBR_1200;
    case 2400: return CBR_2400;
    case 4800: return CBR_4800;
    case 9600: return CBR_9600;
    case 19200: return CBR_19200;
    case 38400: return CBR_38400;
    case 57600: return CBR_57600;
    case 115200: return CBR_115200;
    case 230400: return CBR_230400;
    case 460800: return CBR_460800;
    case 921600: return CBR_921600;
    default: return 0;
  }
}

// Assert host ready-to-receive on CDC VCOM (RTS/DTR on, no handshake).
static int uart_cdc_bringup(HANDLE hComm)
{
  COMSTAT st;
  DWORD err = 0;

  if (!ClearCommError(hComm, &err, &st)) {
    return -1;
  }
  (void)err;

  Sleep(UART_BRINGUP_SETTLE_MS);

  if (!ClearCommError(hComm, &err, &st)) {
    return -1;
  }
  (void)err;

  return 0;
}

// Configure DCB and timeouts
static int uart_configure_port(HANDLE hComm,
                               uint32_t baudRate,
                               uint32_t rtsCts,
                               int32_t timeout_ms,
                               uart_line_mode_t line_mode)
{
  DCB dcb;
  memset(&dcb, 0, sizeof(dcb));
  dcb.DCBlength = sizeof(dcb);

  if (!GetCommState(hComm, &dcb)) {
    return -1;
  }

  DWORD cbr = uart_baud_to_cbr(baudRate);
  if (cbr == 0) {
    return -1;
  }

  dcb.BaudRate = cbr;
  dcb.ByteSize = 8;
  dcb.Parity   = NOPARITY;
  dcb.StopBits = ONESTOPBIT;

  if (line_mode == UART_LINE_BRINGUP) {
    dcb.fOutxCtsFlow = FALSE;
    dcb.fRtsControl  = RTS_CONTROL_ENABLE;
    dcb.fDtrControl  = DTR_CONTROL_ENABLE;
  } else if (rtsCts) {
    dcb.fOutxCtsFlow = TRUE;
    dcb.fRtsControl  = RTS_CONTROL_HANDSHAKE;
    dcb.fDtrControl  = DTR_CONTROL_ENABLE;
  } else {
    dcb.fOutxCtsFlow = FALSE;
    dcb.fRtsControl  = RTS_CONTROL_ENABLE;
    dcb.fDtrControl  = DTR_CONTROL_ENABLE;
  }

  dcb.fOutX = FALSE;
  dcb.fInX  = FALSE;

  if (!SetCommState(hComm, &dcb)) {
    return -1;
  }

  COMMTIMEOUTS to;
  memset(&to, 0, sizeof(to));

  if (timeout_ms < 0) {
    // Block until data
    to.ReadIntervalTimeout     = 0;
    to.ReadTotalTimeoutMultiplier  = 0;
    to.ReadTotalTimeoutConstant  = 0;
  } else if (timeout_ms == 0) {
    // Non-blocking
    to.ReadIntervalTimeout     = MAXDWORD;
    to.ReadTotalTimeoutMultiplier  = 0;
    to.ReadTotalTimeoutConstant  = 0;
  } else {
    // Timeout in ms
    to.ReadIntervalTimeout     = MAXDWORD;
    to.ReadTotalTimeoutMultiplier  = 0;
    to.ReadTotalTimeoutConstant  = (DWORD)timeout_ms;
  }

  to.WriteTotalTimeoutMultiplier = 0;
  to.WriteTotalTimeoutConstant   = (timeout_ms > 0) ? (DWORD)timeout_ms : 0;

  if (!SetCommTimeouts(hComm, &to)) {
    return -1;
  }

  // Request reasonable buffer sizes
  if (!SetupComm(hComm, 4096, 4096)) {
    DWORD ret = GetLastError();
    fprintf(stderr, "SetupComm failed %ld.\n", (unsigned long)ret);
  }

  return 0;
}

// UART open (using Overlapped I/O)
int32_t uartOpen(void *handle, int8_t *port, uint32_t baudRate,
                 uint32_t rtsCts, int32_t timeout)
{
  uart_handle_t *uh = (uart_handle_t *)handle;
  memset(uh, 0, sizeof(*uh));

  char deviceStr[64];
  memset(deviceStr, 0, sizeof(deviceStr));
  // Support COM10+ style names
  _snprintf(deviceStr, sizeof(deviceStr) - 1, "\\\\.\\%s", (char*)port);

  HANDLE hComm = CreateFileA(deviceStr,
                             GENERIC_READ | GENERIC_WRITE,
                             0,
                             NULL,
                             OPEN_EXISTING,
                             FILE_FLAG_OVERLAPPED,
                             NULL);
  if (hComm == INVALID_HANDLE_VALUE) {
    return -1;
  }

  uh->hComm       = hComm;
  uh->baud_rate   = baudRate;
  uh->rts_cts     = rtsCts;
  uh->timeout_ms  = timeout;
  uh->cb          = NULL;
  uh->cb_user     = NULL;

  if (uart_configure_port(hComm, baudRate, rtsCts, timeout,
                          rtsCts ? UART_LINE_BRINGUP : UART_LINE_RUNTIME) < 0) {
    CloseHandle(hComm);
    return -1;
  }

  if (rtsCts && uart_cdc_bringup(hComm) < 0) {
    CloseHandle(hComm);
    return -1;
  }

  uh->hRxEvent   = CreateEventA(NULL, TRUE, FALSE, NULL);
  uh->hStopEvent = CreateEventA(NULL, TRUE, FALSE, NULL);

  if (!uh->hRxEvent || !uh->hStopEvent) {
    if (uh->hRxEvent) {
      CloseHandle(uh->hRxEvent);
    }
    if (uh->hStopEvent) {
      CloseHandle(uh->hStopEvent);
    }
    CloseHandle(hComm);
    return -1;
  }

  return 0;
}

int32_t uartFinishOpen(void *handle, uint32_t rtsCts)
{
  uart_handle_t *uh = (uart_handle_t *)handle;
  if (!uh || !uh->hComm || uh->hComm == INVALID_HANDLE_VALUE) {
    return -1;
  }

  if (rtsCts) {
    if (uart_configure_port(uh->hComm, uh->baud_rate, uh->rts_cts,
                            uh->timeout_ms, UART_LINE_RUNTIME) < 0) {
      return -1;
    }
  }

  if (uh->hThread) {
    return 0;
  }

  DWORD tid = 0;
  uh->hThread = CreateThread(NULL,
                             0,
                             uart_worker_thread,
                             uh,
                             0,
                             &tid);
  if (!uh->hThread) {
    return -1;
  }

  return 0;
}

int32_t uartSetRxCallback(void *handle, uart_rx_callback_t cb, void *user_ctx)
{
  uart_handle_t *uh = (uart_handle_t *)handle;
  if (!uh) {
    return -1;
  }

  uh->cb    = cb;
  uh->cb_user = user_ctx;

  return 0;
}

void uartFlush(void *handle)
{
  uart_handle_t *uh = (uart_handle_t*)handle;
  if (!uh || !uh->hComm || uh->hComm == INVALID_HANDLE_VALUE) {
    return;
  }
  // Do not purge RX: pending bytes are drained into the host ring after open.
  PurgeComm(uh->hComm, PURGE_TXCLEAR);
}

int32_t uartRx(void *handle, uint32_t dataLength, uint8_t *data)
{
  uart_handle_t *uh = (uart_handle_t*)handle;
  if (!uh || !uh->hComm || uh->hComm == INVALID_HANDLE_VALUE) {
    return -1;
  }

  DWORD totalRead = 0;

  while (totalRead < dataLength) {
    OVERLAPPED ov;
    memset(&ov, 0, sizeof(ov));
    ov.hEvent = CreateEventA(NULL, TRUE, FALSE, NULL);
    if (!ov.hEvent) {
      return -1;
    }

    DWORD bytesRead = 0;
    BOOL ok = ReadFile(uh->hComm,
                       data + totalRead,
                       dataLength - totalRead,
                       &bytesRead,
                       &ov);
    if (!ok) {
      DWORD err = GetLastError();
      if (err == ERROR_IO_PENDING) {
        DWORD to = (uh->timeout_ms < 0) ? INFINITE : (DWORD)uh->timeout_ms;
        DWORD w = WaitForSingleObject(ov.hEvent, to);
        if (w != WAIT_OBJECT_0) {
          CloseHandle(ov.hEvent);
          return -1;
        }
        if (!GetOverlappedResult(uh->hComm, &ov, &bytesRead, FALSE)) {
          CloseHandle(ov.hEvent);
          return -1;
        }
      } else {
        CloseHandle(ov.hEvent);
        return -1;
      }
    }

    CloseHandle(ov.hEvent);

    if (bytesRead == 0) {
      if (totalRead > 0) {
        return (int32_t)totalRead;
      }
      return -1;
    }

    totalRead += bytesRead;
  }

  return (int32_t)totalRead;
}

int32_t uartRxNonBlocking(void *handle, uint32_t dataLength, uint8_t *data)
{
  uart_handle_t *uh = (uart_handle_t*)handle;
  if (!uh || !uh->hComm || uh->hComm == INVALID_HANDLE_VALUE) {
    return -1;
  }

  OVERLAPPED ov;
  memset(&ov, 0, sizeof(ov));
  ov.hEvent = CreateEventA(NULL, TRUE, FALSE, NULL);
  if (!ov.hEvent) {
    return -1;
  }

  DWORD bytesRead = 0;
  BOOL ok = ReadFile(uh->hComm,
                     data,
                     dataLength,
                     &bytesRead,
                     &ov);
  if (!ok) {
    DWORD err = GetLastError();
    if (err == ERROR_IO_PENDING) {
      // Nonblocking: do not wait, just check if something is ready
      BOOL res = GetOverlappedResult(uh->hComm, &ov, &bytesRead, FALSE);
      CloseHandle(ov.hEvent);
      if (!res) {
        DWORD err2 = GetLastError();
        if (err2 == ERROR_IO_INCOMPLETE) {
          return 0;
        }
        return -1;
      }
    } else {
      CloseHandle(ov.hEvent);
      return -1;
    }
  } else {
    CloseHandle(ov.hEvent);
  }

  return (int32_t)bytesRead;
}

int32_t uartRxPeek(void *handle)
{
  uart_handle_t *uh = (uart_handle_t*)handle;
  COMSTAT st;
  DWORD err = 0;

  if (!uh || !uh->hComm || uh->hComm == INVALID_HANDLE_VALUE) {
    return -1;
  }

  memset(&st, 0, sizeof(st));
  if (!ClearCommError(uh->hComm, &err, &st)) {
    return -1;
  }
  // Ignore framing/parity flags in err; cbInQue is still valid.
  (void)err;

  return (int32_t)st.cbInQue;
}

int32_t uartTx(void *handle, uint32_t dataLength, uint8_t *data)
{
  uart_handle_t *uh = (uart_handle_t*)handle;
  if (!uh || !uh->hComm || uh->hComm == INVALID_HANDLE_VALUE) {
    return -1;
  }

  DWORD totalWritten = 0;

  while (totalWritten < dataLength) {
    OVERLAPPED ov;
    memset(&ov, 0, sizeof(ov));
    ov.hEvent = CreateEventA(NULL, TRUE, FALSE, NULL);
    if (!ov.hEvent) {
      return -1;
    }

    DWORD bytesWritten = 0;
    BOOL ok = WriteFile(uh->hComm,
                        data + totalWritten,
                        dataLength - totalWritten,
                        &bytesWritten,
                        &ov);
    if (!ok) {
      DWORD err = GetLastError();
      if (err == ERROR_IO_PENDING) {
        DWORD to = (uh->timeout_ms < 0) ? INFINITE : (DWORD)uh->timeout_ms;
        DWORD w = WaitForSingleObject(ov.hEvent, to);
        if (w != WAIT_OBJECT_0) {
          CloseHandle(ov.hEvent);
          return -1;
        }
        if (!GetOverlappedResult(uh->hComm, &ov, &bytesWritten, FALSE)) {
          CloseHandle(ov.hEvent);
          return -1;
        }
      } else {
        CloseHandle(ov.hEvent);
        return -1;
      }
    }

    CloseHandle(ov.hEvent);

    if (bytesWritten == 0) {
      return -1;
    }

    totalWritten += bytesWritten;
  }

  return (int32_t)totalWritten;
}

int32_t uartClose(void *handle)
{
  uart_handle_t *uh = (uart_handle_t*)handle;
  if (!uh) {
    return -1;
  }

  if (uh->hStopEvent) {
    SetEvent(uh->hStopEvent);
  }

  if (uh->hThread) {
    WaitForSingleObject(uh->hThread, INFINITE);
    CloseHandle(uh->hThread);
    uh->hThread = NULL;
  }

  if (uh->hRxEvent) {
    CloseHandle(uh->hRxEvent);
    uh->hRxEvent = NULL;
  }

  if (uh->hStopEvent) {
    CloseHandle(uh->hStopEvent);
    uh->hStopEvent = NULL;
  }

  if (uh->hComm && uh->hComm != INVALID_HANDLE_VALUE) {
    CloseHandle(uh->hComm);
    uh->hComm = INVALID_HANDLE_VALUE;
  }

  return 0;
}
