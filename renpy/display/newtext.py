import renpy.display
import time

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

    def glyphs(self, s):
        """
        Return the list of glyphs corresponding to unicode string s.
        """
        
        start = time.time()
        
        fo = get_font(self.font, self.size, self.bold, self.italic, 0, self.antialias)
        
        print " Get", time.time() - start
        start = time.time()
        
        rv = fo.glyphs(s)
        
        print " Fon", time.time() - start
        start = time.time()
        
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

                
class DisplayableSegment(object):
    """
    This is a segment that contains a displayable.
    """

    def __init__(self, d):        
        self.displayable = d
        
    def __repr__(self):
        return "<DisplayableSegment {!r}>".format(self.displayable)
    
    
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
        
        start = time.time()
         
        # 1. Turn the text into a list of tokens.
        tokens = self.tokenize(text.text)
        
        print "Tok", time.time() - start
        start = time.time()
        
        # 2. Breaks the text into a list of paragraphs, where each paragraph is 
        # represented as a list of (Segment, text string) tuples. 
        paragraphs = self.segment(tokens)

        print "Seg", time.time() - start
        start = time.time()

        # The greatest x coordinate of the text.       
        maxx = 0
        
        # The current y, which becomes the maximum height once all paragraphs
        # have been rendered.
        y = 0

        # A list of (segment, glyph_list) pairs for all paragraphs.
        par_seg_glyphs = [ ]

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

            print "Gly", time.time() - start
            start = time.time()

            # TODO: Apply kerning here.
                        
            # TODO: RTL - Reverse the segments and the glyphs within each
            # segment, so that we can use LTR linebreaking algorithms.
                        
            # Tag the glyphs that are eligible for line breaking, and if
            # they should be included or excluded from the end of a line.
            
            # TODO: Pick between western and eastasian.
            textsupport.annotate_western(all_glyphs)
                     
            print "Ann", time.time() - start
            start = time.time()
                     
                     
            # Break the paragraph up into lines.
            # TODO: subtitle linebreak.
            textsupport.linebreak_greedy(all_glyphs, width, width)
            
            print "Lbr", time.time() - start
            start = time.time()

            
            # Figure out the time each glyph will be drawn. 
              
            # TODO: RTL - Reverse the glyphs in each line, back to RTL order,
            # now that we have lines. 
            
            # Taking into account indentation, kerning, justification, and text_align,
            # lay out the X coordinate of each glyph.
            
            w = textsupport.place_horizontal(all_glyphs, 0, 0, 0)
            if w > maxx:
                maxx = w
            
            print "Hor", time.time() - start
            start = time.time()

            
            # Figure out the line height, line spacing, and the y coordinate of each
            # glyph. 
            lines = textsupport.place_vertical(all_glyphs, y, 0, 0)
            y = lines[-1]

            print "Ver", time.time() - start
            start = time.time()


            # TODO: Place the RUBY_TOP glyphs.

            # Combine continguous hyperlinks ont a line into a single focus block.
            
            # Done with layout! Now drawing each segment and glyph in order will be enough
            # to render the text to a displayable.

        size = (maxx + xborder, y + yborder)
        print "SIZE", size

        surf = renpy.display.pgrender.surface(size, True)
        
        for o, color, xo, yo in outlines:
            for ts, glyphs in par_seg_glyphs:
                ts.draw(surf, glyphs, xoffset + xo - o, yoffset + yo, color, o)

        print "Dra", time.time() - start
        start = time.time()


        renpy.display.draw.mutated_surface(surf)
        self.texture = renpy.display.draw.load_texture(surf)
        
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
    
    def segment(self, tokens):
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
        ts.take_style(renpy.store.style.default)
                
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
                    line.append((ts[-1], " "))
                
                paragraphs.append(line)
                line = [ ]
                
                continue
                
            elif type == TEXT:
                line.append((tss[-1], text))
                continue
            
            elif type == DISPLAYABLE:
                line.append((DisplayableSegment(text), ""))
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
                
        for o, c, x, y in outlines:
            
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
        

class NewText(renpy.display.core.Displayable):
    
    def __init__(self, text, style='default', replaces=None, **properties):
                
        super(NewText, self).__init__(style=style, **properties)
           
        if not isinstance(text, list):
            text = [ text ]
        
        self.text = text
                           
        self.layout = None

        
    def render(self, width, height, st, at):
        
        import time
        start = time.time()
        
        if self.layout is None or self.layout.width != width or self.layout.height != height:
            self.layout = Layout(self, width, height)
        
        tex = self.layout.texture
        w, h = tex.get_size()
           
        rv = renpy.display.render.Render(w, h)
        rv.blit(tex, (0, 0))

        print "NEW", time.time() - start
        
        return rv
        
        

        
            
        
