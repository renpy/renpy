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

# Pre-splash code. The goal of this code is to try to get a pre-splash
# screen up as soon as possible, to let the user know something is
# going on.

import threading
import pygame_sdl2
import os.path
import sys

# The window.
window = None

# Should the event thread keep running?
keep_running = False

def run_event_thread():
    """
    Disposes of events while the window is running.
    """

    pygame_sdl2.time.set_timer(pygame_sdl2.USEREVENT, 20)

    while keep_running:
        pygame_sdl2.event.wait()

    pygame_sdl2.time.set_timer(pygame_sdl2.USEREVENT, 0)

# Called from the main process. This determines if
# we're even doing presplash, and if so what will be shown to the
# user. If it decides to show something to the user, uses subprocess
# to actually handle the showing.
def start(basedir, gamedir):

    if "RENPY_LESS_UPDATES" in os.environ:
        return

    filenames = [ "/presplash.png", "/presplash.jpg" ]
    for fn in filenames:
        fn = gamedir + fn
        if os.path.exists(fn):
            break
    else:
        return

    pygame_sdl2.display.init()

    img = pygame_sdl2.image.load(fn, fn)

    global window

    window = pygame_sdl2.display.Window(
        sys.argv[0],
        img.get_size(),
        flags=pygame_sdl2.WINDOW_BORDERLESS,
        pos=(pygame_sdl2.WINDOWPOS_CENTERED, pygame_sdl2.WINDOWPOS_CENTERED))

    window.get_surface().blit(img, (0, 0))
    window.update()

    global event_thread

    event_thread = threading.Thread(target=run_event_thread)
    event_thread.daemon = True
    event_thread.start()

# Called just before we initialize the display for real, to
# hide the splash, and terminate window centering.
def end():

    global keep_running
    global event_thread
    global window

    if window is None:
        return

    keep_running = False

    event_thread.join()

    window.destroy()
    window = None
