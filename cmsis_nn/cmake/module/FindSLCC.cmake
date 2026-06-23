# find_package for SLC components
#
# Output:
# * Target slc::* -- imported interface target for each requested SLC component
# * Variable SLCC_COMPONENTS -- list of target names for the requested components
#
# Usage:
#   find_package(SLCC MODULE REQUIRED COMPONENTS
#     component_one
#     component_two+condition_x+condition_y
#   )
#   target_link_libraries(<target> ${SLCC_COMPONENTS})
#   # or
#   target_link_libraries(<target> slc::component_one slc::component_two+condition_x+condition_y)

# slcc_create_component_targets
# Create CMake interface targets for a list of SLC component IDs.
# This function does not check if the targets already exist, and will fail if they do.
#
# Arguments:
#   components - list of components to create targets for
function(slcc_create_component_targets components)
    execute_process(
        COMMAND sled --version
        OUTPUT_VARIABLE sled_version_output
        OUTPUT_STRIP_TRAILING_WHITESPACE
        COMMAND_ERROR_IS_FATAL ANY
    )
    string(REPLACE "sled version " "" sled_version "${sled_version_output}")

    if(sled_version VERSION_GREATER_EQUAL "0.9.0")
        cmake_path(GET CMAKE_PARENT_LIST_FILE PARENT_PATH workdir)
    else()
        set(workdir ${CMAKE_CURRENT_LIST_DIR})
    endif()

    # Load SLC metadata for requested components
    execute_process(
        COMMAND sled slc component-to-cmake --components "${components}"
        WORKING_DIRECTORY ${workdir}
        OUTPUT_VARIABLE slcc_data
        OUTPUT_STRIP_TRAILING_WHITESPACE
        COMMAND_ERROR_IS_FATAL ANY
        )

    # Convert multi-line string of CMake lists into nested CMake lists
    string(REGEX REPLACE ";" "\\\\;" slcc_data "${slcc_data}")
    string(REGEX REPLACE "\n" ";" slcc_data "${slcc_data}")

    # Create CMake interface target for each component
    foreach(component_info IN LISTS slcc_data)
        cmake_parse_arguments(component "" "path;id" "includes;defines;provides;config_files;sources" ${component_info})

        add_library(slc::${component_id} INTERFACE IMPORTED)
        set_target_properties(slc::${component_id} PROPERTIES
            INTERFACE_INCLUDE_DIRECTORIES "${component_includes}"
            INTERFACE_COMPILE_DEFINITIONS "${component_defines}"
            LABELS "${component_provides}"
            # Imported targets should not use -isystem, but -I instead
            # While exposing all consumers to compiler warnings from their dependencies is noisy,
            # it's the best way to ensure that warnings propagate far enough to be caught and fixed.
            SYSTEM FALSE
        )
        if(DEFINED component_config_files)
          set_target_properties(slc::${component_id} PROPERTIES
            CONFIG_FILES "${component_config_files}"
          )
        endif()
        if(DEFINED component_sources)
          set_target_properties(slc::${component_id} PROPERTIES
            SLC_SOURCES "${component_sources}"
          )
        endif()

        # Register .slcc file as a prereq for the target
        # Hack: This should ideally be done with the directory property CMAKE_CONFIGURE_DEPENDS,
        # but that doesn't appear to work from within find_package, so we create a fake configure file instead
        STRING(REPLACE "+" "." component_id "${component_id}")
        configure_file(${component_path} "${CMAKE_CURRENT_BINARY_DIR}/slc/${component_id}.stamp" COPYONLY)
    endforeach()
endfunction()

# slcc_find_components
# Find a list of SLC components by ID, create CMake interface targets from them if they
# don't already exist, and set the variable SLCC_COMPONENTS in the parent scope containing
# the list of targets.
#
# Arguments:
#   requested_components - list of components to find
function(slcc_find_components requested_components)
    set(component_targets "")
    set(missing_component_targets "")
    foreach(component IN LISTS requested_components)
        if(TARGET slc::${component})
            set(SLCC_${component}_FOUND TRUE PARENT_SCOPE)
            list(APPEND component_targets "slc::${component}")
        else()
            set(SLCC_${component}_FOUND FALSE PARENT_SCOPE)
            list(APPEND missing_component_targets "${component}")
        endif()
    endforeach()

    if(missing_component_targets)
        slcc_create_component_targets("${missing_component_targets}")
    endif()

    foreach(component IN LISTS missing_component_targets)
        if(TARGET slc::${component})
            set(SLCC_${component}_FOUND TRUE PARENT_SCOPE)
            list(APPEND component_targets "slc::${component}")
        endif()
    endforeach()

    # Export list of targets to caller
    set(SLCC_COMPONENTS "${component_targets}" PARENT_SCOPE)
endfunction()

# Find requested components
slcc_find_components("${SLCC_FIND_COMPONENTS}")

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(SLCC HANDLE_COMPONENTS)
