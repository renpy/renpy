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


"""
Tests for the renpysound channel queue: synchronized starts, queue replacement, and gapless handoff between clips.
"""

import os
import threading
import time

import pytest

from renpy.audio import renpysound

from .audio_harness import assert_gapless, wav

pytestmark = pytest.mark.skipif(
    os.name != "posix", reason="Native audio symbol inspection requires POSIX shared-library exports."
)


def test_immediate_queue_is_gapless(audio):
    """
    A queue issued before the first clip ends hands off with no silent samples.

    Both clips hold the same constant value, so the first and last of the 9600 output frames match.
    """

    audio.play()
    audio.queue()
    renpysound.periodic()
    output = audio.read(9600)
    assert_gapless(output)
    assert output[0] == output[-1]


def test_late_queue_is_gapless_without_periodic_at_handoff(audio):
    """
    A clip queued after playback has started hands off with no silent samples.

    The first clip is already audible when the queue is issued, and both clips hold the same constant value.
    """

    audio.play()
    renpysound.periodic()
    assert all(sample > 0 for sample in audio.read(2400))
    audio.queue()
    renpysound.periodic()
    output = audio.read(7200)
    assert_gapless(output)
    assert output[0] == output[-1]


def test_initial_sync_still_waits_for_periodic(audio):
    """
    A synchronized start stays silent until periodic() releases it, then plays normally.
    """

    audio.play()
    assert all(sample == 0 for sample in audio.read(256))
    renpysound.periodic()
    assert all(sample > 0 for sample in audio.read(4800))


def test_queue_after_natural_eof_starts_playback(audio):
    """
    A clip queued after the first clip has reached EOF starts playing once its synchronized start is released.

    The channel stays silent until periodic() runs, and the restarted clip then plays normally.
    """

    audio.play()
    renpysound.periodic()
    audio.read(4800)
    assert audio.read(256) == [0.0] * 256
    assert renpysound.get_state(0) == 3
    renpysound.queue(0, wav(), "second.wav", synchro_start=True, end=-1)
    audio.wait_ready(audio.channel.playing)
    assert audio.read(256) == [0.0] * 256
    renpysound.periodic()
    assert all(sample > 0 for sample in audio.read(4800))


def test_queue_on_idle_channel_preserves_initial_sync(audio):
    """
    Queuing onto an idle channel keeps the synchronized start: silent until periodic(), then gapless.
    """

    renpysound.queue(0, wav(), "first.wav", synchro_start=True, end=-1)
    audio.wait_ready(audio.channel.playing)
    assert audio.read(256) == [0.0] * 256
    renpysound.periodic()
    assert_gapless(audio.read(4800))


def test_queue_replacement_and_paused_handoff(audio):
    """
    Replacing the queued clip while paused keeps the handoff gapless and ends with the replacement's level.

    The replacement holds half the value of the original clip, so the final sample is half the first sample.
    """

    audio.play(tight=True)
    renpysound.periodic()
    audio.read(2400)
    audio.queue(tight=True)
    renpysound.queue(0, wav(value=5000), "replacement.wav", synchro_start=True, end=-1, tight=True)
    audio.wait_ready(audio.channel.queued)
    renpysound.pause(0)
    assert audio.read(256) == [0.0] * 256
    renpysound.unpause(0)
    output = audio.read(7200)
    assert_gapless(output)
    assert output[-1] == pytest.approx(output[0] / 2, abs=1e-7)
    assert renpysound.playing_name(0) == "replacement.wav"


def test_initial_channels_start_together(audio, request):
    """
    Two channels started with synchronized starts leave the hold together and report equal positions.

    The second channel is stopped by a finalizer, which runs before the audio fixture quits the mixer.
    """

    audio.play()
    renpysound.play(1, wav(value=5000), "other.wav", synchro_start=True, end=-1)
    request.addfinalizer(lambda: renpysound.stop(1))
    assert audio.read(256) == [0.0] * 256
    deadline = time.monotonic() + 5
    event = threading.Event()
    while True:
        renpysound.periodic()
        if not audio.channel.playing_synchro_start:
            break
        assert time.monotonic() < deadline, "Synchronized channels did not become ready."
        event.wait(0.001)
    output = audio.read(2400)
    assert_gapless(output)
    assert renpysound.get_pos(0) == renpysound.get_pos(1)


def test_tight_fadeout_spans_late_queue(audio):
    """
    A fadeout started while a tight clip is queued fades monotonically across the handoff, then stops in silence.
    """

    audio.play(tight=True)
    renpysound.periodic()
    audio.read(2400)
    audio.queue(tight=True)
    renpysound.fadeout(0, 0.15)
    output = audio.read(7200)
    assert_gapless(output)
    assert output[0] > output[2400]
    assert output[2400] > output[-1]
    assert audio.read(1) == [0.0]
