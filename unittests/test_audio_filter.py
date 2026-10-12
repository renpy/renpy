import ctypes
import pickle
import unittest

from renpy.audio import filter as audio_filter


class TestAudioFilter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        capsule = audio_filter.__pyx_capi__["get_apply_audio_filter"]
        get_name = ctypes.pythonapi.PyCapsule_GetName
        get_name.argtypes = [ctypes.py_object]
        get_name.restype = ctypes.c_char_p
        get_pointer = ctypes.pythonapi.PyCapsule_GetPointer
        get_pointer.argtypes = [ctypes.py_object, ctypes.c_char_p]
        get_pointer.restype = ctypes.c_void_p
        getter = ctypes.PYFUNCTYPE(ctypes.c_void_p)(get_pointer(capsule, get_name(capsule)))
        cls.apply_filter = ctypes.PYFUNCTYPE(
            None, ctypes.py_object, ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_int
        )(getter())

    def apply(self, filter, samples):
        buffer = (ctypes.c_float * len(samples))(*samples)
        filter.prepare(1000)
        self.apply_filter(filter, buffer, 2, len(samples) // 2, 1000)
        return list(buffer)

    def test_delay_keeps_stereo_channels_separate(self):
        for delay, frames in ((0.02, (20, 20)), ([0.02, 0.03], (20, 30))):
            for channel in (0, 1):
                with self.subTest(delay=delay, channel=channel):
                    samples = [0.0] * 100
                    samples[channel] = 1.0
                    expected = [0.0] * 100
                    expected[frames[channel] * 2 + channel] = 1.0
                    self.assertEqual(self.apply(audio_filter.Delay(delay), samples), expected)

    def test_delay_wraps_and_preserves_state_between_calls(self):
        samples = [0.0] * 6200
        expected = [0.0] * 6200
        for frame in (0, 1009, 2050):
            for channel, delay in ((0, 20), (1, 30)):
                samples[frame * 2 + channel] = channel + 1.0
                expected[(frame + delay) * 2 + channel] = channel + 1.0

        filter = audio_filter.Delay([0.02, 0.03])
        output = []
        for start in range(0, len(samples), 14):
            output.extend(self.apply(filter, samples[start:start + 14]))
        self.assertEqual(output, expected)

    def test_comb_wet_preserves_input_with_zero_multiplier(self):
        samples = [1.0, -0.5, 0.25, 0.75] * 20
        for kwargs in ({}, {"wet": True}):
            with self.subTest(kwargs=kwargs):
                self.assertEqual(self.apply(audio_filter.Comb(0.02, multiplier=0, **kwargs), samples), samples)

    def test_comb_without_wet_returns_only_delayed_signal(self):
        samples = [0.0] * 120
        samples[0] = 1.0
        expected = [0.0] * 120
        expected[40] = 0.5
        expected[80] = 0.25
        self.assertEqual(self.apply(audio_filter.Comb(0.02, multiplier=0.5, wet=False), samples), expected)

    def test_comb_serialization_preserves_wet(self):
        for wet in (True, False):
            with self.subTest(wet=wet):
                filter = audio_filter.Comb(0.02, multiplier=0, wet=wet)
                self.assertEqual(filter.__reduce__()[1][-1], wet)
                restored = pickle.loads(pickle.dumps(filter))
                self.assertEqual(restored.__reduce__()[1][-1], wet)
                samples = [1.0, -0.5] * 20
                self.assertEqual(self.apply(restored, samples), samples if wet else [0.0] * len(samples))

    def test_reverb_keeps_stereo_channels_separate(self):
        for channel in (0, 1):
            with self.subTest(channel=channel):
                samples = [0.0] * 160
                samples[channel] = 1.0
                filter = audio_filter.Reverb(dampening=100, dry=0, delay_times=[0.02], allpass_frequences=[])
                output = self.apply(filter, samples)
                self.assertEqual(output[1 - channel::2], [0.0] * 80)
                self.assertEqual(output[:40], [0.0] * 40)
                self.assertTrue(any(output[channel::2]))
