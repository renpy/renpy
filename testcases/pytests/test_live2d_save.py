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

"""
Tests that Live2D displayables in saves from before Ren'Py 8.6 load correctly. Those saves hold the filename as it was
given to Live2D, which can be a directory, while newer code expects the path to the .model3.json file.
"""

import pytest
from pytest_mock import MockerFixture

from renpy.compat import pickle
from renpy.gl2 import live2d


def make_old_save(mocker: MockerFixture, filename: str) -> bytes:
    """
    Pickles a Live2D displayable in the shape written before 8.6. Patching the class version is what puts version 0
    in the pickle, and it's stopped before returning so that loading sees the current version.
    """

    displayable = live2d.Live2D.__new__(live2d.Live2D)
    displayable.filename = filename

    patched = mocker.patch.object(live2d.Live2D, "__version__", 0)
    try:
        return pickle.dumps(displayable)
    finally:
        mocker.stop(patched)


@pytest.mark.parametrize(
    ("saved", "expected"),
    [
        ("Mao", "Mao/Mao.model3.json"),
        ("live2d/Mao", "live2d/Mao/Mao.model3.json"),
        ("live2d/Mao/Mao.model3.json", "live2d/Mao/Mao.model3.json"),
    ],
)
def test_old_save_expands_filename(mocker: MockerFixture, saved: str, expected: str) -> None:
    """Directory names from old saves are expanded, and the json paths saved by 8.6 prereleases are left alone."""

    assert pickle.loads(make_old_save(mocker, saved)).filename == expected


def test_old_save_reuses_common_cache(mocker: MockerFixture) -> None:
    """
    A loaded displayable must find the common data created at init. Building a second copy would lose the aliases,
    nonexclusive attributes, and callbacks that were applied to the cached one, without any error.
    """

    common = object()
    key = ("live2d/Mao/Mao.model3.json", 1.0, None, None)

    mocker.patch.object(live2d, "common_cache", {key: common})
    build = mocker.patch.object(live2d, "Live2DCommon")

    assert pickle.loads(make_old_save(mocker, "live2d/Mao")).common is common
    build.assert_not_called()


@pytest.mark.parametrize("filename", ["Mao", "live2d/Mao", "live2d/Mao/Mao.model3.json"])
def test_expand_filename_is_idempotent(filename: str) -> None:
    """Expansion runs on every old-version load, including saves whose filename was already expanded."""

    once = live2d.expand_filename(filename)

    assert once.endswith(".model3.json")
    assert live2d.expand_filename(once) == once
