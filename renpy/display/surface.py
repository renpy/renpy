# Function to allocate a surface.
import pygame
from pygame.constants import *

def Surface(width, height):
    """
    Allocate a surface. Flags and depth are ignored, for compatibility
    with pygame.Surface.
    """

    import renpy.game as game

    return pygame.Surface((width, height), 0,
                          game.interface.display.sample_surface)

# surface = pygame.Surface
