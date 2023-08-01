#@PydevCodeAnalysisIgnore
# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

from sdl2 cimport *
from pygame_sdl2 cimport *
import_pygame_sdl2()

from freetype cimport *
from ttgsubtable cimport *
from renpy.text.textsupport cimport Glyph, SPLIT_INSTEAD
import traceback
import sys

import renpy.config

cdef extern from "ftsupport.h":
    char *freetype_error_to_string(int error)

cdef extern from "hb.h":

    ctypedef int hb_bool_t

    enum hb_direction_t:
        HB_DIRECTION_INVALID
        HB_DIRECTION_LTR
        HB_DIRECTION_RTL
        HB_DIRECTION_TTB
        HB_DIRECTION_BTT

    ctypedef unsigned int hb_codepoint_t

    ctypedef void (*hb_destroy_func_t)(void *)
    ctypedef int hb_position_t

    # hb-buffer
    struct hb_glyph_info_t:
        hb_codepoint_t codepoint;
        uint32_t       cluster;

    struct hb_glyph_position_t:
        hb_position_t  x_advance
        hb_position_t  y_advance
        hb_position_t  x_offset
        hb_position_t  y_offset

    struct hb_buffer_t

    hb_buffer_t *hb_buffer_create()

    void hb_buffer_reset(hb_buffer_t *)

    void hb_buffer_destroy(hb_buffer_t *)

    void hb_buffer_add_utf8 (
        hb_buffer_t *buffer,
        const char *text,
        int text_length,
        unsigned int item_offset,
        int item_length)

    void hb_buffer_add_utf32 (hb_buffer_t *buffer,
        const uint32_t *text,
        int text_length,
        unsigned int item_offset,
        int item_length)

    void hb_buffer_set_direction (hb_buffer_t *buffer, hb_direction_t direction)
    void hb_buffer_guess_segment_properties(hb_buffer_t *buffer)

    hb_glyph_info_t *hb_buffer_get_glyph_infos (hb_buffer_t *buffer, unsigned int *length);
    hb_glyph_position_t *hb_buffer_get_glyph_positions (hb_buffer_t *buffer, unsigned int *length);
    
    enum hb_buffer_cluster_level_t:
        HB_BUFFER_CLUSTER_LEVEL_MONOTONE_GRAPHEMES
        HB_BUFFER_CLUSTER_LEVEL_MONOTONE_CHARACTERS
        HB_BUFFER_CLUSTER_LEVEL_CHARACTERS
        HB_BUFFER_CLUSTER_LEVEL_DEFAULT

    void hb_buffer_set_cluster_level(hb_buffer_t *buffer, hb_buffer_cluster_level_t cluster_level)

    # hb-font
    struct hb_font_t

    void hb_font_destroy(hb_font_t *)

    struct hb_feature_t

    void hb_font_set_scale(hb_font_t *font, int x_scale, int y_scale)

    # hb-shape
    void hb_shape (
        hb_font_t *font,
        hb_buffer_t *buffer,
        const hb_feature_t *features,
        unsigned int num_features);
    


cdef extern from "hb-ft.h":
    hb_font_t *hb_ft_font_create(FT_Face ft_face, hb_destroy_func_t *destroy)
    hb_bool_t hb_ft_font_changed(hb_font_t *font)
    void hb_ft_font_set_funcs(hb_font_t *font)
    void hb_ft_font_set_load_flags (hb_font_t *font, int load_flags)


# The freetype library object we use.
cdef FT_Library library

# Represents a cached glyph.
cdef struct glyph_cache:

    # The character we're caching. -1 if we're not representing a valid
    # character.
    int index

    int width
    float advance

    FT_Bitmap bitmap
    int bitmap_left
    int bitmap_top


class FreetypeError(Exception):
    def __init__(self, code):
        Exception.__init__(self, "%d: %s" % (code, freetype_error_to_string(code)))

def init():

    cdef int error

    error = FT_Init_FreeType(&library)
    if error:
        raise FreetypeError(error)

cdef bint is_vs(unsigned int char):
    if 0xfe00 <= char <= 0xfe0f: # VS1-16
        return True

    elif 0xe0100 <= char <= 0xe01ef: # VS17-256
        return True

    elif 0x180b <= char <= 0x180d: # FVS1-3
        return True

    return False

cdef bint is_zerowidth(unsigned int char):
    if char == 0x200b: # Zero-width space.
        return True

    if char == 0x200c: # Zero-width non-joiner.
        return True

    if char == 0x200d: # Zero-width joiner.
        return True

    if char == 0x2060: # Word joiner.
        return True

    if char == 0xfeff: # Zero width non-breaking space.
        return True

    if is_vs(char): # Variation sequences
        return True

    return False

cdef unsigned long io_func(FT_Stream stream, unsigned long offset, unsigned char *buffer, unsigned long count):
    """
    Seeks to offset, and then reads count bytes from the stream into buffer.
    """

    cdef FTFace face
    cdef char *cbuf
    cdef unsigned long i

    face = <FTFace> stream.descriptor.pointer
    f = face.f

    if face.offset != offset:

        try:
            f.seek(offset)
            face.offset = offset
        except Exception:
            traceback.print_exc()
            return -1

    if count != 0:
        try:
            buf = f.read(count)
            cbuf = buf
            count = len(buf)

            for i from 0 <= i < count:
                buffer[i] = cbuf[i]
        except Exception:
            traceback.print_exc()
            return -1

    face.offset += count

    return count

cdef void close_func(FT_Stream stream):
    """
    Close the stream.

    Currently does nothing, closing is taken care of at the Font
    object level.
    """

    return


cdef class FTFace:
    """
    Represents a freetype face.
    """

    cdef:
        FT_StreamRec stream
        FT_Open_Args open_args
        FT_Face face

        float size

        # The file the font is read from.
        object f

        # The offset in that file.
        unsigned long offset

        public object fn

    def __init__(self, f, index, fn):

        cdef int error
        cdef unsigned long size

        # The filename.
        self.fn = fn

        # The file that the font is opened from.
        self.f = f

        f.seek(0, 2)
        size = f.tell()
        f.seek(0, 0)

        # The offset within the stream we're currently at.
        self.offset = 0

        self.open_args.flags = FT_OPEN_STREAM
        self.open_args.stream = &self.stream

        self.stream.size = size
        self.stream.pos = 0
        self.stream.descriptor.pointer = <void *> self
        self.stream.read = io_func
        self.stream.close = close_func

        error = FT_Open_Face(library, &self.open_args, index, &self.face)
        if error:
            raise FreetypeError(error)

        error = FT_Select_Charmap(self.face, FT_ENCODING_UNICODE)
        if error:
            raise FreetypeError(error)

        # The size the face is at.
        self.size = -1

cdef class FTFont:

    cdef:

        FTFace face_object
        FT_Face face

        # A cache of various properties.
        float size
        float bold
        bint italic
        int outline
        bint antialias
        bint vertical

        # Information used to modify the font.

        # The offset and height of the underline.
        public int underline_offset
        public int underline_height

        # The stroker object.
        FT_Stroker stroker

        # The number of pixels the outlines are expanded by.
        public int expand

        # Basic Y-direction metrics for this font.
        public int ascent
        public int descent
        public int height
        public int lineskip

        glyph_cache cache[256]

        # Have we been setup at least once?
        bint has_setup

        # The hinting flag to use.
        int hinting

        # The font harfbuzz uses.
        hb_font_t *hb_font

    def __cinit__(self):
        for i from 0 <= i < 256:
            self.cache[i].index = -1
            FT_Bitmap_New(&(self.cache[i].bitmap))

    def __dealloc__(self):
        for i from 0 <= i < 256:
            FT_Bitmap_Done(library, &(self.cache[i].bitmap))

        if self.stroker != NULL:
            FT_Stroker_Done(self.stroker)


    def __init__(self, face, float size, float bold, bint italic, int outline, bint antialias, bint vertical, hinting):

        if size < 1:
            size = 1

        if bold:
            antialias = True

        size = size * renpy.config.ftfont_scale.get(face.fn, 1.0) * renpy.game.preferences.font_size

        self.face_object = face
        self.face = self.face_object.face

        self.size = size
        self.bold = bold
        self.italic = italic
        self.outline = outline
        self.antialias = antialias
        self.vertical = vertical

        if outline == 0:
            self.stroker = NULL;
            self.expand = 0

        else:
            FT_Stroker_New(library, &self.stroker)
            FT_Stroker_Set(self.stroker, outline * 64, FT_STROKER_LINECAP_ROUND, FT_STROKER_LINEJOIN_ROUND, 0)
            self.expand = outline * 2

        self.has_setup = False

        if hinting == "bytecode":
            self.hinting = FT_LOAD_NO_AUTOHINT
        elif hinting == "none" or hinting is None:
            self.hinting = FT_LOAD_NO_HINTING
        else:
            self.hinting = FT_LOAD_FORCE_AUTOHINT


        FT_Set_Char_Size(self.face_object.face, 0, <int> (self.size * 64), 0, 0)

        self.hb_font = hb_ft_font_create(self.face_object.face, NULL)
        hb_ft_font_set_funcs(self.hb_font)
        hb_font_set_scale(self.hb_font, <int> (self.size * 64), <int> (self.size * 64))
        hb_ft_font_set_load_flags(self.hb_font, self.hinting | FT_LOAD_COLOR)

    cdef setup(self):
        """
        Changes the parameters of the face to match this font.
        """

        cdef int error
        cdef FT_Face face
        cdef FT_Fixed scale
        cdef float ascent_scale

        face = self.face

        if self.face_object.size != self.size:
            self.face_object.size = self.size

            error = FT_Set_Char_Size(face, 0, <int> (self.size * 64), 0, 0)
            if error:
                raise FreetypeError(error)

            hb_ft_font_changed(self.hb_font)


        if not self.has_setup:

            self.has_setup = True

            scale = face.size.metrics.y_scale

            vextent_scale = renpy.config.ftfont_vertical_extent_scale.get(self.face_object.fn, 1.0)

            self.ascent = FT_CEIL(int(face.size.metrics.ascender * vextent_scale))
            self.descent = FT_FLOOR(int(face.size.metrics.descender * vextent_scale))

            if self.descent > 0:
                self.descent = -self.descent

            self.ascent += self.expand
            self.descent -= self.expand

            self.height = self.ascent - self.descent

            # This is probably more correct, but isn't what 6.12.1 did.
            # self.lineskip = FT_CEIL(face.size.metrics.height) + self.expand

            # if self.height > self.lineskip:
            #     self.lineskip = self.height

            self.lineskip = <int> self.height * renpy.game.preferences.font_line_spacing

            if self.vertical:
                self.underline_offset = FT_FLOOR(FT_MulFix(face.ascender + face.descender - face.underline_position, scale))
            else:
                self.underline_offset = FT_FLOOR(FT_MulFix(face.underline_position, scale))
            self.underline_height = FT_FLOOR(FT_MulFix(face.underline_thickness, scale))

            if self.underline_height < 1:
                self.underline_height = 1

            self.underline_height += self.expand

        return

    cdef glyph_cache *get_glyph(self, int index):
        """
        Returns the glyph_cache object for a given glyph.
        """

        cdef FT_Face face
        cdef FT_Glyph g
        cdef FT_BitmapGlyph bg
        cdef FT_Bitmap bitmap
        cdef FT_Matrix shear

        cdef int error
        cdef glyph_cache *rv
        cdef uint32_t vindex

        cdef int overhang
        cdef FT_Glyph_Metrics metrics

        cdef int x, y

        face = self.face

        rv = &(self.cache[index & 255])
        if rv.index == index:
            return rv

        rv.index = index

        error = FT_Load_Glyph(face, index, self.hinting | FT_LOAD_COLOR)
        if error:
            raise FreetypeError(error)

        g = NULL

        if face.glyph.format != FT_GLYPH_FORMAT_BITMAP:

            if not self.italic and not self.vertical and self.stroker == NULL:

                if self.antialias:
                    FT_Render_Glyph(face.glyph, FT_RENDER_MODE_NORMAL)
                else:
                    FT_Render_Glyph(face.glyph, FT_RENDER_MODE_MONO)

                bitmap = face.glyph.bitmap

                rv.bitmap_left = face.glyph.bitmap_left + self.expand // 2
                rv.bitmap_top = face.glyph.bitmap_top - self.expand // 2

            else:
                error = FT_Get_Glyph(face.glyph, &g)

                if error:
                    raise FreetypeError(error)

                if self.italic:
                    shear.xx = 1 << 16
                    shear.xy = (207 << 16) // 1000 # taken from SDL_ttf.
                    shear.yx = 0
                    shear.yy = 1 << 16

                    FT_Outline_Transform(&(<FT_OutlineGlyph> g).outline, &shear)

                if self.vertical:
                    metrics = face.glyph.metrics
                    # move the origin for vertical layout
                    # if self.vertical:
                    FT_Outline_Translate(&(<FT_OutlineGlyph> g).outline, metrics.vertBearingX - metrics.horiBearingX, -metrics.vertBearingY - metrics.horiBearingY)
                    # else:
                    #     FT_Outline_Translate(&(<FT_OutlineGlyph> g).outline, -metrics.horiAdvance // 2, -face.bbox.yMax)
                    shear.xx = 0
                    shear.xy = -(1 << 16)
                    shear.yx = 1 << 16
                    shear.yy = 0
                    FT_Outline_Transform(&(<FT_OutlineGlyph> g).outline, &shear)
                    # set vertical baseline to a half of the height
                    FT_Outline_Translate(&(<FT_OutlineGlyph> g).outline, 0, (face.bbox.yMax + face.bbox.yMin) // 2)

                if self.stroker != NULL:
                    # FT_Glyph_StrokeBorder(&g, self.stroker, 0, 1)
                    FT_Glyph_Stroke(&g, self.stroker, 1)

                if self.antialias:
                    FT_Glyph_To_Bitmap(&g, FT_RENDER_MODE_NORMAL, NULL, 1)
                else:
                    FT_Glyph_To_Bitmap(&g, FT_RENDER_MODE_MONO, NULL, 1)

                bg = <FT_BitmapGlyph> g
                bitmap = bg.bitmap

                rv.bitmap_left = bg.left + self.expand // 2
                rv.bitmap_top = bg.top - self.expand // 2

        else:

            bitmap = face.glyph.bitmap

            rv.bitmap_left = face.glyph.bitmap_left + self.expand // 2
            rv.bitmap_top = face.glyph.bitmap_top - self.expand // 2

        if bitmap.pixel_mode != FT_PIXEL_MODE_GRAY and bitmap.pixel_mode != FT_PIXEL_MODE_BGRA:
            FT_Bitmap_Convert(library, &(bitmap), &(rv.bitmap), 4)

            # Freetype gives us a bitmap where values range from 0 to 1.
            for y from 0 <= y < rv.bitmap.rows:
                for x from 0 <= x < rv.bitmap.width:
                    if rv.bitmap.buffer[ y * rv.bitmap.pitch + x ]:
                        rv.bitmap.buffer[ y * rv.bitmap.pitch + x ] = 255

        else:
            FT_Bitmap_Copy(library, &(bitmap), &(rv.bitmap))

        if self.bold:
            overhang = face.size.metrics.y_ppem // 10

            FT_Bitmap_Embolden(
                library,
                &(rv.bitmap),
                overhang << 6,
                0)

        else:
            overhang = 0

        rv.width = rv.bitmap.width + rv.bitmap_left

        if g != NULL:
            FT_Done_Glyph(g)

        return rv

    def glyphs(self, unicode s):
        """
        Sizes s, returning a list of Glyph objects.
        """

        cdef FT_Face face
        cdef list rv
        cdef int len_s
        cdef FT_ULong c, next_c, vs
        cdef FT_UInt index, next_index
        cdef int error
        cdef Glyph gl
        cdef FT_Vector kerning
        cdef int kern
        cdef float advance
        cdef int i
        cdef int vs_offset
        cdef glyph_cache *cache

        cdef float min_advance, next_min_advance

        cdef hb_buffer_t *hb
        cdef hb_glyph_info_t *glyph_info
        cdef hb_glyph_position_t *glyph_pos
        cdef unsigned int glyph_count

        self.setup()

        rv = [ ]

        # Start Harfbuzz

        hb = hb_buffer_create()
        utf32_s = s.encode("utf-32")

        hb_buffer_add_utf32(hb, <const uint32_t *> ((<const char *> utf32_s) + 4), len(s), 0, len(s));

        hb_buffer_set_direction(hb, HB_DIRECTION_LTR)
        hb_buffer_guess_segment_properties(hb)
        hb_buffer_set_cluster_level(hb, HB_BUFFER_CLUSTER_LEVEL_MONOTONE_CHARACTERS)

        hb_shape(self.hb_font, hb, NULL, 0)

        glyph_info = hb_buffer_get_glyph_infos(hb, &glyph_count);
        glyph_pos = hb_buffer_get_glyph_positions(hb, &glyph_count);

        face = self.face
        g = face.glyph

        for 0 <= i < glyph_count:
            # print(
            #     repr(s[glyph_info[i].cluster]),
            #     glyph_info[i].codepoint,
            #     glyph_info[i].cluster,
            #     glyph_pos[i].x_advance / 64,
            #     # glyph_pos[i].y_advance,
            #     glyph_pos[i].x_offset / 64,
            #     # glyph_pos[i].y_offset,
            # )

            cache = self.get_glyph(index)

            gl = Glyph.__new__(Glyph)

            gl.character = ord(s[glyph_info[i].cluster])
            gl.glyph = glyph_info[i].codepoint

            gl.ascent = self.ascent
            gl.width = 0
            gl.line_spacing = self.lineskip
            gl.draw = True

            gl.x_offset = glyph_pos[i].x_offset / 64.0
            gl.y_offset = glyph_pos[i].y_offset / 64.0

            if self.vertical:
                gl.advance = glyph_pos[i].y_advance / 64.0
            else:
                gl.advance = glyph_pos[i].x_advance / 64.0

            rv.append(gl)

        hb_buffer_destroy(hb)

        return rv

    def bounds(self, glyphs, bounds):
        """
        Given a list of glyphs, get the intersection of bounds and the area where the glyphs
        will be drawn to. (Not including any offsets or expansions.)

        Returns an x, y, w, h tuple.
        """

        cdef Glyph glyph

        cdef FT_Face face
        cdef FT_GlyphSlot g
        cdef FT_UInt index

        cdef int bmx
        cdef int bmy

        cdef int x, y, w, h

        x, y, w, h = bounds

        face = self.face

        self.setup()

        for glyph in glyphs:

            if glyph.split == SPLIT_INSTEAD:
                continue

            if glyph.character == 0x200b:
                continue

            if glyph.variation == 0:
                index = FT_Get_Char_Index(face, glyph.character)
            else:
                index = FT_Face_GetCharVariantIndex(face, glyph.character, glyph.variation)

            cache = self.get_glyph(index)

            bmx = <int> (glyph.x + .5) + cache.bitmap_left
            bmy = glyph.y - cache.bitmap_top

            if bmx < x:
                x = bmx

            if bmy < y:
                y = bmy

            if bmx + <int> cache.bitmap.width > w:
                w = bmx + cache.bitmap.width

            if bmy + <int> cache.bitmap.rows > h:
                h = bmy + cache.bitmap.rows

        return x, y, w, h

    def draw(self, pysurf, float xo, int yo, color, list glyphs, int underline, bint strikethrough, black_color):
        """
        Draws a list of glyphs to surf, with the baseline starting at x, y.
        """

        cdef SDL_Surface *surf
        cdef unsigned int Sr, Sb, Sg, Sa
        cdef unsigned int Dr, Db, Dg, Da
        cdef unsigned int Gr, Gb, Gg, Ga
        cdef unsigned int rshift, gshift, bshift, ashift
        cdef unsigned int fixed
        cdef unsigned int alpha
        cdef Glyph glyph

        cdef FT_Face face
        cdef FT_GlyphSlot g
        cdef FT_UInt index
        cdef int error
        cdef int bmx, bmy, px, py, pxstart
        cdef int ly, lh, rows, width
        cdef int underline_x, underline_end, expand
        cdef int x, y

        cdef unsigned char *pixels
        cdef unsigned char *line
        cdef unsigned char *gline
        cdef int pitch
        cdef glyph_cache *cache

        Sr, Sg, Sb, Sa = color

        if Sa == 0:
            return

        self.setup()

        surf = PySurface_AsSurface(pysurf)
        pixels = <unsigned char *> surf.pixels
        pitch = surf.pitch

        face = self.face
        g = face.glyph

        expand = self.expand

        for glyph in glyphs:

            if glyph.split == SPLIT_INSTEAD:
                continue

            x = <int> (glyph.x + xo)
            y = <int> (glyph.y + yo)

            underline_x = x - glyph.delta_x_offset
            underline_end = x + <int> glyph.advance + expand

            cache = self.get_glyph(glyph.glyph)

            # with nogil used to be here, but it slowed things down.

            bmx = <int> (x + .5) + cache.bitmap_left
            bmy = y - cache.bitmap_top

            if bmx < 0:
                pxstart = -bmx
                bmx = 0
            else:
                pxstart = 0

            rows = min(cache.bitmap.rows, surf.h - bmy)
            width = min(cache.bitmap.width, surf.w - bmx)

            underline_end = min(underline_end, surf.w - 1)

            if glyph.draw:

                if cache.bitmap.pixel_mode == FT_PIXEL_MODE_BGRA:

                    for py from 0 <= py < rows:

                        if bmy < 0:
                            bmy += 1
                            continue

                        line = pixels + bmy * pitch + bmx * 4
                        gline = cache.bitmap.buffer + py * cache.bitmap.pitch + pxstart

                        for px from 0 <= px < width:

                            Gb = gline[0]
                            Gg = gline[1]
                            Gr = gline[2]
                            Ga = gline[3]

                            line[0] = line[0] * (1 - Ga) // 255 + Gr
                            line[1] = line[1] * (1 - Ga) // 255 + Gg
                            line[2] = line[2] * (1 - Ga) // 255 + Gb
                            line[3] = line[3] * (1 - Ga) // 255 + Ga

                            gline += 4
                            line += 4

                        bmy += 1

                else:

                    for py from 0 <= py < rows:

                        if bmy < 0:
                            bmy += 1
                            continue

                        line = pixels + bmy * pitch + bmx * 4
                        gline = cache.bitmap.buffer + py * cache.bitmap.pitch + pxstart

                        for px from 0 <= px < width:

                            alpha = gline[0]

                            # Modulate Sa by the glyph's alpha.

                            alpha = (alpha * Sa + Sa) >> 8

                            # Only draw if we increase the alpha - a cheap way to
                            # allow overlapping characters.

                            if alpha == 255:
                                line[0] = Sr
                                line[1] = Sg
                                line[2] = Sb
                                line[3] = alpha

                            elif alpha:

                                line[0] = (line[0] * (1 - alpha) + Sr * alpha) // 255
                                line[1] = (line[1] * (1 - alpha) + Sg * alpha) // 255
                                line[2] = (line[2] * (1 - alpha) + Sb * alpha) // 255
                                line[3] = line[3] * (1 - alpha) // 255 + alpha

                            gline += 1
                            line += 4

                        bmy += 1

            # Underlining.
            if underline:

                ly = y - self.underline_offset - 1
                lh = self.underline_height * underline

                for py from ly <= py < min(ly + lh, surf.h):
                    for px from underline_x <= px < underline_end:
                        line = pixels + py * pitch + px * 4

                        line[0] = Sr
                        line[1] = Sg
                        line[2] = Sb
                        line[3] = Sa

            # Strikethrough.
            if strikethrough:
                ly = y - self.ascent + self.height // 2
                lh = self.height // 10
                if lh < 1:
                    lh = 1

                for py from ly <= py < (ly + lh):
                    for px from underline_x <= px < underline_end:
                        line = pixels + py * pitch + px * 4

                        line[0] = Sr
                        line[1] = Sg
                        line[2] = Sb
                        line[3] = Sa
