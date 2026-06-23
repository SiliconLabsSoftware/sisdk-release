/***************************************************************************//**
 * @file
 * @brief This file contains deprecated aliases for CMSIS6 definitions after
 *        migration from CMSIS5.
 *******************************************************************************
 * # License
 * <b>Copyright 2025 Silicon Laboratories Inc. www.silabs.com</b>
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

#ifndef SLI_CMSIS_DEPRECATED_ALIASES_H
#define SLI_CMSIS_DEPRECATED_ALIASES_H

/* DCB/CoreDebug are not in M0/M0+/M1/SC000 headers (DAP-only); omitting avoids
 * undefined DCB_DEMCR_TRCENA_Msk and guards against undefined behavior. */
#if !(defined(__CORE_CM0_H_GENERIC)       \
    || defined(__CORE_CM0PLUS_H_GENERIC) \
    || defined(__CORE_CM1_H_GENERIC)     \
    || defined(__CORE_SC000_H_GENERIC))
#define CoreDebug_DEMCR_TRCENA_Msk      DCB_DEMCR_TRCENA_Msk
#endif

/* ITM Stimulus Port Register Definitions. */
#define ITM_TCR_TraceBusID_Pos          ITM_TCR_TRACEBUSID_Pos
#define ITM_TCR_TraceBusID_Msk          ITM_TCR_TRACEBUSID_Msk
#define ITM_TCR_TSPrescale_Pos          ITM_TCR_TSPRESCALE_Pos
#define ITM_TCR_TSPrescale_Msk          ITM_TCR_TSPRESCALE_Msk

#define ITM_LSR_ByteAcc_Pos             ITM_LSR_BYTEACC_Pos
#define ITM_LSR_ByteAcc_Msk             ITM_LSR_BYTEACC_Msk
#define ITM_LSR_Access_Pos              ITM_LSR_ACCESS_Pos
#define ITM_LSR_Access_Msk              ITM_LSR_ACCESS_Msk
#define ITM_LSR_Present_Pos             ITM_LSR_PRESENT_Pos
#define ITM_LSR_Present_Msk             ITM_LSR_PRESENT_Msk

/* CMSIS_TPI Alias Definitions */
#define TPI TPIU

#define TPI_ACPR_PRESCALER_Pos             TPIU_ACPR_PRESCALER_Pos                     
#define TPI_ACPR_PRESCALER_Msk             TPIU_ACPR_PRESCALER_Msk

#define TPI_SPPR_TXMODE_Pos                TPIU_SPPR_TXMODE_Pos
#define TPI_SPPR_TXMODE_Msk                TPIU_SPPR_TXMODE_Msk

#define TPI_FFSR_FtNonStop_Pos             TPIU_FFSR_FtNonStop_Pos
#define TPI_FFSR_FtNonStop_Msk             TPIU_FFSR_FtNonStop_Msk

#define TPI_FFSR_TCPresent_Pos             TPIU_FFSR_TCPresent_Pos
#define TPI_FFSR_TCPresent_Msk             TPIU_FFSR_TCPresent_Msk

#define TPI_FFSR_FtStopped_Pos             TPIU_FFSR_FtStopped_Pos
#define TPI_FFSR_FtStopped_Msk             TPIU_FFSR_FtStopped_Msk

#define TPI_FFSR_FlInProg_Pos              TPIU_FFSR_FlInProg_Pos
#define TPI_FFSR_FlInProg_Msk              TPIU_FFSR_FlInProg_Msk

#define TPI_FFCR_TrigIn_Pos                TPIU_FFCR_TrigIn_Pos
#define TPI_FFCR_TrigIn_Msk                TPIU_FFCR_TrigIn_Msk

#define TPI_FFCR_FOnMan_Pos                TPIU_FFCR_FOnMan_Pos
#define TPI_FFCR_FOnMan_Msk                TPIU_FFCR_FOnMan_Msk

#define TPI_FFCR_EnFCont_Pos               TPIU_FFCR_EnFCont_Pos
#define TPI_FFCR_EnFCont_Msk               TPIU_FFCR_EnFCont_Msk

#define TPI_TRIGGER_TRIGGER_Pos            TPIU_TRIGGER_TRIGGER_Pos
#define TPI_TRIGGER_TRIGGER_Msk            TPIU_TRIGGER_TRIGGER_Msk

#define TPI_ITFTTD0_ATB_IF2_ATVALID_Pos    TPIU_ITFTTD0_ATB_IF2_ATVALID_Pos
#define TPI_ITFTTD0_ATB_IF2_ATVALID_Msk    TPIU_ITFTTD0_ATB_IF2_ATVALID_Msk

#define TPI_ITFTTD0_ATB_IF2_bytecount_Pos  TPIU_ITFTTD0_ATB_IF2_bytecount_Pos
#define TPI_ITFTTD0_ATB_IF2_bytecount_Msk  TPIU_ITFTTD0_ATB_IF2_bytecount_Msk

#define TPI_ITFTTD0_ATB_IF1_ATVALID_Pos    TPIU_ITFTTD0_ATB_IF1_ATVALID_Pos
#define TPI_ITFTTD0_ATB_IF1_ATVALID_Msk    TPIU_ITFTTD0_ATB_IF1_ATVALID_Msk

#define TPI_ITFTTD0_ATB_IF1_bytecount_Pos  TPIU_ITFTTD0_ATB_IF1_bytecount_Pos
#define TPI_ITFTTD0_ATB_IF1_bytecount_Msk  TPIU_ITFTTD0_ATB_IF1_bytecount_Msk

#define TPI_ITFTTD0_ATB_IF1_data2_Pos      TPIU_ITFTTD0_ATB_IF1_data2_Pos
#define TPI_ITFTTD0_ATB_IF1_data2_Msk      TPIU_ITFTTD0_ATB_IF1_data2_Msk

#define TPI_ITFTTD0_ATB_IF1_data1_Pos      TPIU_ITFTTD0_ATB_IF1_data1_Pos
#define TPI_ITFTTD0_ATB_IF1_data1_Msk      TPIU_ITFTTD0_ATB_IF1_data1_Msk

#define TPI_ITFTTD0_ATB_IF1_data0_Pos      TPIU_ITFTTD0_ATB_IF1_data0_Pos
#define TPI_ITFTTD0_ATB_IF1_data0_Msk      TPIU_ITFTTD0_ATB_IF1_data0_Msk

#define TPI_ITATBCTR2_AFVALID2S_Pos        TPIU_ITATBCTR2_AFVALID2S_Pos
#define TPI_ITATBCTR2_AFVALID2S_Msk        TPIU_ITATBCTR2_AFVALID2S_Msk

#define TPI_ITATBCTR2_AFVALID1S_Pos        TPIU_ITATBCTR2_AFVALID1S_Pos
#define TPI_ITATBCTR2_AFVALID1S_Msk        TPIU_ITATBCTR2_AFVALID1S_Msk

#define TPI_ITATBCTR2_ATREADY2S_Pos        TPIU_ITATBCTR2_ATREADY2S_Pos
#define TPI_ITATBCTR2_ATREADY2S_Msk        TPIU_ITATBCTR2_ATREADY2S_Msk

#define TPI_ITATBCTR2_ATREADY1S_Pos        TPIU_ITATBCTR2_ATREADY1S_Pos
#define TPI_ITATBCTR2_ATREADY1S_Msk        TPIU_ITATBCTR2_ATREADY1S_Msk

#define TPI_ITFTTD1_ATB_IF2_ATVALID_Pos    TPIU_ITFTTD1_ATB_IF2_ATVALID_Pos
#define TPI_ITFTTD1_ATB_IF2_ATVALID_Msk    TPIU_ITFTTD1_ATB_IF2_ATVALID_Msk

#define TPI_ITFTTD1_ATB_IF2_bytecount_Pos  TPIU_ITFTTD1_ATB_IF2_bytecount_Pos
#define TPI_ITFTTD1_ATB_IF2_bytecount_Msk  TPIU_ITFTTD1_ATB_IF2_bytecount_Msk

#define TPI_ITFTTD1_ATB_IF1_ATVALID_Pos    TPIU_ITFTTD1_ATB_IF1_ATVALID_Pos
#define TPI_ITFTTD1_ATB_IF1_ATVALID_Msk    TPIU_ITFTTD1_ATB_IF1_ATVALID_Msk

#define TPI_ITFTTD1_ATB_IF1_bytecount_Pos  TPIU_ITFTTD1_ATB_IF1_bytecount_Pos
#define TPI_ITFTTD1_ATB_IF1_bytecount_Msk  TPIU_ITFTTD1_ATB_IF1_bytecount_Msk

#define TPI_ITFTTD1_ATB_IF2_data2_Pos      TPIU_ITFTTD1_ATB_IF2_data2_Pos
#define TPI_ITFTTD1_ATB_IF2_data2_Msk      TPIU_ITFTTD1_ATB_IF2_data2_Msk

#define TPI_ITFTTD1_ATB_IF2_data1_Pos      TPIU_ITFTTD1_ATB_IF2_data1_Pos
#define TPI_ITFTTD1_ATB_IF2_data1_Msk      TPIU_ITFTTD1_ATB_IF2_data1_Msk

#define TPI_ITFTTD1_ATB_IF2_data0_Pos      TPIU_ITFTTD1_ATB_IF2_data0_Pos
#define TPI_ITFTTD1_ATB_IF2_data0_Msk      TPIU_ITFTTD1_ATB_IF2_data0_Msk

#define TPI_ITATBCTR0_AFVALID2S_Pos        TPIU_ITATBCTR0_AFVALID2S_Pos
#define TPI_ITATBCTR0_AFVALID2S_Msk        TPIU_ITATBCTR0_AFVALID2S_Msk

#define TPI_ITATBCTR0_AFVALID1S_Pos        TPIU_ITATBCTR0_AFVALID1S_Pos
#define TPI_ITATBCTR0_AFVALID1S_Msk        TPIU_ITATBCTR0_AFVALID1S_Msk

#define TPI_ITATBCTR0_ATREADY2S_Pos        TPIU_ITATBCTR0_ATREADY2S_Pos
#define TPI_ITATBCTR0_ATREADY2S_Msk        TPIU_ITATBCTR0_ATREADY2S_Msk

#define TPI_ITATBCTR0_ATREADY1S_Pos        TPIU_ITATBCTR0_ATREADY1S_Pos
#define TPI_ITATBCTR0_ATREADY1S_Msk        TPIU_ITATBCTR0_ATREADY1S_Msk

#define TPI_ITCTRL_Mode_Pos                TPIU_ITCTRL_Mode_Pos
#define TPI_ITCTRL_Mode_Msk                TPIU_ITCTRL_Mode_Msk

#define TPI_DEVID_NRZVALID_Pos             TPIU_DEVID_NRZVALID_Pos
#define TPI_DEVID_NRZVALID_Msk             TPIU_DEVID_NRZVALID_Msk

#define TPI_DEVID_MANCVALID_Pos            TPIU_DEVID_MANCVALID_Pos
#define TPI_DEVID_MANCVALID_Msk            TPIU_DEVID_MANCVALID_Msk

#define TPI_DEVID_PTINVALID_Pos            TPIU_DEVID_PTINVALID_Pos
#define TPI_DEVID_PTINVALID_Msk            TPIU_DEVID_PTINVALID_Msk

#define TPI_DEVID_FIFOSZ_Pos               TPIU_DEVID_FIFOSZ_Pos
#define TPI_DEVID_FIFOSZ_Msk               TPIU_DEVID_FIFOSZ_Msk

#define TPI_DEVID_NrTraceInput_Pos         TPIU_DEVID_NrTraceInput_Pos
#define TPI_DEVID_NrTraceInput_Msk         TPIU_DEVID_NrTraceInput_Msk

#define TPI_DEVTYPE_SubType_Pos            TPIU_DEVTYPE_SubType_Pos
#define TPI_DEVTYPE_SubType_Msk            TPIU_DEVTYPE_SubType_Msk

#define TPI_DEVTYPE_MajorType_Pos          TPIU_DEVTYPE_MajorType_Pos
#define TPI_DEVTYPE_MajorType_Msk          TPIU_DEVTYPE_MajorType_Msk

/* FPU Media and VFP Feature Register 0 Alias Definitions */
#define FPU_MVFR0_FP_rounding_modes_Pos      FPU_MVFR0_FPRound_Pos     
#define FPU_MVFR0_FP_rounding_modes_Msk      FPU_MVFR0_FPRound_Msk     
#define FPU_MVFR0_Short_vectors_Pos          FPU_MVFR0_FPShortvec_Pos  
#define FPU_MVFR0_Short_vectors_Msk          FPU_MVFR0_FPShortvec_Msk  
#define FPU_MVFR0_Square_root_Pos            FPU_MVFR0_FPSqrt_Pos      
#define FPU_MVFR0_Square_root_Msk            FPU_MVFR0_FPSqrt_Msk      
#define FPU_MVFR0_Divide_Pos                 FPU_MVFR0_FPDivide_Pos    
#define FPU_MVFR0_Divide_Msk                 FPU_MVFR0_FPDivide_Msk    
#define FPU_MVFR0_FP_excep_trapping_Pos      FPU_MVFR0_FPExceptrap_Pos 
#define FPU_MVFR0_FP_excep_trapping_Msk      FPU_MVFR0_FPExceptrap_Msk 
#define FPU_MVFR0_Double_precision_Pos       FPU_MVFR0_FPDP_Pos        
#define FPU_MVFR0_Double_precision_Msk       FPU_MVFR0_FPDP_Msk        
#define FPU_MVFR0_Single_precision_Pos       FPU_MVFR0_FPSP_Pos        
#define FPU_MVFR0_Single_precision_Msk       FPU_MVFR0_FPSP_Msk        
#define FPU_MVFR0_A_SIMD_registers_Pos       FPU_MVFR0_SIMDReg_Pos     
#define FPU_MVFR0_A_SIMD_registers_Msk       FPU_MVFR0_SIMDReg_Msk     

/* FPU Media and VFP Feature Register 1 Alias Definitions */
#define FPU_MVFR1_FP_fused_MAC_Pos 	         FPU_MVFR1_FMAC_Pos   
#define FPU_MVFR1_FP_fused_MAC_Msk 	         FPU_MVFR1_FMAC_Msk   
#define FPU_MVFR1_FP_HPFP_Pos      	         FPU_MVFR1_FPHP_Pos   
#define FPU_MVFR1_FP_HPFP_Msk      	         FPU_MVFR1_FPHP_Msk   
#define FPU_MVFR1_D_NaN_mode_Pos   	         FPU_MVFR1_FPDNaN_Pos 
#define FPU_MVFR1_D_NaN_mode_Msk   	         FPU_MVFR1_FPDNaN_Msk 
#define FPU_MVFR1_FtZ_mode_Pos     	         FPU_MVFR1_FPFtZ_Pos  
#define FPU_MVFR1_FtZ_mode_Msk     	         FPU_MVFR1_FPFtZ_Msk  

/* FPU Media and VFP Feature Register 2 Alias Definitions */
#define FPU_MVFR2_VFP_Misc_Pos	             FPU_MVFR2_FPMisc_Pos 
#define FPU_MVFR2_VFP_Misc_Msk	             FPU_MVFR2_FPMisc_Msk 

/* NVIC_Type IP -> NVIC_Type IPR */
#if (defined(__CORE_CM0_H_GENERIC)       \
    || defined(__CORE_CM0PLUS_H_GENERIC) \
    || defined(__CORE_CM1_H_GENERIC)     \
    || defined(__CORE_CM3_H_GENERIC)     \
    || defined(__CORE_CM4_H_GENERIC)     \
    || defined(__CORE_CM7_H_GENERIC)     \
    || defined(__CORE_SC000_H_GENERIC)   \
    || defined(__CORE_SC300_H_GENERIC))
#define IP	             IPR 
#endif

/* SCB_Type SHP -> SCB_Type SHPR */
#if (defined(__CORE_CM0_H_GENERIC)       \
    || defined(__CORE_CM0PLUS_H_GENERIC) \
    || defined(__CORE_CM1_H_GENERIC)     \
    || defined(__CORE_CM3_H_GENERIC)     \
    || defined(__CORE_CM4_H_GENERIC)     \
    || defined(__CORE_SC000_H_GENERIC)   \
    || defined(__CORE_SC300_H_GENERIC))
#define SHP	             SHPR
#endif

/* Aliases for cortex M85, M55 and M52*/
#if (defined(__CORE_CM85_H_GENERIC)   \
    || defined(__CORE_CM55_H_GENERIC) \
    || defined(__CORE_CM52_H_GENERIC))

/* Debug Live Access Register (DLAR) and Debug Live Status Register (DLSR) Aliases */
#define DLAR RESERVED0[0]
#define DLSR RESERVED0[1]

/* CMSIS_EWIC Alias Definitions */
#define EWIC_EVENTSPR_EDBGREQ_Pos            EWIC_EWIC_MASKA_EDBGREQ_Pos
#define EWIC_EVENTSPR_EDBGREQ_Msk            EWIC_EWIC_MASKA_EDBGREQ_Msk
#define EWIC_EVENTSPR_NMI_Pos                EWIC_EWIC_MASKA_NMI_Pos                   
#define EWIC_EVENTSPR_NMI_Msk                EWIC_EWIC_MASKA_NMI_Msk

#define EWIC_EVENTSPR_EVENT_Pos              EWIC_EWIC_MASKA_EVENT_Pos                   
#define EWIC_EVENTSPR_EVENT_Msk              EWIC_EWIC_MASKA_EVENT_Msk

#define EWIC_EVENTMASKA_EDBGREQ_Pos          EWIC_EWIC_PENDA_EDBGREQ_Pos          
#define EWIC_EVENTMASKA_EDBGREQ_Msk          EWIC_EWIC_PENDA_EDBGREQ_Msk

#define EWIC_EVENTMASKA_NMI_Pos              EWIC_EWIC_PENDA_NMI_Pos
#define EWIC_EVENTMASKA_NMI_Msk              EWIC_EWIC_PENDA_NMI_Msk

#define EWIC_EVENTMASKA_EVENT_Pos            EWIC_EWIC_PENDA_EVENT_Pos
#define EWIC_EVENTMASKA_EVENT_Msk            EWIC_EWIC_PENDA_EVENT_Msk

#define EWIC_EVENTMASK_IRQ_Pos               EWIC_EWIC_PENDn_IRQ_Pos
#define EWIC_EVENTMASK_IRQ_Msk               EWIC_EWIC_PENDn_IRQ_Msk
#endif

/* Aliasing Lock Access Register (LAR) of Instrumentation Trace Macrocell Register (ITM) */
// In CMSIS6 ITM_Type structure on some cores, LAR and LSR are removed and replaced with a RESERVED6 array.
// By defining these aliases, existing code using LAR and LSR will still compatible with previous code.
#if (!defined(__CORE_CM3_H_GENERIC)     \
    && !defined(__CORE_CM4_H_GENERIC)   \
    && !defined(__CORE_CM52_H_GENERIC)  \
    && !defined(__CORE_CM7_H_GENERIC)   \
    && !defined(__CORE_SC300_H_GENERIC) \
    && !defined(__CORE_STAR_H_GENERIC))
#define LAR RESERVED6[43]   /*!< Offset: 0xFB0 ( /W)  Lock Access Register */
#define LSR RESERVED6[44]   /*!< Offset: 0xFB4 (R/W)  Lock Status Register */
#endif

#endif
