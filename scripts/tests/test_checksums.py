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

"""Tests for computing the checksums of a release."""

import os

from scripts import checksums


def test_checksums_cover_every_download_format(tmp_path, monkeypatch):
    for fn in ["a.zip", "b.tar.gz", "c.tar.bz2", "d.exe", "e.dmg", "updates.json"]:
        (tmp_path / fn).write_bytes(b"data")

    def fake_gpg(command):
        """Stands in for gpg2 --clearsign, which writes the signed copy beside the input."""

        os.rename(command[-1], command[-1] + ".asc")

    monkeypatch.setattr(checksums.subprocess, "check_call", fake_gpg)
    monkeypatch.setattr("sys.argv", ["checksums.py", str(tmp_path)])

    checksums.main()

    text = (tmp_path / "checksums.txt").read_text()

    for fn in ["a.zip", "b.tar.gz", "c.tar.bz2", "d.exe", "e.dmg"]:
        assert text.count(" " + fn + "\n") == 3

    assert "updates.json" not in text
