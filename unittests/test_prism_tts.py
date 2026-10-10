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
from unittest.mock import MagicMock


class TestPrismTTS(unittest.TestCase):
    def setUp(self):
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
        from renpy.display.tts import PrismTTS
        import renpy.display.tts as tts_module

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
            self.assertEqual(im_ref._tts(raw=False), "eileen happy")
        finally:
            config_module.auto_image_alt = False


if __name__ == "__main__":
    unittest.main()
