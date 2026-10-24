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


"""Tests for the engine startup that pytests/conftest.py performs for the Python tests."""

import subprocess
import sys
from pathlib import Path

import renpy


def test_conftest_initialized_engine():
    """
    Collecting the tests starts the engine before any test runs: the script-visible store is bound and
    the reload backup has been recorded.
    """

    assert renpy.exports.store is renpy.store
    assert renpy.backup.objects_pickle is not None


def test_conftest_initializes_once_in_fresh_process():
    """
    Importing conftest starts the engine exactly once and the reload backup is recorded by that startup.

    This runs in a subprocess because the engine can only start once per process, and the current
    process has already imported conftest. Importing the module a second time must not start the engine
    again; Python's import cache is what guarantees that.
    """

    code = """
from unittest.mock import patch
import importlib
import renpy

with patch.object(renpy, "import_all", wraps=renpy.import_all) as startup:
    import pytests.conftest
    snapshot = renpy.backup.objects_pickle
    importlib.import_module("pytests.conftest")
    startup.assert_called_once_with()
    assert renpy.backup.objects_pickle is snapshot
    assert renpy.exports.store is renpy.store
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=Path(__file__).resolve().parent.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
