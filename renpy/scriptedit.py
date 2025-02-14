# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
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

from dataclasses import dataclass
from pathlib import Path

import renpy.tokenizer

@dataclass(eq=False)
class Line:
    """
    Represent a logical line of Ren'Py code.
    In contrast to renpy.tokenizer.Line, this class represents
    lines exactly as they appear in the file, including comments.
    Also, it includes
    """

    # The full path to the file with the line in it.
    filename: str

    # The line number where logical line starts.
    number: int

    # The lines of the logical line.
    lines: tuple[str, ...]

    # The comments on the lines.
    comments: tuple[str, ...]

    _text: str | None = None
    _full_text: str | None = None

    @property
    def blank(self):
        return self.lines == ["\n"]

    @property
    def text(self):
        if self._text is None:
            self._text = "".join(self.lines)

        return self._text

    @property
    def full_text(self):
        if self._full_text is not None:
            return self._full_text

        def join():
            for i, line in enumerate(self.lines):
                comment = self.comments[i]
                if comment:
                    yield f"{line[:-1]}{comment}\n"
                else:
                    yield line

        self._full_text = "".join(join())
        return self._full_text

    def with_added_code(self, code: str) -> str:
        """
        Return a full text with a code added to the end before comment.
        """

        def join():
            last_i = len(self.lines) - 1
            for i, line in enumerate(self.lines):
                if i == last_i:
                    line = f"{line[:-1]}{code}\n"

                comment = self.comments[i]
                if comment:
                    yield f"{line[:-1]}{comment}\n"
                else:
                    yield line

        return "".join(join())



# A map from elided filename to dict of line number to Line objects
# representing that file.
lines = dict[str, dict[int, Line]]()


def ensure_loaded(filename: str, reload: bool = False ) -> dict[int, Line] | None:
    """
    Ensures that the given filename is loaded.
    Doesn't do anything if the filename can't be loaded or is empty.
    If `reload` is true, the file will be reloaded even if it's already
    loaded.
    """

    filename = renpy.parser.unelide_filename(filename)
    path = Path(filename)

    if not (path.exists() and (
        path.name.endswith("_ren.py") or
        path.name.endswith(".rpy") or
        path.name.endswith(".rpym")
    )):
        return None

    filename = renpy.parser.elide_filename(path.as_posix())

    if reload:
        lines.pop(filename, None)
    elif filename in lines:
        return lines[filename]

    lines[filename] = dict()

    def linesfunc():
        tok = renpy.tokenizer.from_file(filename)

        yield from tok.physical_lines()

        while True:
            yield ""

    file_lines = linesfunc()
    current_line = next(file_lines)
    last_lineno = 1
    start_lineno = 1
    seen_token = False

    tokens = renpy.tokenizer.from_file(filename).tokens()
    text_lines: list[str] = []
    comments: list[str] = []
    for token in tokens:
        # Fast-path for comment-only and empty lines.
        while not seen_token:
            comment = ""
            if token.kind == "comment":
                comment = token.string
                start = token.physical_location.start_col_offset
                end = token.physical_location.end_col_offset
                current_line = f"{current_line[:start]}{current_line[end:]}"
                # Next token is always NL.
                token = next(tokens)

            if token.kind == "nl":
                lines[filename][last_lineno] = Line(
                    filename,
                    last_lineno,
                    (current_line, ),
                    (comment, ))

                current_line = next(file_lines)
                last_lineno += 1
                token = next(tokens)
                continue

            # New logical line just started.
            seen_token = True
            start_lineno = last_lineno
            break

        # Consume lines between the last line and the start of the token.
        # It happens only for multiline strings, so no comments here.
        while last_lineno < token.physical_location.start_lineno:
            text_lines.append(current_line)
            comments.append("")
            current_line = next(file_lines)
            last_lineno += 1

        if token.kind == "comment":
            comment = token.string
            start = token.physical_location.start_col_offset
            end = token.physical_location.end_col_offset
            current_line = f"{current_line[:start]}{current_line[end:]}"

            # Should be NL or NEWLINE.
            token = next(tokens)
        else:
            comment = ""

        if token.kind == "nl":
            text_lines.append(current_line)
            comments.append(comment)
            current_line = next(file_lines)
            last_lineno += 1

        elif token.kind == "newline":
            text_lines.append(current_line)
            comments.append(comment)

            lines[filename][start_lineno] = Line(
                filename,
                start_lineno,
                tuple(text_lines),
                tuple(comments))

            text_lines.clear()
            comments.clear()
            current_line = next(file_lines)
            last_lineno += 1
            seen_token = False

    if not lines[filename]:
        del lines[filename]
        return None

    return lines[filename]


def get_line_text(filename: str, linenumber: int):
    """
    Gets the text of the line with `filename` and `linenumber`, or the None if
    the line does not exist.
    """

    lines = ensure_loaded(filename)
    if lines is None:
        return None

    try:
        return lines[linenumber].text
    except KeyError:
        return None


def get_full_text(filename: str, linenumber: int):
    """
    Returns the full text of `linenumber` from `filename`, including
    any comment or delimiter characters that exist.
    """

    lines = ensure_loaded(filename)
    if lines is None:
        return None

    try:
        return lines[linenumber].full_text
    except KeyError:
        return None


def insert_line_before(code: str, filename: str, linenumber: int):
    """
    Adds `code` immediately before `filename` and `linenumber`. Those must
    correspond to an existing line, and the code is inserted with the same
    indentation as that line.
    """

    if renpy.config.clear_lines:
        raise Exception("config.clear_lines must be False for script editing to work.")

    lines = ensure_loaded(filename)
    if lines is None:
        return

    old_line = lines[linenumber]

    if code:
        indent = re.match(r' *', old_line.text).group(0)
    else:
        indent = ''

    line_ending = "\n" if code.endswith("\n") else "\n"
    code = f"{indent}{code}{line_ending}"

    path = Path(renpy.parser.unelide_filename(old_line.filename))
    with path.open("w", encoding="utf-8") as f, renpy.loader.auto_lock:
        f.write("\ufeff")

        for lineno, line in lines.items():
            if lineno == linenumber:
                f.write(code)

            f.write(line.full_text)

        renpy.loader.add_auto(old_line.filename, force=True)

    ensure_loaded(old_line.filename, reload=True)


def remove_line(filename: str, linenumber: int):
    """
    Removes `linenumber` from `filename`. The line must exist and correspond
    to a logical line.
    """

    if renpy.config.clear_lines:
        raise Exception("config.clear_lines must be False for script editing to work.")

    lines = ensure_loaded(filename)
    if lines is None:
        return

    old_line = lines[linenumber]

    path = Path(renpy.parser.unelide_filename(old_line.filename))
    with path.open("w", encoding="utf-8") as f, renpy.loader.auto_lock:
        f.write("\ufeff")

        for lineno, line in lines.items():
            if lineno == linenumber:
                continue

            f.write(line.full_text)

        renpy.loader.add_auto(old_line.filename, force=True)

    ensure_loaded(old_line.filename, reload=True)


def nodes_on_line(filename: str, linenumber: int) -> list[renpy.ast.Node]:
    """
    Returns a list of nodes that are found on the given line.
    """

    if (lines := ensure_loaded(filename)) is None:
        return [ ]

    filename = next(iter(lines.values())).filename

    rv = [ ]

    for i in renpy.game.script.all_stmts:
        if (i.filename == filename) and (i.linenumber == linenumber) and (i.rollback != "never"):
            rv.append(i)

    return rv


def nodes_on_line_at_or_after(filename: str, linenumber: int) -> list[renpy.ast.Node]:
    """
    Returns a list of nodes that are found at or after the given line.
    """

    if (lines := ensure_loaded(filename)) is None:
        return [ ]

    filename = next(iter(lines.values())).filename

    lines = [ i.linenumber
              for i in renpy.game.script.all_stmts
              if (i.filename == filename)
              if (i.linenumber >= linenumber)
              if (i.rollback != "never") ]

    if not lines:
        return [ ]

    return nodes_on_line(filename, min(lines))


def first_and_last_nodes(nodes: list[renpy.ast.Node]):
    """
    Finds the first and last nodes in `nodes`, a list of nodes. This assumes
    that all the nodes are "simple", with no control flow, and that all of
    the relevant nodes are in `nodes`.
    """

    firsts: list[renpy.ast.Node] = [ ]
    lasts: list[renpy.ast.Node] = [ ]

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


def adjust_ast_linenumbers(filename: str, linenumber: int, offset: int):
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


def add_to_ast_before(code: str, filename: str, linenumber: int):
    """
    Adds `code`, which must be a textual line of Ren'Py code,
    before the given filename and line number.
    """

    nodes = nodes_on_line_at_or_after(filename, linenumber)
    old, _ = first_and_last_nodes(nodes)

    adjust_ast_linenumbers(old.filename, linenumber, 1)

    block, _init = renpy.game.script.load_string(
        old.filename, code, linenumber=linenumber)

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


def can_add_before(filename: str, linenumber: int):
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


def remove_from_ast(filename: str, linenumber: int):
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
