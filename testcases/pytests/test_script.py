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


"""Tests which script files Script.load_script loads after a parse error, and the order it loads them in."""

from types import SimpleNamespace

import pytest

import renpy
from renpy.script import Script


@pytest.fixture
def load(mocker):
    """
    Returns a function that runs Script.load_script over the given game files and returns the names it loaded.

    The Script is built without calling __init__, so nothing scans the real game. Loading a file is replaced by a
    fake that records its name and, for the files named in errors, adds a parse error, which is the only effect of
    a real parse that load_script looks at. The presence of libs.txt and mods.txt is controlled by the files list.
    """

    mocker.patch.object(renpy.parser, "parse_errors", [])
    mocker.patch.object(renpy.display.presplash, "progress")
    mocker.patch.object(renpy.display.presplash, "pump_window")
    mocker.patch.object(renpy.display, "log", SimpleNamespace(write=lambda *args: None))

    def run(files, errors=(), common=(), loaded=(), filtered=()):
        loaded_names = []

        def load_appropriate_file(compiled, source_extensions, dir, fn, initcode):
            loaded_names.append(fn)

            if fn in errors:
                renpy.parser.parse_errors.append(f"error in {fn}")

        script = Script.__new__(Script)
        script.namemap = {}
        script.initcode = []
        script.script_files = [(fn, "/game") for fn in files]
        script.common_script_files = [(fn, "/common") for fn in common]
        script.loaded_scripts = {(fn, "/game") for fn in loaded}
        script.load_languages = set()
        script.translator = mocker.Mock()
        script.compress = mocker.Mock()
        script.load_appropriate_file = load_appropriate_file
        script.script_filter = lambda fn, dir: fn not in filtered

        has_libs = any(fn.startswith("libs/") for fn in files)
        has_mods = any(fn.startswith("mods/") for fn in files)
        markers = {"libs/libs.txt": has_libs, "mods/mods.txt": has_mods}
        mocker.patch.object(renpy.loader, "loadable", lambda name: markers[name])

        script.load_script()

        return loaded_names

    return run


@pytest.mark.parametrize(
    "files,errors,expected",
    [
        # A parse error stops loading only at the end of the group, so every error in the group gets reported.
        (["a", "b", "c"], ["a"], ["a", "b", "c"]),
        # A numbered file that fails stops the lettered files that might use the statement it defines.
        (["01cds", "02more", "script"], ["01cds"], ["01cds", "02more"]),
        # The same split applies inside libs, where the path always starts with a letter.
        (["libs/x/01cds", "libs/x/bar", "script"], ["libs/x/01cds"], ["libs/x/01cds"]),
        # An error in a lettered lib stops the game files, but not the rest of the libs.
        (["libs/x/bar", "libs/x/baz", "script"], ["libs/x/bar"], ["libs/x/bar", "libs/x/baz"]),
        # An error in the game stops mods.
        (["script", "mods/x/01m", "mods/x/m"], ["script"], ["script"]),
        # The same split applies inside mods.
        (["mods/x/01m", "mods/x/m"], ["mods/x/01m"], ["mods/x/01m"]),
    ],
)
def test_parse_error_stops_at_group_end(load, files, errors, expected):
    """
    Tests that a parse error lets the rest of its group load and stops the groups after it. This is what keeps a
    broken creator-defined statement from burying its own error under one error per use of the statement.
    """

    assert load(files, errors) == expected


def test_common_parse_error_stops_game(load):
    """
    Tests that a parse error in a common file stops the game files, even though common files are not sorted by
    game_key.
    """

    assert load(["script"], ["00common"], common=["00common"]) == ["00common"]


def test_common_parse_error_stops_lettered_libs(load):
    """
    Tests that a parse error in a common file stops lettered libs but not numbered ones, which share priority 0 with
    common files. Loading them can only report more errors, since the script still fails to start.
    """

    files = ["libs/x/01cds", "libs/x/bar", "script"]

    assert load(files, ["00common"], common=["00common"]) == ["00common", "libs/x/01cds"]


@pytest.mark.parametrize("skip", ["loaded", "filtered"])
def test_skipped_file_does_not_end_group(load, skip):
    """
    Tests that a file load_script passes over, because it was loaded by an earlier call or filtered out, does not
    end the group of a parse error before it, and is not loaded itself.
    """

    assert load(["a", "b", "c"], ["a"], **{skip: ["b"]}) == ["a", "c"]


def test_load_order_without_errors(load):
    """
    Tests the load order: libs, the game, then mods, with libs and mods sorted without their first directory. The
    numbered and lettered groups only decide where a parse error stops, and must not reorder files.
    """

    files = ["mods/x/m", "script", "libs/x/bar", "mods/y/01m", "00early", "libs/y/01cds"]
    expected = ["00common", "libs/y/01cds", "libs/x/bar", "00early", "script", "mods/y/01m", "mods/x/m"]

    assert load(files, common=["00common"]) == expected
