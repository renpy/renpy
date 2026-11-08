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

"""Tests for how renpy/display/tts.py is imported and initialized: the web build, locating Prism, and the fallback TTS."""

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

import renpy
import renpy.display.tts as tts_module


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


@pytest.mark.parametrize(
    ("flag", "backend"),
    [
        ("android", "AndroidTTS"),
        ("ios", "AppleTTS"),
        ("macintosh", "AppleTTS"),
        ("linux", "LinuxTTS"),
        ("windows", "WindowsTTS"),
        ("emscripten", "WebTTS"),
    ],
)
def test_init_falls_back_when_prism_missing(mocker, flag, backend):
    """
    init() falls back to the legacy TTS class for the current platform when prism is None, without
    creating a PrismTTS.

    Each case sets one platform flag and the legacy backend classes are replaced by factories that return
    a marker, because the real ones would start speech engines. sys.platform is fixed to "linux" so the
    Windows fallback cannot be taken by accident, and check_auto_screenreader is replaced because it
    would query the backend.
    """

    flags = dict.fromkeys(["android", "ios", "macintosh", "linux", "windows", "emscripten"], False)
    flags[flag] = True
    mocker.patch.multiple(renpy, **flags)
    mocker.patch.object(tts_module.sys, "platform", "linux")
    mocker.patch.object(tts_module, "prism", None)
    mocker.patch.object(tts_module, "platform_tts", None)
    mocker.patch.object(tts_module, "check_auto_screenreader")
    prism_tts = mocker.patch.object(tts_module, "PrismTTS")

    marker = object()
    for name in ["AndroidTTS", "AppleTTS", "LinuxTTS", "WindowsTTS", "WebTTS"]:
        mocker.patch.object(tts_module, name, return_value=object())
    mocker.patch.object(tts_module, backend, return_value=marker)

    tts_module.init()

    assert tts_module.platform_tts is marker
    prism_tts.assert_not_called()
