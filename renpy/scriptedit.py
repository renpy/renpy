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
import re
import codecs


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

        # The offset inside the lime where the line delimiter ends.
        self.end_delim = start

        # The text of the line.
        self.text = ''

    def __repr__(self):
        return "<Line {}:{} {!r}>".format(self.filename, self.number, self.text)


def get_line_text(filename, linenumber):
    """
    Gets the text of the line with `filename` and `linenumber`, or the empty
    string if the line does not exist.
    """

    if (filename, linenumber) in lines:
        return lines[filename, linenumber].text
    else:
        return ""


def adjust_line_locations(filename, linenumber, char_offset, line_offset):
    """
    Adjusts the locations in the line data structure.

    `filename`, `linenumber`
        The filename and first line number to adjust.

    `char_offset`
        The number of characters in the file to offset the code by,.

    `line_offset`
        The number of line in the file to offset the code by.
    """

    global lines

    new_lines = { }

    for key, line in lines.iteritems():

        (fn, ln) = key

        if (fn == filename) and (linenumber <= ln):
            ln += line_offset
            line.number += line_offset
            line.start += char_offset
            line.end += char_offset
            line.end_delim += char_offset

        new_lines[fn, ln] = line

    lines = new_lines


def insert_line_before(code, filename, linenumber):
    """
    Adds `code` immediately before `filename` and `linenumber`. Those must
    correspond to an existing line, and the code is inserted with the same
    indentation as that line.
    """

    if renpy.config.clear_lines:
        raise Exception("config.clear_lines must be False for script editing to work.")

    if not renpy.game.args.compile: # @UndefinedVariable
        raise Exception("The compile flag must have been given for script editing to work.")

    old_line = lines[filename, linenumber]

    m = re.match(r' *', old_line.text)
    indent = m.group(0)

    raw_code = indent + code
    code = indent + code + "\r\n"

    new_line = Line(old_line.filename, old_line.number, old_line.start)
    new_line.text = raw_code
    new_line.end = new_line.start + len(raw_code)
    new_line.end_delim = new_line.start + len(code)

    with codecs.open(old_line.filename, "r", "utf-8") as f:
        data = f.read()

    data = data[:old_line.start] + code + data[old_line.start:]

    adjust_line_locations(filename, linenumber, len(code), code.count("\n"))

    with renpy.loader.auto_lock:

        with codecs.open(old_line.filename, "w", "utf-8") as f:
            f.write(data)

        renpy.loader.add_auto(old_line.filename, force=True)

    lines[filename, linenumber] = new_line

def remove_line(filename, linenumber):
    """
    Removes `linenumber` from `filename`. The line must exist and correspond
    to a logical line.
    """

    if renpy.config.clear_lines:
        raise Exception("config.clear_lines must be False for script editing to work.")

    if not renpy.game.args.compile: # @UndefinedVariable
        raise Exception("The compile flag must have been given for script editing to work.")


    line = lines[filename, linenumber]

    with codecs.open(line.filename, "r", "utf-8") as f:
        data = f.read()

    code = data[line.start:line.end_delim]
    data = data[:line.start] + data[line.end_delim:]

    del lines[filename, linenumber]
    adjust_line_locations(filename, linenumber, -len(code), -code.count("\n"))

    with renpy.loader.auto_lock:

        with codecs.open(line.filename, "w", "utf-8") as f:
            f.write(data)

        renpy.loader.add_auto(line.filename, force=True)

def nodes_on_line(filename, linenumber):
    """
    Returns a list of nodes that are found on the given line.
    """

    rv = [ ]

    for i in renpy.game.script.all_stmts:
        if (i.filename == filename) and (i.linenumber == linenumber):
            rv.append(i)

    return rv

def first_and_last_nodes(nodes):
    """
    Finds the first and last nodes in `nodes`, a list of nodes. This assumes
    that all the nodes are "simple", with no control flow, and that all of
    the relevant nodes are in `nodes`.
    """

    firsts = [ ]
    lasts = [ ]

    for i in nodes:
        for j in nodes:
            if j.next is i:
                break
        else:
            firsts.append(i)

        for j in nodes:
            if i.next is j:
                break

        else:
            lasts.append(i)

    if len(firsts) != 1:
        raise Exception("Could not find unique first AST node.")

    if len(lasts) != 1:
        raise Exception("Could not find unique last AST node.")

    return firsts[0], lasts[0]


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


def add_to_ast_before(code, filename, linenumber):
    """
    Adds `code`, which must be a textual line of Ren'Py code, to the AST
    immediately before `statement`, which should be an AST node.
    """

    nodes = nodes_on_line(filename, linenumber)
    old, _ = first_and_last_nodes(nodes)

    adjust_ast_linenumbers(old.filename, linenumber, 1)

    block, _init = renpy.game.script.load_string(old.filename, code, linenumber=linenumber)

    # Remove the return statement at the end of the block.
    ret_stmt = block.pop()
    renpy.game.script.all_stmts.remove(ret_stmt)

    if not block:
        return

    for i in renpy.game.script.all_stmts:
        i.replace_next(old, block[0])

    renpy.ast.chain_block(block, old)

def remove_from_ast(filename, linenumber):
    """
    Removes from the AST all statements that happen to be at `filename`
    and `linenumber`, then adjusts the line numbers appropriately.

    There's an assumption that the statement(s) on the line are "simple",
    not involving control flow.
    """

    nodes = nodes_on_line(filename, linenumber)

    first, last = first_and_last_nodes(nodes)

    new_stmts = [ ]

    for i in renpy.game.script.all_stmts:
        if i in nodes:
            continue

        i.replace_next(first, last.next)

        new_stmts.append(i)

    renpy.game.script.all_stmts = new_stmts

    adjust_ast_linenumbers(filename, linenumber, -1)



serial = 1

def test_add():

    global serial
    s = "'Hello world %f'" % serial
    serial += 1

    node = renpy.game.script.lookup(renpy.game.context().current)
    filename = node.filename
    linenumber = node.linenumber

    add_to_ast_before(s, filename, linenumber)
    insert_line_before(s, filename, linenumber)
    renpy.exports.restart_interaction()

def test_remove():

    node = renpy.game.script.lookup(renpy.game.context().current)
    filename = node.filename
    linenumber = node.linenumber

    remove_from_ast(filename, linenumber)
    remove_line(filename, linenumber)
    renpy.exports.rollback(checkpoints=0, force=True, greedy=True)
