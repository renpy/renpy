# Copyright 2004-2008 PyTom <pytom@bishoujo.us>
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

import os
import os.path
import pygame.display
import pygame.constants

try:
    import pygame.macosx
except:
    pass

# The directory from which presplash images are loaded.
gamedir = None

# Are we actually using presplash?
active = False

# Called at the start of the presplash process. This determines if
# we're even doing presplash, and if so what will be shown to the
# user.
#
# As this is called before any of the renpy modules are even loaded,
# we need to be careful.
def start(_gamedir):

    global gamedir
    global active

    gamedir = _gamedir


    if not os.path.exists(gamedir + "/presplash.png"):
        return
        
    active = True

    os.environ['SDL_VIDEO_CENTERED'] = "1"

    try:
        pygame.macosx.init()
    except:
        pass

    pygame.display.init()

    img = pygame.image.load(gamedir + "/presplash.png")
    screen = pygame.display.set_mode(img.get_size(), pygame.constants.NOFRAME)
    screen.blit(img, (0, 0))
    pygame.display.update()


# Called just before we initialize the display for real, to
# hide the splash, and terminate window centering.
def end():

    global active

    if not active:
        return

    active = False

    del os.environ['SDL_VIDEO_CENTERED']
    pygame.display.quit()
    
