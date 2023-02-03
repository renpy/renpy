# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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
import json


def merge_strings():
    """
    The merge strings command.
    """

    ap = renpy.arguments.ArgumentParser(description="Merges translated strings with the game script.")
    ap.add_argument("language", help="The language to merge translated strings to.")
    ap.add_argument("source", help="The json file to take translated strings from.")
    ap.add_argument("--reverse", action="store_true", help="Reverses the languages in the json file.")
    ap.add_argument("--replace", action="store_true", help="Replaces non-trivial translations.")

    args = ap.parse_args()

    language = args.language

    if language == 'None':
        language = None

    if language not in renpy.game.script.translator.strings:  # @UndefinedVariable
        raise Exception("Language %r does not have any translations." % language)

    with open(args.source, "r", encoding="utf-8") as f:
        data = json.loads(f.read())

    if args.reverse:
        new_data = { }

        for k, v in data.items():
            new_data[v] = k

        data = new_data

    st = renpy.game.script.translator.strings[language]  # @UndefinedVariable

    renpy.config.clear_lines = False

    for k, v in st.translations.items():

        trivial = (not v) or (k == v)

        if (not trivial) and (not args.replace):
            continue

        if k not in data:
            continue

        if k not in st.translation_loc:
            continue

        new = data[k]
        quoted = renpy.translation.quote_unicode(new)
        code = u'new "{}"'.format(quoted)

        filename, linenumber = st.translation_loc[k]
        renpy.scriptedit.insert_line_before(code, filename, linenumber)
        renpy.scriptedit.remove_line(filename, linenumber + 1)

    return False


renpy.arguments.register_command("merge_strings", merge_strings)
