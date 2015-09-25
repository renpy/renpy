# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains code to add and remove statements from the AST
# and the textual representation of Ren'Py code.

import renpy


# A map from line loc (elided filename, line) to the Line object representing
# that line.
lines = { }


class Line(object):
    """
    Represents a logical line in a file.
    """

    def __init__(self, filename, number, start):

        # The full path to the file with the line in it.
        self.filename = filename

        # The line number.
        self.number = number

        # The offset inside the file at which the line starts.
        self.start = start

        # The offset inside the file at which the line ends.
        self.end = start

        # The text of the line.
        self.text = ''

    def __repr__(self):
        return "<Line {}:{} {!r}>".format(self.filename, self.number, self.text)




def adjust_ast_linenumbers(filename, linenumber, offset):
    """
    This adjusts the line numbers in the the ast.

    `filename`
        The filename to adjust.

    `linenumber`
        The first line to adjust.

    `offset`
        The amount to adjust by. Positive numbers increase the line
    """

    for i in renpy.game.script.all_stmts:
        if (i.filename == filename) and (i.linenumber >= linenumber):
            i.linenumber += offset


def add_to_ast_before(line, statement):
    """
    Adds `line`, which must be a textual line of Ren'Py code, to the AST
    immediately before `statement`, which should be an AST node.
    """

    # TODO: We probably want to deal with the file name and line number.

    old = renpy.game.script.lookup(statement)

    linenumber = old.linenumber

    adjust_ast_linenumbers(old.filename, linenumber, 1)

    block, _init = renpy.game.script.load_string(old.filename, line, linenumber=linenumber)

    # Remove the return statement at the end of the block.
    block = block[:-1]

    if not block:
        return

    for i in renpy.game.script.all_stmts:
        i.replace_next(old, block[0])

    renpy.ast.chain_block(block, old)

def test():

    import time
    s = "'Hello world %f'\n" % time.time()

    add_to_ast_before(s, renpy.game.context().current)
