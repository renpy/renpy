#!/usr/bin/env python

# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import print_function

import platform
import sys
import os
import subprocess

import future

# Change to the directory containing this file.
BASE = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(BASE)

# Create the gen directory if it doesn't exist.
try:
    os.makedirs("gen")
except Exception:
    pass

# Generate styles.
import generate_styles
generate_styles.generate()

# If RENPY_CC or RENPY_LD are in the environment, and CC or LD are not, use them.
def setup_env(name):
    renpy_name = "RENPY_" + name
    if (renpy_name in os.environ) and (name not in os.environ):
        os.environ[name] = os.environ[renpy_name]


setup_env("CC")
setup_env("LD")
setup_env("CXX")

import setuplib
from setuplib import android, ios, emscripten, raspi, include, library, cython, cmodule, copyfile, find_unnecessary_gen, generate_all_cython, PY2

# These control the level of optimization versus debugging.
setuplib.extra_compile_args = [ "-Wno-unused-function" ]
setuplib.extra_link_args = [ ]

# Detect win32.
if platform.win32_ver()[0]:
    windows = True
    setuplib.extra_compile_args.append("-fno-strict-aliasing")
    tfd_libs = [ "comdlg32", "ole32" ]

else:
    windows = False
    tfd_libs = [ ]

if raspi:
    setuplib.extra_compile_args.append("-DRASPBERRY_PI")

include("zlib.h")
include("png.h")
include("SDL.h", directory="SDL2")
include("ft2build.h")
include("freetype/freetype.h", directory="freetype2", optional=True) or include("freetype.h", directory="freetype2") # type: ignore
include("libavutil/avstring.h", directory="ffmpeg", optional=True) or include("libavutil/avstring.h") # type: ignore
include("libavformat/avformat.h", directory="ffmpeg", optional=True) or include("libavformat/avformat.h") # type: ignore
include("libavcodec/avcodec.h", directory="ffmpeg", optional=True) or include("libavcodec/avcodec.h") # type: ignore
include("libswscale/swscale.h", directory="ffmpeg", optional=True) or include("libswscale/swscale.h") # type: ignore
include("GL/glew.h")
include("pygame_sdl2/pygame_sdl2.h", directory="python{}.{}".format(sys.version_info.major, sys.version_info.minor))
include("hb.h", directory="harfbuzz")

library("SDL2")
library("png")
library("avformat")
library("avcodec")
library("avutil")
has_avresample = library("avresample", optional=True)
has_swresample = library("swresample", optional=True)
has_swscale = library("swscale", optional=True)
library("freetype")
library("z")
has_libglew = library("GLEW", optional=True)
has_libglew32 = library("glew32", optional=True)

if android:
    sdl = [ 'SDL2', 'GLESv2', 'log' ]
    png = 'png16'
else:
    sdl = [ 'SDL2' ]
    png = 'png'

cubism = os.environ.get("CUBISM", None)
if cubism:
    setuplib.include_dirs.append("{}/Core/include".format(cubism))

# Modules directory.
cython(
    "_renpy",
    [ "IMG_savepng.c", "core.c" ],
    sdl + [ png, 'z', 'm' ])

cython("_renpybidi", [ "renpybidicore.c" ], [ "fribidi" ])

if not (android or ios or emscripten):
    cython("_renpytfd", [ "tinyfiledialogs/tinyfiledialogs.c" ], libs=tfd_libs)

# Sound.

sound = [ "avformat", "avcodec", "avutil", "z" ]
macros = [ ]

if has_swresample:
    sound.insert(3, "swresample")

if has_avresample:
    sound.insert(0, "avresample")
    macros.append(("HAS_RESAMPLE", 1))

if has_swscale:
    sound.insert(0, "swscale")

cython(
    "renpy.audio.renpysound",
    [ "renpysound_core.c", "ffmedia.c" ],
    libs=sdl + sound,
    define_macros=macros,
    compile_args=[ "-Wno-deprecated-declarations" ] if ("RENPY_FFMPEG_NO_DEPRECATED_DECLARATIONS" in os.environ) else [ ])

cython("renpy.audio.filter")

# renpy
cython("renpy.lexersupport")
cython("renpy.pydict")
cython("renpy.style")

cython("renpy.encryption")

# renpy.compat
if PY2:
    cython("renpy.compat.dictviews")

# renpy.styledata
cython("renpy.styledata.styleclass")
cython("renpy.styledata.stylesets")

for p in generate_styles.prefixes:
    cython("renpy.styledata.style_{}functions".format(p), pyx=setuplib.gen + "/style_{}functions.pyx".format(p))

# renpy.display
cython("renpy.display.matrix")
cython("renpy.display.render", libs=[ 'z', 'm' ])
cython("renpy.display.accelerator", libs=sdl + [ 'z', 'm' ])
cython("renpy.display.quaternion", libs=[ 'm' ])

cython("renpy.uguu.gl", libs=sdl)
cython("renpy.uguu.uguu", libs=sdl)

cython("renpy.gl.gldraw", libs=sdl)
cython("renpy.gl.gltexture", libs=sdl)
cython("renpy.gl.glenviron_shader", libs=sdl)
cython("renpy.gl.glrtt_copy", libs=sdl)
cython("renpy.gl.glrtt_fbo", libs=sdl)

cython("renpy.gl2.gl2mesh")
cython("renpy.gl2.gl2mesh2")
cython("renpy.gl2.gl2mesh3")
cython("renpy.gl2.gl2polygon")
cython("renpy.gl2.gl2model")
cython("renpy.gl2.gl2draw", libs=sdl)
cython("renpy.gl2.gl2texture", libs=sdl)
cython("renpy.gl2.gl2shader", libs=sdl)

if cubism:
    cython("renpy.gl2.live2dmodel", libs=sdl)

# renpy.text
cython("renpy.text.textsupport")
cython("renpy.text.texwrap")

cython(
    "renpy.text.ftfont",
    [ "ftsupport.c", "ttgsubtable.c" ],
    libs=sdl + [ 'freetype', 'z', 'm' ])

if not (PY2 and emscripten):

    cython(
        "renpy.text.hbfont",
        [ "ftsupport.c" ],
        libs=sdl + [ 'harfbuzz', 'freetype', 'z', 'm' ])

generate_all_cython()
find_unnecessary_gen()

# Figure out the version, and call setup.
sys.path.insert(0, '..')

import renpy

setuplib.setup("Ren'Py", renpy.version[7:].rstrip('un')) # @UndefinedVariable
