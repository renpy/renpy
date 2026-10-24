import unittest
from unittest.mock import patch

import renpy
from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy.text.extras import filter_alt_text


class TestAltText(unittest.TestCase):
    def setUp(self):
        for patcher in (
            patch.object(renpy.config, "custom_text_tags", {}),
            patch.object(renpy.config, "self_closing_custom_text_tags", {}),
            patch.object(renpy.config, "replace_text", None),
            patch.object(renpy.config, "tts_filter_tags", ["noalt", "rt", "art"]),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_nested_same_filter_tag_stays_hidden_until_outer_close(self):
        text = "{noalt}a {noalt}b{/noalt} c{/noalt}"

        self.assertEqual(filter_alt_text(text), "")

    def test_nested_different_filter_tags_stay_hidden_until_outer_close(self):
        text = "{noalt}hidden {rt}ruby{/rt} still hidden{/noalt}visible"

        self.assertEqual(filter_alt_text(text), "visible")

    def test_unmatched_close_does_not_cancel_later_open(self):
        text = "{/noalt}before{noalt}hidden{noalt}inner{/noalt}hidden{/noalt}{/noalt}after"

        self.assertEqual(filter_alt_text(text), "beforeafter")
