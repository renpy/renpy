# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
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

import math
import renpy.display

from renpy.text.textsupport import \
    TAG, TEXT, PARAGRAPH, DISPLAYABLE

import renpy.text.textsupport as textsupport
import renpy.text.texwrap as texwrap
import renpy.text.font as font
import renpy.text.extras as extras

try:
    from _renpybidi import log2vis, WRTL, RTL, ON
except:
    pass

class Blit(object):
    """
    Represents a blit command, which can be used to render a texture to a
    render. This is a rectangle with an associated alpha.
    """

    def __init__(self, x, y, w, h, alpha=1.0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.alpha = alpha

    def __repr__(self):
        return "<Blit ({0}, {1}, {2}, {3}) {4}>".format(self.x, self.y, self.w, self.h, self.alpha)


def outline_blits(blits, outline):
    """
    Given a list of blits, adjusts it for the given outline size. That means
    adding borders on the left and right of each line of blits. Returns a second
    list of blit objects.

    We assume that there are a discrete set of vertical areas that divide the
    original blits, and that no blit covers two vertical areas. So something
    like:

     _____________________________________
    |_____________________________________|
    |___________|_________________|_______|
    |_____________________|_______________|

    is fine, but:

     _____________________________________
     |              |_____________________|
     |______________|_____________________|

    is forbidden. That's an invariant that the blit_<method> functions are
    required to enforce.
    """

    # Sort the blits.
    blits.sort(key=lambda b : (b.y, b.x))

    # The y coordinate that everything in the current line shares. This can
    # be adjusted in the output blits.
    line_y = 0

    # The y coordinate of the top of the current line.
    top_y = 0

    # The y coordinate of the bottom of the current line.
    bottom_y = 0


    # The maximum x coordinate of the previous blit on this line.
    max_x = 0

    rv = [ ]

    for b in blits:

        x0 = b.x
        x1 = b.x + b.w + outline * 2

        y0 = b.y
        y1 = b.y + b.h + outline * 2

        # Prevents some visual artifacting, where the two lines can overlap.
        y1 -= 1

        if line_y != y0:
            line_y = y0
            top_y = bottom_y
            max_x = 0

        y0 = top_y

        if y1 > bottom_y:
            bottom_y = y1

        if max_x > x0:
            x0 = max_x

        max_x = x1

        rv.append(Blit(x0, y0, x1 - x0, y1 - y0, b.alpha))

    return rv


class DrawInfo(object):
    """
    This object is supplied as a parameter to the draw method of the various
    segments. It has the following fields:

    `surface`
        The surface to draw to.

    `override_color`
        If not None, a color that's used for this outline/shadow.

    `outline`
        The amount to outline the text by.

    `displayable_blits`
        If not none, this is a list of (displayable, xo, yo) tuples. The draw
        method adds displayable blits to this list when this is not None.
    """

    # No implementation, this is set up in the layout object.


class TextSegment(object):
    """
    This represents a segment of text that has a single set of properties
    applied to it.
    """

    def __init__(self, source=None):
        """
        Creates a new segment of text. If `source` is given, this starts off
        a copy of that source segment. Otherwise, it's up to the code that
        creates it to initialize it with defaults.
        """

        if source is not None:
            self.antialias = source.antialias
            self.vertical = source.vertical
            self.font = source.font
            self.size = source.size
            self.bold = source.bold
            self.italic = source.italic
            self.underline = source.underline
            self.strikethrough = source.strikethrough
            self.color = source.color
            self.black_color = source.black_color
            self.hyperlink = source.hyperlink
            self.kerning = source.kerning
            self.cps = source.cps
            self.ruby_top = source.ruby_top
            self.ruby_bottom = source.ruby_bottom

        else:
            self.hyperlink = 0
            self.cps = 0
            self.ruby_top = False
            self.ruby_bottom = False

    def __repr__(self):
        return "<TextSegment font={font}, size={size}, bold={bold}, italic={italic}, underline={underline}, color={color}, black_color={black_color}, hyperlink={hyperlink}, vertical={vertical}>".format(**self.__dict__)

    def take_style(self, style):
        """
        Takes the style of this text segement from the named style object.
        """

        self.antialias = style.antialias
        self.vertical = style.vertical
        self.font = style.font
        self.size = style.size
        self.bold = style.bold
        self.italic = style.italic
        self.underline = style.underline
        self.strikethrough = style.strikethrough
        self.color = style.color
        self.black_color = style.black_color
        self.hyperlink = None
        self.kerning = style.kerning

        if style.slow_cps is True:
            self.cps = renpy.game.preferences.text_cps

        self.cps = self.cps * style.slow_cps_multiplier

    # From here down is the public glyph API.

    def glyphs(self, s):
        """
        Return the list of glyphs corresponding to unicode string s.
        """

        fo = font.get_font(self.font, self.size, self.bold, self.italic, 0, self.antialias, self.vertical)
        rv = fo.glyphs(s)

        # Apply kerning to the glyphs.
        if self.kerning:
            textsupport.kerning(rv, self.kerning)

        if self.hyperlink:
            for g in rv:
                g.hyperlink = self.hyperlink

        if self.ruby_bottom:
            textsupport.mark_ruby_bottom(rv)
        elif self.ruby_top:
            textsupport.mark_ruby_top(rv)

        return rv

    def draw(self, glyphs, di, xo, yo):
        """
        Draws the glyphs to surf.
        """

        if di.override_color:
            color = di.override_color
            black_color = None
        else:
            color = self.color
            black_color = self.black_color

        fo = font.get_font(self.font, self.size, self.bold, self.italic, di.outline, self.antialias, self.vertical)
        fo.draw(di.surface, xo, yo, color, glyphs, self.underline, self.strikethrough, black_color)

    def assign_times(self, gt, glyphs):
        """
        Assigns times to the glyphs. `gt` is the starting time of the first
        glyph, and it returns the starting time of the first glyph in the next
        segment.
        """

        return textsupport.assign_times(gt, self.cps, glyphs)

    def subsegment(self, s):
        """
        This is called to break the current text segment up into multiple
        text segments. It yields one or more(TextSegement, string) tuples
        for each sub-segment it creates.

        This is used by the FontGroup code to create new text segments based
        on the font group.
        """


        if not isinstance(self.font, font.FontGroup):
            yield (self, s)
            return

        segs = { }

        for f, ss in self.font.segment(s):

            seg = segs.get(f, None)

            if seg is None:
                seg = TextSegment(self)
                seg.font = f

                segs[f] = seg

            yield seg, ss

    def bounds(self, glyphs, bounds):
        """
        Given an x, y, w, h bounding box, returns the union of the given
        bounding box and the bounding box the glyphs will actually be drawn
        into, not including any offsets or expansions.

        This is used to deal with glyphs that are on the wrong side of the
        origin point.
        """

        fo = font.get_font(self.font, self.size, self.bold, self.italic, 0, self.antialias, self.vertical)
        return fo.bounds(glyphs, bounds)

class SpaceSegment(object):
    """
    A segment that's used to render horizontal or vertical whitespace.
    """

    def __init__(self, ts, width=0, height=0):
        """
        `ts`
            The text segment that this SpaceSegment follows.
        """

        self.glyph = glyph = textsupport.Glyph()

        glyph.character = 0
        glyph.ascent = 0
        glyph.line_spacing = height
        glyph.advance = width
        glyph.width = width

        if ts.hyperlink:
            glyph.hyperlink = ts.hyperlink

        self.cps = ts.cps

    def glyphs(self, s):
        return [ self.glyph ]

    def bounds(self, glyphs, bounds):
        return bounds

    def draw(self, glyphs, di, xo, yo):
        # Does nothing - since there's nothing to draw.
        return

    def assign_times(self, gt, glyphs):
        if self.cps != 0:
            gt += 1.0 / self.cps

        self.glyph.time = gt
        return gt


class DisplayableSegment(object):
    """
    A segment that's used to render horizontal or vertical whitespace.
    """

    def __init__(self, ts, d, renders):
        """
        `ts`
            The text segment that this SpaceSegment follows.
        """

        self.d = d
        rend = renders[d]

        w, h = rend.get_size()

        self.glyph = glyph = textsupport.Glyph()

        glyph.character = 0
        glyph.ascent = 0
        glyph.line_spacing = h
        glyph.advance = w
        glyph.width = w

        if ts.hyperlink:
            glyph.hyperlink = ts.hyperlink

        self.cps = ts.cps

    def glyphs(self, s):
        return [ self.glyph ]

    def draw(self, glyphs, di, xo, yo):
        if di.displayable_blits is not None:
            di.displayable_blits.append((self.d, self.glyph.x, self.glyph.y, self.glyph.time))

    def assign_times(self, gt, glyphs):
        if self.cps != 0:
            gt += 1.0 / self.cps

        self.glyph.time = gt
        return gt

    def bounds(self, glyphs, bounds):
        return bounds

class FlagSegment(object):
    """
    A do-nothing segment that just exists so we can flag the start and end
    of a run of text.
    """

    def glyphs(self, s):
        return [ ]

    def draw(self, glyphs, di, xo, yo):
        return

    def assign_times(self, gt, glyphs):
        return gt

    def bounds(self, glyphs, bounds):
        return bounds

class Layout(object):
    """
    Represents the layout of text.
    """

    def __init__(self, text, width, height, renders):
        """
        `text`
            The text object this layout is associated with.
        `width`, `height`
            The height of the laid-out text.
        """

        style = text.style

        self.line_overlap_split = style.line_overlap_split

        # Do we have any hyperlinks in this text? Set by segment.
        self.has_hyperlinks = False

        # Do we have any ruby in the text?
        self.has_ruby = False

        # Slow text that is not before the start segment is displayed
        # instantaneously. Text after the end segment is not displayed
        # at all. These are controlled by the {_start} and {_end} tags.
        self.start_segment = None
        self.end_segment = None

        self.width = width
        self.height = height

        # Figure out outlines and other info.
        outlines, xborder, yborder, xoffset, yoffset = self.figure_outlines(style)
        self.outlines = outlines
        self.xborder = xborder
        self.yborder = yborder
        self.xoffset = xoffset
        self.yoffset = yoffset

        # Adjust the borders by the outlines.
        width -= self.xborder
        height -= self.yborder

        # The greatest x coordinate of the text.
        maxx = 0

        # The current y, which becomes the maximum height once all paragraphs
        # have been rendered.
        y = 0

        # A list of glyphs - all the glyphs we know of.
        all_glyphs = [ ]

        # A list of (segment, glyph_list) pairs for all paragraphs.
        par_seg_glyphs = [ ]

        # A list of Line objects.
        lines = [ ]

        # The time at which the next glyph will be displayed.
        gt = 0.0

        # True if we've encountered the end segment while assigning times.
        ended = False

        # 2. Breaks the text into a list of paragraphs, where each paragraph is
        # represented as a list of (Segment, text string) tuples.
        #
        # This takes information from the various styles that apply to the text,
        # and so needs to be redone when the style of the text changes.
        self.paragraphs = self.segment(text.tokens, style, renders)

        first_indent = style.first_indent
        rest_indent = style.rest_indent

        for p in self.paragraphs:

            # RTL - apply RTL to the text of each segment, then
            # reverse the order of the segments in each paragraph.
            if renpy.config.rtl:
                p, rtl = self.rtl_paragraph(p)
            else:
                rtl = False

            # 3. Convert each paragraph into a Segment, glyph list. (Store this
            # to use when we draw things.)

            # A list of glyphs in the line.
            line_glyphs = [ ]

            # A list of (segment, list of glyph) pairs.
            seg_glyphs = [ ]

            for ts, s in p:
                glyphs = ts.glyphs(s)

                t = (ts, glyphs)
                seg_glyphs.append(t)
                par_seg_glyphs.append(t)
                line_glyphs.extend(glyphs)
                all_glyphs.extend(glyphs)

            # RTL - Reverse each line, segment, so that we can use LTR
            # linebreaking algorithms.
            if rtl:
                line_glyphs.reverse()
                for ts, glyphs in seg_glyphs:
                    glyphs.reverse()

            # Tag the glyphs that are eligible for line breaking, and if
            # they should be included or excluded from the end of a line.
            language = style.language

            if language == "unicode" or language == "eastasian":
                textsupport.annotate_unicode(line_glyphs, False, 0)
            elif language == "korean-with-spaces":
                textsupport.annotate_unicode(line_glyphs, True, 0)
            elif language == "western":
                textsupport.annotate_western(line_glyphs)
            elif language == "japanese-loose":
                textsupport.annotate_unicode(line_glyphs, False, 1)
            elif language == "japanese-normal":
                textsupport.annotate_unicode(line_glyphs, False, 2)
            elif language == "japanese-strict":
                textsupport.annotate_unicode(line_glyphs, False, 3)
            else:
                raise Exception("Unknown language: {0}".format(language))

            # Break the paragraph up into lines.
            layout = style.layout

            if layout == "tex":
                texwrap.linebreak_tex(line_glyphs, width - first_indent, width - rest_indent, False)
            elif layout == "subtitle" or layout == "tex-subtitle":
                texwrap.linebreak_tex(line_glyphs, width - first_indent, width - rest_indent, True)
            elif layout == "greedy":
                textsupport.linebreak_greedy(line_glyphs, width - first_indent, width - rest_indent)
            elif layout == "nobreak":
                textsupport.linebreak_nobreak(line_glyphs)
            else:
                raise Exception("Unknown layout: {0}".format(layout))

            for ts, glyphs in seg_glyphs:
                # Only assign a time if we're past the start segment.
                if self.start_segment is not None:
                    if self.start_segment is ts:
                        self.start_segment = None
                    else:
                        continue

                if ts is self.end_segment:
                    ended = True

                if ended:
                    textsupport.assign_times(gt, 0.0, glyphs)
                else:
                    gt = ts.assign_times(gt, glyphs)

            # RTL - Reverse the glyphs in each line, back to RTL order,
            # now that we have lines.
            if rtl:
                line_glyphs = textsupport.reverse_lines(line_glyphs)

            # Taking into account indentation, kerning, justification, and text_align,
            # lay out the X coordinate of each glyph.

            w = textsupport.place_horizontal(line_glyphs, 0, first_indent, rest_indent)
            if w > maxx:
                maxx = w

            # Figure out the line height, line spacing, and the y coordinate of each
            # glyph.
            l, y = textsupport.place_vertical(line_glyphs, y, style.line_spacing, style.line_leading)
            lines.extend(l)

            # Figure out the indent of the next line.
            first_indent = style.newline_indent
            if first_indent is None:
                first_indent = rest_indent

        if style.line_spacing < 0:
            if renpy.config.broken_line_spacing:
                y += -style.line_spacing * len(lines)
            else:
                y += -style.line_spacing

            lines[-1].height = y - lines[-1].y

        if style.min_width > maxx + self.xborder:
            maxx = style.min_width - self.xborder

        maxx = math.ceil(maxx)

        textsupport.align_and_justify(lines, maxx, style.text_align, style.justify)

        # Figure out the size of the texture. (This is a little over-sized,
        # but it simplifies the code to not have to care about borders on a
        # per-outline basis.)
        sw, sh = size = (maxx + self.xborder, y + self.yborder)
        self.size = size

        if self.has_ruby:
            textsupport.place_ruby(all_glyphs, style.ruby_style.yoffset, sw, sh)


        # Check for glyphs that are being drawn out of bounds, because the font
        # or anti-aliasing or whatever makes them bigger than the bounding box. If
        # we have them, grow the b

        bounds = (0, 0, maxx, y)
        for ts, glyphs in par_seg_glyphs:
            bounds = ts.bounds(glyphs, bounds)


        self.add_left = max(-bounds[0], 0)
        self.add_top = max(-bounds[1], 0)
        self.add_right = max(bounds[2] - maxx, 0)
        self.add_bottom = max(bounds[3] - y, 0)

        sw += self.add_left * 10 + self.add_right
        sh += self.add_top + self.add_bottom

        # A map from (outline, color) to a texture.
        self.textures = { }

        di = DrawInfo()

        for o, color, _xo, _yo in self.outlines:
            key = (o, color)

            if key in self.textures:
                continue

            # Create the texture.
            surf = renpy.display.pgrender.surface((sw, sh), True)

            di.surface = surf
            di.override_color = color
            di.outline = o

            if color == None:
                self.displayable_blits = [ ]
                di.displayable_blits = self.displayable_blits
            else:
                di.displayable_blits = None

            for ts, glyphs in par_seg_glyphs:
                if ts is self.end_segment:
                    break

                ts.draw(glyphs, di, self.add_left, self.add_top)


            renpy.display.draw.mutated_surface(surf)
            tex = renpy.display.draw.load_texture(surf)

            self.textures[key] = tex

        # Compute the max time for all lines, and the max max time.
        self.max_time = textsupport.max_times(lines)

        # Store the lines, so we have them for typeout.
        self.lines = lines

        # Store the hyperlinks, if any.
        if self.has_hyperlinks:
            self.hyperlinks = textsupport.hyperlink_areas(lines)
        else:
            self.hyperlinks = [ ]

        # Log an overflow if the laid out width or height is larger than the
        # size of the provided area.
        if renpy.config.debug_text_overflow:
            if sw > width or sh > height:
                filename, line = renpy.exports.get_filename_line()

                renpy.display.to_log.write("")
                renpy.display.to_log.write("File \"%s\", line %d, text overflow:", filename, line)
                renpy.display.to_log.write("     Available: (%d, %d) Laid-out: (%d, %d)", width, height, sw, sh)
                renpy.display.to_log.write("     Text: %r", text.text)

    def segment(self, tokens, style, renders):
        """
        Breaks the text up into segments. This creates a list of paragraphs,
        which each paragraph being represented as a list of TextSegment, glyph
        list tuples.
        """

        # A map from an integer to the number of the hyperlink this segment
        # is part of.
        self.hyperlink_targets = { }

        paragraphs = [ ]
        line = [ ]

        ts = TextSegment(None)

        ts.cps = style.slow_cps
        if ts.cps is None or ts.cps is True:
            ts.cps = renpy.game.preferences.text_cps

        ts.take_style(style)

        # The text segement stack.
        tss = [ ts ]

        def push():
            """
            Creates a new text segment, and pushes it onto the text segement
            stack. Returns the new text segment.
            """

            ts = TextSegment(tss[-1])
            tss.append(ts)

            return ts

        for type, text in tokens: #@ReservedAssignment

            if type == PARAGRAPH:

                # Note that this code is duplicated for the p tag, and for
                # the empty line case, below.
                if not line:
                    line.extend(tss[-1].subsegment(u" "))

                paragraphs.append(line)
                line = [ ]

                continue

            elif type == TEXT:
                line.extend(tss[-1].subsegment(text))
                continue

            elif type == DISPLAYABLE:
                line.append((DisplayableSegment(tss[-1], text, renders), u""))
                continue

            # Otherwise, we have a text tag.

            tag, _, value = text.partition("=")

            if tag and tag[0] == "/":
                tss.pop()

                if not tss:
                    raise Exception("%r closes a text tag that isn't open." % text)

            elif tag == "_start":
                fs = FlagSegment()
                line.append((fs, ""))
                self.start_segment = fs

            elif tag == "_end":
                fs = FlagSegment()
                line.append((fs, ""))
                self.end_segment = fs

            elif tag == "p":
                # Duplicated from the newline tag.

                if not line:
                    line.extend(tss[-1].subsegment(u" "))

                paragraphs.append(line)
                line = [ ]

            elif tag == "space":
                width = int(value)
                line.append((SpaceSegment(tss[-1], width=width), u""))

            elif tag == "vspace":
                # Duplicates from the newline tag.

                height = int(value)

                if line:
                    paragraphs.append(line)

                line = [ (SpaceSegment(tss[-1], height=height), u"") ]
                paragraphs.append(line)

                line = [ ]

            elif tag == "w":
                pass

            elif tag == "fast":
                pass

            elif tag == "nw":
                pass

            elif tag == "a":
                self.has_hyperlinks = True

                hyperlink_styler = style.hyperlink_functions[0]

                if hyperlink_styler:
                    hls = hyperlink_styler(value)
                else:
                    hls = style

                old_prefix = hls.prefix

                link = len(self.hyperlink_targets) + 1
                self.hyperlink_targets[link] = value

                if renpy.display.focus.argument == link:
                    hls.set_prefix("hover_")
                else:
                    hls.set_prefix("idle_")

                ts = push()
                # inherit vertical style
                vert_style = ts.vertical
                ts.take_style(hls)
                ts.vertical = vert_style
                ts.hyperlink = link

                hls.set_prefix(old_prefix)

            elif tag == "b":
                push().bold = True

            elif tag == "i":
                push().italic = True

            elif tag == "u":
                push().underline = True

            elif tag == "s":
                push().strikethrough = True

            elif tag == "plain":
                ts = push()
                ts.bold = False
                ts.italic = False
                ts.underline = False
                ts.strikethrough = False

            elif tag == "":
                style = getattr(renpy.store.style, value)
                push().take_style(style)

            elif tag == "font":
                push().font = value

            elif tag == "size":
                if value[0] in "+-":
                    push().size += int(value)
                else:
                    push().size = int(value)

            elif tag == "color":
                push().color = renpy.easy.color(value)

            elif tag == "k":
                push().kerning = float(value)

            elif tag == "rt":
                ts = push()
                # inherit vertical style
                vert_style = ts.vertical
                ts.take_style(style.ruby_style)
                ts.vertical = vert_style
                ts.ruby_top = True
                self.has_ruby = True

            elif tag == "rb":
                push().ruby_bottom = True
                # We only care about ruby if we have a top.

            elif tag == "cps":
                ts = push()

                if value[0] == "*":
                    ts.cps *= float(value[1:])
                else:
                    ts.cps = float(value)

            elif tag == "vert":
                push().vertical = True

            elif tag == "horiz":
                ts = push()
                ts.vertical = False

            elif tag[0] == "#":
                pass

            else:
                raise Exception("Unknown text tag %r" % text)

        if not line:
            line.extend(tss[-1].subsegment(u" "))

        paragraphs.append(line)

        return paragraphs

    def rtl_paragraph(self, p):
        """
        Given a paragraph (a list of segment, text tuples) handles
        RTL and ligaturization. This returns the reversed RTL paragraph,
        which differers from the LTR one. It also returns a flag that is
        True if this is an rtl paragraph.
        """

        direction = ON

        l = [ ]

        for ts, s in p:
            s, direction = log2vis(s, direction)
            l.append((ts, s))

        rtl = (direction == RTL or direction == WRTL)

        return l, rtl


    def figure_outlines(self, style):
        """
        Return a list containing the outlines, including an outline
        representing the drop shadow, if we have one, also including
        an entry for the main text, with color None. Also returns the
        space reserved for outlines - to be deducted from the width
        and the height.
        """

        style_outlines = style.outlines
        dslist = style.drop_shadow

        if not style_outlines and not dslist:
            return [ (0, None, 0, 0) ], 0, 0, 0, 0

        outlines = [ ]

        if dslist:
            if not isinstance(dslist, list):
                dslist = [ dslist ]

            for dsx, dsy in dslist:
                outlines.append((0, style.drop_shadow_color, dsx, dsy))

        outlines.extend(style_outlines)

        # The outline borders we reserve.
        left = 0
        right = 0
        top = 0
        bottom = 0

        for o, _c, x, y in outlines:

            l = x - o
            r = x + o
            t = y - o
            b = y + o

            if l < left:
                left = l

            if r > right:
                right = r

            if t < top:
                top = t

            if b > bottom:
                bottom = b

        outlines.append((0, None, 0, 0))

        return outlines, right - left, bottom - top, -left, -top


    def blits_typewriter(self, st):
        """
        Given a st and an outline, returns a list of blit objects that
        can be used to blit those objects.
        """

        width, max_height = self.size

        rv = [ ]

        max_y = 0

        for l in self.lines:

            if l.max_time > st:
                break

            max_y = min(l.y + l.height + self.line_overlap_split, max_height)

        else:
            l = None

        if max_y:
            rv.append(Blit(0, 0, width, max_y))

        if l is None:
            return rv

        # If l is not none, then we have a line for which max_time has not
        # yet been reached. Blit it.

        min_x = width
        max_x = 0

        for g in l.glyphs:

            if g.time > st:
                continue

            if g.x + g.advance > max_x:
                max_x = g.x + g.advance

            if g.x  < min_x:
                min_x = g.x

        ly = min(l.y + l.height + self.line_overlap_split, max_height)

        if min_x < max_x:
            rv.append(Blit(min_x, max_y, max_x - min_x, ly - max_y))

        return rv

    def redraw_typewriter(self, st):
        """
        Return the time of the first glyph that should be shown after st.
        """

        for l in self.lines:
            if not l.glyphs:
                continue

            if l.max_time > st:
                break

        else:
            return None

        return 0

# The maximum number of entries in the layout cache.
LAYOUT_CACHE_SIZE = 50

# Maps from a text to the layout of that text - in an old and new generation.
layout_cache_old = { }
layout_cache_new = { }

def layout_cache_clear():
    """
    Clears the old and new layout caches.
    """

    global layout_cache_old, layout_cache_new
    layout_cache_old = { }
    layout_cache_new = { }

def layout_cache_tick():
    """
    Called once per interaction, to merge the old and new layout caches.
    """

    global layout_cache_old, layout_cache_new
    layout_cache_old = layout_cache_new
    layout_cache_new = { }

VERT_REVERSE = renpy.display.render.Matrix2D(0, -1, 1, 0)
VERT_FORWARD = renpy.display.render.Matrix2D(0, 1, -1, 0)

class Text(renpy.display.core.Displayable):

    """
    :doc: text
    :args: (text, slow=None, scope=None, substitute=None, slow_done=None, **properties)

    A displayable that displays text on the screen.

    `text`
        The text to display on the screen. This may be a string, or a list of
        strings and displayables.

    `slow`
        Determines if the text is displayed slowly, being typed out one character at the time.
        If None, slow text mode is determined by the :propref:`slow_cps` style property. Otherwise,
        the truth value of this parameter determines if slow text mode is used.

    `scope`
        If not None, this should be a dictionary that provides an additional scope for text
        interpolation to occur in.

    `substitute`
        If true, text interpolation occurs. If false, it will not occur. If
        None, they are controlled by :var:`config.new_substitutions`.
    """

    __version__ = 4

    def after_upgrade(self, version):

        if version < 3:
            self.ctc = None

        if version < 4:

            if not isinstance(self.text, list):
                self.text = [ self.text ]

            self.scope = None
            self.substitute = False
            self.start = None
            self.end = None
            self.dirty = True

    def __init__(self, text, slow=None, scope=None, substitute=None, slow_done=None, replaces=None, **properties):

        super(Text, self).__init__(**properties)

        # We need text to be a list, so if it's not, wrap it.
        if not isinstance(text, list):
            text = [ text ]

        # Check that the text is all text-able things.
        for i in text:
            if not isinstance(i, (basestring, renpy.display.core.Displayable)):
                if renpy.config.developer:
                    raise Exception("Cannot display {0!r} as text.".format(i))
                else:
                    text = [ "" ]
                    break

        # Sets the text we're showing, and performs substitutions.
        self.set_text(text, scope, substitute)

        if renpy.game.less_updates:
            slow = False

        # True if we're using slow text mode.
        self.slow = slow

        # The callback to be called when slow-text mode ends.
        self.slow_done = None

        # The ctc indicator associated with this text.
        self.ctc = None

        # The index of the start and end strings in the first segment of text.
        # (None to show the whole text.)
        self.start = None
        self.end = None

        if replaces is not None:
            self.slow = replaces.slow
            self.slow_done = replaces.slow_done
            self.ctc = replaces.ctc
            self.start = replaces.start
            self.end = replaces.end

        # Do we need to update ourselves?
        self.dirty = True

        # The list of displayables we use.
        self.displayables = None

    def set_text(self, text, scope=None, substitute=False):

        if not isinstance(text, list):
            text = [ text ]

        self.text = [ ]

        # Perform substitution as necessary.
        for i in text:
            if isinstance(i, basestring):
                if substitute is not False:
                    i = renpy.substitutions.substitute(i, scope, substitute)

                i = unicode(i)

            self.text.append(i)

        self.dirty = True

    def set_ctc(self, ctc):
        self.ctc = ctc
        self.dirty = True

    def update(self):
        """
        This needs to be called after text has been updated, but before
        any layout objects are created.
        """

        self.dirty = False

        self.kill_layout()

        text = self.text

        # Decide the portion of the text to show quickly, the part to
        # show slowly, and the part not to show (but to lay out).
        if self.start is not None:
            start_string = text[0][:self.start]
            mid_string = text[0][self.start:self.end]
            end_string = text[0][self.end:]

            if start_string:
                start_string = start_string + "{_start}"

            if end_string:
                end_string = "{_end}" + end_string

            text_split = [ ]

            if start_string:
                text_split.append(start_string)

            text_split.append(mid_string)

            if self.ctc is not None:
                text_split.append(self.ctc)

            if end_string:
                text_split.append(end_string)

            text_split.extend(text[1:])

            text = text_split

        else:
            # Add the CTC.
            if self.ctc is not None:
                text.append(self.ctc)

        # Tokenize the text.
        tokens = self.tokenize(text)

        # self.tokens is a list of pairs, where the first component of
        # each pair is TEXT, NEWLINE, TAG, or DISPLAYABLE, and the second
        # is text or a displayable.
        #
        # self.displayables is the set of displayables used by this
        # Text.
        self.tokens, self.displayables = self.get_displayables(tokens)


    def visit(self):

        if self.dirty or self.displayables is None:
            self.update()

        return list(self.displayables)

    def kill_layout(self):
        """
        Kills the layout of this Text. Used when the text or style
        changes.
        """

        key = id(self)
        layout_cache_old.pop(key, None)
        layout_cache_new.pop(key, None)

    def get_layout(self):
        """
        Gets the layout of this Text, creating a new layout object if
        none exists.
        """

        key = id(self)

        rv = layout_cache_new.get(key, None)

        if rv is None:
            rv = layout_cache_old.get(key, None)

        return rv

    def focus(self, default=False):
        """
        Called when a hyperlink gains focus.
        """

        layout = self.get_layout()

        self.kill_layout()
        renpy.display.render.redraw(self, 0)

        if layout is None:
            return

        hyperlink_focus = self.style.hyperlink_functions[2]
        target = layout.hyperlink_targets.get(renpy.display.focus.argument, None)

        if hyperlink_focus:
            return hyperlink_focus(target)

    def set_style_prefix(self, prefix, root):
        if prefix != self.style.prefix:
            self.kill_layout()

        super(Text, self).set_style_prefix(prefix, root)

    def unfocus(self, default=False):
        """
        Called when a hyperlink loses focus, or isn't focused to begin with.
        """

        self.kill_layout()
        renpy.display.render.redraw(self, 0)

        hyperlink_focus = self.style.hyperlink_functions[2]

        if hyperlink_focus:
            return hyperlink_focus(None)

    def call_slow_done(self, st):
        """
        Called when slow is finished.
        """

        self.slow = False

        if self.slow_done:
            self.slow_done()
            self.slow_done = None

    def event(self, ev, x, y, st):
        """
        Space, Enter, or Click ends slow, if it's enabled.
        """

        if self.slow and renpy.display.behavior.map_event(ev, "dismiss") and self.style.slow_abortable:
            self.call_slow_done(st)
            self.slow = False
            raise renpy.display.core.IgnoreEvent()

        layout = self.get_layout()
        if layout is None:
            return

        for d, xo, yo, _ in layout.displayable_blits:
            rv = d.event(ev, x - xo - layout.xoffset, y - yo - layout.yoffset, st)
            if rv is not None:
                return rv

        if (self.is_focused() and
            renpy.display.behavior.map_event(ev, "button_select")):

            clicked = self.style.hyperlink_functions[1]

            if clicked is not None:
                target = layout.hyperlink_targets.get(renpy.display.focus.argument, None)

                rv = self.style.hyperlink_functions[1](target)
                return rv

    def render(self, width, height, st, at):

        if self.style.vertical:
            height, width = width, height

        # If slow is None, the style decides if we're in slow text mode.
        if self.slow is None:
            if self.style.slow_cps:
                self.slow = True
            else:
                self.slow = False

        if self.dirty or self.displayables is None:
            self.update()

        # Render all of the child displayables.
        renders = { }

        for i in self.displayables:
            renders[i] = renpy.display.render.render(i, width, self.style.size, st, at)

        # Find the layout, and update to the new size and width if necessary.
        layout = self.get_layout()

        if layout is None or layout.width != width or layout.height != height:
            layout = Layout(self, width, height, renders)

            if len(layout_cache_new) > LAYOUT_CACHE_SIZE:
                layout_cache_new.clear()

            layout_cache_new[id(self)] = layout

        # The laid-out size of this Text.
        w, h = layout.size

        # Get the list of blits we want to undertake.
        if not self.slow:
            blits = [ Blit(0, 0, w - layout.xborder, h - layout.yborder) ]
            redraw = None
        else:
            # TODO: Make this changeable.
            blits = layout.blits_typewriter(st)
            redraw = layout.redraw_typewriter(st)

        # Blit text layers.
        rv = renpy.display.render.Render(w, h)

        for o, color, xo, yo in layout.outlines:
            tex = layout.textures[o, color]

            if o:
                oblits = outline_blits(blits, o)
            else:
                oblits = blits

            for b in oblits:

                b_x = b.x
                b_y = b.y
                b_w = b.w
                b_h = b.h

                # Bound to inside texture rectangle.
                if b_x < 0:
                    b_w += b.x
                    b_x = 0

                if b_y < 0:
                    b_h += b_y
                    b_y = 0

                if b_w > w - b_x:
                    b_w = w - b_x
                if b_h > h - b_y:
                    b_h = h - b_y

                if b_w <= 0 or b_h <= 0:
                    continue

                # Expand the blits and offset them as necessary.
                if b_x + b_w == w:
                    b_w += layout.add_right

                if b_y + b_h == h:
                    b_h += layout.add_bottom

                if b_x == 0:
                    b_w += layout.add_left
                else:
                    b_x += layout.add_left

                if b_y == 0:
                    b_h += layout.add_top
                else:
                    b_y += layout.add_top

                # Blit.
                rv.blit(
                    tex.subsurface((b_x, b_y, b_w, b_h)),
                    (b_x + xo + layout.xoffset - o - layout.add_left,
                     b_y + yo + layout.yoffset - o - layout.add_top)
                     )

        # Blit displayables.
        for d, xo, yo, t in layout.displayable_blits:

            if self.slow and t > st:
                continue

            rv.blit(renders[d], (xo + layout.xoffset, yo + layout.yoffset))

        # Add in the focus areas.
        for hyperlink, hx, hy, hw, hh in layout.hyperlinks:
            rv.add_focus(self, hyperlink, hx + layout.xoffset, hy + layout.yoffset, hw, hh)

        # Figure out if we need to redraw or call slow_done.
        if self.slow:
            if redraw is not None:
                renpy.display.render.redraw(self, redraw)
            else:
                self.call_slow_done(st)

        if self.style.vertical:
            vrv = renpy.display.render.Render(rv.height, rv.width)
            vrv.forward = VERT_FORWARD
            vrv.reverse = VERT_REVERSE
            vrv.blit(rv, (rv.height, 0))
            rv = vrv

        return rv


    def tokenize(self, text):
        """
        Convert the text into a list of tokens.
        """

        tokens = [ ]

        for i in text:

            if isinstance(i, unicode):
                tokens.extend(textsupport.tokenize(i))

            elif isinstance(i, str):
                tokens.extend(textsupport.tokenize(unicode(i)))

            elif isinstance(i, renpy.display.core.Displayable):
                tokens.append((DISPLAYABLE, i))

            else:
                raise Exception("Can't display {0!r} as Text.".format(i))

        return tokens


    def get_displayables(self, tokens):
        """
        Goes through the list of tokens. Returns the set of displayables that
        we know about, and an updated list of tokens with all image tags turned
        into displayables.
        """

        displayables = set()
        new_tokens = [ ]

        for t in tokens:

            kind, text = t

            if kind == DISPLAYABLE:
                displayables.add(text)
                new_tokens.append(t)
                continue

            if kind == TAG:
                tag, _, value = text.partition("=")

                if tag == "image":
                    d = renpy.easy.displayable(value)
                    displayables.add(d)
                    new_tokens.append((DISPLAYABLE, d))

                    continue

            new_tokens.append(t)

        return new_tokens, displayables

language_tailor = textsupport.language_tailor

# Compatibility, in case one of these was pickled.
ParameterizedText = extras.ParameterizedText

