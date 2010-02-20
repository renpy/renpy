import pygame
import _renpy_tegl as gl
import _renpy_pysdlgl as pysdlgl

import glenviron

# TODO:
# - Texgrid Subsurface/size/etc.
# - Texgrid from drawing on screen.
# - Shader Environment.
# - Integrate w/ Ren'Py

# The maximum size of a texture.
MAX_SIZE = 512

# Possible sizes for a texture.
SIZES = [ 512, 256, 128, 64 ]

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

    def __init__(self, number, width, height):


        # The width and height of this texture.
        self.width = width
        self.height = height
        
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
            free_textures[self.width, self.height].append(self)

            
    def load_surface(self, surf, x, y, w, h):
        """
        Loads a pygame surface into this texture rectangle.
        """

        gl.BindTexture(gl.TEXTURE_2D, self.number)
        gl.TexParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR)
        gl.TexParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR)

        
        # If we haven't initalized the texture yet, and we're
        # smaller than it, load in the empty texture.
        if w < self.width or h < self.height:

            if not self.loaded:
                pysdlgl.load_texture(
                    None,
                    0,
                    0,
                    self.width,
                    self.height,
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
        self.xadd = self.yadd = 0
        self.xmul = 1.0 / self.width
        self.ymul = 1.0 / self.height

    def render_to(self, x, y, draw_func):

        glenviron.rtt.render(self.number, x, y, self.width, self.height, draw_func, self.loaded)
        
        self.loaded = True
            
        self.xadd = 0
        self.yadd = 0
        self.xmul = 1.0 / self.width
        self.ymul = 1.0 / self.height

        
# This is a map from texture sizes to a list of free textures of that
# size.
free_textures = { }

# Initialize free_textures.        
for height in SIZES:
    for width in SIZES:
        free_textures[width, height] = [ ]


# This allocates a texture, either from the free list, or by asking
# gl.
def alloc_texture(width, height):
    """
    Allocate a texture, either from the freelist or by asking GL. The
    returned texture has a reference count of 1.
    """

    l = free_textures[width, height]

    if l:
        rv = l.pop()
        
    else:
        texnums = [ 0 ]
        gl.GenTextures(1, texnums)

        rv = Texture(texnums[0], width, height)
        
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

    def __del__(self):
        """
        On delete, drop the tiles' refcounts.
        """

        for i in self.tiles:
            for j in i:
                if j:
                    j.decref()
        

# This is a cache from (width, size) to the results of compute_tiling.
tiling_cache = { }
        
def compute_tiling(width, max_size=MAX_SIZE):
    """
    This computes a tiling for an image with the given width (or
    height). It takes a width as an argument, and returns two lists.

    The first is a list of (offset, width, index) tuples, as are used
    in TextureGrid to determine how to blit an image to the screen.

    The second is a list of (offset, copy-width, total-width) tuples
    that are used to create the tiles.

    While we're thinking about this as if it's working horizontally
    (x, width, etc), it 
    """

    # Check the cache.
    key = (width, max_size)
    if key in tiling_cache:
        return tiling_cache[key]
    
    # width is the remaining width, not including any borders
    # required.

    # The x-offset, relative to the left side of the surface.
    x = 0

    # The list of row tuples.
    row = [ ]

    # The list of tile tuples.
    tiles = [ ]

    # The index into the row.
    row_index = 0 
    
    while width:

        # The size of the left border of this tile.
        if x == 0:
            left_border = 0
        else:
            left_border = 1

        # Figure out the texture size to use.
        for size in SIZES:
            if size > max_size:
                continue

            # Ensure each texture is at least 2/3rds full. (Except the
            # smallest.)
            if size * .66 <= width + left_border:
                break
            
        # Figure out if we want to use a border.
        if size < width + left_border:
            right_border = 1
        else:
            right_border = 0
            
        # The number of pixels to display to the user from this tile.
        row_size = min(width, size - left_border - right_border)

        #Add to the results. 
        row.append((left_border, row_size, row_index))
        tiles.append((x - left_border, row_size + left_border + right_border, size))
                   
        # Update the counters.
        row_index += 1
        x += row_size
        width -= row_size

    tiling_cache[key] = (row, tiles)
        
    return row, tiles


def texture_grid_from_surface(surf):    
    """
    This takes a Surface and turns it into a TextureGrid.
    """

    width, height = surf.get_size()

    rv = TextureGrid(width, height)

    rv.columns, texcolumns = compute_tiling(width)
    rv.rows, texrows = compute_tiling(height)

    for y, height, texheight in texrows:
        row = [ ]
            
        for x, width, texwidth in texcolumns:
            
            tex = alloc_texture(texwidth, texheight)
            tex.load_surface(surf, x, y, width, height)
            
            row.append(tex)
            
        rv.tiles.append(row)
        
    return rv


def texture_grid_from_drawing(width, height, draw_func):    
    """
    This creates a texture grid of `width` by `height` by using
    draw_func to draw to the screen.
    """

    glenviron.rtt.begin()
    
    rv = TextureGrid(width, height)

    rv.columns, texcolumns = compute_tiling(width)
    rv.rows, texrows = compute_tiling(height)

    for y, height, texheight in texrows:
        row = [ ]
            
        for x, width, texwidth in texcolumns:
            
            tex = alloc_texture(texwidth, texheight)
            tex.render_to(x, y, draw_func)
            
            row.append(tex)
            
        rv.tiles.append(row)

    glenviron.rtt.end()
        
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
            

def blit(textures, transform, alpha):
    """
    This draws the supplied textures to the screen.

    `texture` is a list of (tg, sx, sy) tuples, where `tg` is a
    texture grid, and (`sx`, `sy`) is the offset from the upper-left
    corner of the screen, in (fractional) pixels.

    `transform` is the transform to apply to the texgrid, when going from
    texgrid coordinates to screen coordinates.

    `alpha` is the alpha multiplier applied, from 0.0 to 1.0.
    """

    glenviron.environ.blit()
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


def blend(textures, transform, alpha, fraction):
    """
    This blends two textures to the screen.

    `textures` is a list of (tg, sx, sy) tuples, where `tg` is a
    texture grid, and (`sx`, `sy`) is the offset from the upper-left
    corner of the screen, in (fractional) pixels.

    `transform` is the transform to apply to the texgrid, when going from
    texgrid coordinates to screen coordinates.

    `alpha` is the alpha multiplier applied, from 0.0 to 1.0.

    `fraction` is the fraction of the second texture to show.
    """

    glenviron.environ.blend(fraction)
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


def imageblend(textures, transform, alpha, fraction, ramp):
    """
    This uses texture 0 to control the blending of tetures 1 and 2 to
    the screen.

    `textures` is a list of (tg, sx, sy) tuples, where `tg` is a
    texture grid, and (`sx`, `sy`) is the offset from the upper-left
    corner of the screen, in (fractional) pixels.

    `transform` is the transform to apply to the texgrid, when going from
    texgrid coordinates to screen coordinates.

    `alpha` is the alpha multiplier applied, from 0.0 to 1.0.

    `fraction` is the fraction of the second texture to show.

    `ramp` is the length of the blending ramp to use.

    """

    glenviron.environ.imageblend(fraction, ramp)
    gl.Color4f(1.0, 1.0, 1.0, alpha)

    # The three textures must start at the same sx, sy coordinates.
    tg0, sx, sy = textures[0]
    tg1, sx, sy = textures[1]
    tg2, sx, sy = textures[2]

    y = 0

    rows0, rows1, rows2 = align_axes(tg0.rows, tg1.rows, tg2.rows)
    cols0, cols1, cols2 = align_axes(tg0.columns, tg1.columns, tg2.columns)
    
    # t0 = texture 0, t1 = texture 1.
    # x, y - index into the texture.
    # w, h - width and height to draw.
    # ri, ci - row index, column index in tiles.
    for (t0y, t0h, t0ri), (t1y, t1h, t1ri), (t2y, t2h, t2ri) in zip(rows0, rows1, rows2):
        x = 0

        for (t0x, t0w, t0ci), (t1x, t1w, t1ci), (t2x, t2w, t2ci) in zip(cols0, cols1, cols2):
            
            t0 = tg0.tiles[t0ri][t0ci]
            t1 = tg1.tiles[t1ri][t1ci]
            t2 = tg2.tiles[t2ri][t2ci]
            
            pysdlgl.draw_rectangle(
                sx, sy,
                x, y,
                t0w, t0h, 
                transform,
                t0, t0x, t0y,
                t1, t1x, t1y,
                t2, t2x, t2y)

            x += t0w

        y += t0h


