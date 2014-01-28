# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

# The presplash process, if any.
proc = None

# Called from the main process. This determines if
# we're even doing presplash, and if so what will be shown to the
# user. If it decides to show something to the user, uses subprocess
# to actually handle the showing.
def start(basedir, gamedir):
    import os.path

    if "RENPY_LESS_UPDATES" in os.environ:
        return

    global proc

    filenames = [ "/presplash.png", "/presplash.jpg" ]
    for fn in filenames:
        fn = gamedir + fn
        if os.path.exists(fn):
            break
    else:
        return

    try:
        import subprocess
        import sys

        cmd = [sys.executable, "-EO", sys.argv[0], "show", "presplash", fn]

        def fsencode(s):
            if isinstance(s, str):
                return s

            return s.encode(sys.getfilesystemencoding() or "utf-8", "replace")

        proc = subprocess.Popen([ fsencode(i) for i in cmd ], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    except:
        pass


# Called just before we initialize the display for real, to
# hide the splash, and terminate window centering.
def end():

    global proc

    if not proc:
        return

    proc.stdin.close()
    proc.wait()

    proc = None

# Called in the presplash process, to actually display the presplash.
def show(fn):

    import pygame.display
    import pygame.constants
    import sys
    import os

    os.environ['SDL_VIDEO_CENTERED'] = "1"

    try:
        import pygame.macosx
        pygame.macosx.init() #@UndefinedVariable
    except:
        pass

    try:
        import pygame.macosx #@Reimport
        pygame.macosx.Video_AutoInit()
    except:
        pass

    pygame.display.init()

    img = pygame.image.load(fn, fn)
    screen = pygame.display.set_mode(img.get_size(), pygame.constants.NOFRAME)
    screen.blit(img, (0, 0))
    pygame.display.update()

    sys.stdout.write("READY\r\n")
    sys.stdout.flush()
    sys.stdin.read()

    sys.exit(0)
