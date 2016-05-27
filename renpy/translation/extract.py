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

from __future__ import absolute_import, division, print_function

import renpy
import json
import io

def extract_strings():
    """
    The extract strings command.
    """

    ap = renpy.arguments.ArgumentParser(description="Extracts translated strings.")
    ap.add_argument("language", help="The language to extract translated strings from.")
    ap.add_argument("destination", help="The json file to store the translated strings into.")

    args = ap.parse_args()

    language = args.language

    if language not in renpy.game.script.translator.strings: # @UndefinedVariable
        raise Exception("Language %r does not have any translations." % language)

    st = renpy.game.script.translator.strings[language] # @UndefinedVariable

    result = { }

    for k, v in st.translations.iteritems():
        result[k] = v

    data = json.dumps(result, ensure_ascii=False)

    with io.open(args.destination, "w", encoding="utf-8") as f:
        f.write(data)

    return False

renpy.arguments.register_command("extract_strings", extract_strings)

