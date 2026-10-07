import ctypes
import io
import math
import os
import struct
import threading
import time
import unittest
import wave
from pathlib import Path

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


@unittest.skipUnless(os.name == "posix", "Native audio symbol inspection requires POSIX shared-library exports.")
class TestAudioQueue(unittest.TestCase):
    def setUp(self):
        self.native = ctypes.CDLL(renpysound.__file__)
        self.bind("SDL_GetHint", ctypes.c_char_p, ctypes.c_char_p)
        self.bind("SDL_SetHint", ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p)
        self.bind("SDL_ResetHint", ctypes.c_bool, ctypes.c_char_p)
        hint = b"SDL_AUDIO_DRIVER"
        original = self.native.SDL_GetHint(hint)
        if original is None:
            self.addCleanup(self.native.SDL_ResetHint, hint)
        else:
            self.addCleanup(self.native.SDL_SetHint, hint, original)
        self.assertTrue(self.native.SDL_SetHint(hint, b"dummy"))
        self.bind("SDL_PauseAudioStreamDevice", ctypes.c_bool, ctypes.c_void_p)
        self.bind("SDL_ClearAudioStream", ctypes.c_bool, ctypes.c_void_p)
        self.bind("SDL_GetAudioStreamData", ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int)
        self.bind("SDL_GetError", ctypes.c_char_p)
        self.bind("media_is_ready", ctypes.c_int, ctypes.c_void_p)
        self.bind("SDL_LockMutex", None, ctypes.c_void_p)
        self.bind("SDL_UnlockMutex", None, ctypes.c_void_p)
        self.initialize()
        self.addCleanup(renpysound.quit)

    def initialize(self, rate=48000):
        renpysound.init(rate, 2, 256)
        self.stream = ctypes.c_void_p.in_dll(self.native, "audio_stream")
        self.assertTrue(self.native.SDL_PauseAudioStreamDevice(self.stream), self.native.SDL_GetError())
        self.assertTrue(self.native.SDL_ClearAudioStream(self.stream), self.native.SDL_GetError())

    def bind(self, name, result, *arguments):
        function = getattr(self.native, name)
        function.restype = result
        function.argtypes = arguments
        return function

    @property
    def channel(self):
        address = ctypes.c_void_p.in_dll(self.native, "channels")
        return ctypes.cast(address, ctypes.POINTER(ChannelHead)).contents

    def wait_ready(self, media):
        deadline = time.monotonic() + 5
        event = threading.Event()
        while not self.native.media_is_ready(media):
            self.assertLess(time.monotonic(), deadline, "Audio decoder did not become ready.")
            event.wait(0.001)

    def wav(self, samples=4800, value=10000, ramp=False):
        data = io.BytesIO()
        with wave.open(data, "wb") as output:
            output.setparams((2, 2, 48000, 0, "NONE", "not compressed"))
            if ramp:
                output.writeframes(b"".join(struct.pack("<hh", value + i, value + i) for i in range(samples)))
            else:
                output.writeframes(struct.pack("<hh", value, value) * samples)
        return io.BytesIO(data.getvalue())

    def read(self, samples):
        output = (ctypes.c_float * (samples * 2))()
        size = ctypes.sizeof(output)
        self.assertEqual(
            self.native.SDL_GetAudioStreamData(self.stream, output, size), size, self.native.SDL_GetError()
        )
        return list(output)[::2]

    def assert_gapless(self, output):
        self.assertEqual(sum(sample == 0 for sample in output), 0, "Inserted silent samples at the queue handoff.")

    def play(self, **kwargs):
        renpysound.play(0, self.wav(), "first.wav", synchro_start=True, end=-1, **kwargs)
        self.wait_ready(self.channel.playing)

    def queue(self, **kwargs):
        renpysound.queue(0, self.wav(), "second.wav", synchro_start=True, end=-1, **kwargs)
        self.wait_ready(self.channel.queued)

    def test_immediate_queue_is_gapless(self):
        self.play()
        self.queue()
        renpysound.periodic()
        output = self.read(9600)
        self.assert_gapless(output)
        self.assertEqual(output[0], output[-1])

    def test_late_queue_is_gapless_without_periodic_at_handoff(self):
        self.play()
        renpysound.periodic()
        self.assertTrue(all(sample > 0 for sample in self.read(2400)))
        self.queue()
        renpysound.periodic()
        output = self.read(7200)
        self.assert_gapless(output)
        self.assertEqual(output[0], output[-1])

    def test_initial_sync_still_waits_for_periodic(self):
        self.play()
        self.assertTrue(all(sample == 0 for sample in self.read(256)))
        renpysound.periodic()
        self.assertTrue(all(sample > 0 for sample in self.read(4800)))

    def test_queue_after_natural_eof_starts_playback(self):
        self.play()
        renpysound.periodic()
        self.read(4800)
        self.assertEqual(self.read(256), [0.0] * 256)
        self.assertEqual(renpysound.get_state(0), 3)
        renpysound.queue(0, self.wav(), "second.wav", synchro_start=True, end=-1)
        self.wait_ready(self.channel.playing)
        self.assertEqual(self.read(256), [0.0] * 256)
        renpysound.periodic()
        self.assertTrue(all(sample > 0 for sample in self.read(4800)))

    def test_queue_on_idle_channel_preserves_initial_sync(self):
        renpysound.queue(0, self.wav(), "first.wav", synchro_start=True, end=-1)
        self.wait_ready(self.channel.playing)
        self.assertEqual(self.read(256), [0.0] * 256)
        renpysound.periodic()
        self.assert_gapless(self.read(4800))

    def test_queue_replacement_and_paused_handoff(self):
        self.play(tight=True)
        renpysound.periodic()
        self.read(2400)
        self.queue(tight=True)
        renpysound.queue(0, self.wav(value=5000), "replacement.wav", synchro_start=True, end=-1, tight=True)
        self.wait_ready(self.channel.queued)
        renpysound.pause(0)
        self.assertEqual(self.read(256), [0.0] * 256)
        renpysound.unpause(0)
        output = self.read(7200)
        self.assert_gapless(output)
        self.assertAlmostEqual(output[-1], output[0] / 2)
        self.assertEqual(renpysound.playing_name(0), "replacement.wav")

    def test_initial_channels_start_together(self):
        self.play()
        renpysound.play(1, self.wav(value=5000), "other.wav", synchro_start=True, end=-1)
        self.addCleanup(renpysound.stop, 1)
        self.assertEqual(self.read(256), [0.0] * 256)
        deadline = time.monotonic() + 5
        event = threading.Event()
        while True:
            renpysound.periodic()
            if not self.channel.playing_synchro_start:
                break
            self.assertLess(time.monotonic(), deadline, "Synchronized channels did not become ready.")
            event.wait(0.001)
        output = self.read(2400)
        self.assert_gapless(output)
        self.assertEqual(renpysound.get_pos(0), renpysound.get_pos(1))

    def test_tight_fadeout_spans_late_queue(self):
        self.play(tight=True)
        renpysound.periodic()
        self.read(2400)
        self.queue(tight=True)
        renpysound.fadeout(0, 0.15)
        output = self.read(7200)
        self.assert_gapless(output)
        self.assertGreater(output[0], output[2400])
        self.assertGreater(output[2400], output[-1])
        self.assertEqual(self.read(1), [0.0])

    def test_sample_aligned_partial_playback(self):
        renpysound.play(0, self.wav(ramp=True), "ramp.wav", synchro_start=True, end=-1)
        self.wait_ready(self.channel.playing)
        renpysound.periodic()
        reference = self.read(4800)
        for start, end in [(27, 4800), (49, 101), (61, 115)]:
            with self.subTest(start=start, end=end):
                renpysound.play(
                    0, self.wav(ramp=True), "ramp.wav", synchro_start=True, start=start / 48000, end=end / 48000
                )
                self.wait_ready(self.channel.playing)
                renpysound.periodic()
                self.assertEqual(self.read(end - start), reference[start:end])
                self.assertEqual(self.read(1), [0.0])

    def test_subsample_positions_round_to_nearest_sample(self):
        renpysound.play(0, self.wav(ramp=True), "ramp.wav", synchro_start=True, end=-1)
        self.wait_ready(self.channel.playing)
        renpysound.periodic()
        reference = self.read(4800)
        renpysound.play(
            0, self.wav(ramp=True), "ramp.wav", synchro_start=True, start=27.75 / 48000, end=49.75 / 48000
        )
        self.wait_ready(self.channel.playing)
        renpysound.periodic()
        self.assertEqual(self.read(22), reference[28:50])
        self.assertEqual(self.read(1), [0.0])

    def test_natural_duration_rounds_to_whole_samples(self):
        for samples in [27, 49, 61, 101]:
            with self.subTest(samples=samples):
                renpysound.play(0, self.wav(samples=samples), "short.wav", synchro_start=True, end=-1)
                self.wait_ready(self.channel.playing)
                renpysound.periodic()
                self.assert_gapless(self.read(samples))
                self.assertEqual(self.read(1), [0.0])

    def opus(self):
        # Generated from a stereo 440 Hz, 0.1 s sine at 48 kHz using FFmpeg/libopus.
        return io.BytesIO((Path(__file__).parent / "audio" / "tone.opus").read_bytes())

    def seek_opus(self):
        # ffmpeg -f lavfi -i 'anoisesrc=sample_rate=48000:duration=3:seed=7407:amplitude=0.2' \
        #   -f lavfi -i 'sine=frequency=440:sample_rate=48000:duration=3' \
        #   -filter_complex '[1:a]volume=0.1[tone];[0:a][tone]amix=inputs=2:normalize=0' \
        #   -c:a libopus -b:a 64000 -page_duration 20000 -fflags +bitexact -flags:a +bitexact seek.opus
        return io.BytesIO((Path(__file__).parent / "audio" / "seek.opus").read_bytes())

    def read_chunks(self, samples):
        output = []
        while samples:
            count = min(samples, 960)
            output.extend(self.read(count))
            samples -= count
        return output

    def seek_opus_reference(self, rate=48000):
        renpysound.play(0, self.seek_opus(), "seek.opus", synchro_start=True, end=-1)
        self.wait_ready(self.channel.playing)
        renpysound.periodic()
        reference = self.read_chunks(3 * rate)
        self.assertEqual(self.read(1), [0.0])
        return reference

    def assert_opus_matches(self, output, reference, start, rate=48000):
        probe = output[-512:]
        probe_start = start + len(output) - len(probe)
        offsets = range(max(-400, -probe_start), min(400, len(reference) - probe_start - len(probe)) + 1)
        offset = min(
            offsets,
            key=lambda shift: sum(
                (a - b) ** 2 for a, b in zip(probe, reference[probe_start + shift:probe_start + shift + len(probe)])
            ),
        )
        self.assertEqual(offset, 0, "Opus playback is displaced from the requested sample.")
        for begin, end in [(0, 20), (20, 50), (50, 100)]:
            lo, hi = round(begin * rate / 1000), min(round(end * rate / 1000), len(output))
            if lo >= hi:
                continue
            expected = reference[start + lo:start + hi]
            power = sum(sample ** 2 for sample in expected)
            self.assertGreater(power, 0)
            error = math.sqrt(sum((a - b) ** 2 for a, b in zip(output[lo:hi], expected)) / power)
            self.assertLessEqual(error, 0.01, f"Opus decoder has not warmed up at {begin}-{end} ms.")

    def test_opus_interior_loop_matches_continuous_decode(self):
        reference = self.seek_opus_reference()
        for start in [0, 27, 2400, 47999, 48000, 48312, 96000, 141600]:
            with self.subTest(start=start):
                renpysound.play(0, self.seek_opus(), "seek.opus", synchro_start=True, end=-1)
                self.wait_ready(self.channel.playing)
                renpysound.queue(0, self.seek_opus(), "loop.opus", start=start / 48000, end=-1)
                self.wait_ready(self.channel.queued)
                renpysound.periodic()
                self.assertEqual(self.read_chunks(144000), reference)
                output = self.read_chunks(144000 - start)
                self.assert_opus_matches(output, reference, start)
                self.assertEqual(self.read(1), [0.0])

    def test_opus_resampled_interior_start_matches_continuous_decode(self):
        renpysound.quit()
        self.initialize(44100)
        reference = self.seek_opus_reference(44100)
        renpysound.play(0, self.seek_opus(), "seek.opus", synchro_start=True, start=1.0, end=1.2)
        self.wait_ready(self.channel.playing)
        renpysound.periodic()
        self.assert_opus_matches(self.read_chunks(8820), reference, 44100, 44100)
        self.assertEqual(self.read(1), [0.0])

    def wait_seek(self, position):
        media = ctypes.cast(self.channel.playing, ctypes.POINTER(MediaHead)).contents
        deadline = time.monotonic() + 5
        event = threading.Event()
        while True:
            self.native.SDL_LockMutex(media.lock)
            try:
                ready = not media.seek_requested and media.skip == position and media.audio_queue_samples >= 960
            finally:
                self.native.SDL_UnlockMutex(media.lock)
            if ready:
                return
            self.assertLess(time.monotonic(), deadline, "Audio seek did not finish decoding.")
            event.wait(0.001)

    def test_opus_runtime_seeks_match_continuous_decode(self):
        reference = self.seek_opus_reference()
        renpysound.play(0, self.seek_opus(), "seek.opus", synchro_start=True, end=-1)
        self.wait_ready(self.channel.playing)
        renpysound.periodic()
        for position in [1.0, 0.05, 2.0, 0.0, 2.9]:
            with self.subTest(position=position):
                renpysound.pause(0)
                renpysound.seek(0, position)
                self.wait_seek(position)
                self.assertTrue(self.native.SDL_ClearAudioStream(self.stream), self.native.SDL_GetError())
                renpysound.unpause(0)
                start = round(position * 48000)
                output = self.read_chunks(min(9600, 144000 - start))
                self.assert_opus_matches(output, reference, start)

    def test_opus_loop_has_no_codec_delay_padding(self):
        renpysound.play(0, self.opus(), "tone.opus", synchro_start=True, end=-1)
        self.wait_ready(self.channel.playing)
        renpysound.periodic()
        reference = self.read(4800)
        for start in [0, 27, 49]:
            with self.subTest(start=start):
                renpysound.play(0, self.opus(), "tone.opus", synchro_start=True, end=-1)
                self.wait_ready(self.channel.playing)
                renpysound.queue(0, self.opus(), "loop.opus", start=start / 48000, end=-1)
                self.wait_ready(self.channel.queued)
                renpysound.periodic()
                output = self.read(9600 - start)
                self.assertEqual(output[:4800], reference)
                self.assertEqual(output[4800:], reference[start:])
                self.assertEqual(self.read(1), [0.0])

    def test_resampled_opus_drains_audio_at_eof(self):
        renpysound.quit()
        self.initialize(44100)
        renpysound.play(0, self.opus(), "tone.opus", synchro_start=True, end=-1)
        self.wait_ready(self.channel.playing)
        renpysound.queue(0, self.opus(), "loop.opus", end=-1)
        self.wait_ready(self.channel.queued)
        renpysound.periodic()
        output = self.read(8820)
        self.assertEqual(output[:4410], output[4410:])
        self.assertNotEqual(output[4409], 0.0)
        self.assertEqual(self.read(1), [0.0])

    def test_explicit_end_preserves_requested_padding(self):
        renpysound.play(0, self.opus(), "tone.opus", synchro_start=True, end=0.11)
        self.wait_ready(self.channel.playing)
        renpysound.periodic()
        output = self.read(5280)
        self.assertNotEqual(output[4799], 0.0)
        self.assertEqual(output[4800:], [0.0] * 480)
        self.assertEqual(self.read(1), [0.0])

    def test_movie_preserves_container_duration_padding(self):
        renpysound.set_video(0, renpysound.NODROP_VIDEO)
        renpysound.play(0, self.opus(), "tone.opus", synchro_start=True, end=-1)
        self.wait_ready(self.channel.playing)
        renpysound.periodic()
        output = self.read(5112)
        self.assertNotEqual(output[4799], 0.0)
        self.assertEqual(output[4800:], [0.0] * 312)
        self.assertEqual(self.read(1), [0.0])


if __name__ == "__main__":
    unittest.main()
