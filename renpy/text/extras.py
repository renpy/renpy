# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
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
    shader=True,
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


arabic_reverse_mappings = {
    # [ISOLATED],[FINAL],[INITIAL],[MEDIAL] -> [BASE]
    # Arabic Presentation Forms-A
    (u'\uFB50',u'\uFB51'):                      u'\u0671', # ARABIC LETTER ALEF WASLA
    (u'\uFB52',u'\uFB53',u'\uFB54',u'\uFB55'):  u'\u067B', # ARABIC LETTER BEEH
    (u'\uFB56',u'\uFB57',u'\uFB58',u'\uFB59'):  u'\u067E', # ARABIC LETTER PEH
    (u'\uFB5A',u'\uFB5B',u'\uFB5C',u'\uFB5D'):  u'\u0680', # ARABIC LETTER BEHEH
    (u'\uFB5E',u'\uFB5F',u'\uFB60',u'\uFB61'):  u'\u067A', # ARABIC LETTER TTEHEH
    (u'\uFB62',u'\uFB63',u'\uFB64',u'\uFB65'):  u'\u067F', # ARABIC LETTER TEHEH
    (u'\uFB66',u'\uFB67',u'\uFB68',u'\uFB69'):  u'\u0679', # ARABIC LETTER TTEH
    (u'\uFB6A',u'\uFB6B',u'\uFB6C',u'\uFB6D'):  u'\u06A4', # ARABIC LETTER VEH
    (u'\uFB6E',u'\uFB6F',u'\uFB70',u'\uFB71'):  u'\u06A6', # ARABIC LETTER PEHEH
    (u'\uFB72',u'\uFB73',u'\uFB74',u'\uFB75'):  u'\u0684', # ARABIC LETTER DYEH
    (u'\uFB76',u'\uFB77',u'\uFB78',u'\uFB79'):  u'\u0683', # ARABIC LETTER NYEH
    (u'\uFB7A',u'\uFB7B',u'\uFB7C',u'\uFB7D'):  u'\u0686', # ARABIC LETTER TCHEH
    (u'\uFB7E',u'\uFB7F',u'\uFB80',u'\uFB81'):  u'\u0687', # ARABIC LETTER TCHEHEH
    (u'\uFB82',u'\uFB83'):                      u'\u068D', # ARABIC LETTER DDAHAL
    (u'\uFB84',u'\uFB85'):                      u'\u068C', # ARABIC LETTER DAHAL
    (u'\uFB86',u'\uFB87'):                      u'\u068E', # ARABIC LETTER DUL
    (u'\uFB88',u'\uFB89'):                      u'\u0688', # ARABIC LETTER DDAL
    (u'\uFB8A',u'\uFB8B'):                      u'\u0698', # ARABIC LETTER JEH
    (u'\uFB8C',u'\uFB8D'):                      u'\u0691', # ARABIC LETTER RREH
    (u'\uFB8E',u'\uFB8F',u'\uFB90',u'\uFB91'):  u'\u06A9', # ARABIC LETTER KEHEH
    (u'\uFB92',u'\uFB93',u'\uFB94',u'\uFB95'):  u'\u06AF', # ARABIC LETTER GAF
    (u'\uFB96',u'\uFB97',u'\uFB98',u'\uFB99'):  u'\u06B3', # ARABIC LETTER GUEH
    (u'\uFB9A',u'\uFB9B',u'\uFB9C',u'\uFB9D'):  u'\u06B1', # ARABIC LETTER NGOEH
    (u'\uFB9E',u'\uFB9F'):                      u'\u06BA', # ARABIC LETTER NOON GHUNNA
    (u'\uFBA0',u'\uFBA1',u'\uFBA2',u'\uFBA3'):  u'\u06BB', # ARABIC LETTER RNOON
    (u'\uFBA4',u'\uFBA5'):                      u'\u06C0', # ARABIC LETTER HEH WITH YEH ABOVE
    (u'\uFBA6',u'\uFBA7',u'\uFBA8',u'\uFBA9'):  u'\u06C1', # ARABIC LETTER GOAL
    (u'\uFBAA',u'\uFBAB',u'\uFBAC',u'\uFBAD'):  u'\u06BE', # ARABIC LETTER HEH DOACHASHMEE
    (u'\uFBAE',u'\uFBAF'):                      u'\u06D2', # ARABIC LETTER YEH BARREE
    (u'\uFBB0',u'\uFBB1'):                      u'\u06D3', # ARABIC LETTER YEH BARREE WITH HAMZA ABOVE
    (u'\uFBD3',u'\uFBD4',u'\uFBD5',u'\uFBD6'):  U'\u06AD', # ARABIC LETTER NG
    (u'\uFBD7',u'\uFBD8'):                      u'\u06C7', # ARABIC LETTER U
    (u'\uFBD9',u'\uFBDA'):                      u'\u06C6', # ARABIC LETTER OE
    (u'\uFBDB',u'\uFBDC'):                      u'\u06C8', # ARABIC LETTER YU
    (u'\uFBDD'):                                u'\u0677', # ARABIC LETTER U WITH HAMZA ABOVE
    (u'\uFBDE',u'\uFBDF'):                      u'\u06CB', # ARABIC LETTER VE
    (u'\uFBE0',u'\uFBE1'):                      u'\u06C5', # ARABIC LETTER KIRGHIZ OE
    (u'\uFBE2',u'\uFBE3'):                      u'\u06C9', # ARABIC LETTER KIRGHIZ YU
    (u'\uFBE4',u'\uFBE5',u'\uFBE6',u'\uFBE7'):  u'\u06D0', # ARABIC LETTER E
    (None,     None,     u'\uFBE8',u'\uFBE4'):  u'\u0649', # ARABIC LETTER UIGHUR KAZAKH KIRGHIZ ALEF MAKSURA
    (u'\uFBFC',u'\uFBFD',u'\uFBFE',u'\uFBFF'):  u'\u06CC', # ARABIC LETTER FARSI YEH

    # Arabic Presentation Forms-B
    (u'\uFE80'):                                u'\u0621', # ARABIC LETTER HAMZA
    (u'\uFE81',u'\uFE82'):                      u'\u0622', # ARABIC LETTER ALEF WITH MADDA ABOVE
    (u'\uFE83',u'\uFE84'):                      u'\u0623', # ARABIC LETTER ALEF WITH HAMZA ABOVE
    (u'\uFE85',u'\uFE86'):                      u'\u0624', # ARABIC LETTER WAW WITH HAMZA ABOVE
    (u'\uFE87',u'\uFE88'):                      u'\u0625', # ARABIC LETTER ALEF WITH HAMZA BELOW
    (u'\uFE89',u'\uFE8A',u'\uFE8B',u'\uFE8C'):  u'\u0626', # ARABIC LETTER YEH WITH HAMZA ABOVE
    (u'\uFE8D',u'\uFE8E'):                      u'\u0627', # ARABIC LETTER ALEF
    (u'\uFE8F',u'\uFE90',u'\uFE91',u'\uFE92'):  u'\u0628', # ARABIC LETTER BEH
    (u'\uFE93'u'\uFE94'):                       u'\u0629', # ARABIC LETTER TEH MARBUTA
    (u'\uFE95',u'\uFE96',u'\uFE97',u'\uFE98'):  u'\u062A', # ARABIC LETTER TEH
    (u'\uFE99',u'\uFE9A',u'\uFE9B',u'\uFE9C'):  u'\u062B', # ARABIC LETTER THEH
    (u'\uFE9D',u'\uFE9E',u'\uFE9F',u'\uFEA0'):  u'\u062C', # ARABIC LETTER JEEM
    (u'\uFEA1',u'\uFEA2',u'\uFEA3',u'\uFEA4'):  u'\u062D', # ARABIC LETTER HAH
    (u'\uFEA5',u'\uFEA6',u'\uFEA7',u'\uFEA8'):  u'\u062E', # ARABIC LETTER KHAH
    (u'\uFEA9',u'\uFEAA'):                      u'\u062F', # ARABIC LETTER DAL
    (u'\uFEAB',u'\uFEAC'):                      u'\u0630', # ARABIC LETTER THAL
    (u'\uFEAD',u'\uFEAE'):                      u'\u0631', # ARABIC LETTER REH
    (u'\uFEAF',u'\uFEB0'):                      u'\u0632', # ARABIC LETTER ZAIN
    (u'\uFEB1',u'\uFEB2',u'\uFEB3',u'\uFEB4'):  u'\u0633', # ARABIC LETTER SEEN
    (u'\uFEB5',u'\uFEB6',u'\uFEB7',u'\uFEB8'):  u'\u0634', # ARABIC LETTER SHEEN
    (u'\uFEB9',u'\uFEBA',u'\uFEBB',u'\uFEBC'):  u'\u0635', # ARABIC LETTER SAD
    (u'\uFEBD',u'\uFEBE',u'\uFEBF',u'\uFEC0'):  u'\u0636', # ARABIC LETTER DAD
    (u'\uFEC1',u'\uFEC2',u'\uFEC3',u'\uFEC4'):  u'\u0637', # ARABIC LETTER TAH
    (u'\uFEC5',u'\uFEC6',u'\uFEC7',u'\uFEC8'):  u'\u0638', # ARABIC LETTER ZAH
    (u'\uFEC9',u'\uFECA',u'\uFECB',u'\uFECC'):  u'\u0639', # ARABIC LETTER AIN
    (u'\uFECD',u'\uFECE',u'\uFECF',u'\uFED0'):  u'\u063A', # ARABIC LETTER GHAIN
    (u'\uFED1',u'\uFED2',u'\uFED3',u'\uFED4'):  u'\u0641', # ARABIC LETTER FEH
    (u'\uFED5',u'\uFED6',u'\uFED7',u'\uFED8'):  u'\u0642', # ARABIC LETTER QAF
    (u'\uFED9',u'\uFEDA',u'\uFEDB',u'\uFEDC'):  u'\u0643', # ARABIC LETTER KAF
    (u'\uFEDD',u'\uFEDE',u'\uFEDF',u'\uFEE0'):  u'\u0644', # ARABIC LETTER LAM
    (u'\uFEE1',u'\uFEE2',u'\uFEE3',u'\uFEE4'):  u'\u0645', # ARABIC LETTER MEEM
    (u'\uFEE5',u'\uFEE6',u'\uFEE7',u'\uFEE8'):  u'\u0646', # ARABIC LETTER NOON
    (u'\uFEE9',u'\uFEEA',u'\uFEEB',u'\uFEEC'):  u'\u0647', # ARABIC LETTER HEH
    (u'\uFEED',u'\uFEEE'):                      u'\u0648', # ARABIC LETTER WAW
    (u'\uFEEF',u'\uFEF0'):                      u'\u0649', # ARABIC LETTER ALEF MAKSURA
    (u'\uFEF1',u'\uFEF2',u'\uFEF3',u'\uFEF4'):  u'\u064A', # ARABIC LETTER YEH

    # Ligatures
    (u'\uFEF5',u'\uFEF6'):  		  u'\u0622\u0644', # ARABIC LIGATURE LAM WITH ALEF WITH MADDA ABOVE
    (u'\uFEF7',u'\uFEF8'):  		  u'\u0623\u0644', # ARABIC LIGATURE LAM WITH ALEF WITH HAMZA ABOVE
    (u'\uFEF9',u'\uFEFA'):  		  u'\u0625\u0644', # ARABIC LIGATURE LAM WITH ALEF WITH HAMZA BELOW
    (u'\uFEFB',u'\uFEFC'):  		  u'\u0627\u0644'  # ARABIC LIGATURE LAM WITH ALEF
}

# Convert this to one-on-one.
arabic_reverse_mappings = {k: v for l, v in arabic_reverse_mappings.items() for k in l if k is not None}


def unmap_arabic_presentation_forms(s):
    """
    Reverses the Arabic presentation forms in `s` to their base forms.
    """

    if not renpy.config.reverse_arabic_presentation_forms:
        return s

    rv = [ ]

    for c in s:

        c = arabic_reverse_mappings.get(c, c)

        rv.append(c)

    return "".join(rv)
