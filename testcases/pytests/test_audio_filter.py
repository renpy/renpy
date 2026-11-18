import ctypes
import pickle

import pytest

from renpy.audio import filter as audio_filter


@pytest.fixture(scope="module")
def apply_filter():
    """
    Return a ctypes wrapper around the Cython `get_apply_audio_filter` C entry point.

    The entry point is exported as a PyCapsule, so the function pointer is extracted with the
    PyCapsule C API. The wrapper takes (filter, float buffer, channels, frame count, sample rate).
    """

    capsule = audio_filter.__pyx_capi__["get_apply_audio_filter"]
    get_name = ctypes.pythonapi.PyCapsule_GetName
    get_name.argtypes = [ctypes.py_object]
    get_name.restype = ctypes.c_char_p
    get_pointer = ctypes.pythonapi.PyCapsule_GetPointer
    get_pointer.argtypes = [ctypes.py_object, ctypes.c_char_p]
    get_pointer.restype = ctypes.c_void_p
    getter = ctypes.PYFUNCTYPE(ctypes.c_void_p)(get_pointer(capsule, get_name(capsule)))
    return ctypes.PYFUNCTYPE(
        None, ctypes.py_object, ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_int
    )(getter())


def apply(apply_filter, filter, samples):
    """
    Run `samples` (interleaved stereo floats) through `filter` at 1000 Hz and return the result.

    The filter is prepared before each call. The returned list is a copy of the ctypes buffer
    after the in-place update.
    """

    buffer = (ctypes.c_float * len(samples))(*samples)
    filter.prepare(1000)
    apply_filter(filter, buffer, 2, len(samples) // 2, 1000)
    return list(buffer)


@pytest.mark.parametrize(
    ("delay", "channel", "frame"),
    [
        (0.02, 0, 20),
        (0.02, 1, 20),
        ([0.02, 0.03], 0, 20),
        ([0.02, 0.03], 1, 30),
    ],
    ids=["single-left", "single-right", "multi-left", "multi-right"],
)
def test_delay_keeps_stereo_channels_separate(apply_filter, delay, channel, frame):
    """
    An impulse on one channel is delayed only on that channel, so the other channel stays silent.

    Scalar and per-channel delay lists are both covered. Samples are interleaved, so the expected
    index of frame N on channel C is N * 2 + C.
    """

    samples = [0.0] * 100
    samples[channel] = 1.0
    expected = [0.0] * 100
    expected[frame * 2 + channel] = 1.0
    assert apply(apply_filter, audio_filter.Delay(delay), samples) == expected


def test_delay_wraps_and_preserves_state_between_calls(apply_filter):
    """
    A Delay keeps its internal buffer across successive calls, so chunked input matches one large call.

    Impulses are placed at several frames spread across the input, so some echoes land in later
    chunks. The input is fed in 14-sample chunks, and the concatenated output must equal the expected
    delayed signal, which checks state continuity across calls.
    """

    samples = [0.0] * 6200
    expected = [0.0] * 6200
    for frame in (0, 1009, 2050):
        for channel, delay in ((0, 20), (1, 30)):
            samples[frame * 2 + channel] = channel + 1.0
            expected[(frame + delay) * 2 + channel] = channel + 1.0

    filter = audio_filter.Delay([0.02, 0.03])
    output = []
    for start in range(0, len(samples), 14):
        output.extend(apply(apply_filter, filter, samples[start : start + 14]))
    assert output == expected


@pytest.mark.parametrize("kwargs", [{}, {"wet": True}], ids=["default-wet", "explicit-wet"])
def test_comb_wet_preserves_input_with_zero_multiplier(apply_filter, kwargs):
    """
    A wet Comb with a zero multiplier passes the input through unchanged.

    The default and explicit `wet=True` forms are both wet, so both must return the input samples.
    """

    samples = [1.0, -0.5, 0.25, 0.75] * 20
    assert apply(apply_filter, audio_filter.Comb(0.02, multiplier=0, **kwargs), samples) == samples


def test_comb_without_wet_returns_only_delayed_signal(apply_filter):
    """
    A dry-only Comb (`wet=False`) outputs only the feedback taps, so the original impulse is absent.

    At 1000 Hz a 20 ms delay is 20 frames, which is 40 interleaved samples. With multiplier 0.5 the
    impulse reappears at sample 40 with amplitude 0.5 and at sample 80 with amplitude 0.25.
    """

    samples = [0.0] * 120
    samples[0] = 1.0
    expected = [0.0] * 120
    expected[40] = 0.5
    expected[80] = 0.25
    assert apply(apply_filter, audio_filter.Comb(0.02, multiplier=0.5, wet=False), samples) == expected


@pytest.mark.parametrize("wet", [True, False], ids=["wet", "dry"])
def test_comb_serialization_preserves_wet(apply_filter, wet):
    """
    The `wet` setting survives a pickle round trip and still controls the output after restore.

    `__reduce__` stores `wet` as the last constructor argument, which the test reads directly. A wet
    restored filter passes input through, and a dry one outputs silence for this zero-multiplier case.
    """

    filter = audio_filter.Comb(0.02, multiplier=0, wet=wet)
    assert filter.__reduce__()[1][-1] == wet
    restored = pickle.loads(pickle.dumps(filter))
    assert restored.__reduce__()[1][-1] == wet
    samples = [1.0, -0.5] * 20
    assert apply(apply_filter, restored, samples) == (samples if wet else [0.0] * len(samples))


@pytest.mark.parametrize("channel", [0, 1], ids=["left", "right"])
def test_reverb_keeps_stereo_channels_separate(apply_filter, channel):
    """
    A reverb excited on one channel produces a tail only on that channel, never on the other.

    The dry signal is zeroed, so output comes only from the reverb network. The silent channel must be
    all zeros, and the active channel must contain energy. The first 40 interleaved samples (20 frames)
    are checked to be silent, because the 20 ms delay line has not yet produced output.
    """

    samples = [0.0] * 160
    samples[channel] = 1.0
    filter = audio_filter.Reverb(dampening=100, dry=0, delay_times=[0.02], allpass_frequences=[])
    output = apply(apply_filter, filter, samples)
    assert output[1 - channel :: 2] == [0.0] * 80
    assert output[:40] == [0.0] * 40
    assert any(output[channel::2])
