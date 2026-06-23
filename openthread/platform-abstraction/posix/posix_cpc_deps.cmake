#
#  Shared CPC dependency logic. Ensures the cpc target exists.
#  Used by posix_vendor_rcp.cmake (OpenThread) and cpc-spinel-proxy.
#
#  Set CPCD_SOURCE_DIR before including, or pass -DCPCD_SOURCE_DIR=/path.
#
#  # License
#  <b>Copyright 2026 Silicon Laboratories Inc. www.silabs.com</b>
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

set(CPCD_SOURCE_DIR "" CACHE PATH "path to directory containing cpcd CMakeLists.txt")

set(CPC_LIB_TARGET "cpc")

if(NOT TARGET cpc)
    if(CPCD_SOURCE_DIR)
        option(BUILD_SHARED_LIBS "Build shared libraries" OFF)
        add_subdirectory(${CPCD_SOURCE_DIR} ${CMAKE_BINARY_DIR}/cpc-daemon EXCLUDE_FROM_ALL)
    else()
        list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR})
        find_package(cpc REQUIRED)
        set(CPC_LIB_TARGET "cpc::cpc")
    endif()
endif()
