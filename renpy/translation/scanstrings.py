# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

import renpy.translation

################################################################################

STRING_RE = r"""(?x)
\b_[_p]?\s*\(\s*[uU]?(
\"\"\"(?:\\.|\"{1,2}|[^\\"])*?\"\"\"
|'''(?:\\.|\'{1,2}|[^\\'])*?'''
|"(?:\\.|[^\\"])*"
|'(?:\\.|[^\\'])*'
)\s*\)
"""

REGULAR_PRIORITIES = [
    ("script.rpy", 5, "script.rpy"),
    ("options.rpy", 10, "options.rpy"),
    ("gui.rpy", 20, "gui.rpy"),
    ("screens.rpy", 30, "screens.rpy"),
    ("", 100, "launcher.rpy"),
]


COMMON_PRIORITIES = [
    ("_compat/", 420, "obsolete.rpy"),
    ("_layout/", 410, "obsolete.rpy"),
    ("00layout.rpy", 400, "obsolete.rpy"),

    ("00console.rpy", 320, "developer.rpy"),
    ("_developer/", 310, "developer.rpy"),

    ("_errorhandling.rpym", 220, "error.rpy"),
    ("00gamepad.rpy", 210, "error.rpy"),
    ("00gltest.rpy", 200, "error.rpy"),

    ("00gallery.rpy", 180, "common.rpy"),
    ("00compat.rpy", 180, "common.rpy"),
    ("00updater.rpy", 170, "common.rpy"),
    ("00gamepad.rpy", 160, "common.rpy"),
    ("00iap.rpy", 150, "common.rpy"),
    ("", 50, "common.rpy"),
]


class String(object):
    """
    This stores information about a translation string or comment.
    """

    def __init__(self, filename, line, text, comment):

        # The full path to the file the strings came from.
        self.filename = filename

        # The line number of the translation string.
        self.line = line

        # The translation text.
        self.text = text

        # True if this is the translation of a comment.
        self.comment = comment

        # The elided filename, and if this is in the common directory.
        self.elided, self.common = renpy.translation.generation.shorten_filename(self.filename)

        if self.common:
            pl = COMMON_PRIORITIES
        else:
            pl = REGULAR_PRIORITIES

        for prefix, priority, launcher_file in pl:
            if self.elided.startswith(prefix):
                break

        self.priority = priority
        self.sort_key = (priority, self.filename, self.line)

        # The launcher translation file this goes into.
        self.launcher_file = launcher_file

    def __repr__(self):
        return "<String {self.filename}:{self.line} {self.text!r}>".format(self=self)


def scan_strings(filename):
    """
    Scans `filename`, a file containing Ren'Py script, for translatable
    strings.

    Returns a list of TranslationString objects.
    """

    rv = [ ]

    for line, s in renpy.game.script.translator.additional_strings[filename]:  # @UndefinedVariable
        rv.append(String(filename, line, s, False))

    for _filename, lineno, text in renpy.parser.list_logical_lines(filename):

        for m in re.finditer(STRING_RE, text):

            s = m.group(1)
            if s is not None:
                s = s.strip()
                s = "u" + s
                s = eval(s)

                if m.group(0).startswith("_p"):
                    s = renpy.minstore._p(s)

                if s:
                    rv.append(String(filename, lineno, s, False))

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

            rv.append(String(filename, start, s, True))

    return rv


def scan(min_priority=0, max_priority=299, common_only=False):
    """
    Scans all files for translatable strings and comments. Returns a list
    of String objects.
    """

    filenames = renpy.translation.generation.translate_list_files()

    strings = [ ]

    for filename in filenames:
        filename = os.path.normpath(filename)

        if not os.path.exists(filename):
            continue

        strings.extend(scan_strings(filename))
        strings.extend(scan_comments(filename))

    strings.sort(key=lambda s : s.sort_key)

    rv = [  ]
    seen = set()

    for s in strings:

        if s.priority < min_priority:
            continue

        if s.priority > max_priority:
            continue

        if common_only and not s.common:
            continue

        if s.text in seen:
            continue

        seen.add(s.text)
        rv.append(s)

    return rv
