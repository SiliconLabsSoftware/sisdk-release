##################################################################
# Silicon Labs CMake utilities for Embedded Software Development #
##################################################################

# sled_target_set_slc_component_metadata
#   Generate a YAML file containing SLC component metadata for the target.
#   SLC conditions to apply to the target are passed as extra arguments.
#   Generator expressions may be used to apply conditions selectively to specific build configurations.
#
#   Arguments:
#     target_name   -- Name of the target
#     EXPORT        -- Whether this target/configuration should be exported.
#     COMPONENT     -- ID of SLC component to export this target/configuration to, if EXPORT is truthy.
#     INSTALL_DIR   -- If set, the SLC component uses this directory instead of the build directory.
#     INSTALL       -- If true or if INSTALL_DIR is set, the target needs to be installed after building.
#     CONDITION     -- List of conditions to apply to the target.
#     UNLESS        -- List of negative conditions to apply to the target.
#     GCC_CONDITION -- Conditions only applied if the toolchain is GCC
#     GCC_UNLESS    -- Negative conditions only applied if the toolchain is GCC
#     IAR_CONDITION -- Conditions only applied if the toolchain is IAR
#     IAR_UNLESS    -- Negative conditions only applied if the toolchain is IAR
#     LLVM_CONDITION -- Conditions only applied if the toolchain is LLVM
#     LLVM_UNLESS    -- Negative conditions only applied if the toolchain is LLVM
function(sled_target_set_slc_component_metadata target_name)
  cmake_parse_arguments(PARSE_ARGV 0 "target" "" "COMPONENT;EXPORT;INSTALL_DIR;INSTALL" "CONDITION;UNLESS;GCC_CONDITION;GCC_UNLESS;IAR_CONDITION;IAR_UNLESS;LLVM_CONDITION;LLVM_UNLESS")

  list(APPEND content "path: $<PATH:RELATIVE_PATH,$<TARGET_FILE:${target_name}>,${CMAKE_BINARY_DIR}>")
  if(DEFINED target_INSTALL_DIR)
    list(APPEND content "install_path: $<PATH:RELATIVE_PATH,${CMAKE_INSTALL_PREFIX}/${target_INSTALL_DIR}/$<TARGET_FILE_NAME:${target_name}>,${CMAKE_BINARY_DIR}>")
  endif()

  if(target_INSTALL OR DEFINED target_INSTALL_DIR)
    list(APPEND content "require_install: true")
  endif()

  if(DEFINED target_COMPONENT AND DEFINED target_EXPORT)
    list(APPEND content "target: ${target_name}")
    list(APPEND content "configuration: $<CONFIG>")
    list(APPEND content "component: ${target_COMPONENT}")

    get_target_property(link_libs ${target_name} LINK_LIBRARIES)
    list(APPEND content "dependencies: [$<JOIN:$<FILTER:${link_libs},INCLUDE,^slc::>,$<COMMA> >]")

    list(APPEND content "export: $<IF:$<BOOL:${target_EXPORT}>,true,false>")
  endif()

  set(conditions)

  _sled_get_slc_toolchain_condition(toolchain_condition)
  list(APPEND conditions ${toolchain_condition})

  _sled_get_slc_variant_condition(variant_condition)
  list(APPEND conditions ${variant_condition})

  if(target_CONDITION)
    list(APPEND conditions ${target_CONDITION})
  endif()
  if(target_IAR_CONDITION AND CMAKE_C_COMPILER_ID MATCHES IAR)
    list(APPEND conditions ${target_IAR_CONDITION})
  endif()
  if(target_GCC_CONDITION AND CMAKE_C_COMPILER_ID MATCHES GNU)
    list(APPEND conditions ${target_GCC_CONDITION})
  endif()
  if(target_LLVM_CONDITION AND CMAKE_C_COMPILER_ID MATCHES Clang)
    list(APPEND conditions ${target_LLVM_CONDITION})
  endif()
  if(conditions)
    list(APPEND content "condition: [$<JOIN:$<FILTER:${conditions},EXCLUDE,^$>,$<COMMA> >]")
  endif()

  set(unless)
  if(target_UNLESS)
    list(APPEND unless ${target_UNLESS})
  endif()
  if(target_IAR_UNLESS AND CMAKE_C_COMPILER_ID MATCHES IAR)
    list(APPEND unless ${target_IAR_UNLESS})
  endif()
  if(target_GCC_UNLESS AND CMAKE_C_COMPILER_ID MATCHES GNU)
    list(APPEND unless ${target_GCC_UNLESS})
  endif()
  if(target_LLVM_UNLESS AND CMAKE_C_COMPILER_ID MATCHES Clang)
    list(APPEND unless ${target_LLVM_UNLESS})
  endif()
  if(unless)
    list(APPEND content "unless: [$<JOIN:$<FILTER:${unless},EXCLUDE,^$>,$<COMMA> >]")
endif()

  list(JOIN content "\n" content)
  file(GENERATE OUTPUT "$<CONFIG>/${target_name}.yaml"
    CONTENT "${content}"
  )
endfunction()

##############################
### Internal utility functions
##############################

# _sled_get_slc_toolchain_condition
#   Return the SLC toolchain condition corresponding to the current toolchain in
#   the variable given as an argument.
function(_sled_get_slc_toolchain_condition condition)
  if(CMAKE_C_COMPILER_ID MATCHES GNU OR CMAKE_C_COMPILER_ID MATCHES AppleClang )
    set(${condition} toolchain_gcc PARENT_SCOPE)
  elseif(CMAKE_C_COMPILER_ID MATCHES "Clang")
    set(${condition} toolchain_llvm PARENT_SCOPE)
  endif()
  if(CMAKE_C_COMPILER_ID MATCHES IAR)
    set(${condition} toolchain_iar PARENT_SCOPE)
  endif()
endfunction()

# _sled_get_slc_variant_condition
#   Return the SLC device condition corresponding to the current
#   SLED variant in the variable given as an argument.
function(_sled_get_slc_variant_condition condition)
  if(DEFINED SLC_VARIANT_CONDITION)
    set(${condition} ${SLC_VARIANT_CONDITION} PARENT_SCOPE)
  elseif(SLED_VARIANT_MODE STREQUAL "core")
    if(SLED_VARIANT STREQUAL "native")
      set(${condition} native PARENT_SCOPE)
    elseif(SLED_VARIANT STREQUAL "cortex-m0plus")
      set(${condition} cortexm0plus PARENT_SCOPE)
    elseif(SLED_VARIANT STREQUAL "cortex-m3")
      set(${condition} cortexm3 PARENT_SCOPE)
    elseif(SLED_VARIANT STREQUAL "cortex-m4")
      set(${condition} cortexm4 PARENT_SCOPE)
    elseif(SLED_VARIANT STREQUAL "cortex-m33")
      set(${condition} cortexm33 PARENT_SCOPE)
    elseif(SLED_VARIANT STREQUAL "cortex-m55")
      set(${condition} cortexm55 PARENT_SCOPE)
    else()
      set(${condition} ${SLED_VARIANT} PARENT_SCOPE)
    endif()
  endif()
endfunction()
