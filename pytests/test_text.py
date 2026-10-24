import unittest
from types import SimpleNamespace
from unittest.mock import patch

from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

import renpy
from renpy.display.core import IgnoreEvent
from renpy.text import text


class TestTextSlowAbort(unittest.TestCase):
    def setUp(self):
        self.displayable = SimpleNamespace(
            slow=True,
            slow_done=None,
            style=SimpleNamespace(slow_abortable=True),
            get_layout=lambda: None,
        )
        self.event = SimpleNamespace()

    def test_slow_abort_does_not_consume_event_while_grabbed(self):
        with (
            patch.object(renpy.display.behavior, "map_event", return_value=True),
            patch.object(renpy.display.focus, "get_grab", return_value=object()),
        ):
            result = text.Text.event(self.displayable, self.event, 0, 0, 0)

        self.assertIsNone(result)
        self.assertTrue(self.displayable.slow)

    def test_slow_abort_consumes_dismiss_event_without_grab(self):
        with (
            patch.object(renpy.display.behavior, "map_event", return_value=True),
            patch.object(renpy.display.focus, "get_grab", return_value=None),
            patch.object(text, "slow_text", [self.displayable]),
            self.assertRaises(IgnoreEvent),
        ):
            text.Text.event(self.displayable, self.event, 0, 0, 0)

        self.assertFalse(self.displayable.slow)
