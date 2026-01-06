# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
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

import cython


@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline Py_UCS4 _get_c_unbounded(unicode data, Py_ssize_t pos) noexcept:
    return data[pos]


def match_whitespace(unicode data not None, Py_ssize_t pos, /):
    """
    Return position after the run of whitespace characters, or None
    if current position is not at the start of whitespace.
    """

    cdef Py_ssize_t i = pos
    cdef Py_ssize_t length = len(data)

    for i in range(pos, len(data)):
        if _get_c_unbounded(data, i) != ' ':
            break
    else:
        i = length

    return None if i == pos else i


def match_logical_word(unicode data not None, Py_ssize_t pos, /):
    """
    Return position after the run of letters that are valid part
    of a logical word, or None if current position is not at the
    start of a logical word.
    """

    cdef Py_ssize_t i = pos
    cdef Py_ssize_t length = len(data)
    cdef Py_UCS4 c

    for i in range(pos, length):
        c = _get_c_unbounded(data, i)
        # Condition is the same as `is_potential_identifier_char` in CPython.
        if not (
            'a' <= c <= 'z' or
            'A' <= c <= 'Z' or
            '0' <= c <= '9' or
            c == '_' or
            c >= 128
        ):
            break
    else:
        i = length

    return None if i == pos else i


def match_operator(unicode data not None, Py_ssize_t pos, /):
    """
    Return position after the operator, or None if current position
    is not at the start of an operator.
    """

    cdef Py_ssize_t length = len(data)

    cdef Py_UCS4 c1 = 0
    if pos + 0 < length:
        c1 = _get_c_unbounded(data, pos)

    cdef Py_UCS4 c2 = 0
    if pos + 1 < length:
        c2 = _get_c_unbounded(data, pos + 1)

    cdef Py_UCS4 c3 = 0
    if pos + 2 < length:
        c3 = _get_c_unbounded(data, pos + 2)

    # 3-character operators
    if c3 == '.' and c2 == '.' and c1 == '.' or c3 == '=' and (
        c1 == '/' and c2 == '/' or
        c1 == '>' and c2 == '>' or
        c1 == '<' and c2 == '<' or
        c1 == '*' and c2 == '*'
    ):
        return pos + 3

    # 2-character operators
    if (
        c1 == '/' and c2 == '/' or
        c1 == '>' and c2 == '>' or
        c1 == '<' and c2 == '<' or
        c1 == '<' and c2 == '>' or
        c1 == '*' and c2 == '*' or
        c1 == '-' and c2 == '>' or
        c2 == '=' and c1 in '+-*/%@&|^:<>=!'
    ):
        return pos + 2

    # 1-character operators
    if c1 in '+-*/%@&|^,:!.;=~<>$?[]{}()':
        return pos + 1

    return None


def match_string(unicode data not None, Py_ssize_t prefix_pos, Py_ssize_t pos, /):
    """
    Given positions before and after the prefix, return one of the following:
      - `-1` if the string is unterminated.
      - `None` if not at the start of a string.
      - Tuple of (position after the string, need munge flag, number of
      newlines, position after the last newline or None if there is no newline).

    This function does not do any Python's syntax checks for strings, so the
    string need to be compiled again if it is used in Python expression.
    """

    cdef Py_ssize_t length = len(data)
    if pos >= length:
        return None

    cdef Py_UCS4 c = _get_c_unbounded(data, pos)
    if c not in '"\'`':
        return None

    # Check if we have a valid prefix. Otherwise we have (word, string) sequence.
    # # Valid prefixes are case-insensitive: r, u, b, br, rb, f, fr, rf
    cdef Py_ssize_t prefix_len = pos - prefix_pos
    cdef Py_UCS4 c1, c2
    cdef unicode prefix_lower
    cdef bint f_string = False
    if prefix_len == 1:
        c1 = _get_c_unbounded(data, prefix_pos)
        if c1 in 'fF':
            f_string = True
        elif c1 not in 'rRuUbB':
            return None

    elif prefix_len == 2:
        c1 = _get_c_unbounded(data, prefix_pos)
        c2 = _get_c_unbounded(data, prefix_pos + 1)
        prefix_lower = f"{c1}{c2}".lower()
        if prefix_lower in ('rf', 'fr'):
            f_string = True
        elif prefix_lower not in ('rb', 'br'):
            return None

    elif prefix_len != 0:
        return None

    pos += 1
    cdef Py_UCS4 quote = c
    cdef int quote_size = 1

    # Compute quote size
    if pos < length and _get_c_unbounded(data, pos) == quote:
        pos += 1

        if pos < length and _get_c_unbounded(data, pos) == quote:
            quote_size = 3
            pos += 1

        else:
            # Empty string
            return pos, False, 0, None

    cdef:
        int newlines = 0
        int brace_depth = 0
        int line_startpos = -1
        int end_quote_size = 0
        bint need_munge = False
        Py_UCS4 last_c = 0

    while end_quote_size != quote_size:
        # Unterminated string literal.
        if pos >= length:
            return -1

        last_c = c
        c = _get_c_unbounded(data, pos)

        # Skip escaped char.
        if c == '\\':
            end_quote_size = 0
            pos += 2
            continue

        pos += 1

        # In f-string, it is valid to have _anything_ inside {}, even comments
        # and strings with the same quotes. So here we look for closing brace
        # disregarding anything else.
        if f_string and c == '{' and pos < length and _get_c_unbounded(data, pos) != '{':
            end_quote_size = 0
            brace_depth = 1
            while brace_depth:
                # Unterminated string literal.
                if pos >= length:
                    return -1

                last_c = c
                c = _get_c_unbounded(data, pos)

                # Do not catch braces inside comments.
                if c == '#':
                    for i in range(pos, length):
                        if _get_c_unbounded(data, i) != '\n':
                            break
                    else:
                        # Unterminated string literal.
                        return -1

                    c = '\n'

                pos += 1

                if c == '{':
                    brace_depth += 1
                elif c == '}':
                    brace_depth -= 1
                elif c == '\n':
                    line_startpos = pos
                    newlines += 1

            continue

        if c == "\n":
            end_quote_size = 0
            line_startpos = pos
            newlines += 1

        elif c == quote:
            end_quote_size += 1
        else:
            end_quote_size = 0

        if last_c == "_" and c == "_":
            need_munge = True

    return pos, need_munge, newlines, line_startpos if newlines else None
