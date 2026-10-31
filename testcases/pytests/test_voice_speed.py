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


"""Voice speed preferences and request-time capture, without starting a game."""

import pickle
import shutil
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

import renpy
from renpy.audio.audio import Channel, QueueEntry
from renpy.exports.mediaexports import get_voice_speed, set_voice_speed
from renpy.preferences import Preferences, validate_voice_speed


@pytest.fixture
def preferences(mocker):
    """Use isolated player preferences; restore engine globals after each test."""
    preferences = Preferences()
    mocker.patch.object(renpy.game, "preferences", preferences)
    return preferences


@pytest.mark.parametrize("speed", [0.5, 1, 1.5, 2, 3])
def test_voice_speed_preference(preferences, speed):
    """The public getter and setter expose the selected speed on native and Web backends alike."""
    set_voice_speed(speed)
    assert preferences.voice_speed == float(speed)
    assert get_voice_speed() == speed


@pytest.mark.parametrize("speed", [True, False, None, "1.5", object()])
def test_voice_speed_rejects_non_numbers(preferences, speed):
    """Booleans and coercible strings must not silently become playback speeds."""
    with pytest.raises(TypeError):
        set_voice_speed(speed)
    assert get_voice_speed() == 1.0


@pytest.mark.parametrize("speed", [0, -1, 0.49, 3.01, float("nan"), float("inf"), 10**1000])
def test_voice_speed_rejects_out_of_range(preferences, speed):
    """Range checks also reject non-finite values and integers too large to convert to float."""
    with pytest.raises(ValueError):
        validate_voice_speed(speed)
    assert get_voice_speed() == 1.0


@pytest.mark.parametrize("speed", [True, None, 0, float("nan"), float("inf")])
def test_invalid_persistent_speed_is_repaired(preferences, speed):
    """Bad persisted values are repaired during preference validation, before audio uses them."""
    preferences.voice_speed = speed
    assert preferences.check() is not None
    assert preferences.voice_speed == 1.0


def test_old_preferences_and_queue_entries_load_at_normal_speed(preferences):
    """Pickles without the new attributes retain normal-speed defaults after loading."""
    preferences.__dict__.pop("voice_speed", None)
    assert pickle.loads(pickle.dumps(preferences)).voice_speed == 1.0
    entry = QueueEntry("old.ogg", 0, False, False, 1.0, None)
    del entry.playback_speed
    assert pickle.loads(pickle.dumps(entry)).playback_speed == 1.0


@pytest.mark.parametrize(("name", "movie", "expected"), [("voice", False, 2.0), (2, False, 2.0), ("music", False, 1.0), ("custom", False, 1.0), ("voice", True, 1.0)])
def test_speed_is_captured_per_request(preferences, mocker, name, movie, expected):
    """Changing the preference leaves already queued files unchanged and affects only the voice channel."""
    mocker.patch.object(renpy.game, "context", return_value=SimpleNamespace(music={name: SimpleNamespace(audio_filter=None)}))
    mocker.patch.object(renpy.exports, "is_seen_allowed", return_value=False)
    channel = Channel(name, False, False, False, "", "", True, movie, True, False, False)
    # The real default voice is numeric channel 2, aliased as "voice".
    mocker.patch.dict(renpy.audio.audio.channels, {"voice": channel if name in ("voice", 2) else object()})
    set_voice_speed(2.0)
    channel.enqueue(["first.ogg", "second.ogg"], loop=False)
    set_voice_speed(0.5)
    channel.enqueue(["third.ogg"], loop=False)
    assert [entry.playback_speed for entry in channel.queue] == [expected, expected, 0.5 if expected == 2.0 else 1.0]


def test_browser_voice_speed():
    """Run Web Audio PCM and lifecycle regressions in Node; skip when the optional JS runner is absent."""
    node = shutil.which("node")
    if node is None:
        pytest.skip("Web Audio backend tests require Node.js.")
    subprocess.run([node, "--test", str(Path(__file__).with_name("test_voice_speed_web.js"))], check=True)
