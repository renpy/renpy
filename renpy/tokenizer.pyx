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

cimport cython

from libc.string cimport memmove
from cpython.unicode cimport (
    PyUnicode_GET_LENGTH,
    PyUnicode_DATA,
    PyUnicode_KIND,
    PyUnicode_READ,
)

cpdef enum TokenKind:
    # A single '\n'.
    NEWLINE = 1
    # A '#' up to, but not including, the terminating newline.
    COMMENT = 2
    # The intersection of Python NAME and NUMBER, but less strict.
    WORD = 3
    # Python OP, plus '$' and '?'.
    OP = 4
    # The prefix and opening quote of a string literal.
    STRING_START = 5
    # A run of literal text inside a string literal.
    STRING_MIDDLE = 6
    # The closing quote of a string literal.
    STRING_END = 7
    # The end of the data.
    ENDMARKER = 8
    # Some kind of error. The string is the error message, the span is the
    # erroneous input (possibly empty).
    ERRORTOKEN = 9


cdef struct Pos:
    # Offset into the data, 1-based line number and 1-based column.
    Py_ssize_t pos
    Py_ssize_t lineno
    Py_ssize_t column


@cython.final
@cython.freelist(64)
cdef class TokenInfo:
    cdef readonly TokenKind kind
    cdef readonly str string
    cdef Pos _start
    cdef Pos _end

    def __init__(
        self,
        TokenKind kind,
        str string,
        Py_ssize_t start_pos,
        Py_ssize_t end_pos,
        Py_ssize_t start_lineno,
        Py_ssize_t start_column,
        Py_ssize_t end_lineno,
        Py_ssize_t end_column,
    ):
        # Python-level constructor. The tokenizer uses make_token instead.
        self.kind = kind
        self.string = string
        self._start = Pos(start_pos, start_lineno, start_column)
        self._end = Pos(end_pos, end_lineno, end_column)

    @property
    def span(self):
        """The (start, end) positions of the token in the source."""
        return (self._start.pos, self._end.pos)

    @property
    def start(self):
        """The starting (line number, column) of the token."""
        return (self._start.lineno, self._start.column)

    @property
    def end(self):
        """The ending (line number, column) of the token."""
        return (self._end.lineno, self._end.column)

    def __eq__(self, other):
        if not isinstance(other, TokenInfo):
            return NotImplemented

        cdef TokenInfo o = other
        return (
            self.kind == o.kind and
            self.string == o.string and
            self._start.pos == o._start.pos and
            self._start.lineno == o._start.lineno and
            self._start.column == o._start.column and
            self._end.pos == o._end.pos and
            self._end.lineno == o._end.lineno and
            self._end.column == o._end.column
        )

    def __repr__(self):
        return (
            f"TokenInfo(kind={TokenKind(self.kind)!r}, string={self.string!r}, "
            f"span={self.span!r}, start={self.start!r}, end={self.end!r})"
        )


cdef inline TokenInfo make_token(TokenKind kind, str string, Pos start, Pos end):
    # Bypasses __init__; uses the freelist.
    cdef TokenInfo t = TokenInfo.__new__(TokenInfo)
    t.kind = kind
    t.string = string
    t._start = start
    t._end = end
    return t


cdef inline bint is_ident_char(Py_UCS4 c) noexcept:
    return (
        'a' <= c <= 'z' or
        'A' <= c <= 'Z' or
        '0' <= c <= '9' or
        c == '_' or
        128 <= c <= 0x10FFFF
    )

cdef const Py_UCS4 EOF_CHAR = 0xFFFFFFFF

cdef enum:
    # The maximum nesting depth of brackets, strings and replacement fields.
    MAX_DEPTH = 300

cdef enum Context:
    # A '(', '[' or '{' in code.
    BRACKET = 1
    # A string literal; its content is literal text.
    STRING = 2
    # A replacement field inside a string; its content is code.
    FIELD = 3
    # A replacement field after ':'; its content is literal text.
    FIELD_SPEC = 4

cdef struct OpenToken:
    # One entry per construct the user opened.
    Context ctx
    # BRACKET: the bracket char. STRING/FIELD/FIELD_SPEC: the quote char
    # of the (enclosing) string.
    Py_UCS4 opener
    # STRING/FIELD/FIELD_SPEC: the (enclosing) string is triple-quoted.
    bint is_triple
    # STRING: the string may contain replacement fields - an f-string,
    # or any string when split_char is '['. FIELD/FIELD_SPEC: always True.
    bint allow_field
    # The span of the opening token.
    Pos start
    Pos end


cdef class Tokenizer:
    cdef readonly str data
    cdef readonly Py_ssize_t pos
    cdef readonly Py_ssize_t lineno
    cdef readonly Py_ssize_t line_start
    cdef readonly str split_char

    cdef Py_ssize_t length
    cdef int kind
    cdef const void *buf

    cdef Py_UCS4 open_char
    cdef Py_UCS4 close_char

    cdef OpenToken[MAX_DEPTH] open_tokens

    # When this exceeds MAX_DEPTH, the stack overflowed, an ERRORTOKEN
    # was emitted, and tokenization sticks to ENDMARKER.
    cdef Py_ssize_t open_tokens_size

    def __init__(
        self,
        str data not None,
        Py_ssize_t pos=0,
        Py_ssize_t lineno=1,
        str split_char not None="{",
    ):
        self.data = data
        self.length = PyUnicode_GET_LENGTH(data)
        self.kind = PyUnicode_KIND(data)
        self.buf = PyUnicode_DATA(data)

        if pos < 0 or pos > self.length:
            raise ValueError(f"pos {pos} out of range.")

        self.pos = pos
        self.lineno = lineno
        self.line_start = pos

        if split_char == "{":
            self.split_char = '{'
            self.open_char = '{'
            self.close_char = '}'
        elif split_char == "[":
            self.split_char = '['
            self.open_char = '['
            self.close_char = ']'
        else:
            raise ValueError(f"split_char must be '{{' or '[', not {split_char!r}.")

    @property
    def depth(self):
        return self.open_tokens_size

    # Low-level helpers.

    cdef inline Py_UCS4 peek(self, Py_ssize_t pos) noexcept:
        if pos < 0 or pos >= self.length:
            return EOF_CHAR

        return PyUnicode_READ(self.kind, self.buf, pos)

    cdef inline void newline(self, Py_ssize_t pos) noexcept:
        self.lineno += 1
        self.line_start = pos

    cdef inline Pos here(self) noexcept:
        return Pos(self.pos, self.lineno, self.pos - self.line_start + 1)

    cdef inline OpenToken *_top(self) noexcept:
        if self.open_tokens_size == 0:
            return NULL

        return &self.open_tokens[self.open_tokens_size - 1]

    # Matchers. Each returns the end of the match, or 0 if there is none.

    cdef Py_ssize_t whitespace(self, Py_ssize_t pos) noexcept:
        cdef:
            Py_ssize_t start_pos = pos
            Py_UCS4 c

        while (c := self.peek(pos)) != EOF_CHAR:
            if c == ' ':
                pos += 1
                continue

            if c == '\\' and self.peek(pos + 1) == '\n':
                pos += 2
                self.newline(pos)
                continue

            break

        return 0 if pos == start_pos else pos

    cdef Py_ssize_t word(self, Py_ssize_t pos) noexcept:
        cdef Py_ssize_t start_pos = pos

        while is_ident_char(self.peek(pos)):
            pos += 1

        return 0 if pos == start_pos else pos

    cdef Py_ssize_t operator(self, Py_ssize_t pos) noexcept:
        cdef:
            Py_UCS4 c1 = self.peek(pos + 0)
            Py_UCS4 c2 = self.peek(pos + 1)
            Py_UCS4 c3 = self.peek(pos + 2)

        # 3-character operators.
        if (c1 == '.' and c2 == '.' and c3 == '.') or c3 == '=' and (
            c1 == '/' and c2 == '/' or
            c1 == '>' and c2 == '>' or
            c1 == '<' and c2 == '<' or
            c1 == '*' and c2 == '*'
        ):
            return pos + 3

        # 2-character operators.
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

        # 1-character operators.
        if c1 in '+-*/%@&|^,:!.;=~<>$?[]{}()':
            return pos + 1

        return 0

    cdef Py_ssize_t comment(self, Py_ssize_t pos) noexcept:
        if self.peek(pos) != '#':
            return 0

        pos += 1

        cdef Py_UCS4 c
        while (c := self.peek(pos)) != '\n' and c != EOF_CHAR:
            pos += 1

        return pos

    cdef Py_ssize_t string_start(self, Py_ssize_t pos) noexcept:
        cdef Py_UCS4 c = self.peek(pos)

        # Prefix: r, u, b, f, rb, br, rf, fr (any case).
        if c in 'rR':
            pos += 1
            if self.peek(pos) in 'bBfF':
                pos += 1
        elif c in 'bBfF':
            pos += 1
            if self.peek(pos) in 'rR':
                pos += 1
        elif c in 'uU':
            pos += 1

        # Opening quote.
        c = self.peek(pos)
        if c not in '\'"`':
            return 0
        pos += 1

        # Triple quote.
        if self.peek(pos) == c and self.peek(pos + 1) == c:
            pos += 2

        return pos

    cdef Py_ssize_t string_middle(self, Py_ssize_t pos) noexcept:
        # Precondition: the top entry is STRING or FIELD_SPEC.
        cdef:
            OpenToken *top = self._top()
            Py_UCS4 quote = top.opener
            bint triple = top.is_triple
            bint in_spec = top.ctx == FIELD_SPEC
            bint allow_field = top.allow_field
            Py_ssize_t start_pos = pos
            Py_UCS4 c

        while (c := self.peek(pos)) != EOF_CHAR:
            # The escaped character is part of the string, whatever it is.
            if c == '\\':
                pos += 1
                c = self.peek(pos)
                if c == EOF_CHAR:
                    break

                pos += 1
                if c == '\n':
                    self.newline(pos)

                continue

            if c == '\n':
                pos += 1
                self.newline(pos)
                continue

            # Stop before an invalid character; it becomes an ERRORTOKEN.
            if c == '\t' or c < 32 or c == 127:
                break

            if c == quote:
                if not triple:
                    break

                if self.peek(pos + 1) == quote and self.peek(pos + 2) == quote:
                    break

            elif in_spec and c == self.close_char:
                break

            elif allow_field and c == self.open_char:
                if in_spec or self.peek(pos + 1) != self.open_char:
                    break

                pos += 1

            elif (
                allow_field and not in_spec and
                c == self.close_char and self.peek(pos + 1) == self.close_char
            ):
                pos += 1

            pos += 1

        return 0 if pos == start_pos else pos

    cdef Py_ssize_t string_end(self, Py_ssize_t pos) noexcept:
        # Precondition: the top entry is STRING or FIELD_SPEC.
        cdef:
            OpenToken *top = self._top()
            Py_UCS4 quote = top.opener

        if top.is_triple:
            if (
                self.peek(pos + 0) == quote and
                self.peek(pos + 1) == quote and
                self.peek(pos + 2) == quote
            ):
                return pos + 3
        elif self.peek(pos) == quote:
            return pos + 1

        return 0

    # Token construction.

    cdef inline TokenInfo _token(self, TokenKind kind, Pos start, Py_ssize_t end_pos):
        self.pos = end_pos
        return make_token(kind, self.data[start.pos:end_pos], start, self.here())

    cdef inline TokenInfo _error(self, str message, Pos start, Py_ssize_t end_pos):
        # An error covering data[start.pos:end_pos], which is skipped.
        self.pos = end_pos
        return make_token(ERRORTOKEN, message, start, self.here())

    cdef TokenInfo _invalid_char(self, Py_UCS4 c, Pos start):
        if c == '\\':
            return self._error(
                "unexpected character after line continuation character",
                start, start.pos + 1,
            )
        elif c == '\t':
            return self._error(
                "Tab character is not allowed in Ren'Py scripts",
                start, start.pos + 1,
            )
        elif c < 32 or c == 127:
            return self._error(
                f"ASCII control character {c!r} is not allowed in Ren'Py scripts",
                start, start.pos + 1,
            )

        # Should be unreachable.
        raise SystemError(f"Got printable character {c!r} on line {self.lineno}.")

    # Stack management.

    cdef TokenInfo _push(
        self,
        TokenInfo token,
        Context ctx,
        Py_UCS4 opener,
        bint is_triple,
        bint allow_field,
    ):
        # Returns the token, or an ERRORTOKEN if the stack is full. In that
        # case, tokenization sticks to ENDMARKER, as recovery would be too
        # complex.
        if self.open_tokens_size >= MAX_DEPTH:
            self.open_tokens_size = MAX_DEPTH + 1
            return make_token(
                ERRORTOKEN,
                f"more than {MAX_DEPTH} nested brackets and strings",
                token._start, token._end,
            )

        cdef OpenToken *entry = &self.open_tokens[self.open_tokens_size]
        entry.ctx = ctx
        entry.opener = opener
        entry.is_triple = is_triple
        entry.allow_field = allow_field
        entry.start = token._start
        entry.end = token._end
        self.open_tokens_size += 1
        return token

    cdef TokenInfo _push_string(self, TokenInfo token):
        # Derive the quote style from the STRING_START text. A prefix
        # character is never a quote, so the triple check is unambiguous.
        cdef:
            Py_ssize_t start = token._start.pos
            Py_ssize_t end = token._end.pos
            Py_UCS4 quote = self.peek(end - 1)
            bint triple = (
                end - start >= 3 and
                self.peek(end - 2) == quote and
                self.peek(end - 3) == quote
            )
            Py_ssize_t prefix_two_c = end - start - (3 if triple else 1)
            bint allow_field = (
                self.open_char == '[' or
                self.peek(start) in 'fF' or
                (prefix_two_c and self.peek(start + 1) in 'fF')
            )

        return self._push(token, STRING, quote, triple, allow_field)

    cdef TokenInfo _close_bracket(self, TokenInfo token, Py_UCS4 c):
        cdef Py_UCS4 opener = '(' if c == ')' else '[' if c == ']' else '{'

        # Happy path.
        if (
            self.open_tokens_size and
            self.open_tokens[self.open_tokens_size - 1].opener == opener
        ):
            self.open_tokens_size -= 1
            return token

        # Search down for a matching bracket, stopping at the enclosing
        # string or replacement field.
        cdef Py_ssize_t i
        for i in reversed(range(self.open_tokens_size)):
            if self.open_tokens[i].ctx != BRACKET or self.open_tokens[i].opener == opener:
                break
        else:
            i = -1

        if i < 0 or self.open_tokens[i].ctx != BRACKET:
            return make_token(ERRORTOKEN, f"unmatched '{c}'", token._start, token._end)

        # Mismatched: remove the matching entry from the middle of the stack.
        memmove(
            &self.open_tokens[i],
            &self.open_tokens[i + 1],
            (self.open_tokens_size - 1 - i) * sizeof(OpenToken),
        )
        self.open_tokens_size -= 1

        return make_token(
            ERRORTOKEN,
            f"closing parenthesis '{c}' does not match opening parenthesis "
            f"'{self.open_tokens[self.open_tokens_size - 1].opener}'",
            token._start, token._end,
        )

    cdef TokenInfo _end_of_input(self, Pos start, OpenToken *top):
        # Report one unclosed construct per call, then the ENDMARKER.
        cdef str message

        if top == NULL:
            return make_token(ENDMARKER, "", start, start)

        if top.ctx == STRING:
            message = "unterminated string literal"
        elif top.ctx == BRACKET:
            message = f"'{top.opener}' was never closed"
        else:
            message = f"'{self.open_char}' was never closed"

        self.open_tokens_size -= 1
        return make_token(ERRORTOKEN, message, top.start, top.end)

    # The tokenizer.

    cdef TokenInfo _literal_token(self, OpenToken *top, Pos start):
        # Inside a STRING or FIELD_SPEC: literal text and its terminators.
        cdef:
            Py_ssize_t end_pos
            Py_UCS4 c = self.peek(start.pos)
            TokenInfo token

        if end_pos := self.string_middle(start.pos):
            return self._token(STRING_MIDDLE, start, end_pos)

        if end_pos := self.string_end(start.pos):
            if top.ctx == FIELD_SPEC:
                # The quote ends the string, so the field is unclosed.
                # Report it, assume it was closed, and leave the quote to
                # be matched as STRING_END by the next call.
                self.open_tokens_size -= 1
                if self.open_char == '{':
                    return make_token(ERRORTOKEN, "f-string: expecting '}'", start, start)

                return make_token(ERRORTOKEN, "expecting ']'", start, start)

            self.open_tokens_size -= 1
            return self._token(STRING_END, start, end_pos)

        # The end of a format spec, which closes its field.
        if c == self.close_char and top.ctx == FIELD_SPEC:
            self.open_tokens_size -= 1
            return self._token(OP, start, start.pos + 1)

        # A replacement field.
        if c == self.open_char and top.allow_field:
            token = self._token(OP, start, start.pos + 1)
            return self._push(token, FIELD, top.opener, top.is_triple, True)

        return self._invalid_char(c, start)

    cdef TokenInfo _code_token(self, OpenToken *top, Pos start):
        # Outside of literal text: at top level, in brackets or in a FIELD.
        cdef:
            Py_ssize_t end_pos
            Py_UCS4 c = self.peek(start.pos)
            TokenInfo token

        if top != NULL and top.ctx == FIELD:
            # The end of the replacement field.
            if c == self.close_char:
                self.open_tokens_size -= 1
                return self._token(OP, start, start.pos + 1)

            # The format spec. Must come before operators, so that
            # f"{x:=5}" is a spec, not ':='.
            if c == ':':
                top.ctx = FIELD_SPEC
                return self._token(OP, start, start.pos + 1)

        # String quote with optional prefix.
        if end_pos := self.string_start(start.pos):
            token = self._token(STRING_START, start, end_pos)
            return self._push_string(token)

        # A word.
        if end_pos := self.word(start.pos):
            return self._token(WORD, start, end_pos)

        # An operator, which may open or close a bracket.
        if end_pos := self.operator(start.pos):
            token = self._token(OP, start, end_pos)

            if c == '(' or c == '[' or c == '{':
                return self._push(token, BRACKET, c, False, False)

            if c == ')' or c == ']' or c == '}':
                return self._close_bracket(token, c)

            return token

        # A comment.
        if end_pos := self.comment(start.pos):
            return self._token(COMMENT, start, end_pos)

        # A newline.
        if c == '\n':
            token = self._token(NEWLINE, start, start.pos + 1)
            self.newline(start.pos + 1)
            return token

        return self._invalid_char(c, start)

    cdef TokenInfo next_token_impl(self):
        cdef:
            OpenToken *top
            bint literal
            Py_ssize_t end_pos
            Pos start

        # The stack overflowed; stick to ENDMARKER.
        if self.open_tokens_size > MAX_DEPTH:
            start = self.here()
            return make_token(ENDMARKER, "", start, start)

        top = self._top()
        literal = top != NULL and (top.ctx == STRING or top.ctx == FIELD_SPEC)

        # Skip whitespace and continuations, except inside literal text.
        if not literal:
            if end_pos := self.whitespace(self.pos):
                self.pos = end_pos

        start = self.here()

        if start.pos >= self.length:
            return self._end_of_input(start, top)

        if literal:
            return self._literal_token(top, start)

        return self._code_token(top, start)

    def next_token(self):
        return self.next_token_impl()

    def iter_tokens(self):
        return _TokenIterator(self)


@cython.final
cdef class _TokenIterator:
    """Iterates over the tokens of a Tokenizer, through the ENDMARKER."""

    cdef Tokenizer tokenizer
    cdef bint done

    def __init__(self, Tokenizer tokenizer not None):
        self.tokenizer = tokenizer
        self.done = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.done:
            raise StopIteration

        cdef TokenInfo token = self.tokenizer.next_token_impl()
        if token.kind == ENDMARKER:
            self.done = True

        return token
