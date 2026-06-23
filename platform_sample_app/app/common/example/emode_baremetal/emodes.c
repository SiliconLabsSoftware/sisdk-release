/***************************************************************************//**
 * @file
 * @brief Energy modes functions
 *******************************************************************************
 * # License
 * <b>Copyright 2021 Silicon Laboratories Inc. www.silabs.com</b>
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

#include "emodes.h"
#include "em_cmu.h"
#include "sl_hal_emu.h"
#include "sl_power_manager.h"
#include "core_main.h"
#include "sl_hal_gpio.h"
#ifdef RTCC_PRESENT
#include "sl_hal_rtcc.h"
#endif // RTCC_PRESENT
#ifdef BURTC_PRESENT
#include "sl_hal_burtc.h"
#endif // BURTC_PRESENT
#ifdef SYSRTC_PRESENT
#include "sl_hal_sysrtc.h"
#endif // SYSRTC_PRESENT

/*******************************************************************************
 ***************************  LOCAL VARIABLES   ********************************
 ******************************************************************************/

// Flag to indicate to power manager if application can sleep
static bool ok_to_sleep = false;
// Flag for ISR exit behavior
static sl_power_manager_on_isr_exit_t isr_ok_to_sleep = SL_POWER_MANAGER_IGNORE;

/*******************************************************************************
 *********************   LOCAL FUNCTION PROTOTYPES   ***************************
 ******************************************************************************/

static void disable_clocks(void);
static void disable_HF_clocks(void);
static void disable_LF_clocks(void);
static void prime_calc(void); //Calculate Primes
static void em_EM0(energy_mode_t *mode);
static void em_EM1(energy_mode_t *mode);
static void em_EM2(energy_mode_t *mode);
static void em_EM3(energy_mode_t *mode);
static void em_EM4(energy_mode_t *mode);
static void em_EM0_Hfxo(void);
static void em_EM1_Hfxo(void);
static void em_EM0_Fsrco(void);
static void em_EM0_Hfrco(CMU_HFRCODPLLFreq_TypeDef band);
static void em_EM1_Fsrco(void);
static void em_EM1_Hfrco(CMU_HFRCODPLLFreq_TypeDef band);
static void em_EM3_UlfrcoBURTC(bool powerdown_ram);
static void em_EM4_LfrcoBURTC(void);
static void em_EM4_UlfrcoBURTC(void);
static void em_EM4_none(void);
#if defined(RTCC_PRESENT)
static void em_EM2_RTCC(CMU_Select_TypeDef osc, bool powerdown_ram);
#endif // RTCC_PRESENT
#if defined(SYSRTC_PRESENT)
static void em_EM2_LfrcoSYSRTC(bool powerdown_ram);
#if !(defined(ZGM230SB27HGN) && ZGM230SB27HGN == 1)
/* BRD4205B doesn't have a LFXO mounted out of the box
   hence excluding LFXO options for this board. */
static void em_EM2_LfxoSYSRTC(bool powerdown_ram);
#endif // !(defined(ZGM230SB27HGN) && ZGM230SB27HGN == 1)
#endif //SYSRTC_PRESENT

/*******************************************************************************
 **************************   LOCAL FUNCTIONS   *******************************
 ******************************************************************************/

/***************************************************************************//**
 * Enter EM0 with HFXO running.
 *
 * Enter EM0 Active mode with HFXO running and all other peripherals and
 * clocks disabled.
 ******************************************************************************/
static void em_EM0_Hfxo(void)
{
  // Make sure clocks are disabled.
  disable_clocks();

  // Set HFXO as system clock.
#if (_SILICON_LABS_32B_SERIES_2_CONFIG > 1)
  CMU_ClockEnable(cmuClock_HFXO, true);
  CMU_ClockSelectSet(cmuClock_SYSCLK, cmuSelect_HFXO);
  CMU_ClockEnable(cmuClock_HFXO, false);
#else
  CMU_ClockSelectSet(cmuClock_SYSCLK, cmuSelect_HFXO);
#endif
}

/***************************************************************************//**
 * Enter EM0 with FSRCO running.
 *
 * Enter EM0 Active mode with FSRCO running and all other peripherals and
 * clocks disabled.
 ******************************************************************************/
static void em_EM0_Fsrco(void)
{
  // Make sure clocks are disabled.
  disable_clocks();

  // Set FSRCO as system clock.
  CMU_ClockSelectSet(cmuClock_SYSCLK, cmuSelect_FSRCO);
}

/***************************************************************************//**
 * Enter EM0 with HFRCO running at desired frequency.
 *
 * Enter EM0 Active mode with HFRCO running Between 72 and 1 MHz and all other
 * peripherals and clocks disabled. It takes an input parameter for selecting
 * the desired frequency.
 ******************************************************************************/
static void em_EM0_Hfrco(CMU_HFRCODPLLFreq_TypeDef band)
{
  // Make sure clocks are disabled.
  disable_clocks();

  // Set HFRCO as system clock.
  CMU_ClockSelectSet(cmuClock_SYSCLK, cmuSelect_HFRCODPLL);

  // Set HFRCO frequency.
  CMU_HFRCODPLLBandSet(band);
}

/***************************************************************************//**
 * Enter EM1 with HFXO running.
 *
 * Enter EM1 Sleep mode with HFXO running and all other peripherals and
 * clocks disabled.
 ******************************************************************************/
static void em_EM1_Hfxo(void)
{
  // Set HFXO for as system clock.
#if (_SILICON_LABS_32B_SERIES_2_CONFIG > 1)
  CMU_ClockEnable(cmuClock_HFXO, true);
  CMU_ClockSelectSet(cmuClock_SYSCLK, cmuSelect_HFXO);
  CMU_ClockEnable(cmuClock_HFXO, false);
#else
  CMU_ClockSelectSet(cmuClock_SYSCLK, cmuSelect_HFXO);
#endif
  // Set EM1 requirement and allow sleep - sl_power_manager_sleep() is called in main loop
  // NOTE: If wake-up logic is added, call sl_power_manager_remove_em_requirement(SL_POWER_MANAGER_EM1)
  //       to release this requirement when no longer needed.
  sl_power_manager_add_em_requirement(SL_POWER_MANAGER_EM1);
  ok_to_sleep = true;
  isr_ok_to_sleep = SL_POWER_MANAGER_SLEEP;
}

/***************************************************************************//**
 * Enter EM1 with FSRCO running.
 *
 * Enter EM1 Sleep mode with FSRCO running and all other peripherals and
 * clocks disabled.
 ******************************************************************************/
static void em_EM1_Fsrco(void)
{
  // Set FSRCO as system clock.
  CMU_ClockSelectSet(cmuClock_SYSCLK, cmuSelect_FSRCO);

  // Set EM1 requirement and allow sleep - sl_power_manager_sleep() is called in main loop
  // NOTE: If wake-up logic is added, call sl_power_manager_remove_em_requirement(SL_POWER_MANAGER_EM1)
  //       to release this requirement when no longer needed.
  sl_power_manager_add_em_requirement(SL_POWER_MANAGER_EM1);
  ok_to_sleep = true;
  isr_ok_to_sleep = SL_POWER_MANAGER_SLEEP;
}

/***************************************************************************//**
 * Enter EM1 with HFRCO running at desired frequency.
 *
 * Enter EM1 Sleep mode with HFRCO running Between 38 and 1 MHz and all other
 * peripherals and clocks disabled. It takes an input parameter for selecting
 * the desired frequency.
 ******************************************************************************/
static void em_EM1_Hfrco(CMU_HFRCODPLLFreq_TypeDef band)
{
  // Set HFRCODPLL as system clock.
  CMU_ClockSelectSet(cmuClock_SYSCLK, cmuSelect_HFRCODPLL);

  // Set HFRCO frequency.
  CMU_HFRCODPLLBandSet(band);

  // Set EM1 requirement and allow sleep - sl_power_manager_sleep() is called in main loop
  // NOTE: If wake-up logic is added, call sl_power_manager_remove_em_requirement(SL_POWER_MANAGER_EM1)
  //       to release this requirement when no longer needed.
  sl_power_manager_add_em_requirement(SL_POWER_MANAGER_EM1);
  ok_to_sleep = true;
  isr_ok_to_sleep = SL_POWER_MANAGER_SLEEP;
}

#if defined(RTCC_PRESENT)
/***************************************************************************//**
 * Enter EM2 with RTCC running on a low frequency oscillator.
 *
 * Enter EM2 Deep Sleep mode with RTCC running from 32.768 kHz LFXO or LFRCO.
 * Parameter osc is used to choose the RTCC source clock. If powerDownRam is set
 * to true, Ram is turned down to retain only 16 kB.
 ******************************************************************************/
static void em_EM2_RTCC(CMU_Select_TypeDef osc, bool powerdown_ram)
{
  // Route desired oscillator to RTCC clock tree.
  CMU_ClockSelectSet(cmuClock_RTCCCLK, osc);

  // Setup RTC parameters
  sl_hal_rtcc_init_t rtcc_init = SL_HAL_RTCC_INIT_DEFAULT;
  rtcc_init.prescaler = SL_HAL_RTCC_COUNTER_PRESCALER_1;

  // Initialize RTCC
  CMU_ClockEnable(cmuClock_RTCC, true);
  sl_hal_rtcc_reset();
  sl_hal_rtcc_init(&rtcc_init);
  sl_hal_rtcc_enable();
  // Power down all RAM blocks except block 0
  if (powerdown_ram) {
    sl_hal_emu_ram_power_down(SRAM_BASE, 0);
  }

  // Allow sleep - sl_power_manager_sleep() is called in main loop
  ok_to_sleep = true;
  isr_ok_to_sleep = SL_POWER_MANAGER_SLEEP;
}
#endif // RTCC_PRESENT

#if defined(SYSRTC_PRESENT)
/***************************************************************************//**
 * Enter EM2 with SYSRTC running with LFRCO.
 *
 * Enter EM2 Deep Sleep mode with SYSRTC running with 32.768 kHz LFRCO and all
 * other peripheral and clocks disabled. If powerDownRam is set to true, Ram is turned
 * down to retain only 16 kB.
 ******************************************************************************/
static void em_EM2_LfrcoSYSRTC(bool powerdown_ram)
{
  // Route the LFRCO clock to SYSRTC.
  CMU_ClockSelectSet(cmuClock_SYSRTC, cmuSelect_LFRCO);
  CMU_ClockEnable(cmuClock_SYSRTC, true);

  // Setup RTC parameters.
  sl_hal_sysrtc_config_t sysrtc_config = SYSRTC_CONFIG_DEFAULT;

  // Initialize RTC.
  sl_hal_sysrtc_init(&sysrtc_config);

  // Power down all RAM blocks except block 1
  if (powerdown_ram) {
    sl_hal_emu_ram_power_down(SRAM_BASE, 0);
  }

  // Make sure unwanted oscillators are disabled specifically for EM2 and LFRCO.
  CMU_OscillatorEnable(cmuOsc_LFXO, false, true);

  // Allow sleep - sl_power_manager_sleep() is called in main loop
  ok_to_sleep = true;
  isr_ok_to_sleep = SL_POWER_MANAGER_SLEEP;
}

#if !(defined(ZGM230SB27HGN) && ZGM230SB27HGN == 1)
/***************************************************************************//**
 * Enter EM2 with SYSRTC running with LFXO.
 *
 * Enter EM2 Deep Sleep mode with SYSRTC running with LFXO and all other
 * peripheral and clocks disabled. If powerDownRam is set to true, Ram is turned
 * down to retain only 16 kB.
 ******************************************************************************/
static void em_EM2_LfxoSYSRTC(bool powerdown_ram)
{
  // Route the LFXO clock to SYSRTC.
  CMU_ClockSelectSet(cmuClock_SYSRTC, cmuSelect_LFXO);
  CMU_ClockEnable(cmuClock_SYSRTC, true);

  // Setup RTC parameters.
  sl_hal_sysrtc_config_t sysrtc_config = SYSRTC_CONFIG_DEFAULT;

  // Initialize RTC.
  sl_hal_sysrtc_init(&sysrtc_config);

  // Power down all RAM blocks except block 1
  if (powerdown_ram) {
    sl_hal_emu_ram_power_down(SRAM_BASE, 0);
  }

  // Make sure unwanted oscillators are disabled specifically for EM2 and LFXO.
  CMU_OscillatorEnable(cmuOsc_LFRCO, false, true);

  // Allow sleep - sl_power_manager_sleep() is called in main loop
  ok_to_sleep = true;
  isr_ok_to_sleep = SL_POWER_MANAGER_SLEEP;
}
#endif //!(defined(ZGM230SB27HGN) && ZGM230SB27HGN == 1)
#endif // SYSRTC_PRESENT

/***************************************************************************//**
 * Enter EM3 with BURTC running on ULFRCO.
 *
 * Enter EM3 Stop mode with BURTC running on 1kHz ULFRCO and all other
 * peripheral and clocks disabled. If powerDownRam is set to true, Ram is turned
 * down to retain only 16 kB.
 ******************************************************************************/
static void em_EM3_UlfrcoBURTC(bool powerdown_ram)
{
  // Select ULFRCO as the BURTC clock source.
  CMU_ClockSelectSet(cmuClock_EM4GRPACLK, cmuSelect_ULFRCO);

  // Setup BURTC.
  sl_hal_burtc_init_t burtc_init = SL_HAL_BURTC_INIT_DEFAULT;
  CMU_ClockEnable(cmuClock_BURTC, true);

  slx_power_manager_update_clock_info();

  sl_hal_burtc_init(&burtc_init);
  sl_hal_burtc_enable();
  sl_hal_burtc_start();

  // Power down all RAM blocks except block 1
  if (powerdown_ram) {
    sl_hal_emu_ram_power_down(SRAM_BASE, 0);
  }

  // Allow sleep - sl_power_manager_sleep() is called in main loop
  ok_to_sleep = true;
  isr_ok_to_sleep = SL_POWER_MANAGER_SLEEP;
}

/***************************************************************************//**
 * Enter EM4 with BURTC running on a LFRCO.
 *
 * Enter EM4 Hibernate Mode with BURTC running on a 32.768 kHz LFRCO. Only 128b
 * RAM is retained in this mode.
 ******************************************************************************/
static void em_EM4_LfrcoBURTC(void)
{
  // Make sure clocks are disabled.
  disable_clocks();

  // Select LFRCO as the BURTC clock source.
  CMU_ClockSelectSet(cmuClock_EM4GRPACLK, cmuSelect_LFRCO);

  // Setup BURTC.
  sl_hal_burtc_init_t burtc_init = SL_HAL_BURTC_INIT_DEFAULT;
  CMU_ClockEnable(cmuClock_BURTC, true);

  sl_hal_burtc_init(&burtc_init);
  sl_hal_burtc_enable();
  sl_hal_burtc_start();

  // Explicitly enter EM4 mode
  sl_power_manager_enter_em4();
}

/***************************************************************************//**
 * Enter EM4 with BURTC running on a ULFRCO.
 *
 * Enter EM4H Hibernate Mode with BURTC running on a 1kHz ULFRCO. Only 128b RAM
 * is retained in this mode.
 ******************************************************************************/
static void em_EM4_UlfrcoBURTC(void)
{
  // Make sure clocks are disabled.
  disable_clocks();

  // Select ULFRCO as the BURTC clock source.
  CMU_ClockSelectSet(cmuClock_EM4GRPACLK, cmuSelect_ULFRCO);

  // Setup BURTC parameters
  sl_hal_burtc_init_t burtc_init = SL_HAL_BURTC_INIT_DEFAULT;
  CMU_ClockEnable(cmuClock_BURTC, true);

  sl_hal_burtc_init(&burtc_init);
  sl_hal_burtc_enable();
  sl_hal_burtc_start();

  // Explicitly enter EM4 mode
  sl_power_manager_enter_em4();
}

/***************************************************************************//**
 * Enter EM4H without RTCC or CRYOTIMER.
 *
 * Enter EM4H Hibernate Mode with no RTCC or CRYOTIMER running. Only 128b RAM is
 * retained in this mode.
 ******************************************************************************/
static void em_EM4_none(void)
{
  // Make sure clocks are disabled.
  disable_clocks();

  // Explicitly enter EM4 mode
  sl_power_manager_enter_em4();
}

/***************************************************************************//**
 * Disable all high frequency clocks
 ******************************************************************************/
static void disable_HF_clocks(void)
{
  // Disable high frequency peripherals
#if defined(_SILICON_LABS_32B_SERIES_2_CONFIG_1)
  USART0->EN_CLR = 0x1;
  USART1->EN_CLR = 0x1;
  USART2->EN_CLR = 0x1;
  TIMER0->EN_CLR = 0x1;
  TIMER1->EN_CLR = 0x1;
  TIMER2->EN_CLR = 0x1;
  TIMER3->EN_CLR = 0x1;
#if defined(ACMP0)
  ACMP0->EN_CLR = 0x1;
#endif // (ACMP0)
#if defined(ACMP1)
  ACMP1->EN_CLR = 0x1;
#endif // (ACMP1)
#if defined(IADC0)
  IADC0->EN_CLR = 0x1;
#endif // (IADC0)
#if defined(I2C0)
  I2C0->EN_CLR = 0x1;
#endif // (I2C0)
#if defined(I2C1)
  I2C1->EN_CLR = 0x1;
#endif // (I2C1)
  GPCRC->EN_CLR = 0x1;
#else
  CMU->CLKEN0_SET = CMU_CLKEN0_HFRCO0;
#endif
  CMU_ClockSelectSet(cmuClock_SYSCLK, cmuSelect_FSRCO);
#if (_SILICON_LABS_32B_SERIES_2_CONFIG <= 2)
  // Check that HFRCODPLL and HFXO are not requested
  while (((HFRCO0->STATUS & _HFRCO_STATUS_ENS_MASK) != 0U)
         || ((HFXO0->STATUS & _HFXO_STATUS_ENS_MASK) != 0U)) {
  }
#endif
#if (_SILICON_LABS_32B_SERIES_2_CONFIG > 1)
#if defined(USART_PRESENT)
  CMU_ClockEnable(cmuClock_USART0, false);
#endif
  CMU_ClockEnable(cmuClock_PRS, false);
  CMU_ClockEnable(cmuClock_HFXO, false);
  CMU_ClockEnable(cmuClock_DPLL0, false);
  CMU_ClockEnable(cmuClock_HFRCO0, false);
  CMU_ClockEnable(cmuClock_MSC, false);
  CMU_ClockEnable(cmuClock_DCDC, false);
#endif
}

/***************************************************************************//**
 * Disable all low frequency clocks
 ******************************************************************************/
static void disable_LF_clocks(void)
{
  // Disable low frequency peripherals
#if defined(RTCC_PRESENT)
  RTCC->EN_CLR = 0x1;
#endif
#if  defined(_SILICON_LABS_32B_SERIES_2_CONFIG_1)
  WDOG0->EN_CLR = 0x1;
  WDOG1->EN_CLR = 0x1;
  LETIMER0->EN_CLR = 0x1;
  BURTC->EN_CLR = 0x1;
#else
  CMU_ClockEnable(cmuClock_LFRCO, true);
  CMU->CLKEN0_SET = CMU_CLKEN0_LFRCO;
  CMU_ClockEnable(cmuClock_LFXO, true);
  CMU->CLKEN0_SET = CMU_CLKEN0_LFXO;
#endif

  // Check that all low frequency oscillators are stopped
  while ((LFRCO->STATUS != 0U) && (LFXO->STATUS != 0U)) {
  }
#if (_SILICON_LABS_32B_SERIES_2_CONFIG > 1)
#if defined(RTCC_PRESENT)
  CMU_ClockEnable(cmuClock_RTCC, false);
#endif
  CMU_ClockEnable(cmuClock_LFRCO, false);
  CMU_ClockEnable(cmuClock_LFXO, false);
#endif
}

/***************************************************************************//**
 * Disable all clocks to achieve lowest current consumption numbers.
 ******************************************************************************/
static void disable_clocks(void)
{
  // Disable High Frequency Clocks
  disable_HF_clocks();

  // Disable Low Frequency Clocks
  disable_LF_clocks();
}

/***************************************************************************//**
 * Calculate primes.
 ******************************************************************************/
static void prime_calc(void)
{
  uint32_t i, d, n;
  uint32_t primes[64];

  // Find prime numbers forever.
  while (1) {
    primes[0] = 1;
    for (i = 1; i < 64; ) {
      for (n = primes[i - 1] + 1;; n++) {
        for (d = 2; d <= n; d++) {
          if (n == d) {
            primes[i] = n;
            goto nexti;
          }
          if (n % d == 0) {
            break;
          }
        }
      }
      nexti:
      i++;
    }
  }
}

/***************************************************************************//**
 * Helper function to call related function which enters EM0 Active Mode.
 ******************************************************************************/
static void em_EM0(energy_mode_t *mode)
{
  switch ((em01_oscillator_enum_t)mode->osc) {
    case HFXO_:
      em_EM0_Hfxo();
      break;
    case FSRCO_20MHZ:
      em_EM0_Fsrco();
      break;
    case HFRCO_80MHZ:
      em_EM0_Hfrco(cmuHFRCODPLLFreq_80M0Hz);
      break;
    case HFRCO_38MHZ:
      em_EM0_Hfrco(cmuHFRCODPLLFreq_38M0Hz);
      break;
    case HFRCO_26MHZ:
      em_EM0_Hfrco(cmuHFRCODPLLFreq_26M0Hz);
      break;
    case HFRCO_1MHZ:
      em_EM0_Hfrco(cmuHFRCODPLLFreq_1M0Hz);
      break;
    default:
      EFM_ASSERT(false);
      break;
  }
  slx_power_manager_update_clock_info();
  switch (mode->op) {
    case WHILE:
      while (1) {
      }
    // no break
    case PRIME:
      prime_calc();
      break;
    case COREMARK:
      while (1) {
        CoreMark_Main();
      }
    // no break
    default:
      EFM_ASSERT(false);
      break;
  }
}

/***************************************************************************//**
 * Helper function to call related function which enters EM1 Sleep Mode.
 ******************************************************************************/
static void em_EM1(energy_mode_t *mode)
{
  switch ((em01_oscillator_enum_t)mode->osc) {
    case HFXO_:
      em_EM1_Hfxo();
      break;
    case FSRCO_20MHZ:
      em_EM1_Fsrco();
      break;
    case HFRCO_80MHZ:
      em_EM1_Hfrco(cmuHFRCODPLLFreq_80M0Hz);
      break;
    case HFRCO_38MHZ:
      em_EM1_Hfrco(cmuHFRCODPLLFreq_38M0Hz);
      break;
    case HFRCO_26MHZ:
      em_EM1_Hfrco(cmuHFRCODPLLFreq_26M0Hz);
      break;
    case HFRCO_1MHZ:
      em_EM1_Hfrco(cmuHFRCODPLLFreq_1M0Hz);
      break;
    default:
      EFM_ASSERT(false);
      break;
  }
  slx_power_manager_update_clock_info();
}

/***************************************************************************//**
 * Helper function to call related function which enters EM2 Deep Sleep Mode.
 ******************************************************************************/
static void em_EM2(energy_mode_t *mode)
{
  switch ((em2_oscillator_enum_t)mode->osc) {
#if defined(RTCC_PRESENT)
    case EM2_LFXO_RTCC:
      // Full RAM
      em_EM2_RTCC(cmuSelect_LFXO, false);   // disable RAM powerdown
      break;
    case EM2_LFXO_RTCC_RAM_POWERDOWN:
      // 16kB RAM
      em_EM2_RTCC(cmuSelect_LFXO, true);    // enable RAM powerdown
      break;
    case EM2_LFRCO_RTCC:
      // Full RAM
      em_EM2_RTCC(cmuSelect_LFRCO, false);  // disable RAM powerdown
      break;
    case EM2_LFRCO_RTCC_RAM_POWERDOWN:
      // 16kB RAM
      em_EM2_RTCC(cmuSelect_LFRCO, true);   // enable RAM powerdown
      break;
#endif // defined(RTCC_PRESENT)
#if defined(SYSRTC_PRESENT)
    case EM2_LFRCO_SYSRTC:
      em_EM2_LfrcoSYSRTC(false);            // disable RAM powerdown
      break;
    case EM2_LFRCO_SYSRTC_RAM_POWERDOWN:
      em_EM2_LfrcoSYSRTC(true);             // enable RAM powerdown
      break;
#if !(defined(ZGM230SB27HGN) && ZGM230SB27HGN == 1)
    case EM2_LFXO_SYSRTC:
      em_EM2_LfxoSYSRTC(false);             // disable RAM powerdown
      break;
    case EM2_LFXO_SYSRTC_RAM_POWERDOWN:
      em_EM2_LfxoSYSRTC(true);              // enable RAM powerdown
      break;
#endif // !(defined(ZGM230SB27HGN) && ZGM230SB27HGN == 1)
#endif // defined(SYSRTC_PRESENT)
    default:
      EFM_ASSERT(false);
      break;
  }
  slx_power_manager_update_clock_info();
}

/***************************************************************************//**
 * Helper function to call related function which enters EM3 Stop Mode.
 ******************************************************************************/
static void em_EM3(energy_mode_t *mode)
{
  switch ((em3_oscillator_enum_t)mode->osc) {
    case EM3_ULFRCO:
      // Allow sleep - sl_power_manager_sleep() is called in main loop
      ok_to_sleep = true;
      isr_ok_to_sleep = SL_POWER_MANAGER_SLEEP;
      break;
    case EM3_ULFRCO_RAM_POWERDOWN:
      sl_hal_emu_ram_power_down(SRAM_BASE, 0); // Power down all RAM blocks except block 1
      // Allow sleep - sl_power_manager_sleep() is called in main loop
      ok_to_sleep = true;
      isr_ok_to_sleep = SL_POWER_MANAGER_SLEEP;
      break;
    case EM3_ULFRCO_BURTC:
      em_EM3_UlfrcoBURTC(false);            // disable RAM powerdown
      break;
    case EM3_ULFRCO_BURTC_RAM_POWERDOWN:
      em_EM3_UlfrcoBURTC(true);             // enable RAM powerdown
      break;
    default:
      EFM_ASSERT(false);
      break;
  }
}

/***************************************************************************//**
 * Helper function to call related function which enters EM4H Hibernate Mode.
 ******************************************************************************/
static void em_EM4(energy_mode_t *mode)
{
  // Check if the device has Boost DC-DC parts at runtime
  if (_SILICON_LABS_DCDC_FEATURE == _SILICON_LABS_DCDC_FEATURE_DCDC_BOOST) {
    //  DCDC Boost devices will not enter EM4 mode.
    return;
  }

  switch ((em4h_oscillator_enum_t)mode->osc) {
    case NONE:
      // 128b RAM
      em_EM4_none();
      break;
    case EM4_LFRCO_BURTC:
      em_EM4_LfrcoBURTC();
      break;
    case EM4_ULFRCO_BURTC:
      em_EM4_UlfrcoBURTC();
      break;
    default:
      EFM_ASSERT(false);
      break;
  }
}

/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/

/***************************************************************************//**
 * Hook for power manager - indicates if application can sleep.
 ******************************************************************************/
bool app_is_ok_to_sleep(void)
{
  return ok_to_sleep;
}

/***************************************************************************//**
 * Hook for power manager - indicates if application should return to sleep
 * after an interrupt.
 ******************************************************************************/
sl_power_manager_on_isr_exit_t app_sleep_on_isr_exit(void)
{
  return isr_ok_to_sleep;
}

/***************************************************************************//**
 * Hook for power manager - called before entering EM4.
 * This overrides the weak implementation in sl_power_manager.
 * Clears GPIO EM4 wakeup interrupts to prevent immediate wake.
 ******************************************************************************/
void sl_power_manager_em4_presleep_hook(void)
{
#if defined(_GPIO_IF_EM4WU_MASK)
  // Check if GPIO clock is enabled before accessing GPIO registers
#if defined(_CMU_CLKEN0_GPIO_SHIFT)
  if (CMU->CLKEN0 & CMU_CLKEN0_GPIO) {
#endif
    // Clear all EM4 wakeup interrupts before entering EM4
    // This prevents immediate wake from pending GPIO interrupts
    sl_hal_gpio_clear_interrupts(_GPIO_IF_EM4WU_MASK);
#if defined(_CMU_CLKEN0_GPIO_SHIFT)
  }
#endif
#endif
}

/***************************************************************************//**
 * Function to start the Emode test.
 ******************************************************************************/
void start_emode_test(energy_mode_t *mode)
{
#if defined(DCDC_PRESENT)
  if (!mode->dcdc) {
    CMU_ClockEnable(cmuClock_DCDC, true);
    sl_status_t status = sl_hal_emu_set_dcdc_mode(SL_HAL_EMU_DCDC_MODE_BYPASS);
    EFM_ASSERT(status == SL_STATUS_OK);
  }
#if defined(_EMU_DCDCLPEM01CFG_MASK)
  else if (mode->em == 1) {
    CMU_ClockEnable(cmuClock_DCDC, true);
    sl_status_t status = sl_hal_emu_set_dcdc_mode(SL_HAL_EMU_DCDC_MODE_LOWPOWER);
    EFM_ASSERT(status == SL_STATUS_OK);
  }
#endif
#endif
  switch (mode->em) {
    case EM0:
      em_EM0(mode);
      break;
    case EM1:
      em_EM1(mode);
      break;
    case EM2:
      em_EM2(mode);
      break;
    case EM3:
      em_EM3(mode);
      break;
    case EM4:
      em_EM4(mode);
      break;
    default:
      EFM_ASSERT(false);
      break;
  }
}

