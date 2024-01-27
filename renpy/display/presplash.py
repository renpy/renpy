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

# Pre-splash code. The goal of this code is to try to get a pre-splash
# screen up as soon as possible, to let the user know something is
# going on.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *


import os
import sys
import time

import pygame_sdl2
import renpy

if renpy.emscripten:
    import emscripten

# The window.
window = None

# The progress bar (if exists).
progress_bar = None

# The start time.
start_time = time.time()


class ProgressBar(object):

    def __init__(self, foreground, background):
        super(ProgressBar, self).__init__()
        self.foreground = pygame_sdl2.image.load(foreground)
        self.background = pygame_sdl2.image.load(background)
        self.width, self.height = self.background.get_size()

    def convert_alpha(self, surface=None):
        self.foreground = self.foreground.convert_alpha(surface)
        self.background = self.background.convert_alpha(surface)

    def get_size(self):
        return (self.width, self.height)

    def get_at(self, pos):
        return self.background.get_at(pos)

    def draw(self, target, done):
        width = self.width * min(done, 1)
        foreground = self.foreground.subsurface(0, 0, width, self.height)
        target.blit(self.background, (0, 0))
        target.blit(foreground, (0, 0))


def find_file(base_name, root):
    allowed_exts = [ ".png", ".jpg" ]
    for ext in allowed_exts:
        fn = os.path.join(root, base_name + ext)
        if os.path.exists(fn):
            return fn
    return None


def start(basedir, gamedir):
    """
    Called to display the presplash when necessary.
    """

    if "RENPY_LESS_UPDATES" in os.environ:
        return

    presplash_fn = find_file("presplash", root=gamedir)

    if not presplash_fn:
        foreground_fn = find_file("presplash_foreground", root=gamedir)
        background_fn = find_file("presplash_background", root=gamedir)

        if not foreground_fn or not background_fn:
            return

    if renpy.windows:

        import ctypes

        ctypes.windll.user32.SetProcessDPIAware() # type: ignore

    pygame_sdl2.display.init()

    global progress_bar

    if presplash_fn:
        presplash = pygame_sdl2.image.load(presplash_fn)
    else:
        presplash = ProgressBar(foreground_fn, background_fn) # type: ignore
        progress_bar = presplash

    global window

    bounds = pygame_sdl2.display.get_display_bounds(0)

    sw, sh = presplash.get_size()
    x = bounds[0] + bounds[2] // 2 - sw // 2
    y = bounds[1] + bounds[3] // 2 - sh // 2

    if presplash.get_at((0, 0))[3] == 0:
        shape = presplash
    else:
        shape = None

    if isinstance(shape, ProgressBar):
        shape = shape.background

    window = pygame_sdl2.display.Window(
        sys.argv[0],
        (sw, sh),
        flags=pygame_sdl2.WINDOW_BORDERLESS,
        pos=(x, y),
        shape=shape)

    if presplash_fn:
        presplash = presplash.convert_alpha(window.get_surface())
        window.get_surface().blit(presplash, (0, 0))
    else:
        presplash.convert_alpha(window.get_surface())
        presplash.draw(window.get_surface(), 0)

    window.update()


# The last time the progress bar was updated.
last_pump_time = 0

# The number of times the progress was pumped.
pump_count = 0

def pump_window():

    global last_pump_time
    global pump_count

    pump_count += 1

    if renpy.emscripten:
        emscripten.sleep(0)

    if window is None:
        return

    if last_pump_time + 1/24 > time.time():
        return

    last_pump_time = time.time()

    if progress_bar and renpy.game.script:
        progress_bar.draw(window.get_surface(), pump_count / (len(renpy.game.script.script_files) + 23))
        window.update()

    for ev in pygame_sdl2.event.get():
        if ev.type == pygame_sdl2.QUIT:
            raise renpy.game.QuitException(relaunch=False, status=0)

# Becomes true when the presplash is done.
done = False


def end():
    """
    Called just before we initialize the display to hide the presplash.
    """

    global window
    global done

    done = True

    if renpy.emscripten:
        emscripten.run_script(r"""presplashEnd();""")

    if window is None:
        return

    window.destroy()
    window = None

    # Remove references to presplash images
    global progress_bar
    progress_bar = None


def sleep():
    """
    Pump window to the end of config.minimum_presplash_time.
    """

    if not (window or renpy.mobile):
        return

    end_time = start_time + renpy.config.minimum_presplash_time

    while end_time - time.time() > 0:
        pump_window()


progress_kind = None

def progress(kind, done, total):
    """
    Reports progress to emscripten.

    `kind`
        The kind of progress being reported. This is printed each time
        it changes.

    `done`
        The number of units of progress that are complete.

    `total`
        The total number of units of progress.
    """

    global progress_kind

    if not renpy.emscripten:
        return

    if done:
        return

    if not PY2:

        if progress_kind != kind:
            print()
            print(kind)
            progress_kind = kind
            sys.stdout.flush()

        emscripten.run_script(r"""progress(%d, %d);""" % (done, total))

    emscripten.sleep(0)
