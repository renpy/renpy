cmake_minimum_required(VERSION 3.21)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C CXX)

# Find required packages
find_package(Python 3.12 EXACT REQUIRED
    COMPONENTS Interpreter Development.Module Development.Embed)
find_package(PkgConfig REQUIRED)
include(UseCython)

# Core libraries
pkg_check_modules(LIBAVFORMAT REQUIRED libavformat)
pkg_check_modules(LIBAVCODEC REQUIRED libavcodec)
pkg_check_modules(LIBAVUTIL REQUIRED libavutil)
pkg_check_modules(LIBSWRESAMPLE REQUIRED libswresample)
pkg_check_modules(LIBSWSCALE REQUIRED libswscale)
pkg_check_modules(HARFBUZZ REQUIRED harfbuzz)
pkg_check_modules(FREETYPE2 REQUIRED freetype2)
pkg_check_modules(FRIBIDI REQUIRED fribidi)
pkg_check_modules(SDL2 REQUIRED sdl2)
pkg_check_modules(ASSIMP REQUIRED assimp)

# Additional libraries
find_library(PNG_LIBRARY png REQUIRED)
find_library(Z_LIBRARY z REQUIRED)

# Platform-specific libraries
if(WIN32)
    find_library(COMDLG32_LIBRARY comdlg32 REQUIRED)
    find_library(OLE32_LIBRARY ole32 REQUIRED)
endif()

# Global settings
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Build configuration
option(RENPY_STATIC "Build static version" OFF)
option(RENPY_COVERAGE "Enable coverage" OFF)
set(CUBISM_SDK_PATH "" CACHE PATH "Path to Cubism SDK")
set(PYGAME_SDL2_HEADERS "" CACHE PATH "Abosulte path to pygame_sdl2/headers (usually it is .venv/.../site-packages/include)")

if(DEFINED ENV{RENPY_STATIC})
    set(RENPY_STATIC ON)
endif()

if(DEFINED ENV{RENPY_COVERAGE})
    set(RENPY_COVERAGE ON)
endif()

if(DEFINED ENV{CUBISM})
    set(CUBISM_SDK_PATH "$ENV{CUBISM}")
endif()

if (DEFINED ENV{PYGAME_SDL2_HEADERS})
    set(PYGAME_SDL2_HEADERS "$ENV{PYGAME_SDL2_HEADERS}")
else()
    message(FATAL_ERROR "PYGAME_SDL2_HEADERS is not defined")
endif()

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/src
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${PYGAME_SDL2_HEADERS}
    ${LIBAVFORMAT_INCLUDE_DIRS}
    ${LIBAVCODEC_INCLUDE_DIRS}
    ${LIBAVUTIL_INCLUDE_DIRS}
    ${LIBSWRESAMPLE_INCLUDE_DIRS}
    ${LIBSWSCALE_INCLUDE_DIRS}
    ${HARFBUZZ_INCLUDE_DIRS}
    ${FREETYPE2_INCLUDE_DIRS}
    ${FRIBIDI_INCLUDE_DIRS}
    ${SDL2_INCLUDE_DIRS}
    ${ASSIMP_INCLUDE_DIRS}
)

# Add Cubism SDK if available
if(CUBISM_SDK_PATH)
    include_directories(${CUBISM_SDK_PATH}/Core/include)
    add_definitions(-DHAVE_CUBISM)
endif()

# Global libraries
set(GLOBAL_LIBRARIES
    ${LIBAVFORMAT_LIBRARIES}
    ${LIBAVCODEC_LIBRARIES}
    ${LIBAVUTIL_LIBRARIES}
    ${LIBSWRESAMPLE_LIBRARIES}
    ${LIBSWSCALE_LIBRARIES}
    ${HARFBUZZ_LIBRARIES}
    ${FREETYPE2_LIBRARIES}
    ${FRIBIDI_LIBRARIES}
    ${SDL2_LIBRARIES}
    ${ASSIMP_LIBRARIES}
    ${PNG_LIBRARY}
    ${Z_LIBRARY}
)

if(WIN32)
    list(APPEND GLOBAL_LIBRARIES ${COMDLG32_LIBRARY} ${OLE32_LIBRARY})
endif()

set(CYTHON_ARGS
    -X embedsignature=True
    -I${CMAKE_CURRENT_SOURCE_DIR}/src
    -I${CMAKE_CURRENT_SOURCE_DIR})

# Function to create Cython extension
function(add_cython_extension name)
    set(options)
    set(oneValueArgs LANGUAGE PYX_FILE INSTALL_DIR)
    set(multiValueArgs SOURCES LIBRARIES COMPILE_ARGS GENERATED_DEPENDENCIES)
    cmake_parse_arguments(ARG "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

    # Set defaults
    if(NOT ARG_LANGUAGE)
        set(ARG_LANGUAGE "C")
    endif()

    # Convert module name to path
    string(REPLACE "." "/" module_path ${name})

    if(ARG_PYX_FILE)
        set(pyx_file ${ARG_PYX_FILE})
    else()
        set(pyx_file ${CMAKE_CURRENT_SOURCE_DIR}/${module_path}.pyx)
        if(NOT EXISTS ${pyx_file})
            set(pyx_file ${CMAKE_CURRENT_SOURCE_DIR}/src/${module_path}.pyx)
        endif()
    endif()

    cython_transpile(${pyx_file} LANGUAGE ${ARG_LANGUAGE} OUTPUT_VARIABLE c_file)

    # Create Python extension
    python_add_library(${name} MODULE ${c_file} ${ARG_SOURCES})

    # Extract the base filename for the extension
    get_filename_component(base_filename ${module_path} NAME)

    # Set properties
    set_target_properties(${name} PROPERTIES
        PREFIX ""
        OUTPUT_NAME ${base_filename}
    )

    # Link libraries
    target_link_libraries(${name} PRIVATE
        ${GLOBAL_LIBRARIES}
        ${ARG_LIBRARIES}
    )

    # Compile flags
    target_compile_options(${name} PRIVATE
        ${GLOBAL_COMPILE_FLAGS}
        ${ARG_COMPILE_ARGS}
    )

    # Generated dependencies
    if(ARG_GENERATED_DEPENDENCIES)
        add_dependencies(${name} ${ARG_GENERATED_DEPENDENCIES})
    endif()

    # Install the extension
    if(ARG_INSTALL_DIR)
        set(install_dir ${ARG_INSTALL_DIR})
    else()
        string(REPLACE "." "/" install_subpath ${name})
        get_filename_component(install_dir ${install_subpath} DIRECTORY)
    endif()
    install(TARGETS ${name} DESTINATION ${install_dir})
endfunction()

# Style files
set(STYLEGEN_BUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}/stylegen")
file(MAKE_DIRECTORY "${STYLEGEN_BUILD_DIR}")
list(APPEND CYTHON_ARGS -I${STYLEGEN_BUILD_DIR})


function(generate_style_file name)
    set(options)
    set(oneValueArgs)
    set(multiValueArgs ARGS)
    cmake_parse_arguments(ARG "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

    set(target_name "generate_${name}_target")
    add_custom_target(${target_name}
        COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate_styles.py
                --output ${STYLEGEN_BUILD_DIR} ${ARG_ARGS}
        COMMAND_EXPAND_LISTS
        BYPRODUCTS "${STYLEGEN_BUILD_DIR}/${name}"
        COMMENT "Generating styles file ${name}"
    )

    set(${name}_TARGET ${target_name} PARENT_SCOPE)
endfunction()

generate_style_file(styleconstants.pxi ARGS --constants)
generate_style_file(styleclass.pxi ARGS --properties)
generate_style_file(stylesets.pxi ARGS --sets)

set(STYLE_INFIXES
    "_"
    "_activate_"
    "_hover_"
    "_idle_"
    "_insensitive_"
    "_selected_"
    "_selected_activate_"
    "_selected_hover_"
    "_selected_idle_"
    "_selected_insensitive_"
)

foreach(infix ${STYLE_INFIXES})
    generate_style_file("style${infix}functions.pyx" ARGS --function ${infix})
endforeach()

add_custom_target(generate_style_files ALL DEPENDS ${GENERATED_STYLE_FUNCTION_FILES})
message(STATUS "Generated style files: ${GENERATED_STYLE_FUNCTION_FILES}")

# Core extensions
add_cython_extension(_renpy
    INSTALL_DIR .
    SOURCES src/IMG_savepng.c src/core.c
)

add_cython_extension(_renpybidi
    INSTALL_DIR .
    SOURCES src/renpybidicore.c
)

add_cython_extension(_renpytfd
    INSTALL_DIR .
    SOURCES src/tinyfiledialogs/tinyfiledialogs.c
)

# renpy.* extensions
add_cython_extension(renpy.astsupport)
add_cython_extension(renpy.cslots)
add_cython_extension(renpy.lexersupport)
add_cython_extension(renpy.pydict)
add_cython_extension(renpy.style
    GENERATED_DEPENDENCIES ${styleconstants.pxi_TARGET})
add_cython_extension(renpy.encryption)

# renpy.audio extensions
set(AUDIO_COMPILE_ARGS)

add_cython_extension(renpy.audio.renpysound
    SOURCES src/renpysound_core.c src/ffmedia.c
    COMPILE_ARGS ${AUDIO_COMPILE_ARGS}
)

add_cython_extension(renpy.audio.filter)

# renpy.styledata extensions
add_cython_extension(renpy.styledata.styleclass
    GENERATED_DEPENDENCIES ${styleclass.pxi_TARGET})
add_cython_extension(renpy.styledata.stylesets
    GENERATED_DEPENDENCIES ${stylesets.pxi_TARGET})

# Style function extensions
foreach(infix ${STYLE_INFIXES})
    add_cython_extension(renpy.styledata.style${infix}functions
        PYX_FILE "${STYLEGEN_BUILD_DIR}/style${infix}functions.pyx"
    )
endforeach()

# renpy.display extensions
add_cython_extension(renpy.display.matrix)
add_cython_extension(renpy.display.render)
add_cython_extension(renpy.display.accelerator)
add_cython_extension(renpy.display.quaternion)

# renpy.uguu extensions
add_cython_extension(renpy.uguu.gl)
add_cython_extension(renpy.uguu.uguu)

# renpy.gl2 extensions
add_cython_extension(renpy.gl2.gl2mesh)
add_cython_extension(renpy.gl2.gl2mesh2)
add_cython_extension(renpy.gl2.gl2mesh3)
add_cython_extension(renpy.gl2.gl2polygon)
add_cython_extension(renpy.gl2.gl2model)
add_cython_extension(renpy.gl2.gl2draw)
add_cython_extension(renpy.gl2.gl2texture)
add_cython_extension(renpy.gl2.gl2uniform)
add_cython_extension(renpy.gl2.gl2shader)

# Cubism extension (if available)
if(CUBISM_SDK_PATH)
    add_cython_extension(renpy.gl2.live2dmodel)
endif()

add_cython_extension(renpy.gl2.assimp
    SOURCES src/assimpio.cc
    LANGUAGE CXX
)

# renpy.text extensions
add_cython_extension(renpy.text.textsupport)
add_cython_extension(renpy.text.texwrap)
add_cython_extension(renpy.text.ftfont
    SOURCES src/ftsupport.c src/ttgsubtable.c
)
add_cython_extension(renpy.text.hbfont
    SOURCES src/ftsupport.c
)

set(RENPY_VERSION_FILE "${CMAKE_CURRENT_BINARY_DIR}/renpy/vc_version.py")
file(MAKE_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/renpy")

add_custom_target(generate_renpy_version ALL
    COMMAND
    ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/renpy/versions.py --output "${RENPY_VERSION_FILE}"
    BYPRODUCTS "${RENPY_VERSION_FILE}"
    COMMENT "Generating Ren'Py version information in build directory."
)

# Install Python modules
install(
    DIRECTORY renpy/
    DESTINATION renpy
    FILES_MATCHING PATTERN "*.py"
)
