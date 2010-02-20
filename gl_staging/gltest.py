import pygame
import time
import sys

import _renpy
import _renpy_tegl as gl
import _renpy_pysdlgl as pysdlgl

import gltexture
import glenviron

# These are the pixel formats for big- and little-endian platforms.

if sys.byteorder == 'little':

    masks = (
        0x00FF0000,
        0x0000FF00,
        0x000000FF,
        -16777216) # 0xFF000000, but that's not representable as a short int.
else:

    masks = (
        0x0000FF00,
        0x00FF0000,
        -16777216,
        0x000000FF)

try:
    import pygame.macosx
    pygame.macosx.init()
except:
    pass
    
pygame.display.init()

WIDTH = 800
HEIGHT = 600

s = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL|pygame.DOUBLEBUF)
sample = pygame.Surface((10, 10), 0, 32, masks)


pysdlgl.init_glew()
gltexture.init(sample)

def load_image(fn):
    im = pygame.image.load(fn, fn)
    w, h = im.get_size()
    
    # im2 = pygame.Surface((w + 2, h + 2), 0, sample)
    # im2.blit(im, (1, 1))
    im2 = pygame.Surface((w + 0, h + 0), 0, sample)
    im2.blit(im, (0, 0))

    # return im2.subsurface((1, 1, w, h))
    return im2
    

def setup_screen():
    gl.Viewport(0, 0, WIDTH, HEIGHT)

    gl.MatrixMode(gl.PROJECTION)
    gl.LoadIdentity()
    gl.Ortho(0.0, 800.0, 600.0, 0.0, -1.0, 1.0)
    gl.MatrixMode(gl.MODELVIEW)




im0 = load_image("washington.jpg")
tg0 = gltexture.texture_grid_from_surface(im0)

im1 = load_image("whitehouse.jpg")
tg1 = gltexture.texture_grid_from_surface(im1)

im2 = load_image("id_circleiris.png")
# im2 = load_image("id_teleport.png")
_renpy.colormatrix(
   im2, im2,
   1, 0, 0, 0, 0,
   1, 0, 0, 0, 0,
   1, 0, 0, 0, 0,
   1, 0, 0, 0, 0,
   )
tg2 = gltexture.texture_grid_from_surface(im2)

im3 = load_image("eileen_happy.png")
tg3 = gltexture.texture_grid_from_surface(im3)

environ = glenviron.FixedFunctionGLEnviron()

class Transform(object):

    def __init__(self):
        self.xdx = 1
        self.xdy = 0
        self.ydx = 0
        self.ydy = 1

gl.ClearColor(0.0, 0.0, 0.0, 0.0)

transform = Transform()

FRAMES = 1500
start = time.time()

setup_screen()

def draw_func():
    gltexture.blit([ (tg0, 0, 0) ], transform, 1.0, environ)
    gltexture.blit([ (tg3, 0, 0) ], transform, 1.0, environ)
        
def draw_func2():
    gltexture.blit([ (tg0, 0, 0) ], transform, 1.0, environ)
    gltexture.blit([ (tg3, 400, 0) ], transform, 1.0, environ)
        

pygame.display.flip()

gl.Clear(gl.COLOR_BUFFER_BIT)

for i in xrange(FRAMES):
    if sys.argv[1] == "cttblit":
        tg4 = gltexture.texture_grid_from_drawing(800, 600, draw_func)
        setup_screen()
        gltexture.blit([ (tg4, 0, 0) ], transform, 1.0, environ)
    elif sys.argv[1] == "cttblend":
        tg4 = gltexture.texture_grid_from_drawing(800, 600, draw_func)
        tg5 = gltexture.texture_grid_from_drawing(800, 600, draw_func2)
        setup_screen()
        gltexture.blend([ (tg4, 0, 0), (tg5, 0, 0) ], transform, 1.0, environ, 1.0 * i / FRAMES)

    elif sys.argv[1] == "blend":
        gltexture.blend([ (tg0, 0, 0), (tg1, 0, 0) ], transform, 1.0, environ, 1.0 * i / FRAMES)
    elif sys.argv[1] == "halfblend":
        gltexture.blend([ (tg0, -400, 0), (tg1, -400, 0) ], transform, 1.0, environ, 1.0 * i / FRAMES)
    elif sys.argv[1] == "imageblend":
        gltexture.imageblend([ (tg2, 0, 0), (tg0, 0, 0), (tg1, 0, 0) ], transform, 1.0, environ, 1.0 * i / FRAMES, int(sys.argv[2]))
    elif sys.argv[1] == "newtexblit":
        tg0 = gltexture.texture_grid_from_surface(im0)
        gltexture.blit([ (tg0, 0, 0) ], transform, 1.0, environ)
    else:
        gltexture.blit([ (tg0, 0, 0) ], transform, 1.0, environ)

    pygame.display.flip()

end = time.time()
print 1.0 * FRAMES / (end - start)
    
while True:

    
    ev = pygame.event.wait()

    if ev.type == pygame.QUIT:
        break


    break
