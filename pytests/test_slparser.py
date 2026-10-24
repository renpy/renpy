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


"""Tests for screen-language execution that do not need a running game."""

import unittest

import renpy
from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy.display.screen import ScreenNotFound
from renpy.sl2.slast import SLContext, SLUse


class TestLegacyUse(unittest.TestCase):
    def test_missing_screen_restores_ui_stack(self) -> None:
        node = SLUse(("test_slparser.py", 1), "slparser_missing_screen", None, None, None, None)
        old_stack = list(renpy.ui.stack)

        with self.assertRaises(ScreenNotFound):
            node.execute_use_screen(SLContext())

        self.assertEqual(len(renpy.ui.stack), len(old_stack))
        self.assertTrue(all(a is b for a, b in zip(renpy.ui.stack, old_stack)))


if __name__ == "__main__":
    unittest.main()
