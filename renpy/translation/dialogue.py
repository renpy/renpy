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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *



import renpy

import os

from renpy.translation import quote_unicode


def create_dialogue_map(language):
    """
    :undocumented:

    Creates a map from a dialogue string to a potential translation of the
    the dialogue. This is meant for the Ren'Py tutorial, as a way of translating
    strings found in the examples.
    """

    rv = { }

    def get_text(t):
        if isinstance(t, renpy.ast.Say):
            return t.what

        for i in t.block:
            if isinstance(i, renpy.ast.Say):
                return i.what

        return None

    translator = renpy.game.script.translator

    for v in translator.file_translates.values():

        for _, t in v:

            lt = translator.language_translates.get((t.identifier, language), None)

            if lt is None:
                continue

            t_text = get_text(t)
            lt_text = get_text(lt)

            if t_text and lt_text:
                rv[t_text] = lt_text

    return rv


def notags_filter(s):

    def tag_pass(s):

        brace = False
        first = False
        rv = ""

        for i in s:

            if i == '{':

                if first:

                    brace = False
                    first = False
                    rv += '{{'
                else:
                    brace = True
                    first = True

            elif i == "}":
                first = False

                if brace:
                    brace = False
                else:
                    rv += i

            else:
                first = False

                if brace:
                    pass
                else:
                    rv += i

        return rv

    def square_pass(s):
        squares = 0
        first = False

        rv = ""
        buf = ""

        for i in s:

            if i == "[":
                if first:
                    squares = 0
                else:
                    rv += tag_pass(buf)
                    buf = ""

                    if squares == 0:
                        first = True

                    squares += 1

                rv += "["

            elif i == "]":

                first = False

                squares -= 1
                if squares < 0:
                    squares += 1

                rv += "]"

            else:
                if squares:
                    rv += i
                else:
                    buf += i

        if buf:
            rv += tag_pass(buf)

        return rv

    return square_pass(s)


def combine_filter(s):

    doubles = [ "{{", "%%" ]

    if renpy.config.lenticular_bracket_ruby:
        doubles.append("\u3010\u3010") # LENTICULAR BRACKET LEFT x 2

    for double in doubles:
        while True:
            if s.find(double) >= 0:
                i = s.find(double)
                s = s[:i] + s[i+1:]
            else:
                break
    return s


def what_filter(s):
    return "[what]"


class DialogueFile(object):

    def __init__(self, filename, output, tdf=True, strings=False, notags=True, escape=True, language=None): # @ReservedAssignment
        """
        `filename`
            The file we're extracting dialogue from.

        `tdf`
            If true, dialogue is extracted in tab-delimited format. If false,
            dialogue is extracted by itself.

        `strings`
            If true, extract all translatable strings, not just dialogue.

        `notags`
            If true, strip text tags from the extracted dialogue.

        `escape`
            If true, escape special characters in the dialogue.
        """

        self.filename = filename

        commondir = os.path.normpath(renpy.config.commondir) # type: ignore

        if filename.startswith(commondir):
            return

        self.tdf = tdf
        self.notags = notags
        self.escape = escape
        self.strings = strings
        self.language = language

        self.f = open(output, "a", encoding="utf-8")

        with self.f:
            self.write_dialogue()

    def write_dialogue(self):
        """
        Writes the dialogue to the file.
        """

        lines = []

        translator = renpy.game.script.translator

        for label, t in translator.file_translates[self.filename]:

            if label is None:
                label = ""

            identifier = t.identifier.replace('.', '_')

            tl = None
            if self.language is not None:
                tl = translator.language_translates.get((identifier, self.language), None)


            if tl is None:
                tl = t

            if isinstance(tl, renpy.ast.TranslateSay):
                block = [ tl ]
            else:
                block = tl.block

            for n in block:

                if isinstance(n, renpy.ast.Say):

                    if not n.who:
                        who = ""
                    else:
                        who = n.who

                    what = n.what

                    if self.notags:
                        what = notags_filter(what)

                    what = combine_filter(what)

                    if self.escape:
                        what = quote_unicode(what)
                    elif self.tdf:
                        what = what.replace("\\", "\\\\")
                        what = what.replace("\t", "\\t")
                        what = what.replace("\n", "\\n")

                    if self.tdf:

                        lines.append([
                            t.identifier,
                            who,
                            what,
                            n.filename,
                            str(n.linenumber),
                            n.get_code(what_filter)
                            ])

                    else:
                        lines.append([what])

        if self.strings:
            lines.extend(self.get_strings())

            # If we're tab-delimited, we have line number info, which means we
            # can sort the list so everything's in order, for menus and stuff.
            if self.tdf:
                lines.sort(key=lambda x: int(x[4]))

        for line in lines:
            self.f.write("\t".join(line) + "\n")

    def get_strings(self):
        """
        Finds the strings in the file.
        """

        lines = []

        filename = renpy.lexer.elide_filename(self.filename)

        for ss in renpy.translation.scanstrings.scan_strings(self.filename):

            line = ss.line
            s = ss.text

            stl = renpy.game.script.translator.strings[None] # @UndefinedVariable

            # don't include s in common.rpym
            if s in stl.translations:
                continue

            # avoid to include same s
            stl.translations[s] = s

            s = renpy.translation.translate_string(s, self.language) # type: ignore

            if self.notags:
                s = notags_filter(s)

            s = combine_filter(s)

            if self.escape:
                s = quote_unicode(s)

            elif self.tdf:
                s = s.replace("\\", "\\\\")
                s = s.replace("\t", "\\t")
                s = s.replace("\n", "\\n")

            if self.tdf:
                lines.append(["", "", s, filename, str(line)])

            else:
                lines.append([s])

        return lines


def dialogue_command():
    """
    The dialogue command. This updates dialogue.txt, a file giving all the dialogue
    in the game.
    """

    ap = renpy.arguments.ArgumentParser(description="Generates or updates translations.")
    ap.add_argument("language", help="The language to extract dialogue for.")
    ap.add_argument("--text", help="Output the dialogue as plain text, instead of a tab-delimited file.", dest="text", action="store_true")
    ap.add_argument("--strings", help="Output all translatable strings, not just dialogue.", dest="strings", action="store_true")
    ap.add_argument("--notags", help="Strip text tags from the dialogue.", dest="notags", action="store_true")
    ap.add_argument("--escape", help="Escape quotes and other special characters.", dest="escape", action="store_true")
    args = ap.parse_args()

    tdf = not args.text
    if tdf:
        output = os.path.join(renpy.config.basedir, "dialogue.tab")
    else:
        output = os.path.join(renpy.config.basedir, "dialogue.txt")

    with open(output, "w") as f:
        if tdf:
            line = [
                "Identifier",
                "Character",
                "Dialogue",
                "Filename",
                "Line Number",
                "Ren'Py Script",
                ]

            f.write("\t".join(line) + "\n")

    for dirname, filename in renpy.loader.listdirfiles():
        if dirname is None:
            continue

        filename = os.path.join(dirname, filename)

        if not (filename.endswith(".rpy") or filename.endswith(".rpym")):
            continue

        filename = os.path.normpath(filename)
        language = args.language
        if language in ("None", ""):
            language = None
        DialogueFile(filename, output, tdf=tdf, strings=args.strings,
                     notags=args.notags, escape=args.escape, language=language)

    return False


renpy.arguments.register_command("dialogue", dialogue_command)
