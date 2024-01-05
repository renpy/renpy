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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *


import tokenize
import token
import io
import ast


def fix_octal_numbers(tokens):
    """
    This fixes python-2 style octal numbers. Tokenize seems to report this
    as two numbers, the first of which has a string of '0'. This merges that
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

def fix_spaceship(tokens):
    """
    This fixes the Python 2 spaceship operator (<>).
    """

    old = tokens[0]
    rv = [ ]

    for new in tokens:

        if old.exact_type == token.LESS and new.exact_type == token.GREATER:
            rv.pop()
            new = tokenize.TokenInfo(token.OP, "!=", old.start, new.end, old.line)

        rv.append(new)
        old = new

    return rv


def fix_backtick_repr(tokens):
    """
    This fixes the Python 2 backtick-repr.
    """

    rv = [ ]

    # Is this the first backtick in a pair?
    first = True

    for t in tokens:

        if t.type == token.ERRORTOKEN and t.string == "`":
            if first:
                rv.append(tokenize.TokenInfo(token.NAME, "repr", t.start, t.end, t.line))
                rv.append(tokenize.TokenInfo(token.LPAR, "(", t.end, t.end, t.line))
                first = False
            else:
                rv.append(tokenize.TokenInfo(token.RPAR, ")", t.start, t.end, t.line))
                first = True
        else:
            rv.append(t)

    return rv



def fix_print(line):
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


def fix_raise(line):
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


def fix_lines(tokens):

    def fix_line(line):
        line = fix_print(line)
        line = fix_raise(line)
        return line

    rv = [ ]
    line = [ ]

    for i in tokens:

        if not line:
            if i.exact_type == token.NL:
                rv.append(i)
                continue

            if i.exact_type == token.INDENT:
                rv.append(i)
                continue

            if i.exact_type == token.DEDENT:
                rv.append(i)
                continue

            if i.exact_type == token.ENDMARKER:
                rv.append(i)
                continue

            if i.exact_type == token.ENCODING:
                rv.append(i)
                continue

        line.append(i)

        if i.type != token.NEWLINE:
            continue

        rv.extend(fix_line(line))
        line = [ ]

    rv.extend(fix_line(line))

    return rv


def fix_tokens(source):
    """
    This applies fixes that will help python 2 code run under python 3. Not all
    problem will be fixed, but this will attempt to handle common issues.

    These are fixes that apply at the source code level.
    """

    try:

        if PY2:
            return source

        bio = io.BytesIO(source.encode("utf-8"))
        tokens = list(tokenize.tokenize(bio.readline))

        tokens = fix_octal_numbers(tokens)
        tokens = fix_spaceship(tokens)
        tokens = fix_backtick_repr(tokens)

        tokens = fix_lines(tokens)

        rv = tokenize.untokenize(tokens).decode("utf-8")

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

    def visit_Global(self, n):

        for i in n.names:
            self.globals.add(i)

        return ast.Pass()

    def visit_FunctionDef(self, n):

        old_globals = self.globals

        try:
            n = self.generic_visit(n)

            new_globals = list(self.globals)
            new_globals.sort()

            if new_globals:
                n.body.insert(0, ast.Global(names=new_globals)) # type: ignore

            return n
        finally:
            self.globals = old_globals

reorder_globals = ReorderGlobals()


def fix_ast(tree):
    """
    This applies fixes that will help python 2 code run under python 3. Not all
    problems will be fixed, but this will attempt to handle common issues.

    These are fixes that apply at the AST level.
    """

    if PY2:
        return tree

    try:

        tree = reorder_globals.visit(tree)
        return tree

    except Exception as e:
        # import traceback
        # traceback.print_exc()
        raise e
