# Function to allocate a surface.
import pygame
from pygame.constants import *

import renpy

def Surface(width, height):
    """
    Allocate a surface. Flags and depth are ignored, for compatibility
    with pygame.Surface.
    """

    return pygame.Surface((width, height), 0,
                          renpy.game.interface.display.sample_surface)

# surface = pygame.Surface
