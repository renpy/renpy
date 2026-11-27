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


"""Tests for Channel: parsing partial-playback audio specs such as ``<loop 1.0>music.ogg``, and seeking."""

import pytest

import renpy.audio.audio
from renpy.audio.audio import AudioData, Channel


@pytest.fixture
def channel():
    """A bare Channel with no file prefix or suffix, enough to call split_filename without audio set up."""

    channel = Channel.__new__(Channel)
    channel.file_prefix = ""
    channel.file_suffix = ""
    return channel


def test_loop_spec_on_audio_data(channel):
    """
    A ``<loop ...>`` spec on in-memory AudioData is parsed like one on a filename, and the result is
    still AudioData carrying the original bytes under the stripped name.

    The first play starts at 0; the looped play starts at the loop point and runs to the end (-1). The
    loop point 0.0005625 seconds is exactly 27 samples at 48 kHz, so the float comparison is exact.
    """

    data = b"audio data"
    filename = AudioData(data, "<loop 0.0005625>first.wav")

    first, start, _end, _volume = channel.split_filename(filename, False)
    assert start == 0.0

    loop, start, end, _volume = channel.split_filename(filename, True)
    assert start == 27 / 48000
    assert end == -1

    for split in (first, loop):
        assert isinstance(split, AudioData)
        assert str(split) == "first.wav"
        assert split.data == data


@pytest.mark.parametrize("depth", [0, 1])
def test_seek_marks_restarted_channel_playing(mocker, channel, depth):
    """
    A seek that leaves the backend with audio marks the channel as playing, so that a force-stop stops it.

    A seek can restart audio that played to its end, after which the channel had been marked as not playing, so
    muting a channel that stops on mute silenced the audio rather than stopping it. A seek on an idle channel leaves
    the channel as it was. The native backend is patched, since the test covers the channel's bookkeeping.
    """

    channel._number = 0
    channel.playing = False
    mocker.patch.object(renpy.audio.audio, "pcm_ok", True)
    mocker.patch.object(renpy.audio.audio.renpysound, "seek")
    mocker.patch.object(renpy.audio.audio.renpysound, "queue_depth", return_value=depth)

    channel.seek(0.25)

    assert channel.playing == (depth > 0)
