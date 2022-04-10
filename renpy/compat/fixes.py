# Copyright 2004-2022 Tom Rothamel <pytom@bishoujo.us>
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


import tokenize
import token
import io


def fix_octal_numbers(tokens):
    """
    This fixes python-2 style octal numbers. Tokenize seems to report this
    as two numbers, the first of which has a tring of '0'. This merges that
    with the next token.
    """

    old = tokens[0]
    rv = [ ]

    for new in tokens:

        if (old.type == token.NUMBER) and (new.type == token.NUMBER) and old.string == "0":
            rv.pop()
            new = tokenize.TokenInfo(token.NUMBER, old.string + "o" + new.string, old.start, new.end, new.line)

        rv.append(new)
        old = new

    return rv


def fix_tokens(source):
    """
    This applies fixes that will help python 2 code run under python 3. Not all
    source will be fixed, but this will attempt to handle common issues.

    These are fixes that apply at the Python level.
    """

    try:

        if PY2:
            return source

        bio = io.BytesIO(source.encode("utf-8"))
        tokens = list(tokenize.tokenize(bio.readline))

        tokens = fix_octal_numbers(tokens)

        rv = tokenize.untokenize(tokens).decode("utf-8")
        return rv

    except Exception as e:
        # import traceback
        # traceback.print_exc()
        raise e
