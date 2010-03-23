# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import collections
import pygame; pygame # other modules might depend on pygame.

try:
    import _renpy_tegl as gl; gl
    import _renpy_pysdlgl as pysdlgl; pysdlgl
except ImportError:
    gl = None
    pysdlgl = None


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
    

# A list of texture number allocated.
texture_numbers = [ ]
    
class Texture(object):
    """
    This object stores information about an OpenGL texture.
    """

    def __init__(self, width, height):


        # The width and height of this texture.
        self.width = width
        self.height = height
        
        # The number of the OpenGL texture this texture object
        # represents.
        self.generation = 0
        self.number = None

        # True if the texture has been created inside the GPU.
        self.created = False

        # These are used to map an index into texture coordinates.
        self.xmul = 0
        self.xadd = 0
        self.ymul = 0
        self.yadd = 0

        # These contained the premultiplied (but not GPU-loaded)
        # surface. They allow us to defer loading until the surface is
        # needed.

        self.premult = None
        self.premult_size = None
        
        # True if we're in NEAREST mode. False if we're in LINEAR mode.
        self.nearest = False

        # The free list we should be put on, or None if we're already on
        # a free list.
        self.free_list = None
        
        
    def __del__(self):

        # Release the surface.
        self.premult = None
        self.premult_size = None

        # The test needs to be here so we don't try to append during
        # interpreter shutdown.
        if self.free_list is not None:
            self.free_list.append(self)
            self.free_list = None
        
            
    def load_surface(self, surf, x, y, w, h):
        """
        Loads a pygame surface into this texture rectangle.
        """

        # This just queues the surface up for loading. The actual loading
        # occurs when the texture is first needed. This ensures that the
        # texture loading only occurs in the GL thread.

        self.premult = pysdlgl.premultiply(surf, x, y, w, h)
        self.premult_size = (w, h)

        
    def make_nearest(self):
        """
        Causes this texture to be rendered in nearest-neighbor mode.
        """

        if self.nearest:
            return

        gl.BindTexture(gl.TEXTURE_2D, self.number)
        gl.TexParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST)
        gl.TexParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST)
        
        self.nearest = True

        
    def make_linear(self):
        """
        Causes this texture to be rendered in linear interpolation mode.
        """

        if not self.nearest:
            return

        gl.BindTexture(gl.TEXTURE_2D, self.number)
        gl.TexParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR)
        gl.TexParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR)
        
        self.nearest = False
        

    def make_ready(self):
        """
        Makes the texture ready for use.
        """

        self.allocate()

        if self.premult:
            
            w, h = self.premult_size

            gl.BindTexture(gl.TEXTURE_2D, self.number)
            gl.TexParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR)
            gl.TexParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR)

            self.nearest = False
            
            # If we haven't initalized the texture yet, and we're
            # smaller than it, load in the empty texture.
            if w < self.width or h < self.height:

                if not self.created:
                    pysdlgl.load_premultiplied(
                        None,
                        self.width,
                        self.height,
                        0)

                self.created = True

            # Otherwise, either load or replace the texture.
            pysdlgl.load_premultiplied(
                self.premult,
                w,
                h,
                self.created)

            # Needs to be here twice, since we may not go through the w < SIDE
            # h < SIDE thing all the time.
            self.created = True

            # Finally, load in the default math.
            self.xadd = self.yadd = 0
            self.xmul = 1.0 / self.width
            self.ymul = 1.0 / self.height

            # We don't need to be loaded anymore.
            self.premult = None
            self.premult_size = None

            
    def render_to(self, x, y, draw_func, rtt):

        self.allocate()
        
        if not self.created:
            
            gl.BindTexture(gl.TEXTURE_2D, self.number)
            gl.TexParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR)
            gl.TexParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR)

            self.nearest = False
            
            pysdlgl.load_premultiplied(
                None,
                self.width,
                self.height,
                0)

            self.created = True
         
        rtt.render(self.number, x, y, self.width, self.height, draw_func)

        self.xadd = 0
        self.yadd = 0
        self.xmul = 1.0 / self.width
        self.ymul = 1.0 / self.height

        
    def allocate(self):
        """
        This allocates a texture number, if necessary.
        """

        if self.number is not None:
            return
        
        texnums = [ 0 ]
        gl.GenTextures(1, texnums)
        
        self.number = texnums[0]
        self.created = False
        
        texture_numbers.append(texnums[0])

        
# This is a map from texture sizes to a list of free textures of that
# size.
free_textures = collections.defaultdict(list)

        
# The total size (in bytes) of all the textures that have been allocated.
total_texture_size = 0

# This allocates a texture, either from the free list, or by asking
# gl.
def alloc_texture(width, height):
    """
    Allocate a texture, either from the freelist or by asking GL. The
    returned texture has a reference count of 1.
    """

    global total_texture_size

    
    l = free_textures[width, height]

    if l:
        rv = l.pop()
    else:        
        rv = Texture(width, height)
        total_texture_size += width * height * 4        

    rv.free_list = l
        
    return rv


def dealloc_textures():
    global texture_numbers
    
    for t in texture_numbers:
        gl.DeleteTextures(1, [ t ])

    texture_numbers = [ ]
    free_textures.clear()


def compute_subrow(row, offset, width):
    """
    Given a row (or column), this computes a subrow starting at the given
    offset and having the given width.

    It returns two list. The first is a list of (offset, width,
    output-tile) tuples. The second is a list of integers, giving the
    input tile corresponding to each output tile.
    """

    # An iterator over row.
    rowi = iter(row)

    # The output row and the output tile list. 
    outrow = [ ]
    tiles = [ ]

    # The output tile index.
    outtile = 0
    
    try:
        ioff, iwidth, itile = rowi.next()

        # Consume the offset.
        while True:
            if offset < iwidth:
                ioff += offset
                iwidth -= offset
                break

            
            offset -= iwidth
            ioff, iwidth, itile = rowi.next()

        # Consume the width.
        while True:
            
            if width < iwidth:
                outrow.append((ioff, width, outtile))
                tiles.append(itile)
                outtile += 1
                break

            outrow.append((ioff, iwidth, outtile))
            tiles.append(itile)
            outtile += 1

            width -= iwidth
            
            ioff, iwidth, itile = rowi.next()

    except StopIteration:
        pass

    return outrow, tiles


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

        # If it exists, a TextureGrid that is half the size of this
        # one.
        self.half_cache = None

        
    def get_size(self):
        return self.width, self.height

    
    def subsurface(self, (x, y, w, h)):
        """
        This produces a texture grid containing a rectangle "cut out"
        of this texture grid.
        """

        rv = TextureGrid(width, height)
        
        rv.rows, rowtiles = compute_subrow(self.rows, y, h)
        rv.columns, coltiles = compute_subrow(self.columns, x, w)

        for i in rowtiles:
            row = [ ]
            for j in coltiles:
                row.append(self.tiles[i][j])

            rv.tiles.append(row)

        return rv


    def make_ready(self, nearest=False):
        """
        Makes ready all the tile-textures in this texture grid.
        """

        for row in self.tiles:
            for t in row:
                t.make_ready()

                if nearest:
                    t.make_nearest()
                else:
                    t.make_linear()
        
        

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

        # Ensure we have an extra pixel to our right, so we don't
        # get garbage.
        if row_size + left_border != size:
            right_border = 1
        
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


def texture_grid_from_drawing(width, height, draw_func, rtt):    
    """
    This creates a texture grid of `width` by `height` by using
    draw_func to draw to the screen.
    """

    rtt.begin()
    
    rv = TextureGrid(width, height)

    rv.columns, texcolumns = compute_tiling(width)
    rv.rows, texrows = compute_tiling(height)

    for y, height, texheight in texrows:
        row = [ ]
            
        for x, width, texwidth in texcolumns:
            
            tex = alloc_texture(texwidth, texheight)
            tex.render_to(x, y, draw_func, rtt)
            
            row.append(tex)
            
        rv.tiles.append(row)

    rtt.end()
        
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
            

def blit(tg, sx, sy, transform, alpha, environ, nearest=False):
    """
    This draws texgrid `tg` to the screen. `sx` and `sy` are offsets from
    the upper-left corner of the screen.

    `transform` is the transform to apply to the texgrid, when going from
    texgrid coordinates to screen coordinates.

    `alpha` is the alpha multiplier applied, from 0.0 to 1.0.
    """

    tg.make_ready(nearest)
    
    environ.blit()
    gl.Color4f(alpha, alpha, alpha, alpha)

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


def blend(tg0, tg1, sx, sy, transform, alpha, fraction, environ):
    """
    Blends two textures to the screen.

    `tg0` and `tg1` are the texture.
    
    `sx` and `sy` are the offsets from the upper-left corner of the screen.
        
    `transform` is the transform to apply to the texgrid, when going from
    texgrid coordinates to screen coordinates.

    `alpha` is the alpha multiplier applied, from 0.0 to 1.0.

    `fraction` is the fraction of the second texture to show.
    """

    tg0.make_ready()
    tg1.make_ready()
    
    environ.blend(fraction)
    gl.Color4f(alpha, alpha, alpha, alpha)

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


def imageblend(tg0, tg1, tg2, sx, sy, transform, alpha, fraction, ramp, environ):
    """
    This uses texture 0 to control the blending of tetures 1 and 2 to
    the screen.

    `tg0`, `tg1`, and `tg2` are the textures. 
    
    `sx` and `sy` are the offsets from the upper-left corner of the screen.

    `transform` is the transform to apply to the texgrid, when going from
    texgrid coordinates to screen coordinates.

    `alpha` is the alpha multiplier applied, from 0.0 to 1.0.

    `fraction` is the fraction of the second texture to show.

    `ramp` is the length of the blending ramp to use.

    """

    tg0.make_ready()
    tg1.make_ready()
    tg2.make_ready()
    
    environ.imageblend(fraction, ramp)
    gl.Color4f(alpha, alpha, alpha, alpha)

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


