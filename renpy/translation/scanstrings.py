# Copyright 2004-2016 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function, unicode_literals

import os
import re
import codecs

import renpy

################################################################################

STRING_RE = r"""(?x)
\b__?\s*\(\s*[uU]?(
\"\"\"(?:\\.|\"{1,2}|[^\\"])*?\"\"\"
|'''(?:\\.|\'{1,2}|[^\\'])*?'''
|"(?:\\.|[^\\"])*"
|'(?:\\.|[^\\'])*'
)\s*\)
"""


class String(object):
    """
    This stores information about a translation string or comment.
    """

    def __init__(self, filename, line, text):

        # The full path to the file that contained this translation.
        self.full_filename = filename

        # The line number of the translation string.
        self.line = line

        # The translation text.
        self.text = text

        # A friendly (elided) name for the translation file.
        self.filename = None

        # True if this file is from the common directory.
        self.common = False

        # A tag we apply to the strings.
        self.tag = "strings"

        commondir = os.path.normpath(renpy.config.commondir)
        gamedir = os.path.normpath(renpy.config.gamedir)

        if filename.startswith(commondir):
            self.common = True
            self.filename = os.path.relpath(filename, commondir)

        elif filename.startswith(gamedir):
            self.filename = os.path.relpath(filename, gamedir)

        else:
            self.filename = os.path.basename(filename)

        # The destination file.
        if self.common:
            self.destination = "common.rpy"
        else:
            self.destination = self.filename

        if self.destination[-1] == "m":
            self.destination = self.destination[:-1]

    def __repr__(self):
        return "<String {self.filename}:{self.line} {self.text!r} {self.tag} {self.destination}>".format(self=self)


def scan_strings(filename):
    """
    Scans `filename`, a file containing Ren'Py script, for translatable
    strings.

    Returns a list of TranslationString objects.
    """

    rv = [ ]

    for line, s in renpy.game.script.translator.additional_strings[filename]:  # @UndefinedVariable
        rv.append((line, s))

    line = 1

    for _filename, lineno, text in renpy.parser.list_logical_lines(filename):

        for m in re.finditer(STRING_RE, text):

            s = m.group(1)
            if s is not None:
                s = s.strip()
                s = "u" + s
                s = eval(s)
                rv.append(String(filename, lineno, s))

    return rv


def scan_comments(filename):

    rv = [ ]

    if filename not in renpy.config.translate_comments:
        return rv

    comment = [ ]
    start = 0

    with codecs.open(filename, "r", "utf-8") as f:
        lines = [ i.rstrip() for i in f.read().replace(u"\ufeff", "").split('\n') ]

    for i, l in enumerate(lines):

        if not comment:
            start = i + 1

        m = re.match(r'\s*## (.*)', l)

        if m:
            c = m.group(1)

            if comment:
                c = c.strip()

            comment.append(c)

        elif comment:
            s = "## " + " ".join(comment)

            if s.endswith("#"):
                s = s.rstrip("# ")

            comment = [ ]

            rv.append(String(filename, start, s))

    return rv


def scan():
    """
    Scans all files for translatable strings and comments, and returns
    all available translations.
    """

    filenames = list(renpy.config.translate_files)

    for dirname, filename in renpy.loader.listdirfiles():
        if dirname is None:
            continue

        filename = os.path.join(dirname, filename)

        if not (filename.endswith(".rpy") or filename.endswith(".rpym")):
            continue

        filenames.append(filename)

    rv = [ ]

    for filename in filenames:
        filename = os.path.normpath(filename)

        if not os.path.exists(filename):
            continue

        rv.extend(scan_strings(filename))
        rv.extend(scan_comments(filename))

    return rv
