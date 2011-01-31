#cython: profile=False
# Copyright 2004-2011 Tom Rothamel <pytom@bishoujo.us>
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

from gl cimport *
from pygame cimport *

import collections
import renpy
    
# The maximum size of a texture.
MAX_SIZE = 512

# Possible sizes for a texture.
SIZES = [ 1024, 512, 256, 128, 64 ]

# A list of texture number allocated.
texture_numbers = [ ]

cdef int rtt_format = GL_RGBA
cdef int rtt_internalformat = GL_RGBA

def use_gles():
    """
    Called to trigger gles mode.
    """
    global rtt_format
    global rtt_internalformat
    
    rtt_format = GL_RGB 
    rtt_internalformat = GL_RGB 


cdef class TextureCore:
    """
    This object stores information about an OpenGL texture.
    """
    
    def __init__(TextureCore self, int width, int height):

        # The width and height of this texture.
        self.width = width
        self.height = height
        
        # The number of the OpenGL texture this texture object
        # represents.
        self.generation = 0
        self.number = -1

        # The format of this texture in the GPU (or 0 if not known).
        self.format = 0

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
        self.premult_left = 0
        self.premult_right = 0
        self.premult_top = 0
        self.premult_bottom = 0
        
        # True if we're in NEAREST mode. False if we're in LINEAR mode.
        self.nearest = False

        # The free list we should be put on, or None if we're already on
        # a free list.
        self.free_list = None
        
        
    def __del__(self):

        cdef unsigned int num

        # Release the surface.
        self.premult = None
        self.premult_size = None
        self.premult_left = 0
        self.premult_right = 0
        self.premult_top = 0
        self.premult_bottom = 0
        
        # The test needs to be here so we don't try to append during
        # interpreter shutdown.
        if self.free_list is not None:
            try:
                self.free_list.append(self)
                self.free_list = None
            except TypeError:
                pass # Let's not error on shutdown.
                
            
    def load_surface(self, surf, x, y, w, h,
                     border_left, border_top, border_right, border_bottom):

        """
        Loads a pygame surface into this texture rectangle.
        """

        # This just queues the surface up for loading. The actual loading
        # occurs when the texture is first needed. This ensures that the
        # texture loading only occurs in the GL thread.
        
        self.premult = premultiply(
            surf, x, y, w, h,
            border_left, border_top, border_right, border_bottom)
            
        self.premult_size = (w, h)

        
    cdef void make_nearest(TextureCore self):
        """
        Causes this texture to be rendered in nearest-neighbor mode.
        """

        if self.nearest:
            return

        glBindTexture(GL_TEXTURE_2D, self.number)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        
        self.nearest = True

        
    cdef void make_linear(TextureCore self):
        """
        Causes this texture to be rendered in linear interpolation mode.
        """

        if not self.nearest:
            return

        glBindTexture(GL_TEXTURE_2D, self.number)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        
        self.nearest = False
        

    cdef void make_ready(TextureCore self):
        """
        Makes the texture ready for use.
        """

        self.allocate()

        if self.premult:
            
            w, h = self.premult_size

            glBindTexture(GL_TEXTURE_2D, self.number)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

            self.nearest = False
            
            # If we haven't initalized the texture yet, and we're
            # smaller than it, load in the empty texture.
            if w < self.width or h < self.height:

                if self.format != GL_RGBA:
                    load_premultiplied(
                        None,
                        self.width,
                        self.height,
                        0,
                        GL_RGBA,
                        GL_RGBA)

                    self.format = GL_RGBA

            # Otherwise, either load or replace the texture.
            load_premultiplied(
                self.premult,
                w,
                h,
                (self.format == GL_RGBA),
                GL_RGBA,
                GL_RGBA)

            # Needs to be here twice, since we may not go through the w < SIDE
            # h < SIDE thing all the time.
            self.format = GL_RGBA

            # Finally, load in the default math.
            self.xadd = self.yadd = 0
            self.xmul = 1.0 / self.width
            self.ymul = 1.0 / self.height

            # We don't need to be loaded anymore.
            self.premult = None
            self.premult_size = None

            
    def render_to(self, x, y, draw_func, rtt):

        self.allocate()
        
        if self.format != rtt_format:
            
            glBindTexture(GL_TEXTURE_2D, self.number)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

            self.nearest = False
            
            load_premultiplied(
                None,
                self.width,
                self.height,
                0,
                rtt_format,
                rtt_internalformat)

            self.format = rtt_format
         
        rtt.render(self.number, x, y, self.width, self.height, draw_func)

        self.xadd = 0
        self.yadd = 0
        self.xmul = 1.0 / self.width
        self.ymul = 1.0 / self.height
        
    cpdef int allocate(self):
        """
        This allocates a texture number, if necessary.
        """

        cdef unsigned int texnums[1]        
        
        
        if self.number != -1:
            return 0
        
        glGenTextures(1, texnums)
        
        self.number = texnums[0]
        self.format = 0

        texture_numbers.append(texnums[0])

        return 0
        
class Texture(TextureCore):
    """
    We need to be a real python class, not a C extension, to ensure that
    the __del__ method is called.
    """

    def __getstate__(self):
        if renpy.config.developer:
            raise Exception("Can't pickle a texture.")
        else:
            return { }
        
    def __setstate__(self, state):
        return
        
        
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

    cdef GLuint texnums[1]
    
    for t in texture_numbers:
        texnums[0] = t

        glDeleteTextures(1, texnums)

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


cdef class TextureGrid(object):
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

    def __getstate__(self):
        if renpy.config.developer:
            raise Exception("Can't pickle a texture.")
        else:
            return { }
        
    def __setstate__(self, state):
        return
                
    def get_size(self):
        return self.width, self.height
    
    def subsurface(self, rect):
        """
        This produces a texture grid containing a rectangle "cut out"
        of this texture grid.
        """

        (x, y, w, h) = rect
        
        rv = TextureGrid(w, h)

        rv.rows, rowtiles = compute_subrow(self.rows, y, h)
        rv.columns, coltiles = compute_subrow(self.columns, x, w)

        for i in rowtiles:
            row = [ ]
            for j in coltiles:
                row.append(self.tiles[i][j])

            rv.tiles.append(row)

        return rv


    cdef void make_ready(self, bint nearest):
        """
        Makes ready all the tile-textures in this texture grid.
        """

        cdef list row
        cdef TextureCore t
        
        for row in self.tiles:
            for t in row:
                t.make_ready()

                if nearest:
                    t.make_nearest()
                else:
                    t.make_linear()
        
        

# This is a cache from (width, size) to the results of compute_tiling.
tiling_cache = { }
        
def compute_tiling(width, max_size, min_fill_factor):
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
        # The size of the right border of this tile.
        right_border = 1
        
        # Figure out the texture size to use.
        for size in SIZES:
            if size > max_size:
                continue

            # Ensure each texture is full enough.
            if size * min_fill_factor <= width + left_border + right_border:
                break
            
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

    rv.columns, texcolumns = compute_tiling(width, MAX_SIZE, .66)
    rv.rows, texrows = compute_tiling(height, MAX_SIZE, .66)

    rownum = 0
    lastrow = len(texrows) - 1
    lastcol = len(texcolumns) - 1
    
    for y, height, texheight in texrows:

        border_top = (rownum == 0)
        border_bottom = (rownum == lastrow)
        rownum += 1
        
        row = [ ]

        colnum = 0
        
        for x, width, texwidth in texcolumns:

            border_left = (colnum == 0)
            border_right = (colnum == lastcol)
            colnum += 1

            tex = alloc_texture(texwidth, texheight)
            tex.load_surface(surf, x, y, width, height,
                             border_left, border_top, border_right, border_bottom)
            
            row.append(tex)
            
        rv.tiles.append(row)

    return rv


def texture_grid_from_drawing(width, height, draw_func, rtt):    
    """
    This creates a texture grid of `width` by `height` by using
    draw_func to draw to the screen.
    """

    rv = TextureGrid(width, height)

    gldraw = renpy.display.draw    
    pwidth, pheight = gldraw.physical_size
    
    rv.columns, texcolumns = compute_tiling(width, rtt.get_size_limit(pwidth), .5)
    rv.rows, texrows = compute_tiling(height, rtt.get_size_limit(pheight), .5)
    
    for y, height, texheight in texrows:
        row = [ ]
            
        for x, width, texwidth in texcolumns:
            
            tex = alloc_texture(texwidth, texheight)
            tex.render_to(x, y, draw_func, rtt)
            
            row.append(tex)
            
        rv.tiles.append(row)
        
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
            

cpdef blit(TextureGrid tg, double sx, double sy, render.Matrix2D transform, double alpha, environ, bint nearest):
    """
    This draws texgrid `tg` to the screen. `sx` and `sy` are offsets from
    the upper-left corner of the screen.

    `transform` is the transform to apply to the texgrid, when going from
    texgrid coordinates to screen coordinates.

    `alpha` is the alpha multiplier applied, from 0.0 to 1.0.
    """

    cdef int x, y
    cdef int texx, texy, texw, texh
    
    tg.make_ready(nearest)
    
    environ.blit()
    glColor4f(alpha, alpha, alpha, alpha)
    
    y = 0

    for texy, texh, rowindex in tg.rows:
        x = 0

        for texx, texw, colindex in tg.columns:

            tex = tg.tiles[rowindex][colindex]

            draw_rectangle(
                sx, sy,
                x, y,
                texw, texh, 
                transform,
                tex, texx, texy,
                None, 0, 0,
                None, 0, 0,
                )

            x += texw

        y += texh
 
cpdef blend(TextureGrid tg0, TextureGrid tg1, double sx, double sy, render.Matrix2D transform, double alpha, double fraction, environ):
    """
    Blends two textures to the screen.

    `tg0` and `tg1` are the texture.
    
    `sx` and `sy` are the offsets from the upper-left corner of the screen.
        
    `transform` is the transform to apply to the texgrid, when going from
    texgrid coordinates to screen coordinates.

    `alpha` is the alpha multiplier applied, from 0.0 to 1.0.

    `fraction` is the fraction of the second texture to show.
    """

    tg0.make_ready(False)
    tg1.make_ready(False)
    
    environ.blend(fraction)
    glColor4f(alpha, alpha, alpha, alpha)

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
            
            draw_rectangle(
                sx, sy,
                x, y,
                t0w, t0h, 
                transform,
                t0, t0x, t0y,
                t1, t1x, t1y,
                None, 0, 0,
                )

            x += t0w

        y += t0h

cpdef imageblend(TextureGrid tg0, TextureGrid tg1, TextureGrid tg2, double sx, double sy, render.Matrix2D transform, double alpha, double fraction, int ramp, environ):
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

    tg0.make_ready(False)
    tg1.make_ready(False)
    tg2.make_ready(False)
    
    environ.imageblend(fraction, ramp)
    glColor4f(alpha, alpha, alpha, alpha)

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

            draw_rectangle(
                sx, sy,
                x, y,
                t0w, t0h, 
                transform,
                t0, t0x, t0y,
                t1, t1x, t1y,
                t2, t2x, t2y,
                )
            
            x += t0w
            
        y += t0h

    
def premultiply(
    object pysurf,
    int x,
    int y,
    int w,
    int h,
    border_left, border_top, border_right, border_bottom):
    
    """
    Creates a string containing the premultiplied image data for
    for the (x, y, w, h) box inside pysurf. The various border_
    parameters control the addition of a border on the sides.
    """

    # Adjust the alpha if we have an alpha-free image.
    cdef unsigned char alpha_and
    cdef unsigned char alpha_or
    
    if pysurf.get_masks()[3]:
        alpha_and = 255
        alpha_or = 0
    else:
        alpha_and = 0
        alpha_or = 255

    # Allocate an uninitialized string.
    cdef unsigned char *null = NULL
    rv = null[:w*h*4]
    
    # Out is where we put the output.
    cdef unsigned char *out = rv
    
    # The pixels in the source image.
    cdef unsigned char *pixels = NULL
    cdef SDL_Surface *surf

    # Pointer to the current pixel.
    cdef unsigned char *p

    # Pointer to the current output pixel.
    cdef unsigned char *op
    
    # Pointer to the row end.
    cdef unsigned char *pend

    # alpha value.
    cdef unsigned int a

    # pixel pointer.
    cdef unsigned int *pp

    surf = PySurface_AsSurface(pysurf)
    pixels = <unsigned char *> surf.pixels

    pixels += y * surf.pitch
    pixels += x * 4

    op = out
    
    for y from 0 <= y < h:
        p = pixels + y * surf.pitch
        pend = p + w * 4

        while p < pend:
            a = (p[3] & alpha_and) | alpha_or

            op[0] = p[0] * a / 255
            op[1] = p[1] * a / 255
            op[2] = p[2] * a / 255
            op[3] = a
            
            p += 4
            op += 4

    if border_left:
        pp = <unsigned int *> (out)

        for y from 0 <= y < h:
            pp[0] = pp[1]
            pp += w

    if border_right:
        pp = <unsigned int *> (out)
        pp += w - 2
        
        for y from 0 <= y < h:
            pp[1] = pp[0]
            pp += w

    if border_top:
        pp = <unsigned int *> (out)

        for x from 0 <= x < w:
            pp[0] = pp[w]
            pp += 1

    if border_top:
        pp = <unsigned int *> (out)
        pp += (y - 2) * w

        for x from 0 <= x < w:
            pp[w] = pp[0]
            pp += 1
            
    return rv


def load_premultiplied(
    data, width, height, update, format, internalformat,
    ):

    cdef char *pixels

    if data:
        pixels = data
    else:
        pixels = NULL
    
    if update:
        glTexSubImage2D(
            GL_TEXTURE_2D,
            0,
            0,
            0,
            width,
            height,
            format,
            GL_UNSIGNED_BYTE,
            <GLubyte *> pixels)

    else:
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            internalformat,
            width,
            height,
            0,
            format,
            GL_UNSIGNED_BYTE,
            <GLubyte *> pixels)

cdef void draw_rectangle(
    double sx,
    double sy,
    double x,
    double y,
    double w,
    double h,
    render.Matrix2D transform,
    TextureCore tex0, float tex0x, float tex0y,
    TextureCore tex1, float tex1x, float tex1y,
    TextureCore tex2, float tex2x, float tex2y,
    ):

    """
    This draws a rectangle (textured with up to four textures) to the
    screen.

    Note that this is usually implemented in C code in the Ren'Py
    module, and that this version is for debugging.
    

    `sx`, `sy`
        The location in the untransformed screen coordinate of the
        upper-left corner of the drawing region. (Think of this as an
        offset that is applied to coordinates.)
    `x`, `y`
        The location in the transformed coordinates to draw the
        upper-left corner of the texture.
    `w`, `h`
        The width and height of texture.
    `tex0`
        The texture to bind to texture unit 0.
    `tex0x`, `tex0y`
        The coordinates within that texture of the upper-left corner.
    `tex1...`, `tex2...`
        Same, but for the other two textures.
    `toff_...`
        Texture offset to apply to the given side of the texture.
    """

    # Do we have the given texture?
    cdef int has_tex0, has_tex1, has_tex2

    # Texture coordinates.
    cdef double t0u0, t0v0, t0u1, t0v1
    cdef double t1u0, t1v0, t1u1, t1v1
    cdef double t2u0, t2v0, t2u1, t2v1    
    
    # Pull apart the transform.
    cdef double xdx = transform.xdx
    cdef double xdy = transform.xdy
    cdef double ydx = transform.ydx
    cdef double ydy = transform.ydy

    # Transform the vertex coordinates to screen-space.
    cdef double x0 = (x + 0) * xdx + (y + 0) * xdy + sx
    cdef double y0 = (x + 0) * ydx + (y + 0) * ydy + sy

    cdef double x1 = (x + w) * xdx + (y + 0) * xdy + sx
    cdef double y1 = (x + w) * ydx + (y + 0) * ydy + sy

    cdef double x2 = (x + 0) * xdx + (y + h) * xdy + sx
    cdef double y2 = (x + 0) * ydx + (y + h) * ydy + sy

    cdef double x3 = (x + w) * xdx + (y + h) * xdy + sx
    cdef double y3 = (x + w) * ydx + (y + h) * ydy + sy

    # Compute the texture coordinates, and set up the textures.
    cdef double xadd, yadd, xmul, ymul

    if tex0 is not None:

        has_tex0 = 1

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex0.number)
        
        xadd = tex0.xadd
        yadd = tex0.yadd
        xmul = tex0.xmul
        ymul = tex0.ymul
        
        t0u0 = xadd + xmul * (tex0x + 0)
        t0u1 = xadd + xmul * (tex0x + w)
        t0v0 = yadd + ymul * (tex0y + 0)
        t0v1 = yadd + ymul * (tex0y + h)

    else:
        has_tex0 = 0
    
    if tex1 is not None:

        has_tex1 = 1

        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, tex1.number)
        
        xadd = tex1.xadd
        yadd = tex1.yadd
        xmul = tex1.xmul
        ymul = tex1.ymul
        
        t1u0 = xadd + xmul * (tex1x + 0)
        t1u1 = xadd + xmul * (tex1x + w)
        t1v0 = yadd + ymul * (tex1y + 0)
        t1v1 = yadd + ymul * (tex1y + h)

    else:
        has_tex1 = 0

    if tex2 is not None:

        has_tex2 = 1

        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, tex2.number)
        
        xadd = tex2.xadd
        yadd = tex2.yadd
        xmul = tex2.xmul
        ymul = tex2.ymul
        
        t2u0 = xadd + xmul * (tex2x + 0)
        t2u1 = xadd + xmul * (tex2x + w)
        t2v0 = yadd + ymul * (tex2y + 0)
        t2v1 = yadd + ymul * (tex2y + h)

    else:
        has_tex2 = 0


    # Now, actually draw the textured rectangle.

    cdef GLfloat tex0coords[8]
    cdef GLfloat tex1coords[8]
    cdef GLfloat tex2coords[8]
    cdef GLfloat vcoords[8]

    if has_tex0:
        tex0coords[0] = t0u0
        tex0coords[1] = t0v0
        tex0coords[2] = t0u1
        tex0coords[3] = t0v0
        tex0coords[4] = t0u0
        tex0coords[5] = t0v1
        tex0coords[6] = t0u1
        tex0coords[7] = t0v1

        glClientActiveTexture(GL_TEXTURE0)
        glTexCoordPointer(2, GL_FLOAT, 0, <GLubyte *> tex0coords)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    else:
        glClientActiveTexture(GL_TEXTURE0)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

       
    if has_tex1:
        tex1coords[0] = t1u0
        tex1coords[1] = t1v0
        tex1coords[2] = t1u1
        tex1coords[3] = t1v0
        tex1coords[4] = t1u0
        tex1coords[5] = t1v1
        tex1coords[6] = t1u1
        tex1coords[7] = t1v1

        glClientActiveTexture(GL_TEXTURE1)
        glTexCoordPointer(2, GL_FLOAT, 0, <GLubyte *> tex1coords)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    else:
        glClientActiveTexture(GL_TEXTURE1)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)


    if has_tex2:
        tex2coords[0] = t2u0
        tex2coords[1] = t2v0
        tex2coords[2] = t2u1
        tex2coords[3] = t2v0
        tex2coords[4] = t2u0
        tex2coords[5] = t2v1
        tex2coords[6] = t2u1
        tex2coords[7] = t2v1

        glClientActiveTexture(GL_TEXTURE2)
        glTexCoordPointer(2, GL_FLOAT, 0, <GLubyte *> tex2coords)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    else:
        glClientActiveTexture(GL_TEXTURE2)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

    vcoords[0] = x0
    vcoords[1] = y0
    vcoords[2] = x1
    vcoords[3] = y1
    vcoords[4] = x2
    vcoords[5] = y2
    vcoords[6] = x3
    vcoords[7] = y3

    glVertexPointer(2, GL_FLOAT, 0, <GLubyte *> vcoords)
    glEnableClientState(GL_VERTEX_ARRAY)    
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
