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

    for gamedir in [ _gamedir, 'game', 'data' ]:
        if os.path.exists(gamedir + "/presplash.png"):
            break
    else:
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
    
