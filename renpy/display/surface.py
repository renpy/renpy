# Function to allocate a surface.
import pygame
from pygame.constants import *

def surface(size, flags, depth):
    """
    Allocate a surface. Flags and depth are ignored, for compatibility
    with pygame.Surface.
    """

    return pygame.Surface(size, flags, 32)

# surface = pygame.Surface
