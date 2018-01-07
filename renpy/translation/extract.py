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

from __future__ import absolute_import, division, print_function

import renpy
import json


def extract_strings_core(language, destination, merge=False, force=False):

    if (not force) and (language not in renpy.game.script.translator.strings):  # @UndefinedVariable
        raise Exception("Language %r does not have any translations." % language)

    st = renpy.game.script.translator.strings[language]  # @UndefinedVariable

    result = { }

    if merge:
        with open(destination, "r") as f:
            result.update(json.load(f, "utf-8"))

    for k, v in st.translations.iteritems():
        if v and v != k:
            result[k] = v

    with open(destination, "wb") as f:
        json.dump(result, f, ensure_ascii=True)


def extract_strings():
    """
    The extract strings command.
    """

    ap = renpy.arguments.ArgumentParser(description="Extracts translated strings.")
    ap.add_argument("language", help="The language to extract translated strings from.")
    ap.add_argument("destination", help="The json file to store the translated strings into.")
    ap.add_argument("--merge", help="If given, the current contents of the file are preserved, and new contents are merged into the file.", action="store_true")
    ap.add_argument("--force", help="If given, noting happens if the language does not exist.", action="store_true")

    args = ap.parse_args()

    language = args.language

    if language == 'None':
        language = None

    extract_strings_core(language, args.destination, args.merge, args.force)

    return False

renpy.arguments.register_command("extract_strings", extract_strings)
