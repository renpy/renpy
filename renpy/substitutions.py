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

# This file contains support for string translation and string formatting
# operations.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import renpy
import string
import os
import re


update_translations = "RENPY_UPDATE_TRANSLATIONS" in os.environ
flags = frozenset('rstiqulc!')
formatter = string.Formatter()

SIMPLE_NAME = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

def interpolate(s, scope):
    """
    Formats a string using Ren'Py's formatting rules. Ren'Py uses square
    brackets to denote interpolation, but is otherwise similar to native
    f-strings, with a few caveats and additional conversions available.
    """

    rv = ''

    for lit, expr, conv, fmt in parse(s):
        if lit:
            rv += lit

        if expr is None:
            continue

        if conv is None:
            conv = ''
        elif not conv:
            raise ValueError('conversion specifier cannot be empty')

        code = expr.strip()

        if not code:
            raise ValueError('expected expression')

        if code[-1] == '=':
            rv += expr
            code = code[:-1]

            if not conv and fmt is None:
                conv = 'r'

        if renpy.config.interpolate_exprs:
            if (code in scope) and SIMPLE_NAME.match(code):
                value = scope[code]
            else:
                try:
                    value = renpy.python.py_eval(code, {}, scope)
                except Exception as e:
                    if renpy.config.interpolate_exprs == "fallback":
                        try:
                            value, _ = formatter.get_field(code, (), scope)
                        except Exception:
                            raise e
                    else:
                        raise e

        else:
            value, _ = formatter.get_field(code, (), scope)

        if conv:
            value = convert(value, conv, scope)

        if fmt is None:
            fmt = ''

        rv += format(value, fmt)

    return rv


def parse(s):
    """
    Parses s according to Ren'Py string formatting rules. Emits a series
    of (literal, expression, conversion, format) tuples.
    """

    # States for the parse state machine.
    LITERAL = 0
    EXPRESSION = 1
    CONVERSION = 2
    FORMAT = 3

    # Conversion flags that we accept.
    FLAGS = flags

    # Markers and offsets for slicing.
    pos = -1
    size = len(s) + pos
    cut = 0
    mark = 0

    # The depth of brackets we've seen.
    brackets = 0
    parens = 0

    # The parts we've seen.
    lit = ''
    expr = None
    conv = None
    fmt = None

    state = LITERAL

    while pos < size:
        pos += 1
        c = s[pos]

        if state is LITERAL:
            if c == '[':
                lit += s[cut:pos]
                cut = pos + 1

                if c == s[pos+1:pos+2]:
                    pos += 1
                else:
                    state = EXPRESSION

        elif state is EXPRESSION:
            if c == '(':
                parens += 1

            elif c == ')':
                if not parens:
                    break

                parens -= 1

            elif c == '"' or c == "'":
                chars = 1
                found = 0

                if c * 2 == s[pos+1:pos+3]:
                    chars += 2
                    pos += 2

                while pos < size:
                    pos += 1
                    n = s[pos]

                    if n == c:
                        found += 1

                        if found == chars:
                            break

                    else:
                        if n == '\\':
                            pos += 1

                        found = 0

            elif parens:
                pass

            elif c == '[':
                brackets += 1

            elif c == ']':
                if brackets:
                    brackets -= 1
                else:
                    yield lit, s[cut:pos], None, None
                    cut = pos + 1
                    state = LITERAL
                    lit = ''

            elif c == '!':
                if s[pos+1:pos+2] == '=':
                    pos += 1
                else:
                    state = CONVERSION
                    expr = s[cut:pos]
                    cut = pos + 1

            elif c == ':':
                state = FORMAT
                expr = s[cut:pos]
                cut = pos + 1

        elif state is CONVERSION:
            if c == ']':
                yield lit, expr, s[cut:pos], fmt
                cut = pos + 1
                state = LITERAL
                lit = ''
                expr = None
                fmt = None

            elif c == ':':
                state = FORMAT
                conv = s[cut:pos]
                cut = pos + 1

            elif c not in FLAGS:
                if fmt is None:
                    raise ValueError('invalid conversion {!r}'.format(c))

                state = FORMAT
                pos = cut
                cut = mark

        elif state is FORMAT:
            if c == ']':
                yield lit, expr, conv, s[cut:pos]
                cut = pos + 1
                state = LITERAL
                lit = ''
                expr = None
                conv = None

            elif conv is None and c == '!':
                state = CONVERSION
                fmt = s[cut:pos]
                mark = cut
                cut = pos + 1

    if state is not LITERAL:
        raise Exception('String {!r} ends with an open format operation.'.format(s))

    if cut <= size:
        lit += s[cut:]

    if lit:
        yield lit, None, None, None


def convert(value, conv, scope):
    conv = set(conv)

    if 'r' in conv:
        value = repr(value)
        conv.discard('r')

    elif 's' in conv:
        value = str(value)
        conv.discard('s')

    if not conv:
        return value

    # All conversion symbols below assume we have a string.
    if not isinstance(value, basestring):
        value = str(value)

    if 't' in conv:
        value = renpy.translation.translate_string(value)

    if 'i' in conv:
        try:
            value = interpolate(value, scope)
        except RuntimeError: # PY3 RecursionError
            raise ValueError('Substitution {!r} refers to itself in a loop.'.format(value))

    if 'q' in conv:
        value = value.replace('{', '{{')

    if 'u' in conv:
        value = value.upper()

    if 'l' in conv:
        value = value.lower()

    if 'c' in conv:
        value = value[:1].capitalize() + value[1:]

    return value


class MultipleDict(object):

    def __init__(self, *dicts):
        self.dicts = dicts

    def __getitem__(self, key):
        for d in self.dicts:
            if key in d:
                return d[key]

        raise NameError("Name '{}' is not defined.".format(key))

    def __contains__(self, key):
        for d in self.dicts:
            if key in d:
                return True

        return False


def substitute(s, scope=None, force=False, translate=True):
    """
    Performs translation and formatting on `s`, as necessary.

    `scope`
        The scope which is used in formatting, in addition to the default
        store.

    `force`
        Force substitution to occur, even if it's disabled in the config.

    `translate`
        Determines if translation occurs.

    Returns the substituted string, and a flag that is True if substitution
    occurred, or False if no substitution occurred.
    """

    if not isinstance(s, basestring):
        s = str(s)

    if translate:
        s = renpy.translation.translate_string(s)

    # Substitute.
    if not renpy.config.new_substitutions and not force:
        return s, False

    if "[" not in s:
        return s, False

    old_s = s


    dicts = [ renpy.store.__dict__ ]

    if "store.interpolate" in renpy.python.store_dicts:
        dicts.insert(0, renpy.python.store_dicts["store.interpolate"])

    if scope is not None:
        dicts.insert(0, scope)

    if dicts:
        kwargs = MultipleDict(*dicts)
    else:
        kwargs = dicts[0]

    try:
        s = interpolate(s, kwargs) # type: ignore
    except Exception:
        if renpy.display.predict.predicting: # @UndefinedVariable
            return " ", True
        raise

    return s, (s != old_s)
