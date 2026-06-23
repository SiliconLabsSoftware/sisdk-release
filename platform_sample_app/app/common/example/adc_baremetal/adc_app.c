/***************************************************************************//**
 * @file adc_app.c
 * @brief ADC bare-metal sample using sl_hal_adc (immediate single conversion).
 *
 * @details
 *   GPIO loopback drives the ADC positive input, ADC0 performs immediate
 *   scans on channel 0, and the second conversion result is used (see HAL
 *   documentation for successive-approximation behavior).
 *******************************************************************************
 * # License
 * <b>Copyright 2020 Silicon Laboratories Inc. www.silabs.com</b>
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
#include "em_device.h"

#if defined(ADC_PRESENT)

#include <stdio.h>
#include "sl_hal_adc.h"
#include "sl_hal_gpio.h"
#include "sl_clock_manager.h"
#include "sl_device_peripheral.h"
#include "sl_simple_led.h"
#include "sl_simple_led_instances.h"
#include "sl_sleeptimer.h"
#include "sl_code_classification.h"

/*******************************************************************************
 *******************************   DEFINES   ***********************************
 ******************************************************************************/

#ifndef LED_INSTANCE
#define LED_INSTANCE    sl_led_led0
#endif

#ifndef SAMPLE_PERIOD_MS
#define SAMPLE_PERIOD_MS         500
#endif

/// Scan channel used by this sample (matches @ref adc_test.c single-channel tests).
#define ADC_SAMPLE_CHANNEL      0U
// Board pin mapping: align with platform/peripheral/test/src/adc_test.c
#if defined(SIMG301_BRD4408A)
#define ADC0_IN_GPIO_PORT     SL_HAL_ADC_PORT_POS_PORTC
#define ADC0_IN_GPIO_PIN      0
#define GPIO_ADC0_PORT        SL_GPIO_PORT_C
#define GPIO_ADC0_PIN         0
#define GPIO_OUT_PORT         SL_GPIO_PORT_B
#define GPIO_OUT_PIN          0

#elif defined(SIMG301_BRD4407A)
#define ADC0_IN_GPIO_PORT     SL_HAL_ADC_PORT_POS_PORTC
#define ADC0_IN_GPIO_PIN      0
#define GPIO_ADC0_PORT        SL_GPIO_PORT_C
#define GPIO_ADC0_PIN         0
#define GPIO_OUT_PORT         SL_GPIO_PORT_A
#define GPIO_OUT_PIN          5

#elif defined(EFR32XG2B_BRD1011A) || defined(EFR32MG2B_BRD4418A) || defined(EFR32BG2B_BRD4419A)
// ADC0 related config
#define ADC0_IN_GPIO_PORT     SL_HAL_ADC_PORT_POS_PORTC
#define ADC0_IN_GPIO_PIN      6
#define GPIO_ADC0_PORT        SL_GPIO_PORT_C
#define GPIO_ADC0_PIN         6

//GPIO output port and pin  
#define GPIO_OUT_PORT         SL_GPIO_PORT_A
#define GPIO_OUT_PIN          5

// ADC1 related config
#define ADC1_IN_GPIO_PORT      SL_HAL_ADC_PORT_POS_PORTD
#define ADC1_IN_GPIO_PIN       2
#define GPIO_ADC1_PORT         SL_GPIO_PORT_D
#define GPIO_ADC1_PIN          2
#else
 #error Define pin mapping for this board
#endif

/*******************************************************************************
 ***************************  LOCAL VARIABLES   ********************************
 ******************************************************************************/

static sl_gpio_t gpio_loopback;
static sl_gpio_t gpio_adc_in;

static sl_sleeptimer_timer_handle_t sample_timer;
static volatile bool sample_due = false;
static uint32_t sample_count = 0;

/*******************************************************************************
 *********************   LOCAL FUNCTION PROTOTYPES   ***************************
 ******************************************************************************/

SL_CODE_RAM static void on_sample_tick(sl_sleeptimer_timer_handle_t *handle,
                                       void *data);

static void config_gpios(void);
static void adc_hw_init(void);
static void adc_sample_once(void);

/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/

void adc_init(void)
{
  // Prevent buffering of output (newlib/GCC only; IAR DLIB does not expose setvbuf).
#if !defined(__CROSSWORKS_ARM) && defined(__GNUC__)
  setvbuf(stdout, NULL, _IONBF, 0);
#endif

  config_gpios();

  sl_clock_manager_enable_bus_clock(SL_BUS_CLOCK_ADC0);

  adc_hw_init();

  sl_hal_gpio_set_pin(&gpio_loopback);

  sl_sleeptimer_start_periodic_timer_ms(&sample_timer,
                                        SAMPLE_PERIOD_MS,
                                        on_sample_tick, NULL,
                                        0,
                                        SL_SLEEPTIMER_NO_HIGH_PRECISION_HF_CLOCKS_REQUIRED_FLAG);

  // stdout is redirected to VCOM in project configuration
  printf("Welcome to the ADC bare-metal example application\r\n");
  printf("Sampling channel %u every %u ms\r\n",
         (unsigned)ADC_SAMPLE_CHANNEL, (unsigned)SAMPLE_PERIOD_MS);
}

void adc_process_action(void)
{
  if (sample_due) {
    adc_sample_once();
    sample_due = false;
  }
}

/*******************************************************************************
 **************************   LOCAL FUNCTIONS   *******************************
 ******************************************************************************/

static void config_gpios(void)
{
  gpio_loopback.port = GPIO_OUT_PORT;
  gpio_loopback.pin = GPIO_OUT_PIN;

  gpio_adc_in.port = GPIO_ADC0_PORT;
  gpio_adc_in.pin = GPIO_ADC0_PIN;

  sl_clock_manager_enable_bus_clock(SL_BUS_CLOCK_GPIO);

  GPIO->CDBUSALLOC_SET = _GPIO_CDBUSALLOC_CDEVEN0_ADC0;
  GPIO->CDBUSALLOC_SET = _GPIO_CDBUSALLOC_CDODD0_ADC0;

  sl_hal_gpio_set_pin_mode(&gpio_loopback, SL_GPIO_MODE_PUSH_PULL, 1);
  sl_hal_gpio_set_pin_mode(&gpio_adc_in, SL_GPIO_MODE_DISABLED, 1);
}

static void adc_hw_init(void)
{
  sl_hal_adc_scan_entry_t entry = SL_HAL_ADC_SCAN_ENTRY_DEFAULT;
  entry.neg_pin = 1;
  entry.pos_port = ADC0_IN_GPIO_PORT;
  entry.pos_pin = ADC0_IN_GPIO_PIN;

  sl_hal_adc_init_t init = SL_HAL_ADC_INIT_DEFAULT;
  init.scan_trigger = SL_HAL_ADC_TRIGGER_IMMEDIATE;
  init.scan_trigger_action = SL_HAL_ADC_TRIGGER_ACTION_ONCE;
  init.entries[SL_HAL_ADC_CHANNEL_ID_0] = entry;

  sl_hal_adc_config_t config = SL_HAL_ADC_CONFIG_DEFAULT;
  config.acquisition_time = 16;
  init.config[SL_HAL_ADC_CONFIG_ID_0] = config;

  sl_clock_branch_t clock_branch = sl_device_peripheral_get_clock_branch(SL_PERIPHERAL_ADC0);
  uint32_t branch_clock_freq = 0;
  sl_clock_manager_get_clock_branch_frequency(clock_branch, &branch_clock_freq);

  sl_hal_adc_reset(ADC0);
  sl_hal_adc_enable_interrupts(ADC0, ADC_IF_SCANENTRYDONE);

  sl_hal_adc_init(ADC0, &init, branch_clock_freq);
  sl_hal_adc_enable(ADC0);
}

static void adc_sample_once(void)
{
  sl_hal_adc_result_t second_sample;

  sl_hal_adc_flush_fifo(ADC0);
  while (ADC0->STATUS & ADC_STATUS_SCANFIFOFLUSHING) {
  }

  sl_hal_adc_set_scan_mask(ADC0, 1U << ADC_SAMPLE_CHANNEL);

  // First (warm-up) conversion: drain the FIFO entry and discard it.
  sl_hal_adc_start(ADC0);
  while (!sl_hal_adc_get_enabled_pending_interrupts(ADC0)) {
  }
  (void)sl_hal_adc_pull(ADC0);
  sl_hal_adc_clear_interrupts(ADC0, ADC_IF_SCANENTRYDONE);

  // Second conversion: this is the result we report.
  sl_hal_adc_start(ADC0);
  while (!sl_hal_adc_get_enabled_pending_interrupts(ADC0)) {
  }
  (void)sl_hal_adc_peek(ADC0);
  sl_hal_adc_clear_interrupts(ADC0, ADC_IF_SCANENTRYDONE);
  second_sample = sl_hal_adc_pull(ADC0);

  sample_count++;

  // Print the current ADC sample to vcom
  printf("\r\n");
  printf("Sample #%lu\r\n", (unsigned long)sample_count);
  printf("ADC data = %lu (0x%04lX)\r\n",
         (unsigned long)second_sample.data,
         (unsigned long)second_sample.data);

  sl_led_toggle(&LED_INSTANCE);
}

static void on_sample_tick(sl_sleeptimer_timer_handle_t *handle, void *data)
{
  (void)handle;
  (void)data;
  sample_due = true;
}

#else /* !ADC_PRESENT */

void adc_init(void)
{
}

void adc_process_action(void)
{
}

#endif /* ADC_PRESENT */
