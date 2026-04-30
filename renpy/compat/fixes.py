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

from __future__ import annotations

from typing import Iterator

import tokenize
import token
import io
import ast


def fix_octal_numbers(tokens: Iterator[tokenize.TokenInfo]):
    """
    This fixes python-2 style octal numbers. Tokenize reports this
    as NUMBER which starts with '0'. This replaces this as a 0oXXX.
    """

    for t in tokens:
        if t.type == token.NUMBER and t.string != "0" and t.string.startswith("0"):
            yield tokenize.TokenInfo(token.NUMBER, f"0o{t.string[1:]}", t.start, t.end, t.line)
        else:
            yield t


def fix_spaceship(tokens: Iterator[tokenize.TokenInfo]):
    """
    This fixes the Python 2 spaceship operator (<>).
    """

    for t in tokens:
        if t.type == token.OP and t.string == "<>":
            yield tokenize.TokenInfo(token.OP, "!=", t.start, t.end, t.line)
        else:
            yield t


def fix_backtick_repr(tokens: Iterator[tokenize.TokenInfo]):
    """
    This fixes the Python 2 backtick-repr and replaces it with call to repr.
    """

    # Is this the first backtick in a pair?
    first = True

    for t in tokens:
        if t.type == token.OP and t.string == "`":
            if first:
                yield tokenize.TokenInfo(token.NAME, "repr", t.start, t.end, t.line)
                yield tokenize.TokenInfo(token.LPAR, "(", t.end, t.end, t.line)
                first = False
            else:
                yield tokenize.TokenInfo(token.RPAR, ")", t.start, t.end, t.line)
                first = True
        else:
            yield t


def fix_print(line: list[tokenize.TokenInfo]):
    """
    This tries to remove Python 2-style print statements.
    """

    if len(line) < 2:
        return line

    if line[0].type != token.NAME:
        return line

    if line[0].string != "print":
        return line

    if line[1].exact_type == token.LPAR:
        return line

    if line[1].exact_type == token.RIGHTSHIFT:
        newline = line[2:]
    else:
        newline = line[1:]

    # Replace the print statement 0, arguments.
    old = line[0]
    newline.insert(0, tokenize.TokenInfo(token.NUMBER, "0", old.start, old.start, old.line))
    newline.insert(1, tokenize.TokenInfo(token.OP, ",", old.end, old.end, old.line))

    return newline


def fix_raise(line: list[tokenize.TokenInfo]):
    if len(line) < 4:
        return line

    if line[0].type != token.NAME:
        return line

    if line[0].string != "raise":
        return line

    if line[1].exact_type != token.NAME:
        return line

    if line[2].exact_type != token.COMMA:
        return line

    newline = list(line)
    newline[2] = tokenize.TokenInfo(token.LPAR, "(", line[2].start, line[2].end, line[2].line)
    newline.insert(-1, tokenize.TokenInfo(token.RPAR, ")", line[-2].end, line[-2].end, line[-2].line))

    return newline


def fix_lines(tokens: Iterator[tokenize.TokenInfo]):
    def fix_line(line):
        line = fix_print(line)
        line = fix_raise(line)
        return line

    line: list[tokenize.TokenInfo] = []

    extra_tokens = (
        token.NL,
        token.INDENT,
        token.DEDENT,
        token.COMMENT,
        token.ENDMARKER,
        token.ENCODING,
    )

    for t in tokens:
        if not line and t.exact_type in extra_tokens:
            yield t
            continue

        line.append(t)

        if t.type != token.NEWLINE:
            continue

        yield from fix_line(line)
        line = []

    yield from fix_line(line)


def fix_tokens(source: str):
    """
    This applies fixes that will help python 2 code run under python 3. Not all
    problem will be fixed, but this will attempt to handle common issues.

    These are fixes that apply at the source code level.
    """

    try:
        bio = io.StringIO(source, None)
        tokens = tokenize.generate_tokens(bio.readline)

        tokens = fix_octal_numbers(tokens)
        tokens = fix_spaceship(tokens)
        tokens = fix_backtick_repr(tokens)

        tokens = fix_lines(tokens)

        rv: str = tokenize.untokenize(tokens)

        return rv

    except Exception as e:
        # import traceback
        # traceback.print_exc()
        raise e


class ReorderGlobals(ast.NodeTransformer):
    """
    This removes all global statements from functions, and places the variables
    therein in a new global statement on the first line of the function.
    """

    def __init__(self):
        self.globals = set()

    def visit_Global(self, node):
        for i in node.names:
            self.globals.add(i)

        return ast.Pass()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        old_globals = self.globals

        try:
            node = self.generic_visit(node)  # type: ignore

            new_globals = list(self.globals)
            new_globals.sort()

            if new_globals:
                node.body.insert(0, ast.Global(names=new_globals))

            return node
        finally:
            self.globals = old_globals


reorder_globals = ReorderGlobals()


def fix_ast(tree):
    """
    This applies fixes that will help python 2 code run under python 3. Not all
    problems will be fixed, but this will attempt to handle common issues.

    These are fixes that apply at the AST level.
    """

    try:
        tree = reorder_globals.visit(tree)
        return tree

    except Exception as e:
        # import traceback
        # traceback.print_exc()
        raise e
