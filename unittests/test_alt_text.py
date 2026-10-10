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

    def test_nested_same_tags_stay_hidden_until_outer_close(self):
        for tag in renpy.config.tts_filter_tags:
            with self.subTest(tag=tag):
                text = "{%s}hidden {%s}inner{/%s} leaked{/%s} visible" % (tag, tag, tag, tag)
                self.assertEqual(filter_alt_text(text), " visible")

    def test_nested_different_tags_stay_hidden_until_outer_close(self):
        self.assertEqual(filter_alt_text("{noalt}hidden {rt}ruby{/rt} still hidden{/noalt}visible"), "visible")

    def test_unmatched_close_does_not_cancel_later_open(self):
        self.assertEqual(
            filter_alt_text("{/noalt}before{noalt}hidden{noalt}inner{/noalt}hidden{/noalt}{/noalt}after"),
            "beforeafter",
        )

    def test_unclosed_outer_tag_keeps_text_hidden(self):
        self.assertEqual(filter_alt_text("before{noalt}hidden{noalt}inner{/noalt}hidden"), "before")

    def test_arguments_and_formatting_tags(self):
        self.assertEqual(
            filter_alt_text("{b}before{/b}{noalt=value}hidden{noalt}inner{/noalt}hidden{/noalt}{alt}after{/alt}"),
            "beforeafter",
        )
