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

import unittest
from types import SimpleNamespace

from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy.display.ime import IMECandidates, place_candidates


class TestIMECandidates(unittest.TestCase):
    def test_from_event(self):
        ev = SimpleNamespace(candidates=["a", "b", "c"], selected=1, horizontal=True)
        self.assertEqual(IMECandidates.from_event(ev), IMECandidates(("a", "b", "c"), 1, True))

    def test_from_event_empty(self):
        self.assertIsNone(IMECandidates.from_event(SimpleNamespace(candidates=[], selected=-1, horizontal=False)))
        self.assertIsNone(IMECandidates.from_event(SimpleNamespace()))

    def test_from_event_out_of_range_selection(self):
        for selected in (-1, 3, 12):
            ev = SimpleNamespace(candidates=["a", "b", "c"], selected=selected, horizontal=False)
            self.assertEqual(IMECandidates.from_event(ev).selected, -1)


class TestPlaceCandidates(unittest.TestCase):
    def test_below(self):
        self.assertEqual(place_candidates((100, 100, 10, 20), (50, 40), (800, 600)), (100, 120))

    def test_flip_above(self):
        self.assertEqual(place_candidates((100, 570, 10, 20), (50, 40), (800, 600)), (100, 530))

    def test_clamp_right(self):
        self.assertEqual(place_candidates((780, 100, 10, 20), (50, 40), (800, 600)), (750, 120))

    def test_clamp_when_no_room_above_or_below(self):
        self.assertEqual(place_candidates((100, 20, 10, 20), (50, 590), (800, 600)), (100, 10))


if __name__ == "__main__":
    unittest.main()
