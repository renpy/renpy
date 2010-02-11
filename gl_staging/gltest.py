import pygame
import time
import sys

import _renpy_tegl as gl
import _renpy_pysdlgl as pysdlgl

import surface

little_endian = (
    0x000000FF,
    0x0000FF00,
    0x00FF0000,
    0xFF000000)

big_endian = (
    0xFF000000,
    0x00FF0000,
    0x0000FF00,
    0x000000FF
    )

pygame.display.init()

s = pygame.display.set_mode((800, 600), pygame.OPENGL|pygame.DOUBLEBUF)
sample = pygame.Surface((10, 10), 0, 32, little_endian)

surface.init(sample)

def load_image(fn):
    im = pygame.image.load(fn, fn)
    w, h = im.get_size()
    
    im2 = pygame.Surface((w + 2, h + 2), 0, sample)
    im2.blit(im, (1, 1))

    return im2.subsurface((1, 1, w, h))


gl.ClearColor(0.0, 0.0, 0.0, 1.0)
gl.Clear(gl.COLOR_BUFFER_BIT)

gl.MatrixMode(gl.PROJECTION)
gl.LoadIdentity()
gl.Ortho2D(0, 800, 800, 0)
gl.MatrixMode(gl.MODELVIEW)

gl.Enable(gl.BLEND)
gl.BlendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA)

gl.Enable(gl.TEXTURE_2D)

im0 = load_image("washington.jpg")
tg0 = surface.texture_grid_from_surface(im0)
