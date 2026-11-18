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
Tests for renpysound's partial playback: sample-aligned start and end positions, rounding to whole samples,
and natural clip durations.
"""

import os

import pytest

from renpy.audio import renpysound

from .audio_harness import assert_gapless, wav

pytestmark = pytest.mark.skipif(
    os.name != "posix", reason="Native audio symbol inspection requires POSIX shared-library exports."
)


@pytest.mark.parametrize(("start", "end"), [(27, 4800), (49, 101), (61, 115)])
def test_sample_aligned_partial_playback(audio, start, end):
    """
    Playing a sample-aligned range returns exactly the reference samples for that range, then silence.

    The reference is the full ramp clip, so each frame's value identifies its position in the clip.
    """

    renpysound.play(0, wav(ramp=True), "ramp.wav", synchro_start=True, end=-1)
    audio.wait_ready(audio.channel.playing)
    renpysound.periodic()
    reference = audio.read(4800)
    renpysound.play(0, wav(ramp=True), "ramp.wav", synchro_start=True, start=start / 48000, end=end / 48000)
    audio.wait_ready(audio.channel.playing)
    renpysound.periodic()
    assert audio.read(end - start) == reference[start:end]
    assert audio.read(1) == [0.0]


def test_subsample_positions_round_to_nearest_sample(audio):
    """
    Start and end positions between frames round to the nearest frame, matching an integer-frame range.

    A start of 27.75 frames rounds to frame 28 and an end of 49.75 frames rounds to frame 50.
    """

    renpysound.play(0, wav(ramp=True), "ramp.wav", synchro_start=True, end=-1)
    audio.wait_ready(audio.channel.playing)
    renpysound.periodic()
    reference = audio.read(4800)
    renpysound.play(0, wav(ramp=True), "ramp.wav", synchro_start=True, start=27.75 / 48000, end=49.75 / 48000)
    audio.wait_ready(audio.channel.playing)
    renpysound.periodic()
    assert audio.read(22) == reference[28:50]
    assert audio.read(1) == [0.0]


@pytest.mark.parametrize("samples", [27, 49, 61, 101])
def test_natural_duration_rounds_to_whole_samples(audio, samples):
    """
    A clip whose natural length is a whole number of frames plays exactly those frames, with no silence before the end.
    """

    renpysound.play(0, wav(samples=samples), "short.wav", synchro_start=True, end=-1)
    audio.wait_ready(audio.channel.playing)
    renpysound.periodic()
    assert_gapless(audio.read(samples))
    assert audio.read(1) == [0.0]
