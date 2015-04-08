#!/usr/bin/env python

# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

import platform
import sys
import os
import subprocess

# Change to the directory containing this file.
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

# Create the gen directory if it doesn't exist.
try:
    os.makedirs("gen")
except:
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
from setuplib import android, ios, include, library, cython, pymodule, copyfile, find_unnecessary_gen

# These control the level of optimization versus debugging.
setuplib.extra_compile_args = [ "-Wno-unused-function" ]
setuplib.extra_link_args = [ ]

# Detect win32.
if platform.win32_ver()[0]:
    windows = True
    setuplib.extra_compile_args.append("-fno-strict-aliasing")
else:
    windows = False

include("zlib.h")
include("png.h")
include("SDL.h", directory="SDL2")
include("ft2build.h")
include("freetype/freetype.h", directory="freetype2", optional=True) or include("freetype.h", directory="freetype2")
include("libavutil/avstring.h")
include("libavformat/avformat.h")
include("libavcodec/avcodec.h")
include("libswscale/swscale.h")
include("GL/glew.h")
include("pygame_sdl2/pygame_sdl2.h", directory="python{}.{}".format(sys.version_info.major, sys.version_info.minor))

library("SDL2")
library("png")
library("avformat")
library("avcodec")
library("avutil")
has_avresample = library("avresample", optional=True)
has_swscale = library("swscale", optional=True)
library("freetype")
has_fribidi = library("fribidi", optional=True)
library("z")
has_libglew = library("GLEW", optional=True)
has_libglew32 = library("glew32", optional=True)

has_angle = windows and library("EGL", optional=True) and library("GLESv2", optional=True)

if android:
    sdl = [ 'SDL2', 'GLESv2', 'log' ]
    png = 'png16'
else:
    sdl = [ 'SDL2' ]
    png = 'png'


if has_fribidi and (not android) and (not ios):
    try:
        # Some versions of fribidi require glib, and it doesn't hurt to include it in
        # our path.
        glib_flags = subprocess.check_output(["pkg-config", "--cflags", "glib-2.0"])
        setuplib.extra_compile_args.extend(glib_flags.split())
    except:
        pass

steam_sdk = os.environ.get("RENPY_STEAM_SDK", None)
steam_platform = os.environ.get("RENPY_STEAM_PLATFORM", "")

if steam_sdk:
    setuplib.library_dirs.append("{}/redistributable_bin/{}".format(steam_sdk, steam_platform))
    setuplib.include_dirs.append("{}/public".format(steam_sdk))

# Modules directory.
cython(
    "_renpy",
    [ "IMG_savepng.c", "core.c", "subpixel.c"],
    sdl + [ png, 'z', 'm' ])

if has_fribidi:
    cython(
        "_renpybidi",
        [ "renpybidicore.c" ],
        ['fribidi'], define_macros=[ ("FRIBIDI_ENTRY", "") ])

cython("_renpysteam", language="c++", compile_if=steam_sdk, libs=["steam_api"])

# Sound.
pymodule("pysdlsound.__init__")

sound = [ "avformat", "avcodec", "avutil", "z" ]
macros = [ ]

if has_avresample:
    sound.insert(0, "avresample")
    macros.append(("HAS_RESAMPLE", 1))

if has_swscale:
    sound.insert(0, "swscale")

cython(
    "pysdlsound.sound",
    [ "pss.c", "ffdecode.c" ],
    libs = sdl + sound,
    define_macros=macros)

# renpy
cython("renpy.style")
# cython("renpy.styleclass")

# renpy.styledata
cython("renpy.styledata.styleclass")
cython("renpy.styledata.stylesets")

for p in generate_styles.prefixes:
    cython("renpy.styledata.style_{}functions".format(p), pyx="gen/style_{}functions.pyx".format(p))

# renpy.display
cython("renpy.display.render", libs=[ 'z', 'm' ])
cython("renpy.display.accelerator", libs=sdl + [ 'z', 'm' ])

# renpy.gl
if (android or ios):
    glew_libs = [ 'GLESv2', 'z', 'm' ]
    gl2_only = True
    egl = "egl_none.c"
elif has_libglew:
    glew_libs = [ 'GLEW' ]
    gl2_only = False
    egl = "egl_none.c"
else:
    glew_libs = [ 'glew32', 'opengl32' ]
    gl2_only = False
    egl = "egl_none.c"

cython("renpy.gl.gl", libs=glew_libs)
cython("renpy.gl.gl1", libs=glew_libs, compile_if=not gl2_only)
cython("renpy.gl.gldraw", libs=glew_libs, source=[ egl ])
cython("renpy.gl.gltexture", libs=glew_libs)
cython("renpy.gl.glenviron_shader", libs=glew_libs)
cython("renpy.gl.glenviron_fixed", libs=glew_libs, compile_if=not gl2_only)
cython("renpy.gl.glenviron_limited", libs=glew_libs, compile_if=not gl2_only)
cython("renpy.gl.glrtt_copy", libs=glew_libs)
cython("renpy.gl.glrtt_fbo", libs=glew_libs)

if not (android or ios):
    # renpy.angle
    def anglecopy(fn):
        copyfile("renpy/gl/" + fn, "renpy/angle/" + fn, "DEF ANGLE = False", "DEF ANGLE = True")

    anglecopy("glblacklist.py")
    anglecopy("gldraw.pxd")
    anglecopy("gldraw.pyx")
    anglecopy("glenviron_shader.pyx")
    anglecopy("glrtt_fbo.pyx")
    anglecopy("glrtt_copy.pyx")
    anglecopy("gltexture.pxd")
    anglecopy("gltexture.pyx")

    angle_libs = [ "SDL2", "EGL", "GLESv2" ]

    def anglecython(name, source=[]):
        cython(name, libs=angle_libs, compile_if=has_angle, define_macros=[ ( "ANGLE", None ) ], source=source)

    anglecython("renpy.angle.gl")
    anglecython("renpy.angle.gldraw", source=[ "egl_angle.c" ])
    anglecython("renpy.angle.gltexture")
    anglecython("renpy.angle.glenviron_shader")
    anglecython("renpy.angle.glrtt_fbo")
    anglecython("renpy.angle.glrtt_copy")

# renpy.text
cython("renpy.text.textsupport")
cython("renpy.text.texwrap")

cython(
    "renpy.text.ftfont",
    [ "ftsupport.c", "ttgsubtable.c" ],
    libs = sdl + [ 'freetype', 'z', 'm' ])

find_unnecessary_gen()

# Figure out the version, and call setup.
sys.path.insert(0, '..')

import renpy

setuplib.setup("Ren'Py", renpy.version[7:])

if not has_fribidi:
    print "Warning: Did not include fribidi."
