# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
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
from renpy.compat import *

import renpy.text

from renpy.text.textsupport import TAG, PARAGRAPH
import renpy.text.textsupport as textsupport

# A list of text tags, mapping from the text tag prefix to if it
# requires a closing tag.
text_tags = dict(
    alpha=True,
    alt=True,
    art=True,
    done=False,
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
def check_text_tags(s):
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
        if text.find('=') != -1:
            text = text[:text.find('=')]

        # Closing tag.
        if text and text[0] == '/':
            if not tag_stack:
                return "Close text tag '%s' does not match an open text tag." % text

            if tag_stack[-1] != text[1:]:
                return "Close text tag '%s' does not match open text tag '%s'." % (text, tag_stack[-1])

            tag_stack.pop()
            continue

        if text not in all_tags:
            return "Text tag '%s' is not known." % text

        if all_tags[text]:
            tag_stack.append(text)

    if tag_stack:
        return "One or more text tags were left open at the end of the string: " + ", ".join([ "'" + i + "'" for i in tag_stack])

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
    """

    def __init__(self, style='default', **properties):
        self.style = style
        self.properties = properties

    _duplicatable = True

    def _duplicate(self, args):

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
