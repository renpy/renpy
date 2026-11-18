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

"""Tests for the release command's preflight checks."""

import pathlib
import runpy
import sys
from typing import TYPE_CHECKING

import pytest

import renpy

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


@pytest.mark.parametrize(
    ("options", "tags", "tag_required"),
    [
        (["-n"], b"", True),
        (["--no-tag"], b"", True),
        (["-n"], b"8.6.2.26111701\n", False),
        ([], b"", False),
    ],
)
def test_add_requires_a_tag_with_no_tag(
    mocker: "MockerFixture",
    capsys: pytest.CaptureFixture[str],
    options: list[str],
    tags: bytes,
    tag_required: bool,
) -> None:
    """Only --no-tag requires an existing tag before checking the build's version."""
    script = pathlib.Path(renpy.__file__).resolve().parents[1] / "add.py"
    mocker.patch.object(sys, "argv", [str(script), "--real", "--release", "--version", "8.6.2.26111701", *options])
    mocker.patch("subprocess.check_output", return_value=tags)
    # A mismatched build stops the release before checksums, tagging, or uploads.
    mocker.patch("distribute.read_release_version", return_value="8.6.2.26111700")

    with pytest.raises(SystemExit) as exc:
        runpy.run_path(str(script), run_name="__main__")

    output = capsys.readouterr()
    if tag_required:
        assert exc.value.code == 2
        assert "--no-tag requires the current commit to have a tag" in output.err
    else:
        assert exc.value.code == 1
        assert "dl/8.6.2 contains 8.6.2.26111700" in output.out
