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

import importlib.util
import io
import sys
import time
import zipfile
from pathlib import Path
from types import SimpleNamespace

import pytest

import renpy
import renpy.config
import renpy.display
import renpy.display.displayable
import renpy.display.tts as tts_module
import renpy.object
from renpy.display.tts import SCREEN_READER_BACKENDS, PrismTTS


def create_voices(count, language="en-US"):
    """Create distinct voices sharing a language to expose unwanted duplicate representatives."""
    return [(language, f"Voice {index}") for index in range(count)]


def _ensure_image_environment(mocker):
    """Prepare minimal module mock environment to import renpy.display.image outside full binary."""
    import types

    if not hasattr(renpy, "pygame"):
        renpy.pygame = mocker.MagicMock()
        sys.modules["renpy.pygame"] = renpy.pygame

    if not hasattr(renpy.display, "core"):
        renpy.display.core = mocker.MagicMock()
    if not hasattr(renpy.display, "im"):
        renpy.display.im = mocker.MagicMock()
    if not hasattr(renpy.display, "imagelike"):
        renpy.display.imagelike = mocker.MagicMock()
    if not hasattr(renpy.display, "behavior"):
        renpy.display.behavior = mocker.MagicMock()

    if "renpy.display.render" not in sys.modules:
        render_mod = types.ModuleType("renpy.display.render")
        render_mod.render = mocker.MagicMock()
        render_mod.Render = mocker.MagicMock()
        sys.modules["renpy.display.render"] = render_mod
        renpy.display.render = render_mod

    if "renpy.style" not in sys.modules or not hasattr(renpy, "style"):
        style_mod = types.ModuleType("renpy.style")

        class DummyStyle:
            """Stand-in for renpy.style.Style that only records the alt attribute."""

            def __init__(self, *args, **kwargs):
                self.alt = None

        style_mod.Style = DummyStyle
        sys.modules["renpy.style"] = style_mod
        renpy.style = style_mod

    if "renpy.substitutions" not in sys.modules or not hasattr(renpy, "substitutions"):
        subst_mod = types.ModuleType("renpy.substitutions")
        subst_mod.substitute = lambda s, scope=None: (s, False)
        sys.modules["renpy.substitutions"] = subst_mod
        renpy.substitutions = subst_mod

    import renpy.display.image as image_module

    return image_module


def _load_fetch_prism_module():
    """Load scripts/fetch_prism.py from the repository without installing it as a package."""
    script_path = Path(__file__).resolve().parents[2] / "scripts" / "fetch_prism.py"
    spec = importlib.util.spec_from_file_location("fetch_prism", script_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _build_mock_sdk_zip(tag="v0.18.3"):
    """Build an in-memory SDK archive with fake binaries for each target platform plus one ignored shim."""
    buf = io.BytesIO()
    payloads = {
        f"prism-sdk-{tag}/windows/x64/dynamic/release/bin/prism.dll": b"MZ_FAKE_WINDOWS_DLL" * 50,
        f"prism-sdk-{tag}/macos/universal/dynamic/release/lib/libprism.dylib": b"\xcf\xfa\xed\xfe_FAKE_MAC_DYLIB" * 50,
        f"prism-sdk-{tag}/linux/x64/dynamic/release/lib/libprism.so": b"\x7fELF_FAKE_LINUX_X64_SO" * 50,
        f"prism-sdk-{tag}/linux/arm64/dynamic/release/lib/libprism.so": b"\x7fELF_FAKE_LINUX_ARM64_SO" * 50,
        f"prism-sdk-{tag}/windows/x64/dynamic/release/bin/tolk.dll": b"SHIM_SHOULD_BE_IGNORED",
    }
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_STORED) as zf:
        for name, content in payloads.items():
            zf.writestr(name, content)
    return buf.getvalue(), payloads


def _make_range_opener(zip_bytes, resolved_tag="v0.18.3"):
    """Return a urlopen replacement that serves the archive, honoring HEAD and HTTP Range requests.

    The "latest" release URL redirects to resolved_tag, mimicking GitHub's release redirect.
    """

    class FakeResponse:
        """Minimal response object supporting read() and the context-manager protocol."""

        def __init__(self, data, url, headers):
            self._data = data
            self.url = url
            self.headers = headers

        def read(self):
            return self._data

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    def opener(req):
        url = req.full_url
        method = getattr(req, "method", None) or "GET"
        if url.endswith("/releases/latest"):
            return FakeResponse(
                b"",
                f"https://github.com/ethindp/prism/releases/tag/{resolved_tag}",
                {},
            )
        if method == "HEAD":
            return FakeResponse(
                b"",
                url,
                {"Content-Length": str(len(zip_bytes))},
            )
        range_hdr = req.headers.get("Range") or req.headers.get("range")
        if range_hdr and range_hdr.startswith("bytes="):
            start_s, end_s = range_hdr[len("bytes=") :].split("-")
            start = int(start_s)
            end = int(end_s)
            return FakeResponse(zip_bytes[start : end + 1], url, {})
        return FakeResponse(zip_bytes, url, {})

    return opener


@pytest.fixture
def has_prism():
    """Report whether the Prism dynamic library loaded; tests that need native Prism skip when this is False."""
    return tts_module.prism is not None


@pytest.fixture
def make_tts(mocker):
    """Factory that builds a PrismTTS over mocked Prism backends and shuts each one down at teardown.

    Each specification is (backend name, [(language, voice name), ...], default voice index or None). A None
    default makes the backend's voice property raise, as when no current voice exists. The Prism context and
    _ensure_input_desktop are patched only while PrismTTS is constructed, so the tests exercise the real methods.
    """
    created = []

    def make(specifications):
        """Build a PrismTTS from the given specifications and register it for shutdown at teardown."""
        backends = []
        for name, voices, default in specifications:
            backend = mocker.MagicMock()
            backend.name = name
            backend.voices_count = len(voices)
            backend.get_voice_language.side_effect = lambda index, entries=voices: entries[index][0]
            backend.get_voice_name.side_effect = lambda index, entries=voices: entries[index][1]
            backend.speaking = False
            if default is None:
                type(backend).voice = mocker.PropertyMock(side_effect=RuntimeError("No current voice"))
            else:
                backend.voice = default
            backends.append(backend)

        context = mocker.MagicMock()
        context.backends_count = len(backends)
        context.id_of.side_effect = lambda index: index
        context.name_of.side_effect = lambda bid: backends[bid].name
        context.acquire.side_effect = lambda bid: backends[bid]
        context.acquire_best.return_value = next(iter(backends), None)
        prism = SimpleNamespace(Context=mocker.MagicMock(return_value=context))
        prism_patch = mocker.patch.object(tts_module, "prism", prism)
        ensure_patch = mocker.patch.object(tts_module, "_ensure_input_desktop")
        tts = PrismTTS()
        mocker.stop(prism_patch)
        mocker.stop(ensure_patch)
        created.append(tts)
        return tts, backends

    yield make

    for tts in reversed(created):
        tts.shutdown()


def test_web_without_ctypes(mocker):
    """Importing tts.py with ctypes unavailable must still let the web backend initialize.

    The module is executed under a private name with ctypes hidden from sys.modules, which simulates the browser
    runtime. The platform flags and sys.platform are faked as emscripten only for the init() call. Those fakes are
    not stopped early, so they remain in effect until the test ends.
    """
    path = Path(__file__).resolve().parents[2] / "renpy" / "display" / "tts.py"
    spec = importlib.util.spec_from_file_location("_test_web_tts", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)

    ctypes_hidden = mocker.patch.dict(sys.modules, {"ctypes": None, "ctypes.util": None})
    spec.loader.exec_module(module)
    mocker.stop(ctypes_hidden)

    assert module.prism is None
    mocker.patch.multiple(
        renpy,
        android=False,
        ios=False,
        macintosh=False,
        linux=False,
        windows=False,
        emscripten=True,
    )
    mocker.patch.object(
        renpy,
        "config",
        SimpleNamespace(tts_substitutions=[], auto_screenreader_voicing=False),
        create=True,
    )
    mocker.patch.object(module.sys, "platform", "emscripten")
    module.init()

    assert isinstance(module.platform_tts, module.WebTTS)


@pytest.mark.parametrize("second_count", [10, 11], ids=["total-50", "total-51"])
def test_combined_threshold_boundary(make_tts, second_count):
    """Exactly 50 combined voices remain complete; 51 trigger reduction of both large backends.

    second_count varies the size of the second backend, which sets the combined total to 50 or 51.
    """
    first = create_voices(40)
    second = create_voices(second_count)
    tts, _ = make_tts([("sapi", first, 3), ("espeak", second, 2)])
    expected = (
        ["en-US: Voice 3", "en-US: Voice 2"]
        if second_count == 11
        else [
            f"{language}: {name}"
            for backend, entries in (("sapi", first), ("espeak", second))
            for language, name in entries
        ]
    )
    assert tts.get_tts_voices() == expected


def test_small_backends_remain_complete(make_tts):
    """Above 50 total voices, a 10-voice backend stays complete while an 11-voice backend reduces.

    The reduction rule applies per backend: only backends with more than 10 voices collapse to one representative
    per language, so the 10-voice backend keeps all of its voices.
    """
    tts, _ = make_tts([
        ("sapi", create_voices(30), 5),
        ("small", create_voices(10), 4),
        ("espeak", create_voices(11), 6),
    ])
    assert tts.get_tts_voices() == (
        ["en-US: Voice 5"] + [f"en-US: Voice {index}" for index in range(10)] + ["en-US: Voice 6"]
    )


def test_exact_languages_and_initial_default(make_tts):
    """Regional and unknown languages stay distinct; the captured default replaces the first voice.

    The default is read when the backend is acquired. Changing the backend's current voice afterwards must not
    alter the listing.
    """
    entries = [("en-US", "First US"), ("en-GB", "First GB"), ("", "Unknown")]
    entries += create_voices(47)
    entries.append(("en-US", "Default US"))
    tts, backends = make_tts([("sapi", entries, 50)])
    expected = ["en-US: Default US", "en-GB: First GB", ": Unknown"]
    assert tts.get_tts_voices() == expected
    assert backends[0].voice == 50
    backends[0].voice = 0
    assert tts.get_tts_voices() == expected


@pytest.mark.parametrize("default", [None, -1, 51], ids=["unavailable", "negative", "out-of-range"])
def test_unavailable_and_invalid_defaults_use_first_voice(make_tts, mocker, default):
    """An unavailable or out-of-range default cannot discard a language's representative.

    default varies the captured default voice: None means the voice query raised, while -1 and 51 are outside the
    51-voice catalog. In each case the first voice of the language must be the representative. The log patch
    records the failure message that the unavailable case should produce.
    """
    log = mocker.patch.object(tts_module.renpy.display.log, "write")
    tts, _ = make_tts([("sapi", create_voices(51), default)])
    assert tts.get_tts_voices() == ["en-US: Voice 0"]
    if default is None:
        log.assert_called()


def test_reduction_is_not_a_hard_cap(make_tts):
    """All language groups remain available even when more than 50 survive.

    Fifty-one distinct languages collapse to one representative each, so the result is not truncated to 50 entries.
    """
    entries = [(f"language-{index}", "Voice") for index in range(51)]
    tts, _ = make_tts([("sapi", entries, 0)])
    assert tts.get_tts_voices() == [f"{language}: Voice" for language, name in entries]


@pytest.mark.parametrize(
    "specifications",
    [[], [("sapi", [], 0)]],
    ids=["no-backends", "backend-without-voices"],
)
def test_empty_catalogs(make_tts, specifications):
    """No backends and backends without voices both produce empty lists.

    specifications varies whether the registry is empty or contains a backend that reports no voices.
    """
    tts, _ = make_tts(specifications)
    assert tts.get_tts_voices() == []
    assert tts.resolve_voice("missing") is None


def test_secondary_voice_routes_speech_and_controls(make_tts, mocker):
    """A menu entry must speak through its own backend at its original, unreduced index.

    The SAPI backend has 40 voices and is reduced in the menu, while the espeak voice at index 7 is listed. Speech
    must go to espeak with that index, and the stop call must reach only the other backend, which may still be
    talking.
    """
    tts, backends = make_tts([
        (
            "sapi",
            [(language, f"SAPI Voice {index}") for index, (language, _) in enumerate(create_voices(40))],
            8,
        ),
        ("espeak", create_voices(11), 7),
    ])
    assert "en-US: Voice 7" in tts.get_tts_voices()
    get_voice = mocker.patch.object(tts_module, "get_voice", return_value=("en-US: Voice 7", "Hello"))
    tts.speak("Hello", mode="tts")
    mocker.stop(get_voice)

    assert backends[1].voice == 7
    backends[1].output.assert_called_once_with("Hello", interrupt=True)
    backends[0].output.assert_not_called()
    assert tts.tts_backend is backends[0]
    # Interrupting speech must silence the other backend, which may still be talking.
    backends[0].stop.assert_called_once()
    backends[1].stop.assert_not_called()
    for backend in backends:
        backend.stop.reset_mock()
    backends[1].speaking = True
    assert tts.is_speaking()
    tts.stop()
    for backend in backends:
        backend.stop.assert_called_once()
    assert tts.context.acquire.call_count == 2
    context = tts.context
    tts.shutdown()
    tts.shutdown()
    for backend in backends:
        backend.free.assert_called_once()
    context.shutdown.assert_called_once()


def test_legacy_preference_omitted_from_menu_still_speaks(make_tts, mocker):
    """Saved unqualified preferences remain valid even when their voice is filtered out.

    The saved preference "en-US: Voice 3" refers to a voice that is reduced away from the menu. The preference must
    still resolve and speak, and the saved value must not be rewritten.
    """
    tts, backends = make_tts([
        ("sapi", create_voices(40), 8),
        ("espeak", [("fr-FR", "French")] * 11, 0),
    ])
    preferences = SimpleNamespace(tts_voice="en-US: Voice 3")
    mocker.patch.object(tts_module, "platform_tts", tts)
    mocker.patch.object(tts_module, "_tts_voices_cache", None)
    mocker.patch.object(tts_module.renpy, "game", SimpleNamespace(preferences=preferences), create=True)

    assert "en-US: Voice 3" not in tts_module.get_tts_voices()
    assert tts_module.get_voice("Hello") == ("en-US: Voice 3", "Hello")
    tts.speak("Hello")
    assert backends[0].voice == 3
    backends[0].output.assert_called_once_with("Hello", interrupt=True)
    assert preferences.tts_voice == "en-US: Voice 3"
    assert "en-US: Voice 8" in tts.get_tts_voices()
    assert tts_module.get_tts_voices() == sorted(tts.get_tts_voices(), key=str.lower)


def test_enumeration_failure_is_logged_and_other_backends_remain_available(make_tts, mocker):
    """A backend failure must be visible without preventing selection from healthy backends.

    The sapi backend raises while its voice names are read. The failure must be written to the log, and the espeak
    backend must still be resolvable by its qualified name.
    """
    tts, backends = make_tts([("sapi", create_voices(1), 0), ("espeak", create_voices(1), 0)])
    backends[0].get_voice_name.side_effect = RuntimeError("Voice enumeration failed")
    log = mocker.patch.object(tts_module.renpy.display.log, "write")
    assert tts.get_tts_voices() == ["en-US: Voice 0"]
    log.assert_called()
    mocker.stop(log)
    assert tts.resolve_voice("en-US: Voice 0 [espeak]") == (backends[1], 0)


def test_legacy_collision_prefers_default_backend(make_tts):
    """Identical legacy names prefer the normal backend, not merely the first registry entry.

    Both backends list "en-US: Shared" with no backend qualifier. The unqualified name must resolve to sapi, which
    is the normal backend, while the explicit "[espeak]" suffix selects espeak.
    """
    tts, backends = make_tts([("espeak", [("en-US", "Shared")], 0), ("sapi", [("en-US", "Shared")], 0)])
    assert tts.resolve_voice("en-US: Shared") == (backends[1], 0)
    assert tts.resolve_voice("en-US: Shared [espeak]") == (backends[0], 0)


def test_screen_reader_excluded_and_routing_unchanged(make_tts, mocker):
    """Screen-reader voices are never listed and a TTS preference cannot redirect screen-reader output.

    The nvda backend is a screen reader, so its "Reader" voice is hidden from the listing. Speech in screenreader mode
    must still be routed to the nvda backend.
    """
    tts, backends = make_tts([("nvda", [("en-US", "Reader")], 0), ("sapi", create_voices(1), 0)])
    assert tts.get_tts_voices() == ["en-US: Voice 0"]
    get_voice = mocker.patch.object(tts_module, "get_voice", return_value=("en-US: Voice 0", "Hello"))
    tts.speak("Hello", mode="screenreader")
    mocker.stop(get_voice)
    backends[0].output.assert_called_once_with("Hello", interrupt=True)
    backends[1].output.assert_not_called()


def test_default_speech_uses_preferred_backend(make_tts, mocker):
    """Listing all backends does not change which backend handles speech without a preference.

    The onecore backend is preferred over espeak for speech, so it must receive the output even though espeak was
    registered first.
    """
    tts, backends = make_tts([("espeak", create_voices(1), 0), ("onecore", create_voices(1), 0)])
    tts.get_tts_voices()
    get_voice = mocker.patch.object(tts_module, "get_voice", return_value=(None, "Hello"))
    tts.speak("Hello")
    mocker.stop(get_voice)
    backends[1].output.assert_called_once_with("Hello", interrupt=True)
    backends[0].output.assert_not_called()


def test_screen_reader_backends_defined():
    """Known screen readers are classified in SCREEN_READER_BACKENDS, and speech engines are not.

    The classification decides which backends are excluded from the TTS voice list, so a misclassified speech
    engine would vanish from the menu and a screen reader would be offered as a voice.
    """
    assert "nvda" in SCREEN_READER_BACKENDS
    assert "jaws" in SCREEN_READER_BACKENDS
    assert "orca" in SCREEN_READER_BACKENDS
    assert "voiceover" in SCREEN_READER_BACKENDS
    assert "onecore" not in SCREEN_READER_BACKENDS
    assert "sapi" not in SCREEN_READER_BACKENDS
    for backend in ("hal", "supernova", "cobra", "dolphin", "narrator"):
        assert backend not in SCREEN_READER_BACKENDS


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


def test_default_tts_function_modes(mocker):
    """default_tts_function passes the mode that matches the self_voicing preference to speak.

    A "screenreader" preference selects screen-reader mode, and a True preference selects tts mode. The game object
    is replaced with a stub, and the patch is removed by the fixture at teardown.
    """
    mock_platform_tts = mocker.MagicMock(spec=PrismTTS)
    mocker.patch.object(tts_module, "platform_tts", mock_platform_tts)
    preferences = SimpleNamespace(self_voicing="screenreader")
    mocker.patch.object(tts_module.renpy, "game", SimpleNamespace(preferences=preferences), create=True)

    tts_module.default_tts_function("Hello Screen Reader")
    mock_platform_tts.speak.assert_called_with("Hello Screen Reader", mode="screenreader")

    preferences.self_voicing = True
    tts_module.default_tts_function("Hello TTS")
    mock_platform_tts.speak.assert_called_with("Hello TTS", mode="tts")


def test_init_prefers_prism_tts(mocker, has_prism):
    """init() instantiates PrismTTS when the Prism library is available.

    Skipped when the Prism dynamic library is not installed.
    """
    if not has_prism:
        pytest.skip("Prism dynamic library is not available")

    mocker.patch.object(tts_module, "platform_tts", None)
    tts_module.init()
    assert isinstance(tts_module.platform_tts, PrismTTS)


def test_init_falls_back_when_prism_missing(mocker):
    """init() falls back to the legacy platform TTS when prism is None.

    The Windows assertion is the only check of the chosen backend. On other platforms the test only verifies that
    init() completes without error.
    """
    mocker.patch.object(tts_module, "prism", None)
    mocker.patch.object(tts_module, "platform_tts", None)
    tts_module.init()
    # If on Windows, should be WindowsTTS, on Linux LinuxTTS, etc.
    if sys.platform.startswith("win"):
        assert isinstance(tts_module.platform_tts, tts_module.WindowsTTS)


def test_has_active_screenreader_true(mocker):
    """has_active_screenreader returns True when a supported screen reader is active.

    The context is a mock that reports a single "nvda" backend, and the acquired backend must be cached in sr_backend
    as a side effect of the check.
    """
    tts = PrismTTS.__new__(PrismTTS)
    mock_ctx = mocker.MagicMock()
    mock_ctx.backends_count = 1
    mock_ctx.id_of.return_value = 1
    mock_ctx.name_of.return_value = "nvda"
    mock_backend = mocker.MagicMock()
    mock_backend.name = "nvda"
    mock_ctx.acquire.return_value = mock_backend
    tts.context = mock_ctx
    tts.sr_backend = None
    tts.tts_backend = None

    assert tts.has_active_screenreader()
    assert tts.sr_backend == mock_backend


def test_has_active_screenreader_false(mocker):
    """has_active_screenreader returns False when only a non-screen-reader backend is present.

    The single "sapi" backend is a speech engine, not a screen reader, so no screen reader can be reported active.
    """
    tts = PrismTTS.__new__(PrismTTS)
    mock_ctx = mocker.MagicMock()
    mock_ctx.backends_count = 1
    mock_ctx.id_of.return_value = 1
    mock_ctx.name_of.return_value = "sapi"
    tts.context = mock_ctx
    tts.sr_backend = None
    tts.tts_backend = None

    assert not tts.has_active_screenreader()


def test_check_auto_screenreader_enables_screenreader(mocker):
    """check_auto_screenreader turns on screen reader voicing when a screen reader is active.

    The self_voicing preference starts unset, so it must become "screenreader". The check runs only once per session,
    which the _auto_screenreader_checked patch isolates for this test.
    """
    preferences = SimpleNamespace(self_voicing=None)
    platform = mocker.MagicMock(spec=PrismTTS)
    platform.has_active_screenreader.return_value = True

    mocker.patch.object(tts_module, "platform_tts", platform)
    mocker.patch.object(tts_module, "_auto_screenreader_checked", False)
    mocker.patch.object(tts_module.renpy, "game", SimpleNamespace(preferences=preferences), create=True)
    mocker.patch.object(tts_module.renpy.config, "auto_screenreader_voicing", True, create=True)

    tts_module.check_auto_screenreader()
    assert preferences.self_voicing == "screenreader"


def test_check_auto_screenreader_respects_explicit_user_disabled(mocker):
    """check_auto_screenreader does not override an explicit False self_voicing preference.

    A user who turned self-voicing off must keep it off even when a screen reader is active.
    """
    preferences = SimpleNamespace(self_voicing=False)
    platform = mocker.MagicMock(spec=PrismTTS)
    platform.has_active_screenreader.return_value = True

    mocker.patch.object(tts_module, "platform_tts", platform)
    mocker.patch.object(tts_module, "_auto_screenreader_checked", False)
    mocker.patch.object(tts_module.renpy, "game", SimpleNamespace(preferences=preferences), create=True)
    mocker.patch.object(tts_module.renpy.config, "auto_screenreader_voicing", True, create=True)

    tts_module.check_auto_screenreader()
    assert not preferences.self_voicing


def test_check_auto_screenreader_respects_config_disabled(mocker):
    """check_auto_screenreader does not enable voicing when config.auto_screenreader_voicing is False.

    The screen reader is active here, so the config flag is the only reason voicing stays unset.
    """
    preferences = SimpleNamespace(self_voicing=None)
    platform = mocker.MagicMock(spec=PrismTTS)
    platform.has_active_screenreader.return_value = True

    mocker.patch.object(tts_module, "platform_tts", platform)
    mocker.patch.object(tts_module, "_auto_screenreader_checked", False)
    mocker.patch.object(tts_module.renpy, "game", SimpleNamespace(preferences=preferences), create=True)
    mocker.patch.object(tts_module.renpy.config, "auto_screenreader_voicing", False, create=True)

    tts_module.check_auto_screenreader()
    assert preferences.self_voicing is None


def test_availability_callback_runtime_start_stop(mocker):
    """_on_availability_changed sets the screen reader backend when it becomes available and clears it when it stops.

    The NVDA start event must set the backend and turn on screen-reader voicing. The stop event must clear the
    backend reference.
    """
    preferences = SimpleNamespace(self_voicing=None)
    mocker.patch.object(tts_module.renpy, "game", SimpleNamespace(preferences=preferences), create=True)
    mocker.patch.object(tts_module.renpy.config, "auto_screenreader_voicing", True, create=True)

    tts = PrismTTS.__new__(PrismTTS)
    mock_ctx = mocker.MagicMock()
    mock_backend = mocker.MagicMock()
    mock_backend.name = "nvda"
    mock_ctx.acquire.return_value = mock_backend
    tts.context = mock_ctx
    tts.sr_backend = None
    tts.tts_backend = None

    # NVDA becomes available
    tts._on_availability_changed(None, 1, b"nvda", True)
    assert tts.sr_backend == mock_backend
    assert preferences.self_voicing == "screenreader"

    # NVDA stops
    tts._on_availability_changed(None, 1, b"nvda", False)
    assert tts.sr_backend is None


def test_image_reference_explicit_alt(mocker):
    """ImageReference returns the explicit style.alt when one is set.

    The substitution is patched to echo its input, so the result comes only from the explicit alt text.
    """
    image_module = _ensure_image_environment(mocker)
    im_ref = image_module.ImageReference(("eileen", "happy"))
    im_ref.target = mocker.MagicMock(_tts=lambda raw: "")
    im_ref.style = mocker.MagicMock()
    im_ref.style.alt = "Eileen smiling warmly"
    mocker.patch("renpy.substitutions.substitute", return_value=("Eileen smiling warmly", False))
    assert im_ref._tts(raw=False) == "Eileen smiling warmly"


def test_image_reference_auto_image_alt(mocker):
    """ImageReference derives alt text from the image tags only when config.auto_image_alt is True.

    With the option off the reference produces no text. With it on, the substituted tag and attribute names are
    returned. The config value is restored by the mocker at teardown.
    """
    image_module = _ensure_image_environment(mocker)
    import renpy.config as config_module

    im_ref = image_module.ImageReference(("eileen", "happy"))
    im_ref.target = mocker.MagicMock(_tts=lambda raw: "")
    im_ref.style = mocker.MagicMock()
    im_ref.style.alt = None

    # When auto_image_alt is False
    mocker.patch.object(config_module, "auto_image_alt", False, create=True)
    assert im_ref._tts(raw=False) == ""

    # When auto_image_alt is True
    config_module.auto_image_alt = True
    mocker.patch("renpy.substitutions.substitute", return_value=("eileen happy", False))
    assert im_ref._tts(raw=False) == "eileen happy"


def test_find_and_load_prism_checks_executable_dir(mocker, tmp_path):
    """_find_and_load_prism looks for the Prism library in the directory containing sys.executable first.

    ctypes.CDLL is replaced so no real library is loaded. The fake library sits next to the fake executable, and the
    first path attempted must be that library.
    """
    if sys.platform.startswith("win"):
        dll_name = "prism.dll"
    elif sys.platform.startswith("darwin"):
        dll_name = "libprism.dylib"
    else:
        dll_name = "libprism.so"

    fake_dll_path = str(tmp_path / dll_name)
    (tmp_path / dll_name).write_bytes(b"fake")
    fake_exe = str(tmp_path / "renpy")
    loaded_paths = []

    class DummyCDLL:
        """Records each load path, giving the fake library a prism_init attribute."""

        def __init__(self, path):
            loaded_paths.append(path)
            if path == fake_dll_path:
                self.prism_init = mocker.MagicMock()

    mocker.patch.object(sys, "executable", fake_exe)
    mocker.patch("ctypes.CDLL", side_effect=DummyCDLL)
    mocker.patch.object(tts_module, "_CtypesPrismModule", side_effect=lambda dll: dll)

    res = tts_module._find_and_load_prism()
    assert res is not None
    assert loaded_paths[0] == fake_dll_path


def test_resolve_release_tag():
    """resolve_release_tag normalizes explicit tags and follows the redirect for "latest".

    A bare version gains the "v" prefix, an explicit tag is returned unchanged, and "latest" is resolved through the
    release redirect served by the fake opener.
    """
    mod = _load_fetch_prism_module()
    zip_bytes, _ = _build_mock_sdk_zip("v0.18.3")
    opener = _make_range_opener(zip_bytes, resolved_tag="v0.18.3")

    assert mod.resolve_release_tag("0.18.3", opener=opener) == "v0.18.3"
    assert mod.resolve_release_tag("v0.18.3", opener=opener) == "v0.18.3"
    assert mod.resolve_release_tag("latest", opener=opener) == "v0.18.3"


def test_fetch_prism_libraries_extracts_only_target_binaries(tmp_path):
    """fetch_prism_libraries extracts exact platform binaries via HTTP Range requests and ignores other entries.

    Four platform binaries are written, and the macOS dylib is also copied into the app bundle. The tolk.dll shim in
    the archive must not be extracted.
    """
    mod = _load_fetch_prism_module()
    zip_bytes, payloads = _build_mock_sdk_zip("v0.18.3")
    opener = _make_range_opener(zip_bytes, resolved_tag="v0.18.3")

    root_dir = tmp_path
    lib_dir = root_dir / "lib"
    mac_app_dir = root_dir / "renpy.app" / "Contents" / "MacOS"
    mac_app_dir.mkdir(parents=True)

    tag, written = mod.fetch_prism_libraries(
        version="latest",
        dest_dir=lib_dir,
        platforms="all",
        opener=opener,
    )

    assert tag == "v0.18.3"
    assert len(written) == 4

    win_dll = lib_dir / "py3-windows-x86_64" / "prism.dll"
    mac_dylib = lib_dir / "py3-mac-universal" / "libprism.dylib"
    linux_x64_so = lib_dir / "py3-linux-x86_64" / "libprism.so"
    linux_arm_so = lib_dir / "py3-linux-aarch64" / "libprism.so"
    mac_app_dylib = mac_app_dir / "libprism.dylib"

    assert win_dll.read_bytes() == payloads["prism-sdk-v0.18.3/windows/x64/dynamic/release/bin/prism.dll"]
    assert mac_dylib.read_bytes() == payloads["prism-sdk-v0.18.3/macos/universal/dynamic/release/lib/libprism.dylib"]
    assert linux_x64_so.read_bytes() == payloads["prism-sdk-v0.18.3/linux/x64/dynamic/release/lib/libprism.so"]
    assert linux_arm_so.read_bytes() == payloads["prism-sdk-v0.18.3/linux/arm64/dynamic/release/lib/libprism.so"]
    assert (
        mac_app_dylib.read_bytes() == payloads["prism-sdk-v0.18.3/macos/universal/dynamic/release/lib/libprism.dylib"]
    )
    assert not (lib_dir / "py3-windows-x86_64" / "tolk.dll").exists()


def test_fetch_zip_entry_detects_crc_mismatch():
    """fetch_zip_entry raises RuntimeError when the downloaded entry's CRC32 does not match the directory.

    The expected CRC is flipped, which simulates a corrupted download. Only the RuntimeError type is asserted here.
    """
    mod = _load_fetch_prism_module()
    zip_bytes, _ = _build_mock_sdk_zip("v0.18.3")
    opener = _make_range_opener(zip_bytes, resolved_tag="v0.18.3")

    final_url, entries = mod.read_remote_zip_directory(
        "https://example.com/prism-sdk-v0.18.3.zip",
        opener=opener,
    )
    entry = dict(entries["prism-sdk-v0.18.3/windows/x64/dynamic/release/bin/prism.dll"])
    entry["crc"] ^= 0xFFFFFFFF

    with pytest.raises(RuntimeError):
        mod.fetch_zip_entry(final_url, entry, opener=opener)
