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
Smoke tests that run PrismTTS against the real native libprism, with real speech backends.

They depend on the host's installed speech engines and screen readers, and some of them make sound, so they are
opt-in: a default pytest run skips them. Run them with ``uv run pytest -m prism_native``. They also skip, with a
reason, when the Prism dynamic library cannot be loaded.
"""

import time

import pytest

import renpy.display.tts as tts_module
from renpy.display.tts import SCREEN_READER_BACKENDS, PrismTTS

pytestmark = pytest.mark.prism_native


@pytest.fixture(autouse=True)
def require_opt_in(request):
    """
    Skips the native tests unless the prism_native marker was selected with -m.

    A marker expression in addopts would deselect these tests instead, which makes running this file directly
    exit with "no tests ran". Skipping keeps `pytest <file>` working and says how to run them.
    """

    if "prism_native" not in (request.config.getoption("markexpr") or ""):
        pytest.skip("native Prism tests are opt-in; run them with: pytest -m prism_native")


@pytest.fixture
def has_prism():
    """Report whether the Prism dynamic library loaded; tests that need native Prism skip when this is False."""
    return tts_module.prism is not None


def test_prism_tts_initialization(has_prism):
    """PrismTTS can initialize with the real native library and selects a non-screen-reader TTS backend.

    Skipped when the Prism dynamic library is not installed.
    """
    if not has_prism:
        pytest.skip("Prism dynamic library is not available")

    tts = PrismTTS()
    try:
        assert tts.context is not None
        # Should have acquired a backend (or fallback)
        backend = tts.get_backend("tts")
        assert backend is not None
        assert backend.name.lower() not in {"nvda", "jaws", "orca", "voiceover"}
    finally:
        tts.shutdown()


def test_prism_tts_mode_separation(has_prism):
    """mode='tts' never returns a screen reader backend, while mode='screenreader' always returns one.

    Skipped when the Prism dynamic library is not installed. The screenreader assertion requires a backend to exist,
    which depends on the screen readers available on the host, so it can fail on a machine with none.
    """
    if not has_prism:
        pytest.skip("Prism dynamic library is not available")

    tts = PrismTTS()
    try:
        tts_backend = tts.get_backend("tts")
        if tts_backend is not None:
            assert tts_backend.name.lower() not in SCREEN_READER_BACKENDS

        sr_backend = tts.get_backend("screenreader")
        assert sr_backend is not None
    finally:
        tts.shutdown()


def test_prism_tts_voices(has_prism):
    """get_tts_voices returns a list of "language: name" strings on the real native library.

    Skipped when the Prism dynamic library is not installed. An empty list is accepted, since the host may have no
    voices installed.
    """
    if not has_prism:
        pytest.skip("Prism dynamic library is not available")

    tts = PrismTTS()
    try:
        voices = tts.get_tts_voices()
        assert isinstance(voices, list)
        for v in voices:
            assert ": " in v
    finally:
        tts.shutdown()


def test_prism_tts_speak_and_stop(has_prism):
    """speak and stop run against the real backend without raising, and stop ends speech.

    Skipped when the Prism dynamic library is not installed. The short sleep gives the backend time to process the
    stop request before is_speaking() is checked, so this check is timing-dependent.
    """
    if not has_prism:
        pytest.skip("Prism dynamic library is not available")

    tts = PrismTTS()
    try:
        tts.speak("Test line for accessibility.", mode="tts")
        tts.stop()
        time.sleep(0.05)
        assert not tts.is_speaking()
    finally:
        tts.shutdown()


def test_init_prefers_prism_tts(mocker, has_prism):
    """init() instantiates PrismTTS when the Prism library is available.

    Skipped when the Prism dynamic library is not installed.
    """
    if not has_prism:
        pytest.skip("Prism dynamic library is not available")

    mocker.patch.object(tts_module, "platform_tts", None)
    tts_module.init()
    assert isinstance(tts_module.platform_tts, PrismTTS)
