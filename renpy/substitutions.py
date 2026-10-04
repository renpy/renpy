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

# This file contains support for string translation and string formatting
# operations.

import collections
import string
import sys
from collections.abc import Iterator, Mapping
from typing import Literal

import renpy
from renpy.tokenizer import Tokenizer, TokenKind

flags = frozenset({
    "u",  # Upper
    "t",  # Translate
    "q",  # Quote
    "s",  # String
    "r",  # Raw
    "l",  # Lower
    "i",  # Interpolate
    "f",  # Filter
    "c",  # Capitalize
    "!",  # Extra conversion flags
})
formatter = string.Formatter()


class SubstitutionError(ValueError):
    """
    Raised when a Ren'Py substitution is malformed.
    """

    pos: int
    "The position in the original string where the error occurred."

    def __init__(self, message: str, pos: int):
        super().__init__(message)
        self.message = message
        self.pos = pos


def parse(s: str) -> Iterator[tuple[Literal["literal", "expr", "conv", "fmt"], str]]:
    """
    Parses `s` according to Ren'Py's string formatting rules, yielding a
    stream of (kind, value) tokens:

        ("literal", text) -- literal text outside any substitution.
        ("expr", code)    -- a substitution's expression.
        ("conv", spec)    -- the conversion specifier for the preceding "expr".
        ("fmt", spec)     -- the format spec for the preceding "expr".

    Yields ("literal", "") if new substitution or end of the string is reached
    after a substitution.

    Malformed input raises SubstitutionError with a position to blame.
    """

    FLAGS = flags
    seen_literal = True

    tokenizer = Tokenizer.renpy_substitution_string(s)
    tokens = tokenizer.iter_tokens()

    for token in tokens:
        kind = token.kind

        if kind is TokenKind.ERRORTOKEN:
            raise SubstitutionError(token.string, token.span[0])

        if kind is TokenKind.ENDMARKER:
            if not seen_literal:
                yield "literal", ""
            return

        if kind is TokenKind.STRING_MIDDLE:
            # The tokenizer keeps a doubled "[[" in literal text; it escapes
            # a single "[" here. There is no closing-bracket escape.
            yield "literal", token.string.replace("[[", "[")
            seen_literal = True
            continue

        assert kind is TokenKind.OP and token.string == "[", f"unexpected token {token.kind}."
        assert tokenizer.depth == 2, "Tokenizer depth is not 2 when entering replacement field."

        if not seen_literal:
            yield "literal", ""

        # New replacement field.
        stage = "expr"
        opener = token
        start = token.span[1]
        conv_seen = False
        seen_literal = False

        for token in tokens:
            kind = token.kind

            if kind is TokenKind.ERRORTOKEN:
                raise SubstitutionError(token.string, token.span[0])

            if kind is TokenKind.ENDMARKER:
                raise SubstitutionError(f"string {s!r} ends with an open format operation", opener.span[0])

            if kind is not TokenKind.OP:
                continue

            text = token.string

            if text not in ("!", ":", "]"):
                continue

            # "[foo[0:]]"
            if tokenizer.depth > (1 if text == "]" else 2):
                continue

            a, b = token.span

            if stage == "expr":
                code = s[start:a].strip()
                # "[]", "[!]" or "[:]"
                if not code:
                    raise SubstitutionError("expected expression", opener.span[0])

                yield "expr", code
                start = b

                if text == "]":
                    break
                elif text == "!":
                    stage = "conv"
                elif text == ":":
                    stage = "fmt"

            elif stage == "conv":
                # "[foo!!]", "[foo!i!]" or "[foo!i!t]"
                # Could be more strict, but for now we just skip over '!' characters.
                if text == "!":
                    continue

                conv = s[start:a]
                # "[foo!]"
                if not conv:
                    raise SubstitutionError("conversion specifier cannot be empty", start)

                # "[foo!invalid-flag]"
                for i, c in enumerate(conv):
                    if c not in FLAGS:
                        raise SubstitutionError(f"invalid conversion character {c!r}", start + i)

                yield "conv", conv
                conv_seen = True
                start = b

                if text == "]":
                    break

                stage = "fmt"

            else:  # fmt: raw text up to the closing ']'
                assert text == "]", f"Unexpected token {text!r} in format stage."

                spec = s[start:a]

                # Undocumented Ren'Py rule: "[x:>10!i]" - if everything after
                # the last '!' is a valid flag, it's a conversion; otherwise
                # the '!' is literal format text. Not applicable if a
                # conversion was already given before the ':'.
                if not conv_seen:
                    head, bang, tail = spec.rpartition("!")
                    if bang and tail and set(tail).issubset(FLAGS):
                        yield "conv", tail
                        yield "fmt", head
                        break

                yield "fmt", spec
                break


def interpolate(s: str, scope: Mapping[str, object]) -> str:
    """
    Formats a string using Ren'Py's formatting rules. Ren'Py uses square
    brackets to denote interpolation, but is otherwise similar to native
    f-strings, with a few caveats and additional conversions available.
    """

    rv: list[str] = []
    expr = conv = fmt = None

    for kind, value in parse(s):
        if kind == "conv":
            conv = value
        elif kind == "fmt":
            fmt = value
        elif kind == "expr":
            expr = value
        else:
            # "literal" or "expr": any pending substitution is complete.
            if expr is not None:
                rv.append(_substitute(expr, conv, fmt, scope))
                expr = conv = fmt = None

            if value:
                rv.append(value)

    assert expr is None, "Expression without following literal."
    return "".join(rv)


def _substitute(expr: str, conv: str | None, fmt: str | None, scope: Mapping[str, object]) -> str:
    code = expr.strip()
    prefix = ""

    if code[-1] == "=":
        prefix = expr
        code = code[:-1].rstrip()

        if conv is None and fmt is None:
            conv = "r"

    if renpy.config.interpolate_exprs:
        if code in scope and code.isidentifier():
            value = scope[code]
        else:
            try:
                value = renpy.python.py_eval(code, {}, scope)
            except Exception as e:
                if renpy.config.interpolate_exprs != "fallback":
                    raise

                try:
                    value, _ = formatter.get_field(code, (), scope)
                except Exception:
                    raise e

    else:
        value, _ = formatter.get_field(code, (), scope)

    if conv is not None:
        value = convert(value, conv, scope)

    return prefix + format(value, "" if fmt is None else fmt)


def convert(value: object, conv: str, scope: Mapping[str, object]) -> object:
    """
    Converts the value according to the specified conversion flags.
    """

    if not conv:
        raise ValueError("conversion specifier cannot be empty")

    conv_set = set(conv)

    if conv_set - flags:
        raise ValueError(f"invalid conversion characters: {conv_set - flags}")

    if "r" in conv_set:
        value = repr(value)
        conv_set.discard("r")

    elif "s" in conv_set:
        value = str(value)
        conv_set.discard("s")

    if not conv_set:
        return value

    # All conversion symbols below assume we have a string.
    rv = str(value)

    if "t" in conv_set:
        rv = renpy.translation.translate_string(rv)

    if "i" in conv_set:
        try:
            rv = interpolate(rv, scope)
        except RecursionError:
            raise ValueError(f"Substitution {rv!r} refers to itself in a loop.")

    if "f" in conv_set:
        if renpy.config.say_menu_text_filter is not None:
            rv = renpy.config.say_menu_text_filter(rv)

        for f in renpy.config.say_menu_text_filters:
            rv = f(rv)

    if "q" in conv_set:
        rv = rv.replace("{", "{{")

    if "u" in conv_set:
        rv = rv.upper()

    if "l" in conv_set:
        rv = rv.lower()

    if "c" in conv_set:
        rv = rv[:1].capitalize() + rv[1:]

    return rv


def substitute(
    s: object,
    scope: dict[str, object] | None = None,
    force: bool = False,
    translate: bool = True,
) -> tuple[str, bool]:
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

    rv = str(s)

    if translate:
        rv = renpy.translation.translate_string(rv)

    # Substitute.
    if not renpy.config.new_substitutions and not force:
        return rv, False

    if "[" not in rv:
        return rv, False

    old_s = rv

    dicts = []

    if scope is not None:
        dicts.append(scope)

    if "store.interpolate" in renpy.python.store_dicts:
        dicts.append(renpy.python.store_dicts["store.interpolate"])

    dicts.append(renpy.store.__dict__)

    if len(dicts) == 1:
        variables = dicts[0]
    else:
        variables = collections.ChainMap(*dicts)

    try:
        rv = interpolate(rv, variables)
    except Exception:
        if renpy.display.predict.predicting:
            return " ", True
        raise

    return rv, (rv != old_s)


def ___(s):
    """
    :undocumented: Documented directly in the .rst.

    Translates a string, then performs substitutions on it.
    """

    scope = sys._getframe(1).f_locals

    return substitute(s, scope)[0]
