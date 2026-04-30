# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode  # *


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
    feature=True,
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
    shader=True,
    rt=True,
    rb=True,
    k=True,
    cps=True,
    space=False,
    vspace=False,
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

    tag_stack = []

    for type, text in tokens:
        if type != TAG:
            continue

        if text[0] == "#":
            continue

        # Strip off arguments for tags.
        text = text.partition("=")[0]
        text = text.partition(":")[0]

        if text.find("=") != -1:
            text = text[: text.find("=")]

        # Closing tag.
        if text and text[0] == "/":
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

    rv = []

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


def filter_alt_text(s) -> str:
    """
    Returns a copy of `s` with the contents of text tags that shouldn't be in
    alt text filtered. This returns just the text to say, with no text tags
    at all in it.
    """

    tokens = textsupport.tokenize(str(s))

    if (
        renpy.config.custom_text_tags
        or renpy.config.self_closing_custom_text_tags
        or (renpy.config.replace_text is not None)
    ):
        tokens = renpy.text.text.Text.apply_custom_tags(tokens)

    rv = []

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
            rv.append(text._tts(raw=False))
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

    def __init__(self, style="default", **properties):
        self.style = style
        self.properties = properties

    _duplicatable = True

    def _duplicate(self, args):
        if args.lint:
            return renpy.text.text.Text("", style=self.style, **self.properties)

        if len(args.args) == 0:
            raise Exception("'%s' takes a single string parameter." % " ".join(args.name))

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

    glyphs = []

    for c in str(s):
        eaw = unicodedata.east_asian_width(c)

        if (eaw == "F") or (eaw == "W"):
            gwidth = 20
        elif eaw == "A":
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
    Reencodes `s` to the Thai C90 encoding, a legacy font-specific scheme
    used to render Thai text with correct glyph positioning in C90-compatible fonts
    by mapping character sequences to PUA glyph code points.
    """

    # Copyright (c) 2021 SahabandhSthabara, Saamkhaih Kyakya
    # MIT License.
    # Taken from https://gitlab.com/sahabandha/renpy-thai-font-adjuster/

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

    # Precompute lookup tables
    TOP_LEFT = str.maketrans(
        '\u0E48\u0E49\u0E4A\u0E4B\u0E4C',
        '\uF713\uF714\uF715\uF716\uF717'
    )
    TOP_LOWLEFT = str.maketrans(
        '\u0E48\u0E49\u0E4A\u0E4B\u0E4C',
        '\uF705\uF706\uF707\uF708\uF709'
    )
    TOP_LOW = str.maketrans(
        '\u0E48\u0E49\u0E4A\u0E4B\u0E4C',
        '\uF70A\uF70B\uF70C\uF70D\uF70E'
    )
    UPPER_LEFT = str.maketrans(
        '\u0E31\u0E34\u0E35\u0E36\u0E37\u0E4D\u0E47',
        '\uF710\uF701\uF702\uF703\uF704\uF711\uF712'
    )
    LOWER_DESC = str.maketrans(
        '\u0E38\u0E39\u0E3A',
        '\uF718\uF719\uF71A'
    )
    UPPER      = frozenset('\u0E31\u0E34\u0E35\u0E36\u0E37\u0E47\u0E4D')
    BASE_ASC   = frozenset('\u0E1B\u0E1D\u0E1F\u0E2C')
    BASE_DESC  = frozenset('\u0E0E\u0E0F')
    result: list[str] = []
    length = len(s)
    z = 0
    while z < length:
        c = s[z]
        if c == '\u0E33':
            base = ''
            if z >= 2 and '\u0E38' <= s[z-1] <= '\u0E3A':
                base = s[z - 2]
            elif z >= 1:
                base = s[z - 1]

            if base in BASE_ASC:
                result.append('\uF711')
            else:
                result.append('\u0E4D')
            result.append('\u0E32')
            z += 1
            continue
        if '\u0E48' <= c <= '\u0E4C' and z > 0:
            prev = s[z - 1]
            prev2 = s[z - 2] if z > 1 else ''
            base = s[z-2] if z >= 2 and '\u0E38' <= prev <= '\u0E3A' else prev
            if z + 1 < length:
                next_c = s[z+1]
                if next_c == '\u0E4D':
                    if base in BASE_ASC:
                        result.append('\uF711')
                        result.append(c.translate(TOP_LEFT))
                    else:
                        result.append('\u0E4D')
                        result.append(c)
                    z += 2
                    continue
                if next_c == '\u0E33':
                    if base in BASE_ASC:
                        result.append('\uF711')
                        result.append(c.translate(TOP_LEFT))
                    else:
                        result.append('\u0E4D')
                        result.append(c)
                    result.append('\u0E32')
                    z += 2
                    continue
            if prev in UPPER:
                if prev2 in BASE_ASC:
                    result.append(c.translate(TOP_LEFT))
                else :
                    result.append(c)
            elif base in BASE_ASC:
                result.append(c.translate(TOP_LOWLEFT))
            else:
                result.append(c.translate(TOP_LOW))
            z += 1
            continue
        elif c in UPPER and z > 0 and s[z - 1] in BASE_ASC:
            result.append(c.translate(UPPER_LEFT))
            z += 1
            continue
        elif '\u0E38' <= c <= '\u0E3A' and z > 0 and s[z - 1] in BASE_DESC:
            result.append(c.translate(LOWER_DESC))
            z += 1
            continue
        elif c == '\u0E0D' and z < length - 1 and '\u0E38' <= s[z + 1] <= '\u0E3A':
            result.append('\uF70F')
            z += 1
            continue
        elif c == '\u0E10' and z < length - 1 and '\u0E38' <= s[z + 1] <= '\u0E3A':
            result.append('\uF700')
            z += 1
            continue
        result.append(c)
        z += 1
    return ''.join(result)
