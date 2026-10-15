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

import sys
import unittest
from unittest.mock import MagicMock, patch


class TestPrismTTS(unittest.TestCase):
    def setUp(self):
        import renpy

        if not hasattr(renpy, "error"):
            import renpy.error

            renpy.error = renpy.error
        import renpy.config

        try:
            from renpy.display.tts import prism

            self.has_prism = prism is not None
        except Exception:
            self.has_prism = False

    def test_screen_reader_backends_defined(self):
        """Test that known screen readers are classified in SCREEN_READER_BACKENDS."""
        from renpy.display.tts import SCREEN_READER_BACKENDS

        self.assertIn("nvda", SCREEN_READER_BACKENDS)
        self.assertIn("jaws", SCREEN_READER_BACKENDS)
        self.assertIn("orca", SCREEN_READER_BACKENDS)
        self.assertIn("voiceover", SCREEN_READER_BACKENDS)
        self.assertNotIn("onecore", SCREEN_READER_BACKENDS)
        self.assertNotIn("sapi", SCREEN_READER_BACKENDS)
        for backend in ("hal", "supernova", "cobra", "dolphin", "narrator"):
            self.assertNotIn(backend, SCREEN_READER_BACKENDS)

    def test_prism_tts_initialization(self):
        """Test that PrismTTS can initialize when prism is installed."""
        if not self.has_prism:
            self.skipTest("Prism dynamic library is not available")

        from renpy.display.tts import PrismTTS

        tts = PrismTTS()
        try:
            self.assertIsNotNone(tts.context)
            # Should have acquired a backend (or fallback)
            backend = tts.get_backend("tts")
            self.assertIsNotNone(backend)
            self.assertFalse(backend.name.lower() in {"nvda", "jaws", "orca", "voiceover"})
        finally:
            tts.shutdown()

    def test_prism_tts_mode_separation(self):
        """Test that mode='tts' does not return a screen reader backend."""
        if not self.has_prism:
            self.skipTest("Prism dynamic library is not available")

        from renpy.display.tts import SCREEN_READER_BACKENDS, PrismTTS

        tts = PrismTTS()
        try:
            tts_backend = tts.get_backend("tts")
            if tts_backend is not None:
                self.assertNotIn(tts_backend.name.lower(), SCREEN_READER_BACKENDS)

            sr_backend = tts.get_backend("screenreader")
            self.assertIsNotNone(sr_backend)
        finally:
            tts.shutdown()

    def test_prism_tts_voices(self):
        """Test that get_tts_voices returns a list of formatted voice strings."""
        if not self.has_prism:
            self.skipTest("Prism dynamic library is not available")

        from renpy.display.tts import PrismTTS

        tts = PrismTTS()
        try:
            voices = tts.get_tts_voices()
            self.assertIsInstance(voices, list)
            for v in voices:
                self.assertIn(": ", v)
        finally:
            tts.shutdown()

    def test_prism_tts_speak_and_stop(self):
        """Test speak and stop methods without errors."""
        if not self.has_prism:
            self.skipTest("Prism dynamic library is not available")

        import time

        from renpy.display.tts import PrismTTS

        tts = PrismTTS()
        try:
            tts.speak("Test line for accessibility.", mode="tts")
            tts.stop()
            time.sleep(0.05)
            self.assertFalse(tts.is_speaking())
        finally:
            tts.shutdown()

    def test_default_tts_function_modes(self):
        """Test that default_tts_function calls speak with correct mode based on self_voicing preference."""
        import renpy.display.tts as tts_module

        mock_platform_tts = MagicMock(spec=tts_module.PrismTTS)
        old_platform_tts = tts_module.platform_tts
        tts_module.platform_tts = mock_platform_tts

        class DummyPreferences:
            self_voicing = "screenreader"

        class DummyGame:
            preferences = DummyPreferences()

        old_game = getattr(tts_module.renpy, "game", None)
        tts_module.renpy.game = DummyGame()

        try:
            # Test screenreader mode
            tts_module.default_tts_function("Hello Screen Reader")
            mock_platform_tts.speak.assert_called_with("Hello Screen Reader", mode="screenreader")

            # Test tts mode
            DummyPreferences.self_voicing = True
            tts_module.default_tts_function("Hello TTS")
            mock_platform_tts.speak.assert_called_with("Hello TTS", mode="tts")
        finally:
            tts_module.platform_tts = old_platform_tts
            if old_game is not None:
                tts_module.renpy.game = old_game
            elif hasattr(tts_module.renpy, "game"):
                delattr(tts_module.renpy, "game")

    def test_init_prefers_prism_tts(self):
        """Test that init() instantiates PrismTTS when prism is available."""
        if not self.has_prism:
            self.skipTest("Prism dynamic library is not available")

        import renpy.display.tts as tts_module

        old_platform_tts = tts_module.platform_tts
        try:
            tts_module.platform_tts = None
            tts_module.init()
            self.assertIsInstance(tts_module.platform_tts, tts_module.PrismTTS)
        finally:
            tts_module.platform_tts = old_platform_tts

    def test_init_falls_back_when_prism_missing(self):
        """Test that init() falls back to legacy platform TTS when prism is None."""
        import renpy.display.tts as tts_module

        old_prism = tts_module.prism
        old_platform_tts = tts_module.platform_tts
        try:
            tts_module.prism = None
            tts_module.platform_tts = None
            tts_module.init()
            # If on Windows, should be WindowsTTS, on Linux LinuxTTS, etc.
            if sys.platform.startswith("win"):
                self.assertIsInstance(tts_module.platform_tts, tts_module.WindowsTTS)
        finally:
            tts_module.prism = old_prism
            tts_module.platform_tts = old_platform_tts

    def test_has_active_screenreader_true(self):
        """Test that has_active_screenreader() returns True when a supported screen reader is active."""
        from renpy.display.tts import PrismTTS

        tts = PrismTTS.__new__(PrismTTS)
        mock_ctx = MagicMock()
        mock_ctx.backends_count = 1
        mock_ctx.id_of.return_value = 1
        mock_ctx.name_of.return_value = "nvda"
        mock_backend = MagicMock()
        mock_backend.name = "nvda"
        mock_ctx.acquire.return_value = mock_backend
        tts.context = mock_ctx
        tts.sr_backend = None
        tts.tts_backend = None

        self.assertTrue(tts.has_active_screenreader())
        self.assertEqual(tts.sr_backend, mock_backend)

    def test_has_active_screenreader_false(self):
        """Test that has_active_screenreader() returns False when no screen reader is available."""
        from renpy.display.tts import PrismTTS

        tts = PrismTTS.__new__(PrismTTS)
        mock_ctx = MagicMock()
        mock_ctx.backends_count = 1
        mock_ctx.id_of.return_value = 1
        mock_ctx.name_of.return_value = "sapi"
        tts.context = mock_ctx
        tts.sr_backend = None
        tts.tts_backend = None

        self.assertFalse(tts.has_active_screenreader())

    def test_check_auto_screenreader_enables_screenreader(self):
        """Test that check_auto_screenreader() automatically enables screen reader voicing when active."""
        import renpy.display.tts as tts_module

        class DummyPreferences:
            self_voicing = None

        class DummyGame:
            preferences = DummyPreferences()

        old_platform_tts = tts_module.platform_tts
        old_checked = tts_module._auto_screenreader_checked
        old_game = getattr(tts_module.renpy, "game", None)

        mock_platform_tts = MagicMock(spec=tts_module.PrismTTS)
        mock_platform_tts.has_active_screenreader.return_value = True

        tts_module.platform_tts = mock_platform_tts
        tts_module._auto_screenreader_checked = False
        tts_module.renpy.game = DummyGame()
        tts_module.renpy.config.auto_screenreader_voicing = True

        try:
            tts_module.check_auto_screenreader()
            self.assertEqual(DummyGame.preferences.self_voicing, "screenreader")
        finally:
            tts_module.platform_tts = old_platform_tts
            tts_module._auto_screenreader_checked = old_checked
            if old_game is not None:
                tts_module.renpy.game = old_game
            elif hasattr(tts_module.renpy, "game"):
                delattr(tts_module.renpy, "game")

    def test_check_auto_screenreader_respects_explicit_user_disabled(self):
        """Test that check_auto_screenreader() does not override an explicit False preference."""
        import renpy.display.tts as tts_module

        class DummyPreferences:
            self_voicing = False

        class DummyGame:
            preferences = DummyPreferences()

        old_platform_tts = tts_module.platform_tts
        old_checked = tts_module._auto_screenreader_checked
        old_game = getattr(tts_module.renpy, "game", None)

        mock_platform_tts = MagicMock(spec=tts_module.PrismTTS)
        mock_platform_tts.has_active_screenreader.return_value = True

        tts_module.platform_tts = mock_platform_tts
        tts_module._auto_screenreader_checked = False
        tts_module.renpy.game = DummyGame()
        tts_module.renpy.config.auto_screenreader_voicing = True

        try:
            tts_module.check_auto_screenreader()
            self.assertFalse(DummyGame.preferences.self_voicing)
        finally:
            tts_module.platform_tts = old_platform_tts
            tts_module._auto_screenreader_checked = old_checked
            if old_game is not None:
                tts_module.renpy.game = old_game
            elif hasattr(tts_module.renpy, "game"):
                delattr(tts_module.renpy, "game")

    def test_check_auto_screenreader_respects_config_disabled(self):
        """Test that check_auto_screenreader() does not enable voicing if config option is False."""
        import renpy.display.tts as tts_module

        class DummyPreferences:
            self_voicing = None

        class DummyGame:
            preferences = DummyPreferences()

        old_platform_tts = tts_module.platform_tts
        old_checked = tts_module._auto_screenreader_checked
        old_game = getattr(tts_module.renpy, "game", None)

        mock_platform_tts = MagicMock(spec=tts_module.PrismTTS)
        mock_platform_tts.has_active_screenreader.return_value = True

        tts_module.platform_tts = mock_platform_tts
        tts_module._auto_screenreader_checked = False
        tts_module.renpy.game = DummyGame()
        tts_module.renpy.config.auto_screenreader_voicing = False

        try:
            tts_module.check_auto_screenreader()
            self.assertIsNone(DummyGame.preferences.self_voicing)
        finally:
            tts_module.renpy.config.auto_screenreader_voicing = True
            tts_module.platform_tts = old_platform_tts
            tts_module._auto_screenreader_checked = old_checked
            if old_game is not None:
                tts_module.renpy.game = old_game
            elif hasattr(tts_module.renpy, "game"):
                delattr(tts_module.renpy, "game")

    def test_availability_callback_runtime_start_stop(self):
        """Test that _on_availability_changed dynamically activates and clears screen reader backend."""
        import renpy.display.tts as tts_module
        from renpy.display.tts import PrismTTS

        class DummyPreferences:
            self_voicing = None

        class DummyGame:
            preferences = DummyPreferences()

        old_game = getattr(tts_module.renpy, "game", None)
        tts_module.renpy.game = DummyGame()
        tts_module.renpy.config.auto_screenreader_voicing = True

        tts = PrismTTS.__new__(PrismTTS)
        mock_ctx = MagicMock()
        mock_backend = MagicMock()
        mock_backend.name = "nvda"
        mock_ctx.acquire.return_value = mock_backend
        tts.context = mock_ctx
        tts.sr_backend = None
        tts.tts_backend = None

        try:
            # NVDA becomes available
            tts._on_availability_changed(None, 1, b"nvda", True)
            self.assertEqual(tts.sr_backend, mock_backend)
            self.assertEqual(DummyGame.preferences.self_voicing, "screenreader")

            # NVDA stops
            tts._on_availability_changed(None, 1, b"nvda", False)
            self.assertIsNone(tts.sr_backend)
        finally:
            if old_game is not None:
                tts_module.renpy.game = old_game
            elif hasattr(tts_module.renpy, "game"):
                delattr(tts_module.renpy, "game")

    def _ensure_image_environment(self):
        """Prepare minimal module mock environment to import renpy.display.image outside full binary."""
        import types

        import renpy

        if not hasattr(renpy, "error"):
            import renpy.error

            renpy.error = renpy.error
        if not hasattr(renpy, "config"):
            import renpy.config

            renpy.config = renpy.config
        if not hasattr(renpy, "object"):
            import renpy.object

            renpy.object = renpy.object
        if not hasattr(renpy, "pygame"):
            renpy.pygame = MagicMock()
            sys.modules["renpy.pygame"] = renpy.pygame

        import renpy.display

        if not hasattr(renpy.display, "core"):
            renpy.display.core = MagicMock()
        if not hasattr(renpy.display, "im"):
            renpy.display.im = MagicMock()
        if not hasattr(renpy.display, "imagelike"):
            renpy.display.imagelike = MagicMock()
        if not hasattr(renpy.display, "behavior"):
            renpy.display.behavior = MagicMock()

        if "renpy.display.render" not in sys.modules:
            render_mod = types.ModuleType("renpy.display.render")
            render_mod.render = MagicMock()
            render_mod.Render = MagicMock()
            sys.modules["renpy.display.render"] = render_mod
            renpy.display.render = render_mod

        if "renpy.style" not in sys.modules or not hasattr(renpy, "style"):
            style_mod = types.ModuleType("renpy.style")

            class DummyStyle(object):
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

        import renpy.display.tts

        renpy.display.tts = renpy.display.tts
        import renpy.display.displayable

        renpy.display.displayable = renpy.display.displayable

        import renpy.display.image as image_module

        return image_module

    def test_image_reference_explicit_alt(self):
        """Test that ImageReference returns explicit style.alt if set."""
        image_module = self._ensure_image_environment()
        im_ref = image_module.ImageReference(("eileen", "happy"))
        im_ref.target = MagicMock(_tts=lambda raw: "")
        im_ref.style = MagicMock()
        im_ref.style.alt = "Eileen smiling warmly"
        with patch("renpy.substitutions.substitute", return_value=("Eileen smiling warmly", False)):
            self.assertEqual(im_ref._tts(raw=False), "Eileen smiling warmly")

    def test_image_reference_auto_image_alt(self):
        """Test that ImageReference returns tag/attribute names when auto_image_alt is True."""
        image_module = self._ensure_image_environment()
        import renpy.config as config_module

        im_ref = image_module.ImageReference(("eileen", "happy"))
        im_ref.target = MagicMock(_tts=lambda raw: "")
        im_ref.style = MagicMock()
        im_ref.style.alt = None

        # When auto_image_alt is False
        config_module.auto_image_alt = False
        self.assertEqual(im_ref._tts(raw=False), "")

        # When auto_image_alt is True
        config_module.auto_image_alt = True
        try:
            with patch("renpy.substitutions.substitute", return_value=("eileen happy", False)):
                self.assertEqual(im_ref._tts(raw=False), "eileen happy")
        finally:
            config_module.auto_image_alt = False

    def test_find_and_load_prism_checks_executable_dir(self):
        """Test that _find_and_load_prism checks the directory containing sys.executable."""
        import os
        import tempfile
        from unittest.mock import patch

        import renpy.display.tts as tts_module

        with tempfile.TemporaryDirectory() as tmpdir:
            if sys.platform.startswith("win"):
                dll_name = "prism.dll"
            elif sys.platform.startswith("darwin"):
                dll_name = "libprism.dylib"
            else:
                dll_name = "libprism.so"

            fake_dll_path = os.path.join(tmpdir, dll_name)
            with open(fake_dll_path, "wb") as f:
                f.write(b"fake")

            fake_exe = os.path.join(tmpdir, "renpy")
            loaded_paths = []

            class DummyCDLL:
                def __init__(self, path):
                    loaded_paths.append(path)
                    if path == fake_dll_path:
                        self.prism_init = MagicMock()

            with (
                patch.object(sys, "executable", fake_exe),
                patch("ctypes.CDLL", side_effect=DummyCDLL),
                patch.object(tts_module, "_CtypesPrismModule", side_effect=lambda dll: dll),
            ):
                res = tts_module._find_and_load_prism()
                self.assertIsNotNone(res)
                self.assertEqual(loaded_paths[0], fake_dll_path)


class TestFetchPrismScript(unittest.TestCase):
    def _load_fetch_prism_module(self):
        import importlib.util
        import pathlib

        script_path = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "fetch_prism.py"
        spec = importlib.util.spec_from_file_location("fetch_prism", script_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def _build_mock_sdk_zip(self, tag="v0.18.3"):
        import io
        import zipfile

        buf = io.BytesIO()
        payloads = {
            f"prism-sdk-{tag}/windows/x64/dynamic/release/bin/prism.dll": b"MZ_FAKE_WINDOWS_DLL" * 50,
            f"prism-sdk-{tag}/macos/universal/dynamic/release/lib/libprism.dylib": b"\xcf\xfa\xed\xfe_FAKE_MAC_DYLIB"
            * 50,
            f"prism-sdk-{tag}/linux/x64/dynamic/release/lib/libprism.so": b"\x7fELF_FAKE_LINUX_X64_SO" * 50,
            f"prism-sdk-{tag}/linux/arm64/dynamic/release/lib/libprism.so": b"\x7fELF_FAKE_LINUX_ARM64_SO" * 50,
            f"prism-sdk-{tag}/windows/x64/dynamic/release/bin/tolk.dll": b"SHIM_SHOULD_BE_IGNORED",
        }
        with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for name, content in payloads.items():
                zf.writestr(name, content)
        return buf.getvalue(), payloads

    def _make_range_opener(self, zip_bytes, resolved_tag="v0.18.3"):
        class FakeResponse:
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

    def test_resolve_release_tag(self):
        """Test that resolve_release_tag normalizes explicit tags and follows redirects for 'latest'."""
        mod = self._load_fetch_prism_module()
        zip_bytes, _ = self._build_mock_sdk_zip("v0.18.3")
        opener = self._make_range_opener(zip_bytes, resolved_tag="v0.18.3")

        self.assertEqual(mod.resolve_release_tag("0.18.3", opener=opener), "v0.18.3")
        self.assertEqual(mod.resolve_release_tag("v0.18.3", opener=opener), "v0.18.3")
        self.assertEqual(mod.resolve_release_tag("latest", opener=opener), "v0.18.3")

    def test_fetch_prism_libraries_extracts_only_target_binaries(self):
        """Test that fetch_prism_libraries extracts exact platform binaries via HTTP Range requests."""
        import pathlib
        import tempfile

        mod = self._load_fetch_prism_module()
        zip_bytes, payloads = self._build_mock_sdk_zip("v0.18.3")
        opener = self._make_range_opener(zip_bytes, resolved_tag="v0.18.3")

        with tempfile.TemporaryDirectory() as tmpdir:
            root_dir = pathlib.Path(tmpdir)
            lib_dir = root_dir / "lib"
            mac_app_dir = root_dir / "renpy.app" / "Contents" / "MacOS"
            mac_app_dir.mkdir(parents=True)

            tag, written = mod.fetch_prism_libraries(
                version="latest",
                dest_dir=lib_dir,
                platforms="all",
                opener=opener,
            )

            self.assertEqual(tag, "v0.18.3")
            self.assertEqual(len(written), 4)

            win_dll = lib_dir / "py3-windows-x86_64" / "prism.dll"
            mac_dylib = lib_dir / "py3-mac-universal" / "libprism.dylib"
            linux_x64_so = lib_dir / "py3-linux-x86_64" / "libprism.so"
            linux_arm_so = lib_dir / "py3-linux-aarch64" / "libprism.so"
            mac_app_dylib = mac_app_dir / "libprism.dylib"

            self.assertEqual(
                win_dll.read_bytes(),
                payloads["prism-sdk-v0.18.3/windows/x64/dynamic/release/bin/prism.dll"],
            )
            self.assertEqual(
                mac_dylib.read_bytes(),
                payloads["prism-sdk-v0.18.3/macos/universal/dynamic/release/lib/libprism.dylib"],
            )
            self.assertEqual(
                linux_x64_so.read_bytes(),
                payloads["prism-sdk-v0.18.3/linux/x64/dynamic/release/lib/libprism.so"],
            )
            self.assertEqual(
                linux_arm_so.read_bytes(),
                payloads["prism-sdk-v0.18.3/linux/arm64/dynamic/release/lib/libprism.so"],
            )
            self.assertEqual(
                mac_app_dylib.read_bytes(),
                payloads["prism-sdk-v0.18.3/macos/universal/dynamic/release/lib/libprism.dylib"],
            )
            self.assertFalse((lib_dir / "py3-windows-x86_64" / "tolk.dll").exists())

    def test_fetch_zip_entry_detects_crc_mismatch(self):
        """Test that fetch_zip_entry raises RuntimeError on corrupted CRC32."""
        mod = self._load_fetch_prism_module()
        zip_bytes, _ = self._build_mock_sdk_zip("v0.18.3")
        opener = self._make_range_opener(zip_bytes, resolved_tag="v0.18.3")

        final_url, entries = mod.read_remote_zip_directory(
            "https://example.com/prism-sdk-v0.18.3.zip",
            opener=opener,
        )
        entry = dict(entries["prism-sdk-v0.18.3/windows/x64/dynamic/release/bin/prism.dll"])
        entry["crc"] ^= 0xFFFFFFFF

        with self.assertRaises(RuntimeError):
            mod.fetch_zip_entry(final_url, entry, opener=opener)


if __name__ == "__main__":
    unittest.main()
