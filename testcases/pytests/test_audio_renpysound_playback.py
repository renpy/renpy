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
Tests for renpysound's playback: sample-aligned start and end positions, rounding to whole samples, natural clip
durations, seeking after a clip has played to its end, and reading video frames.
"""

import faulthandler
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


# -----------------------------------------------------------------------------
# Partial playback
# -----------------------------------------------------------------------------


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


# -----------------------------------------------------------------------------
# Seeking after the end
# -----------------------------------------------------------------------------


def read_until_ended(audio):
    """
    Read the mixer's output in 480-frame chunks until channel 0 reports that its clip ended, and return the output.

    Fails after five seconds.
    """

    output = []
    deadline = time.monotonic() + 5
    while audio.state != "ended":
        assert time.monotonic() < deadline, "The clip did not reach its end."
        output.extend(audio.read(480))
    return output


@pytest.mark.parametrize("paused", [False, True])
def test_seek_after_end_plays_from_new_position(audio, paused):
    """
    Seeking a clip that has played to its end plays it again from the new position, and it then ends again.

    The decoder's lock is held while seeking, so the decode thread can't start the seek, which makes the window
    before the seek is carried out deterministic. SDL mutexes are recursive, so this thread can still seek and mix.
    In that window the finished decoder has no audio, which the mixer used to take as the end of the clip again,
    leaving the channel ended. A paused channel used to stay ended as well, losing the seek. The ramp clip makes
    each frame's value identify its position, so the output after the seek must match the clip from frame 2400. A
    WAV's packets carry no timestamps, so this also checks that the seek isn't taken to start at frame 0, which used
    to play the clip from twice the requested position.
    """

    renpysound.play(0, wav(ramp=True), "ramp.wav", synchro_start=True, end=-1)
    audio.wait_ready(audio.channel.playing)
    renpysound.periodic()
    reference = read_until_ended(audio)[:4800]

    media = audio.media(audio.channel.playing)
    audio.native.SDL_LockMutex(media.lock)
    try:
        if paused:
            renpysound.pause(0)

        renpysound.seek(0, 2400 / 48000)

        if paused:
            assert audio.state == "paused"
            renpysound.unpause(0)

        assert audio.read(480) == [0.0] * 480
        assert audio.state == "playing"
    finally:
        audio.native.SDL_UnlockMutex(media.lock)

    audio.wait_seek(2400 / 48000)
    assert audio.read(2400) == reference[2400:]
    read_until_ended(audio)


def test_fadeout_finishes_during_seek(audio):
    """
    A fadeout that runs out while a seek is in progress still stops the clip on time.

    The decoder's lock is held so the seek can't finish, as in the test above. While it waits, the mixer has no audio
    from the channel, but the fadeout must keep counting down rather than wait for the seek.
    """

    renpysound.play(0, wav(samples=9600), "clip.wav", synchro_start=True, end=-1)
    audio.wait_ready(audio.channel.playing)
    renpysound.periodic()
    audio.read(480)

    media = audio.media(audio.channel.playing)
    audio.native.SDL_LockMutex(media.lock)
    try:
        renpysound.seek(0, 0.1)
        renpysound.fadeout(0, 0.02)
        assert audio.read(1440) == [0.0] * 1440
        assert audio.state == "idle"
    finally:
        audio.native.SDL_UnlockMutex(media.lock)


# -----------------------------------------------------------------------------
# Video
# -----------------------------------------------------------------------------


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


def movie_bytes():
    """
    Return the bytes of the tutorial's webm (VP8 and Vorbis), used as the test movie.
    """

    movie = Path(__file__).parents[2] / "tutorial" / "game" / "oa4_launch.webm"
    if not movie.exists():
        pytest.fail(f"Missing movie fixture {movie}.")

    return movie.read_bytes()


# The two ways of reading a frame, and whether the channel offers YUV frames to each.
READERS = [
    pytest.param(renpysound.read_video, False, id="read_video"),
    pytest.param(renpysound.read_video_yuv, True, id="read_video_yuv"),
]


@pytest.mark.usefixtures("video_channel")
@pytest.mark.parametrize(("reader", "yuv"), READERS)
def test_ended_movie_reports_video_ready(audio, reader, yuv):
    """
    A movie channel that has played to its end reports a frame as ready, so it doesn't hold back other movies.

    The display only redraws movies when every movie channel is ready, so an ended movie that reported not ready kept
    every other movie on screen at about 10 frames per second (#7561). The movie is the tutorial's webm (VP8 and
    Vorbis), cut to 0.3 seconds so reading its audio reaches the end quickly. The mixer is driven by reading its
    output, so the loop reads until the channel reports that it ended. The display reads every frame it is offered, so
    the test does the same: the queue of decoded frames is drained before checking readiness, because a frame still
    waiting in the queue would make the channel ready regardless. Both readers are covered, the YUV one with YUV
    frames enabled, since that is when the display uses it.
    """

    renpysound.set_video(0, renpysound.NODROP_VIDEO, yuv=yuv)
    renpysound.play(0, io.BytesIO(movie_bytes()), "movie.webm", synchro_start=True, end=0.3)
    audio.wait_ready(audio.channel.playing)
    renpysound.periodic()

    deadline = time.monotonic() + 5
    event = threading.Event()
    while audio.state != "ended":
        assert time.monotonic() < deadline, "The movie did not reach its end."
        audio.read(480)
        renpysound.advance_time()
        reader(0)
        event.wait(0.001)

    deadline = time.monotonic() + 5
    while True:
        renpysound.advance_time()
        if reader(0) is None:
            break
        assert time.monotonic() < deadline, "The movie's frames were not drained."

    assert renpysound.video_ready(0)


class GatedFile(io.BytesIO):
    """
    An in-memory file whose reads wait until `gate` is set, which keeps a decoder reading it from becoming ready.

    It is a file-like object rather than a buffer, so the decoder reads it through Python, which needs the GIL.
    """

    def __init__(self, data, gate):
        super().__init__(data)
        self.gate = gate

    def read(self, *args):
        self.gate.wait()
        return super().read(*args)

    def readinto(self, buffer):
        self.gate.wait()
        return super().readinto(buffer)


@pytest.mark.usefixtures("video_channel")
@pytest.mark.parametrize(("reader", "yuv"), READERS)
def test_video_read_before_decoder_ready_returns_no_frame(audio, reader, yuv):
    """
    Reading a frame before the movie's decoder is ready returns no frame at once, and frames arrive once it is ready.

    Frame reads hold the GIL, so that the periodic thread can't close the stream during a read. A read that waited
    for the decoder would stall the display, and would deadlock with a decoder reading a Python file, which needs the
    GIL. The decoder here can't read its file until the gate is set. A timer sets it after three seconds, so a read
    that waits with the GIL released fails the timing check rather than hanging the test run. A read that waits while
    keeping the GIL would deadlock, so a watchdog ends the run with a traceback.
    """

    gate = threading.Event()
    timer = threading.Timer(3, gate.set)
    timer.start()

    try:
        renpysound.set_video(0, renpysound.NODROP_VIDEO, yuv=yuv)
        renpysound.play(0, GatedFile(movie_bytes(), gate), "movie.webm", synchro_start=True, end=0.3)
        renpysound.advance_time()

        # A read that waits while keeping the GIL would deadlock with the decoder and stop the timer from setting the
        # gate, so a watchdog that doesn't need the GIL ends the run with a traceback instead.
        faulthandler.dump_traceback_later(10, exit=True)
        try:
            started = time.monotonic()
            assert reader(0) is None
            assert time.monotonic() - started < 1
        finally:
            faulthandler.cancel_dump_traceback_later()

        gate.set()
        audio.wait_ready(audio.channel.playing)
        renpysound.periodic()

        deadline = time.monotonic() + 5
        event = threading.Event()
        while True:
            renpysound.advance_time()
            if reader(0) is not None:
                break
            assert time.monotonic() < deadline, "The movie produced no frame."
            audio.read(480)
            event.wait(0.001)

    finally:
        gate.set()
        timer.cancel()
