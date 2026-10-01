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



# Tokenizer for Ren'Py scripts. tokenizer.pyi documents the token stream and
# the public API. This comment only covers how the code is built.
#
# - Each call to next_token() reads one token and doesn't keep any token
#   history. All the state it needs is the position, the line number and
#   a stack of open constructs.
#
# - The OpenToken stack has one entry per open bracket, string, field or
#   format spec. Entry 0 is the top level and is never popped. The ctx of
#   the top entry chooses the mode: if it's below STRING, the input is read
#   as code; otherwise it's read as literal text. Each entry also stores
#   the string's quote, whether it's triple-quoted, and the characters that
#   open and close a field. A field copies its string's entry when pushed,
#   so the string-middle scanner only ever looks at the top entry.
#
# - Stack storage: the first 16 entries are inline in the object. If
#   nesting goes deeper, the whole stack moves to one heap block sized for
#   MAX_DEPTH, and it never grows again. Once the depth limit is hit, one
#   ERRORTOKEN is emitted and every later call returns ENDMARKER.
#
# - Buffer access: next_token() checks the string's PyUnicode kind once.
#   Everything else is a fused-type specialization (ucs_t) that indexes the
#   raw buffer directly. peek() returns EOF_CHAR (0x110000) when reading
#   past the end, so none of the scanners need a separate end-of-input
#   check.
#
# - Character tests use the 256-entry CHARS table. The low 4 bits hold the
#   character's class when it starts a token, and the high bits hold flags
#   (F_IDENT, F_STRING_SPECIAL). Code points of 256 and above are always
#   identifier characters, and are handled outside the table.
#
# - Token text comes from slicing data on the fly. Error tokens put their
#   message in string instead.
#
# - When a bracket doesn't match, the code searches down the stack, but
#   stops at the nearest string. If it finds the matching opener, it
#   removes that entry so the brackets around it stay paired.

# cython: boundscheck=False, wraparound=False

cimport cython

from libc.string cimport memmove, memcpy
from libc.stdint cimport uint8_t, uint16_t, uint32_t
from cpython.mem cimport PyMem_Malloc, PyMem_Free
from cpython.unicode cimport (
    PyUnicode_GET_LENGTH,
    PyUnicode_DATA,
    PyUnicode_KIND,
    PyUnicode_1BYTE_KIND,
    PyUnicode_2BYTE_KIND,
)


# ---------------------------------------------------------------------------
# Tokens
# ---------------------------------------------------------------------------

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
    # Offset into the data
    Py_ssize_t pos
    # 1-based line number
    Py_ssize_t lineno
    # 1-based column
    Py_ssize_t column


@cython.final
@cython.no_gc
@cython.freelist(64)
cdef class TokenInfo:
    cdef readonly TokenKind kind
    # The token text. When None, it is sliced out of _data on first access.
    cdef readonly str string
    # The source the token was cut from, or None if _string is set eagerly.
    cdef str _data
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
        self.kind = kind
        self.string = string
        self._start = Pos(start_pos, start_lineno, start_column)
        self._end = Pos(end_pos, end_lineno, end_column)

    @property
    def span(self):
        return (self._start.pos, self._end.pos)

    @property
    def start(self):
        return (self._start.lineno, self._start.column)

    @property
    def end(self):
        return (self._end.lineno, self._end.column)

    def __eq__(self, other):
        if not isinstance(other, TokenInfo):
            return NotImplemented

        cdef TokenInfo o = other
        return (
            self.kind == o.kind
            and self._start.pos == o._start.pos
            and self._start.lineno == o._start.lineno
            and self._start.column == o._start.column
            and self._end.pos == o._end.pos
            and self._end.lineno == o._end.lineno
            and self._end.column == o._end.column
            and self.string == o.string
        )

    def __repr__(self):
        return (
            f"TokenInfo(kind={TokenKind(self.kind)!r}, string={self.string!r}, "
            f"span={self.span!r}, start={self.start!r}, end={self.end!r})"
        )


# ---------------------------------------------------------------------------
# Character tables and helper functions
# ---------------------------------------------------------------------------

# Low 4 bits of a CHARS entry: the CharClass of a character when it starts
# a token. Classes are mutually exclusive.
cdef enum CharClass:
    CC_EOF = 0
    CC_NEWLINE = 1
    CC_COMMENT = 2
    # A quote, which always starts a string.
    CC_QUOTE = 3
    # An identifier char that may start a string prefix (r, u, b, f).
    CC_PREFIX = 4
    # Any other identifier char.
    CC_IDENT = 5
    # '(', '[' or '{'.
    CC_OPEN = 6
    # ')', ']' or '}'.
    CC_CLOSE = 7
    # Any other operator char; always a valid operator start.
    CC_OP = 8

cdef enum:
    # Must cover every CharClass value (<= 15), or classes collide with flags.
    CLASS_MASK = 0x0F
    # Independent flags, OR-ed on top of the class.
    # May continue an identifier: [a-zA-Z0-9_] and everything >= 0x80.
    F_IDENT = 0x10
    # Needs handling inside string literal text: control chars, escapes,
    # quotes and replacement field chars. Anything else is plain text.
    F_STRING_SPECIAL = 0x20

# One entry per byte value: class in the low bits, flags in the high bits.
# Code points >= 256 are never looked up; the helpers below handle them.
cdef uint8_t CHARS[256]

cdef void _init_tables() noexcept:
    cdef int c

    for c in range(128, 256):
        CHARS[c] = CC_IDENT
    for c in b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_':
        CHARS[c] = CC_IDENT
    for c in b'rRuUbBfF':
        CHARS[c] = CC_PREFIX
    for c in b'+-*/%@&|^,:!.;=~<>$?':
        CHARS[c] = CC_OP
    for c in b'([{':
        CHARS[c] = CC_OPEN
    for c in b')]}':
        CHARS[c] = CC_CLOSE
    for c in b'\'"`':
        CHARS[c] = CC_QUOTE
    CHARS[ord('#')] = CC_COMMENT
    CHARS[ord('\n')] = CC_NEWLINE

    for c in range(128, 256):
        CHARS[c] |= F_IDENT
    for c in b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_':
        CHARS[c] |= F_IDENT
    for c in range(32):
        CHARS[c] |= F_STRING_SPECIAL
    CHARS[127] |= F_STRING_SPECIAL
    for c in b'\\\'"`{}[]':
        CHARS[c] |= F_STRING_SPECIAL

_init_tables()

cdef enum:
    MAX_UNICODE = 0x10FFFF
    EOF_CHAR = 0x110000

cdef inline CharClass char_class(Py_UCS4 c) noexcept:
    if c < 256:
        return <CharClass>(CHARS[c] & CLASS_MASK)
    return CC_EOF if c == EOF_CHAR else CC_IDENT

cdef inline bint is_ident_char(Py_UCS4 c) noexcept:
    if c < 256:
        return (CHARS[c] & F_IDENT) != 0
    return c != EOF_CHAR

cdef inline bint is_string_special(Py_UCS4 c) noexcept:
    if c < 256:
        return (CHARS[c] & F_STRING_SPECIAL) != 0
    return c == EOF_CHAR

# The tokenizer is specialized on the unicode kind of its input, so the
# hot loops read characters straight from the buffer.
ctypedef fused ucs_t:
    uint8_t   # Py_UCS1
    uint16_t  # Py_UCS2
    uint32_t  # Py_UCS4

cdef inline Py_UCS4 peek(const ucs_t *buf, Py_ssize_t length, Py_ssize_t pos) noexcept:
    if 0 <= pos < length:
        return buf[pos]
    return EOF_CHAR

# ---------------------------------------------------------------------------
# The bracket / string stack
# ---------------------------------------------------------------------------

cdef enum:
    # Stack entries embedded in a Tokenizer. Deeper nesting moves the
    # whole stack to a single heap block of MAX_DEPTH entries.
    INLINE_DEPTH = 15
    # The maximum nesting depth of brackets, strings and replacement fields.
    MAX_DEPTH = 255

cdef enum Context:
    # The bottom of the stack: top-level code. Never removed.
    NOTHING = 0
    # A '(', '[' or '{' in code.
    BRACKET = 1
    # A replacement field inside a string.
    FIELD = 2
    # Contexts below are parsed as literal text.
    # A Python string literal.
    STRING = 3
    # A Ren'Py string passed to renpy_substitution_string.
    RENPY_STRING = 4
    # A replacement field after ':'.
    FIELD_SPEC = 5

cdef struct OpenToken:
    Context ctx
    # The char reported as "never closed" at end of input: the bracket
    # for BRACKET, the field opener for FIELD/FIELD_SPEC, 0 for strings.
    # Never modified after push.
    Py_UCS4 open_char
    # BRACKET: the bracket char.
    # STRING/FIELD/FIELD_SPEC: the quote char of the enclosing string.
    # RENPY_STRING: EOF_CHAR, which never matches a real char.
    Py_UCS4 opener
    # Whether the enclosing string is triple-quoted.
    bint is_triple
    # The char that opens a replacement field here.
    # STRING: '{' or EOF_CHAR. RENPY_STRING: '['.
    # FIELD: the char that opened this field.
    # FIELD_SPEC: same, except EOF_CHAR for Ren'Py specs, where '[' and '{'
    # are literal text.
    Py_UCS4 field_open
    # The char that closes a field opened by field_open.
    Py_UCS4 field_close
    # The position of the opening bracket or first char of STRING_OPEN.
    Pos pos


# ---------------------------------------------------------------------------
# The tokenizer
# ---------------------------------------------------------------------------

@cython.final
@cython.freelist(4)
cdef class Tokenizer:
    cdef readonly str data
    cdef readonly Py_ssize_t pos
    cdef readonly Py_ssize_t lineno
    cdef readonly Py_ssize_t line_start

    cdef Py_ssize_t length
    cdef int kind
    cdef const void *buf

    # Most lines have very low depth. On overflow, the stack moves to a heap
    # block of MAX_DEPTH entries.
    cdef OpenToken _inline_tokens[INLINE_DEPTH + 1]
    cdef OpenToken *open_tokens
    # Index of currently open tokens.
    cdef Py_ssize_t open_tokens_index

    def __cinit__(self, str data not None, Py_ssize_t pos=0, Py_ssize_t lineno=1):
        self.open_tokens = &self._inline_tokens[0]
        self.open_tokens[0].ctx = NOTHING
        self.open_tokens[0].open_char = EOF_CHAR
        self.open_tokens[0].opener = EOF_CHAR
        self.open_tokens[0].is_triple = False
        self.open_tokens[0].field_open = 0
        self.open_tokens[0].field_close = 0
        self.open_tokens[0].pos = Pos(pos, lineno, 1)
        self.open_tokens_index = 0

        self.data = data
        self.length = PyUnicode_GET_LENGTH(data)
        self.kind = PyUnicode_KIND(data)
        self.buf = PyUnicode_DATA(data)

        if not 0 <= pos <= self.length:
            raise ValueError(f"pos {pos} out of range.")

        self.pos = pos
        self.lineno = lineno
        self.line_start = pos

    @classmethod
    def renpy_substitution_string(cls, str data not None):
        cdef Tokenizer self = Tokenizer.__new__(Tokenizer, data)

        cdef OpenToken *entry = &self.open_tokens[1]
        entry.ctx = RENPY_STRING
        entry.open_char = 0
        entry.opener = EOF_CHAR
        entry.is_triple = False
        entry.field_open = '['
        entry.field_close = ']'
        entry.pos = Pos(0, 1, 1)
        self.open_tokens_index += 1

        return self

    def __dealloc__(self):
        if self.open_tokens != &self._inline_tokens[0]:
            PyMem_Free(self.open_tokens)

    @property
    def depth(self):
        return self.open_tokens_index

    cpdef TokenInfo next_token(self):
        # Dispatch once on the unicode kind; everything below works on a
        # specialized buffer pointer.
        if self.kind == PyUnicode_1BYTE_KIND:
            return self._next_token(<const uint8_t *>self.buf)
        if self.kind == PyUnicode_2BYTE_KIND:
            return self._next_token(<const uint16_t *>self.buf)
        else:
            return self._next_token(<const uint32_t *>self.buf)

    def iter_tokens(self):
        return _TokenIterator(self)

    # -- Helpers ------------------------------------------------------------

    cdef inline void _newline(self, Py_ssize_t pos) noexcept:
        self.lineno += 1
        self.line_start = pos

    cdef inline Pos _pos_at(self, Py_ssize_t pos) noexcept:
        return Pos(pos, self.lineno, pos - self.line_start + 1)

    cdef inline TokenInfo _make_token(self, TokenKind kind, Pos start, Pos end):
        cdef TokenInfo t = TokenInfo.__new__(TokenInfo)
        t.kind = kind
        t.string = self.data[start.pos:end.pos]
        t._start = start
        t._end = end
        self.pos = end.pos
        return t

    cdef inline TokenInfo _error_token(self, str string, Pos start, Pos end):
        cdef TokenInfo t = TokenInfo.__new__(TokenInfo)
        t.kind = ERRORTOKEN
        t.string = string
        t._start = start
        t._end = end
        return t

    # -- Stack --------------------------------------------------------------

    cdef inline OpenToken *_next_open_token(self) except NULL:
        cdef OpenToken *new_stack

        if self.open_tokens_index >= MAX_DEPTH:
            raise SystemError("Called Tokenizer._push with tokens stack exhausted.")

        if (
            self.open_tokens_index >= INLINE_DEPTH
            and self.open_tokens == &self._inline_tokens[0]
        ):
            # The unlikely case: move the whole stack to the heap in one
            # go, with room for every entry up to MAX_DEPTH.
            new_stack = <OpenToken *> PyMem_Malloc((MAX_DEPTH + 1) * sizeof(OpenToken))
            if new_stack == NULL:
                raise MemoryError
            memcpy(new_stack, self.open_tokens, (INLINE_DEPTH + 1) * sizeof(OpenToken))
            self.open_tokens = new_stack

        self.open_tokens_index += 1
        return &self.open_tokens[self.open_tokens_index]

    cdef inline str _close_bracket(self, Py_UCS4 c):
        cdef Py_UCS4 opener = '(' if c == ')' else '[' if c == ']' else '{'

        # Likely case of correct closing bracket.
        if self.open_tokens[self.open_tokens_index].opener == opener:
            self.open_tokens_index -= 1
            return None

        # Search down for the matching bracket on the stack.
        cdef Py_ssize_t i
        for i in range(self.open_tokens_index - 1, 0, -1):
            # Open string stops scanning because it delimits brackets stack.
            if self.open_tokens[i].ctx != BRACKET:
                break

            # Mismatched: remove the matching entry from the middle of the stack
            # and return it as ERRORTOKEN.
            if self.open_tokens[i].opener == opener:
                memmove(
                    &self.open_tokens[i],
                    &self.open_tokens[i + 1],
                    (self.open_tokens_index - i) * sizeof(OpenToken),
                )
                self.open_tokens_index -= 1

                return (
                    f"closing parenthesis '{c}' does not match opening parenthesis "
                    f"'{self.open_tokens[self.open_tokens_index].opener}'"
                )

        return f"unmatched '{c}'"

    # -- Matchers -----------------------------------------------------------

    cdef inline Py_ssize_t _whitespace(self, const ucs_t *buf, Py_ssize_t pos) noexcept:
        # Returns pos unchanged if there is no whitespace.
        cdef Py_ssize_t length = self.length
        cdef Py_UCS4 c
        while True:
            c = peek(buf, length, pos)
            if c == ' ':
                pos += 1
            elif c == '\\' and peek(buf, length, pos + 1) == '\n':
                pos += 2
                self._newline(pos)
            else:
                return pos

    cdef inline Py_ssize_t _comment(self, const ucs_t *buf, Py_ssize_t pos) noexcept:
        # A '#' up to, but not including, the newline.
        # Precondition: buf[pos] == '#'.
        cdef Py_ssize_t length = self.length
        cdef Py_UCS4 c
        pos += 1
        while True:
            c = peek(buf, length, pos)
            if c == '\n' or c == EOF_CHAR:
                return pos
            pos += 1

    cdef inline Py_ssize_t _word(self, const ucs_t *buf, Py_ssize_t pos) noexcept:
        # Return pos unchanged if not at identifier char.
        cdef Py_ssize_t length = self.length
        while is_ident_char(peek(buf, length, pos)):
            pos += 1

        return pos

    cdef inline Py_ssize_t _operator(self, const ucs_t *buf, Py_ssize_t pos) noexcept:
        # Precondition: char_class(buf[pos]) == CC_OP
        cdef Py_ssize_t length = self.length
        cdef Py_UCS4 c1 = peek(buf, length, pos)
        cdef Py_UCS4 c2 = peek(buf, length, pos + 1)
        cdef Py_UCS4 c3 = peek(buf, length, pos + 2)
        # //, >>, <<, **
        cdef bint doubled = c1 == c2 and c1 in '/><*'

        # ..., //=, >>=, <<=, **=
        if (c1 == '.' and c2 == '.' and c3 == '.') or (doubled and c3 == '='):
            return pos + 3

        # //, >>, <<, **, <>, ->, and augmented assignment / comparison.
        if (
            doubled
            or (c1 == '<' and c2 == '>')
            or (c1 == '-' and c2 == '>')
            or (c2 == '=' and c1 in '+-*/%@&|^:<>=!')
        ):
            return pos + 2

        return pos + 1

    cdef inline Py_ssize_t _string_start(self, const ucs_t *buf, Py_ssize_t pos) except -1:
        # An optional prefix (r, u, b, f, rb, br, rf, fr, any case) and
        # an opening quote, which may be tripled.
        cdef Py_ssize_t length = self.length
        cdef Py_ssize_t start_pos = pos
        cdef Py_UCS4 c = peek(buf, length, pos)
        cdef bint is_f = False
        cdef Py_UCS4 quote

        if c in 'rR':
            pos += 1
            c = peek(buf, length, pos)
            if c in 'bBfF':
                is_f = c in 'fF'
                pos += 1
        elif c in 'bBfF':
            is_f = c in 'fF'
            pos += 1
            if peek(buf, length, pos) in 'rR':
                pos += 1
        elif c in 'uU':
            pos += 1

        quote = peek(buf, length, pos)
        if quote not in '\'"`':
            return pos

        # Prefill the next open token struct.
        cdef OpenToken *next = self._next_open_token()
        next.ctx = STRING
        next.open_char = 0
        next.opener = quote
        next.is_triple = False
        next.field_open = '{' if is_f else EOF_CHAR
        next.field_close = '}' if is_f else EOF_CHAR
        next.pos = self._pos_at(start_pos)

        pos += 1

        if peek(buf, length, pos) == quote and peek(buf, length, pos + 1) == quote:
            next.is_triple = True
            pos += 2

        return pos

    cdef inline Py_ssize_t _string_middle(self, const ucs_t *buf, Py_ssize_t pos) noexcept:
        # A run of literal text, up to a closing quote, a replacement
        # field, the end of a format spec, or an invalid character.
        cdef Py_ssize_t length = self.length
        cdef OpenToken *top = &self.open_tokens[self.open_tokens_index]
        # EOF_CHAR for RENPY_STRING, so the quote never matches there.
        cdef Py_UCS4 quote = top.opener
        cdef Py_UCS4 c

        while True:
            c = peek(buf, length, pos)

            # Fast path: plain text.
            if not is_string_special(c):
                pos += 1
                continue

            if c == EOF_CHAR:
                break

            # An escape. The escaped char is literal, whatever it is.
            if c == '\\':
                pos += 1
                c = peek(buf, length, pos)
                if c == EOF_CHAR:
                    break
                pos += 1
                if c == '\n':
                    self._newline(pos)
                continue

            if c == '\n':
                pos += 1
                self._newline(pos)
                continue

            # A control char (including tab) becomes an ERRORTOKEN.
            if c < 32 or c == 127:
                break

            if c == quote:
                if not top.is_triple:
                    break
                if (
                    peek(buf, length, pos + 1) == quote
                    and peek(buf, length, pos + 2) == quote
                ):
                    break

            elif top.ctx == FIELD_SPEC:
                # The close char ends the spec; an open char starts a nested field.
                if c == top.field_close or c == top.field_open:
                    break

            elif c == top.field_open:
                # A lone open char starts a field; a doubled one is literal.
                if peek(buf, length, pos + 1) != top.field_open:
                    break
                pos += 1

            pos += 1

        return pos

    cdef inline Py_ssize_t _string_end(self, const ucs_t *buf, Py_ssize_t pos) noexcept:
        cdef Py_ssize_t length = self.length
        cdef OpenToken *top = &self.open_tokens[self.open_tokens_index]
        cdef Py_UCS4 quote = top.opener

        # RENPY_STRING's EOF_CHAR opener must never match the end of data.
        if pos >= length or peek(buf, length, pos) != quote:
            return pos

        if not top.is_triple:
            return pos + 1

        if (
            peek(buf, length, pos + 1) == quote
            and peek(buf, length, pos + 2) == quote
        ):
            return pos + 3

        return pos

    # -- Dispatch -----------------------------------------------------------

    cdef TokenInfo _next_token(self, const ucs_t *buf):
        cdef OpenToken *top
        cdef OpenToken *next
        cdef Py_ssize_t length = self.length
        cdef Py_ssize_t end_pos, prefix_end, i
        cdef Pos start, end
        cdef Py_UCS4 quote, c
        cdef CharClass cls
        cdef TokenInfo token
        cdef str message

        # The stack overflowed; stick to ENDMARKER.
        if self.open_tokens_index > MAX_DEPTH:
            start = self._pos_at(self.pos)
            return self._make_token(ENDMARKER, start, start)

        top = &self.open_tokens[self.open_tokens_index]

        # Whitespace is significant inside literal text.
        if top.ctx < STRING:
            self.pos = self._whitespace(buf, self.pos)

        # The end of the input. Report one unclosed construct per call, then the ENDMARKER.
        if self.pos >= length:
            if top.ctx == NOTHING or top.ctx == RENPY_STRING:
                end = self._pos_at(length)
                return self._make_token(ENDMARKER, end, end)

            if top.open_char:
                message = f"'{top.open_char}' was never closed"
            else:
                message = "unterminated string literal"

            self.open_tokens_index -= 1
            end = Pos(top.pos.pos + 1, top.pos.lineno, top.pos.column + 1)
            return self._error_token(message, top.pos, end)

        start = self._pos_at(self.pos)

        # No room to open another construct; report the offending
        # character, then stick to ENDMARKER.
        if self.open_tokens_index == MAX_DEPTH:
            self.open_tokens_index += 1
            return self._error_token(
                f"more than {MAX_DEPTH} nested brackets and strings",
                start, self._pos_at(start.pos + 1),
            )

        c = peek(buf, length, start.pos)
        cls = char_class(c)

        if top.ctx >= STRING:
            # Inside a STRING, RENPY_STRING or FIELD_SPEC:
            # literal text and whatever ends it.
            if (end_pos := self._string_middle(buf, start.pos)) != start.pos:
                return self._make_token(STRING_MIDDLE, start, self._pos_at(end_pos))

            if (end_pos := self._string_end(buf, start.pos)) != start.pos:
                self.open_tokens_index -= 1

                if top.ctx == FIELD_SPEC:
                    # The quote ends the string, so the field is unclosed.
                    # Report it, treat the field as closed, and leave the quote
                    # to become a STRING_END on the next call.
                    if top.open_char == '{':
                        message = "f-string: expecting '}'"
                    else:
                        message = "expecting ']'"
                    return self._error_token(message, start, start)

                return self._make_token(STRING_END, start, self._pos_at(end_pos))

            # The end of a format spec, which also closes its field.
            if top.ctx == FIELD_SPEC and c == top.field_close:
                self.open_tokens_index -= 1
                return self._make_token(OP, start, self._pos_at(start.pos + 1))

            if c == top.field_open:
                # A replacement field.
                next = self._next_open_token()
                memcpy(next, top, sizeof(OpenToken))
                next.ctx = FIELD
                next.open_char = next.field_open
                next.pos = start
                return self._make_token(OP, start, self._pos_at(start.pos + 1))

            # Anything else is a control character, handled below.

        else:
            # Outside literal text: at top level, in brackets, or in a FIELD.
            if top.ctx == FIELD:
                # The end of the replacement field.
                if c == top.field_close:
                    self.open_tokens_index -= 1
                    return self._make_token(OP, start, self._pos_at(start.pos + 1))

                # The start of a format spec. Checked before operators,
                # so f"{x:=5}" is a spec rather than ':='.
                if c == ':':
                    top.ctx = FIELD_SPEC
                    # Ren'Py specs do not nest substitutions; '[' is literal text there.
                    if top.field_open == '[':
                        top.field_open = EOF_CHAR
                    return self._make_token(OP, start, self._pos_at(start.pos + 1))

            # Ordered roughly by frequency in Ren'Py scripts.
            if cls == CC_IDENT:
                return self._make_token(WORD, start, self._pos_at(self._word(buf, start.pos)))

            if cls == CC_PREFIX or cls == CC_QUOTE:
                # An optional prefix and an opening quote.
                # A prefix may fail to start a string, for a word like "fred".
                # Sets next OpenToken to STRING on success.
                end_pos = self._string_start(buf, start.pos)
                if self.open_tokens[self.open_tokens_index].ctx == STRING:
                    return self._make_token(STRING_START, start, self._pos_at(end_pos))

                return self._make_token(WORD, start, self._pos_at(self._word(buf, end_pos)))

            if cls == CC_NEWLINE:
                token = self._make_token(NEWLINE, start, self._pos_at(start.pos + 1))
                self._newline(start.pos + 1)
                return token

            if cls == CC_COMMENT:
                return self._make_token(COMMENT, start, self._pos_at(self._comment(buf, start.pos)))

            if cls == CC_OPEN:
                next = self._next_open_token()
                next.ctx = BRACKET
                next.open_char = c
                next.opener = c
                next.pos = start
                return self._make_token(OP, start, self._pos_at(start.pos + 1))

            if cls == CC_CLOSE:
                message = self._close_bracket(c)
                if message is not None:
                    # Consume the bracket so the error is not repeated.
                    self.pos = start.pos + 1
                    return self._error_token(message, start, self._pos_at(start.pos + 1))

                return self._make_token(OP, start, self._pos_at(start.pos + 1))

            if cls == CC_OP:
                return self._make_token(OP, start, self._pos_at(self._operator(buf, start.pos)))

            # CC_EOF: a character that cannot start a token, handled below.

        # An invalid character: in code, a tab, a line continuation or a
        # control character; in literal text, a control character.
        if c == '\\':
            message = "unexpected character after line continuation character"
        elif c == '\t':
            message = "Tab character is not allowed in Ren'Py scripts"
        elif c < 32 or c == 127:
            message = f"ASCII control character {c!r} is not allowed in Ren'Py scripts"
        else:
            raise SystemError(f"Got printable character {c!r} on line {self.lineno}.")

        # Consume the character so the error is not repeated.
        self.pos = start.pos + 1
        return self._error_token(message, start, self._pos_at(start.pos + 1))


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

        cdef TokenInfo token = self.tokenizer.next_token()
        if token.kind == ENDMARKER:
            self.done = True

        return token
