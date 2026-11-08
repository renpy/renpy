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


"""Tests for renpy.audio.music.playable, which finds files in the directories that config.audio_directories adds."""

from types import SimpleNamespace

import pytest

import renpy
from renpy import loader
from renpy.audio.audio import Channel


@pytest.fixture(autouse=True)
def loader_config(mocker):
    """
    Gives the tests a known search path and no language, the same as the loader tests do. search_prefixes is
    reduced to the game directory, so the only directories searched are the mapped and configured audio ones.
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
