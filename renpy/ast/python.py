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

from __future__ import annotations

from typing import Literal, Any

import time
import hashlib
import ast
import renpy


class PyExpr(str):
    """
    Represents a string containing python expression.
    """

    __slots__ = [
        'filename',
        'linenumber',
        "py",
    ]

    filename: str
    linenumber: int
    py: int

    def __new__(cls, s, filename, linenumber, py=3):
        self = str.__new__(cls, s)
        self.filename = filename
        self.linenumber = linenumber
        self.py = py

        # Queue the string for precompilation.
        if self and (renpy.game.script.all_pyexpr is not None):
            renpy.game.script.all_pyexpr.append(self)

        return self

    def __getnewargs__(self):  # type: ignore
        return (str(self), self.filename, self.linenumber, self.py)

    @staticmethod
    def checkpoint() -> Any:
        """
        Checkpoints the pyexpr list. Returns an opaque object that can be used
        to revert the list.
        """

        if renpy.game.script.all_pyexpr is None:
            return None

        return len(renpy.game.script.all_pyexpr)

    @staticmethod
    def revert(opaque: Any):

        if renpy.game.script.all_pyexpr is None:
            return

        if opaque is None:
            return

        renpy.game.script.all_pyexpr[opaque:] = []


class PyCode:
    __slots__ = [
        'source',
        'location',
        'mode',
        'bytecode',
        'hash',
        'py',
    ]

    source: str
    location: tuple[Any, ...]
    mode: Literal["eval", "exec", "hide"]
    bytecode: bytes | None
    hash: bytes
    py: int

    def __getstate__(self):
        return (1, self.source, self.location, self.mode, self.py)

    def __setstate__(self, state):
        if len(state) == 4:
            (_, self.source, self.location, self.mode) = state
            self.py = 2
        else:
            (_, self.source, self.location, self.mode, self.py) = state

        self.bytecode = None

        if renpy.game.script.record_pycode:
            renpy.game.script.all_pycode.append(self)

    def __init__(self, source: str, loc: tuple[str, int] = ('<none>', 1),
                 mode: Literal["eval", "exec", "hide"] = 'exec'):

        self.py = 3

        # The source code.
        self.source = source

        # The time is necessary so we can disambiguate between Python
        # blocks on the same line in different script versions.
        if isinstance(source, PyExpr):
            self.location = (source.filename, source.linenumber, source, int(time.time()))
        else:
            self.location = (*loc, int(time.time()))

        self.mode = mode

        # This will be initialized later on, after we are serialized.
        self.bytecode = None

        if renpy.game.script.record_pycode:
            renpy.game.script.all_pycode.append(self)

        self.hash = self.get_hash()

    def get_hash(self) -> bytes:
        try:
            return self.hash
        except AttributeError:
            pass

        code = self.source
        if isinstance(code, ast.AST):
            code = ast.dump(code)

        source = (repr(self.location) + code).encode("utf-8")
        self.hash = bytes([renpy.bytecode_version]) + \
            hashlib.md5(source).digest()

        return self.hash
