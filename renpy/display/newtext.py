import renpy.display

from renpy.display.textsupport import \
    TAG, TEXT, PARAGRAPH, DISPLAYABLE

import renpy.display.textsupport as textsupport
import renpy.display.ftfont as ftfont

ftfont.init()

# TODO: Remove.
font_cache = { }
font_face_cache = { }


def get_font(font, size, bold, italic, outline, antialias):
    key = (size, bold, italic, outline, antialias)

    rv = font_cache.get(key, None)    
    if rv is not None:
        return rv
    
    face = font_face_cache.get(font, None)
    if face is None:
        face = ftfont.FTFace(renpy.loader.load(font), 0)
        font_face_cache[font] = face
        
        
    rv = ftfont.FTFont(face, size, bold, italic, outline, antialias)
    font_cache[key] = rv
    
    return rv


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
     
    is forbidden. That's a variant that the blit_<method> functions are
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
        
        self.antialias = True
            
        if source is not None:
            self.font = source.font
            self.size = source.size
            self.bold = source.bold
            self.italic = source.italic
            self.underline = source.underline
            self.color = source.color
            self.black_color = source.black_color
            self.hyperlink = source.hyperlink
            self.kerning = source.kerning
            self.cps = source.cps
            
            
    def __repr__(self):
        return "<TextSegment font={font}, size={size}, bold={bold}, italic={italic}, underline={underline}, color={color}, black_color={black_color}, hyperlink={hyperlink}>".format(**self.__dict__)
            
    def take_style(self, style):
        """
        Takes the style of this text segement from the named style object.
        """
        
        self.font = style.font
        self.size = style.size
        self.bold = style.bold
        self.italic = style.italic
        self.underline = style.underline
        self.color = style.color
        self.black_color = style.black_color
        self.hyperlink = None
        self.kerning = style.kerning
        
        cps = style.slow_cps
        if cps is None:
            cps = renpy.game.preferences.text_cps
        
        self.cps = cps * style.slow_cps_multiplier

        # TODO:
        self.cps = 5.0

        

    def glyphs(self, s):
        """
        Return the list of glyphs corresponding to unicode string s.
        """
        
        fo = get_font(self.font, self.size, self.bold, self.italic, 0, self.antialias)
        
        rv = fo.glyphs(s)
        
        # Apply kerning to the glyphs.
        if self.kerning:
            textsupport.kerning(rv, self.kerning)
        
        return rv

    def draw(self, surf, glyphs, xo, yo, override_color, outline):
        """
        Draws the glyphs to surf.
        """
        
        if override_color:
            color = override_color
        else:
            color = self.color
        
        fo = get_font(self.font, self.size, self.bold, self.italic, outline, self.antialias)
        fo.draw(surf, xo, yo, color, glyphs)

    def assign_times(self, gt, glyphs):
        """
        Assigns times to the glyphs. `gt` is the starting time of the first
        glyph, and it returns the starting time of the first glyph in the next
        segment.
        """
        
        return textsupport.assign_times(gt, self.cps, glyphs)

                
class DisplayableSegment(object):
    """
    This is a segment that contains a displayable.
    """

    def __init__(self, d):        
        self.displayable = d
        
    def __repr__(self):
        return "<DisplayableSegment {!r}>".format(self.displayable)
    
    def assign_times(self, gt, glyphs):
        for i in glyphs:
            i.time = gt
            
        return gt
    
class Layout(object):
    """
    Represents the layout of text.
    """

    def __init__(self, text, width, height):
        """
        `text` 
            The text object this layout is associated with.
        `width`, `height` 
            The height of the laid-out text.
        """
        
        self.width = width
        self.height = height
                
        style = text.style
                
        # Slow text that is not before the start segment is displayed
        # instantaneously.
        self.start_segment = None

        # Figure out outlines and other info.
        outlines, xborder, yborder, xoffset, yoffset = self.figure_outlines(style)        
        width -= xborder
        height -= yborder
        
        # The list of outlines.
        self.outlines = outlines
        
        # The borders.
        self.xborder = xborder
        self.yborder = yborder
        
        # The offset of (0, 0) relative to the render.
        self.xoffset = xoffset
        self.yoffset = yoffset
        
        # 1. Turn the text into a list of tokens.
        tokens = self.tokenize(text.text)
        
        # 2. Breaks the text into a list of paragraphs, where each paragraph is 
        # represented as a list of (Segment, text string) tuples. 
        paragraphs = self.segment(tokens, style)

        # The greatest x coordinate of the text.       
        maxx = 0
        
        # The current y, which becomes the maximum height once all paragraphs
        # have been rendered.
        y = 0

        # A list of (segment, glyph_list) pairs for all paragraphs.
        par_seg_glyphs = [ ]

        # The lines.
        lines = [ ]

        # The time at which the next glyph will be displayed.
        gt = 0.0

        for p in paragraphs:

            # TODO: RTL - apply RTL to the text of each segment, then 
            # reverse the order of the segments in each paragraph.
                    
            # 3. Convert each paragraph into a Segment, glyph list. (Store this
            # to use when we draw things.)
            
            # A list of all glyphs in the line.
            all_glyphs = [ ]
            
            # A list of (segment, list of glyph) pairs.
            seg_glyphs = [ ]

            for ts, s in p:
                glyphs = ts.glyphs(s)

                t = (ts, glyphs)                
                seg_glyphs.append(t)
                par_seg_glyphs.append(t)
                
                all_glyphs.extend(glyphs)

            # TODO: RTL - Reverse the segments and the glyphs within each
            # segment, so that we can use LTR linebreaking algorithms.
            
            # Tag the glyphs that are eligible for line breaking, and if
            # they should be included or excluded from the end of a line.
            # TODO: Pick between western and eastasian.
            textsupport.annotate_western(all_glyphs)
                     
            # Break the paragraph up into lines.
            # TODO: subtitle linebreak.
            textsupport.linebreak_greedy(all_glyphs, width, width)
                        
            # Figure out the time each glyph will be drawn. 
            for ts, glyphs in seg_glyphs:
                gt = ts.assign_times(gt, glyphs)
                                      
            # TODO: RTL - Reverse the glyphs in each line, back to RTL order,
            # now that we have lines. 
            
            # Taking into account indentation, kerning, justification, and text_align,
            # lay out the X coordinate of each glyph.
            
            w = textsupport.place_horizontal(all_glyphs, 0, 0, 0)
            if w > maxx:
                maxx = w
           
            # Figure out the line height, line spacing, and the y coordinate of each
            # glyph. 
            l, y = textsupport.place_vertical(all_glyphs, y, 0, 0)
            lines.extend(l)

            # TODO: Place the RUBY_TOP glyphs.

            # Combine continguous hyperlinks ont a line into a single focus block.
            
        # Figure out the size of the texture. (This is a little over-sized,
        # but it simplifies the code to not have to care about borders on a 
        # per-outline basis.)
        size = (maxx + xborder, y + yborder)
        self.size = size

        # A map from (outline, color) to a texture.
        self.textures = { }

        for o, color, _xo, _yo in outlines:
            key = (o, color)
            
            if key in self.textures:
                continue
            
            # Create the texture.
            surf = renpy.display.pgrender.surface(size, True)
            
            for ts, glyphs in par_seg_glyphs:
                ts.draw(surf, glyphs, 0, 0, color, o)
    
            renpy.display.draw.mutated_surface(surf)
            tex = renpy.display.draw.load_texture(surf)
        
            self.textures[key] = tex
        
        # Compute the max time for all lines, and the max max time.
        self.max_time = textsupport.max_times(lines)
        
        # Store the lines, so we have them for typeout.
        self.lines = lines
        
        # TODO: Log an overflow if the laid out width or height is larger than the
        # size of the provided area.
            
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
                raise Exception("Can't display {!r} as Text.".format(i))
                
        return tokens    
    
    def segment(self, tokens, style):
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
                
        for type, text in tokens:
            
            if type == PARAGRAPH:
                
                # Note that this code is duplicated for the p tag, below.
                if not line:
                    line.append((tss[-1], u" "))
                
                paragraphs.append(line)
                line = [ ]
                
                continue
                
            elif type == TEXT:
                line.append((tss[-1], text))
                continue
            
            elif type == DISPLAYABLE:
                line.append((DisplayableSegment(text), u""))
                continue
            
            # Otherwise, we have a text tag.
            
            tag, _, value = text.partition("=")
            
            if tag[0] == "/":
                tss.pop()
                
                if not tss:                
                    raise Exception("%r closes a text tag that isn't open." % text)
            
            elif tag == "_start":
                push()
                tss.pop(-2)
                self.start_segment = tss 
                
            elif tag == "p":
                # Duplicated from the newline tag.
                
                if not line:
                    line.append((ts[-1], " "))
                
                paragraphs.append(line)
                line = [ ]

            elif tag == "w":
                pass
            
            elif tag == "fast":
                pass
            
            elif tag == "nw":
                pass
            
            elif tag == "a":
                hyperlink_styler = self.style.hyperlink_functions[0]
                    
                if hyperlink_styler:                                        
                    hls = hyperlink_styler(value)
                else:
                    hls = self.style

                old_prefix = hls.prefix

                link = len(self.hyperlink_targets) + 1
                self.hyperlink_targers[link] = value

                if renpy.display.focus.argument == link:
                    hls.set_prefix("hover_")
                else:
                    hls.set_prefix("idle_")

                ts = push()
                ts.take_style(hls)
                ts.hyperlink = link

                hls.set_prefix(old_prefix)

                continue
 
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
                
            else:
                raise Exception("Unknown text tag %r" % text)
            
        if not line:
            line.append((ts, ""))
                
        paragraphs.append(line)

        return paragraphs

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
        
        width, _height = self.size
        
        rv = [ ]
        
        max_y = 0
        
        for l in self.lines:
            
            if l.max_time > st:
                break
            
            max_y = l.y + l.height
            
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
                
        if min_x < max_x:
            rv.append(Blit(min_x, l.y, max_x - min_x, l.height))
            
        return rv
        
        

class NewText(renpy.display.core.Displayable):
    
    def __init__(self, text, style='default', replaces=None, **properties):
                
        super(NewText, self).__init__(style=style, **properties)
           
        if not isinstance(text, list):
            text = [ text ]
        
        self.text = text
                           
        self.layout = None
        self.slow = True
        
        
    def render(self, width, height, st, at):
        
        if self.layout is None or self.layout.width != width or self.layout.height != height:
            layout = self.layout = Layout(self, width, height)
        else:
            layout = self.layout
            
        w, h = layout.size            
        rv = renpy.display.render.Render(w, h)
            
        if self.slow:            
            # TODO: Make this changable.
            blits = layout.blits_typewriter(st)
            
        else:
            blits = [ Blit(0, 0, w - layout.xborder, h - layout.yborder) ]
        
        # Draw everything.                            
        for o, color, xo, yo in layout.outlines:
            tex = layout.textures[o, color]
            
            if o:
                oblits = outline_blits(blits, o)            
            else:
                oblits = blits            
        
            for b in oblits:
            
                rv.blit(
                    tex.subsurface((b.x, b.y, b.w, b.h)),
                    (b.x + xo + layout.xoffset - o, b.y + yo + layout.yoffset - o))

        
        # TODO: Deal with really slow text drawing, by pausing > 0.
        if self.slow:
            renpy.display.render.redraw(self, 0)

        # TODO: Deal with displayables.
        
        return rv
        
        

        
            
        
