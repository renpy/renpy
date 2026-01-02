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

# This file contains code to add and remove statements from the AST
# and the textual representation of Ren'Py code.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode  # *


import renpy
import re
import codecs

# A map from line loc (elided filename, line) to the Line object representing
# that line.
lines: dict[tuple[str, int], "Line"] = {}

# The set of files that have been loaded.
files = set()


class Line(object):
    """
    Represents a logical line in a file.
    """

    def __init__(self, filename, number, start):
        filename = filename.replace("\\", "/")

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
        self.text = ""

        # The full text, including any comments or delimiters.
        self.full_text = ""

    def __repr__(self):
        return "<Line {}:{} {!r}>".format(self.filename, self.number, self.text)


def load_lines(filename, elided_filename):
    """
    Loads the lines out of `filename`.

    This is very similar to renpy.lexer.list_logical_lines, but it includes empty lines
    and lines with only comments.
    """

    global original_filename
    original_filename = filename

    with open(filename, "r", encoding="utf-8") as f:
        data = f.read()

    filename = elided_filename

    if not data.endswith("\n"):
        data += "\n"

    # The line number in the physical file.
    number = 1

    # The current position we're looking at in the buffer.
    pos = 0

    # Are we looking at a triple-quoted string?

    # Skip the BOM, if any.
    if len(data) and data[0] == u'\ufeff':
        pos += 1

    len_data = len(data)

    files.add(filename)

    line = 0
    start_number = 0

    # Looping over the lines in the file.
    while pos < len_data:

        # The line number of the start of this logical line.
        start_number = number

        # The number of open parenthesis there are right now.
        parendepth = 0

        loc = (filename, start_number)
        lines[loc] = renpy.scriptedit.Line(original_filename, start_number, pos)

        endpos = None

        while pos < len_data:

            startpos = pos
            c = data[pos]

            if c == u'\n' and not parendepth:

                if endpos is None:
                    endpos = pos

                lines[loc].end_delim = endpos + 1

                while data[endpos - 1] in u' \r':
                    endpos -= 1

                lines[loc].end = endpos
                lines[loc].text = data[lines[loc].start:lines[loc].end]
                lines[loc].full_text = data[lines[loc].start:lines[loc].end_delim]

                pos += 1
                number += 1
                endpos = None
                break

            if c == u'\n':
                number += 1
                endpos = None

            if c == u"\r":
                pos += 1
                continue

            # Backslash/newline.
            if c == u"\\" and data[pos + 1] == u"\n":
                pos += 2
                number += 1
                continue

            # Parenthesis.
            if c in u'([{':
                parendepth += 1

            if (c in u'}])') and parendepth:
                parendepth -= 1

            # Comments.
            if c == u'#':
                endpos = pos

                while data[pos] != u'\n':
                    pos += 1

                continue

            # Strings.
            if c in u'"\'`':
                delim = c
                pos += 1

                escape = False
                triplequote = False

                if (pos < len_data - 1) and (data[pos] == delim) and (data[pos + 1] == delim):
                    pos += 2
                    triplequote = True

                while pos < len_data:

                    c = data[pos]

                    if c == u'\n':
                        number += 1

                    if c == u'\r':
                        pos += 1
                        continue

                    if escape:
                        escape = False
                        pos += 1
                        continue

                    if c == delim:

                        if not triplequote:
                            pos += 1
                            break

                        if (pos < len_data - 2) and (data[pos + 1] == delim) and (data[pos + 2] == delim):
                            pos += 3
                            break

                    if c == u'\\':
                        escape = True

                    pos += 1

                    continue

                continue

            _word, _magic, end = renpy.lexer.match_logical_word(data, pos)

            pos = end


def ensure_loaded(filename):
    """
    Ensures that the given filename and linenumber are loaded. Doesn't do
    anything if the filename can't be loaded.
    """

    if filename in files:
        return

    if not (filename.endswith(".rpy") or filename.endswith(".rpym")):
        return

    files.add(filename)

    fn = renpy.lexer.unelide_filename(filename)
    load_lines(fn, filename)


def get_line_text(filename, linenumber):
    """
    Gets the text of the line with `filename` and `linenumber`, or the None if
    the line does not exist.
    """

    filename = filename.replace("\\", "/")

    ensure_loaded(filename)

    if (filename, linenumber) in lines:
        return lines[filename, linenumber].text
    else:
        return None


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

    filename = filename.replace("\\", "/")

    ensure_loaded(filename)

    global lines

    new_lines = {}

    for key, line in lines.items():
        (fn, ln) = key

        if (fn == filename) and (linenumber <= ln):
            ln += line_offset
            line.number += line_offset
            line.start += char_offset
            line.end += char_offset
            line.end_delim += char_offset

        new_lines[fn, ln] = line

    lines.clear()
    lines.update(new_lines)


def insert_line_before(code, filename, linenumber):
    """
    Adds `code` immediately before `filename` and `linenumber`. Those must
    correspond to an existing line, and the code is inserted with the same
    indentation as that line.
    """

    filename = filename.replace("\\", "/")

    if renpy.config.clear_lines:
        raise Exception("config.clear_lines must be False for script editing to work.")

    ensure_loaded(filename)

    old_line = lines[filename, linenumber]

    if code:
        indent = re.match(r" *", old_line.text).group(0)
    else:
        indent = ""

    raw_code = indent + code
    code = indent + code + "\n"

    new_line = Line(old_line.filename, old_line.number, old_line.start)
    new_line.text = raw_code
    new_line.full_text = code
    new_line.end = new_line.start + len(raw_code)
    new_line.end_delim = new_line.start + len(code)

    with open(old_line.filename, "r", encoding="utf-8") as f:
        data = f.read()

    data = data[: old_line.start] + code + data[old_line.start :]

    adjust_line_locations(filename, linenumber, len(code), code.count("\n"))

    with renpy.loader.auto_lock:
        with open(old_line.filename, "w", encoding="utf-8") as f:
            f.write(data)

        renpy.loader.add_auto(old_line.filename, force=True)

    lines[filename, linenumber] = new_line


def remove_line(filename, linenumber):
    """
    Removes `linenumber` from `filename`. The line must exist and correspond
    to a logical line.
    """

    filename = filename.replace("\\", "/")

    if renpy.config.clear_lines:
        raise Exception("config.clear_lines must be False for script editing to work.")

    ensure_loaded(filename)

    line = lines[filename, linenumber]

    with open(line.filename, "r", encoding="utf-8") as f:
        data = f.read()

    code = data[line.start : line.end_delim]
    data = data[: line.start] + data[line.end_delim :]

    del lines[filename, linenumber]
    adjust_line_locations(filename, linenumber, -len(code), -code.count("\n"))

    with renpy.loader.auto_lock:
        with open(line.filename, "w", encoding="utf-8") as f:
            f.write(data)

        renpy.loader.add_auto(line.filename, force=True)


def get_full_text(filename, linenumber):
    """
    Returns the full text of `linenumber` from `filename`, including
    any comment or delimiter characters that exist.
    """

    filename = filename.replace("\\", "/")

    ensure_loaded(filename)

    if (filename, linenumber) not in lines:
        return None

    return lines[filename, linenumber].full_text


def nodes_on_line(filename, linenumber):
    """
    Returns a list of nodes that are found on the given line.
    """

    ensure_loaded(filename)

    rv = []

    for i in renpy.game.script.all_stmts:
        if (i.filename == filename) and (i.linenumber == linenumber) and (i.rollback != "never"):
            rv.append(i)

    return rv


def nodes_on_line_at_or_after(filename, linenumber):
    """
    Returns a list of nodes that are found at or after the given line.
    """

    ensure_loaded(filename)

    lines = [
        i.linenumber
        for i in renpy.game.script.all_stmts
        if (i.filename == filename)
        if (i.linenumber >= linenumber)
        if (i.rollback != "never")
    ]

    if not lines:
        return []

    return nodes_on_line(filename, min(lines))


def first_and_last_nodes(nodes):
    """
    Finds the first and last nodes in `nodes`, a list of nodes. This assumes
    that all the nodes are "simple", with no control flow, and that all of
    the relevant nodes are in `nodes`.
    """

    firsts = []
    lasts = []

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
    This adjusts the line numbers in the ast.

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
    Adds `code`, which must be a textual line of Ren'Py code,
    before the given filename and line number.
    """

    nodes = nodes_on_line_at_or_after(filename, linenumber)
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

    for i in renpy.game.contexts:
        i.replace_node(old, block[0])

    renpy.game.log.replace_node(old, block[0])


def can_add_before(filename, linenumber):
    """
    Returns True if it's possible to add a line before the given filename
    and linenumber, and False if it's not possible.
    """

    try:
        nodes = nodes_on_line(filename, linenumber)
        first_and_last_nodes(nodes)

        return True
    except Exception:
        return False


def remove_from_ast(filename, linenumber):
    """
    Removes from the AST all statements that happen to be at `filename`
    and `linenumber`, then adjusts the line numbers appropriately.

    There's an assumption that the statement(s) on the line are "simple",
    not involving control flow.
    """

    nodes = nodes_on_line(filename, linenumber)

    first, last = first_and_last_nodes(nodes)

    new_stmts = []

    for i in renpy.game.script.all_stmts:
        if i in nodes:
            continue

        i.replace_next(first, last.next)

        new_stmts.append(i)

    renpy.game.script.all_stmts = new_stmts

    namemap = renpy.game.script.namemap

    # This is fairly slow - when we remove a node, we have to replace it with
    # the next node. But if we then remove the next node, we have to replace it
    # again. So we just walk all the known names to do this.
    for k in list(namemap):
        if namemap[k] in nodes:
            namemap[k] = last.next

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
