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

from __future__ import print_function

import renpy

import re
import os
import time
import io
import codecs

from renpy.translation import quote_unicode

################################################################################
# Translation Generation
################################################################################

STRING_RE = r"""(?x)
\b__?\s*\(\s*[uU]?(
\"\"\"(?:\\.|\"{1,2}|[^\\"])*?\"\"\"
|'''(?:\\.|\'{1,2}|[^\\'])*?'''
|"(?:\\.|[^\\"])*"
|'(?:\\.|[^\\'])*'
)\s*\)
"""

def scan_strings(filename):
    """
    Scans `filename`, a file containing Ren'Py script, for translatable
    strings.

    Generates a list of (line, string) tuples.
    """


    rv = [ ]

    for line, s in renpy.game.script.translator.additional_strings[filename]: # @UndefinedVariable
        rv.append((line, s))

    line = 1

    for _filename, lineno, text in renpy.parser.list_logical_lines(filename):

        for m in re.finditer(STRING_RE, text):

            s = m.group(1)
            if s is not None:
                s = s.strip()
                s = "u" + s
                s = eval(s)
                rv.append((lineno, s))

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

            rv.append((start, s))

    return rv


def open_tl_file(fn):

    if not os.path.exists(fn):
        dn = os.path.dirname(fn)

        try:
            os.makedirs(dn)
        except:
            pass

        f = io.open(fn, "a", encoding="utf-8")
        f.write(u"\ufeff")

    else:
        f = io.open(fn, "a", encoding="utf-8")

    f.write(u"# TO" + "DO: Translation updated at {}\n".format(time.strftime("%Y-%m-%d %H:%M")))
    f.write(u"\n")

    return f


class TranslateFile(object):

    def __init__(self, filename, language, filter, count=False): # @ReservedAssignment
        self.filename = filename
        self.filter = filter

        commondir = os.path.normpath(renpy.config.commondir)
        gamedir = os.path.normpath(renpy.config.gamedir)

        if filename.startswith(commondir):
            relfn = os.path.relpath(filename, commondir)

            if relfn == "_developer.rpym":
                return

            if relfn.startswith("compat"):
                return

            self.tl_filename = os.path.join(renpy.config.gamedir, renpy.config.tl_directory, language, "common.rpy")

        elif filename.startswith(gamedir):
            fn = os.path.relpath(filename, gamedir)
            self.tl_filename = os.path.join(renpy.config.gamedir, renpy.config.tl_directory, language, fn)

        else:

            fn = os.path.basename(filename)
            self.tl_filename = os.path.join(renpy.config.gamedir, renpy.config.tl_directory, language, fn)

        if self.tl_filename.endswith(".rpym"):
            self.tl_filename = self.tl_filename[:-1]

        if language == "None":
            language = None

        self.language = language
        self.f = None

        if count:

            self.count_missing()

        else:

            if language is not None:
                self.write_translates()

            self.write_strings()

        self.close()

    def open(self):
        """
        Opens a translation file.
        """

        if self.f is not None:
            return

        self.f = open_tl_file(self.tl_filename)

    def close(self):
        """
        Closes the translation file, if it's open.
        """

        if self.f is not None:
            self.f.close()

    def write_translates(self):
        """
        Writes the translates to the file.
        """

        translator = renpy.game.script.translator

        for label, t in translator.file_translates[self.filename]:

            if (t.identifier, self.language) in translator.language_translates:
                continue

            self.open()

            if label is None:
                label = ""

            self.f.write(u"# {}:{}\n".format(t.filename, t.linenumber))
            self.f.write(u"translate {} {}:\n".format(self.language, t.identifier.replace('.', '_')))
            self.f.write(u"\n")

            for n in t.block:
                self.f.write(u"    # " + n.get_code() + "\n")

            for n in t.block:
                self.f.write(u"    " + n.get_code(self.filter) + "\n")

            self.f.write(u"\n")

    def write_strings(self):
        """
        Writes strings to the file.
        """

        # If this function changes, count_missing may also need to
        # change.

        started = False
        filename = renpy.parser.elide_filename(self.filename)

        strings = scan_strings(self.filename)

        if renpy.config.translate_comments:
            strings.extend(scan_comments(self.filename))

        # Sort by line number.
        strings.sort(key=lambda a : a[0])

        for line, s in strings:

            stl = renpy.game.script.translator.strings[self.language] # @UndefinedVariable

            if s in stl.translations:
                continue

            stl.translations[s] = s

            if not started:
                started = True

                self.open()
                self.f.write(u"translate {} strings:\n".format(self.language))
                self.f.write(u"\n")

            fs = self.filter(s)

            self.f.write(u"    # {}:{}\n".format(filename, line))
            self.f.write(u"    old \"{}\"\n".format(quote_unicode(s)))
            self.f.write(u"    new \"{}\"\n".format(quote_unicode(fs)))
            self.f.write(u"\n")

    def count_missing(self):
        """
        Counts the number of missing translations.
        """

        # Translates.

        missing_translates = 0

        translator = renpy.game.script.translator

        for _, t in translator.file_translates[self.filename]:

            if (t.identifier, self.language) in translator.language_translates:
                continue

            missing_translates += 1

        # Strings.

        missing_strings = 0

        strings = scan_strings(self.filename)

        if renpy.config.translate_comments:
            strings.extend(scan_comments(self.filename))

        for _, s in strings:

            stl = renpy.game.script.translator.strings[self.language] # @UndefinedVariable

            if s in stl.translations:
                continue

            missing_strings += 1

        self.missing_translates = missing_translates
        self.missing_strings = missing_strings

def null_filter(s):
    return s

def empty_filter(s):
    return ""

def generic_filter(s, transform):

    def remove_special(s, start, end, process):
        specials = 0
        first = False

        rv = ""
        buf = ""

        for i in s:

            if i == start:
                if first:
                    specials = 0
                else:
                    rv += process(buf)
                    buf = ""

                    if specials == 0:
                        first = True

                    specials += 1

                rv += start

            elif i == end:

                first = False

                specials -= 1
                if specials < 0:
                    specials += 1

                rv += end

            else:
                if specials:
                    rv += i
                else:
                    buf += i

        if buf:
            rv += process(buf)

        return rv

    def remove_braces(s):
        return remove_special(s, "{", "}", transform)

    return remove_special(s, "[", "]", remove_braces)

def rot13_transform(s):

    ROT13 = { }

    for i, j in zip("ABCDEFGHIJKLM", "NMOPQRSTUVWYZ"):
        ROT13[i] = j
        ROT13[j] = i

        i = i.lower()
        j = j.lower()

        ROT13[i] = j
        ROT13[j] = i

    return "".join(ROT13.get(i, i) for i in s)

def rot13_filter(s):
    return generic_filter(s, rot13_transform)

def piglatin_transform(s):
    # Based on http://stackoverflow.com/a/23177629/3549890

    lst = ['sh', 'gl', 'ch', 'ph', 'tr', 'br', 'fr', 'bl', 'gr', 'st', 'sl', 'cl', 'pl', 'fl']

    def replace(m):
        i = m.group(0)

        if i[0] in ['a', 'e', 'i', 'o', 'u']:
            rv = i + 'ay'
        elif i[:2] in lst:
            rv = i[2:] + i[:2] + 'ay'
        else:
            rv = i[1:] + i[0] + 'ay'

        if i[0].isupper():
            rv = rv.capitalize()

        return rv

    return re.sub(r'\w+', replace, s)

def piglatin_filter(s):
    return generic_filter(s, piglatin_transform)

def translate_command():
    """
    The translate command. When called from the command line, this generates
    the translations.
    """

    ap = renpy.arguments.ArgumentParser(description="Generates or updates translations.")
    ap.add_argument("language", help="The language to generate translations for.")
    ap.add_argument("--rot13", help="Apply rot13 while generating translations.", dest="rot13", action="store_true")
    ap.add_argument("--piglatin", help="Apply pig latin while generating translations.", dest="piglatin", action="store_true")
    ap.add_argument("--empty", help="Produce empty strings while generating translations.", dest="empty", action="store_true")
    ap.add_argument("--count", help="Instead of generating files, print a count of missing translations.", dest="count", action="store_true")

    args = ap.parse_args()

    if args.rot13:
        filter = rot13_filter #@ReservedAssignment
    elif args.piglatin:
        filter = piglatin_filter #@ReservedAssignment
    elif args.empty:
        filter = empty_filter # @ReservedAssignment
    else:
        filter = null_filter #@ReservedAssignment

    filenames = list(renpy.config.translate_files)

    for dirname, filename in renpy.loader.listdirfiles():
        if dirname is None:
            continue

        filename = os.path.join(dirname, filename)

        if not (filename.endswith(".rpy") or filename.endswith(".rpym")):
            continue

        filenames.append(filename)


    missing_translates = 0
    missing_strings = 0


    for filename in filenames:
        filename = os.path.normpath(filename)

        if not os.path.exists(filename):
            continue

        tf = TranslateFile(filename, args.language, filter, args.count)

        if args.count:
            missing_translates += tf.missing_translates
            missing_strings += tf.missing_strings

    if args.count:

        print("{}: {} missing dialogue translations, {} missing string translations.".format(
            args.language,
            missing_translates,
            missing_strings
            ))

    return False

renpy.arguments.register_command("translate", translate_command)



