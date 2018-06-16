# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

# This module contains code to support user-defined statements.

from __future__ import print_function

import renpy

# The statement registry. It's a map from tuples giving the prefixes of
# statements to dictionaries giving the methods used for that statement.
registry = { }

parsers = renpy.parser.ParseTrie()


def register(name, parse=None, lint=None, execute=None, predict=None, next=None, scry=None, block=False, init=False, translatable=False, execute_init=None, label=None, warp=None):  # @ReservedAssignment
    """
    :doc: statement_register
    :name: renpy.register_statement

    This registers a user-defined statement.

    `name`
        This is either a space-separated list of names that begin the statement, or the
        empty string to define a new default statement (the default statement will
        replace the say statement).

    `block`
        When this is False, the statement does not expect a block. When True, it
        expects a block, but leaves it up to the lexer to parse that block. If the
        string "script", the block is interpreted as containing one or more
        Ren'Py script language statements.

    `parse`
        This is a function that takes a Lexer object. This function should parse the
        statement, and return an object. This object is passed as an argument to all the
        other functions. The lexer argument has the following methods:

    `lint`
        This is called to check the statement. It is passed a single argument, the
        object returned from parse. It should call renpy.error to report errors.

    `execute`
        This is a function that is called when the statement executes. It is passed a
        single argument, the object returned from parse.

    `execute_init`
        This is a function that is called at init time, at priority 0.

    `predict`
        This is a function that is called to predict the images used by the statement.
        It is passed a single argument, the object returned from parse. It should return
        a list of displayables used by the statement.

    `next`
        This is a function that is called to determine the next statement.

        If `block` is not "script", this is passed a single argument, the object
        returned from the parse function. If `block` is "script", an additional
        argument is passed, an object that names the first statement in the block.

        The function should return either a string giving a label to jump to,
        the second argument to transfer control into the block, or None to
        continue to the statement after this one.

    `label`
        This is a function that is called to determine the label of this
        statement. If it returns a string, that string is used as the statement
        label, which can be called and jumped to like any other label.

    `warp`
        This is a function that is called to determine if this statement
        should execute during warping. If the function exists and returns
        true, it's run during warp, otherwise the statement is not run
        during warp.

    `scry`
        Used internally by Ren'Py.

    `init`
        True if this statement should be run at init-time. (If the statement
        is not already inside an init block, it's automatically placed inside
        an init 0 block.) This calls the execute function, in addition to the
        execute_init function.

    """
    name = tuple(name.split())

    registry[name] = dict(parse=parse,
                          lint=lint,
                          execute=execute,
                          execute_init=execute_init,
                          predict=predict,
                          next=next,
                          scry=scry,
                          label=label,
                          warp=warp)

    # The function that is called to create an ast.UserStatement.
    def parse_user_statement(l, loc):
        renpy.exports.push_error_handler(l.error)

        try:
            rv = renpy.ast.UserStatement(loc, l.text, l.subblock)
            rv.translatable = translatable

            if not block:
                l.expect_noblock(" ".join(name) + " statement")
                l.advance()
            elif block == "script":
                l.expect_block(" ".join(name) + " statement")
                rv.code_block = renpy.parser.parse_block(l.subblock_lexer())
                l.advance()
            else:
                l.expect_block(" ".join(name) + " statement")
                l.advance()
        finally:
            renpy.exports.pop_error_handler()

        if init and not l.init:
            rv = renpy.ast.Init(loc, [ rv ], 0)

        return rv

    renpy.parser.statements.add(name, parse_user_statement)

    # The function that is called to get our parse data.
    def parse_data(l):
        return (name, registry[name]["parse"](l))

    parsers.add(name, parse_data)


def parse(node, line, subblock):

    block = [ (node.filename, node.linenumber, line, subblock) ]
    l = renpy.parser.Lexer(block)
    l.advance()

    renpy.exports.push_error_handler(l.error)
    try:

        pf = parsers.parse(l)
        if pf is None:
            l.error("Could not find user-defined statement at runtime.")

        return pf(l)

    finally:
        renpy.exports.pop_error_handler()


def call(method, parsed, *args, **kwargs):
    name, parsed = parsed

    method = registry[name].get(method)
    if method is None:
        return None

    return method(parsed, *args, **kwargs)


def get_name(parsed):
    name, _parsed = parsed
    return " ".join(name)
