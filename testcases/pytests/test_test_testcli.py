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

"""Tests for renpy.test.testcli: the output of `test --list`, and how options map to test settings."""

import argparse
import sys

import pytest

import renpy
from renpy.test import testcli, testexecution, testreporter, testsettings


@pytest.mark.parametrize(
    ("paths", "expected"),
    [
        ([], []),
        (["s", "s.case(x=1)"], ["s", "s.case(x=1)"]),
        (
            ["s", "s.case(x=nan)", "s.case(x=1)", "s.obj(o=<Thing object at 0x1>)", "s.c(t=x) : (y)"],
            ["s", "s.case(x=nan) *", "s.case(x=1)", "s.obj(o=<Thing object at 0x1>) *", "s.c(t=x) : (y) *", "",
             testcli.INVALID_NAME_WARNING],
        ),
    ],
    ids=["empty", "all-valid", "some-invalid"],
)
def test_format_test_list_marks_invalid_names(paths, expected):
    """
    Names that can't be used as filters, because a parameter's repr isn't a Python literal, are marked with an
    asterisk, and the warning explaining the asterisk is printed once at the end. Valid names are printed as they
    are, so they can be pasted into a filter, and no warning is printed when every name is valid.

    The invalid names cover a value that parses but isn't a literal (nan), a repr that isn't valid Python, and a
    repr that closes the parameter parenthesis itself, leaving a colon outside it, which the filter parser rejects
    with DeprecationWarning rather than KeyError.
    """

    assert testcli.format_test_list(paths) == expected


################################################################################
# Persisting after the tests
################################################################################


@pytest.fixture
def run_test_command(mocker):
    """
    Returns a function that runs the test command with the given extra arguments, and returns the test settings
    it produced.

    Setting up and starting a test run are patched out, as these tests are only about how the arguments map to
    settings. The settings object is replaced, so that the values parsed here don't leak into later tests.
    """

    settings = testsettings.TestSettings()
    mocker.patch.object(testcli, "_test", settings)
    mocker.patch.object(testexecution, "initialized", False)
    mocker.patch.object(testcli, "setup_global_test_suite")
    mocker.patch.object(testexecution, "evaluate_enabled_expressions")
    mocker.patch.object(testexecution, "initialize")
    mocker.patch.object(testreporter.reporter, "add_reporter")

    # The parser names the command's argument group after the command found by the first parsing pass.
    mocker.patch.object(renpy.game, "args", argparse.Namespace(command="test"))

    def run(*args):
        mocker.patch.object(sys, "argv", ["renpy.py", "game", "test", *args])
        assert testcli.test_command()
        return settings

    return run


@pytest.mark.parametrize(
    ("args", "expected"),
    [((), None), (("--persist",), True), (("--nopersist",), False)],
    ids=["default", "persist", "nopersist"],
)
def test_persist_options_set_persist(run_test_command, args, expected):
    """
    --persist and --nopersist set `_test.persist`, and leaving both out keeps it None, so that
    config.persist_after_tests decides.
    """

    assert run_test_command(*args).persist is expected


def test_persist_options_are_exclusive(run_test_command):
    """
    Passing both --persist and --nopersist is a usage error, rather than one silently winning.
    """

    with pytest.raises(SystemExit) as excinfo:
        run_test_command("--persist", "--nopersist")

    assert excinfo.value.code == 2
