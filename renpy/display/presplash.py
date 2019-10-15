# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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

# Pre-splash code. The goal of this code is to try to get a pre-splash
# screen up as soon as possible, to let the user know something is
# going on.

from __future__ import print_function

import pygame_sdl2
import os.path
import sys
import time

import renpy

# The window.
window = None

# The start time.
start_time = time.time()

def start(basedir, gamedir):
    """
    Called to display the presplash when necessary.
    """

    if "RENPY_LESS_UPDATES" in os.environ:
        return

    filenames = [ "/presplash.png", "/presplash.jpg" ]
    for fn in filenames:
        fn = gamedir + fn
        if os.path.exists(fn):
            break
    else:
        return

    if renpy.windows:

        import ctypes
        from ctypes import c_void_p, c_int

        ctypes.windll.user32.SetProcessDPIAware()

    pygame_sdl2.display.init()

    img = pygame_sdl2.image.load(fn, fn)

    global window

    bounds = pygame_sdl2.display.get_display_bounds(0)

    sw, sh = img.get_size()
    x = bounds[0] + bounds[2] // 2 - sw // 2
    y = bounds[1] + bounds[3] // 2 - sh // 2

    window = pygame_sdl2.display.Window(
        sys.argv[0],
        (sw, sh),
        flags=pygame_sdl2.WINDOW_BORDERLESS,
        pos=(x, y))

    img = img.convert_alpha(window.get_surface())

    window.get_surface().blit(img, (0, 0))
    window.update()

    global start_time
    start_time = time.time()


def pump_window():
    if window is None:
        return

    for ev in pygame_sdl2.event.get():
        if ev.type == pygame_sdl2.QUIT:
            raise renpy.game.QuitException(relaunch=False, status=0)


def end():
    """
    Called just before we initialize the display to hide the presplash.
    """

    global window

    if renpy.emscripten:
        # presplash handled on the JavaScript side, because emscripten
        # currently does not support destroying/recreating GL contexts
        import emscripten
        emscripten.run_script(r"""presplashEnd();""")

    if window is None:
        return

    window.destroy()
    window = None


def sleep():
    """
    Pump window to the end of config.minimum_presplash_time.
    """

    if not (window or renpy.mobile):
        return

    end_time = start_time + renpy.config.minimum_presplash_time

    while end_time - time.time() > 0:
        pump_window()
