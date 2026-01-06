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
    Reencodes `s` to the Thai C90 encoding, which is used by Thai-specific
    fonts to combine base characters, upper vowels, lower vowls, and tone marks
    into singe precomposed characters in the unicode private use area.
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
        return ("\u0e01" <= c <= "\u0e30") or c == "\u0e30" or c == "\u0e40" or c == "\u0e41"

    def isBaseAsc(c):
        return c == "\u0e1b" or c == "\u0e1d" or c == "\u0e1f" or c == "\u0e2c"

    def isBaseDesc(c):
        return c == "\u0e0e" or c == "\u0e0f"

    def isTop(c):
        # Tone Mark, THANTHAKHAT
        if "\u0e48" <= c <= "\u0e4c":
            return True

    def isLower(c):
        # SARA U, SARA UU, PHINTHU
        return c >= "\u0e38" and c <= "\u0e3a"

    def isUpper(c):
        return (
            c == "\u0e31"
            or c == "\u0e34"
            or c == "\u0e35"
            or c == "\u0e36"
            or c == "\u0e37"
            or c == "\u0e47"
            or c == "\u0e4d"
        )

    rv = []

    # [sara am] -> [nikhahit] [sara aa]
    s = s.replace("\u0e33", "\u0e4d\u0e32")
    s = s.replace("\u0e48\u0e4d", "\u0e4d\u0e48")
    s = s.replace("\u0e49\u0e4d", "\u0e4d\u0e49")
    s = s.replace("\u0e4a\u0e4d", "\u0e4d\u0e4a")
    s = s.replace("\u0e4b\u0e4d", "\u0e4d\u0e4b")
    s = s.replace("\u0e4c\u0e4d", "\u0e4d\u0e4c")

    length = len(s)
    for z in range(length):
        c = s[z]

        #  [base] ~ [top]
        if isTop(c) and z > 0:
            # [base]             [top] -> [base]             [top.low]
            # [base]     [lower] [top] -> [base]     [lower] [top.low]
            # [base.asc]         [top] -> [base.asc]         [top.lowleft]
            # [base.asc] [lower] [top] -> [base.asc] [lower] [top.lowleft]
            b = s[z - 1]
            if isLower(b) and z > 0:
                b = s[z - 2]
            if isBase(b):
                Nikhahit = z < length - 1 and (s[z + 1] == "\u0e33" or s[z + 1] == "\u0e4d")
                if isBaseAsc(b):
                    if Nikhahit:
                        # [base.asc] [nikhahit] [top] -> [base.asc] [nikhahit] [top.left]
                        choices = {
                            "\u0e48": "\uf713",
                            "\u0e49": "\uf714",
                            "\u0e4a": "\uf715",
                            "\u0e4b": "\uf716",
                            "\u0e4c": "\uf717",
                        }
                        c = choices.get(c, "error")
                    else:
                        choices = {
                            "\u0e48": "\uf705",
                            "\u0e49": "\uf706",
                            "\u0e4a": "\uf707",
                            "\u0e4b": "\uf708",
                            "\u0e4c": "\uf709",
                        }
                        c = choices.get(c, "error")
                else:
                    if Nikhahit == False:
                        choices = {
                            "\u0e48": "\uf70a",
                            "\u0e49": "\uf70b",
                            "\u0e4a": "\uf70c",
                            "\u0e4b": "\uf70d",
                            "\u0e4c": "\uf70e",
                        }
                        c = choices.get(c, "error")
            # [base.asc] [upper] [top] -> [base.asc] [upper] [top.left]
            if z > 1 and isUpper(s[z - 1]) and isBaseAsc(s[z - 2]):
                choices = {
                    "\u0e48": "\uf713",
                    "\u0e49": "\uf714",
                    "\u0e4a": "\uf715",
                    "\u0e4b": "\uf716",
                    "\u0e4c": "\uf717",
                }
                c = choices.get(c, "error")
        # [base.asc] [upper] -> [base.asc] [upper-left]
        elif isUpper(c) and z > 0 and isBaseAsc(s[z - 1]):
            choices = {
                "\u0e31": "\uf710",
                "\u0e34": "\uf701",
                "\u0e35": "\uf702",
                "\u0e36": "\uf703",
                "\u0e37": "\uf704",
                "\u0e4d": "\uf711",
                "\u0e47": "\uf712",
            }
            c = choices.get(c, "error")
        elif isLower(c) and z > 0 and isBaseDesc(s[z - 1]):
            choices = {"\u0e38": "\uf718", "\u0e39": "\uf719", "\u0e3a": "\uf71a"}
            c = choices.get(c, "error")
        elif c == "\u0e0d" and z < length - 1 and isLower(s[z + 1]):
            c = "\uf70f"
        elif c == "\u0e10" and z < length - 1 and isLower(s[z + 1]):
            c = "\uf700"
        else:
            c = s[z]

        rv.append(c)

    return "".join(rv)
