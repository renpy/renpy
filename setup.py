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

import os
import sys
from pathlib import Path

import scripts.generate_styles as generate_styles
import scripts.setuplib as setuplib
from scripts.setuplib import cython, env, generate_all_cython, generate_setup_files

# Change to the directory containing this file.
BASE = Path(__file__).resolve().parent


def main():
    os.chdir(BASE)

    setuplib.init()
    setuplib.check_imports(BASE / "scripts", "setuplib.py", "generate_styles.py")

    generate_styles.generate()

    # These control the level of optimization versus debugging.
    setuplib.extra_compile_args = ["-Wno-unused-function"]
    setuplib.extra_link_args = []

    cubism = os.environ.get("CUBISM", None)
    if cubism:
        setuplib.include_dirs.append(f"{cubism}/Core/include")

    # src/ directory.
    cython("_renpy", ["src/IMG_savepng.c", "src/core.c"], packages="sdl3 libpng")

    # renpy.pygame
    cython("renpy.pygame.iostream", packages="sdl3")
    cython("renpy.pygame.locals", packages="sdl3")
    cython(
        "renpy.pygame.image",
        ["src/pygame/write_png.c", "src/pygame/write_jpeg.c"],
        packages="sdl3-image libjpeg libpng sdl3",
    )
    cython("renpy.pygame.sdl_image", packages="sdl3")
    cython("renpy.pygame.controller", packages="sdl3")
    cython("renpy.pygame.joystick", packages="sdl3")
    cython("renpy.pygame.pygame_time", packages="sdl3")
    cython("renpy.pygame.power", packages="sdl3")
    cython("renpy.pygame.transform", source=["src/pygame/SDL3_rotozoom.c"], packages="sdl3")
    cython("renpy.pygame.scrap", packages="sdl3")
    cython("renpy.pygame.key", packages="sdl3")
    cython("renpy.pygame.mouse", packages="sdl3")
    cython("renpy.pygame.event", packages="sdl3")
    cython("renpy.pygame.display", packages="sdl3")
    cython("renpy.pygame.sdl", packages="sdl3")
    cython("renpy.pygame.color", packages="sdl3")
    cython("renpy.pygame.rect", packages="sdl3")
    cython("renpy.pygame.error", packages="sdl3")
    cython("renpy.pygame.surface", packages="sdl3")
    cython("renpy.pygame.draw", packages="sdl3")
    cython(
        "renpy.pygame.gfxdraw",
        source=["src/pygame/SDL3_gfxPrimitives.c", "src/pygame/SDL3_rotozoom.c"],
        packages="sdl3",
    )

    # renpy
    cython("renpy.astsupport")
    cython("renpy.cslots")
    cython("renpy.lexersupport")
    cython("renpy.pydict")
    cython("renpy.style")
    cython("renpy.encryption")
    cython("renpy.tfd", ["src/tinyfiledialogs/tinyfiledialogs.c"], setup_filename="Setup.tfd")
    cython("renpy.ecsign", ["src/ec_sign_core.c", "src/ec_sign_core_web.c"], packages="openssl")

    # renpy.audio
    cython(
        "renpy.audio.renpysound",
        ["src/renpysound_core.c", "src/ffmedia.c"],
        compile_args=["-Wno-deprecated-declarations"]
        if ("RENPY_FFMPEG_NO_DEPRECATED_DECLARATIONS" in os.environ)
        else [],
        packages="libavformat libavcodec libavutil libswresample libswscale sdl3",
    )

    cython("renpy.audio.filter")

    # renpy.styledata
    cython("renpy.styledata.styleclass")

    for p in generate_styles.prefixes:
        cython(f"renpy.styledata.style_{p}functions")

    # renpy.display
    cython("renpy.display.matrix")
    cython("renpy.display.render")
    cython("renpy.display.accelerator", packages="sdl3")
    cython("renpy.display.quaternion")

    # renpy.uguu
    cython("renpy.uguu.gl", packages="sdl3")
    cython("renpy.uguu.uguu", packages="sdl3")

    # renpy.gl2
    cython("renpy.gl2.gl2mesh")
    cython("renpy.gl2.gl2mesh2")
    cython("renpy.gl2.gl2mesh3")
    cython("renpy.gl2.gl2polygon")
    cython("renpy.gl2.gl2model")
    cython("renpy.gl2.gl2draw", packages="sdl3")
    cython("renpy.gl2.gl2texture", packages="sdl3")
    cython("renpy.gl2.gl2uniform")
    cython("renpy.gl2.gl2shader")

    if cubism:
        cython("renpy.gl2.live2dmodel", ["src/live2dcsm.c"], packages="sdl3")

    cython("renpy.gl2.assimp", ["src/assimpio.cc"], language="c++", packages="assimp sdl3")

    # renpy.text
    cython("renpy.text.textsupport")
    cython("renpy.text.texwrap")
    cython("renpy.text.ftfont", ["src/ftsupport.c", "src/ttgsubtable.c"], packages="freetype2 harfbuzz sdl3")
    cython("renpy.text.hbfont", ["src/ftsupport.c"], packages="freetype2 harfbuzz sdl3")
    cython("renpy.text.bidi", ["src/renpybidicore.c"], packages="fribidi")

    generate_all_cython()
    generate_setup_files()

    if len(sys.argv) >= 2 and sys.argv[1] == "generate":
        return

    env("CC")
    env("LD")
    env("CXX")
    env("CFLAGS")
    env("LDFLAGS")

    setuplib.setup("renpy", "8.99.99")


if __name__ == "__main__":
    main()
