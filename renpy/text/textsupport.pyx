# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

include "linebreak.pxi"

cdef class Glyph:

    def __cinit__(self):
        self.delta_x_offset = 0

    def __repr__(self):
        return "<Glyph {0!r} time={1}>".format(self.character, self.time)

cdef class Line:

    def __init__(self, int y, int height, list glyphs):
        self.y = y
        self.height = height
        self.glyphs = glyphs
        self.eop = False

    def __repr__(self):
        return "<Line y={0}, height={1}>".format(self.y, self.height)

# The maximum width of text we lay out. This should be quite a bit smaller
# than the maximum SDL surface width. (16384)
cdef int MAX_WIDTH
MAX_WIDTH = 8192

TEXT=1
TAG=2
PARAGRAPH=3
DISPLAYABLE=4

def tokenize(unicode s):
    """
    This tokenizes a unicode string into text tags and tokens. It returns a list
    of pairs, where each pair begins with TEXT, TAG or PARAGRAPH, and then has
    the contents of the text run or tag.
    """

    cdef int TEXT_STATE = 1
    cdef int LEFT_BRACE_STATE = 2
    cdef int TAG_STATE = 3
    cdef int state = TEXT_STATE

    cdef Py_UNICODE c
    cdef unicode buf = u''

    cdef list rv = [ ]

    for c in s:

        if state == TEXT_STATE:

            if c == u'\n':
                if buf:
                    rv.append((TEXT, buf))

                rv.append((PARAGRAPH, u''))
                buf = u''

                continue

            elif c == u'{':
                state = LEFT_BRACE_STATE
                continue

            else:
                buf += c
                continue

        elif state == LEFT_BRACE_STATE:
            if c == u'{':
                buf += c
                state = TEXT_STATE
                continue

            elif c == u'}':
                raise Exception("Empty text tag in {0!r}.".format(s))

            else:
                if buf:
                    rv.append((TEXT, buf))

                buf = c
                state = TAG_STATE
                continue

        elif state == TAG_STATE:

            if c == u'}':
                rv.append((TAG, buf))
                buf = u''
                state = TEXT_STATE
                continue

            else:
                buf += c

    if state != TEXT_STATE:
        raise Exception("Open text tag at end of string {0!r}.".format(s))

    if buf:
        rv.append((TEXT, buf))

    return rv


def annotate_western(list glyphs):
    """
    Annotate the characters with line splitting information.
    """

    cdef Glyph g

    for g in glyphs:

        # Don't split ruby.
        if g.ruby != RUBY_NONE:
            continue

        if g.character == 0:
            g.split = SPLIT_BEFORE
        elif g.character == 0x20 or g.character == 0x200b:
            g.split = SPLIT_INSTEAD
        else:
            g.split = SPLIT_NONE

# This is used to tailor the unicode break algorithm. If a character in this
# array is mapped to not
cdef char break_tailor[65536]

for i in range(0, 65536):
    break_tailor[i] = BC_XX

def language_tailor(chars, cls):
    """
    :doc: other

    This can be used to override the line breaking class of a character. For
    example, the linebreaking class of a character can be set to ID to
    treat it as an ideograph, which allows breaks before and after that
    character.

    `chars`
        A list of characters to tailor.

    `cls`
        The character class. This should be one of the classes defined in Table
        1 of `UAX #14: Unicode Line Breaking Algorithm <http://www.unicode.org/reports/tr14/tr14-30.html>`_.
    """

    ncls = CLASSES.get(cls, BC_XX)

    for c in chars:
        break_tailor[ord(c)] = ncls

# cjk
#
# 0 = western
# 1 = loose
# 2 = normal
# 3 = strict
def annotate_unicode(list glyphs, bint no_ideographs, int cjk):
    """
    Annotate unicode characters with information as to if they can be used
    for linebreaking.
    """

    cdef char old_type, new_type, tailor_type
    cdef int space_pos, pos
    cdef int len_glyphs = len(glyphs)
    cdef int c
    cdef char bc
    cdef Glyph g, g1, old_g
    cdef char *break_classes

    old_type = BC_WJ
    pos = 1
    space_pos = 0

    if not glyphs:
        return

    if cjk == 0:
        break_classes = break_western
    elif cjk == 1:
        break_classes = break_cjk_loose
    elif cjk == 2:
        break_classes = break_cjk_normal
    elif cjk == 3:
        break_classes = break_cjk_strict
    else:
        break_classes = break_western

    for pos from 1 <= pos < len_glyphs:

        g = glyphs[pos]
        c = g.character

        if 0x20000 <= c <= 0x2ffff: # Supplemental Ideographic Plane
            new_type = BC_ID
            tailor_type = BC_XX
        elif c > 65535: # Other non-basic planes.
            new_type = BC_AL
            tailor_type = BC_XX
        else: # Basic plane - use lookup table.
            new_type = break_classes[c]
            tailor_type = break_tailor[c]

        # If given no-ideographs, then turn ideographs and hangul syllables
        # into alphabetic characters.
        if no_ideographs and (
            new_type == BC_H2 or
            new_type == BC_H3 or
            new_type == BC_ID or
            new_type == BC_JL or
            new_type == BC_JV or
            new_type == BC_JT):

            new_type = BC_AL

        # Normalize the class by turning various groups into AL.
        if (new_type >= BC_PITCH and new_type != BC_SP):
            new_type = BC_AL

        if tailor_type != BC_XX:
            new_type = tailor_type

        # If we have a space, record it and continue.
        if new_type == BC_SP:
            g.split = SPLIT_NONE
            space_pos = pos
            continue

        # If we have a combining mark, continue.
        if new_type == BC_CM:
            g.split = SPLIT_NONE
            continue

        # Figure out the type of break opportunity we have here.
        # ^ Prohibited break.
        # % Indirect break.
        # @ Prohibited break (combining mark)
        # # Indirect break (combining mark)
        # _ Direct break.

        bc = break_rules[ old_type * BC_PITCH + new_type]

        if bc == "%": # Indirect break.
            if space_pos:
                g1 = glyphs[space_pos]
                g1.split = SPLIT_INSTEAD

            g.split = SPLIT_NONE

        elif bc == "_": # Direct break.
            if space_pos:
                g1 = glyphs[space_pos]
                g1.split = SPLIT_INSTEAD
                g.split = SPLIT_NONE
            else:
                g.split = SPLIT_BEFORE

        else:
            g.split = SPLIT_NONE

        old_type = new_type
        space_pos = 0

    # Deal with ruby, by marking it as non-spacing.
    old_g = glyphs[0]
    old_g.split = SPLIT_NONE

    for g in glyphs:

        if g.character == 0:
            g.split = SPLIT_BEFORE

        if g.ruby == RUBY_TOP:
            g.split = SPLIT_NONE

        elif g.ruby == RUBY_BOTTOM and old_g.ruby == RUBY_BOTTOM:
            g.split = SPLIT_NONE

        old_g = g



def linebreak_greedy(list glyphs, int first_width, int rest_width):
    """
    Starting with a list of glyphs, decides where to split it. The result of
    this is the same list of glyphs, but with some of the .split fields set
    back to SPLIT_NONE, where we decided not to go ahead with the split after
    all.

    This is the greedy algorithm, which splits when the line is longer
    than a specified width.
    """

    cdef Glyph g, split_g
    cdef float width, x, splitx, gwidth

    width = first_width
    split_g = None

    # The x position of the current character. Invariant: x can never be more
    # that one character-width greater than width.
    x = 0

    # The x position after splitting the line.
    splitx = 0

    for g in glyphs:

        if g.ruby == RUBY_TOP:
            continue

        # If the x coordinate is greater than the width of the screen,
        # split at the last split point, if any.
        if x > width and split_g is not None:
            x = splitx
            split_g = None
            width = rest_width

        x += g.advance
        splitx += g.advance

        if g.split == SPLIT_INSTEAD:
            if split_g is not None:
                split_g.split = SPLIT_NONE

            split_g = g
            splitx = 0

        elif g.split == SPLIT_BEFORE:

            if split_g is not None:
                split_g.split = SPLIT_NONE

            split_g = g
            splitx = g.advance

    # Split at the last character, if necessary.
    if x > width:
        split_g = None

    if split_g is not None:
        split_g.split = SPLIT_NONE

def linebreak_nobreak(list glyphs):
    """
    Linebreak without linebreaking.
    """

    cdef Glyph g

    for g in glyphs:
        g.split = SPLIT_NONE


def linebreak_debug(list glyphs):
    """
    Return a string giving the results of linebreaking a list of glyphs.
    """

    cdef Glyph g

    rv = ""

    for g in glyphs:

        if g.split == SPLIT_INSTEAD:
            rv += "|"
        elif g.split == SPLIT_BEFORE:
            rv += "[" + unichr(g.character)
        else:
            rv += unichr(g.character)

    return rv


def linebreak_list(list glyphs):
    """
    Returns a list of unicode strings, one per broken line.
    """

    cdef Glyph g

    rv = [ ]
    line = u""

    for g in glyphs:

        if g.split == SPLIT_INSTEAD:
            rv.append(line)
            line = u""
        elif g.split == SPLIT_BEFORE:
            rv.append(line)
            line = unichr(g.character)
        else:
            line += unichr(g.character)

    if line:
        rv.append(line)

    return rv


def place_horizontal(list glyphs, float start_x, float first_indent, float rest_indent):
    """
    Place the glyphs horizontally, without taking into account the indentation
    at the start of the line. Returns the width of the laid-out line.
    """

    if not glyphs:
        return 0

    cdef Glyph g, old_g
    cdef float x, maxx

    x = start_x + first_indent
    maxx = 0
    old_g = None

    for g in glyphs:

        if g.ruby == RUBY_TOP:
            continue

        if g.split != SPLIT_NONE and old_g:
            # When a glyph is at the end of the line, set its advance to
            # be its width. (This makes things like strikeout and underline
            # easier, since we only need consider advance.)
            old_g.advance = old_g.width

        if g.split == SPLIT_INSTEAD:
            x = start_x + rest_indent
            continue

        elif g.split == SPLIT_BEFORE:
            x = start_x + rest_indent

        g.x = <short> (x + .5)

        if maxx < x + g.width:
            maxx = x + g.width
        if maxx < x + g.advance:
            maxx = x + g.advance

        x += g.advance

        # Limit us to some width.
        if x > MAX_WIDTH:
            x = MAX_WIDTH

        old_g = g

    return maxx

def place_vertical(list glyphs, int y, int spacing, int leading):
    """
    Vertically places the non-ruby glyphs. Returns a list of line end heights,
    and the y-value for the top of the next line.
    """

    cdef Glyph g, gg

    cdef int pos, sol, len_glyphs, i
    cdef int ascent, line_spacing
    cdef bint end_line

    if not glyphs:
        return [ ], y

    len_glyphs = len(glyphs)

    pos = 0
    sol = 0

    ascent = 0
    line_spacing = 0

    rv = [ ]

    y += leading

    while True:

        if pos >= len_glyphs:
            end_line = True
        else:
            g = glyphs[pos]
            end_line = (g.split != SPLIT_NONE)

        if end_line:

            for i from sol <= i < pos:
                gg = glyphs[i]

                if gg.ruby == RUBY_TOP:
                    continue

                if gg.ascent:
                    gg.y = y + ascent

                else:
                    # Glyphs without ascents are displayables, which get
                    # aligned to the top of the line.
                    gg.y = y
                    gg.ascent = ascent

            l = Line(y - leading, leading + line_spacing + spacing, glyphs[sol:pos])
            rv.append(l)

            y += line_spacing
            y += spacing
            y += leading

            sol = pos

            ascent = 0
            line_spacing = 0

            if g.split == SPLIT_INSTEAD:
                sol += 1
                pos += 1

                if pos >= len_glyphs:
                    break
                else:
                    continue

        if pos >= len_glyphs:
            break

        if g.ascent > ascent:
            ascent = g.ascent

        if g.line_spacing > line_spacing:
            line_spacing = g.line_spacing

        pos += 1


    rv[-1].eop = True
    return rv, y - leading

def kerning(list glyphs, float amount):
    cdef Glyph g

    for g in glyphs:
        g.advance += amount


def assign_times(float t, float gps, list glyphs):
    """
    Assign a display time to each glyph.

    `t`
        The start time of the first glyph.

    `gps`
        The number of glyphs per second to show.

    `glyphs`
        A list of glyphs to apply this to.

    Returns the time of the first glyph in the next block.
    """

    cdef float tpg # time per glyph
    cdef Glyph g

    if gps == 0:
        tpg = 0.0
    else:
        tpg = 1.0 / gps

    for g in glyphs:

        if g.ruby == RUBY_TOP:
            g.time = t
            continue

        t += tpg
        g.time = t

    return t


def max_times(list l):
    """
    Set the max_time filed on each line.
    """

    cdef Line line
    cdef Glyph g
    cdef float max_time

    max_time = 0

    for line in l:
        for g in line.glyphs:
            if g.time > max_time:
                max_time = g.time

        line.max_time = max_time

    return max_time


def hyperlink_areas(list l):
    """
    Returns a list of (hyperlink, x, y, w, h) tuples, where each entry in
    the rectangle represents a contiguous portion of a hyperlink on the
    given line.
    """

    cdef Line line
    cdef Glyph g
    cdef list gl
    cdef int len_gl

    cdef int pos

    cdef int max_x
    cdef int min_x
    cdef int hyperlink

    rv = [ ]

    for line in l:
        gl = line.glyphs
        len_gl = len(gl)

        hyperlink = 0
        max_x = 0
        min_x = 1000000
        pos = 0

        while pos < len_gl:

            g = gl[pos]

            if (hyperlink and g.hyperlink != hyperlink):
                rv.append((hyperlink, min_x, line.y, max_x - min_x, line.height))
                hyperlink = 0
                max_x = 0
                min_x = 1000000

            hyperlink = g.hyperlink

            if hyperlink:
                if g.x < min_x:
                    min_x = g.x

                if g.x + g.width > max_x:
                    max_x = g.x + <int> g.width

            pos += 1

        if hyperlink:
            rv.append((hyperlink, min_x, line.y, max_x - min_x, line.height))

    return rv


def mark_ruby_top(list l):

    cdef Glyph g

    for g in l:
        g.ruby = RUBY_TOP

def mark_ruby_bottom(list l):

    cdef Glyph g

    for g in l:
        g.ruby = RUBY_BOTTOM


def place_ruby(list glyphs, int ruby_offset, int surf_width, int surf_height):

    cdef Glyph g
    cdef ruby_t last_ruby = RUBY_NONE
    cdef int len_glyphs = len(glyphs)
    cdef float x, width, min_x = 0, max_x = 0
    cdef int y = 0
    cdef int start_top
    cdef int pos = 0
    cdef int i

    while pos < len_glyphs:

        g = glyphs[pos]

        if g.ruby == RUBY_NONE:

            min_x = g.x
            max_x = g.x + g.width
            y = g.y

            last_ruby = RUBY_NONE

            pos += 1
            continue

        elif g.ruby == RUBY_BOTTOM:

            if last_ruby != RUBY_BOTTOM:
                min_x = g.x

            max_x = g.x + g.width
            y = g.y

            last_ruby = RUBY_BOTTOM

            pos += 1
            continue

        # Otherwise, we have RUBY_TOP.

        # Find the run of RUBY_TOP. When this is done, the run will be in
        # glyphs[start_top:pos].
        start_top = pos

        while pos < len_glyphs:

            g = glyphs[pos]
            if g.ruby != RUBY_TOP:
                break

            pos += 1

        # Compute the width of the run.

        width = 0
        for i from start_top <= i < pos:
            g = glyphs[i]
            width += g.advance

        width -= glyphs[pos - 1].advance
        width += glyphs[pos - 1].width

        # Place the glyphs.
        x = (max_x + min_x) / 2 - width / 2

        for i from start_top <= i < pos:
            g = glyphs[i]
            g.x = <int> (x + .5)
            g.y = y + ruby_offset

            x += g.advance

        last_ruby = RUBY_TOP

def align_and_justify(list lines, int width, float text_align, bint justify):
    """
    Handle text alignment and justification.
    """

    cdef Line l
    cdef Glyph g

    cdef int max_x
    cdef int spaces

    cdef float justify_offset
    cdef float justify_per_space

    cdef int offset

    # See if we have to do anything at all.
    if not justify and text_align == 0.0:
        return

    for l in lines:

        spaces = 0
        max_x = 0

        for g in l.glyphs:

            if g.ruby == RUBY_TOP:
                continue

            if g.character == 0x20:
                spaces += 1

            max_x = <int> (g.x + g.width)

        # If we're too big, give up.
        if max_x >= MAX_WIDTH:
            continue

        if justify and spaces and not l.eop:

            justify_per_space = 1.0 * (width - max_x) / spaces
            justify_offset = 0.5 # Makes numbers round better.

            for g in l.glyphs:

                if g.ruby == RUBY_TOP:
                    continue

                if g.character == 0x20:
                    justify_offset += justify_per_space

                g.x += <int> justify_offset

        else:
            offset = <int> ((width - max_x) * text_align)

            for g in l.glyphs:

                if g.ruby == RUBY_TOP:
                    continue

                g.x += offset

def reverse_lines(list glyphs):
    """
    Reverses each line in glyphs, while keeping the lines themselves in
    the original order.
    """

    cdef list rv
    cdef list block
    cdef Glyph g

    rv = [ ]
    block = [ ]

    for g in glyphs:

        if g.split == SPLIT_INSTEAD:
            block.reverse()
            rv.extend(block)
            rv.append(g)
            block = [ ]

            continue

        block.append(g)

    block.reverse()
    rv.extend(block)

    return rv

def copy_splits(list source, list dest):
    """
    Copies break and timing information from one list of glyphs
    to another.
    """

    cdef Glyph s
    cdef Glyph d
    cdef int i

    for 0 <= i < len(dest):
        s = source[i]
        d = dest[i]

        d.split = s.split


def tweak_glyph_spacing(list glyphs, list lines, double dx, double dy, double w, double h):
    cdef Glyph g

    if w <= 0 or h <= 0:
        return

    cdef short old_x_offset = 0
    cdef short x_offset

    for g in glyphs:

        x_offset = <short> (dx * g.x / w)

        g.x += x_offset
        g.y += <short> (dy * g.y / h)

        if x_offset > old_x_offset:
            g.delta_x_offset = x_offset - old_x_offset

        old_x_offset = x_offset

    for l in lines:
        end = l.y + l.height

        l.y += int(dy * l.y / h)
        end += int(dy * end / h)

        l.height = end - l.y
