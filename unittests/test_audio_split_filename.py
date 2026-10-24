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


"""Tests for parsing partial-playback audio specs such as ``<loop 1.0>music.ogg``."""

import unittest

from unittests.renpy_test_support import initialize_renpy

initialize_renpy()

from renpy.audio.audio import AudioData, Channel


class TestSplitFilename(unittest.TestCase):
    def setUp(self) -> None:
        self.channel = Channel.__new__(Channel)
        self.channel.file_prefix = ""
        self.channel.file_suffix = ""

    def test_loop_spec_on_audio_data(self) -> None:
        data = b"audio data"
        filename = AudioData(data, "<loop 0.0005625>first.wav")

        first, start, _end, _volume = self.channel.split_filename(filename, False)
        self.assertEqual(start, 0.0)

        loop, start, end, _volume = self.channel.split_filename(filename, True)
        self.assertEqual(start, 27 / 48000)
        self.assertEqual(end, -1)

        for split in (first, loop):
            self.assertIsInstance(split, AudioData)
            self.assertEqual(str(split), "first.wav")
            self.assertEqual(split.data, data)


if __name__ == "__main__":
    unittest.main()
