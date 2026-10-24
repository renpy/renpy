import ctypes
import io
import math
import os
import struct
import threading
import time
import wave
from pathlib import Path

import pytest

from renpy.audio import renpysound


class ChannelHead(ctypes.Structure):
    # Only the prefix of src/renpysound_core.c's Channel, for channel zero.
    _fields_ = [
        ("state", ctypes.c_int),
        ("playing", ctypes.c_void_p),
        ("playing_name", ctypes.c_void_p),
        ("playing_fadein", ctypes.c_int),
        ("playing_tight", ctypes.c_int),
        ("playing_start_ms", ctypes.c_int),
        ("playing_relative_volume", ctypes.c_float),
        ("playing_synchro_start", ctypes.c_int),
        ("playing_pad", ctypes.c_int),
        ("playing_audio_filter", ctypes.c_void_p),
        ("queued", ctypes.c_void_p),
    ]


class MediaHead(ctypes.Structure):
    # Prefix of src/ffmedia.c's MediaState, inspected while holding its lock.
    _fields_ = [
        ("next", ctypes.c_void_p),
        ("thread", ctypes.c_void_p),
        ("cond", ctypes.c_void_p),
        ("lock", ctypes.c_void_p),
        ("rwops", ctypes.c_void_p),
        ("filename", ctypes.c_void_p),
        ("want_video", ctypes.c_int),
        ("ready", ctypes.c_int),
        ("needs_decode", ctypes.c_int),
        ("quit", ctypes.c_int),
        ("skip", ctypes.c_double),
        ("seek_requested", ctypes.c_int),
        ("seek_target", ctypes.c_double),
        ("audio_finished", ctypes.c_int),
        ("video_finished", ctypes.c_int),
        ("video_stream", ctypes.c_int),
        ("audio_stream", ctypes.c_int),
        ("ctx", ctypes.c_void_p),
        ("video_context", ctypes.c_void_p),
        ("audio_context", ctypes.c_void_p),
        ("video_packets_first", ctypes.c_void_p),
        ("video_packets_last", ctypes.c_void_p),
        ("audio_packets_first", ctypes.c_void_p),
        ("audio_packets_last", ctypes.c_void_p),
        ("total_duration", ctypes.c_double),
        ("end_time", ctypes.c_double),
        ("audio_frames_first", ctypes.c_void_p),
        ("audio_frames_last", ctypes.c_void_p),
        ("audio_queue_samples", ctypes.c_int),
    ]


pytestmark = pytest.mark.skipif(
    os.name != "posix", reason="Native audio symbol inspection requires POSIX shared-library exports."
)


def wav(samples=4800, value=10000, ramp=False):
    """
    Build an in-memory 48 kHz stereo 16-bit WAV clip.

    A constant clip repeats `value` in every frame. A ramp clip uses value + frame index, which makes each sample's
    position recognizable in the output. Both forms are used to check where playback starts and ends.
    """

    data = io.BytesIO()
    with wave.open(data, "wb") as output:
        output.setparams((2, 2, 48000, 0, "NONE", "not compressed"))
        if ramp:
            output.writeframes(b"".join(struct.pack("<hh", value + i, value + i) for i in range(samples)))
        else:
            output.writeframes(struct.pack("<hh", value, value) * samples)
    return io.BytesIO(data.getvalue())


def assert_gapless(output):
    """
    Assert that no sample in `output` is exactly zero, meaning the queue handoff inserted no silence.

    Silence is detected as exact zero, which a continuous nonzero signal never produces at a handoff.
    """

    assert sum(sample == 0 for sample in output) == 0, "Inserted silent samples at the queue handoff."


def opus():
    """
    Return the bytes of the 0.1 s stereo 440 Hz Opus tone shipped in pytests/audio/tone.opus.

    The file is 4800 frames long at 48 kHz, and the tests use it to check codec padding and EOF behavior.
    """

    # Generated from a stereo 440 Hz, 0.1 s sine at 48 kHz using FFmpeg/libopus.
    return io.BytesIO((Path(__file__).parent / "audio" / "tone.opus").read_bytes())


def seek_opus():
    """
    Return the bytes of the 3 s seek fixture in pytests/audio/seek.opus.

    The fixture is noise mixed with a quiet 440 Hz tone, so any misplaced seek shows up as a waveform mismatch.
    """

    # ffmpeg -f lavfi -i 'anoisesrc=sample_rate=48000:duration=3:seed=7407:amplitude=0.2' \
    #   -f lavfi -i 'sine=frequency=440:sample_rate=48000:duration=3' \
    #   -filter_complex '[1:a]volume=0.1[tone];[0:a][tone]amix=inputs=2:normalize=0' \
    #   -c:a libopus -b:a 64000 -page_duration 20000 -fflags +bitexact -flags:a +bitexact seek.opus
    return io.BytesIO((Path(__file__).parent / "audio" / "seek.opus").read_bytes())


class AudioHarness:
    """
    Wraps the renpysound module and the native SDL and ffmedia symbols the audio tests inspect.

    The shared library is loaded from renpysound.__file__ so the SDL audio stream and the channel table can be read
    directly. Construction only binds signatures; initialize() opens the mixer.
    """

    def __init__(self):
        """
        Load renpysound's shared library and bind the native SDL and ffmedia symbols the tests use.

        Binding only sets signatures. The mixer is not opened until initialize() runs.
        """

        self.native = ctypes.CDLL(renpysound.__file__)
        self.bind("SDL_GetHint", ctypes.c_char_p, ctypes.c_char_p)
        self.bind("SDL_SetHint", ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p)
        self.bind("SDL_ResetHint", ctypes.c_bool, ctypes.c_char_p)
        self.bind("SDL_PauseAudioStreamDevice", ctypes.c_bool, ctypes.c_void_p)
        self.bind("SDL_ClearAudioStream", ctypes.c_bool, ctypes.c_void_p)
        self.bind("SDL_GetAudioStreamData", ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int)
        self.bind("SDL_GetError", ctypes.c_char_p)
        self.bind("media_is_ready", ctypes.c_int, ctypes.c_void_p)
        self.bind("SDL_LockMutex", None, ctypes.c_void_p)
        self.bind("SDL_UnlockMutex", None, ctypes.c_void_p)

    def initialize(self, rate=48000):
        """
        Open the renpysound mixer at `rate` Hz, stereo, with a 256-sample buffer, then pause and clear its stream.

        The stream starts paused and empty, so each test decides when audio begins to be read.
        """

        renpysound.init(rate, 2, 256)
        self.stream = ctypes.c_void_p.in_dll(self.native, "audio_stream")
        assert self.native.SDL_PauseAudioStreamDevice(self.stream), self.native.SDL_GetError()
        assert self.native.SDL_ClearAudioStream(self.stream), self.native.SDL_GetError()

    def bind(self, name, result, *arguments):
        """
        Set the ctypes restype and argtypes of a native symbol and return the bound function.

        Explicit signatures keep pointer and boolean return values from being truncated to int.
        """

        function = getattr(self.native, name)
        function.restype = result
        function.argtypes = arguments
        return function

    @property
    def channel(self):
        """
        Return a live view of renpysound's channel 0 state, read directly from native memory.

        The view reflects the channel at the time of access, so tests can inspect the playing and queued media
        pointers without going through the Python API.
        """

        address = ctypes.c_void_p.in_dll(self.native, "channels")
        return ctypes.cast(address, ctypes.POINTER(ChannelHead)).contents

    def wait_ready(self, media):
        """
        Poll until the decoder for `media` reports ready, failing if that takes longer than five seconds.

        Polling sleeps on an Event wait so the decoder thread can make progress between checks.
        """

        deadline = time.monotonic() + 5
        event = threading.Event()
        while not self.native.media_is_ready(media):
            assert time.monotonic() < deadline, "Audio decoder did not become ready."
            event.wait(0.001)

    def read(self, samples):
        """
        Read `samples` stereo frames from the SDL stream and return the left channel as floats.

        Asserts that SDL returned the full requested byte count. Interleaved output is sliced with [::2], so only
        the left channel is returned.
        """

        output = (ctypes.c_float * (samples * 2))()
        size = ctypes.sizeof(output)
        got = self.native.SDL_GetAudioStreamData(self.stream, output, size)
        assert got == size, self.native.SDL_GetError()
        return list(output)[::2]

    def play(self, **kwargs):
        """
        Start the first clip on channel 0 with a synchronized start, then wait until its decoder is ready.

        Extra keyword arguments pass through to renpysound.play, for example tight=True.
        """

        renpysound.play(0, wav(), "first.wav", synchro_start=True, end=-1, **kwargs)
        self.wait_ready(self.channel.playing)

    def queue(self, **kwargs):
        """
        Queue the second clip behind channel 0 with a synchronized start, then wait until its decoder is ready.

        Extra keyword arguments pass through to renpysound.queue.
        """

        renpysound.queue(0, wav(), "second.wav", synchro_start=True, end=-1, **kwargs)
        self.wait_ready(self.channel.queued)


@pytest.fixture
def audio():
    """
    Provide an AudioHarness with SDL's dummy audio driver and an initialized renpysound mixer.

    The SDL_AUDIO_DRIVER hint is restored after the test, and renpysound.quit() runs before the restore.
    """

    harness = AudioHarness()
    hint = b"SDL_AUDIO_DRIVER"
    original = harness.native.SDL_GetHint(hint)
    assert harness.native.SDL_SetHint(hint, b"dummy")
    try:
        harness.initialize()
        try:
            yield harness
        finally:
            renpysound.quit()
    finally:
        if original is None:
            harness.native.SDL_ResetHint(hint)
        else:
            harness.native.SDL_SetHint(hint, original)


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
