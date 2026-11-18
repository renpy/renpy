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
Tests for renpysound's Opus handling: seeking, looping, resampling, codec-delay padding, and EOF behavior.
"""

import ctypes
import io
import math
import os
import threading
import time
from pathlib import Path

import pytest

from renpy.audio import renpysound

from .audio_harness import MediaHead

pytestmark = pytest.mark.skipif(
    os.name != "posix", reason="Native audio symbol inspection requires POSIX shared-library exports."
)


# -----------------------------------------------------------------------------
# Fixtures and helpers
# -----------------------------------------------------------------------------


def opus():
    """
    Return the bytes of the 0.1 s stereo 440 Hz Opus tone shipped in testcases/pytests/audio/tone.opus.

    The file is 4800 frames long at 48 kHz, and the tests use it to check codec padding and EOF behavior.
    """

    # Generated from a stereo 440 Hz, 0.1 s sine at 48 kHz using FFmpeg/libopus.
    return io.BytesIO((Path(__file__).parent / "audio" / "tone.opus").read_bytes())


def seek_opus():
    """
    Return the bytes of the 3 s seek fixture in testcases/pytests/audio/seek.opus.

    The fixture is noise mixed with a quiet 440 Hz tone, so any misplaced seek shows up as a waveform mismatch.
    """

    # ffmpeg -f lavfi -i 'anoisesrc=sample_rate=48000:duration=3:seed=7407:amplitude=0.2' \
    #   -f lavfi -i 'sine=frequency=440:sample_rate=48000:duration=3' \
    #   -filter_complex '[1:a]volume=0.1[tone];[0:a][tone]amix=inputs=2:normalize=0' \
    #   -c:a libopus -b:a 64000 -page_duration 20000 -fflags +bitexact -flags:a +bitexact seek.opus
    return io.BytesIO((Path(__file__).parent / "audio" / "seek.opus").read_bytes())


def read_chunks(audio, samples):
    """
    Read `samples` frames in 960-frame chunks, waiting for the decoder to buffer each chunk before reading it.

    Chunked reads keep SDL from being asked for more audio than the decoder has produced so far.
    """

    output = []
    while samples:
        count = min(samples, 960)
        wait_audio_buffered(audio, count)
        output.extend(audio.read(count))
        samples -= count
    return output


def wait_audio_buffered(audio, samples):
    """
    Poll until the playing and queued decoders together hold at least `samples` buffered frames.

    Each decoder's audio_queue_samples is read while holding its lock. Fails after five seconds.
    """

    deadline = time.monotonic() + 5
    event = threading.Event()

    while True:
        channel = audio.channel
        buffered = 0

        for address in (channel.playing, channel.queued):
            if address:
                media = ctypes.cast(address, ctypes.POINTER(MediaHead)).contents
                audio.native.SDL_LockMutex(media.lock)
                try:
                    buffered += media.audio_queue_samples
                finally:
                    audio.native.SDL_UnlockMutex(media.lock)

        if buffered >= samples:
            return

        assert time.monotonic() < deadline, "Audio decoder did not buffer enough samples."
        event.wait(0.001)


def seek_opus_reference(audio, rate=48000):
    """
    Decode the 3 s seek fixture continuously at `rate` and return its left channel as the reference waveform.

    Seek and loop tests compare their output against this continuous decode, so a misplaced seek shows as a mismatch.
    """

    renpysound.play(0, seek_opus(), "seek.opus", synchro_start=True, end=-1)
    audio.wait_ready(audio.channel.playing)
    renpysound.periodic()
    reference = read_chunks(audio, 3 * rate)
    assert audio.read(1) == [0.0]
    return reference


def assert_opus_matches(output, reference, start, rate=48000):
    """
    Assert that `output` is the continuous decode of `reference` beginning at frame `start`.

    The best-matching alignment within 400 frames of `start` must be zero. Each window (0-20 ms, 20-50 ms,
    50-100 ms) must have a relative error of at most 1%, which shows the decoder has warmed up.
    """

    probe = output[-512:]
    probe_start = start + len(output) - len(probe)
    offsets = range(max(-400, -probe_start), min(400, len(reference) - probe_start - len(probe)) + 1)
    offset = min(
        offsets,
        key=lambda shift: sum(
            (a - b) ** 2 for a, b in zip(probe, reference[probe_start + shift : probe_start + shift + len(probe)])
        ),
    )
    assert offset == 0, "Opus playback is displaced from the requested sample."
    for begin, end in [(0, 20), (20, 50), (50, 100)]:
        lo, hi = round(begin * rate / 1000), min(round(end * rate / 1000), len(output))
        if lo >= hi:
            continue
        expected = reference[start + lo : start + hi]
        power = sum(sample**2 for sample in expected)
        assert power > 0
        error = math.sqrt(sum((a - b) ** 2 for a, b in zip(output[lo:hi], expected)) / power)
        assert error <= 0.01, f"Opus decoder has not warmed up at {begin}-{end} ms."


def wait_seek(audio, position):
    """
    Poll until the playing decoder has finished seeking to `position` seconds and buffered at least 960 frames.

    The decoder state is read while holding its lock. Fails after five seconds.
    """

    media = ctypes.cast(audio.channel.playing, ctypes.POINTER(MediaHead)).contents
    deadline = time.monotonic() + 5
    event = threading.Event()
    while True:
        audio.native.SDL_LockMutex(media.lock)
        try:
            ready = not media.seek_requested and media.skip == position and media.audio_queue_samples >= 960
        finally:
            audio.native.SDL_UnlockMutex(media.lock)
        if ready:
            return
        assert time.monotonic() < deadline, "Audio seek did not finish decoding."
        event.wait(0.001)


# -----------------------------------------------------------------------------
# Seeking and looping
# -----------------------------------------------------------------------------


@pytest.mark.parametrize("start", [0, 27, 2400, 47999, 48000, 48312, 96000, 141600])
def test_opus_interior_loop_matches_continuous_decode(audio, start):
    """
    A queued loop starting at an interior frame of the Opus clip matches the continuous decode from that frame.

    The first clip is decoded from the start and checked against the reference, then the loop's output must align
    with the reference at `start` after decoder warm-up.
    """

    reference = seek_opus_reference(audio)
    renpysound.play(0, seek_opus(), "seek.opus", synchro_start=True, end=-1)
    audio.wait_ready(audio.channel.playing)
    renpysound.queue(0, seek_opus(), "loop.opus", start=start / 48000, end=-1)
    audio.wait_ready(audio.channel.queued)
    renpysound.periodic()
    assert read_chunks(audio, 144000) == reference
    output = read_chunks(audio, 144000 - start)
    assert_opus_matches(output, reference, start)
    assert audio.read(1) == [0.0]


def test_opus_resampled_interior_start_matches_continuous_decode(audio):
    """
    At 44.1 kHz, a 1.0 s start into the Opus clip matches the continuous decode from that frame.

    The mixer is reopened at 44.1 kHz before decoding, so the check covers the resampling path as well.
    """

    renpysound.quit()
    audio.initialize(44100)
    reference = seek_opus_reference(audio, 44100)
    renpysound.play(0, seek_opus(), "seek.opus", synchro_start=True, start=1.0, end=1.2)
    audio.wait_ready(audio.channel.playing)
    renpysound.periodic()
    assert_opus_matches(read_chunks(audio, 8820), reference, 44100, 44100)
    assert audio.read(1) == [0.0]


def test_opus_runtime_seeks_match_continuous_decode(audio):
    """
    Seeking a playing Opus clip to several positions, in sequence, reproduces the continuous decode from each one.

    The positions are a plain loop rather than parametrized cases, because each seek depends on the decoder state
    left by the previous one, and the sequence exercises backward and forward seeks in a single run.
    """

    reference = seek_opus_reference(audio)
    renpysound.play(0, seek_opus(), "seek.opus", synchro_start=True, end=-1)
    audio.wait_ready(audio.channel.playing)
    renpysound.periodic()
    for position in [1.0, 0.05, 2.0, 0.0, 2.9]:
        renpysound.pause(0)
        renpysound.seek(0, position)
        wait_seek(audio, position)
        assert audio.native.SDL_ClearAudioStream(audio.stream), audio.native.SDL_GetError()
        renpysound.unpause(0)
        start = round(position * 48000)
        output = read_chunks(audio, min(9600, 144000 - start))
        assert_opus_matches(output, reference, start)


# -----------------------------------------------------------------------------
# Codec padding and end of file
# -----------------------------------------------------------------------------


@pytest.mark.parametrize("start", [0, 27, 49])
def test_opus_loop_has_no_codec_delay_padding(audio, start):
    """
    A loop starting at a frame offset into the Opus clip plays the clip with no codec-delay padding at the seam.

    The first 4800 frames equal the clip's own decode, and the loop's remainder equals the clip from `start` onward.
    """

    renpysound.play(0, opus(), "tone.opus", synchro_start=True, end=-1)
    audio.wait_ready(audio.channel.playing)
    renpysound.periodic()
    reference = audio.read(4800)
    renpysound.play(0, opus(), "tone.opus", synchro_start=True, end=-1)
    audio.wait_ready(audio.channel.playing)
    renpysound.queue(0, opus(), "loop.opus", start=start / 48000, end=-1)
    audio.wait_ready(audio.channel.queued)
    renpysound.periodic()
    output = audio.read(9600 - start)
    assert output[:4800] == reference
    assert output[4800:] == reference[start:]
    assert audio.read(1) == [0.0]


def test_resampled_opus_drains_audio_at_eof(audio):
    """
    At 44.1 kHz, the Opus clip plays to its end and the queued copy follows without a gap.

    The last frame of the first copy is audible, so the clip is not cut short before EOF.
    """

    renpysound.quit()
    audio.initialize(44100)
    renpysound.play(0, opus(), "tone.opus", synchro_start=True, end=-1)
    audio.wait_ready(audio.channel.playing)
    renpysound.queue(0, opus(), "loop.opus", end=-1)
    audio.wait_ready(audio.channel.queued)
    renpysound.periodic()
    output = audio.read(8820)
    assert output[:4410] == output[4410:]
    assert output[4409] != 0.0
    assert audio.read(1) == [0.0]


def test_explicit_end_preserves_requested_padding(audio):
    """
    An explicit end of 0.11 s keeps the padding after the 4800-frame clip: its last frame is audible, then 480 silent frames.
    """

    renpysound.play(0, opus(), "tone.opus", synchro_start=True, end=0.11)
    audio.wait_ready(audio.channel.playing)
    renpysound.periodic()
    output = audio.read(5280)
    assert output[4799] != 0.0
    assert output[4800:] == [0.0] * 480
    assert audio.read(1) == [0.0]


def test_movie_preserves_container_duration_padding(audio):
    """
    Playing the Opus clip as a movie keeps the container's duration padding: 312 silent frames follow the clip.

    The clip's last frame is audible before the padding starts.
    """

    renpysound.set_video(0, renpysound.NODROP_VIDEO)
    renpysound.play(0, opus(), "tone.opus", synchro_start=True, end=-1)
    audio.wait_ready(audio.channel.playing)
    renpysound.periodic()
    output = audio.read(5112)
    assert output[4799] != 0.0
    assert output[4800:] == [0.0] * 312
    assert audio.read(1) == [0.0]
