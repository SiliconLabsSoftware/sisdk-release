/***************************************************************************//**
 * @file
 * @brief UART header file
 *******************************************************************************
 * # License
 * <b>Copyright 2021 Silicon Laboratories Inc. www.silabs.com</b>
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

#ifndef UART_H
#define UART_H

/**************************************************************************//**
 * \defgroup uart UART
 * \brief UART API
 *****************************************************************************/

/**************************************************************************//**
 * \defgroup platform_hw Platform HW
 * \brief Platform HW
 *****************************************************************************/

/**************************************************************************//**
 * @addtogroup platform_hw
 * @{
 *****************************************************************************/

/**************************************************************************//**
 * @addtogroup uart
 * @{
 *****************************************************************************/

/**************************************************************************//**
 * Callback type invoked when receive data is available on the UART.
 * @param[in]  handle Descriptor handle (same as passed to uartOpen).
 * @param[in]  user_ctx User context pointer passed to uartSetRxCallback().
 *****************************************************************************/
typedef void (*uart_rx_callback_t)(void *handle, void *user_ctx);

/**************************************************************************//**
 * Allocate internal handle structure for use with uartOpen and all other
 * UART APIs. The caller must not assume size or layout of the internal state.
 * @return  Handle pointer on success; NULL on allocation failure.
 *****************************************************************************/
void *uartHandleAlloc(void);

/**************************************************************************//**
 * Free the handle previously allocated by uartHandleAlloc().
 * @note  Call uartClose(handle) before uartHandleFree(handle); the port must
 *        be closed before freeing the handle.
 * @param[in]  handle Handle returned by uartHandleAlloc(), or NULL (no-op).
 *****************************************************************************/
void uartHandleFree(void *handle);

/**************************************************************************//**
 * Register a callback to be invoked when receive data is available.
 * @note  Optional; legacy implementations doesn't rely on asynchronous
 *        RX notification.
 *        When used, the callback is invoked from an internal thread when
 *        data is ready to be read (e.g. after uartRxPeek() would return > 0).
 * @param[in]  handle Descriptor handle from uartOpen().
 * @param[in]  cb Callback function, or NULL to clear.
 * @param[in]  user_ctx User context passed to the callback when invoked.
 * @return  0 on success, -1 on failure (e.g. invalid handle).
 *****************************************************************************/
int32_t uartSetRxCallback(void *handle, uart_rx_callback_t cb, void *user_ctx);

/**************************************************************************//**
 * Open the serial port.
 * @param[out]  handle Descriptor handle
 * @param[in]  port Serial port to use.
 * @param[in]  baudRate Baud rate to use.
 * @param[in]  rtsCts Enable/disable hardware flow control.
 * @param[in]  timeout Constant used to calculate the total time-out period for
 *                     read operations, in milliseconds.
 * @return  -1 on failure; on Win 0 on success,
 *          on Posix serial handler on success
 *****************************************************************************/
int32_t uartOpen(void *handle, int8_t *port, uint32_t baudRate,
                 uint32_t rtsCts, int32_t timeout);

/**************************************************************************//**
 * After uartOpen(), drain any pending RX into the host ring buffer, then call
 * this to enable RTS/CTS handshake (Windows CDC bring-up) and start the
 * internal RX notification thread. No-op on POSIX.
 * @return  0 on success, -1 on failure.
 *****************************************************************************/
int32_t uartFinishOpen(void *handle, uint32_t rtsCts);

/**************************************************************************//**
 * Flushes accumulated data.
 *
 * @param[in]  handle Descriptor handle
 *****************************************************************************/
void uartFlush(void *handle);

/**************************************************************************//**
 * Close the serial port.
 * @param[in]  handle Descriptor handle
 * @return  0 on success, -1 on failure. Don't forget to call @ref
 *          uartHandleFree after successful close.
 *****************************************************************************/
int32_t uartClose(void *handle);

/**************************************************************************//**
 * Blocking read data from serial port. The function will block until the
 *          desired amount has been read or an error occurs.
 * @note  In order to use this function the serial port has to be configured
 *        blocking. This can be done by calling uartOpen() with 'timeout = 0'.
 * @param[in]  handle Descriptor handle
 * @param[in]  dataLength The amount of bytes to read.
 * @param[out]  data Buffer used for storing the data.
 * @return  The amount of bytes read or -1 on failure.
 *****************************************************************************/
int32_t uartRx(void *handle, uint32_t dataLength, uint8_t *data);

/**************************************************************************//**
 * Non-blocking read from serial port.
 * @note  A truly non-blocking operation is possible only if uartOpen()
 *        is called with timeout parameter set to 0.
 * @param[in]  handle Descriptor handle
 * @param[in]  dataLength The amount of bytes to read.
 * @param[out]  data Buffer used for storing the data.
 * @return  The amount of bytes read, 0 if configured serial blocking time
 *          interval elapses or -1 on failure.
 *****************************************************************************/
int32_t uartRxNonBlocking(void *handle, uint32_t dataLength, uint8_t *data);

/**************************************************************************//**
 * Return the number of bytes in the input buffer.
 * @param[in]  handle Descriptor handle
 * @return  The number of bytes in the input buffer or -1 on failure.
 *****************************************************************************/
int32_t uartRxPeek(void *handle);

/**************************************************************************//**
 * Write data to serial port. The function will block until
 *          the desired amount has been written or an error occurs.
 * @param[in]  handle Descriptor handle
 * @param[in]  dataLength The amount of bytes to write.
 * @param[in]  data Buffer used for storing the data.
 * @return  The amount of bytes written or -1 on failure.
 *****************************************************************************/
int32_t uartTx(void *handle, uint32_t dataLength, uint8_t *data);

/** @} (end addtogroup uart) */
/** @} (end addtogroup platform_hw) */

#endif /* UART_H */
