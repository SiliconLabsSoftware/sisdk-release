/*
 *  Copyright (c) 2025, The OpenThread Authors.
 *  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions are met:
 *  1. Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *  2. Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *  3. Neither the name of the copyright holder nor the
 *     names of its contributors may be used to endorse or promote products
 *     derived from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 *  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 *  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 *  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 *  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 *  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 *  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 *  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 */

/**
 * @file
 *   This file implements the OpenThread platform abstraction for SPI communication.
 *
 */

#ifdef SL_COMPONENT_CATALOG_PRESENT
#include "sl_component_catalog.h"
#endif

#include "sl_core.h"

// GPIO: unified HAL for Series 2 and Series 3
#include "sl_device_gpio.h"
#include "sl_gpio.h"
#include "sl_hal_gpio.h"

#include "sl_device_dma.h"
#include "sl_device_peripheral.h"
#include "sl_dma_channel.h"
#include "sl_dma_channel_device.h"

#include "spidrv.h"

// Include em_device.h early to get series defines
#include "em_device.h"
// Determine USART/EUSART presence
#if defined(_SILICON_LABS_32B_SERIES_2)
#define USART_SPI_PERIPHERAL
#elif defined(_SILICON_LABS_32B_SERIES_3)
#define EUSART_SPI_PERIPHERAL
#endif

#include "sl_clock_manager.h"
#if defined(SL_CATALOG_POWER_MANAGER_PRESENT)
#include "sl_power_manager.h"
#endif

// Conditional config header includes
#if defined(USART_SPI_PERIPHERAL)
#include "sl_ncp_spidrv_usart_config.h"
#elif defined(EUSART_SPI_PERIPHERAL)
#include "sl_ncp_spidrv_eusart_config.h"
#endif

#include "platform-efr32.h"
#include <openthread-system.h>
#include <openthread/error.h>
#include <openthread/platform/spi-slave.h>
#include "common/code_utils.hpp"
#include "common/debug.hpp"

#define SL_OT_SPIDRV_SPI_CONCAT_PASTER(first, second, third) first##second##third

// Peripheral DMA request signals (sl_dma_signal_t / SL_DMA_SIGNAL_*)
#if defined(USART_SPI_PERIPHERAL)
#define SL_OT_SPIDRV_SPI_DMA_RX_SIGNAL(periph_nbr) \
    SL_OT_SPIDRV_SPI_CONCAT_PASTER(SL_DMA_SIGNAL_USART, periph_nbr, _RXDATAV)
#define SL_OT_SPIDRV_SPI_DMA_TX_SIGNAL(periph_nbr) \
    SL_OT_SPIDRV_SPI_CONCAT_PASTER(SL_DMA_SIGNAL_USART, periph_nbr, _TXBL)
#elif defined(EUSART_SPI_PERIPHERAL)
#define SL_OT_SPIDRV_SPI_DMA_RX_SIGNAL(periph_nbr) \
    SL_OT_SPIDRV_SPI_CONCAT_PASTER(SL_DMA_SIGNAL_EUSART, periph_nbr, _RXFL)
#define SL_OT_SPIDRV_SPI_DMA_TX_SIGNAL(periph_nbr) \
    SL_OT_SPIDRV_SPI_CONCAT_PASTER(SL_DMA_SIGNAL_EUSART, periph_nbr, _TXFL)
#endif

// ============================================================================
// Configuration Macros (to reduce repetition)
// ============================================================================

#if defined(USART_SPI_PERIPHERAL)
#define SPI_CS_PORT SL_NCP_SPIDRV_USART_CS_PORT
#define SPI_CS_PIN SL_NCP_SPIDRV_USART_CS_PIN
#define SPI_CS_RISING_EDGE_INT SL_NCP_SPIDRV_USART_CS_RISING_EDGE_INT_NO
#define SPI_CS_FALLING_EDGE_INT SL_NCP_SPIDRV_USART_CS_FALLING_EDGE_INT_NO
#define SPI_HOST_INT_PORT SL_NCP_SPIDRV_USART_HOST_INT_PORT
#define SPI_HOST_INT_PIN SL_NCP_SPIDRV_USART_HOST_INT_PIN
#define SPI_PERIPHERAL_NO SL_NCP_SPIDRV_USART_PERIPHERAL_NO
#elif defined(EUSART_SPI_PERIPHERAL)
#define SPI_CS_PORT SL_NCP_SPIDRV_EUSART_CS_PORT
#define SPI_CS_PIN SL_NCP_SPIDRV_EUSART_CS_PIN
#define SPI_CS_RISING_EDGE_INT SL_NCP_SPIDRV_EUSART_CS_RISING_EDGE_INT_NO
#define SPI_CS_FALLING_EDGE_INT SL_NCP_SPIDRV_EUSART_CS_FALLING_EDGE_INT_NO
#define SPI_HOST_INT_PORT SL_NCP_SPIDRV_EUSART_HOST_INT_PORT
#define SPI_HOST_INT_PIN SL_NCP_SPIDRV_EUSART_HOST_INT_PIN
#define SPI_PERIPHERAL_NO SL_NCP_SPIDRV_EUSART_PERIPHERAL_NO
#endif // USART_SPI_PERIPHERAL

//  Member variables
static volatile bool should_process_transaction = false;
static bool          s_ot_spi_slave_ready       = false;

static uint8_t default_tx_value;

static sl_dma_channel_xfer_descriptor_t s_tx_dma_descriptors[2];
static sl_dma_channel_xfer_descriptor_t s_rx_dma_descriptor;

static sl_dma_channel_transfer_t s_tx_dma_transfers[2];
static sl_dma_channel_transfer_t s_rx_dma_transfer;

// Sizes matching legacy two-descriptor TX layout (seg0 + seg1) for transaction byte counting
static uint16_t s_tx_seg0_bytes;
static uint16_t s_tx_seg1_bytes;

// Last prepared buffers reported to the complete callback
static uint8_t *s_tx_output_buf;
static uint16_t s_tx_output_len;
static uint8_t *s_rx_buf;
static uint16_t s_rx_len;

// Transaction events callback
static volatile otPlatSpiSlaveTransactionCompleteCallback complete_callback;
static volatile otPlatSpiSlaveTransactionProcessCallback  process_callback;
static volatile void                                     *context;

// SPI Peripheral
static volatile SPIDRV_HandleData_t sl_spidrv_handle_data;

static sl_dma_channel_handle_t *spidrv_get_tx_dma_handle(void)
{
    return (sl_dma_channel_handle_t *)&sl_spidrv_handle_data.txDMACh;
}

static sl_dma_channel_handle_t *spidrv_get_rx_dma_handle(void)
{
    return (sl_dma_channel_handle_t *)&sl_spidrv_handle_data.rxDMACh;
}

// ============================================================================
// DMA helpers (DMA Channel driver)
// ============================================================================

static void dma_setup_tx_transfer(sl_dma_channel_transfer_t        *aDmaTransferConfig,
                                  void                             *src,
                                  void                             *dst_reg,
                                  size_t                            size,
                                  bool                              inc_src,
                                  sl_dma_channel_xfer_descriptor_t *desc)
{
    *aDmaTransferConfig = (sl_dma_channel_transfer_t){
        .source                = src,
        .destination           = dst_reg,
        .size                  = size,
        .unit_size             = SL_DMA_CTRL_SIZE_BYTE,
        .block_size            = SL_DMA_CTRL_BLOCK_SIZE_UNIT_1,
        .increment_source      = inc_src,
        .increment_destination = false,
        .block_handshake_mode  = true,
        .callback_on_complete  = false,
        .cacheable             = false,
        .descriptor            = desc,
        .next                  = NULL,
    };
}

static void dma_setup_rx_transfer(sl_dma_channel_transfer_t        *aDmaTransferConfig,
                                  void                             *src_reg,
                                  void                             *dst,
                                  size_t                            size,
                                  sl_dma_channel_xfer_descriptor_t *desc)
{
    *aDmaTransferConfig = (sl_dma_channel_transfer_t){
        .source                = src_reg,
        .destination           = dst,
        .size                  = size,
        .unit_size             = SL_DMA_CTRL_SIZE_BYTE,
        .block_size            = SL_DMA_CTRL_BLOCK_SIZE_UNIT_1,
        .increment_source      = false,
        .increment_destination = true,
        .block_handshake_mode  = true,
        .callback_on_complete  = false,
        .cacheable             = false,
        .descriptor            = desc,
        .next                  = NULL,
    };
}

// Forward declaration of peripheral_get_tx_status_shifted for dma_compute_tx_transaction_size
static uint32_t peripheral_get_tx_status_shifted(void);

// Snapshots TX progress from LDMA channel registers (must run before @ref sl_dma_channel_abort).
static uint32_t dma_compute_tx_transaction_size()
{
    sl_dma_channel_handle_t *tx_dma        = spidrv_get_tx_dma_handle();
    uint8_t                  tx_channel    = tx_dma->channel_number;
    uint32_t                 fifo_tx_count = peripheral_get_tx_status_shifted();

    LDMA_TypeDef *tx_ldma   = sl_device_peripheral_ldma_get_base_addr((sl_peripheral_t)tx_dma->dma_peripheral);
    uint32_t      ctrl_reg  = tx_ldma->CH[tx_channel].CTRL;
    uint32_t      link_reg  = tx_ldma->CH[tx_channel].LINK;
    uint32_t      remaining = ((ctrl_reg & _LDMA_CH_CTRL_XFERCNT_MASK) >> _LDMA_CH_CTRL_XFERCNT_SHIFT) + 1U;
    remaining += fifo_tx_count;

    uint32_t link_rel  = (link_reg & _LDMA_CH_LINK_LINK_MASK) >> _LDMA_CH_LINK_LINK_SHIFT;
    uint32_t xfer_cnt0 = (uint32_t)s_tx_seg0_bytes - 1U;

    if (link_rel == 0U)
    {
        return (uint32_t)s_tx_seg0_bytes + (uint32_t)s_tx_seg1_bytes - remaining;
    }
    return (xfer_cnt0 - remaining) + 1U;
}

// ============================================================================
// Generic GPIO Helper Functions
// ============================================================================

static void gpio_set_host_request(void)
{
#if defined(SPI_HOST_INT_PORT) && defined(SPI_HOST_INT_PIN)
    const sl_gpio_t host_int_gpio = {.port = SPI_HOST_INT_PORT, .pin = SPI_HOST_INT_PIN};
    sl_hal_gpio_clear_pin(&host_int_gpio);
#endif
}

static void gpio_deassert_host_request(void)
{
#if defined(SPI_HOST_INT_PORT) && defined(SPI_HOST_INT_PIN)
    const sl_gpio_t host_int_gpio = {.port = SPI_HOST_INT_PORT, .pin = SPI_HOST_INT_PIN};
    sl_hal_gpio_set_pin(&host_int_gpio);
#endif
}

static void gpio_set_pin_mode(uint32_t port, uint32_t pin, uint32_t mode, uint32_t out)
{
    const sl_gpio_t gpio = {.port = static_cast<uint8_t>(port), .pin = static_cast<uint8_t>(pin)};
    sl_hal_gpio_set_pin_mode(&gpio, mode, out);
}

static bool gpio_get_pin_input(uint32_t port, uint32_t pin)
{
    const sl_gpio_t gpio = {.port = static_cast<uint8_t>(port), .pin = static_cast<uint8_t>(pin)};
    return sl_hal_gpio_get_pin_input(&gpio) != 0U;
}

// Unified CS pin check helper
static bool gpio_is_cs_high(void)
{
    return gpio_get_pin_input(SPI_CS_PORT, SPI_CS_PIN);
}

// Forward declaration for interrupt callback
static void spi_transaction_end_interrupt(uint8_t intNo, void *ctx);

static void gpio_configure_cs_interrupt(uint32_t port, uint32_t pin, uint32_t int_no, bool rising_edge)
{
    const sl_gpio_t cs_gpio = {.port = static_cast<uint8_t>(port), .pin = static_cast<uint8_t>(pin)};
    int32_t         intNo   = (int32_t)int_no;
    sl_status_t     status  = sl_gpio_configure_external_interrupt(&cs_gpio,
                                                              &intNo,
                                                              rising_edge ? SL_GPIO_INTERRUPT_RISING_EDGE
                                                                               : SL_GPIO_INTERRUPT_FALLING_EDGE,
                                                              spi_transaction_end_interrupt,
                                                              NULL);
    OT_ASSERT(status == SL_STATUS_OK);
}

static void gpio_deconfigure_cs_interrupt(uint32_t int_no)
{
    IgnoreReturnValue(sl_gpio_deconfigure_external_interrupt((int32_t)int_no));
}

// ============================================================================
// Generic Peripheral Helper Functions
// ============================================================================

static uint32_t peripheral_get_tx_status(void)
{
#if defined(USART_SPI_PERIPHERAL)
    return sl_spidrv_handle_data.peripheral.usartPort->STATUS & _USART_STATUS_TXBUFCNT_MASK;
#elif defined(EUSART_SPI_PERIPHERAL)
    return sl_spidrv_handle_data.peripheral.eusartPort->STATUS & _EUSART_STATUS_TXFCNT_MASK;
#endif
}

static uint32_t peripheral_get_tx_status_shifted(void)
{
#if defined(USART_SPI_PERIPHERAL)
    return (sl_spidrv_handle_data.peripheral.usartPort->STATUS & _USART_STATUS_TXBUFCNT_MASK)
           >> _USART_STATUS_TXBUFCNT_SHIFT;
#elif defined(EUSART_SPI_PERIPHERAL)
    return (sl_spidrv_handle_data.peripheral.eusartPort->STATUS & _EUSART_STATUS_TXFCNT_MASK)
           >> _EUSART_STATUS_TXFCNT_SHIFT;
#endif
}

static uint32_t peripheral_get_rx_status(void)
{
#if defined(USART_SPI_PERIPHERAL)
    return sl_spidrv_handle_data.peripheral.usartPort->STATUS & _USART_STATUS_RXDATAV_MASK;
#elif defined(EUSART_SPI_PERIPHERAL)
    return sl_spidrv_handle_data.peripheral.eusartPort->STATUS & _EUSART_STATUS_RXFL_MASK;
#endif
}

static void peripheral_clear_fifos(void)
{
#if defined(USART_SPI_PERIPHERAL)
    sl_spidrv_handle_data.peripheral.usartPort->CMD = USART_CMD_CLEARTX | USART_CMD_CLEARRX;
#elif defined(EUSART_SPI_PERIPHERAL)
    EUSART_TypeDef *eusart = sl_spidrv_handle_data.peripheral.eusartPort;
    // EUSART_CMD_CLEARTX reportedly only affects UART, not SPI mode,
    // and there is no EUSART_CMD_CLEARRX. Only way to clear the
    // FIFOs is via the big hammer of disabling then reenabling it.
    sl_hal_eusart_disable_rx(eusart);
    sl_hal_eusart_disable_tx(eusart);
    sl_hal_eusart_disable(eusart);
    while (eusart->EN & _EUSART_EN_DISABLING_MASK);
    sl_hal_eusart_enable(eusart);
    sl_hal_eusart_enable_rx(eusart);
    sl_hal_eusart_enable_tx(eusart);
    sl_hal_eusart_wait_sync(eusart, _EUSART_SYNCBUSY_MASK);
#endif
}

static void peripheral_clear_rx_fifo(void)
{
#if defined(USART_SPI_PERIPHERAL)
    sl_spidrv_handle_data.peripheral.usartPort->CMD = USART_CMD_CLEARRX;
#elif defined(EUSART_SPI_PERIPHERAL)
    // Cannot directly clear rx fifo on S3; instead, clear rx and tx
    peripheral_clear_fifos();
#endif
}

static void peripheral_clear_tx_fifo(void)
{
#if defined(USART_SPI_PERIPHERAL)
    sl_spidrv_handle_data.peripheral.usartPort->CMD = USART_CMD_CLEARTX;
#elif defined(EUSART_SPI_PERIPHERAL)
    // Cannot directly clear tx fifo on S3; instead, clear tx and rx
    peripheral_clear_fifos();
#endif
}

static void peripheral_wait_tx_fifo_empty(void)
{
#if defined(USART_SPI_PERIPHERAL)
    while (sl_spidrv_handle_data.peripheral.usartPort->STATUS & _USART_STATUS_TXBUFCNT_MASK);
#endif
    // Note: on series 3, it is assumed that we run peripheral_clear_fifos() before this, which already
    // involves waiting for the fifos to empty. Thus, no action is required here for S3.
}

static void peripheral_wait_rx_fifo_empty(void)
{
#if defined(USART_SPI_PERIPHERAL)
    while (sl_spidrv_handle_data.peripheral.usartPort->STATUS & _USART_STATUS_RXDATAV_MASK);
#endif
    // Note: on series 3, it is assumed that we run peripheral_clear_fifos() before this, which already
    // involves waiting for the fifos to empty. Thus, no action is required here for S3.
}

// RX: clear stale RX data; on Series 2, block until STATUS shows RX drained.
static void peripheral_clear_rx_fifo_and_drain(void)
{
    peripheral_clear_rx_fifo();
    peripheral_wait_rx_fifo_empty();
}

// TX: clear non-empty TX FIFO if needed; always run drain (Series 2: STATUS poll;
// Series 3: wait is a no-op after clear_fifos).
static void peripheral_clear_tx_fifo_if_needed_and_drain(void)
{
    if (peripheral_get_tx_status())
    {
        peripheral_clear_tx_fifo();
    }
    peripheral_wait_tx_fifo_empty();
}

// RXDATA is const volatile in device headers (read-only register) but DMA descriptors need a
// non-const volatile peripheral address; const is discarded only for that use.
static volatile void *peripheral_get_rxdata_addr(void)
{
#if defined(USART_SPI_PERIPHERAL)
    return (volatile void *)&(sl_spidrv_handle_data.peripheral.usartPort->RXDATA);
#elif defined(EUSART_SPI_PERIPHERAL)
    return (volatile void *)&(sl_spidrv_handle_data.peripheral.eusartPort->RXDATA);
#endif
}

static volatile void *peripheral_get_txdata_addr(void)
{
#if defined(USART_SPI_PERIPHERAL)
    return &(sl_spidrv_handle_data.peripheral.usartPort->TXDATA);
#elif defined(EUSART_SPI_PERIPHERAL)
    return &(sl_spidrv_handle_data.peripheral.eusartPort->TXDATA);
#endif
}

// ============================================================================
// Main Implementation Functions
// ============================================================================

static void spi_transaction_end_interrupt(uint8_t intNo, void *ctx)
{
    OT_UNUSED_VARIABLE(ctx);

    // Handle falling edge (transaction start) - no action needed
    if (intNo == SPI_CS_FALLING_EDGE_INT)
    {
        return;
    }

    // Handle rising edge (transaction end)
    if (intNo == SPI_CS_RISING_EDGE_INT)
    {
        // Must be done before calling the "complete_callback" since
        // this callback will use otPlatSpiSlavePrepareTransaction who
        // would not setup the buffers if a transaction is ongoing.
        gpio_deassert_host_request();
    }

    uint32_t tx_transaction_size = dma_compute_tx_transaction_size();

    uint8_t *old_tx_buffer      = (s_tx_output_len != 0U) ? s_tx_output_buf : (uint8_t *)&default_tx_value;
    uint16_t old_tx_buffer_size = (s_tx_output_len != 0U) ? s_tx_output_len : 1U;

    uint8_t *old_rx_buffer      = s_rx_buf;
    uint16_t old_rx_buffer_size = (s_rx_len != 0U) ? s_rx_len : 1U;

    IgnoreReturnValue(sl_dma_channel_abort(spidrv_get_tx_dma_handle()));
    IgnoreReturnValue(sl_dma_channel_abort(spidrv_get_rx_dma_handle()));

    // Clear the FIFOs if there are more bytes to transmit than expected DMA tx xferCnt.
    if (peripheral_get_tx_status())
    {
        peripheral_clear_fifos();
    }

    // call's otPlatSpiSlavePrepareTransaction in the background, the DMA buffer's will be ready after this call.
    if (complete_callback((void *)context,
                          old_tx_buffer,
                          old_tx_buffer_size,
                          old_rx_buffer,
                          old_rx_buffer_size,
                          tx_transaction_size))
    {
        should_process_transaction = true;
#ifdef SL_CATALOG_KERNEL_PRESENT
        sl_ot_rtos_set_pending_event(SL_OT_RTOS_EVENT_SERIAL);
#endif
        otSysEventSignalPending();
    }
}

otError otPlatSpiSlaveEnable(otPlatSpiSlaveTransactionCompleteCallback aCompleteCallback,
                             otPlatSpiSlaveTransactionProcessCallback  aProcessCallback,
                             void                                     *aContext)
{
    CORE_DECLARE_IRQ_STATE;
    otError     error         = OT_ERROR_NONE;
    bool        spidrv_inited = false;
    bool        in_atomic     = false;
    sl_status_t st;

    if (complete_callback != NULL || process_callback != NULL || context != NULL)
    {
        return OT_ERROR_ALREADY;
    }

    sl_clock_manager_enable_bus_clock(SL_BUS_CLOCK_GPIO);

#if defined(USART_SPI_PERIPHERAL)
    SPIDRV_Init_t init_data = (SPIDRV_Init_t){
        SL_NCP_SPIDRV_USART_PERIPHERAL, // The USART used for SPI.
#if defined(_USART_ROUTELOC0_MASK)
        SL_NCP_SPIDRV_USART_TX_LOC,  // A location number for the SPI Tx pin.
        SL_NCP_SPIDRV_USART_RX_LOC,  // A location number for the SPI Rx pin.
        SL_NCP_SPIDRV_USART_CLK_LOC, // A location number for the SPI Clk pin.
        SL_NCP_SPIDRV_USART_CS_LOC,  // A location number for the SPI Cs pin.
#elif defined(_GPIO_USART_ROUTEEN_MASK)
        SL_NCP_SPIDRV_USART_TX_PORT,  // Tx port.
        SL_NCP_SPIDRV_USART_RX_PORT,  // Rx port.
        SL_NCP_SPIDRV_USART_CLK_PORT, // Clock port.
        SL_NCP_SPIDRV_USART_CS_PORT,  // Chip select port.
        SL_NCP_SPIDRV_USART_TX_PIN,   // Tx pin.
        SL_NCP_SPIDRV_USART_RX_PIN,   // Rx pin.
        SL_NCP_SPIDRV_USART_CLK_PIN,  // Clock pin.
        SL_NCP_SPIDRV_USART_CS_PIN,   // Chip select pin.
#endif
        0U,                             // An SPI bitrate.
        8,                              // An SPI framelength, valid numbers are 4..16
        0,                              // The value to transmit when using SPI receive API functions.
        spidrvSlave,                    // An SPI type, slave.
        SL_NCP_SPIDRV_USART_BIT_ORDER,  // A bit order on the SPI bus, MSB or LSB first.
        SL_NCP_SPIDRV_USART_CLOCK_MODE, // SPI mode, CLKPOL/CLKPHASE setting.
        spidrvCsControlAuto,            // A select master mode chip select (CS) control scheme.
        spidrvSlaveStartImmediate,      // A slave mode transfer start scheme.
    };
#elif defined(EUSART_SPI_PERIPHERAL)
    SPIDRV_Init_t init_data = (SPIDRV_Init_t){
        SL_NCP_SPIDRV_EUSART_PERIPHERAL, // The EUSART used for SPI.
        SL_NCP_SPIDRV_EUSART_TX_PORT,    // Tx port.
        SL_NCP_SPIDRV_EUSART_RX_PORT,    // Rx port.
        SL_NCP_SPIDRV_EUSART_SCLK_PORT,  // Clock port.
        SL_NCP_SPIDRV_EUSART_CS_PORT,    // Chip select port.
        SL_NCP_SPIDRV_EUSART_TX_PIN,     // Tx pin.
        SL_NCP_SPIDRV_EUSART_RX_PIN,     // Rx pin.
        SL_NCP_SPIDRV_EUSART_SCLK_PIN,   // Clock pin.
        SL_NCP_SPIDRV_EUSART_CS_PIN,     // Chip select pin.
        0U,                              // An SPI bitrate.
        8,                               // An SPI framelength, valid numbers are 4..16
        0,                               // The value to transmit when using SPI receive API functions.
        spidrvSlave,                     // An SPI type, slave.
        SL_NCP_SPIDRV_EUSART_BIT_ORDER,  // A bit order on the SPI bus, MSB or LSB first.
        SL_NCP_SPIDRV_EUSART_CLOCK_MODE, // SPI mode, CLKPOL/CLKPHASE setting.
        spidrvCsControlAuto,             // A select master mode chip select (CS) control scheme.
        spidrvSlaveStartImmediate,       // A slave mode transfer start scheme.
    };
#endif // USART_SPI_PERIPHERAL

    VerifyOrExit(SPIDRV_Init((SPIDRV_HandleData_t *)&sl_spidrv_handle_data, &init_data) == ECODE_EMDRV_SPIDRV_OK,
                 error = OT_ERROR_FAILED);

    spidrv_inited = true; // SPIDRV owns DMA channel init/allocation in txDMACh / rxDMACh.

    // TX default value.
    default_tx_value = 0xFFU;

    s_tx_output_buf = NULL;
    s_tx_output_len = 0U;
    s_rx_buf        = NULL;
    s_rx_len        = 0U;
    s_tx_seg0_bytes = 1U;
    s_tx_seg1_bytes = (uint16_t)SL_DMA_CHANNEL_MAX_XFER_UNIT_COUNT;

    // Configuring Host INT line. Active low
#if defined(SPI_HOST_INT_PORT) && defined(SPI_HOST_INT_PIN)
    gpio_set_pin_mode(SPI_HOST_INT_PORT, SPI_HOST_INT_PIN, SL_GPIO_MODE_PUSH_PULL, 1U);
#endif

    // Configure CS pin
    gpio_set_pin_mode(SPI_CS_PORT, SPI_CS_PIN, SL_GPIO_MODE_INPUT_PULL_FILTER, 1);

    CORE_ENTER_ATOMIC();
    in_atomic = true;

    // Initialization during transaction is not supported.
    VerifyOrExit(gpio_is_cs_high(), error = OT_ERROR_FAILED);

    // Configure CS interrupts
    gpio_configure_cs_interrupt(SPI_CS_PORT, SPI_CS_PIN, SPI_CS_RISING_EDGE_INT, true);
    gpio_configure_cs_interrupt(SPI_CS_PORT, SPI_CS_PIN, SPI_CS_FALLING_EDGE_INT, false);

    // Clear the peripheral RX/TX FIFO before configuring the dma transfers.
    peripheral_clear_fifos();

    st = sl_dma_channel_set_peripheral_signal(spidrv_get_tx_dma_handle(),
                                              SL_OT_SPIDRV_SPI_DMA_TX_SIGNAL(SPI_PERIPHERAL_NO));
    VerifyOrExit(st == SL_STATUS_OK, error = OT_ERROR_FAILED);

    // Buffer/padding transfer
    dma_setup_tx_transfer(&s_tx_dma_transfers[1],
                          &default_tx_value,
                          (void *)peripheral_get_txdata_addr(),
                          SL_DMA_CHANNEL_MAX_XFER_UNIT_COUNT,
                          false,
                          &s_tx_dma_descriptors[1]);

    st = sl_dma_channel_submit_transfer_list(spidrv_get_tx_dma_handle(), &s_tx_dma_transfers[1]);
    VerifyOrExit(st == SL_STATUS_OK, error = OT_ERROR_FAILED);

    complete_callback          = aCompleteCallback;
    process_callback           = aProcessCallback;
    context                    = aContext;
    should_process_transaction = false;
    s_ot_spi_slave_ready       = true;

#if defined(SL_CATALOG_POWER_MANAGER_PRESENT)
    sl_power_manager_add_em_requirement(SL_POWER_MANAGER_EM1);
#endif

exit:
    if (in_atomic)
    {
        if (error != OT_ERROR_NONE)
        {
            gpio_deconfigure_cs_interrupt(SPI_CS_RISING_EDGE_INT);
            gpio_deconfigure_cs_interrupt(SPI_CS_FALLING_EDGE_INT);
        }
        CORE_EXIT_ATOMIC();
    }

    if (error != OT_ERROR_NONE)
    {
        if (spidrv_inited)
        {
            IgnoreReturnValue(SPIDRV_DeInit((SPIDRV_Handle_t)&sl_spidrv_handle_data));
        }
        complete_callback          = NULL;
        process_callback           = NULL;
        context                    = NULL;
        should_process_transaction = false;
    }

    return error;
}

void otPlatSpiSlaveDisable(void)
{
    CORE_DECLARE_IRQ_STATE;
    CORE_ENTER_ATOMIC();

    // Disable CS GPIO IRQ.
    gpio_deconfigure_cs_interrupt(SPI_CS_RISING_EDGE_INT);
    gpio_deconfigure_cs_interrupt(SPI_CS_FALLING_EDGE_INT);

    CORE_EXIT_ATOMIC();

    if (s_ot_spi_slave_ready)
    {
        IgnoreReturnValue(SPIDRV_DeInit((SPIDRV_Handle_t)&sl_spidrv_handle_data));
        s_ot_spi_slave_ready = false;
    }

    // Host INT line.
    gpio_deassert_host_request();
#if defined(SPI_HOST_INT_PORT) && defined(SPI_HOST_INT_PIN)
    gpio_set_pin_mode(SPI_HOST_INT_PORT, SPI_HOST_INT_PIN, SL_GPIO_MODE_INPUT, 0U);
#endif

#if defined(SL_CATALOG_POWER_MANAGER_PRESENT)
    sl_power_manager_remove_em_requirement(SL_POWER_MANAGER_EM1);
#endif

    should_process_transaction = false;

    complete_callback = NULL;
    process_callback  = NULL;
    context           = NULL;
}

otError otPlatSpiSlavePrepareTransaction(uint8_t *aOutputBuf,
                                         uint16_t aOutputBufLen,
                                         uint8_t *aInputBuf,
                                         uint16_t aInputBufLen,
                                         bool     aRequestTransactionFlag)
{
    CORE_DECLARE_IRQ_STATE;
    CORE_ENTER_ATOMIC();

    otError error = OT_ERROR_NONE;

    VerifyOrExit(aOutputBufLen <= SL_DMA_CHANNEL_MAX_XFER_UNIT_COUNT, error = OT_ERROR_INVALID_ARGS);
    VerifyOrExit(aInputBufLen <= SL_DMA_CHANNEL_MAX_XFER_UNIT_COUNT, error = OT_ERROR_INVALID_ARGS);

    // Check the CS pin if SPI transactions are in progress (must be high/idle).
    VerifyOrExit(gpio_is_cs_high(), error = OT_ERROR_BUSY);

    if (aOutputBuf)
    {
        IgnoreReturnValue(sl_dma_channel_abort(spidrv_get_tx_dma_handle()));
    }

    if (aInputBuf)
    {
        // Clear the rxFifo only if it is not empty.
        if (peripheral_get_rx_status())
        {
            peripheral_clear_rx_fifo_and_drain();
        }

        IgnoreReturnValue(sl_dma_channel_abort(spidrv_get_rx_dma_handle()));
    }

    // Verify CS is still high after stopping transfers.
    VerifyOrExit(gpio_is_cs_high(), error = OT_ERROR_BUSY);

    if (aOutputBuf != NULL)
    {
        peripheral_clear_tx_fifo_if_needed_and_drain();

        s_tx_output_buf = aOutputBuf;
        s_tx_output_len = aOutputBufLen;
        s_tx_seg0_bytes = aOutputBufLen;
        s_tx_seg1_bytes = (uint16_t)SL_DMA_CHANNEL_MAX_XFER_UNIT_COUNT;
    }

    if (aInputBuf != NULL)
    {
        s_rx_buf = aInputBuf;
        s_rx_len = aInputBufLen;
    }

    // Final CS check before starting transfers.
    VerifyOrExit(gpio_is_cs_high(), error = OT_ERROR_BUSY);

    if (aOutputBuf != NULL)
    {
        sl_status_t st = sl_dma_channel_set_peripheral_signal(spidrv_get_tx_dma_handle(),
                                                              SL_OT_SPIDRV_SPI_DMA_TX_SIGNAL(SPI_PERIPHERAL_NO));
        VerifyOrExit(st == SL_STATUS_OK, error = OT_ERROR_FAILED);

        // Payload
        dma_setup_tx_transfer(&s_tx_dma_transfers[0],
                              aOutputBuf,
                              (void *)peripheral_get_txdata_addr(),
                              aOutputBufLen,
                              true,
                              &s_tx_dma_descriptors[0]);
        // Padding bytes
        dma_setup_tx_transfer(&s_tx_dma_transfers[1],
                              &default_tx_value,
                              (void *)peripheral_get_txdata_addr(),
                              SL_DMA_CHANNEL_MAX_XFER_UNIT_COUNT,
                              false,
                              &s_tx_dma_descriptors[1]);
        s_tx_dma_transfers[0].next = &s_tx_dma_transfers[1];

        st = sl_dma_channel_submit_transfer_list(spidrv_get_tx_dma_handle(), &s_tx_dma_transfers[0]);
        VerifyOrExit(st == SL_STATUS_OK, error = OT_ERROR_FAILED);
    }

    if (aInputBuf != NULL)
    {
        sl_status_t st = sl_dma_channel_set_peripheral_signal(spidrv_get_rx_dma_handle(),
                                                              SL_OT_SPIDRV_SPI_DMA_RX_SIGNAL(SPI_PERIPHERAL_NO));
        VerifyOrExit(st == SL_STATUS_OK, error = OT_ERROR_FAILED);

        dma_setup_rx_transfer(&s_rx_dma_transfer,
                              (void *)peripheral_get_rxdata_addr(),
                              aInputBuf,
                              aInputBufLen,
                              &s_rx_dma_descriptor);

        st = sl_dma_channel_submit_transfer_list(spidrv_get_rx_dma_handle(), &s_rx_dma_transfer);
        VerifyOrExit(st == SL_STATUS_OK, error = OT_ERROR_FAILED);
    }

    if (aRequestTransactionFlag)
    {
        gpio_set_host_request();
    }
    else
    {
        gpio_deassert_host_request();
    }

exit:

    CORE_EXIT_ATOMIC();
    return error;
}

void efr32SpiProcess(void)
{
    if (should_process_transaction)
    {
        if (context)
        {
            process_callback((void *)context);
        }

        should_process_transaction = false;
    }
}
