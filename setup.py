#!/usr/bin/env python

# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
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

import sys
import os

# Change to the directory containing this file.
BASE = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(BASE)

SCRIPTS = os.path.join(BASE, 'scripts')
sys.path.insert(0, SCRIPTS)

import setuplib
from setuplib import windows, library, cython, find_unnecessary_gen, generate_all_cython, env

import generate_styles

def main():

    setuplib.init()
    setuplib.check_imports(SCRIPTS, "setuplib.py", "generate_styles.py")

    generate_styles.generate()

    # These control the level of optimization versus debugging.
    setuplib.extra_compile_args = [ "-Wno-unused-function" ]
    setuplib.extra_link_args = [ ]

    pkgconfig_packages = """
    libavformat
    libavcodec
    libavutil
    libswresample
    libswscale
    harfbuzz
    freetype2
    fribidi
    sdl2
    """

    library("avformat")
    library("avcodec")
    library("avutil")
    library("swresample")
    library("swscale")
    library("harfbuzz")
    library("freetype")
    library("fribidi")
    library("SDL2")
    library("png")
    library("z")

    if windows:
        setuplib.extra_compile_args.append("-fno-strict-aliasing")
        library("comdlg32")
        library("ole32")

    cubism = os.environ.get("CUBISM", None)
    if cubism:
        setuplib.include_dirs.append("{}/Core/include".format(cubism))

    pkgconfig_packages = "assimp\n" + pkgconfig_packages
    library("assimp")

    # src/ directory.
    cython("_renpy", [ "src/IMG_savepng.c", "src/core.c" ])
    cython("_renpybidi", [ "src/renpybidicore.c" ])
    cython("_renpytfd", [ "src/tinyfiledialogs/tinyfiledialogs.c" ])

    # renpy
    cython("renpy.astsupport")
    cython("renpy.cslots")
    cython("renpy.lexersupport")
    cython("renpy.pydict")
    cython("renpy.style")
    cython("renpy.encryption")

    # renpy.audio
    cython("renpy.audio.renpysound", [ "src/renpysound_core.c", "src/ffmedia.c" ],
        compile_args=[ "-Wno-deprecated-declarations" ] if ("RENPY_FFMPEG_NO_DEPRECATED_DECLARATIONS" in os.environ) else [ ])

    cython("renpy.audio.filter")

    # renpy.styledata
    cython("renpy.styledata.styleclass")
    cython("renpy.styledata.stylesets")

    for p in generate_styles.prefixes:
        cython("renpy.styledata.style_{}functions".format(p), pyx=setuplib.gen + "/style_{}functions.pyx".format(p))

    # renpy.display
    cython("renpy.display.matrix")
    cython("renpy.display.render")
    cython("renpy.display.accelerator")
    cython("renpy.display.quaternion")

    # renpy.uguu
    cython("renpy.uguu.gl")
    cython("renpy.uguu.uguu")

    # renpy.gl2
    cython("renpy.gl2.gl2mesh")
    cython("renpy.gl2.gl2mesh2")
    cython("renpy.gl2.gl2mesh3")
    cython("renpy.gl2.gl2polygon")
    cython("renpy.gl2.gl2model")
    cython("renpy.gl2.gl2draw")
    cython("renpy.gl2.gl2texture")
    cython("renpy.gl2.gl2uniform")
    cython("renpy.gl2.gl2shader")

    if cubism:
        cython("renpy.gl2.live2dmodel")

    cython("renpy.gl2.assimp", [ "src/assimpio.cc" ], language="c++")

    # renpy.text
    cython("renpy.text.textsupport")
    cython("renpy.text.texwrap")
    cython("renpy.text.ftfont", [ "src/ftsupport.c", "src/ttgsubtable.c" ])
    cython("renpy.text.hbfont", [ "src/ftsupport.c" ])

    generate_all_cython()
    find_unnecessary_gen()

    pkgconfig_packages = pkgconfig_packages.replace("\n", " ").strip()

    env("CC")
    env("LD")
    env("CXX")
    env("CFLAGS", f"pkg-config --cflags {pkgconfig_packages}")
    env("LDFLAGS", f"pkg-config --libs {pkgconfig_packages}")

    import renpy
    version = renpy.version[7:].partition(".")[0] + ".99.99"

    setuplib.setup("renpy", version)


if __name__ == "__main__":
    main()
