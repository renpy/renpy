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

"""Tests for building and reading Ren'Py version numbers."""

import pytest

import renpy.versions


@pytest.mark.parametrize(
    ("branch", "official", "nightly", "dirty", "expected"),
    [
        ("master", True, False, False, "8.6.0.26110101"),
        ("master", True, True, False, "8.6.0.26110101+nightly"),
        ("master", True, False, True, "8.6.0.26110101+dirty"),
        ("master", False, False, False, "8.6.0.26110101+unofficial"),
        ("feature", False, False, True, "8.6.0.26110101+unofficial.dirty.feature"),
    ],
)
def test_make_version_string(branch, official, nightly, dirty, expected):
    assert renpy.versions._make_version_string((8, 6, 0, 26110101), branch, official, nightly, dirty) == expected


@pytest.mark.parametrize(
    ("version", "branch", "nightly", "expected"),
    [
        ("8.5.3.26051504", "fix", True, "8.5.2"),
        ("8.5.0.26051504", "fix", True, "8.5.0"),
        ("8.5.3.26051504", "fix", False, "8.5.3"),
        ("8.6.0.26110101+nightly", "master", True, "8.6.0"),
    ],
)
def test_get_release_version(monkeypatch, version, branch, nightly, expected):
    monkeypatch.setattr(
        renpy.versions, "get_version", lambda: {"version": version, "branch": branch, "nightly": nightly}
    )

    assert renpy.versions.get_release_version() == expected
