#
#  # License
#  <b>Copyright 2024 Silicon Laboratories Inc. www.silabs.com</b>
# 
#  SPDX-License-Identifier: Zlib
# 
#  The licensor of this software is Silicon Laboratories Inc.
# 
#  This software is provided 'as-is', without any express or implied
#  warranty. In no event will the authors be held liable for any damages
#  arising from the use of this software.
# 
#  Permission is granted to anyone to use this software for any purpose,
#  including commercial applications, and to alter it and redistribute it
#  freely, subject to the following restrictions:
# 
#  1. The origin of this software must not be misrepresented; you must not
#     claim that you wrote the original software. If you use this software
#     in a product, an acknowledgment in the product documentation would be
#     appreciated but is not required.
#  2. Altered source versions must be plainly marked as such, and must not be
#     misrepresented as being the original software.
#  3. This notice may not be removed or altered from any source distribution.
#

set(OT_POSIX_CONFIG_RCP_VENDOR_TARGET "cpc-interface")

if (NOT OT_PLATFORM_CONFIG)
    message(WARNING "OT_PLATFORM_CONFIG file which defines OT_VENDOR_RADIO_URL_HELP_BUS missing")
endif()

include(${CMAKE_CURRENT_LIST_DIR}/posix_cpc_deps.cmake)

# `vendor.cmake` creates `rcp-vendor-intf` with `OT_POSIX_CONFIG_RCP_VENDOR_INTERFACE`
# Adding remaining sources here for compatibility with previous configure options.
if(TARGET rcp-vendor-intf)
    target_sources(rcp-vendor-intf PRIVATE "${CMAKE_CURRENT_LIST_DIR}/cpc_transport.cpp")
endif()

add_library(${OT_POSIX_CONFIG_RCP_VENDOR_TARGET} INTERFACE)

# Add cpc header path for OpenThread (when built from CPCD_SOURCE_DIR)
if(CPCD_SOURCE_DIR)
    target_include_directories(${OT_POSIX_CONFIG_RCP_VENDOR_TARGET} INTERFACE ${CPCD_SOURCE_DIR}/lib)
endif()

target_link_libraries(${OT_POSIX_CONFIG_RCP_VENDOR_TARGET} 
    INTERFACE
        ${CPC_LIB_TARGET}
        ot-posix-config
)

target_include_directories(${OT_POSIX_CONFIG_RCP_VENDOR_TARGET}
    INTERFACE
        ${CMAKE_CURRENT_LIST_DIR}
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/src
        ${PROJECT_SOURCE_DIR}/src/core
        ${PROJECT_SOURCE_DIR}/src/posix/platform/
        ${PROJECT_SOURCE_DIR}/src/posix/platform/include
)
