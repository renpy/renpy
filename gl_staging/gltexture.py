import pygame
import _renpy_tegl as gl
import _renpy_pysdlgl as pysdlgl

# The size of the side of a texture, not including the 1-pixel
# border on all sides.
SIDE = 126

# An empty texture we can use to initialize a texture to the right size.
# This is (SIDE + 2, SIDE + 2) in size.
empty_surface = None


def check_error():
    """
    This checks for an opengl error, and throws an exception if it occurs.
    """

    err = gl.GetError()
    
    if err:
        raise Exception("GL Error: 0x%x" % err)
    

class Texture(object):
    """
    This object stores information about an OpenGL texture.
    """

    def __init__(self, number):

        
        # The number of the OpenGL texture this texture object
        # represents.
        self.number = number

        # True if the texture has been loaded at least once.
        self.loaded = False
            
        # These are used to map an index into texture coordinates.
        self.xmul = 0
        self.xadd = 0
        self.ymul = 0
        self.yadd = 0

        # A reference count giving the number of TextureGrids that
        # refer to this texture. When this falls to 0, the texture
        # can be placed back into the pool.
        self.refcount = 0

        
    def incref(self):
        """
        Increases the reference count of this texture.
        """

        self.refcount += 1

        
    def decref(self):
        """
        Decreases the reference count of this texture by 1. If it
        falls to 0, puts the texture back on the freelist.
        """

        self.refcount -= 1
        if not self.refcount:
            free_textures.append(self)

            
    def load_surface(self, surf, x, y, w, h):
        """
        Loads a pygame surface into this texture rectangle.
        """

        x = x - 1
        y = y - 1
        w = w + 2
        h = h + 2

        gl.BindTexture(gl.TEXTURE_2D, self.number)
        gl.TexParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR)
        gl.TexParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR)

        # If we haven't initalized the texture yet, and we're
        # smaller than it, load in the empty texture.
        if w < SIDE or h < SIDE:
            if not self.loaded:
                pysdlgl.load_texture(
                    empty_surface,
                    0,
                    0,
                    SIDE + 2,
                    SIDE + 2, 
                    0)

            self.loaded = True

        # Otherwise, either load or replace the texture.
        pysdlgl.load_texture(
            surf,
            x,
            y,
            w,
            h,
            self.loaded)

        # Needs to be here twice, since we may not go through the w < SIDE
        # h < SIDE thing all the time.
        self.loaded = True

        # Finally, load in the default math.
        self.xmul = self.xadd = self.ymul = self.yadd = 1.0 / (SIDE + 2)

        
# This is a list of unused Textures.
free_textures = [ ]

# This allocates a texture, either from the free list, or by asking
# gl.
def alloc_texture():
    """
    Allocate a texture, either from the freelist or by asking GL. The
    returned texture has a reference count of 1.
    """
    
    if free_textures:
        rv = free_textures.pop(0)

    else:
        texnums = [ 0 ]
        gl.GenTextures(1, texnums)

        rv = Texture(texnums[0])

    rv.incref()
    return rv




        
class TextureGrid(object):
    """
    This represents one or more textures that cover a rectangular
    area.   
    """

    def __init__(self, width, height):

        # The width and height of this TextureGrid
        self.width = width
        self.height = height

        # For each row of tiles, a tuple giving:
        # - The y offset within the texture.
        # - The height of the row.
        self.rows = [ ]

        # For each column of tiles, a tuple giving.
        # - The x offset within the texture.
        # - The width of the column.
        self.columns = [ ]

        # The actual grid of texture titles, a list of lists of
        # textures. The outer list represents the rows, the inner
        # lists columns.
        self.tiles = [ ]
    
    
def texture_grid_from_surface(surf):    
    """
    This takes a Surface and turns it into a TextureGrid.
    """

    width, height = surf.get_size()

    rv = TextureGrid(width, height)

    # Fill in the widths.
    for x in xrange(0, width, SIDE):
        rv.columns.append((0, min(width - x, SIDE)))

    # Fill in the heights, and at the same time, load the textures.
    for y in xrange(0, height, SIDE):
        rowheight = min(height - y, SIDE)
        rv.rows.append((0, rowheight))

        row = [ ]
        
        for x in xrange(0, width, SIDE):
            colwidth = min(width - x, SIDE)

            tex = alloc_texture()

            tex.load_surface(surf, x, y, colwidth, rowheight)

            row.append(tex)
            
        rv.tiles.append(row)

    return rv
            
def draw_texgrid(tg, sx, sy):
    """
    This draws the supplied texture grid at coordinates x, y on the
    screen.

    `sx`, `sy` - The screen coordinates at which the texture grid
    should be drawn.
    """
    
    y = 0
    
    for (texy, texh), row in zip(tg.rows, tg.tiles):
        x = 0

        for (texx, texw), tex in zip(tg.columns, row):

            # These should be forward-transformed.
            x0, y0 = x, y
            x1, y1 = x + texw, y
            x2, y2 = x, y + texh
            x3, y3 = x + texw, y + texh

            u0 = tex.xadd + tex.xmul * texx
            u1 = tex.xadd + tex.xmul * (texx + texw)
            v0 = tex.yadd + tex.ymul * texy
            v1 = tex.yadd + tex.ymul * (texy + texh)

            gl.Color4f(1.0, 1.0, 1.0, 1.0)
            gl.BindTexture(gl.TEXTURE_2D, tex.number)
            
            gl.Begin(gl.TRIANGLE_STRIP)

            gl.TexCoord2f(u0, v0)
            gl.Vertex2f(x0, y0)

            gl.TexCoord2f(u1, v0)
            gl.Vertex2f(x1, y1)

            gl.TexCoord2f(u0, v1)
            gl.Vertex2f(x2, y2)

            gl.TexCoord2f(u1, v1)
            gl.Vertex2f(x3, y3)

            gl.End()

            x += texw

        y += texh


def init(sample):
    """
    Initialize this module. This must be called after pygame has been
    initialized.
    """
        
    # Create the empty surface.
    global empty_surface
    empty_surface = pygame.Surface((SIDE + 2, SIDE + 2), 0, sample)
    
    
        
