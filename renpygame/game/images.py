
import renpygame as pygame
import constants

bullet = None
missile1 = None
missile2 = None
missile3 = None
invisible = None
background = None

def init():
    global bullet, missile1, missile2, missile3, invisible, background

    bullet = pygame.image.load(constants.datadir + "bullet.png")
    missile1 = pygame.image.load(constants.datadir + "ball1.png")
    missile2 = pygame.image.load(constants.datadir + "ball2.png")
    missile3 = pygame.image.load(constants.datadir + "ball3.png")
    invisible = pygame.image.load(constants.datadir + "bullet.png")
    background = pygame.image.load(constants.datadir + "background.png").convert()

