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

import renpy.display.tts as tts_module
from renpy.display.tts import PrismTTS


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
