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


import gc
import io
import os
from collections.abc import Callable

import pytest
from pytest_mock import MockerFixture

import renpy
from renpy.pygame import iostream
from renpy.text import font

FONT = os.path.join(renpy.config.renpy_base, "sdk-fonts", "Vazirmatn-RD-UI-Light.ttf")


def open_subfile() -> io.BufferedReader:
    """Mirrors what archives and Android apks return for an uncompressed entry."""

    return io.BufferedReader(iostream.IOSubFile(FONT, 0, os.path.getsize(FONT)))


def open_buffer() -> io.BufferedReader:
    """Mirrors what archives and Android apks return for a compressed entry."""

    with open(FONT, "rb") as f:
        return io.BufferedReader(iostream.IOBuffer(f.read()))


@pytest.mark.parametrize("opener", [open_subfile, open_buffer])
def test_streamed_face_survives_dropped_loader_file(
    mocker: MockerFixture, opener: Callable[[], io.BufferedReader]
) -> None:
    """
    A harfbuzz face streamed from a wrapped IOStream stays readable after the loader's file is dropped.

    open_io unwraps the io.BufferedReader and the face borrows the inner stream, which the reader
    closes when it is collected. The memory buffer size is patched to 0 to force the streaming path,
    which large fonts take in real games. Without the fix, glyphs() reads a freed SDL stream and the
    process segfaults (#7506), so a regression shows up as a crash rather than an assertion failure.
    """

    mocker.patch.object(renpy.config, "font_memory_buffer_size", 0)
    mocker.patch.object(renpy.loader, "load", side_effect=lambda fn, directory=None: opener())
    mocker.patch.dict(font.face_cache, clear=True)
    mocker.patch.dict(font.font_cache, clear=True)

    f = font.get_font("test.ttf", 22, False, False, 0, True, False, "auto", 1.0, "harfbuzz", None, {}, {})
    gc.collect()

    glyphs = f.glyphs("سلام abc", 0)

    assert len(glyphs) > 0
    assert any(g.width > 0 for g in glyphs)
