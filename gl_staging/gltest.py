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



s = pygame.display.set_mode((800, 600), pygame.OPENGL|pygame.DOUBLEBUF)
sample = pygame.Surface((10, 10), 0, 32, masks)


pysdlgl.init_glew()
gltexture.init(sample)

def load_image(fn):
    im = pygame.image.load(fn, fn)
    w, h = im.get_size()
    
    im2 = pygame.Surface((w + 2, h + 2), 0, sample)
    im2.blit(im, (1, 1))

    return im2.subsurface((1, 1, w, h))

gl.ClearColor(0.0, 0.0, 0.0, 0.0)
gl.Clear(gl.COLOR_BUFFER_BIT)


gl.MatrixMode(gl.PROJECTION)
gl.LoadIdentity()
# gl.Ortho2D(0, 800, 600, 0)
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

environ = glenviron.FixedFunctionGLEnviron()

start = time.time()

class Transform(object):

    def __init__(self):
        self.xdx = 1
        self.xdy = 0
        self.ydx = 0
        self.ydy = 1

transform = Transform()

FRAMES = 1500

for i in xrange(FRAMES):
    if sys.argv[1] == "blend":
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


