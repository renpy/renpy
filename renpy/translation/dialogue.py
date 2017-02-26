# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function

import renpy

import os

from renpy.translation import quote_unicode
from renpy.translation.generation import scan_strings


def notags_filter(s):

    def tag_pass(s):

        brace = False
        first = False
        rv = ""

        for i in s:

            if i == '{':

                if first:
                    brace = False
                else:
                    brace = True
                    first = True

            elif i == "}":
                first = False

                if brace:
                    brace = False

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


class DialogueFile(object):

    def __init__(self, filename, output, tdf=True, strings=False, notags=True, escape=True):  # @ReservedAssignment
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

        commondir = os.path.normpath(renpy.config.commondir)

        if filename.startswith(commondir):
            return

        self.tdf = tdf
        self.notags = notags
        self.escape = escape
        self.strings = strings

        self.f = open(output, "a")

        self.write_dialogue()

        self.f.close()

    def write_dialogue(self):
        """
        Writes the dialogue to the file.
        """

        lines = []

        translator = renpy.game.script.translator

        for label, t in translator.file_translates[self.filename]:

            if label is None:
                label = ""

            for n in t.block:

                if isinstance(n, renpy.ast.Say):

                    if not n.who:
                        who = ""
                    else:
                        who = n.who

                    what = n.what

                    if self.notags:
                        what = notags_filter(what)

                    if self.escape:
                        what = quote_unicode(what)

                    if self.tdf:

                        lines.append([
                            t.identifier,
                            who,
                            what,
                            n.filename,
                            str(n.linenumber),
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
            self.f.write("\t".join(line).encode("utf-8") + "\n")

    def get_strings(self):
        """
        Finds the strings in the file.
        """

        lines = []

        filename = renpy.parser.elide_filename(self.filename)

        for line, s in scan_strings(self.filename):

            stl = renpy.game.script.translator.strings[None]  # @UndefinedVariable

            if s in stl.translations:
                continue

            stl.translations[s] = s

            if self.notags:
                s = notags_filter(s)

            if self.escape:
                s = quote_unicode(s)

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
                ]

            f.write("\t".join(line).encode("utf-8") + "\n")

    for dirname, filename in renpy.loader.listdirfiles():
        if dirname is None:
            continue

        filename = os.path.join(dirname, filename)

        if not (filename.endswith(".rpy") or filename.endswith(".rpym")):
            continue

        filename = os.path.normpath(filename)
        DialogueFile(filename, output, tdf=tdf, strings=args.strings, notags=args.notags, escape=args.escape)

    return False

renpy.arguments.register_command("dialogue", dialogue_command)
