import pygame
import _renpy_tegl as gl
import _renpy_pysdlgl as pysdlgl
import sys

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
        # - The rowindex in tiles.
        self.rows = [ ]

        # For each column of tiles, a tuple giving.
        # - The x offset within the texture.
        # - The width of the column.
        # - The colindex in tiles.
        self.columns = [ ]

        # The actual grid of texture titles, a list of lists of
        # textures. This is looked up by looking up rowindex and
        # colindex.
        self.tiles = [ ]
    
    
def texture_grid_from_surface(surf):    
    """
    This takes a Surface and turns it into a TextureGrid.
    """

    width, height = surf.get_size()

    rv = TextureGrid(width, height)

    colindex = 0
    rowindex = 0
    
    # Fill in the widths.
    for x in xrange(0, width, SIDE):
        rv.columns.append((0, min(width - x, SIDE), colindex))
        colindex += 1
        
    # Fill in the heights, and at the same time, load the textures.
    for y in xrange(0, height, SIDE):
        rowheight = min(height - y, SIDE)
        rv.rows.append((0, rowheight, rowindex))

        row = [ ]
        
        for x in xrange(0, width, SIDE):
            colwidth = min(width - x, SIDE)

            tex = alloc_texture()

            tex.load_surface(surf, x, y, colwidth, rowheight)

            row.append(tex)
            
        rv.tiles.append(row)

        rowindex += 1
        
    return rv


def align_axes(*args):
    """
    This takes n axes, each a list consisting of (offset, size, index)
    tuples. It returns a list of n lists. For each of the n lists, the
    ith element will be the same size. The indexes will appear in the
    same order they did in the original list.

    This is used to combine the grids of two or more texgrids into a
    single grid.
    """

    # The lists we're building.
    rv = [ [] for i in args ]

    # The index of the current element, for each member of args.
    cur = [ 0 for i in args ]

    # The parts of the current element.
    offset = [ i[0][0] for i in args ]
    size = [ i[0][1] for i in args ]
    index = [ i[0][2] for i in args ]

    # Cache it here to save function calls.
    nargs = len(args)

    loop = True
    
    while loop:

        # Figure out the minimum size.
        minsize = min(size)

        for i in xrange(nargs):

            # Create an entry of minsize.
            rv[i].append((offset[i], minsize, index[i]))

            # Adjust the offset and size.
            offset[i] += minsize
            size[i] -= minsize
                       
            # If the size fell to 0, then load the next element from
            # the arguments into offset, size, index. If we can't
            # we're done.
            if size[i] == 0:
                cur[i] += 1
                
                if cur[i] >= len(args[i]):
                    loop = False
                else:
                    offset[i], size[i], index[i] = args[i][cur[i]]

    return rv
            

def blit(textures, transform, alpha, environ):
    """
    This draws the supplied textures to the screen.

    `texture` is a list of (tg, sx, sy) tuples, where `tg` is a
    texture grid, and (`sx`, `sy`) is the offset from the upper-left
    corner of the screen, in (fractional) pixels.

    `transform` is the transform to apply to the texgrid, when going from
    texgrid coordinates to screen coordinates.

    `alpha` is the alpha multiplier applied, from 0.0 to 1.0.

    `environ` is the GLEnviron used.
    """

    environ.blit_environ()
    gl.Color4f(1.0, 1.0, 1.0, alpha)
    
    for tg, sx, sy in textures:
        y = 0

        for texy, texh, rowindex in tg.rows:
            x = 0

            for texx, texw, colindex in tg.columns:

                tex = tg.tiles[rowindex][colindex]
                
                pysdlgl.draw_rectangle(
                    sx, sy,
                    x, y,
                    texw, texh, 
                    transform,
                    tex, texx, texy,
                    None, 0, 0,
                    None, 0, 0)
                
                x += texw

            y += texh


def blend(textures, transform, alpha, environ, fraction):
    """
    This blends two textures to the screen.

    `textures` is a list of (tg, sx, sy) tuples, where `tg` is a
    texture grid, and (`sx`, `sy`) is the offset from the upper-left
    corner of the screen, in (fractional) pixels.

    `transform` is the transform to apply to the texgrid, when going from
    texgrid coordinates to screen coordinates.

    `alpha` is the alpha multiplier applied, from 0.0 to 1.0.

    `environ` is the GLEnviron used.
    
    `fraction` is the fraction of the second texture to show.
    """

    environ.blend_environ(fraction)
    gl.Color4f(1.0, 1.0, 1.0, alpha)

    # The two textures must start at the same sx, sy coordinates.
    tg0, sx, sy = textures[0]
    tg1, sx, sy = textures[1]

    y = 0

    rows0, rows1 = align_axes(tg0.rows, tg1.rows)
    cols0, cols1 = align_axes(tg0.columns, tg1.columns)
    
    # t0 = texture 0, t1 = texture 1.
    # x, y - index into the texture.
    # w, h - width and height to draw.
    # ri, ci - row index, column index in tiles.
    for (t0y, t0h, t0ri), (t1y, t1h, t1ri) in zip(rows0, rows1):
        x = 0

        for (t0x, t0w, t0ci), (t1x, t1w, t1ci) in zip(cols0, cols1):
            
            t0 = tg0.tiles[t0ri][t0ci]
            t1 = tg1.tiles[t1ri][t1ci]
            
            pysdlgl.draw_rectangle(
                sx, sy,
                x, y,
                t0w, t0h, 
                transform,
                t0, t0x, t0y,
                t1, t1x, t1y,
                None, 0, 0)

            x += t0w

        y += t0h


            

def init(sample):
    """
    Initialize this module. This must be called after pygame has been
    initialized.
    """
        
    # Create the empty surface.
    global empty_surface
    empty_surface = pygame.Surface((SIDE + 2, SIDE + 2), 0, sample)
    
    
        
