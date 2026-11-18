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
Tests for the voice catalog of renpy/display/tts.py PrismTTS: which voices are listed, how a listed voice is routed
to its backend, and how inline {voice=...} tags and the saved preference choose a voice.

The Prism backends are replaced by mocks, so these tests run without the native library.
"""

from types import SimpleNamespace

import pytest

import renpy.display.tts as tts_module
from renpy.display.tts import PrismTTS

################################################################################
# Voice catalog
################################################################################


def create_voices(count, language="en-US"):
    """Create distinct voices sharing a language to expose unwanted duplicate representatives."""
    return [(language, f"Voice {index}") for index in range(count)]


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


################################################################################
# Routing speech to the backend that owns a voice
################################################################################


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


################################################################################
# Inline {voice=} tags and the voice preference
################################################################################


def test_inline_voice_tag_overrides_preference(make_tts, mocker):
    """An inline {voice=...} tag is stripped from the text and takes precedence over preferences.tts_voice.

    The preferences screen uses the tag to preview each voice in that voice. The tag must be honoured even when the
    saved preference names a different voice, and a tag naming an unavailable voice must yield no voice (not fall
    back to the preference) while still being stripped from the text.
    """
    tts, _backends = make_tts([("sapi", create_voices(4), 0)])
    preferences = SimpleNamespace(tts_voice="en-US: Voice 1")
    mocker.patch.object(tts_module, "platform_tts", tts)
    mocker.patch.object(tts_module, "_tts_voices_cache", None)
    mocker.patch.object(tts_module.renpy, "game", SimpleNamespace(preferences=preferences), create=True)

    assert tts_module.get_voice("{voice=en-US: Voice 3}Hello") == ("en-US: Voice 3", "Hello")
    assert tts_module.get_voice("{voice=xx-XX: Missing}Hello") == (None, "Hello")
    assert tts_module.get_voice("Hello") == ("en-US: Voice 1", "Hello")


@pytest.mark.parametrize(
    ("last_spoken", "retried_text", "preference_after"),
    [
        ("{voice=en-US: Voice 3}Hello", "Hello", "en-US: Voice 1"),
        ("{voice=en-US: Voice 1}Hello", "Hello", None),
        ("Hello", "Hello", None),
    ],
    ids=["tagged", "tagged-same-as-preference", "preference"],
)
def test_failed_speech_retry_drops_tag_and_blames_only_the_preference(
    make_tts, mocker, last_spoken, retried_text, preference_after
):
    """After a nonzero speech exit, periodic() retries once without the voice and blames only the preference.

    A failure with an inline {voice=...} tag must retry with the tag stripped and leave the saved preference alone;
    retrying the tagged text would fail the same way forever. A failure with the preference voice, whether it was
    chosen by the preference or by a tag naming the same voice, clears the preference, as before.
    """
    tts, _backends = make_tts([("sapi", create_voices(4), 0)])
    preferences = SimpleNamespace(tts_voice="en-US: Voice 1")
    tts_function = mocker.Mock()
    process = mocker.Mock(returncode=1)
    process.poll.return_value = 1
    mocker.patch.object(tts_module, "platform_tts", tts)
    mocker.patch.object(tts_module, "_tts_voices_cache", None)
    mocker.patch.object(tts_module, "process", process)
    mocker.patch.object(tts_module, "last_spoken", last_spoken)
    mocker.patch.object(tts_module.renpy, "game", SimpleNamespace(preferences=preferences), create=True)
    mocker.patch.object(tts_module.renpy.config, "tts_function", tts_function)

    tts_module.periodic()

    tts_function.assert_called_once_with(retried_text)
    assert preferences.tts_voice == preference_after
    assert tts_module.process is None


def test_previewed_voice_is_restored_for_default_speech(make_tts, mocker):
    """A voice chosen by an inline {voice=...} tag does not leak into later untagged speech.

    With no saved preference, previewing a non-default voice changes the Prism backend's voice. The next utterance
    without a tag must put the backend back to the default voice captured at startup, and further untagged speech
    must not touch the voice again.
    """
    tts, backends = make_tts([("sapi", create_voices(4), 2)])
    preferences = SimpleNamespace(tts_voice=None, tts_speed=1.0, get_mixer=lambda name: 1.0)
    mocker.patch.object(tts_module, "platform_tts", tts)
    mocker.patch.object(tts_module, "_tts_voices_cache", None)
    mocker.patch.object(tts_module.renpy, "game", SimpleNamespace(preferences=preferences), create=True)

    tts.speak("{voice=en-US: Voice 3}Preview")
    assert backends[0].voice == 3

    tts.speak("Hello")
    assert backends[0].voice == 2

    backends[0].voice = 1
    tts.speak("Again")
    assert backends[0].voice == 1
