cmake_minimum_required(VERSION 3.15)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C CXX)

# Find required packages
find_package(Python 3.12 EXACT REQUIRED COMPONENTS Interpreter Development.Module)
find_package(PkgConfig REQUIRED)

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

# Set up Cython
find_program(CYTHON_EXECUTABLE cython REQUIRED)

# Global settings
set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 11)

# Build configuration
option(RENPY_STATIC "Build static version" OFF)
option(RENPY_COVERAGE "Enable coverage" OFF)
set(CUBISM_SDK_PATH "" CACHE PATH "Path to Cubism SDK")
set(PYGAME_SDL2_HEADERS "" CACHE PATH "Path to pygame_sdl2/headers")

if(DEFINED ENV{RENPY_STATIC})
    set(RENPY_STATIC ON)
    message(STATUS "RENPY_STATIC is defined")
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
    message(STATUS "$ENV{PYGAME_SDL2_HEADERS}")
    message(FATAL_ERROR "PYGAME_SDL2_HEADERS is not defined")
endif()


# Set generation directory
set(GEN_DIR ${CMAKE_CURRENT_BINARY_DIR}/gen3)
if(RENPY_COVERAGE)
    set(GEN_DIR ${GEN_DIR}-coverage)
endif()
if(RENPY_STATIC)
    set(GEN_DIR ${GEN_DIR}-static)
endif()

file(MAKE_DIRECTORY ${GEN_DIR})

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/src
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${PYGAME_SDL2_HEADERS}
    ${GEN_DIR}
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

# Global compile flags
set(GLOBAL_COMPILE_FLAGS
    -Wno-unused-function
    -std=gnu99
)

if(WIN32)
    list(APPEND GLOBAL_COMPILE_FLAGS -fno-strict-aliasing)
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

# Function to create Cython extension
function(add_cython_extension name)
    set(options)
    set(oneValueArgs LANGUAGE PYX_FILE)
    set(multiValueArgs SOURCES LIBRARIES COMPILE_ARGS DEFINITIONS)
    cmake_parse_arguments(ARG "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

    # Set defaults
    if(NOT ARG_LANGUAGE)
        set(ARG_LANGUAGE "c")
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

    # Set output file extension
    if(ARG_LANGUAGE STREQUAL "c++")
        set(c_file ${GEN_DIR}/${name}.cc)
    else()
        set(c_file ${GEN_DIR}/${name}.c)
    endif()

    # Cython flags
    set(CYTHON_FLAGS
        -3
        --3str
        -X profile=False
        -X embedsignature=True
        -I${CMAKE_CURRENT_SOURCE_DIR}/src
        -I${GEN_DIR}
        -I${CMAKE_CURRENT_SOURCE_DIR}
    )

    if(ARG_LANGUAGE STREQUAL "c++")
        list(APPEND CYTHON_FLAGS --cplus)
    endif()

    if(RENPY_COVERAGE)
        list(APPEND CYTHON_FLAGS -X linetrace=true)
    endif()

    if(DEFINED ENV{RENPY_ANNOTATE_CYTHON})
        list(APPEND CYTHON_FLAGS -a)
    endif()

    # Generate C file from Cython
    add_custom_command(
        OUTPUT ${c_file}
        COMMAND ${CYTHON_EXECUTABLE} ${CYTHON_FLAGS} ${pyx_file} -o ${c_file}
        DEPENDS ${pyx_file}
        COMMENT "Generating ${c_file} from ${pyx_file}"
    )

    # Handle static build modifications
    if(RENPY_STATIC)
        set(static_c_file ${GEN_DIR}/${name}_static.c)

        add_custom_command(
            OUTPUT ${static_c_file}
            COMMAND ${CMAKE_COMMAND} -E copy ${c_file} ${c_file}.dynamic
            COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/scripts/fix_static.py
                ${c_file} ${static_c_file} ${name}
            DEPENDS ${c_file}
            COMMENT "Creating static version of ${name}"
        )

        set(final_c_file ${static_c_file})
    else()
        set(final_c_file ${c_file})
    endif()

    # Create Python extension
    python_add_library(${name} MODULE ${final_c_file} ${ARG_SOURCES})

    # Extract the base filename for the extension
    get_filename_component(base_filename ${module_path} NAME)

    # Set properties
    set_target_properties(${name} PROPERTIES
        PREFIX ""
        OUTPUT_NAME ${base_filename}
    )

    # Compile flags
    target_compile_options(${name} PRIVATE
        ${GLOBAL_COMPILE_FLAGS}
        ${ARG_COMPILE_ARGS}
    )

    # Link libraries
    target_link_libraries(${name} PRIVATE
        ${GLOBAL_LIBRARIES}
        ${ARG_LIBRARIES}
    )

    # Add definitions
    if(ARG_DEFINITIONS)
        target_compile_definitions(${name} PRIVATE ${ARG_DEFINITIONS})
    endif()

    if(RENPY_COVERAGE)
        target_compile_definitions(${name} PRIVATE CYTHON_TRACE=1)
    endif()

    # Install the extension
    string(REPLACE "." "/" install_subpath ${name})
    get_filename_component(install_dir ${install_subpath} DIRECTORY)
    if (install_dir STREQUAL "")
        set(install_dir "renpy")
    endif()
    install(TARGETS ${name} DESTINATION ${install_dir})
endfunction()

# Generate style files

set(STYLE_PREFIXES
    "" "selected_hover_" "selected_idle_" "selected_insensitive_"
    "hover_" "idle_" "insensitive_" "activate_" "selected_activate_"
)

set(STYLE_FUNCTION_FILES
    ${GEN_DIR}/styleconstants.pxi
    ${GEN_DIR}/styleclass.pxi
    ${GEN_DIR}/stylesets.pxi
)
foreach(prefix ${STYLE_PREFIXES})
    set(style_file ${GEN_DIR}/style_${prefix}functions.pyx)
    list(APPEND STYLE_FUNCTION_FILES ${style_file})
endforeach()

add_custom_command(
    OUTPUT ${STYLE_FUNCTION_FILES}
    COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate_styles.py ${GEN_DIR}
    WORKING_DIRECTORY ${GEN_DIR}
    COMMENT "Generating style files"
)

# Core extensions
add_cython_extension(_renpy
    SOURCES src/IMG_savepng.c src/core.c
)

add_cython_extension(_renpybidi
    SOURCES src/renpybidicore.c
)

add_cython_extension(_renpytfd
    SOURCES src/tinyfiledialogs/tinyfiledialogs.c
)

# renpy.* extensions
add_cython_extension(renpy.astsupport)
add_cython_extension(renpy.cslots)
add_cython_extension(renpy.lexersupport)
add_cython_extension(renpy.pydict)
add_cython_extension(renpy.style)
add_cython_extension(renpy.encryption)

# renpy.audio extensions
set(AUDIO_COMPILE_ARGS)

add_cython_extension(renpy.audio.renpysound
    SOURCES src/renpysound_core.c src/ffmedia.c
    COMPILE_ARGS ${AUDIO_COMPILE_ARGS}
)

add_cython_extension(renpy.audio.filter)

# renpy.styledata extensions
add_cython_extension(renpy.styledata.styleclass)
add_cython_extension(renpy.styledata.stylesets)

# Style function extensions
foreach(prefix ${STYLE_PREFIXES})
    add_cython_extension(renpy.styledata.style_${prefix}functions
        PYX_FILE ${GEN_DIR}/style_${prefix}functions.pyx
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
    LANGUAGE c++
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

install(
    DIRECTORY renpy/
    DESTINATION renpy
    FILES_MATCHING PATTERN "*.py"
)
