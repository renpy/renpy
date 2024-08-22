#@PydevCodeAnalysisIgnore
# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

    # hb-face
    struct hb_face_t

    void hb_face_destroy(hb_face_t *)

    # hb-font
    struct hb_font_t

    void hb_font_destroy(hb_font_t *)

    struct hb_feature_t

    void hb_font_set_scale(hb_font_t *font, int x_scale, int y_scale)
    void hb_font_set_synthetic_slant(hb_font_t *font, float slant)

    struct hb_glyph_extents_t:
        hb_position_t x_bearing
        hb_position_t y_bearing
        hb_position_t width
        hb_position_t height

    void hb_font_get_glyph_advance_for_direction(hb_font_t *font, hb_codepoint_t glyph, hb_direction_t direction, hb_position_t *x, hb_position_t *y)
    void hb_font_get_glyph_extents_for_origin(hb_font_t *font, hb_codepoint_t glyph, hb_position_t *x, hb_position_t *y, hb_glyph_extents_t *extents)

    # hb-shape
    void hb_shape (
        hb_font_t *font,
        hb_buffer_t *buffer,
        const hb_feature_t *features,
        unsigned int num_features);


cdef extern from "hb-ft.h":
    hb_face_t *hb_ft_face_create(FT_Face ft_face, hb_destroy_func_t *destroy)
    hb_font_t *hb_ft_font_create(FT_Face ft_face, hb_destroy_func_t *destroy)
    hb_bool_t hb_ft_font_changed(hb_font_t *font)
    void hb_ft_font_set_funcs(hb_font_t *font)
    void hb_ft_font_set_load_flags (hb_font_t *font, int load_flags)


cdef extern from "hb-ot.h":
    ctypedef unsigned int hb_ot_name_id_t
    struct hb_language_impl_t
    ctypedef const hb_language_impl_t *hb_language_t

    unsigned int hb_ot_name_get_utf8 (hb_face_t *face,
                     hb_ot_name_id_t name_id,
                     hb_language_t language,
                     unsigned int *text_size,
                     char *text)

    ctypedef enum hb_ot_metrics_tag_t:
        HB_OT_METRICS_TAG_HORIZONTAL_ASCENDER
        HB_OT_METRICS_TAG_HORIZONTAL_DESCENDER
        HB_OT_METRICS_TAG_HORIZONTAL_LINE_GAP
        HB_OT_METRICS_TAG_HORIZONTAL_CLIPPING_ASCENT
        HB_OT_METRICS_TAG_HORIZONTAL_CLIPPING_DESCENT
        HB_OT_METRICS_TAG_VERTICAL_ASCENDER
        HB_OT_METRICS_TAG_VERTICAL_DESCENDER
        HB_OT_METRICS_TAG_VERTICAL_LINE_GAP
        HB_OT_METRICS_TAG_HORIZONTAL_CARET_RISE
        HB_OT_METRICS_TAG_HORIZONTAL_CARET_RUN
        HB_OT_METRICS_TAG_HORIZONTAL_CARET_OFFSET
        HB_OT_METRICS_TAG_VERTICAL_CARET_RISE
        HB_OT_METRICS_TAG_VERTICAL_CARET_RUN
        HB_OT_METRICS_TAG_VERTICAL_CARET_OFFSET
        HB_OT_METRICS_TAG_X_HEIGHT
        HB_OT_METRICS_TAG_CAP_HEIGHT
        HB_OT_METRICS_TAG_SUBSCRIPT_EM_X_SIZE
        HB_OT_METRICS_TAG_SUBSCRIPT_EM_Y_SIZE
        HB_OT_METRICS_TAG_SUBSCRIPT_EM_X_OFFSET
        HB_OT_METRICS_TAG_SUBSCRIPT_EM_Y_OFFSET
        HB_OT_METRICS_TAG_SUPERSCRIPT_EM_X_SIZE
        HB_OT_METRICS_TAG_SUPERSCRIPT_EM_Y_SIZE
        HB_OT_METRICS_TAG_SUPERSCRIPT_EM_X_OFFSET
        HB_OT_METRICS_TAG_SUPERSCRIPT_EM_Y_OFFSET
        HB_OT_METRICS_TAG_STRIKEOUT_SIZE
        HB_OT_METRICS_TAG_STRIKEOUT_OFFSET
        HB_OT_METRICS_TAG_UNDERLINE_SIZE
        HB_OT_METRICS_TAG_UNDERLINE_OFFSET

    void hb_ot_metrics_get_position_with_fallback (hb_font_t *font, hb_ot_metrics_tag_t metrics_tag, hb_position_t *position)


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

    cdef HBFace face
    cdef char *cbuf
    cdef unsigned long i

    face = <HBFace> stream.descriptor.pointer
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

class Axis:
    """
    Represents an axis in a variable font.
    """

    def __init__(self, index, minimum, default, maximum):
        self.index = index
        self.minimum = minimum
        self.default = default
        self.maximum = maximum

    def __repr__(self):
        return "<Axis index={self.index} minimum={self.minimum} default={self.default} maximum={self.maximum}>".format(self=self)


class Variations:
    """
    Represents the variations of a font.
    """

    # Ensure this isn't shortened by the console.
    _console_always_long = True

    def __init__(self):
        # A map fron a named instance name to its index.
        self.instance = { }

        # A map from an axis name to its Axis object.
        self.axis = { }

    def __repr__(self):
        rv = [ ]

        for k in self.instance:
            rv.append("  Named Instance: " + repr(k))

        for k, v in self.axis.items():
            rv.append("  Axis: " + repr(k) + " (minimum={}, default={}, maximum={})".format(v.minimum, v.default, v.maximum))

        return "\n".join(rv)


cdef class HBFace:
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

        # The basic info about variations.
        FT_MM_Var *mm_var

        # Information about the variations, in Python.
        public object variations

        # Used to keep from switching instance and axis when not
        # required.
        public object current_instance
        public object current_axis

    def __dealloc__(self):
        if self.mm_var:
            FT_Done_MM_Var(library, self.mm_var)

    def __init__(self, f, index, fn):

        cdef int error
        cdef unsigned long size
        cdef hb_face_t *hb_face

        cdef char text[256]
        cdef unsigned int text_length

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

        # Variations.
        self.mm_var = NULL
        self.variations = None

        rv = FT_Get_MM_Var(self.face, &(self.mm_var))
        if rv == 0:

            self.variations = Variations()

            hb_face = hb_ft_face_create(self.face, NULL)

            for 0 <= i < self.mm_var.num_axis:
                if i >= 16:
                    continue

                self.variations.axis[self.mm_var.axis[i].name.decode("utf-8").lower()] = Axis(
                    i,
                    self.mm_var.axis[i].minimum / 65536.0,
                    self.mm_var.axis[i].default / 65536.0,
                    self.mm_var.axis[i].maximum / 65536.0,
                )

            for 0 < i < self.mm_var.num_namedstyles:
                text_length = 256
                if hb_ot_name_get_utf8(hb_face, self.mm_var.namedstyle[i].strid, NULL, &text_length, text):
                    self.variations.instance[text[0:text_length].decode("utf-8").lower()] = i

            hb_face_destroy(hb_face)


cdef class HBFont:

    cdef:

        HBFace face_object
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

        # For a variable font, the instance to use.
        object instance

        # For a variable font, the values for all non-default axes.
        object axis


    def __cinit__(self):
        for i from 0 <= i < 256:
            self.cache[i].index = -1
            FT_Bitmap_New(&(self.cache[i].bitmap))

    def __dealloc__(self):
        for i from 0 <= i < 256:
            FT_Bitmap_Done(library, &(self.cache[i].bitmap))

        if self.stroker != NULL:
            FT_Stroker_Done(self.stroker)

        if self.hb_font:
            hb_font_destroy(self.hb_font)

    def __init__(self, face, float size, float bold, bint italic, int outline, bint antialias, bint vertical, hinting, instance, axis):

        self.face_object = face
        self.face = self.face_object.face

        if size < 1:
            size = 1

        if instance is None and face.variations:
            if bold >= 1.0:
                if "bold" in face.variations.instance:
                    bold = 0.0
                    instance = "bold"
                elif "bold italic" in face.variations.instance:
                    bold = 0.0
                    instance = "bold italic"
            else:
                if "regular" in face.variations.instance:
                    instance = "regular"
                elif "italic" in face.variations.instance:
                    instance = "italic"

        if bold:
            antialias = True

        self.instance = instance
        self.axis = axis

        size = size * renpy.config.ftfont_scale.get(face.fn, 1.0) * renpy.game.preferences.font_size

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

        if hinting == "none" or hinting is None:
            self.hinting = FT_LOAD_NO_HINTING | FT_LOAD_TARGET_NORMAL
        elif hinting == "bytecode":
            self.hinting = FT_LOAD_NO_AUTOHINT | FT_LOAD_TARGET_NORMAL
        elif hinting == "auto-light":
            self.hinting = FT_LOAD_FORCE_AUTOHINT | FT_LOAD_TARGET_LIGHT
        elif hinting == "auto":
            self.hinting = FT_LOAD_FORCE_AUTOHINT | FT_LOAD_TARGET_NORMAL
        else:
            self.hinting = FT_LOAD_FORCE_AUTOHINT | FT_LOAD_TARGET_NORMAL

        FT_Set_Char_Size(self.face_object.face, 0, <int> (self.size * 64), 0, 0)


    cdef setup_variations(self):
        cdef FT_Fixed coords[16]

        fo = self.face_object
        axis = self.axis
        instance = self.instance
        variations = fo.variations

        if axis == fo.current_axis and instance == fo.current_instance:
            return

        fo.current_axis = axis
        fo.current_instance = instance

        # If we have a known instance, use it.

        if instance and instance.lower() in variations.instance:
            index = variations.instance[instance.lower()]
            for 0 <= i < min(fo.mm_var.num_axis, 16):
                coords[i] = fo.mm_var.namedstyle[index].coords[i]

        else:

            # Otherwise, use per-axis defaults.

            for k, v in variations.axis.items():
                coords[v.index] = int(v.default * 65536 + 1)

        if axis:

            # If we have per-axis information, use that.

            for k, value in axis.items():

                k = k.lower()
                if k in variations.axis:
                    ax = variations.axis[k]

                    if ax.index >= 16:
                        continue

                    if value < ax.minimum:
                        value = ax.minimum
                    elif value > ax.maximum:
                        value = ax.maximum

                    coords[ax.index] = int(value * 65536)

        FT_Set_Var_Design_Coordinates(self.face, min(fo.mm_var.num_axis, 16), coords)

    cdef setup(self):
        """
        Changes the parameters of the face to match this font.
        """

        cdef int error
        cdef FT_Face face
        cdef float ascent_scale

        cdef hb_position_t horizontal_ascender
        cdef hb_position_t horizontal_descender
        cdef hb_position_t horizontal_line_gap

        cdef hb_position_t vertical_ascender
        cdef hb_position_t vertical_descender
        cdef hb_position_t vertical_line_gap

        cdef hb_position_t underline_offset
        cdef hb_position_t underline_size

        face = self.face

        if self.face_object.variations:
            self.setup_variations()

        if self.face_object.size != self.size:
            self.face_object.size = self.size

            error = FT_Set_Char_Size(face, 0, <int> (self.size * 64), 0, 0)
            if error:
                raise FreetypeError(error)

        if not self.has_setup:

            self.has_setup = True

            self.hb_font = hb_ft_font_create(self.face_object.face, NULL)

            hb_ft_font_set_funcs(self.hb_font)

            hb_font_set_scale(self.hb_font, <int> (self.size * 64), <int> (self.size * 64))

            if self.italic:
                hb_font_set_synthetic_slant(self.hb_font, .207)

            hb_ft_font_set_load_flags(self.hb_font, self.hinting | FT_LOAD_COLOR)

            # Get the metrics.
            hb_ot_metrics_get_position_with_fallback(self.hb_font, HB_OT_METRICS_TAG_HORIZONTAL_ASCENDER, &horizontal_ascender)
            hb_ot_metrics_get_position_with_fallback(self.hb_font, HB_OT_METRICS_TAG_HORIZONTAL_DESCENDER, &horizontal_descender)

            hb_ot_metrics_get_position_with_fallback(self.hb_font, HB_OT_METRICS_TAG_VERTICAL_ASCENDER, &vertical_ascender)
            hb_ot_metrics_get_position_with_fallback(self.hb_font, HB_OT_METRICS_TAG_VERTICAL_DESCENDER, &vertical_descender)

            hb_ot_metrics_get_position_with_fallback(self.hb_font, HB_OT_METRICS_TAG_UNDERLINE_OFFSET, &underline_offset)
            hb_ot_metrics_get_position_with_fallback(self.hb_font, HB_OT_METRICS_TAG_UNDERLINE_SIZE, &underline_size)

            vextent_scale = renpy.config.ftfont_vertical_extent_scale.get(self.face_object.fn, 1.0)

            # Deal with fonts where harbuzz can't figure out the metrics.
            if horizontal_ascender == 0 and horizontal_descender == 0:
                horizontal_ascender = face.size.metrics.ascender
                horizontal_descender = face.size.metrics.descender

            if self.vertical:
                self.ascent = FT_CEIL(vertical_ascender)
                self.descent = FT_FLOOR(vertical_descender)
            else:
                self.ascent = FT_CEIL(int(horizontal_ascender * vextent_scale))
                self.descent = FT_FLOOR(int(horizontal_descender * vextent_scale))

            if self.descent > 0:
                self.descent = -self.descent

            self.ascent += self.expand
            self.descent -= self.expand

            self.height = self.ascent - self.descent

            self.lineskip = <int> self.height * renpy.game.preferences.font_line_spacing

            if self.vertical:
                self.underline_offset = FT_FLOOR(self.ascent - self.descent - underline_offset)
            else:
                self.underline_offset = FT_FLOOR(underline_offset)

            self.underline_height = FT_FLOOR(underline_size)

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
                    shear.xx = 0
                    shear.xy = -(1 << 16)
                    shear.yx = 1 << 16
                    shear.yy = 0
                    FT_Outline_Transform(&(<FT_OutlineGlyph> g).outline, &shear)

                if self.stroker != NULL:
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
        cdef int error
        cdef Glyph gl
        cdef FT_Vector kerning
        cdef int kern
        cdef float advance
        cdef unsigned int i
        cdef int vs_offset
        cdef glyph_cache *cache

        cdef float min_advance, next_min_advance

        cdef hb_buffer_t *hb
        cdef hb_glyph_info_t *glyph_info
        cdef hb_glyph_position_t *glyph_pos
        cdef unsigned int glyph_count

        cdef int bmx
        cdef int bmy

        self.setup()

        rv = [ ]

        # Start Harfbuzz

        hb = hb_buffer_create()
        utf32_s = s.encode("utf-32")

        hb_buffer_add_utf32(hb, <const uint32_t *> ((<const char *> utf32_s) + 4), len(s), 0, len(s));

        if self.vertical:
            hb_buffer_set_direction(hb, HB_DIRECTION_TTB)
        else:
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
            #     glyph_pos[i].y_advance / 64,
            #     glyph_pos[i].x_offset / 64,
            #     glyph_pos[i].y_offset / 64,
            # )

            gl = Glyph.__new__(Glyph)

            gl.character = ord(s[glyph_info[i].cluster])
            gl.glyph = glyph_info[i].codepoint

            gl.ascent = self.ascent
            gl.descent = -self.descent
            gl.line_spacing = self.lineskip
            gl.draw = True

            if self.vertical:
                gl.x_offset = -glyph_pos[i].y_offset / 64.0
                gl.y_offset = -glyph_pos[i].x_offset / 64.0
                gl.advance = -glyph_pos[i].y_advance / 64.0
            else:
                gl.x_offset = glyph_pos[i].x_offset / 64.0
                gl.y_offset = glyph_pos[i].y_offset / 64.0
                gl.advance = glyph_pos[i].x_advance / 64.0

            gl.width = gl.advance

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

            cache = self.get_glyph(glyph.glyph)

            bmx = <int> (glyph.x + .5 + glyph.x_offset) + cache.bitmap_left
            bmy = <int> (glyph.y + glyph.y_offset) - cache.bitmap_top

            if bmx < x:
                x = bmx

            if bmy < y:
                y = bmy

            if bmx + <int> cache.bitmap.width > w:
                w = bmx + cache.bitmap.width

            if bmy + <int> cache.bitmap.rows > h:
                h = bmy + cache.bitmap.rows

            glyph.add_left = <int> max(-(bmx - glyph.x), 0)
            glyph.add_right = <int> max(bmx + cache.bitmap.width - (glyph.x + glyph.width), 0)
            glyph.add_top = <int> max(-(bmy - glyph.y), 0)
            glyph.add_bottom = <int> max(bmy + cache.bitmap.rows - (glyph.y + glyph.line_spacing), 0)

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

            x = <int> (glyph.x + xo + glyph.x_offset)
            y = <int> (glyph.y + yo + glyph.y_offset)

            underline_x = x - glyph.delta_x_adjustment
            underline_end = x + <int> (glyph.advance + expand + .9999)

            cache = self.get_glyph(glyph.glyph)

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

                            elif alpha > line[3]:

                                line[0] = Sr * alpha // 255
                                line[1] = Sg * alpha // 255
                                line[2] = Sb * alpha // 255
                                line[3] = alpha

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

                        line[0] = Sr * Sa // 255
                        line[1] = Sg * Sa // 255
                        line[2] = Sb * Sa // 255
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

                        line[0] = Sr * Sa // 255
                        line[1] = Sg * Sa // 255
                        line[2] = Sb * Sa // 255
                        line[3] = Sa
