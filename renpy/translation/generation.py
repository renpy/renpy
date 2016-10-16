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

import renpy.translation

import re
import os
import time
import io
import codecs
import collections

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


tl_file_cache = { }


def open_tl_file(fn):

    if fn in tl_file_cache:
        return tl_file_cache[fn]

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

    tl_file_cache[fn] = f

    return f


def close_tl_files():

    for i in tl_file_cache.values():
        i.close()

    tl_file_cache.clear()


def shorten_filename(filename):
    """
    Shortens a file name. Returns the shortened filename, and a flag that says
    if the filename is in the common directory.
    """

    commondir = os.path.normpath(renpy.config.commondir)
    gamedir = os.path.normpath(renpy.config.gamedir)

    if filename.startswith(commondir):
        fn = os.path.relpath(filename, commondir)
        common = True

    elif filename.startswith(gamedir):
        fn = os.path.relpath(filename, gamedir)
        common = False

    else:
        fn = os.path.basename(filename)
        common = False

    return fn, common


def write_translates(filename, language, filter):  # @ReservedAssignment

    fn, common = shorten_filename(filename)

    # The common directory should not have dialogue in it.
    if common:
        return

    tl_filename = os.path.join(renpy.config.gamedir, renpy.config.tl_directory, language, fn)

    if tl_filename[-1] == "m":
        tl_filename = tl_filename[:-1]

    if language == "None":
        language = None

    translator = renpy.game.script.translator

    for label, t in translator.file_translates[filename]:

        if (t.identifier, language) in translator.language_translates:
            continue

        f = open_tl_file(tl_filename)

        if label is None:
            label = ""

        f.write(u"# {}:{}\n".format(t.filename, t.linenumber))
        f.write(u"translate {} {}:\n".format(language, t.identifier.replace('.', '_')))
        f.write(u"\n")

        for n in t.block:
            f.write(u"    # " + n.get_code() + "\n")

        for n in t.block:
            f.write(u"    " + n.get_code(filter) + "\n")

        f.write(u"\n")


def translation_file_callback(filename, common, comment):

    if common:

        if filename.startswith("_compat"):
            return None

        return "common.rpy"

    else:
        if filename[-1] == "m":
            filename = filename[:-1]

        return filename


def write_strings(language, filter, min_priority, max_priority):  # @ReservedAssignment
    """
    Writes strings to the file.
    """

    # If this function changes, count_missing may also need to
    # change.

    stl = renpy.game.script.translator.strings[language]  # @UndefinedVariable

    strings = renpy.translation.scanstrings.scan(min_priority, max_priority)

    stringfiles = collections.defaultdict(list)

    for s in strings:

        fn, common = shorten_filename(s.filename)
        tlfn = translation_file_callback(fn, common, s.comment)

        if tlfn is None:
            continue

        # Already seen.
        if s.text in stl.translations:
            continue

        stringfiles[tlfn].append(s)

    for tlfn, sl in stringfiles.items():

        sl.sort(key=lambda s : (s.filename, s.line))

        tlfn = os.path.join(renpy.config.gamedir, renpy.config.tl_directory, language, tlfn)

        f = open_tl_file(tlfn)
        sfn, _ = shorten_filename(s.filename)

        f.write(u"translate {} strings:\n".format(language))
        f.write(u"\n")

        for s in sl:
            text = filter(s.text)

            f.write(u"    # {}:{}\n".format(sfn, s.line))
            f.write(u"    old \"{}\"\n".format(quote_unicode(s.text)))
            f.write(u"    new \"{}\"\n".format(quote_unicode(text)))
            f.write(u"\n")


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


def translate_list_files():
    """
    Returns a list of files that exist and should be scanned for translations.
    """

    filenames = list(renpy.config.translate_files)

    for dirname, filename in renpy.loader.listdirfiles():
        if dirname is None:
            continue

        filename = os.path.join(dirname, filename)

        if not (filename.endswith(".rpy") or filename.endswith(".rpym")):
            continue

        filename = os.path.normpath(filename)

        if not os.path.exists(filename):
            continue

        filenames.append(filename)

    return filenames


def count_missing(language, min_priority, max_priority):
    """
    Prints a count of missing translations for `language`.
    """

    translator = renpy.game.script.translator

    missing_translates = 0

    for filename in translate_list_files():
        for _, t in translator.file_translates[filename]:
            if (t.identifier, language) not in translator.language_translates:
                missing_translates += 1

    missing_strings = 0

    stl = renpy.game.script.translator.strings[language]  # @UndefinedVariable

    strings = renpy.translation.scanstrings.scan(min_priority, max_priority)

    for s in strings:

        fn, common = shorten_filename(s.filename)
        tlfn = translation_file_callback(fn, common, s.comment)

        if tlfn is None:
            continue

        if s.text in stl.translations:
            continue

        missing_strings += 1

    print("{}: {} missing dialogue translations, {} missing string translations.".format(
        language,
        missing_translates,
        missing_strings
        ))


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
    ap.add_argument("--min-priority", help="Translate strings with more than this priority.", dest="min_priority", default=0, type=int)
    ap.add_argument("--max-priority", help="Translate strings with more than this priority.", dest="max_priority", default=299, type=int)

    args = ap.parse_args()

    if args.count:
        count_missing(args.language, args.min_priority, args.max_priority)
        return False

    if args.rot13:
        filter = rot13_filter  # @ReservedAssignment
    elif args.piglatin:
        filter = piglatin_filter  # @ReservedAssignment
    elif args.empty:
        filter = empty_filter  # @ReservedAssignment
    else:
        filter = null_filter  # @ReservedAssignment

    for filename in translate_list_files():
        write_translates(filename, args.language, filter)

    write_strings(args.language, filter, args.min_priority, args.max_priority)

    close_tl_files()

#         if args.count:
#             missing_translates += tf.missing_translates
#             missing_strings += tf.missing_strings
#
#     if args.count:
#
#         print("{}: {} missing dialogue translations, {} missing string translations.".format(
#             args.language,
#             missing_translates,
#             missing_strings
#             ))

    return False

renpy.arguments.register_command("translate", translate_command)
