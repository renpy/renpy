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
        ("work/tom/test123", False, False, False, "8.6.0.26110101+unofficial.test123"),
        ("work/tom/test123", False, False, True, "8.6.0.26110101+unofficial.dirty.test123"),
        ("", False, False, False, "8.6.0.26110101+unofficial"),
        ("", False, False, True, "8.6.0.26110101+unofficial.dirty"),
        ("work/tom/test123", True, True, False, "8.6.0.26110101+nightly"),
    ],
)
def test_make_version_string(branch, official, nightly, dirty, expected):
    """
    Checks the version suffix. Only the part of the branch name after the last slash is used, and an empty
    branch name (detached HEAD) must not leave a trailing dot. Official builds never include the branch.
    """

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
    """
    The release version is the last one that shipped. A nightly build of the fix branch reports the previous point
    release, since the version it carries has not shipped yet, except for x.y.0, which has no previous point
    release. Every other build reports its own version without the build date or suffix.
    """

    monkeypatch.setattr(
        renpy.versions, "get_version", lambda: {"version": version, "branch": branch, "nightly": nightly}
    )

    assert renpy.versions.get_release_version() == expected
