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
natural clip durations, and the state of a movie channel that has played to its end.
"""

import io
import os
import threading
import time
from pathlib import Path

import pytest

import renpy.pygame
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


@pytest.fixture
def video_channel():
    """
    Mark channel 0 as a video channel for the test, and restore it to an audio-only channel afterwards.

    The video decoder converts frames to the format of the sample surfaces, which the display normally provides at
    startup; without a display, the test provides RGBA surfaces itself. The audio fixture's teardown doesn't reset the
    video flag, so leaving it set would make later tests on channel 0 decode as video.
    """

    masks = (0xFF, 0xFF00, 0xFF0000, 0xFF000000)
    rgba = renpy.pygame.Surface((10, 10), 0, 32, masks)
    rgb = renpy.pygame.Surface((10, 10), 0, 32, masks[:3] + (0,))
    renpysound.sample_surfaces(rgb, rgba)

    renpysound.set_video(0, renpysound.NODROP_VIDEO)
    yield
    renpysound.stop(0)
    renpysound.set_video(0, renpysound.NO_VIDEO)


def test_ended_movie_reports_video_ready(audio, video_channel):
    """
    A movie channel that has played to its end reports a frame as ready, so it doesn't hold back other movies.

    The display only redraws movies when every movie channel is ready, so an ended movie that reported not ready kept
    every other movie on screen at about 10 frames per second (#7561). The movie is the tutorial's webm (VP8 and
    Vorbis), cut to 0.3 seconds so reading its audio reaches the end quickly. The mixer is driven by reading its
    output, so the loop reads until the channel reports that it ended. The display reads every frame it is offered, so
    the test does the same: the queue of decoded frames is drained before checking readiness, because a frame still
    waiting in the queue would make the channel ready regardless.
    """

    movie = Path(__file__).parents[2] / "tutorial" / "game" / "oa4_launch.webm"
    if not movie.exists():
        pytest.fail(f"Missing movie fixture {movie}.")

    renpysound.play(0, io.BytesIO(movie.read_bytes()), "movie.webm", synchro_start=True, end=0.3)
    audio.wait_ready(audio.channel.playing)
    renpysound.periodic()

    deadline = time.monotonic() + 5
    event = threading.Event()
    while renpysound.get_state(0) != 3:
        assert time.monotonic() < deadline, "The movie did not reach its end."
        audio.read(480)
        renpysound.advance_time()
        renpysound.read_video(0)
        event.wait(0.001)

    deadline = time.monotonic() + 5
    while True:
        renpysound.advance_time()
        if renpysound.read_video(0) is None:
            break
        assert time.monotonic() < deadline, "The movie's frames were not drained."

    assert renpysound.video_ready(0)
