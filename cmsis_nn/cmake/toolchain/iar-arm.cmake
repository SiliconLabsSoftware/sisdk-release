set(CMAKE_SYSTEM_NAME                   Generic)
set(CMAKE_SYSTEM_PROCESSOR              arm)
set(CMAKE_TRY_COMPILE_TARGET_TYPE       STATIC_LIBRARY)

if(WIN32)
    set(EXE_SUFFIX ".exe")
else()
    set(EXE_SUFFIX "")
endif()

set(CMAKE_C_COMPILER    $ENV{SLED_TOOL_IAR_ARM_PATH}iccarm${EXE_SUFFIX})
set(CMAKE_CXX_COMPILER  $ENV{SLED_TOOL_IAR_ARM_PATH}iccarm${EXE_SUFFIX} --c++)
set(CMAKE_ASM_COMPILER  $ENV{SLED_TOOL_IAR_ARM_PATH}iasmarm${EXE_SUFFIX})
set(CMAKE_LINKER        $ENV{SLED_TOOL_IAR_ARM_PATH}ilinkarm${EXE_SUFFIX})
set(CMAKE_AR            $ENV{SLED_TOOL_IAR_ARM_PATH}iarchive${EXE_SUFFIX})
set(CMAKE_SIZE_UTIL     $ENV{SLED_TOOL_IAR_ARM_PATH}ielftool${EXE_SUFFIX})
set(CMAKE_STRIP         $ENV{SLED_TOOL_IAR_ARM_PATH}ielftool${EXE_SUFFIX})
set(CMAKE_OBJCOPY       $ENV{SLED_TOOL_IAR_ARM_PATH}ielftool${EXE_SUFFIX})
set(CMAKE_OBJDUMP       $ENV{SLED_TOOL_IAR_ARM_PATH}ielftool${EXE_SUFFIX})

set(CMAKE_C_STANDARD_REQUIRED   ON)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS          ON) # IAR needs C extensions to be more similar to GCC
set(CMAKE_CXX_EXTENSIONS        ON) # IAR needs C++ extensions to be more similar to GCC

if(DEFINED ENV{SLED_TOOL_IAR_ARM_CSTAT_CHECKS})
    message(STATUS "CSTAT is enabled. Compiler will not produce object files.")

    if (NOT DEFINED ENV{SLED_TOOL_IAR_ARM_CSTAT_DB})
        message(SEND_ERROR "Environment variable SLED_TOOL_IAR_ARM_CSTAT_DB must be set to the absolute location of the CSTAT database file.")
    endif()

    # Configure icstat as a compiler launcher
    set(CMAKE_C_COMPILER_LAUNCHER   $ENV{SLED_TOOL_IAR_ARM_PATH}icstat${EXE_SUFFIX} "--db" $ENV{SLED_TOOL_IAR_ARM_CSTAT_DB} "--checks" $ENV{SLED_TOOL_IAR_ARM_CSTAT_CHECKS} "analyze" "--")
    set(CMAKE_CXX_COMPILER_LAUNCHER $ENV{SLED_TOOL_IAR_ARM_PATH}icstat${EXE_SUFFIX} "--db" $ENV{SLED_TOOL_IAR_ARM_CSTAT_DB} "--checks" $ENV{SLED_TOOL_IAR_ARM_CSTAT_CHECKS} "analyze" "--")

    # Don't interrogate compiler to find supported features, since CSTAT doesn't actually compile the feature test code
    set(CMAKE_C_COMPILER_FORCED     TRUE)
    set(CMAKE_CXX_COMPILER_FORCED   TRUE)

    # Set archive tool to the `true` command to prevent errors when trying to link nonexistant objects
    # This is a horrible hack.
    set(CMAKE_AR                    "true")
endif()

if(SLED_VARIANT_MODE STREQUAL "core")
    if(SLED_VARIANT STREQUAL "cortex-m0plus")
        set(CPU_FLAGS "--cpu CORTEX-M0+ --cpu_mode thumb --endian little")
        set(FPU_FLAGS "")
    elseif(SLED_VARIANT STREQUAL "cortex-m3")
        set(CPU_FLAGS "--cpu CORTEX-M3 --cpu_mode thumb --endian little")
        set(FPU_FLAGS "")
    elseif(SLED_VARIANT STREQUAL "cortex-m4")
        set(CPU_FLAGS "--cpu CORTEX-M4F --cpu_mode thumb --endian little")
        set(FPU_FLAGS "--fpu=VFPv4_sp")
    elseif(SLED_VARIANT STREQUAL "cortex-m33")
        set(CPU_FLAGS "--cpu CORTEX-M33 --cpu_mode thumb --endian little")
        set(FPU_FLAGS "--fpu=VFPv5_sp")
    elseif(SLED_VARIANT STREQUAL "cortex-m55")
        set(CPU_FLAGS "--cpu CORTEX-M55 --cpu_mode thumb --endian little")
        set(FPU_FLAGS "--fpu=VFPv5_sp")
    endif()
elseif(SLED_VARIANT_MODE STREQUAL "architecture")
# TODO
endif()

set(CMAKE_C_FLAGS_INIT                  "${CPU_FLAGS} ${FPU_FLAGS} --no_path_in_file_macros")
set(CMAKE_CXX_FLAGS_INIT                "${CMAKE_C_FLAGS_INIT}")
set(CMAKE_ASM_FLAGS_INIT                "${CPU_FLAGS} ${FPU_FLAGS} -x assembler-with-cpp")
set(CMAKE_EXE_LINKER_FLAGS_INIT         "${CPU_FLAGS} ${FPU_FLAGS}")
set(CMAKE_STATIC_LINKER_FLAGS_INIT      "--create")

# Pe193: zero used for undefined preprocessing identifier
# Pa050: non-native end of line sequence detected
set(SLED_DEFAULT_WARNINGS "--warnings_are_errors --diag_suppress=Pe193 --diag_suppress=Pa050")

set(CMAKE_C_FLAGS_DEBUG                 "-Ol --debug ${SLED_DEFAULT_WARNINGS}" CACHE STRING "")
set(CMAKE_C_FLAGS_RELEASE               "-Ohz -DNDEBUG ${SLED_DEFAULT_WARNINGS}" CACHE STRING "")
set(CMAKE_C_FLAGS_RELWITHDEBINFO        "-Ohz --debug -DNDEBUG ${SLED_DEFAULT_WARNINGS}" CACHE STRING "")
set(CMAKE_CXX_FLAGS_DEBUG               "-Ol --debug ${SLED_DEFAULT_WARNINGS}" CACHE STRING "")
set(CMAKE_CXX_FLAGS_RELEASE             "-Ohz -DNDEBUG ${SLED_DEFAULT_WARNINGS}" CACHE STRING "")
set(CMAKE_CXX_FLAGS_RELWITHDEBINFO      "-Ohz --debug -DNDEBUG ${SLED_DEFAULT_WARNINGS}" CACHE STRING "")


set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM   NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY   ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE   ONLY)
