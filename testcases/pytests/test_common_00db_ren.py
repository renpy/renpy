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

"""Tests for the JSONDB class in renpy/common/00db_ren.py: its writes go through renpy.safe_rename."""

import importlib.util
import json
import pathlib
import sys

import pytest

import renpy


@pytest.fixture
def jsondb(mocker, tmp_path):
    """
    A JSONDB stored in a temporary directory over an existing file, with one changed entry. Returns (object, path).

    Common scripts don't run during engine startup in these tests, but a _ren.py file is also valid Python, so the
    module is loaded from its source. JSONDBs are created during init, and save at exit, so those are patched out.
    """

    source = pathlib.Path(renpy.__file__).parent / "common" / "00db_ren.py"
    spec = importlib.util.spec_from_file_location("test_00db_ren", source)

    # Keeps bytecode for this file out of renpy/common, where a distribution could pick it up.
    mocker.patch.object(sys, "dont_write_bytecode", True)

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    mocker.patch.object(renpy.exports, "is_init_phase", return_value=True)
    mocker.patch.object(renpy.exports, "loadable", return_value=False)
    mocker.patch.object(renpy.config, "gamedir", str(tmp_path))
    mocker.patch.object(renpy.config, "developer", True)
    mocker.patch.object(renpy.config, "at_exit_callbacks", [])

    path = tmp_path / "db.json"
    path.write_text("previous data")

    db = module.JSONDB("db.json")
    db["entry"]["key"] = "value"
    return db, path


def test_jsondb_replaces_file_another_program_has_open(windows_replace, jsondb):
    """A JSONDB goes through renpy.safe_rename, so a refused replacement moves the old file out of the way."""

    db, path = jsondb

    db.save()

    assert json.loads(path.read_text()) == {"entry": {"key": "value"}}
    assert [p.name for p in path.parent.iterdir()] == [path.name]


def test_failed_jsondb_write_keeps_existing_file(mocker, jsondb):
    """
    This used to delete the file before moving the new one into place, so a failure could lose it. The error still
    reaches the caller, and the new data stays in the .new file, as it did before.
    """

    db, path = jsondb
    mocker.patch("renpy.loadsave.os.replace", side_effect=OSError("disk error"))

    with pytest.raises(OSError, match="disk error"):
        db.save()

    assert path.read_text() == "previous data"
    assert json.loads(path.with_name("db.json.new").read_text()) == {"entry": {"key": "value"}}
