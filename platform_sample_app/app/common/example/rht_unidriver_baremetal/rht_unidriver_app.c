/***************************************************************************//**
 * @file
 * @brief RHT UniDriver API exercise (Si70xx on BRD4002A or SHT4x on WPK BRD4002B)
 *******************************************************************************
 * # License
 * <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * SPDX-License-Identifier: Zlib
 *
 ******************************************************************************/
#include <stdio.h>
#include <stdbool.h>
#include "rht_unidriver_app.h"
#include "sl_i2cspm_instances.h"
#include "sl_rht_unidriver.h"
#include "sl_sleeptimer.h"

/** Periodic print interval (ms). */
#define RHT_APP_SAMPLE_MS  2000U

static sl_sleeptimer_timer_handle_t s_periodic_timer;
static uint32_t s_rh_milli;
static int32_t s_temp_milli_c;
/** Set from the sleeptimer callback; sampling runs in @ref rht_unidriver_app_process_action. */
static volatile bool s_periodic_sample_pending;

/*
 * SHT4x path uses @ref sl_sleeptimer_delay_millisecond inside
 * @ref sl_sht4x_measure_rh_and_temp. Calling that from the same sleeptimer's
 * IRQ/callback deadlocks. Si70xx measure has no such delay, so BRD4002A worked.
 * Always take RH/T via @ref sl_rht_unidriver_measure_rh_and_temp from thread
 * context (main loop), not from the timer callback.
 */

static void print_status_line(const char *label, sl_status_t status)
{
  printf("  %-28s status=0x%08lX\r\n", label, (unsigned long)status);
}

/***************************************************************************//**
 * One-shot API walk-through after successful init.
 ******************************************************************************/
static void rht_unidriver_exercise_optional_apis(void)
{
  sl_status_t st;
  uint8_t fw_rev;
  uint8_t lp_cmd;
  int32_t v_data;

  st = sl_rht_unidriver_get_firmware_revision(&fw_rev);
  print_status_line("get_firmware_revision", st);
  printf("    fw_rev=0x%02X (Si70xx; SHT4x returns NOT_SUPPORTED)\r\n", fw_rev);

  st = sl_rht_unidriver_enable_low_power_mode(true, &lp_cmd);
  print_status_line("enable_low_power_mode(true)", st);
  if (st == SL_STATUS_OK) {
    printf("    SHT4x measure cmd (LP)=0x%02X\r\n", lp_cmd);
  }

  st = sl_rht_unidriver_enable_low_power_mode(false, &lp_cmd);
  print_status_line("enable_low_power_mode(false)", st);
  if (st == SL_STATUS_OK) {
    printf("    SHT4x measure cmd (HP)=0x%02X\r\n", lp_cmd);
  }

  st = sl_rht_unidriver_measure_analog_voltage(&v_data);
  print_status_line("measure_analog_voltage", st);
  if (st == SL_STATUS_OK) {
    printf("    v_data=%ld (Si7013 only)\r\n", (long)v_data);
  }

  st = sl_rht_unidriver_start_no_hold_measure_rh_and_temp();
  print_status_line("start_no_hold_measure", st);
  if (st == SL_STATUS_OK) {
    sl_sleeptimer_delay_millisecond(25);
    st = sl_rht_unidriver_read_rh_and_temp(&s_rh_milli, &s_temp_milli_c);
    print_status_line("read_rh_and_temp (after no-hold)", st);
    if (st == SL_STATUS_OK) {
      printf("    RH %%x1000=%lu  Temperature_mC=%ld\r\n",
             (unsigned long)s_rh_milli,
             (long)s_temp_milli_c);
    }
  }
}

static void on_periodic_timeout(sl_sleeptimer_timer_handle_t *handle, void *data)
{
  (void)handle;
  (void)data;

  s_periodic_sample_pending = true;
}

void rht_unidriver_app_init(void)
{
  sl_status_t st;
  uint8_t device_id;

  sl_sleeptimer_init();

  printf("\r\n--- RHT UniDriver bare-metal test ---\r\n");

  st = sl_rht_unidriver_init(sl_i2cspm_sensor);
  print_status_line("sl_rht_unidriver_init", st);
  if (st != SL_STATUS_OK) {
    printf("Init failed; check I2C wiring and RHT enable.\r\n");
    return;
  }

  st = sl_rht_unidriver_get_device_id(&device_id);
  print_status_line("sl_rht_unidriver_get_device_id", st);
  if (st == SL_STATUS_OK) {
    if (device_id == RHT_UNIDRIVER_SHT4X_ID) {
      printf("    Sensor: SHT4x (placeholder ID 0x%02X)\r\n", device_id);
    } else {
      printf("    Si70xx silicon ID=0x%02X\r\n", device_id);
    }
  }

  rht_unidriver_exercise_optional_apis();

  printf("Starting periodic samples every %u ms...\r\n", (unsigned)RHT_APP_SAMPLE_MS);
  sl_sleeptimer_start_periodic_timer_ms(&s_periodic_timer,
                                        RHT_APP_SAMPLE_MS,
                                        on_periodic_timeout,
                                        NULL,
                                        0,
                                        0);
}

void rht_unidriver_app_process_action(void)
{
  if (!s_periodic_sample_pending) {
    return;
  }
  s_periodic_sample_pending = false;

  sl_status_t st = sl_rht_unidriver_measure_rh_and_temp(&s_rh_milli, &s_temp_milli_c);
  if (st != SL_STATUS_OK) {
    printf("measure_rh_and_temp failed: 0x%08lX\r\n", (unsigned long)st);
    return;
  }

  printf("RH %%x1000=%lu  Temperature_mC=%ld\r\n",
         (unsigned long)s_rh_milli,
         (long)s_temp_milli_c);
}
