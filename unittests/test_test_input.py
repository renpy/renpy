import unittest
from unittest.mock import patch

from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy import pygame
from renpy.test import testkey


class TestKeyboardEvents(unittest.TestCase):
    def test_printable_key_does_not_require_native_text_input(self):
        for active in (False, True):
            with self.subTest(active=active):
                with (
                    patch.object(pygame.key, "text_input_active", return_value=active),
                    patch.object(pygame.event, "post") as post,
                ):
                    testkey.down("a")
                    testkey.up("a")

                events = [call.args[0] for call in post.call_args_list]
                self.assertEqual([event.type for event in events], [pygame.KEYDOWN, pygame.KEYUP])
                self.assertEqual(events[0].unicode, "a")
                self.assertEqual(events[0].key, pygame.K_a)
                self.assertTrue(all(event.test for event in events))

    def test_uppercase_and_modifiers(self):
        for keysym, text, mods in (
            ("H", "H", pygame.KMOD_LSHIFT),
            ("shift_K_a", "a", pygame.KMOD_LSHIFT),
            ("ctrl_K_a", "a", pygame.KMOD_LCTRL),
            ("alt_K_a", "a", pygame.KMOD_LALT),
        ):
            with self.subTest(keysym=keysym):
                with patch.object(pygame.event, "post") as post:
                    testkey.down(keysym)

                event = post.call_args.args[0]
                self.assertEqual(event.unicode, text)
                self.assertEqual(event.mod, mods)
                post.assert_called_once()

    def test_navigation_keys_do_not_insert_text(self):
        for keysym in ("K_LEFT", "K_BACKSPACE", "K_RETURN"):
            with self.subTest(keysym=keysym):
                with patch.object(pygame.event, "post") as post:
                    testkey.queue_keysym(keysym)

                events = [call.args[0] for call in post.call_args_list]
                self.assertEqual([event.type for event in events], [pygame.KEYDOWN, pygame.KEYUP])
                self.assertEqual(events[0].unicode, "")

    def test_keymap_event_uses_existing_queue(self):
        with (
            patch.dict(testkey.renpy.config.keymap, {"dismiss": ["K_RETURN"]}),
            patch.object(testkey.renpy.exports, "queue_event") as queue,
        ):
            testkey.queue_keysym("dismiss")

        queue.assert_called_once_with("dismiss")
