#@PydevCodeAnalysisIgnore
#cython: profile=False
# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function

DEF ANGLE = False

from uguugl cimport *
from gl2draw cimport *

from sdl2 cimport *
from pygame_sdl2 cimport *
import_pygame_sdl2()

from cpython.string cimport PyString_FromStringAndSize
from libc.stdlib cimport calloc, free

import sys
import time
import collections
import renpy

# The maximum size of a texture.
MAX_SIZE = 4096

# A list of texture number allocated.
texture_numbers = set()

# The texture generation.
generation = 1

# A map from texture number to generation
texture_generation = { }

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
        self.number = 0

        # The format of this texture in the GPU (or 0 if not known).
        self.loaded = False

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
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

            self.nearest = False

            # If we haven't initialized the texture yet, and we're
            # smaller than it, load in the empty texture.
            if w < self.width or h < self.height:

                if not self.loaded:
                    load_premultiplied(
                        None,
                        self.width,
                        self.height,
                        0,
                        False,
                        )

            # Otherwise, either load or replace the texture.
            load_premultiplied(
                self.premult,
                w,
                h,
                self.loaded,
                False,
                )

            self.loaded = True

            # Finally, load in the default math.
            self.xadd = self.yadd = 0
            self.xmul = 1.0 / self.width
            self.ymul = 1.0 / self.height

            # We don't need to be loaded anymore.
            self.premult = None
            self.premult_size = None


    def render_to(self, x, y, draw_func, rtt, environ):

        self.allocate()

        if not self.loaded:

            glBindTexture(GL_TEXTURE_2D, self.number)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

            self.nearest = False

            load_premultiplied(
                None,
                self.width,
                self.height,
                0,
                True)

            self.loaded = True

        rtt.render(environ, self.number, x, y, self.width, self.height, draw_func)

        self.xadd = 0
        self.yadd = 0
        self.xmul = 1.0 / self.width
        self.ymul = 1.0 / self.height

    cpdef int allocate(self):
        """
        This allocates a texture number, if necessary.
        """

        global total_texture_size
        global texture_count

        cdef unsigned int texnums[1]

        if self.number != 0:
            return 0

        glGenTextures(1, texnums)

        self.number = texnums[0]
        self.loaded = False

        texture_generation[self.number] = generation

        texture_numbers.add(texnums[0])

        total_texture_size += self.width * self.height * 4
        texture_count += 1

        return 0

    def deallocate(self):
        """
        Deallocates this texture. The texture must have been removed from a
        free list before this is called.
        """

        global total_texture_size
        global texture_count

        if self.number == 0:
            return

        cdef GLuint texnums[1]

        texnums[0] = self.number

        if texture_generation[self.number] == self.generation:
            glDeleteTextures(1, texnums)

        self.number = 0

        texture_numbers.discard(self.number)
        total_texture_size -= self.width * self.height * 4
        texture_count -= 1


class Texture(TextureCore):
    """
    We need to be a real python class, not a C extension, to ensure that
    the __del__ method is called.
    """

    def __sizeof__(self):
        return TextureCore.__sizeof__(self) + self.width * self.height * 4

    def __getstate__(self):
        if renpy.config.developer:
            raise Exception("Can't pickle a texture.")
        else:
            return { }

    def __setstate__(self, state):
        return


# A list of NPOT textures that need to be freed.
npot_free_textures = [ ]

# The number of textues that have been allocated but not deallocated.
texture_count = 0

# The total size (in bytes) of all the textures that have been allocated
# but not deallocated.
total_texture_size = 0

# This allocates a texture, either from the free list, or by asking
# gl.
def alloc_texture(width, height):
    """
    Allocate a texture, either from the freelist or by asking GL. The
    returned texture has a reference count of 1.
    """

    rv = Texture(width, height)
    rv.free_list = npot_free_textures
    rv.generation = generation
    return rv



def dealloc_textures():
    cdef GLuint texnums[1]

    for i in npot_free_textures:
        i.deallocate()

    npot_free_textures[:] = [ ]

    # Do not reset texture numbers - we don't want to reuse a number that's
    # in use, only to have it deallocated later.

    global generation
    generation += 1



def cleanup():
    """
    This is called once per frame.
    """

    # If we have more than one of a texture size, deallocate the last one of
    # that size. This prevents us from leaking memory via textures, while
    # making it unlikely we'll constantly allocate/deallocate textures.

    for i in npot_free_textures:
        i.deallocate()

    npot_free_textures[:] = [ ]

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

    def __init__(self, width, height): #@DuplicatedSignature

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

        # Has the texture been made ready once?
        self.ready = False

    def __getstate__(self): #@DuplicatedSignature
        if renpy.config.developer:
            raise Exception("Can't pickle a texture.")
        else:
            return { }

    def __setstate__(self, state): #@DuplicatedSignature
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


    cpdef void make_ready(self, bint nearest):
        """
        Makes ready all the tile-textures in this texture grid.
        """

        cdef list row
        cdef TextureCore t

        self.ready = True

        for row in self.tiles:
            for t in row:
                t.make_ready()

                if nearest:
                    t.make_nearest()
                else:
                    t.make_linear()



# This is a cache from (width, size) to the results of compute_tiling.
tiling_cache = { }

def compute_tiling(width, max_size):
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

    max_size = min(MAX_SIZE, max_size)

    orig_width = width

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

    if width <= max_size:
        left_border = 0
        right_border = 0
    else:
        left_border = 1
        right_border = 1

    while width:

        size = min(width + left_border + right_border, max_size)

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


def texture_grid_from_surface(surf, transient):
    """
    This takes a Surface and turns it into a TextureGrid.
    """

    max_size = MAX_SIZE

    width, height = surf.get_size()

    rv = TextureGrid(width, height)

    rv.columns, texcolumns = compute_tiling(width, max_size)
    rv.rows, texrows = compute_tiling(height, max_size)

    for rv_row, texrow in zip(rv.rows, texrows):
        border_top, _, border_bottom = rv_row
        y, height, texheight = texrow

        row = [ ]

        colnum = 0

        for rv_col, texcol in zip(rv.columns, texcolumns):
            border_left, _, border_right = rv_col
            x, width, texwidth = texcol

            tex = alloc_texture(texwidth, texheight)
            tex.load_surface(surf, x, y, width, height,
                             border_left, border_top, border_right, border_bottom)

            row.append(tex)

        rv.tiles.append(row)

    return rv


def texture_grid_from_drawing(width, height, draw_func, rtt, environ):
    """
    This creates a texture grid of `width` by `height` by using
    draw_func to draw to the screen.
    """

    rv = TextureGrid(width, height)

    gldraw = renpy.display.draw
    pwidth, pheight = gldraw.physical_size

    rv.columns, texcolumns = compute_tiling(width, rtt.get_size_limit(pwidth))
    rv.rows, texrows = compute_tiling(height, rtt.get_size_limit(pheight))

    for y, height, texheight in texrows:
        row = [ ]

        for x, width, texwidth in texcolumns:

            tex = alloc_texture(texwidth, texheight)
            tex.render_to(x, y, draw_func, rtt, environ)

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

    # If we have an empty list, do nothing.
    for i in args:
        if not i:
            return rv

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




def premultiply(
    object pysurf,
    int x,
    int y,
    int w,
    int h,
    bint border_left, bint border_top, bint border_right, bint border_bottom):

    """
    Creates a string containing the premultiplied image data for
    for the (x, y, w, h) box inside pysurf. The various border_
    parameters control the addition of a border on the sides.
    """

    # Iterator y and x.
    cdef int ix, iy

    # Does the original image have an alpha channel?
    cdef unsigned int alpha

    if pysurf.get_masks()[3]:
        alpha = True
    else:
        alpha = False

    # Allocate an uninitialized string.
    rv = PyString_FromStringAndSize(<char *>NULL, w * h * 4)

    # Out is where we put the output.
    cdef unsigned char *out = rv

    # The pixels in the source image.
    cdef unsigned char *pixels
    cdef unsigned char *pixels_end

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
    cdef unsigned int *ppend

    surf = PySurface_AsSurface(pysurf)
    pixels = <unsigned char *> surf.pixels

    # The start of the pixel data to read out.
    pixels += y * surf.pitch
    pixels += x * 4

    # A pointer to the row past the last pixel data we read out.
    pixels_end = pixels + h * surf.pitch

    # A pointer to the output byte to write.
    op = out

    with nogil:

        while pixels < pixels_end:

            # The start and end of the current row.
            p = pixels
            pend = p + w * 4

            # Advance to the next row.
            pixels += surf.pitch

            if alpha:

                while p < pend:

                    a = p[3]

                    op[0] = (p[0] * a + a) >> 8
                    op[1] = (p[1] * a + a) >> 8
                    op[2] = (p[2] * a + a) >> 8
                    op[3] = a

                    p += 4
                    op += 4

            else:

                while p < pend:

                    (<unsigned int *> op)[0] = (<unsigned int *> p)[0]
                    op[3] = 255

                    p += 4
                    op += 4

        if border_left:
            pp = <unsigned int *> (out)
            ppend = pp + w * h

            while pp < ppend:
                pp[0] = pp[1]
                pp += w

        if border_right:
            pp = <unsigned int *> (out)
            pp += w - 2
            ppend = pp + w * h

            while pp < ppend:
                pp[1] = pp[0]
                pp += w

        if border_top:
            pp = <unsigned int *> (out)
            ppend = pp + w

            while pp < ppend:
                pp[0] = pp[w]
                pp += 1

        if border_bottom:
            pp = <unsigned int *> (out)
            pp += (h - 2) * w
            ppend = pp + w

            while pp < ppend:
                pp[w] = pp[0]
                pp += 1

    return rv


def load_premultiplied(data, width, height, update, rtt):

    cdef char *pixels

    cdef GLenum internalformat
    cdef GLenum format
    cdef GLenum type

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
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            <GLubyte *> pixels)

    else:
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            <GLubyte *> pixels)

