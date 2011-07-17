#!/usr/bin/env python


import platform
import sys
import os

# Change to the directory containing this file.
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

import setuplib
from setuplib import android, include, library, cython, cmodule, pymodule 

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
include("SDL.h", directory="SDL")
include("ft2build.h")
include("freetype/freetype.h", directory="freetype2")
include("libavutil/avstring.h")
include("libavformat/avformat.h")
include("libavcodec/avcodec.h")
include("libswscale/swscale.h")
include("GL/glew.h")

library("SDL")
library("png")
library("avformat")
library("avcodec")
library("avutil")
has_swscale = library("swscale", optional=True)
library("freetype")
has_fribidi = library("fribidi", optional=True)            
library("z")
has_libglew = library("GLEW", True)
has_libglew32 = library("glew32", True)

if android:
    sdl = [ 'sdl', 'GLESv1_CM', 'log' ]
else:
    sdl = [ 'SDL' ]


# Modules directory.
cython(
    "_renpy", 
    [ "IMG_savepng.c", "core.c", "rwobject.c", "subpixel.c"],
    sdl + [ 'png', 'z', 'm' ])

cmodule(
    "_renpy_font",
    [ "renpy_ttf.c", "renpy_font.c"],
    sdl + [ 'freetype', 'z', 'm' ],
    )

if has_fribidi and not android:
    cython(
        "_renpybidi", 
        [ "renpybidicore.c" ],
        ['fribidi'])
        

# Sound.
pymodule("pysdlsound.__init__")

if not android:

    sound = [ "avformat", "avcodec", "avutil", "z" ]
    if has_swscale:
        sound.insert(0, "swscale")

    cython(
        "pysdlsound.sound",
        [ "pss.c", "rwobject.c", "ffdecode.c" ],
        libs = sdl + sound)


# Display.
if android:
    glew_libs = [ 'GLESv1_CM', 'z', 'm' ]
elif has_libglew:
    glew_libs = [ 'GLEW' ]
else:
    glew_libs = [ 'glew32', "opengl32" ]

cython("renpy.display.render", libs=[ 'z', 'm' ])
cython("renpy.display.accelerator", libs=[ 'z', 'm' ])

cython("renpy.display.gldraw", libs=glew_libs )
cython("renpy.display.gltexture", libs=glew_libs)
cython("renpy.display.glenviron", libs=glew_libs)

if not android:
    cython("renpy.display.glenviron_fixed", libs=glew_libs)
    cython("renpy.display.glenviron_shader", libs=glew_libs)
    cython("renpy.display.glshader", libs=glew_libs)

cython("renpy.display.glenviron_limited", libs=glew_libs)

cython("renpy.display.glrtt_copy", libs=glew_libs)
cython("renpy.display.glrtt_fbo", libs=glew_libs)


# Text.
cython("renpy.text.textsupport")
cython("renpy.text.texwrap")

cython(
    "renpy.text.ftfont", 
    [ "ftsupport.c" ],
    libs = sdl + [ 'freetype', 'z', 'm' ])


# Figure out the version, and call setup.
sys.path.append('..')
import renpy

setuplib.setup(
    "Ren'Py",
    renpy.version[7:])
