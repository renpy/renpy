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

import unittest

from renpy.tokenizer import Tokenizer, TokenKind

NEWLINE = TokenKind.NEWLINE
COMMENT = TokenKind.COMMENT
WORD = TokenKind.WORD
OP = TokenKind.OP
STRING_START = TokenKind.STRING_START
STRING_MIDDLE = TokenKind.STRING_MIDDLE
STRING_END = TokenKind.STRING_END
ENDMARKER = TokenKind.ENDMARKER
ERRORTOKEN = TokenKind.ERRORTOKEN


def tokenize_all(data, **kwargs):
    """Tokenize `data` and return a list of TokenInfo."""
    return list(Tokenizer(data, **kwargs).iter_tokens())


def tokenize(data, **kwargs):
    """Tokenize `data` and return a list of (kind, string) pairs."""
    return [(t.kind, t.string) for t in tokenize_all(data, **kwargs)]


def errors(data, **kwargs):
    """Tokenize `data` and return the list of ERRORTOKEN messages."""
    return [t.string for t in tokenize_all(data, **kwargs) if t.kind is ERRORTOKEN]


class TokenizerTestCase(unittest.TestCase):
    def assertTokens(self, data, expected, **kwargs):
        """Assert `data` tokenizes to `expected` (kind, string) pairs,
        followed by an empty ENDMARKER."""
        self.assertEqual(
            tokenize(data, **kwargs),
            list(expected) + [(ENDMARKER, "")],
        )


class TestTokenKind(TokenizerTestCase):
    def test_values(self):
        self.assertEqual(TokenKind.NEWLINE, 1)
        self.assertEqual(TokenKind.COMMENT, 2)
        self.assertEqual(TokenKind.WORD, 3)
        self.assertEqual(TokenKind.OP, 4)
        self.assertEqual(TokenKind.STRING_START, 5)
        self.assertEqual(TokenKind.STRING_MIDDLE, 6)
        self.assertEqual(TokenKind.STRING_END, 7)
        self.assertEqual(TokenKind.ENDMARKER, 8)
        self.assertEqual(TokenKind.ERRORTOKEN, 9)

    def test_all_kinds_distinct(self):
        self.assertEqual(len(set(TokenKind)), 9)


class TestTokenInfo(TokenizerTestCase):
    def test_fields(self):
        token = Tokenizer("a").next_token()
        self.assertEqual(token.kind, WORD)
        self.assertEqual(token.string, "a")
        self.assertEqual(token.span, (0, 1))
        self.assertEqual(token.start, (1, 1))
        self.assertEqual(token.end, (1, 2))

    def test_token_is_immutable(self):
        token = Tokenizer("a").next_token()
        with self.assertRaises(AttributeError):
            token.string = "b"

    def test_span_matches_string(self):
        # Except for ERRORTOKEN, whose string is the error message.
        data = "one  two\nthree"
        for token in tokenize_all(data):
            self.assertEqual(data[token.span[0] : token.span[1]], token.string)


class TestBasicTokens(TokenizerTestCase):
    def test_empty_source(self):
        token = Tokenizer("").next_token()
        self.assertEqual(token.kind, ENDMARKER)
        self.assertEqual(token.string, "")
        self.assertEqual(token.span, (0, 0))
        self.assertEqual(token.start, (1, 1))
        self.assertEqual(token.end, (1, 1))

    def test_endmarker_is_sticky(self):
        tk = Tokenizer("a")
        tk.next_token()
        for _ in range(3):
            self.assertEqual(tk.next_token().kind, ENDMARKER)

    def test_words(self):
        for data in ("hello", "_private", "abc123", "a1_b2"):
            with self.subTest(data=data):
                self.assertTokens(data, [(WORD, data)])

    def test_numbers(self):
        for data in ("123", "0xFF", "1_000", "1e5", "0b101"):
            with self.subTest(data=data):
                self.assertTokens(data, [(WORD, data)])

    def test_dotted_number(self):
        # WORD is less strict than Python's NUMBER.
        self.assertTokens("1.5", [(WORD, "1"), (OP, "."), (WORD, "5")])

    def test_unicode_word(self):
        self.assertTokens("café_变量", [(WORD, "café_变量")])

    def test_whitespace_is_skipped(self):
        # Whitespace runs are not emitted as tokens, but the following
        # token still has correct positions.
        token = Tokenizer("   a").next_token()
        self.assertEqual((token.kind, token.string), (WORD, "a"))
        self.assertEqual(token.span, (3, 4))
        self.assertEqual(token.start, (1, 4))
        self.assertEqual(token.end, (1, 5))

    def test_whitespace_between_tokens(self):
        self.assertTokens("a  b", [(WORD, "a"), (WORD, "b")])

    def test_whitespace_line_continuation(self):
        # Backslash-newline is skipped with the whitespace, but still
        # advances the line number.
        tk = Tokenizer("a  \\\n  b")

        token = tk.next_token()
        self.assertEqual((token.kind, token.string), (WORD, "a"))
        self.assertEqual((token.start, token.end), ((1, 1), (1, 2)))

        token = tk.next_token()
        self.assertEqual((token.kind, token.string), (WORD, "b"))
        self.assertEqual(token.span, (7, 8))
        self.assertEqual((token.start, token.end), ((2, 3), (2, 4)))
        self.assertEqual(tk.lineno, 2)

    def test_comment(self):
        self.assertTokens(
            "# a comment\nb",
            [(COMMENT, "# a comment"), (NEWLINE, "\n"), (WORD, "b")],
        )

    def test_comment_at_eof(self):
        self.assertTokens("# a comment", [(COMMENT, "# a comment")])

    def test_comment_excludes_newline(self):
        token = Tokenizer("# c\n").next_token()
        self.assertEqual((token.kind, token.string), (COMMENT, "# c"))
        self.assertEqual(token.span, (0, 3))

    def test_newline_positions(self):
        tk = Tokenizer("a\nbb\n")

        token = tk.next_token()
        self.assertEqual((token.start, token.end), ((1, 1), (1, 2)))

        token = tk.next_token()
        self.assertEqual((token.kind, token.string), (NEWLINE, "\n"))
        self.assertEqual((token.start, token.end), ((1, 2), (1, 3)))
        self.assertEqual(tk.lineno, 2)

        token = tk.next_token()
        self.assertEqual((token.kind, token.string), (WORD, "bb"))
        self.assertEqual((token.start, token.end), ((2, 1), (2, 3)))

        token = tk.next_token()
        self.assertEqual((token.kind, token.string), (NEWLINE, "\n"))
        self.assertEqual((token.start, token.end), ((2, 3), (2, 4)))

        token = tk.next_token()
        self.assertEqual((token.kind, token.start), (ENDMARKER, (3, 1)))

    def test_one_char_operators(self):
        for op in "+-*/%@&|^,:!.;=~<>$?":
            with self.subTest(op=op):
                self.assertTokens(op, [(OP, op)])

    def test_two_char_operators(self):
        for op in (
            "//",
            ">>",
            "<<",
            "<>",
            "**",
            "->",
            "+=",
            "-=",
            "*=",
            "/=",
            "%=",
            "@=",
            "&=",
            "|=",
            "^=",
            ":=",
            "<=",
            ">=",
            "==",
            "!=",
        ):
            with self.subTest(op=op):
                self.assertTokens(op, [(OP, op)])

    def test_three_char_operators(self):
        for op in ("...", "//=", ">>=", "<<=", "**="):
            with self.subTest(op=op):
                self.assertTokens(op, [(OP, op)])

    def test_dollar_and_question_are_operators(self):
        self.assertTokens("$x?", [(OP, "$"), (WORD, "x"), (OP, "?")])

    def test_operator_sequences(self):
        self.assertTokens("..", [(OP, "."), (OP, ".")])
        self.assertTokens("===", [(OP, "=="), (OP, "=")])
        self.assertTokens("a+=1", [(WORD, "a"), (OP, "+="), (WORD, "1")])
        self.assertTokens("a->b", [(WORD, "a"), (OP, "->"), (WORD, "b")])


class TestStrings(TokenizerTestCase):
    def test_simple_strings(self):
        for quote in ('"', "'", "`"):
            with self.subTest(quote=quote):
                data = quote + "abc" + quote
                self.assertTokens(
                    data,
                    [(STRING_START, quote), (STRING_MIDDLE, "abc"), (STRING_END, quote)],
                )

    def test_empty_string(self):
        self.assertTokens(
            '""',
            [(STRING_START, '"'), (STRING_END, '"')],
        )

    def test_prefixes(self):
        for prefix in (
            "r",
            "u",
            "b",
            "f",
            "R",
            "U",
            "B",
            "F",
            "rb",
            "br",
            "rf",
            "fr",
            "Rb",
            "rF",
            "FR",
        ):
            with self.subTest(prefix=prefix):
                self.assertTokens(
                    prefix + '"x"',
                    [
                        (STRING_START, prefix + '"'),
                        (STRING_MIDDLE, "x"),
                        (STRING_END, '"'),
                    ],
                )

    def test_prefix_like_words(self):
        for data in ("fx", "frank", "r", "ur"):
            with self.subTest(data=data):
                self.assertTokens(data, [(WORD, data)])

    def test_triple_quoted_string(self):
        self.assertTokens(
            '"""abc"""',
            [
                (STRING_START, '"""'),
                (STRING_MIDDLE, "abc"),
                (STRING_END, '"""'),
            ],
        )

    def test_empty_triple_quoted_string(self):
        self.assertTokens(
            '""""""',
            [(STRING_START, '"""'), (STRING_END, '"""')],
        )

    def test_quotes_inside_triple_quoted_string(self):
        self.assertTokens(
            '"""a""b\'c"""',
            [
                (STRING_START, '"""'),
                (STRING_MIDDLE, 'a""b\'c'),
                (STRING_END, '"""'),
            ],
        )

    def test_triple_quoted_string_positions(self):
        tk = Tokenizer('"""a\nb"""\nc')

        token = tk.next_token()
        self.assertEqual((token.start, token.end), ((1, 1), (1, 4)))

        token = tk.next_token()
        self.assertEqual((token.kind, token.string), (STRING_MIDDLE, "a\nb"))
        self.assertEqual((token.start, token.end), ((1, 4), (2, 2)))

        token = tk.next_token()
        self.assertEqual((token.kind, token.string), (STRING_END, '"""'))
        self.assertEqual((token.start, token.end), ((2, 2), (2, 5)))

        token = tk.next_token()
        self.assertEqual((token.kind, token.string), (NEWLINE, "\n"))
        self.assertEqual((token.start, token.end), ((2, 5), (2, 6)))

    def test_escaped_quote(self):
        self.assertTokens(
            '"a\\"b"',
            [
                (STRING_START, '"'),
                (STRING_MIDDLE, 'a\\"b'),
                (STRING_END, '"'),
            ],
        )

    def test_escaped_backslash_before_end(self):
        self.assertTokens(
            '"a\\\\"',
            [
                (STRING_START, '"'),
                (STRING_MIDDLE, "a\\\\"),
                (STRING_END, '"'),
            ],
        )

    def test_escaped_tab_in_string(self):
        # The escaped character is part of the string, whatever it is.
        self.assertTokens(
            '"a\\\tb"',
            [(STRING_START, '"'), (STRING_MIDDLE, "a\\\tb"), (STRING_END, '"')],
        )

    def test_adjacent_strings(self):
        self.assertTokens(
            '"a" "b"',
            [
                (STRING_START, '"'),
                (STRING_MIDDLE, "a"),
                (STRING_END, '"'),
                (STRING_START, '"'),
                (STRING_MIDDLE, "b"),
                (STRING_END, '"'),
            ],
        )

    def test_comment_like_text_in_string(self):
        self.assertTokens(
            '"a # b"',
            [(STRING_START, '"'), (STRING_MIDDLE, "a # b"), (STRING_END, '"')],
        )

    def test_braces_in_plain_string(self):
        self.assertTokens(
            '"{x}"',
            [(STRING_START, '"'), (STRING_MIDDLE, "{x}"), (STRING_END, '"')],
        )

    def test_unterminated_string(self):
        # The ERRORTOKEN covers the opening quote of the string.
        self.assertTokens(
            '"abc',
            [
                (STRING_START, '"'),
                (STRING_MIDDLE, "abc"),
                (ERRORTOKEN, "unterminated string literal"),
            ],
        )

        token = tokenize_all('"abc')[2]
        self.assertEqual(token.span, (0, 1))
        self.assertEqual(token.start, (1, 1))

    def test_unterminated_triple_quoted_string(self):
        self.assertTokens(
            '"""ab',
            [
                (STRING_START, '"""'),
                (STRING_MIDDLE, "ab"),
                (ERRORTOKEN, "unterminated string literal"),
            ],
        )

    def test_unterminated_string_ending_in_backslash(self):
        self.assertTokens(
            '"a\\',
            [
                (STRING_START, '"'),
                (STRING_MIDDLE, "a\\"),
                (ERRORTOKEN, "unterminated string literal"),
            ],
        )

    def test_tab_in_string(self):
        # The literal text stops before the tab, which is reported and
        # skipped; tokenization of the string then continues.
        self.assertTokens(
            '"ab\tx"',
            [
                (STRING_START, '"'),
                (STRING_MIDDLE, "ab"),
                (ERRORTOKEN, "Tab character is not allowed in Ren'Py scripts"),
                (STRING_MIDDLE, "x"),
                (STRING_END, '"'),
            ],
        )

        token = tokenize_all('"ab\tx"')[2]
        self.assertEqual(token.span, (3, 4))
        self.assertEqual((token.start, token.end), ((1, 4), (1, 5)))

    def test_control_character_in_string(self):
        self.assertEqual(
            errors('"a\x02b"'),
            ["ASCII control character '\\x02' is not allowed in Ren'Py scripts"],
        )


class TestFStrings(TokenizerTestCase):
    def test_replacement_field(self):
        self.assertTokens(
            'f"{x}"',
            [
                (STRING_START, 'f"'),
                (OP, "{"),
                (WORD, "x"),
                (OP, "}"),
                (STRING_END, '"'),
            ],
        )

    def test_replacement_field_positions(self):
        tokens = tokenize_all('f"{x}"')

        self.assertEqual((tokens[0].start, tokens[0].end), ((1, 1), (1, 3)))
        self.assertEqual((tokens[1].start, tokens[1].end), ((1, 3), (1, 4)))
        self.assertEqual((tokens[2].start, tokens[2].end), ((1, 4), (1, 5)))

    def test_literal_braces(self):
        self.assertTokens(
            'f"{{{x}}}"',
            [
                (STRING_START, 'f"'),
                (STRING_MIDDLE, "{{"),
                (OP, "{"),
                (WORD, "x"),
                (OP, "}"),
                (STRING_MIDDLE, "}}"),
                (STRING_END, '"'),
            ],
        )

    def test_field_with_expression(self):
        self.assertTokens(
            'f"{a + b}"',
            [
                (STRING_START, 'f"'),
                (OP, "{"),
                (WORD, "a"),
                (OP, "+"),
                (WORD, "b"),
                (OP, "}"),
                (STRING_END, '"'),
            ],
        )

    def test_conversion(self):
        self.assertTokens(
            'f"{x!r}"',
            [
                (STRING_START, 'f"'),
                (OP, "{"),
                (WORD, "x"),
                (OP, "!"),
                (WORD, "r"),
                (OP, "}"),
                (STRING_END, '"'),
            ],
        )

    def test_format_spec(self):
        self.assertTokens(
            'f"{x:>5}"',
            [
                (STRING_START, 'f"'),
                (OP, "{"),
                (WORD, "x"),
                (OP, ":"),
                (STRING_MIDDLE, ">5"),
                (OP, "}"),
                (STRING_END, '"'),
            ],
        )

    def test_empty_format_spec(self):
        self.assertTokens(
            'f"{x:}"',
            [
                (STRING_START, 'f"'),
                (OP, "{"),
                (WORD, "x"),
                (OP, ":"),
                (OP, "}"),
                (STRING_END, '"'),
            ],
        )

    def test_format_spec_starting_with_equals(self):
        # ':=' must be split into a spec ':' and the '=5' spec text.
        self.assertTokens(
            'f"{x:=5}"',
            [
                (STRING_START, 'f"'),
                (OP, "{"),
                (WORD, "x"),
                (OP, ":"),
                (STRING_MIDDLE, "=5"),
                (OP, "}"),
                (STRING_END, '"'),
            ],
        )

    def test_debug_equals(self):
        self.assertTokens(
            'f"{x=}"',
            [
                (STRING_START, 'f"'),
                (OP, "{"),
                (WORD, "x"),
                (OP, "="),
                (OP, "}"),
                (STRING_END, '"'),
            ],
        )

    def test_nested_string_in_field(self):
        self.assertTokens(
            "f\"{'a'}\"",
            [
                (STRING_START, 'f"'),
                (OP, "{"),
                (STRING_START, "'"),
                (STRING_MIDDLE, "a"),
                (STRING_END, "'"),
                (OP, "}"),
                (STRING_END, '"'),
            ],
        )

    def test_nested_field_in_format_spec(self):
        self.assertTokens(
            'f"{x:{w}}"',
            [
                (STRING_START, 'f"'),
                (OP, "{"),
                (WORD, "x"),
                (OP, ":"),
                (OP, "{"),
                (WORD, "w"),
                (OP, "}"),
                (OP, "}"),
                (STRING_END, '"'),
            ],
        )

    def test_format_spec_continues_after_nested_field(self):
        # Python allows f"{x:{w}d}"; after the nested field closes, the
        # remaining text is still part of the format spec.
        self.assertTokens(
            'f"{x:{w}d}"',
            [
                (STRING_START, 'f"'),
                (OP, "{"),
                (WORD, "x"),
                (OP, ":"),
                (OP, "{"),
                (WORD, "w"),
                (OP, "}"),
                (STRING_MIDDLE, "d"),
                (OP, "}"),
                (STRING_END, '"'),
            ],
        )

    def test_multiline_field(self):
        self.assertTokens(
            'f"{\nx\n}"',
            [
                (STRING_START, 'f"'),
                (OP, "{"),
                (NEWLINE, "\n"),
                (WORD, "x"),
                (NEWLINE, "\n"),
                (OP, "}"),
                (STRING_END, '"'),
            ],
        )

    def test_comment_in_field(self):
        self.assertTokens(
            'f"{x # c\n}"',
            [
                (STRING_START, 'f"'),
                (OP, "{"),
                (WORD, "x"),
                (COMMENT, "# c"),
                (NEWLINE, "\n"),
                (OP, "}"),
                (STRING_END, '"'),
            ],
        )

    def test_brackets_in_field(self):
        self.assertTokens(
            'f"{d[1:2]}"',
            [
                (STRING_START, 'f"'),
                (OP, "{"),
                (WORD, "d"),
                (OP, "["),
                (WORD, "1"),
                (OP, ":"),
                (WORD, "2"),
                (OP, "]"),
                (OP, "}"),
                (STRING_END, '"'),
            ],
        )

    def test_unterminated_field(self):
        # Unclosed constructs are reported innermost first, then the
        # ENDMARKER is produced.
        self.assertTokens(
            'f"{x',
            [
                (STRING_START, 'f"'),
                (OP, "{"),
                (WORD, "x"),
                (ERRORTOKEN, "'{' was never closed"),
                (ERRORTOKEN, "unterminated string literal"),
            ],
        )

    def test_unterminated_fstring(self):
        self.assertTokens(
            'f"{x}',
            [
                (STRING_START, 'f"'),
                (OP, "{"),
                (WORD, "x"),
                (OP, "}"),
                (ERRORTOKEN, "unterminated string literal"),
            ],
        )

    def test_string_end_in_format_spec(self):
        # The error has an empty span at the quote, and the tokenizer
        # recovers by closing the field and matching the quote.
        tokens = tokenize_all('f"{x:>5"')
        self.assertEqual(
            [(t.kind, t.string) for t in tokens],
            [
                (STRING_START, 'f"'),
                (OP, "{"),
                (WORD, "x"),
                (OP, ":"),
                (STRING_MIDDLE, ">5"),
                (ERRORTOKEN, "f-string: expecting '}'"),
                (STRING_END, '"'),
                (ENDMARKER, ""),
            ],
        )
        self.assertEqual(tokens[5].span, (7, 7))
        self.assertEqual(tokens[5].start, (1, 8))

    def test_unclosed_nested_field_in_format_spec(self):
        self.assertTokens(
            'f"{x:{y',
            [
                (STRING_START, 'f"'),
                (OP, "{"),
                (WORD, "x"),
                (OP, ":"),
                (OP, "{"),
                (WORD, "y"),
                (ERRORTOKEN, "'{' was never closed"),
                (ERRORTOKEN, "'{' was never closed"),
                (ERRORTOKEN, "unterminated string literal"),
            ],
        )

    def test_unterminated_nested_string_in_field(self):
        # PEP 701: a quote inside a replacement field opens a nested string.
        self.assertTokens(
            'f"{x:{y"',
            [
                (STRING_START, 'f"'),
                (OP, "{"),
                (WORD, "x"),
                (OP, ":"),
                (OP, "{"),
                (WORD, "y"),
                (STRING_START, '"'),
                (ERRORTOKEN, "unterminated string literal"),
                (ERRORTOKEN, "'{' was never closed"),
                (ERRORTOKEN, "'{' was never closed"),
                (ERRORTOKEN, "unterminated string literal"),
            ],
        )

    def test_non_fstring_does_not_split(self):
        for prefix in ("", "r", "b", "u"):
            with self.subTest(prefix=prefix):
                self.assertTokens(
                    prefix + '"{x}"',
                    [
                        (STRING_START, prefix + '"'),
                        (STRING_MIDDLE, "{x}"),
                        (STRING_END, '"'),
                    ],
                )


class TestBrackets(TokenizerTestCase):
    def test_max_depth(self):
        # Exceeding MAX_DEPTH (300) emits one ERRORTOKEN for the offending
        # bracket, then sticks to ENDMARKER.
        tk = Tokenizer("(" * 302)
        tokens = list(tk.iter_tokens())

        self.assertEqual(len(tokens), 302)
        self.assertTrue(all(t.kind is OP for t in tokens[:300]))

        error = tokens[300]
        self.assertEqual(error.kind, ERRORTOKEN)
        self.assertEqual(error.string, "more than 300 nested brackets and strings")
        self.assertEqual(error.span, (300, 301))

        self.assertEqual(tokens[301].kind, ENDMARKER)
        self.assertEqual(tk.next_token().kind, ENDMARKER)

    def test_nested_brackets(self):
        self.assertTokens(
            "a([{b}])",
            [
                (WORD, "a"),
                (OP, "("),
                (OP, "["),
                (OP, "{"),
                (WORD, "b"),
                (OP, "}"),
                (OP, "]"),
                (OP, ")"),
            ],
        )

    def test_brackets_across_lines(self):
        self.assertTokens(
            "(\n1,\n2\n)",
            [
                (OP, "("),
                (NEWLINE, "\n"),
                (WORD, "1"),
                (OP, ","),
                (NEWLINE, "\n"),
                (WORD, "2"),
                (NEWLINE, "\n"),
                (OP, ")"),
            ],
        )

    def test_top_level_braces(self):
        self.assertTokens(
            "{x}",
            [(OP, "{"), (WORD, "x"), (OP, "}")],
        )

    def test_depth_tracking(self):
        tk = Tokenizer("([a])")
        self.assertEqual(tk.depth, 0)

        tk.next_token()
        self.assertEqual(tk.depth, 1)

        tk.next_token()
        self.assertEqual(tk.depth, 2)

        tk.next_token()
        self.assertEqual(tk.depth, 2)

        tk.next_token()
        self.assertEqual(tk.depth, 1)

        tk.next_token()
        self.assertEqual(tk.depth, 0)

    def test_depth_in_fstring(self):
        tk = Tokenizer('f"{x}"')
        tk.next_token()  # f"
        self.assertEqual(tk.depth, 1)
        tk.next_token()  # {
        self.assertEqual(tk.depth, 2)
        tk.next_token()  # x
        tk.next_token()  # }
        self.assertEqual(tk.depth, 1)
        tk.next_token()  # "
        self.assertEqual(tk.depth, 0)

    def test_mismatched_brackets(self):
        # The tokenizer recovers by discarding the mismatched opener, so
        # the rest of the input still tokenizes.
        tokens = tokenize_all("([)]")
        self.assertEqual(
            [(t.kind, t.string) for t in tokens],
            [
                (OP, "("),
                (OP, "["),
                (ERRORTOKEN, "closing parenthesis ')' does not match opening parenthesis '['"),
                (OP, "]"),
                (ENDMARKER, ""),
            ],
        )
        self.assertEqual(tokens[2].span, (2, 3))
        self.assertEqual(tokens[2].start, (1, 3))

    def test_unmatched_close(self):
        self.assertTokens(
            "a)",
            [(WORD, "a"), (ERRORTOKEN, "unmatched ')'")],
        )

    def test_unmatched_close_does_not_change_depth(self):
        tk = Tokenizer(")")
        token = tk.next_token()
        self.assertEqual(token.kind, ERRORTOKEN)
        self.assertEqual(tk.depth, 0)

    def test_unclosed_bracket(self):
        self.assertTokens(
            "(a",
            [(OP, "("), (WORD, "a"), (ERRORTOKEN, "'(' was never closed")],
        )

        token = tokenize_all("(a")[2]
        self.assertEqual(token.span, (0, 1))
        self.assertEqual(token.start, (1, 1))

    def test_unclosed_brackets_innermost_first(self):
        self.assertTokens(
            "([",
            [
                (OP, "("),
                (OP, "["),
                (ERRORTOKEN, "'[' was never closed"),
                (ERRORTOKEN, "'(' was never closed"),
            ],
        )


class TestErrors(TokenizerTestCase):
    def test_tab_character(self):
        # The tab is reported and skipped, and tokenization continues.
        self.assertTokens(
            "a\tb",
            [
                (WORD, "a"),
                (ERRORTOKEN, "Tab character is not allowed in Ren'Py scripts"),
                (WORD, "b"),
            ],
        )

        token = tokenize_all("a\tb")[1]
        self.assertEqual(token.span, (1, 2))
        self.assertEqual((token.start, token.end), ((1, 2), (1, 3)))

    def test_control_characters(self):
        for c in ("\x01", "\x0b", "\x0c", "\x7f"):
            with self.subTest(c=c):
                (message,) = errors("a" + c + "b")
                self.assertIn("control character", message)

    def test_stray_backslash(self):
        self.assertTokens(
            "\\x",
            [
                (ERRORTOKEN, "unexpected character after line continuation character"),
                (WORD, "x"),
            ],
        )

    def test_backslash_at_eof(self):
        self.assertTokens(
            "a\\",
            [
                (WORD, "a"),
                (ERRORTOKEN, "unexpected character after line continuation character"),
            ],
        )

    def test_error_lineno(self):
        token = tokenize_all("a\nb\tc")[3]
        self.assertEqual(token.kind, ERRORTOKEN)
        self.assertEqual(token.start, (2, 2))

    def test_no_error_on_valid_input(self):
        self.assertEqual(errors('f"{x:{w}d}" # c\n(a)\n'), [])


class TestConstructor(TokenizerTestCase):
    def test_defaults(self):
        tk = Tokenizer("ab")
        self.assertEqual(tk.data, "ab")
        self.assertEqual(tk.filename, "<lexer>")
        self.assertEqual(tk.pos, 0)
        self.assertEqual(tk.lineno, 1)
        self.assertEqual(tk.line_start, 0)
        self.assertEqual(tk.split_char, "{")
        self.assertEqual(tk.depth, 0)

    def test_custom_filename(self):
        tk = Tokenizer("ab", filename="script.rpy")
        self.assertEqual(tk.filename, "script.rpy")

    def test_pos(self):
        tk = Tokenizer("hello world", pos=6)
        token = tk.next_token()
        self.assertEqual((token.kind, token.string), (WORD, "world"))
        self.assertEqual(token.span, (6, 11))

    def test_pos_at_end(self):
        tk = Tokenizer("ab", pos=2)
        self.assertEqual(tk.next_token().kind, ENDMARKER)

    def test_lineno(self):
        tk = Tokenizer("hello world", pos=6, lineno=5)
        token = tk.next_token()
        self.assertEqual(token.start[0], 5)
        self.assertEqual(tk.lineno, 5)

        tk = Tokenizer("a\nb", lineno=10)
        tk.next_token()
        tk.next_token()
        token = tk.next_token()
        self.assertEqual((token.kind, token.start), (WORD, (11, 1)))

    def test_pos_out_of_range(self):
        for pos in (-1, 3):
            with self.subTest(pos=pos), self.assertRaises(ValueError):
                Tokenizer("ab", pos=pos)

    def test_invalid_split_char(self):
        for split_char in ("(", "", "xx"):
            with self.subTest(split_char=split_char), self.assertRaises(ValueError):
                Tokenizer("ab", split_char=split_char)  # type: ignore

    def test_properties_are_readonly(self):
        tk = Tokenizer("ab")
        for prop in ("data", "filename", "pos", "lineno", "line_start", "split_char"):
            with self.subTest(prop=prop), self.assertRaises(AttributeError):
                setattr(tk, prop, None)


class TestSplitChar(TokenizerTestCase):
    def test_split_char_bracket(self):
        tk = Tokenizer("ab", split_char="[")
        self.assertEqual(tk.split_char, "[")

    def test_substitution(self):
        # Any string allows [...] substitutions, without an f prefix.
        self.assertTokens(
            '"Hello [name]!"',
            [
                (STRING_START, '"'),
                (STRING_MIDDLE, "Hello "),
                (OP, "["),
                (WORD, "name"),
                (OP, "]"),
                (STRING_MIDDLE, "!"),
                (STRING_END, '"'),
            ],
            split_char="[",
        )

    def test_escaped_bracket(self):
        self.assertTokens(
            '"a[[b"',
            [(STRING_START, '"'), (STRING_MIDDLE, "a[[b"), (STRING_END, '"')],
            split_char="[",
        )

    def test_lone_close_bracket_is_text(self):
        self.assertTokens(
            '"a]b"',
            [(STRING_START, '"'), (STRING_MIDDLE, "a]b"), (STRING_END, '"')],
            split_char="[",
        )

    def test_braces_are_text(self):
        # Text tags are not replacement fields in "[" mode.
        self.assertTokens(
            '"{b}bold{/b}"',
            [(STRING_START, '"'), (STRING_MIDDLE, "{b}bold{/b}"), (STRING_END, '"')],
            split_char="[",
        )

    def test_nested_brackets(self):
        self.assertTokens(
            '"[a[0]]"',
            [
                (STRING_START, '"'),
                (OP, "["),
                (WORD, "a"),
                (OP, "["),
                (WORD, "0"),
                (OP, "]"),
                (OP, "]"),
                (STRING_END, '"'),
            ],
            split_char="[",
        )

    def test_format_spec(self):
        self.assertTokens(
            '"[x:.2f]"',
            [
                (STRING_START, '"'),
                (OP, "["),
                (WORD, "x"),
                (OP, ":"),
                (STRING_MIDDLE, ".2f"),
                (OP, "]"),
                (STRING_END, '"'),
            ],
            split_char="[",
        )

    def test_nested_field_in_format_spec(self):
        self.assertTokens(
            '"[x:[y]]"',
            [
                (STRING_START, '"'),
                (OP, "["),
                (WORD, "x"),
                (OP, ":"),
                (OP, "["),
                (WORD, "y"),
                (OP, "]"),
                (OP, "]"),
                (STRING_END, '"'),
            ],
            split_char="[",
        )

    def test_conversion(self):
        self.assertTokens(
            '"[x!r]"',
            [
                (STRING_START, '"'),
                (OP, "["),
                (WORD, "x"),
                (OP, "!"),
                (WORD, "r"),
                (OP, "]"),
                (STRING_END, '"'),
            ],
            split_char="[",
        )

    def test_dict_braces_in_field(self):
        self.assertTokens(
            '"[{1: 2}[0]]"',
            [
                (STRING_START, '"'),
                (OP, "["),
                (OP, "{"),
                (WORD, "1"),
                (OP, ":"),
                (WORD, "2"),
                (OP, "}"),
                (OP, "["),
                (WORD, "0"),
                (OP, "]"),
                (OP, "]"),
                (STRING_END, '"'),
            ],
            split_char="[",
        )

    def test_unterminated_field(self):
        self.assertTokens(
            '"[x',
            [
                (STRING_START, '"'),
                (OP, "["),
                (WORD, "x"),
                (ERRORTOKEN, "'[' was never closed"),
                (ERRORTOKEN, "unterminated string literal"),
            ],
            split_char="[",
        )

    def test_string_end_in_format_spec(self):
        self.assertTokens(
            '"[x:>5"',
            [
                (STRING_START, '"'),
                (OP, "["),
                (WORD, "x"),
                (OP, ":"),
                (STRING_MIDDLE, ">5"),
                (ERRORTOKEN, "expecting ']'"),
                (STRING_END, '"'),
            ],
            split_char="[",
        )

    def test_brackets_still_brackets_in_code(self):
        self.assertTokens(
            "a[0]",
            [(WORD, "a"), (OP, "["), (WORD, "0"), (OP, "]")],
            split_char="[",
        )


class TestIterTokens(TokenizerTestCase):
    def test_iterates_through_endmarker(self):
        tokens = list(Tokenizer("a b").iter_tokens())
        self.assertEqual(
            [(t.kind, t.string) for t in tokens],
            [
                (WORD, "a"),
                (WORD, "b"),
                (ENDMARKER, ""),
            ],
        )

    def test_stops_after_endmarker(self):
        # A second ENDMARKER must not be produced.
        tokens = list(Tokenizer("").iter_tokens())
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].kind, ENDMARKER)

    def test_yields_error_tokens(self):
        # Errors are reported as tokens rather than raised, so iteration
        # drains the whole input.
        tokens = list(Tokenizer('"a\tb"').iter_tokens())
        self.assertEqual(tokens[-1].kind, ENDMARKER)
        self.assertIn(ERRORTOKEN, [t.kind for t in tokens])

    def test_matches_next_token_loop(self):
        data = 'f"{x:>{w}}" # c\n(a)\n'

        tk = Tokenizer(data)
        result = []
        while True:
            token = tk.next_token()
            result.append(token)
            if token.kind is ENDMARKER:
                break

        self.assertEqual(list(Tokenizer(data).iter_tokens()), result)


if __name__ == "__main__":
    unittest.main()
