/***************************************************************************//**
 * @file btl_glitch_mitigation.h
 * @brief Bootloader glitch mitigation functionality
 *******************************************************************************
 * # License
 * <b>Copyright 2025 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * The licensor of this software is Silicon Laboratories Inc.  Your use of this
 * software is governed by the terms of Silicon Labs Master Software License
 * Agreement (MSLA) available at
 * www.silabs.com/about-us/legal/master-software-license-agreement.  This
 * software is distributed to you in Source Code format and is governed by the
 * sections of the MSLA applicable to Source Code.
 *
 ******************************************************************************/
#ifndef BTL_GLITCH_MITIGATION_H
#define BTL_GLITCH_MITIGATION_H

#include <stdint.h>
#include "em_device.h"

#if defined(__ICCARM__)      /* IAR */
  #define BTL_SEC_NORETURN __noreturn
#elif defined(__GNUC__) || defined(__clang__)  /* GCC/Clang/armclang */
  #define BTL_SEC_NORETURN __attribute__((noreturn))
#else
  #define BTL_SEC_NORETURN
#endif

BTL_SEC_NORETURN extern void sys_dead_spin(void);

#define BTL_SEC_VOLATILE volatile

#if defined(__ICCARM__)
  #define BTL_SEC_DIAG_PRAGMA(x) _Pragma(#x)
  #define BTL_SEC_DIAG_SUPPRESS_PE128() BTL_SEC_DIAG_PRAGMA(diag_suppress=Pe128)
  #define BTL_SEC_DIAG_DEFAULT_PE128() BTL_SEC_DIAG_PRAGMA(diag_default=Pe128)
#else
  #define BTL_SEC_DIAG_SUPPRESS_PE128()
  #define BTL_SEC_DIAG_DEFAULT_PE128()
#endif

#if defined(__GNUC__) && !defined(__clang__)
  #define BTL_SEC_DEAD_SPIN() \
  __asm__ __volatile__(       \
    "%=:           \n\t"      \
    "WFI          ;\n\t"      \
    "B   %=b      ;\n\t"      \
    "WFI          ;\n\t"      \
    "B   %=b      ;\n\t"      \
    "WFI          ;\n\t"      \
    "B   %=b      ;\n\t"      \
    : /* outputs: none*/);    \
  __builtin_unreachable();

  #define BTL_SEC_SYS_DEAD_SPIN() \
  do {                            \
    __asm__ __volatile__(         \
      ".extern sys_dead_spin\n\t" \
      "  BL sys_dead_spin ;\n\t"  \
      "  NOP              ;\n\t"  \
      "  NOP              ;\n\t"  \
      "  BL sys_dead_spin ;\n\t"  \
      : /* outputs */);           \
    __builtin_unreachable();      \
  } while (0)

  #define BTL_SEC_ASSERT_EQUAL(op1, op2)                                    \
  do {                                                                      \
    uintptr_t x;                                                            \
    __asm__ __volatile__(                                                   \
      "CMP  %[a], %[b]             \n\t"                                    \
      "NOP                          \n\t"                                   \
      "NOP                          \n\t"                                   \
      "NOP                          \n\t"                                   \
      "CMP  %[a], %[b]             \n\t"                                    \
      "NOP                          \n\t"                                   \
      "NOP                          \n\t"                                   \
      "NOP                          \n\t"                                   \
      "BEQ  1f                     \n\t"   /* equal -> go run XOR check */  \
      /* Fail (or BE glitch fall-through) -> hardened sink */               \
      "BL   sys_dead_spin          \n\t"                                    \
      "NOP                          \n\t"                                   \
      "NOP                          \n\t"                                   \
      "BL   sys_dead_spin          \n\t"                                    \
      "1:                           \n\t"                                   \
      /* -------- Dissimilar check: ONE XOR -------- */                     \
      "EOR  %[x], %[a], %[b]       \n\t"   /* x = a ^ b */                  \
      "CMP  %[x], #0               \n\t"                                    \
      "BEQ  2f                     \n\t"   /* zero => equal confirmed */    \
      /* XOR says NOT equal (or glitch) -> hardened sink */                 \
      "BL   sys_dead_spin          \n\t"                                    \
      "NOP                          \n\t"                                   \
      "NOP                          \n\t"                                   \
      "BL   sys_dead_spin          \n\t"                                    \
      "2:                           \n\t"                                   \
      : /* outputs */[x] "=&r" (x)                                          \
      : /* inputs  */[a] "r" ((uintptr_t)(op1)), [b] "r" ((uintptr_t)(op2)) \
      : /* clobbers */ "cc");                                               \
  } while (0)

/// This macro asserts that two values are not equal and dead_spins if not.
  #define BTL_SEC_ASSERT_NOT_EQUAL(op1, op2)                                     \
  do {                                                                           \
    uintptr_t x;                                                                 \
    __asm__ __volatile__(                                                        \
      /* -------- Double CMP (glitch-resistant, unchanged) -------- */           \
      "CMP  %[a], %[b]             \n\t"                                         \
      "NOP                          \n\t"                                        \
      "NOP                          \n\t"                                        \
      "NOP                          \n\t"                                        \
      "CMP  %[a], %[b]             \n\t"                                         \
      "NOP                          \n\t"                                        \
      "NOP                          \n\t"                                        \
      "NOP                          \n\t"                                        \
      "BNE  1f                     \n\t"   /* not equal -> go run XOR check */   \
      /* Fail (or BNE glitch fall-through) -> hardened sink */                   \
      "BL   sys_dead_spin          \n\t"                                         \
      "NOP                          \n\t"                                        \
      "NOP                          \n\t"                                        \
      "BL   sys_dead_spin          \n\t"                                         \
      "1:                           \n\t"                                        \
      /* -------- Dissimilar check: ONE XOR -------- */                          \
      "EOR  %[x], %[a], %[b]       \n\t"   /* x = a ^ b */                       \
      "CMP  %[x], #0               \n\t"                                         \
      "BNE  2f                     \n\t"   /* non-zero => not equal confirmed */ \
      /* XOR says equal (or glitch) -> hardened sink */                          \
      "BL   sys_dead_spin          \n\t"                                         \
      "NOP                          \n\t"                                        \
      "NOP                          \n\t"                                        \
      "BL   sys_dead_spin          \n\t"                                         \
      "2:                           \n\t"                                        \
      : /* outputs */[x] "=&r" (x)                                               \
      : /* inputs  */[a] "r" ((uintptr_t)(op1)), [b] "r" ((uintptr_t)(op2))      \
      : /* clobbers */ "cc");                                                    \
  } while (0)

#else

#define BTL_SEC_DEAD_SPIN() \
  do {                      \
    for (;; ) { __WFI(); }  \
  } while (0)

#define BTL_SEC_SYS_DEAD_SPIN() \
  do {                          \
    sys_dead_spin();            \
    __NOP(); __NOP();           \
    sys_dead_spin();            \
    for (;; ) { __WFI(); }      \
  } while (0)

/* Equality: require BOTH
 *  (1) two spaced reads that agree on equality, AND
 *  (2) a single XOR (on the second read) that equals zero.
 * Any disagreement => hardened sink.
 */
#undef  BTL_SEC_ASSERT_EQUAL
#define BTL_SEC_ASSERT_EQUAL(op1, op2)                                      \
  do {                                                                      \
    BTL_SEC_DIAG_SUPPRESS_PE128();                                          \
    /* First read */                                                        \
    BTL_SEC_VOLATILE uintptr_t __a1 = (uintptr_t)(op1);                     \
    BTL_SEC_VOLATILE uintptr_t __b1 = (uintptr_t)(op2);                     \
    __NOP(); __NOP(); __NOP();            /* spacing */                     \
    /* Second read */                                                       \
    BTL_SEC_VOLATILE uintptr_t __a2 = (uintptr_t)(op1);                     \
    BTL_SEC_VOLATILE uintptr_t __b2 = (uintptr_t)(op2);                     \
    /* Single XOR check on second read */                                   \
    uintptr_t __xor2 = (uintptr_t)(__a2 ^ __b2);                            \
    if (!((__a1 == __b1) && (__a2 == __b2) && (__xor2 == (uintptr_t)0u))) { \
      BTL_SEC_SYS_DEAD_SPIN();                                              \
    }                                                                       \
    BTL_SEC_DIAG_DEFAULT_PE128();                                           \
  } while (0)

/* Inequality: require BOTH
 *  (1) two spaced reads that agree on inequality, AND
 *  (2) a single XOR (on the second read) that is non-zero.
 * Any disagreement => hardened sink.
 */
#undef  BTL_SEC_ASSERT_NOT_EQUAL
#define BTL_SEC_ASSERT_NOT_EQUAL(op1, op2)                                  \
  do {                                                                      \
    /* First read */                                                        \
    BTL_SEC_VOLATILE uintptr_t __a1 = (uintptr_t)(op1);                     \
    BTL_SEC_VOLATILE uintptr_t __b1 = (uintptr_t)(op2);                     \
    __NOP(); __NOP(); __NOP();            /* spacing */                     \
    /* Second read */                                                       \
    BTL_SEC_VOLATILE uintptr_t __a2 = (uintptr_t)(op1);                     \
    BTL_SEC_VOLATILE uintptr_t __b2 = (uintptr_t)(op2);                     \
    /* Single XOR check on second read */                                   \
    uintptr_t __xor2 = (uintptr_t)(__a2 ^ __b2);                            \
    if (!((__a1 != __b1) && (__a2 != __b2) && (__xor2 != (uintptr_t)0u))) { \
      BTL_SEC_SYS_DEAD_SPIN();                                              \
    }                                                                       \
  } while (0)

#endif
#endif // BTL_GLITCH_MITIGATION_H