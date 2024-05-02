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

# Other text-related things.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *



import renpy

from renpy.text.textsupport import DISPLAYABLE, PARAGRAPH, TAG
import renpy.text.textsupport as textsupport

# A list of text tags, mapping from the text tag prefix to if it
# requires a closing tag.
text_tags = dict(
    alpha=True,
    alt=True,
    art=True,
    axis=True,
    done=False,
    instance=True,
    image=False,
    p=False,
    w=False,
    fast=False,
    b=True,
    i=True,
    u=True,
    a=True,
    plain=True,
    font=True,
    color=True,
    outlinecolor=True,
    size=True,
    noalt=True,
    nw=False,
    s=True,
    rt=True,
    rb=True,
    k=True,
    cps=True,
    space=False,
    vspace=False
    )

text_tags[""] = True


# This checks the text tags in a string to be sure they are all matched, and
# properly nested. It returns an error message, or None if the line is okay.
def check_text_tags(s, check_unclosed=False):
    """
    :doc: lint

    Checks the text tags in s for correctness. Returns an error string if there is
    an error, or None if there is no error.
    """

    all_tags = dict(text_tags)

    custom_tags = renpy.config.custom_text_tags
    if custom_tags:
        all_tags.update(custom_tags)

    self_closing_custom_tags = renpy.config.self_closing_custom_text_tags
    if self_closing_custom_tags:
        all_tags.update(dict.fromkeys(self_closing_custom_tags, False))

    try:
        tokens = textsupport.tokenize(str(s))
    except Exception as e:
        return e.args[0]

    tag_stack = [ ]

    for type, text in tokens: # @ReservedAssignment
        if type != TAG:
            continue

        if text[0] == "#":
            continue

        # Strip off arguments for tags.
        text = text.partition('=')[0]
        text = text.partition(':')[0]

        if text.find('=') != -1:
            text = text[:text.find('=')]

        # Closing tag.
        if text and text[0] == '/':
            if not tag_stack:
                return "Close text tag '{%s}' does not match an open text tag." % text

            if tag_stack[-1] != text[1:]:
                return "Close text tag '{%s}' does not match open text tag '{%s}'." % (text, tag_stack[-1])

            tag_stack.pop()
            continue

        if text not in all_tags:
            return "Text tag '%s' is not known." % text

        if all_tags[text]:
            tag_stack.append(text)

    if check_unclosed and tag_stack:
            return "One or more text tags were left open at the end of the string: " + ", ".join(repr(i) for i in tag_stack)

    return None


def filter_text_tags(s, allow=None, deny=None):
    """
    :doc: text_utility

    Returns a copy of `s` with the text tags filtered. Exactly one of the `allow` and `deny` keyword
    arguments must be given.

    `allow`
        A set of tags that are allowed. If a tag is not in this list, it is removed.

    `deny`
        A set of tags that are denied. If a tag is not in this list, it is kept in the string.
    """

    if (allow is None) and (deny is None):
        raise Exception("Only one of the allow and deny keyword arguments should be given to filter_text_tags.")

    if (allow is not None) and (deny is not None):
        raise Exception("Only one of the allow and deny keyword arguments should be given to filter_text_tags.")

    tokens = textsupport.tokenize(str(s))

    rv = [ ]

    for tokentype, text in tokens:

        if tokentype == PARAGRAPH:
            rv.append("\n")
        elif tokentype == TAG:
            kind = text.partition("=")[0]
            kind = kind.partition(":")[0]

            if kind and (kind[0] == "/"):
                kind = kind[1:]

            if allow is not None:
                if kind in allow:
                    rv.append("{" + text + "}")
            else:
                if kind not in deny:
                    rv.append("{" + text + "}")
        else:
            rv.append(text.replace("{", "{{"))

    return "".join(rv)


def filter_alt_text(s):
    """
    Returns a copy of `s` with the contents of text tags that shouldn't be in
    alt text filtered. This returns just the text to say, with no text tags
    at all in it.
    """

    tokens = textsupport.tokenize(str(s))

    if renpy.config.custom_text_tags or renpy.config.self_closing_custom_text_tags or (renpy.config.replace_text is not None):
        tokens = renpy.text.text.Text.apply_custom_tags(tokens)

    rv = [ ]

    active = set()

    for tokentype, text in tokens:

        if tokentype == PARAGRAPH:
            rv.append("\n")
        elif tokentype == TAG:
            kind = text.partition("=")[0]

            if kind.startswith("/"):
                kind = kind[1:]
                end = True
            else:
                end = False

            if kind in renpy.config.tts_filter_tags:
                if end:
                    active.discard(kind)
                else:
                    active.add(kind)
        elif tokentype == DISPLAYABLE:
            rv.append(text._tts())
        else:
            if not active:
                rv.append(text)

    return "".join(rv)


class ParameterizedText(object):
    """
    :name: ParameterizedText
    :doc: text

    This is a displayable that can be shown with an additional string
    parameter, which then shows that string as if it was an image.
    This is usually used as part of the pre-defined ``text`` image.

    For example, one can do::

        show text "Hello, World" at truecenter
        with dissolve
        pause 1
        hide text
        with dissolve

    You can use ParameterizedText directly to define similar images with
    different style properties. For example, one can write::

        image top_text = ParameterizedText(xalign=0.5, yalign=0.0)

        label start:
            show top_text "This text is shown at the center-top of the screen"
    """

    def __init__(self, style='default', **properties):
        self.style = style
        self.properties = properties

    _duplicatable = True

    def _duplicate(self, args):

        if args.lint:
            return renpy.text.text.Text("", style=self.style, **self.properties)

        if len(args.args) == 0:
            raise Exception("'%s' takes a single string parameter." % ' '.join(args.name))

        param = "".join(args.args)
        string = renpy.python.py_eval(param)

        return renpy.text.text.Text(string, style=self.style, **self.properties)


def textwrap(s, width=78, asian=False):
    """
    Wraps the unicode string `s`, and returns a list of strings.

    `width`
        The number of half-width characters that fit on a line.
    `asian`
        True if we should make ambiguous width characters full-width, as is
        done in Asian encodings.
    """

    import unicodedata

    glyphs = [ ]

    for c in str(s):

        eaw = unicodedata.east_asian_width(c)

        if (eaw == "F") or (eaw == "W"):
            gwidth = 20
        elif (eaw == "A"):
            if asian:
                gwidth = 20
            else:
                gwidth = 10
        else:
            gwidth = 10

        g = textsupport.Glyph()
        g.character = ord(c)
        g.ascent = 10
        g.line_spacing = 10
        g.width = gwidth
        g.advance = gwidth

        glyphs.append(g)

    textsupport.annotate_unicode(glyphs, False, 2)
    renpy.text.texwrap.linebreak_tex(glyphs, width * 10, width * 10, False)
    return textsupport.linebreak_list(glyphs)


def thaic90(s):
    """
    Reencodes `s` to the Thai C90 encoding, which is used by Thai-specific
    fonts to combine base characters, upper vowels, lower vowls, and tone marks
    into singe precomposed characters in thje unicode private use area.
    """


    # Copyright (c) 2021 SahabandhSthabara, Saamkhaih Kyakya
    # MIT License.
    # Taken from https://gitlab.com/sahabandha/renpy-thai-font-adjuster/-/blob/main/renpythaic90.py

    # http://www.bakoma-tex.com/doc/fonts/enc/c90/c90.pdf
    # ========== EXTENDED CHARACTER TABLE ==========
    # F700:     uni0E10.descless    (base.descless)
    # F701~04:  uni0E34~37.left     (upper.left)
    # F705~09:  uni0E48~4C.lowleft  (top.lowleft)
    # F70A~0E:  uni0E48~4C.low      (top.low)
    # F70F:     uni0E0D.descless    (base.descless)
    # F710~12:  uni0E31,4D,47.left  (upper.left)
    # F713~17:  uni0E48~4C.left     (top.left)
    # F718~1A:  uni0E38~3A.low      (lower.low)
    # ==============================================

    def isBase(c):
        return (u'\u0E01' <= c <= u'\u0E30') or c == u"\u0E30" or c == u"\u0E40" or c == u"\u0E41"

    def isBaseAsc(c):
        return c == u'\u0E1B' or c == u'\u0E1D' or c == u'\u0E1F' or c == u'\u0E2C'

    def isBaseDesc(c):
        return c == u'\u0E0E' or c == u'\u0E0F'

    def isTop(c):
        # Tone Mark, THANTHAKHAT
        if u"\u0E48" <= c <= u"\u0E4C":
            return True

    def isLower(c):
        #SARA U, SARA UU, PHINTHU
        return c >= u"\u0E38" and c <= u"\u0E3A"

    def isUpper(c):
        return c == u'\u0E31' or c == u'\u0E34' or c == u'\u0E35' or c == u'\u0E36' or c == u'\u0E37' or c == u'\u0E47' or c == u'\u0E4D'

    rv = [ ]

    # [sara am] -> [nikhahit] [sara aa]
    s = s.replace(u"\u0E33", u"\u0E4D\u0E32")
    s = s.replace(u"\u0E48\u0E4D", u"\u0E4D\u0E48")
    s = s.replace(u"\u0E49\u0E4D", u"\u0E4D\u0E49")
    s = s.replace(u"\u0E4A\u0E4D", u"\u0E4D\u0E4A")
    s = s.replace(u"\u0E4B\u0E4D", u"\u0E4D\u0E4B")
    s = s.replace(u"\u0E4C\u0E4D", u"\u0E4D\u0E4C")

    length = len(s)
    for z in range(length):
        c = s[z]

        #  [base] ~ [top]
        if isTop(c) and z > 0:
                # [base]             [top] -> [base]             [top.low]
                # [base]     [lower] [top] -> [base]     [lower] [top.low]
                # [base.asc]         [top] -> [base.asc]         [top.lowleft]
                # [base.asc] [lower] [top] -> [base.asc] [lower] [top.lowleft]
            b = s[z - 1];
            if isLower(b) and z > 0:
                b = s[z -2]
            if isBase(b):
                Nikhahit = (z < length - 1 and (s[z + 1] == u'\u0E33' or s[z + 1] == u'\u0E4D'))
                if isBaseAsc(b):
                    if Nikhahit:
                        # [base.asc] [nikhahit] [top] -> [base.asc] [nikhahit] [top.left]
                        choices = {
                            u'\u0E48': u'\uF713',
                            u'\u0E49': u'\uF714',
                            u'\u0E4A': u'\uF715',
                            u'\u0E4B': u'\uF716',
                            u'\u0E4C': u'\uF717'
                            }
                        c = choices.get(c, 'error')
                    else:
                        choices = {
                            u'\u0E48': u'\uF705',
                            u'\u0E49': u'\uF706',
                            u'\u0E4A': u'\uF707',
                            u'\u0E4B': u'\uF708',
                            u'\u0E4C': u'\uF709'
                            }
                        c = choices.get(c, 'error')
                else:
                    if Nikhahit == False:
                        choices = {
                            u'\u0E48': u'\uF70A',
                            u'\u0E49': u'\uF70B',
                            u'\u0E4A': u'\uF70C',
                            u'\u0E4B': u'\uF70D',
                            u'\u0E4C': u'\uF70E'
                            }
                        c = choices.get(c, 'error')
            # [base.asc] [upper] [top] -> [base.asc] [upper] [top.left]
            if (z > 1 and isUpper(s[z -1]) and isBaseAsc(s[z - 2])):
                choices = {
                    u'\u0E48': u'\uF713',
                    u'\u0E49': u'\uF714',
                    u'\u0E4A': u'\uF715',
                    u'\u0E4B': u'\uF716',
                    u'\u0E4C': u'\uF717'
                    }
                c = choices.get(c, 'error')
        # [base.asc] [upper] -> [base.asc] [upper-left]
        elif (isUpper(c)and z > 0 and isBaseAsc(s[z -1])):
            choices = {
                u'\u0E31': u'\uF710',
                u'\u0E34': u'\uF701',
                u'\u0E35': u'\uF702',
                u'\u0E36': u'\uF703',
                u'\u0E37': u'\uF704',
                u'\u0E4D': u'\uF711',
                u'\u0E47': u'\uF712'
                }
            c = choices.get(c, 'error')
        elif (isLower(c) and z > 0 and isBaseDesc(s[z -1])):
            choices = {
                u'\u0E38': u'\uF718',
                u'\u0E39': u'\uF719',
                u'\u0E3A': u'\uF71A'
                }
            c = choices.get(c, 'error')
        elif (c == u'\u0E0D' and z < length -1 and isLower(s[z + 1])):
            c = u'\uF70F'
        elif (c == u'\u0E10' and z < length -1 and isLower(s[z + 1])):
            c = u'\uF700'
        else:
            c = s[z]

        rv.append(c)

    return u''.join(rv)



class TextShader(object):
    """
    This stores information about a text shader.
    """

    def __init__(self, shader, extra_slow_time=0, redraw=None, redraw_when_slow=0, **kwargs):
        """
        `shader`
            The shader to apply to the text. This can be a string, or a list of strings.
            The shader or shaders must be registered with :func:`renpy.register_shader`.

        `extra_slow_time`
            Extra time to add to the slow time effect beyond what Ren'Py will compute from
            the current characters per second. This is useful for shaders that
            might take more time to transition a character than the default time.
            If True, the shader is always updated.

        `redraw`
            The amount in time in seconds before the text is redrawn, after
            all slow text has been show and `extra_slow_time` has passed.

        `redraw_when_slow`
            The amount of time in seconds before the text is redrawn when showing
            slow text.

        Keyword argument beginning with ``u_`` are passed as uniforms to the shader.
        """

        # A tuple of shaders to apply to text.
        if isinstance(shader, basestring):
            self.shader = (shader,)
        else:
            self.shader = tuple(shader)

        # The amount of extra time to add to the slow effect, in addition
        # to the time Ren'Py would normally take to display the text.
        self.extra_slow_time = extra_slow_time

        # The redraw time.
        self.redraw = redraw

        # The redraw when showing slow text.
        self.redraw_when_slow = redraw_when_slow

        # A tuple of uniform name, value pairs.
        uniforms = { }

        for k, v in kwargs:
            if k.startswith("u_"):

                if v and v[0] == "#":
                    v = renpy.easy.color(v).rgba

                uniforms[k] = v
            else:
                raise ValueError("Unknown keyword argument %r." % (k,))

        self.uniforms = tuple(sorted(uniforms.items()))

        self.key = (
            self.shader,
            self.extra_slow_time,
            self.redraw,
            self.redraw_when_slow,
            self.uniforms
            )

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return self.key == other.key

    def copy(self, new_uniforms):
        """
        Create a copy of this TextShader, with the uniforms updated with
        the new uniforms.
        """

        rv = TextShader(None)
        rv.__dict__.update(self.__dict__)

        uniforms = dict(self.uniforms)
        uniforms.update(new_uniforms)
        rv.uniforms = tuple(sorted(uniforms.items()))

        return rv

def create_textshader_args_dict(s):
    """
    Given a string, create a textshader uniforms from it.
    """

    rv = { }

    for arg in s.split(":"):
        try:
            uniform, _, value = arg.split("=")

            uniform = uniform.strip()
            value = value.strip()

            if not uniform.startswith("u_"):
                raise ValueError()

            if value and (value[0] == "#"):
                numeric_value = renpy.easy.color(value).rgba
            else:
                numeric_value = tuple(float(i) for i in value.split(","))

            if len(numeric_value) == 1:
                rv[uniform] = numeric_value[0]
            else:
                rv[uniform] = numeric_value

        except Exception as e:
            raise ValueError("Expected a uniform assignment, but got %r." % arg)

    return rv


def check_textshader(o):
    if o is None:
        return o

    if isinstance(o, TextShader):
        return o

    if isinstance(o, basestring):
        name, _, args = o.partition(":")

        rv = renpy.config.text_shaders.get(o, None)

        if rv is not None:
            if args:
                rv = rv.copy(create_textshader_args_dict(args))

        else:
            raise Exception("Unknown text shader %r." % o)


    raise Exception("Expected a TextShader, but got %r." % o)
