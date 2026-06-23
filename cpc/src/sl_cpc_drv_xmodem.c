/***************************************************************************/ /**
 * @file
 * @brief CPC XMODEM Driver implementation.
 *******************************************************************************
 * # License
 * <b>Copyright 2023 Silicon Laboratories Inc. www.silabs.com</b>
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

#include <string.h>

#include "sl_cpc_weak_prototypes.h"
#include "cmsis_compiler.h"
#include "sl_hal_ldma.h"
#include "sl_clock_manager.h"
#include "sl_cpc_drv_uart_config.h"
#include "sli_cpc_assert.h"
#include "sli_cpc_reboot_sequence.h"
#include "sli_cpc_fwu.h"
#include "sli_cpc_drv.h"
#include "sli_cpc_crc.h"
#include "sli_cpc_trace.h"
#include "sli_cpc_xmodem.h"

#if defined(SL_CPC_DRV_PERIPH_IS_EUSART)
#include "sl_hal_eusart.h"
#elif defined(SL_CPC_DRV_PERIPH_IS_USART)
#include "sl_hal_usart.h"
#endif

#include "sl_hal_gpio.h"
#include "sl_udelay.h"
#include "sl_cpc_primary_config.h"

#if (SL_CPC_PRIMARY_FIRMWARE_UPGRADE_SUPPORT_ENABLED >= 1)

/*******************************************************************************
 *********************************   DEFINES   *********************************
 ******************************************************************************/
#if defined(_SILICON_LABS_32B_SERIES_2)
#define LDMA_PERIPH                       LDMA
#else
#define LDMA_PERIPH                       LDMA(0)
#endif
#define BTL_MENU_PROMPT "BL > "

/*******************************************************************************
 ***************************  LOCAL VARIABLES   ********************************
 ******************************************************************************/

// Shared variable from the USART driver
extern uint8_t read_channel;
extern uint8_t write_channel;
extern sl_hal_ldma_transfer_config_t rx_config;
extern sl_hal_ldma_transfer_config_t tx_config;

static XmodemFrame_t frame;

/*******************************************************************************
 **************************   LOCAL FUNCTIONS   ********************************
 ******************************************************************************/

/***************************************************************************//**
 * Activate the UART for xmodem transfer
 ******************************************************************************/
void sli_cpc_drv_fwu_init(void)
{
  // The E/USART's pin and config was left untouched. During the de-init :
  // - The DMA channels were stopped
  // - The TX interrupt of the USART was de-activated
  // - The E/USART was stopped

  sl_clock_manager_enable_bus_clock(SL_BUS_CLOCK_LDMAXBAR0);

  // Enable the UART
  #if defined(SL_CPC_DRV_PERIPH_IS_EUSART)
  sl_hal_eusart_enable(SL_CPC_DRV_UART_PERIPHERAL);
  sl_hal_eusart_enable_tx(SL_CPC_DRV_UART_PERIPHERAL);
  sl_hal_eusart_enable_rx(SL_CPC_DRV_UART_PERIPHERAL);
  #else
  sl_hal_usart_enable(SL_CPC_DRV_UART_PERIPHERAL);
  sl_hal_usart_enable_tx(SL_CPC_DRV_UART_PERIPHERAL);
  sl_hal_usart_enable_rx(SL_CPC_DRV_UART_PERIPHERAL);
  #endif
}

/***************************************************************************//**
 * Called when the fwu fsm needs to send a control character and prime the
 * DMA to receive the prompt
 *
 * @param[in] input : The control character to send to the bootloader
 ******************************************************************************/
static void fwu_send_input_char_and_receive_prompt(char input)
{
  // First, setup the LDMA to receive some amount of data
  {
    memset(frame.data, 0x00, sizeof(frame.data));

    // Since this is a unique descriptor being used to start a transfer, its okay for it to be declared on the
    // stack and not being a global variable. This is because sl_hal_ldma_init_transfer loads the descriptor
    // values into the LDMA when starting a transfer,
    // so this descriptor can disappear after this function return and there will be no problem.
    sl_hal_ldma_descriptor_t fwu_receive_prompt_descriptor = (sl_hal_ldma_descriptor_t) SL_HAL_LDMA_DESCRIPTOR_SINGLE_P2M(SL_HAL_LDMA_CTRL_SIZE_BYTE,
      &(SL_CPC_DRV_UART_PERIPHERAL->RXDATA),
      frame.data,
      sizeof(frame.data) - 1);  // Leave space for a trailing \0

    fwu_receive_prompt_descriptor.xfer.done_ifs = 0; // No interrupt

    sl_hal_ldma_init_transfer(LDMA_PERIPH, read_channel, &rx_config, &fwu_receive_prompt_descriptor);
    sl_hal_ldma_start_transfer(LDMA_PERIPH, read_channel);
  }

  // Now that the LDMA is setup to receive the prompt from the bootloader, send the CR character that will
  // make the prompt being printed
  #if defined(SL_CPC_DRV_PERIPH_IS_EUSART)
  sl_hal_eusart_tx(SL_CPC_DRV_UART_PERIPHERAL, input);
  #else
  sl_hal_usart_tx(SL_CPC_DRV_UART_PERIPHERAL, input);
  #endif
}

/***************************************************************************//**
 * Called when the fwu fsm is waiting for the bootloader prompt
 *
 * @return sl_status_t :
 *   SL_STATUS_NOT_READY : No prompt received. This function needs to be called again
 *   SL_STATUS_OK        : The prompt has been received
 ******************************************************************************/
static sl_status_t fwu_wait_for_prompt(void)
{
  if (NULL == strstr((char*)frame.data, BTL_MENU_PROMPT)) {
    return SL_STATUS_NOT_READY;
  } else {
    memset(frame.data, 0x00, sizeof(frame.data));
    return SL_STATUS_OK;
  }
}

/***************************************************************************//**
 * Called when the fwu fsm is waiting for the character XMODEM_CMD_C
 *
 * @return sl_status_t :
 *   SL_STATUS_NOT_READY : No XMODEM_CMD_C character received.
 *                         This function needs to be called again
 *   SL_STATUS_OK        : XMODEM_CMD_C has been received
 ******************************************************************************/
static sl_status_t fwu_wait_for_C(void)
{
  for (size_t i = 0; i != sizeof(frame.data); i++) {
    if (frame.data[i] == XMODEM_CMD_C) {
      return SL_STATUS_OK;
    }
  }

  return SL_STATUS_NOT_READY;
}

/***************************************************************************//**
 * The firmware image sending state machine.
 *
 * @return sl_status_t :
 *   SL_STATUS_IN_PROGRESS : The sending of the firmware image is not complete.
 *                           This function will need to be called again
 *   SL_STATUS_OK          : The image has been completely sent
 ******************************************************************************/
static sl_status_t btl_send_frame_step(void)
{
  static size_t index = 0;
  size_t out_size;
  bool last_chunk;
  sl_status_t ret = SL_STATUS_IN_PROGRESS;

  sl_status_t valid = sl_cpc_get_fwu_chunk(frame.data, index, XMODEM_DATA_SIZE, &out_size, &last_chunk);

  if (valid != SL_STATUS_OK) {
    return ret;
  }

  frame.header = XMODEM_CMD_SOH;
  frame.seq++; // The first seq is 1, then rolling back to 0 after wrapping around.
  frame.seq_neg = (uint8_t)(0xff - frame.seq);

  if (last_chunk) {
    // If this is the last chunk, pad last bytes with 0xFF
    size_t bytes_to_pad = XMODEM_DATA_SIZE - out_size;
    memset(frame.data + out_size, 0xff, bytes_to_pad);
  }

  // We retrieved a valid chunk

  // Xmodem CRC is big-endian. The value returned by sli_cpc_get_crc_sw is little endian
  frame.crc = __REVSH(sli_cpc_get_crc_sw(frame.data, sizeof(frame.data)));

  {
    sl_hal_ldma_descriptor_t fwu_frame_descriptor = (sl_hal_ldma_descriptor_t) SL_HAL_LDMA_DESCRIPTOR_SINGLE_M2P(SL_HAL_LDMA_CTRL_SIZE_BYTE,
      &frame,
      &(SL_CPC_DRV_UART_PERIPHERAL->TXDATA),
      sizeof(frame));

    fwu_frame_descriptor.xfer.done_ifs = 0; // No interrupt

    sl_hal_ldma_init_transfer(LDMA_PERIPH, write_channel, &tx_config, &fwu_frame_descriptor);
    sl_hal_ldma_start_transfer(LDMA_PERIPH, write_channel);    
  }

  if (last_chunk) {
    index = 0;
    ret = SL_STATUS_OK;
  } else {
    index += XMODEM_DATA_SIZE;
  }

  return ret;
}

/***************************************************************************//**
 * Called when the fwu fsm is waiting for an ACK from the bootloader. This
 * function does not wait and returns immediately
 *
 * @param[out] c : The character received by the bootloader. Value valid only
 *                 when the function returns true.
 *
 * @return sl_status :
 *   SL_STATUS_NOT_READY : No character received.
 *                         This function needs to be called again
 *   SL_STATUS_OK        : A character has been received and placed in 'c'
 ******************************************************************************/
static sl_status_t fwu_wait_for_ack(uint8_t *c)
{
  uint32_t status;
#if defined(SL_CPC_DRV_PERIPH_IS_EUSART)
  status = sl_hal_eusart_get_status(SL_CPC_DRV_UART_PERIPHERAL) & EUSART_STATUS_RXFL;
#else
  status = sl_hal_usart_get_status(SL_CPC_DRV_UART_PERIPHERAL) & USART_STATUS_RXDATAV;
#endif

  if (status) {
    *c = (uint8_t)SL_CPC_DRV_UART_PERIPHERAL->RXDATA;
    return SL_STATUS_OK;
  }

  return SL_STATUS_NOT_READY;
}

/***************************************************************************//**
 * The main firmware upgrade finite state machine
 *
 * @return sl_status_t :
 *   SL_STATUS_IN_PROGRESS : The firmware upgrade is still and progress.
 *                           This funcion needs do be called again
 *   SL_STATUS_OK          : The firmware update is done
 ******************************************************************************/
sl_status_t sli_cpc_drv_fwu_step(void)
{
  sl_status_t return_fwu_done = SL_STATUS_IN_PROGRESS;

  static enum {
    FWU_START,
    FWU_WAITING_PROMPT,
    FWU_WAIT_C_CHAR,
    FWU_SEND_XMODEM_FRAME,
    FWU_WAIT_ACK_FRAME,
    FWU_WAIT_ACK_FRAME_AND_SEND_EOT,
    FWU_DONE
  } fwu_state = FWU_START;

  switch (fwu_state) {
    case FWU_START:
      fwu_send_input_char_and_receive_prompt('\r');
      fwu_state = FWU_WAITING_PROMPT;
      break;

    case FWU_WAITING_PROMPT:
    {
      sl_status_t status = fwu_wait_for_prompt();
      if (status == SL_STATUS_OK) {
        TRACE_FWU("Bootloader prompt received");
        // Now that the prompt was received, send a '1' to enter the firmware upload
        fwu_send_input_char_and_receive_prompt('1');

        fwu_state = FWU_WAIT_C_CHAR;
      }
    }
    break;

    case FWU_WAIT_C_CHAR:
    {
      sl_status_t C_received = fwu_wait_for_C();
      if (C_received == SL_STATUS_OK) {
        TRACE_FWU("Bootloader ready for firmware upgrade");

        sl_hal_ldma_stop_transfer(LDMA_PERIPH, read_channel);
        fwu_state = FWU_SEND_XMODEM_FRAME;
      }
    }
    break;

    case FWU_SEND_XMODEM_FRAME:
    {
      sl_status_t status = btl_send_frame_step();
      if (status == SL_STATUS_OK) {
        TRACE_FWU("Last frame sent");
        fwu_state = FWU_WAIT_ACK_FRAME_AND_SEND_EOT;
      } else {
        fwu_state = FWU_WAIT_ACK_FRAME;
      }
    }
    break;

    case FWU_WAIT_ACK_FRAME:
    {
      uint8_t c;
      sl_status_t received = fwu_wait_for_ack(&c);

      if (received == SL_STATUS_OK) {
        if (c == XMODEM_CMD_ACK) {
          TRACE_FWU("Frame ack'ed");
          fwu_state = FWU_SEND_XMODEM_FRAME;
        } else if (c == XMODEM_CMD_NAK) {
          TRACE_FWU("Frame Nack'ed !!");
          SLI_CPC_ASSERT(0);
        } else {
          TRACE_FWU("Frame response : %02hhX", c);
        }
      }
    }
    break;

    case FWU_WAIT_ACK_FRAME_AND_SEND_EOT:
    {
      uint8_t c;
      sl_status_t received = fwu_wait_for_ack(&c);

      if (received == SL_STATUS_OK) {
        if (c == XMODEM_CMD_ACK) {
          #if defined(SL_CPC_DRV_PERIPH_IS_EUSART)
          sl_hal_eusart_tx(SL_CPC_DRV_UART_PERIPHERAL, XMODEM_CMD_EOT);
          #else
          sl_hal_usart_tx(SL_CPC_DRV_UART_PERIPHERAL, XMODEM_CMD_EOT);
          #endif

          TRACE_FWU("Firmware upgrade successful");

          fwu_state = FWU_DONE;
        } else if (c == XMODEM_CMD_NAK) {
          TRACE_FWU("Frame Nack'ed!");
          SLI_CPC_ASSERT(0);
        } else {
          TRACE_FWU("Frame response : %02hhX", c);
        }
      }
    }
    break;

    case FWU_DONE:
      // Reset the internal state for if the firmware update process is restarted
      fwu_state = FWU_START;
      return_fwu_done = SL_STATUS_OK;
      break;

    default:
      SLI_CPC_ASSERT(0);
      break;
  }

  return return_fwu_done;
}

/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/

/***************************************************************************//**
 * Checks if the bootloader is currently running
 *
 * @return bool :
 *   true : The bootloader responded to the poke.
 *   false : The bootloader did not respond to the poke.
 ******************************************************************************/
bool sli_cpc_is_bootloader_running(void)
{
  static bool bootloader_has_been_probed = false;
  static bool is_bootloader_running = false;

  if (bootloader_has_been_probed) {
    return is_bootloader_running;
  }
  bootloader_has_been_probed = true;

  memset(frame.data, 0x00, XMODEM_DATA_SIZE);

  for (size_t i = 0; i != 16; i++) {
    (void) SL_CPC_DRV_UART_PERIPHERAL->RXDATA;
  }

  // Since this is a unique descriptor being used to start a transfer, its okay for it to be declared on the
  // stack and not being a global variable. This is because sl_hal_ldma_init_transfer loads the descriptor
  // values into the LDMA when starting a transfer, so this descriptor can disappear after this function
  // return and there will be no problem.
  sl_hal_ldma_descriptor_t fwu_receive_prompt_descriptor = (sl_hal_ldma_descriptor_t) SL_HAL_LDMA_DESCRIPTOR_SINGLE_P2M(SL_HAL_LDMA_CTRL_SIZE_BYTE,
    &(SL_CPC_DRV_UART_PERIPHERAL->RXDATA),
    &frame.data[0],
    XMODEM_DATA_SIZE - 1); // Leave space for a trailing \0

  fwu_receive_prompt_descriptor.xfer.done_ifs = 0; // No interrupt

  sl_hal_ldma_init_transfer(LDMA_PERIPH, read_channel, &rx_config, &fwu_receive_prompt_descriptor);
  sl_hal_ldma_start_transfer(LDMA_PERIPH, read_channel);


  #if defined(SL_CPC_DRV_PERIPH_IS_EUSART)
  sl_hal_eusart_tx(SL_CPC_DRV_UART_PERIPHERAL, '\r');
  #else
  sl_hal_usart_tx(SL_CPC_DRV_UART_PERIPHERAL, '\r');
  #endif

  const char gecko_string[] = "\r\nGecko";

  #define USEC_IN_SEC 1000000
  #define BITS_PER_UART_BYTE 10
  #define GECKO_STRING_USEC ((USEC_IN_SEC * sizeof(gecko_string) * BITS_PER_UART_BYTE) / SL_CPC_DRV_UART_BAUDRATE)
  #define BOOTLOADER_SAFE_MARGIN_USEC 200

  sl_udelay_wait(GECKO_STRING_USEC + BOOTLOADER_SAFE_MARGIN_USEC);

  if (!strstr((char*)frame.data, &gecko_string[2])) {
    sl_hal_ldma_stop_transfer(LDMA_PERIPH, read_channel);
    is_bootloader_running = false;
    goto end_of_function;
  }

  size_t time_elapsed_ms = 0;

  #define BOOTLOADER_PROMPT_LENGTH 71
  #define MSEC_IN_SEC 1000
  #define GECKO_STRING_MSEC ((USEC_IN_SEC * BOOTLOADER_PROMPT_LENGTH * BITS_PER_UART_BYTE) / SL_CPC_DRV_UART_BAUDRATE)
  #define GECKO_STRING_SAFE_MARGIN_MSEC 2

  do {
    if (time_elapsed_ms == (GECKO_STRING_MSEC + GECKO_STRING_SAFE_MARGIN_MSEC)) {
      WARN("Received the beginning of the bootloader prompt but never received the end under 10ms");
      sl_hal_ldma_stop_transfer(LDMA_PERIPH, read_channel);
      return false;
    }

    sl_udelay_wait(1000);

    time_elapsed_ms++;
  } while (!strstr((char*)frame.data, BTL_MENU_PROMPT));

  sl_hal_ldma_stop_transfer(LDMA_PERIPH, read_channel);

  is_bootloader_running = true;

  end_of_function:
  return is_bootloader_running;
}

#if (SL_CPC_PRIMARY_FIRMWARE_UPGRADE_RECOVERY_PINS_SUPPORT_ENABLED >= 1)
void sli_cpc_drv_fwu_enter_bootloader_via_recovery_pins(void)
{
  // Give a bit of time from the moment the pins were initialized and driven high
  // to now when they will be toggled
  sl_udelay_wait(10);

  {
    sl_gpio_t gpio = { .port = SL_CPC_DRV_UART_WAKE_PORT, .pin = SL_CPC_DRV_UART_WAKE_PIN };
    sl_hal_gpio_clear_pin(&gpio);
  }

  // Give a bit of time to properly
  sl_udelay_wait(100);

  {
    sl_gpio_t gpio = { .port = SL_CPC_DRV_UART_RESET_PORT, .pin = SL_CPC_DRV_UART_RESET_PIN };
    sl_hal_gpio_clear_pin(&gpio);
  }

  // Properly register the falling edge of reset
  sl_udelay_wait(100);

  {
    sl_gpio_t gpio = { .port = SL_CPC_DRV_UART_RESET_PORT, .pin = SL_CPC_DRV_UART_RESET_PIN };
    sl_hal_gpio_set_pin(&gpio);
  }

  // With the UART bootloader, there is no way of knowing when the bootloader has checked
  // for the value of the WAKE pin. It generally takes 25ms for the bootloader to come
  // online and ready for communication, so wait double that just to be sure
  sl_udelay_wait(50000);

  {
    sl_gpio_t gpio = { .port = SL_CPC_DRV_UART_WAKE_PORT, .pin = SL_CPC_DRV_UART_WAKE_PIN };
    sl_hal_gpio_set_pin(&gpio);
  }
}
#endif

#endif // SL_CPC_PRIMARY_FIRMWARE_UPGRADE_SUPPORT_ENABLED
