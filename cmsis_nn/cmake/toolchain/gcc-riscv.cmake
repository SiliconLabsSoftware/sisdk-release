set(CMAKE_SYSTEM_NAME                   Generic)
set(CMAKE_SYSTEM_PROCESSOR              riscv)
set(CMAKE_TRY_COMPILE_TARGET_TYPE       STATIC_LIBRARY)

if(WIN32)
    set(EXE_SUFFIX ".exe")
else()
    set(EXE_SUFFIX "")
endif()

# Figure out which RISC-V compiler to use:
#   - If defined, use the SLED_TOOL_GCC_RISCV_TARGET_TRIPLET environment variable.
#   - If compiler not found using define, determine the path using default TARGET_TRIPLET 
#       or via CMake cached variable
#   - If not found using default or cached, search for riscv32-unknown-elf, riscv32-corev-elf,
#       riscv64-unknown-elf, or riscv64-corev-elf in that order.
unset(found_riscv_toolchain)
if(DEFINED ENV{SLED_TOOL_GCC_RISCV_TARGET_TRIPLET})
    find_program(found_riscv_toolchain $ENV{SLED_TOOL_GCC_RISCV_PATH}$ENV{SLED_TOOL_GCC_RISCV_TARGET_TRIPLET}-gcc${EXE_SUFFIX} NO_CACHE)
    if (found_riscv_toolchain)
        set(TARGET_TRIPLET $ENV{SLED_TOOL_GCC_RISCV_TARGET_TRIPLET})
    endif()
endif()
if(NOT found_riscv_toolchain)
    unset(found_riscv_toolchain)
    if (DEFINED TARGET_TRIPLET)
        find_program(found_riscv_toolchain $ENV{SLED_TOOL_GCC_RISCV_PATH}${TARGET_TRIPLET}-gcc${EXE_SUFFIX} NO_CACHE)
    endif()
    if(NOT found_riscv_toolchain)
        set(TARGET_TRIPLET_LIST
            "riscv32-unknown-elf"
            "riscv32-corev-elf"
            "riscv64-unknown-elf"
            "riscv64-corev-elf"
        )
        foreach(TARGET_TRIPLET_NAME ${TARGET_TRIPLET_LIST})
            unset(found_riscv_toolchain)
            find_program(found_riscv_toolchain $ENV{SLED_TOOL_GCC_RISCV_PATH}${TARGET_TRIPLET_NAME}-gcc${EXE_SUFFIX} NO_CACHE)
            if(found_riscv_toolchain)
                set(TARGET_TRIPLET ${TARGET_TRIPLET_NAME})
                break()
            endif()
        endforeach()
        if(NOT found_riscv_toolchain)
            message(FATAL_ERROR "Could not find a valid RISC-V compiler")
        endif()
    endif()
endif()

set(CMAKE_C_COMPILER    $ENV{SLED_TOOL_GCC_RISCV_PATH}${TARGET_TRIPLET}-gcc${EXE_SUFFIX})
set(CMAKE_CXX_COMPILER  $ENV{SLED_TOOL_GCC_RISCV_PATH}${TARGET_TRIPLET}-g++${EXE_SUFFIX})
set(CMAKE_ASM_COMPILER  $ENV{SLED_TOOL_GCC_RISCV_PATH}${TARGET_TRIPLET}-gcc${EXE_SUFFIX})
set(CMAKE_LINKER        $ENV{SLED_TOOL_GCC_RISCV_PATH}${TARGET_TRIPLET}-gcc${EXE_SUFFIX})
set(CMAKE_AR            $ENV{SLED_TOOL_GCC_RISCV_PATH}${TARGET_TRIPLET}-ar${EXE_SUFFIX})
set(CMAKE_SIZE_UTIL     $ENV{SLED_TOOL_GCC_RISCV_PATH}${TARGET_TRIPLET}-size${EXE_SUFFIX})
set(CMAKE_STRIP         $ENV{SLED_TOOL_GCC_RISCV_PATH}${TARGET_TRIPLET}-strip${EXE_SUFFIX})
set(CMAKE_OBJCOPY       $ENV{SLED_TOOL_GCC_RISCV_PATH}${TARGET_TRIPLET}-objcopy${EXE_SUFFIX})
set(CMAKE_OBJDUMP       $ENV{SLED_TOOL_GCC_RISCV_PATH}${TARGET_TRIPLET}-objdump${EXE_SUFFIX})
set(CMAKE_NM_UTIL       $ENV{SLED_TOOL_GCC_RISCV_PATH}${TARGET_TRIPLET}-gcc-nm${EXE_SUFFIX})
set(CMAKE_RANLIB        $ENV{SLED_TOOL_GCC_RISCV_PATH}${TARGET_TRIPLET}-gcc-ranlib${EXE_SUFFIX})
set(CMAKE_GCOV          $ENV{SLED_TOOL_GCC_RISCV_PATH}${TARGET_TRIPLET}-gcov${EXE_SUFFIX})

# Function to get the version from the RISC-V toolchain
function(find_riscv_toolchain_version riscv_version)
    execute_process(
        COMMAND ${CMAKE_C_COMPILER} --version
        OUTPUT_VARIABLE RISCV_VERSION_LOG
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    string(REGEX MATCH "${TARGET_TRIPLET}-gcc \\([^)]+\\) ([^ ]+)" _ ${RISCV_VERSION_LOG})
    set(${riscv_version} ${CMAKE_MATCH_1} PARENT_SCOPE)
endfunction()

if(NOT DEFINED ENV{SLED_TOOL_GCC_RISCV_VERSION})
    # Try deducing the RISC-V toolchain version if the environment variable is not set
    find_riscv_toolchain_version(RISCV_TOOLCHAIN_VERSION)
    # Set SLED_TOOL_GCC_RISCV_VERSION environment variable
    set(ENV{SLED_TOOL_GCC_RISCV_VERSION} ${RISCV_TOOLCHAIN_VERSION})
endif()

set(CMAKE_C_STANDARD_REQUIRED   ON)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS          OFF)

if(SLED_VARIANT_MODE STREQUAL "core")
    if(SLED_VARIANT STREQUAL "cv32e40p")
        set(CPU_FLAGS_COMMON "-march=rv32imc -mabi=ilp32")
        set(CPU_FLAGS_C      "${CPU_FLAGS_COMMON}")
        set(CPU_FLAGS_ASM    "${CPU_FLAGS_COMMON}")
        set(CPU_FLAGS_LINKER "${CPU_FLAGS_COMMON}")

    elseif(SLED_VARIANT MATCHES "cv32e40([sx])(-)(lpw[0-1]|se)")
        # --- Core configuration
        # When adding support for a new instantiation of the CV32E40[SX] core in
        # a subsystem, give it a descriptive name and add it to the
        # configuration lists below.

        # --- Common configurations for E40S and E40X

        # Base ISA can be RV32I or RV32E
        set(_rv32e_variants             "lpw1")

        # Mul extension is optional. Zmmul is multiply-only.
        set(_mul_m_variants             "lpw0" "se")
        set(_mul_zmmul_variants)
        set(_mul_none_variants          "lpw1")

        # Bitmanip extensions are optional. If present, can either include or exclude Zbc
        set(_bitmanip_partial_variants  "lpw0" "lpw1" "se")
        set(_bitmanip_full_variants)

        # --- Configurations for E40X only

        # Atomic extension is optional. Zalrsc is lr.w/sc.w only.
        set(_atomic_zalrsc_variants     "lpw0" "lpw1")
        set(_atomic_full_variants)

        # Zawrs is optional. Wait-on-reservation-set requires basic atomic support.
        set(_zawrs_variants             "lpw0" "lpw1")
        # Zicond is optional. Integer Conditional operations.
        set(_zicond_variants            "lpw0" "lpw1")
        # Zihintpause is optional. Pause hint instruction, with configurable delay in the cpuctrl.timeout MSR.
        # Available without inline assembly using the __builtin_riscv_pause() intrinsic.
        set(_zihintpause_variants       "lpw0" "lpw1")
        # --- End core configuration

        if(CMAKE_MATCH_3 IN_LIST _rv32e_variants)
            set(_arch "rv32e")
            set(_abi  "ilp32e")
        else()
            set(_arch "rv32i")
            set(_abi  "ilp32")
        endif()

        if(CMAKE_MATCH_3 IN_LIST _mul_m_variants)
            set(_arch "${_arch}m")
        endif()
        if(CMAKE_MATCH_3 IN_LIST _mul_zmmul_variants)
            set(_arch "${_arch}m")
            set(_no_div "-mno-div ")
        endif()
        if(CMAKE_MATCH_3 IN_LIST _atomic_full_variants)
            set(_arch "${_arch}a")
        endif()

        set(_arch_extensions "zicsr" "zifencei")
        if("$ENV{SLED_TOOL_GCC_RISCV_VERSION}" VERSION_GREATER_EQUAL "14")
           list(APPEND _arch_extensions "zca" "zcb" "zcmp" "zcmt")
        endif()

        if("$ENV{SLED_TOOL_GCC_RISCV_VERSION}" VERSION_GREATER_EQUAL "13" AND CMAKE_MATCH_3 IN_LIST _zawrs_variants)
            list(APPEND _arch_extensions "zawrs")
        endif()
        if("$ENV{SLED_TOOL_GCC_RISCV_VERSION}" VERSION_GREATER_EQUAL "13" AND CMAKE_MATCH_3 IN_LIST _zicond_variants)
            list(APPEND _arch_extensions "zicond")
        endif()
        if(CMAKE_MATCH_3 IN_LIST _zihintpause_variants)
            list(APPEND _arch_extensions "zihintpause")
        endif()

        if(CMAKE_MATCH_3 IN_LIST _bitmanip_partial_variants)
            list(APPEND _arch_extensions "zba" "zbb" "zbs")
        elseif(CMAKE_MATCH_3 IN_LIST _bitmanip_full_variants)
            list(APPEND _arch_extensions "zba" "zbb" "zbc" "zbs")
        endif()

        # TODO: Zalrsc extension when supported in GCC. No trace of it yet upstream.
        # if("$ENV{SLED_TOOL_GCC_RISCV_VERSION}" VERSION_GREATER_EQUAL "14" AND CMAKE_MATCH_3 IN_LIST _atomic_zalrsc_variants)
        #    list(APPEND _arch_extensions "zalrsc")
        # endif()

        list(JOIN _arch_extensions "_" _arch_extensions)

        set(CPU_FLAGS_COMMON "-march=${_arch}c_${_arch_extensions} -mabi=${_abi}")
        set(CPU_FLAGS_C      "${CPU_FLAGS_COMMON} ${_no_div}")
        set(CPU_FLAGS_ASM    "${CPU_FLAGS_COMMON}")
        set(CPU_FLAGS_LINKER "${CPU_FLAGS_COMMON}")

        unset(_rv32e_variants)
        unset(_mul_m_variants)
        unset(_mul_zmmul_variants)
        unset(_mul_none_variants)
        unset(_bitmanip_partial_variants)
        unset(_bitmanip_full_variants)
        unset(_atomic_zalrsc_variants)
        unset(_atomic_full_variants)
        unset(_zawrs_variants)
        unset(_zicond_variants)
        unset(_zihintpause_variants)
        unset(_arch)
        unset(_arch_extensions)
        unset(_abi)
        unset(_no_div)
    endif()
elseif(SLED_VARIANT_MODE STREQUAL "architecture")
    if(SLED_VARIANT STREQUAL "rv32")
        set(CPU_FLAGS_COMMON "-march=${SLED_VARIANT_ARCH} -mabi=${SLED_VARIANT_ABI}")
        set(CPU_FLAGS_C      "${CPU_FLAGS_COMMON}")
        set(CPU_FLAGS_ASM    "${CPU_FLAGS_COMMON}")
        set(CPU_FLAGS_LINKER "${CPU_FLAGS_COMMON}")
    endif()
endif()

set(CMAKE_C_FLAGS_INIT                  "${CPU_FLAGS_C} -ffunction-sections -fdata-sections -fomit-frame-pointer")
set(CMAKE_CXX_FLAGS_INIT                "${CMAKE_C_FLAGS_INIT} -fno-exceptions -fno-rtti")
set(CMAKE_ASM_FLAGS_INIT                "${CPU_FLAGS_ASM} -x assembler-with-cpp")
set(CMAKE_EXE_LINKER_FLAGS_INIT         "${CPU_FLAGS_LINKER}")
set(CMAKE_STATIC_LINKER_FLAGS_INIT      "")

set(SLED_DEFAULT_WARNINGS "-Wall -Wextra -Werror")

set(CMAKE_C_FLAGS_DEBUG                 "-Og -g ${SLED_DEFAULT_WARNINGS}" CACHE STRING "")
set(CMAKE_C_FLAGS_RELEASE               "-Os -DNDEBUG ${SLED_DEFAULT_WARNINGS}" CACHE STRING "")
set(CMAKE_C_FLAGS_RELWITHDEBINFO        "-Os -g -DNDEBUG ${SLED_DEFAULT_WARNINGS}" CACHE STRING "")
set(CMAKE_CXX_FLAGS_DEBUG               "-Og -g ${SLED_DEFAULT_WARNINGS}" CACHE STRING "")
set(CMAKE_CXX_FLAGS_RELEASE             "-Os -DNDEBUG ${SLED_DEFAULT_WARNINGS}" CACHE STRING "")
set(CMAKE_CXX_FLAGS_RELWITHDEBINFO      "-Os -g -DNDEBUG ${SLED_DEFAULT_WARNINGS}" CACHE STRING "")

#set(CMAKE_C_OUTPUT_EXTENSION            ".o")
#set(CMAKE_CXX_OUTPUT_EXTENSION          ".o")

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM   NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY   ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE   ONLY)
