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
Tests for the screen reader handling of renpy/display/tts.py: choosing the speech mode, detecting an active screen
reader, and turning on screen reader voicing automatically.
"""

from types import SimpleNamespace

import pytest

import renpy.display.tts as tts_module
from renpy.display.tts import PrismTTS


class FakeBackend:
    """A Prism backend that records the text it is asked to output, in place of the native library."""

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.spoken: list[str] = []
        self.features: SimpleNamespace = SimpleNamespace(supports_set_volume=False, supports_set_rate=False)
        self.voices_count: int = 0
        self.voice: int = 0
        self.speaking: bool = False

    def output(self, s: str, interrupt: bool = True) -> None:
        self.spoken.append(s)

    def stop(self) -> None:
        pass

    def free(self) -> None:
        pass


class FakeContext:
    """
    A Prism context whose list of available backends a test can change, as when a screen reader starts or stops
    while the game runs.
    """

    def __init__(self, backends: list[FakeBackend]) -> None:
        self.backends: list[FakeBackend] = backends
        self.by_id: dict[int, FakeBackend] = dict(enumerate(backends))

    @property
    def backends_count(self) -> int:
        return len(self.backends)

    def id_of(self, index: int) -> int:
        return next(bid for bid, b in self.by_id.items() if b is self.backends[index])

    def name_of(self, bid: int) -> str:
        return self.by_id[bid].name

    def acquire(self, bid: int) -> FakeBackend:
        return self.by_id[bid]

    def acquire_best(self) -> FakeBackend | None:
        return next(iter(self.backends), None)

    def add(self, backend: FakeBackend) -> int:
        """Makes `backend` available, and returns its id."""
        bid = len(self.by_id)
        self.by_id[bid] = backend
        self.backends.append(backend)
        return bid

    def remove(self, backend: FakeBackend) -> None:
        """Makes `backend` unavailable. Its id stays known, as Prism ids are stable."""
        self.backends.remove(backend)


@pytest.fixture
def make_tts(mocker):
    """
    Factory that builds a real PrismTTS over a FakeContext holding backends with the given names, and shuts it down
    at teardown. The prism module is replaced only while PrismTTS is constructed.
    """
    created = []

    def make(*names: str) -> tuple[PrismTTS, FakeContext]:
        context = FakeContext([FakeBackend(name) for name in names])
        prism = SimpleNamespace(Context=lambda **kwargs: context)
        prism_patch = mocker.patch.object(tts_module, "prism", prism)
        tts = PrismTTS()
        mocker.stop(prism_patch)
        created.append(tts)
        return tts, context

    yield make

    for tts in reversed(created):
        tts.shutdown()


@pytest.fixture
def preferences(mocker):
    """Replaces renpy.game with a stub holding only the preferences that self-voicing reads."""
    prefs = SimpleNamespace(self_voicing=None, tts_voice=None)
    mocker.patch.object(tts_module.renpy, "game", SimpleNamespace(preferences=prefs), create=True)
    return prefs


def spoken_by(context: FakeContext) -> dict[str, list[str]]:
    """Returns what each backend known to `context` has spoken, by backend name."""
    return {b.name: b.spoken for b in context.by_id.values()}


@pytest.mark.parametrize(
    ("self_voicing", "expected"),
    [
        ("screenreader", {"nvda": ["Hello"], "sapi": []}),
        (True, {"nvda": [], "sapi": ["Hello"]}),
    ],
    ids=["screenreader", "tts"],
)
def test_default_tts_function_routes_by_preference(make_tts, preferences, mocker, self_voicing, expected):
    """
    default_tts_function speaks through the screen reader when self_voicing is "screenreader", and through the speech
    synthesizer when it is True, with both an nvda screen reader and a sapi synthesizer available.
    """
    tts, context = make_tts("nvda", "sapi")
    mocker.patch.object(tts_module, "platform_tts", tts)
    preferences.self_voicing = self_voicing

    tts_module.default_tts_function("Hello")

    assert spoken_by(context) == expected


@pytest.mark.parametrize(
    ("names", "expected"),
    [(("nvda", "sapi"), True), (("sapi",), False)],
    ids=["screen-reader", "synthesizer-only"],
)
def test_has_active_screenreader(make_tts, names, expected):
    """
    has_active_screenreader reports whether a screen reader backend is available. A sapi speech synthesizer alone is
    not a screen reader, even though it is the fallback for screen reader speech.
    """
    tts, _context = make_tts(*names)

    assert tts.has_active_screenreader() is expected


class FakePlatformTTS:
    """A platform TTS object that reports a fixed screen reader state to check_auto_screenreader."""

    def __init__(self, active: bool) -> None:
        self.active: bool = active

    def has_active_screenreader(self) -> bool:
        return self.active


@pytest.mark.parametrize(
    ("initial", "config_enabled", "active", "expected"),
    [
        (None, True, True, "screenreader"),
        (False, True, True, False),
        (None, False, True, None),
        (None, True, False, None),
    ],
    ids=["enables", "user-disabled", "config-disabled", "no-screen-reader"],
)
def test_check_auto_screenreader(preferences, mocker, initial, config_enabled, active, expected):
    """
    check_auto_screenreader turns on screen reader voicing only when the preference is unset, the screen reader is
    active, and config.auto_screenreader_voicing is true. An explicit False preference, set by a user who turned
    self-voicing off, is kept. The check runs once per session, so _auto_screenreader_checked is reset for each test.
    """
    preferences.self_voicing = initial
    mocker.patch.object(tts_module, "platform_tts", FakePlatformTTS(active))
    mocker.patch.object(tts_module, "_auto_screenreader_checked", False)
    mocker.patch.object(tts_module.renpy.config, "auto_screenreader_voicing", config_enabled, create=True)

    tts_module.check_auto_screenreader()

    assert preferences.self_voicing == expected


def test_screen_reader_started_and_stopped_at_runtime(make_tts, preferences, mocker):
    """
    When a screen reader becomes available after startup, screen reader speech goes to it and screen reader voicing
    is turned on. When it stops, screen reader speech falls back to the synthesizer.

    Prism reports these changes through the availability callback, which the test calls the way Prism does, after
    changing which backends the fake context lists.
    """
    mocker.patch.object(tts_module.renpy.config, "auto_screenreader_voicing", True, create=True)
    tts, context = make_tts("sapi")
    nvda = FakeBackend("nvda")

    bid = context.add(nvda)
    tts._on_availability_changed(None, bid, b"nvda", True)
    tts.speak("Started", mode="screenreader")

    assert preferences.self_voicing == "screenreader"
    assert spoken_by(context) == {"sapi": [], "nvda": ["Started"]}

    context.remove(nvda)
    tts._on_availability_changed(None, bid, b"nvda", False)
    tts.speak("Stopped", mode="screenreader")

    assert spoken_by(context) == {"sapi": ["Stopped"], "nvda": ["Started"]}
