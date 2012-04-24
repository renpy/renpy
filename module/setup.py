#!/usr/bin/env python

import platform
import sys
import os

# Change to the directory containing this file.
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

import setuplib
from setuplib import android, include, library, cython, cmodule, pymodule, copyfile, find_unnecessary_gen

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
has_libglew = library("GLEW", optional=True)
has_libglew32 = library("glew32", optional=True)
has_angle = windows and library("EGL", optional=True) and library("GLESv2", optional=True)

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
        ['fribidi'], define_macros=[ ("FRIBIDI_ENTRY", "") ])

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
cython("renpy.display.render", libs=[ 'z', 'm' ])
cython("renpy.display.accelerator", libs=[ 'z', 'm' ])

# Gl.
if android:
    glew_libs = [ 'GLESv1_CM', 'z', 'm' ]
elif has_libglew:
    glew_libs = [ 'GLEW' ]
else:
    glew_libs = [ 'glew32', 'opengl32' ]

cython("renpy.gl.gldraw", libs=glew_libs )
cython("renpy.gl.gltexture", libs=glew_libs)
cython("renpy.gl.glenviron_fixed", libs=glew_libs, compile_if=not android)
cython("renpy.gl.glenviron_shader", libs=glew_libs, compile_if=not android)
cython("renpy.gl.glenviron_limited", libs=glew_libs)
cython("renpy.gl.glrtt_copy", libs=glew_libs)
cython("renpy.gl.glrtt_fbo", libs=glew_libs)

# Angle
def anglecopy(fn):
    if android:
        return
    
    copyfile("renpy/gl/" + fn, "renpy/angle/" + fn, "DEF ANGLE = False", "DEF ANGLE = True")
    
anglecopy("glblacklist.py")
anglecopy("gldraw.pxd")
anglecopy("gldraw.pyx")
anglecopy("glenviron_shader.pyx")
anglecopy("gl.pxd")
anglecopy("glrtt_fbo.pyx")
anglecopy("glrtt_copy.pyx")
anglecopy("gltexture.pxd")
anglecopy("gltexture.pyx")

angle_libs = [ "SDL", "EGL", "GLESv2" ]

def anglecython(name, source=[]):
    cython(name, libs=angle_libs, compile_if=has_angle, define_macros=[ ( "ANGLE", None ) ], source=source)

anglecython("renpy.angle.gldraw", source=[ "anglesupport.c" ])
anglecython("renpy.angle.gltexture")
anglecython("renpy.angle.glenviron_shader")
anglecython("renpy.angle.glrtt_fbo")
anglecython("renpy.angle.glrtt_copy")

# Text.
cython("renpy.text.textsupport")
cython("renpy.text.texwrap")

cython(
    "renpy.text.ftfont", 
    [ "ftsupport.c" ],
    libs = sdl + [ 'freetype', 'z', 'm' ])

find_unnecessary_gen()

# Figure out the version, and call setup.
sys.path.append('..')
import renpy

setuplib.setup("Ren'Py", renpy.version[7:])

if not has_fribidi:
    print "Warning: Did not include fribidi."
