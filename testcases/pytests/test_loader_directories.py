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


"""Tests that the loader searches config.audio_directories and config.image_directories when loading by name."""

from types import SimpleNamespace

import pytest

import renpy
from renpy import loader
from renpy.audio.audio import Channel


@pytest.fixture(autouse=True)
def loader_config(mocker):
    """
    Gives the tests a known search path and no language. search_prefixes is reduced to the game directory, so each
    expected list shows only what the directory argument adds.
    """

    mocker.patch.object(renpy.config, "search_prefixes", [""])
    mocker.patch.object(renpy.config, "tl_directory", "tl")
    mocker.patch.object(renpy.config, "add_to_special_directories", True)
    mocker.patch.object(renpy.config, "loadable_callback", None)
    mocker.patch.object(renpy.config, "audio_directories", ["audio"])
    mocker.patch.object(renpy.config, "image_directories", ["images"])
    mocker.patch.object(
        renpy.config, "special_directory_map", {"images": ["images"], "audio": ["audio"], "fonts": ["fonts"]}
    )
    mocker.patch.object(renpy.game, "preferences", SimpleNamespace(language=None))


@pytest.mark.parametrize(
    "directory,variable",
    [
        ("audio", "audio_directories"),
        ("images", "image_directories"),
    ],
)
def test_configured_directories_follow_mapped(mocker, directory, variable):
    """
    Configured directories are searched after the mapped ones, so a file found before this feature existed still
    resolves to the same path.
    """

    mocker.patch.object(renpy.config, variable, ["common/" + directory, "full/" + directory])

    assert loader.get_prefixes(tl=False, directory=directory) == [
        "",
        directory + "/",
        "common/" + directory + "/",
        "full/" + directory + "/",
    ]


def test_directories_are_normalized_and_deduplicated(mocker):
    """
    Slashes are stripped as the namespace scan does, and a directory that is listed twice, or is also a mapped
    directory, is only searched once.
    """

    mocker.patch.object(renpy.config, "audio_directories", ["/audio/", "full/audio/", "full/audio"])

    assert loader.get_prefixes(tl=False, directory="audio") == ["", "audio/", "full/audio/"]


def test_empty_list_keeps_mapped_directories(mocker):
    """
    Games declaring older compatibility have an empty list, and must still search the mapped directory as before.
    """

    mocker.patch.object(renpy.config, "audio_directories", [])

    assert loader.get_prefixes(tl=False, directory="audio") == ["", "audio/"]


def test_other_directories_are_unaffected(mocker):
    """
    Only audio and images have a matching variable. Fonts and unmapped names search what they always did, and neither
    variable leaks into them.
    """

    mocker.patch.object(renpy.config, "audio_directories", ["full/audio"])
    mocker.patch.object(renpy.config, "image_directories", ["full/images"])

    assert loader.get_prefixes(tl=False, directory="fonts") == ["", "fonts/"]
    assert loader.get_prefixes(tl=False, directory="other") == ["", "other/"]
    assert loader.get_prefixes(tl=False) == [""]


def test_special_directory_map_keeps_priority(mocker):
    """
    A customized special_directory_map is searched first, in its own order, and its entries are not repeated.
    """

    mocker.patch.dict(renpy.config.special_directory_map, {"audio": ["first", "full/audio"]})
    mocker.patch.object(renpy.config, "audio_directories", ["full/audio", "last"])

    assert loader.get_prefixes(tl=False, directory="audio") == ["", "first/", "full/audio/", "last/"]


def test_special_directory_map_is_not_modified(mocker):
    """
    Lookups must not write the configured directories back into the map, as config can't change after init.
    """

    mocker.patch.object(renpy.config, "audio_directories", ["full/audio"])

    loader.get_prefixes(tl=False, directory="audio")

    assert renpy.config.special_directory_map["audio"] == ["audio"]


def test_configured_directories_get_translated_prefixes(mocker):
    """
    A translated copy of a file in a configured directory takes priority over the original, as in a mapped directory.
    """

    mocker.patch.object(renpy.game, "preferences", SimpleNamespace(language="french"))
    mocker.patch.object(renpy.config, "audio_directories", ["full/audio"])

    assert loader.get_prefixes(directory="audio") == [
        "tl/french/",
        "",
        "tl/french/audio/",
        "audio/",
        "tl/french/full/audio/",
        "full/audio/",
    ]


def test_compatibility_variable_disables_search(mocker):
    """
    With config.add_to_special_directories False, as for games declaring compatibility with Ren'Py 8.5 or earlier, only
    the mapped directories are searched, even when the game sets the lists itself.
    """

    mocker.patch.object(renpy.config, "add_to_special_directories", False)
    mocker.patch.object(renpy.config, "audio_directories", ["full/audio"])
    mocker.patch.object(renpy.config, "image_directories", ["full/images"])

    assert loader.get_prefixes(tl=False, directory="audio") == ["", "audio/"]
    assert loader.get_prefixes(tl=False, directory="images") == ["", "images/"]


@pytest.fixture
def playable_channel(mocker):
    """
    Makes only full/audio/mini/x.ogg exist, and supplies a bare channel, so renpy.music.playable can run without
    audio set up.
    """

    channel = Channel.__new__(Channel)
    channel.file_prefix = ""
    channel.file_suffix = ""

    mocker.patch.object(renpy.audio.music, "get_channel", return_value=channel)
    mocker.patch.object(loader, "loadable_core", side_effect=lambda name: name == "full/audio/mini/x.ogg")


@pytest.mark.parametrize("filename", ["mini/x.ogg", "<from 0.0 to 12.0>mini/x.ogg"])
def test_audio_directories_make_file_playable(mocker, playable_channel, filename):
    """
    Regression test for #7496: a path relative to a configured audio directory is playable, with or without a partial
    playback spec. The reporter saw this with a spec, but the spec was never the cause.
    """

    mocker.patch.object(renpy.config, "audio_directories", ["common/audio", "full/audio"])

    assert renpy.audio.music.playable(filename, "sound")


@pytest.mark.parametrize("filename", ["mini/x.ogg", "<from 0.0 to 12.0>mini/x.ogg"])
def test_file_outside_audio_directories_is_not_playable(playable_channel, filename):
    """
    The same file is not found when its directory isn't configured, so the regression test above can't pass merely
    because everything is reported as loadable.
    """

    assert not renpy.audio.music.playable(filename, "sound")
