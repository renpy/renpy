# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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

from cpython.unicode cimport PyUnicode_GET_LENGTH, PyUnicode_DATA, PyUnicode_KIND, PyUnicode_READ


def match_whitespace(str data not None, Py_ssize_t pos, /):
    """
    Return position after the run of whitespace characters, or None
    if current position is not at the start of whitespace.
    """

    cdef int kind = PyUnicode_KIND(data)
    cdef const void *buf = PyUnicode_DATA(data)
    cdef Py_ssize_t length = PyUnicode_GET_LENGTH(data)
    cdef Py_ssize_t i = pos

    for i in range(pos, length):
        if PyUnicode_READ(kind, buf, i) != ' ':
            break
    else:
        i = length

    return None if i == pos else i


cdef inline bint is_ident_char(Py_UCS4 c) noexcept:
    # Condition is the same as `is_potential_identifier_char` in CPython.
    return (
        'a' <= c <= 'z' or
        'A' <= c <= 'Z' or
        '0' <= c <= '9' or
        c == '_' or
        c >= 128
    )


def match_logical_word(str data not None, Py_ssize_t pos, /):
    """
    Return position after the run of letters that are valid part
    of a logical word, or None if current position is not at the
    start of a logical word.
    """

    cdef int kind = PyUnicode_KIND(data)
    cdef const void *buf = PyUnicode_DATA(data)
    cdef Py_ssize_t length = PyUnicode_GET_LENGTH(data)
    cdef Py_ssize_t i = pos

    for i in range(pos, length):
        if not is_ident_char(PyUnicode_READ(kind, buf, i)):
            break
    else:
        i = length

    return None if i == pos else i


def match_operator(str data not None, Py_ssize_t pos, /):
    """
    Return position after the operator, or None if current position
    is not at the start of an operator.
    """

    cdef int kind = PyUnicode_KIND(data)
    cdef const void *buf = PyUnicode_DATA(data)
    cdef Py_ssize_t length = PyUnicode_GET_LENGTH(data)

    cdef Py_UCS4 c1 = 0
    if pos + 0 < length:
        c1 = PyUnicode_READ(kind, buf, pos + 0)

    cdef Py_UCS4 c2 = 0
    if pos + 1 < length:
        c2 = PyUnicode_READ(kind, buf, pos + 1)

    cdef Py_UCS4 c3 = 0
    if pos + 2 < length:
        c3 = PyUnicode_READ(kind, buf, pos + 2)

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


def match_string(str data not None, Py_ssize_t prefix_pos, Py_ssize_t pos, /):
    """
    Given positions before and after the prefix, return one of the following:
      - `-1` if the string is unterminated.
      - `None` if not at the start of a string.
      - Tuple of (position after the string, need munge flag, number of
      newlines, position after the last newline or None if there is no newline).

    This function does not do any Python's syntax checks for strings, so the
    string need to be compiled again if it is used in Python expression.
    """

    cdef int kind = PyUnicode_KIND(data)
    cdef const void *buf = PyUnicode_DATA(data)
    cdef Py_ssize_t length = PyUnicode_GET_LENGTH(data)

    if pos >= length:
        return None

    cdef Py_UCS4 c = PyUnicode_READ(kind, buf, pos)
    if c not in '"\'`':
        return None

    # Check if we have a valid prefix. Otherwise we have (word, string) sequence.
    # Valid prefixes are case-insensitive: r, u, b, br, rb, f, fr, rf
    cdef Py_ssize_t prefix_len = pos - prefix_pos
    cdef Py_UCS4 c1, c2
    cdef str prefix_lower
    cdef bint f_string = False
    if prefix_len == 1:
        c1 = PyUnicode_READ(kind, buf, prefix_pos)
        if c1 in 'fF':
            f_string = True
        elif c1 not in 'rRuUbB':
            return None

    elif prefix_len == 2:
        c1 = PyUnicode_READ(kind, buf, prefix_pos + 0)
        c2 = PyUnicode_READ(kind, buf, prefix_pos + 1)
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
    if pos < length and PyUnicode_READ(kind, buf, pos) == quote:
        pos += 1

        if pos < length and PyUnicode_READ(kind, buf, pos) == quote:
            quote_size = 3
            pos += 1

        else:
            # Empty string
            return pos, False, 0, None

    cdef:
        Py_ssize_t newlines = 0
        Py_ssize_t brace_depth = 0
        Py_ssize_t bracket_depth = 0
        Py_ssize_t spec_depth = -1
        Py_ssize_t line_startpos = -1
        Py_ssize_t nested_prefix = 0
        int end_quote_size = 0
        bint need_munge = False
        Py_UCS4 last_c = 0

    while end_quote_size != quote_size:
        # Unterminated string literal.
        if pos >= length:
            return -1

        last_c = c
        c = PyUnicode_READ(kind, buf, pos)

        pos += 1

        # Skip escaped char.
        if c == '\\':
            # Unterminated string literal (trailing backslash).
            if pos >= length:
                return -1

            # But line continuation should add to newlines.
            if PyUnicode_READ(kind, buf, pos) == '\n':
                line_startpos = pos + 1
                newlines += 1

            end_quote_size = 0
            pos += 1
            continue

        # `{{` and `}}` are escapes - consume both characters, so the second
        # one can not be mistaken for the start of a replacement field, i.e.
        # `f"{{"` is valid string.
        if f_string and c in '{}' and pos < length and PyUnicode_READ(kind, buf, pos) == c:
            end_quote_size = 0
            last_c = c
            pos += 1
            continue

        # In f-string, it is valid to have _anything_ inside {}, even comments
        # and strings with the same quotes. So here we look for closing brace
        # disregarding anything else.
        if f_string and c == '{':
            end_quote_size = 0
            brace_depth = 1
            while brace_depth:
                # Unterminated string literal.
                if pos >= length:
                    return -1

                last_c = c
                c = PyUnicode_READ(kind, buf, pos)

                # Inside a format spec everything is literal text, apart
                # from nested replacement fields, i.e.
                # `f"{x:#x}"` and `f"{x:'>10}"` are valid strings.
                if spec_depth != brace_depth:
                    # Try to parse a string here. '#' in the string should not
                    # be read as a comment.
                    # A quote here may be preceded by a string prefix, which
                    # has already been consumed by this loop as ordinary
                    # characters. Track back over at most two of them, so a
                    # nested f-string is recognized as an f-string.
                    nested_prefix = pos

                    while (
                        nested_prefix > 0 and
                        pos - nested_prefix < 2 and
                        PyUnicode_READ(kind, buf, nested_prefix - 1) in 'rRuUbBfF'
                    ):
                        nested_prefix -= 1

                    # The run is only a prefix if it starts a word, otherwise
                    # it is the tail of an identifier, like `format'x'`.
                    if nested_prefix > 0 and is_ident_char(
                        PyUnicode_READ(kind, buf, nested_prefix - 1)
                    ):
                        nested_prefix = pos

                    string_match = match_string(data, nested_prefix, pos)
                    if string_match == -1:
                        return -1
                    elif string_match is not None:
                        (
                            match_string_endpos,
                            match_need_munge,
                            match_newlines,
                            match_new_line_startpos,
                        ) = string_match
                        pos = match_string_endpos
                        need_munge = match_need_munge or need_munge
                        newlines += match_newlines
                        if match_new_line_startpos is not None:
                            line_startpos = match_new_line_startpos

                        last_c = 0
                        c = 0
                        continue

                    # Other parenthesis could contain valid `:`
                    if c == '(' or c == '[':
                        bracket_depth += 1
                    elif c == ')' or c == ']':
                        if bracket_depth:
                            bracket_depth -= 1
                    # Otherwise we could enter format specifier.
                    elif (
                        c == ':' and
                        bracket_depth == 0 and
                        spec_depth < 0 and
                        # Check for ':=' operator.
                        not (
                            pos + 1 < length and
                            PyUnicode_READ(kind, buf, pos + 1) == '='
                        )
                    ):
                        spec_depth = brace_depth

                    # Do not catch braces inside comments.
                    elif c == '#':
                        while (
                            pos < length and
                            PyUnicode_READ(kind, buf, pos) != '\n'
                        ):
                            pos += 1

                        # Unterminated string literal.
                        if pos >= length:
                            return -1

                        c = '\n'

                if c == '{':
                    brace_depth += 1
                elif c == '}':
                    brace_depth -= 1
                    # We no longer in format specifier when brace closes.
                    if spec_depth > brace_depth:
                        spec_depth = -1
                elif c == '\n':
                    line_startpos = pos
                    newlines += 1

                pos += 1
            continue

        if c == '\n':
            end_quote_size = 0
            line_startpos = pos
            newlines += 1

        elif c == quote:
            end_quote_size += 1
        else:
            end_quote_size = 0

        if last_c == '_' and c == '_':
            need_munge = True

    return pos, need_munge, newlines, line_startpos if newlines else None
