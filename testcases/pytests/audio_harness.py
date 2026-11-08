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
Shared harness for the renpysound tests (test_audio_renpysound_*.py).

It wraps the native SDL and ffmedia symbols that the tests inspect through ctypes, and builds the in-memory
clips they play. The ``audio`` fixture that opens the mixer around it lives in conftest.py.
"""

import ctypes
import io
import struct
import threading
import time
import wave

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
