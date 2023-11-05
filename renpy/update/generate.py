# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import argparse
import json
import os
import zlib
import threading

from . import common


class BlockGenerator(object):
    """
    This generates the block file containing the segments for an update.
    """

    def __init__(self, targetdir, max_rpu_size=50 * 1024 * 1024):

        # Used to lock generation.
        self.lock = threading.Lock()

        # The target directory in which the segments will be stored.
        self.targetdir = targetdir

        # A map from hash to segment object.
        self.seen_hashes = dict()

        # The maximum size of an rpu file.
        self.max_rpu_size = max_rpu_size

        # Clean out files in the target directory.
        for i in os.listdir(targetdir):
            os.unlink(os.path.join(targetdir, i))

        # The following variables are changed by each call to generate. ########

        # The filelist being created.
        self.filelist = None

        # The current segment list.
        self.segments = [ ]

        # The set of hashes seen while processing the current file list.
        self.current_seen_hashes = set()

        # The following field is changed quite a bit. ##########################

        # If new.rpu is open, a file object for it.
        self.new_rpu = None

    def path(self, name):
        """
        Returns the path to a file in the target directory.
        """

        return os.path.join(self.targetdir, name)

    def open_new_rpu(self):
        """
        Opens the new.rpu file if it's closed.
        """

        if self.new_rpu is None:
            self.new_rpu = open(self.path("new.rpu"), "wb")
            self.new_rpu.write(b"RPU-BLOCK-1.0\r\n")

    def close_new_rpu(self):
        """
        Closes new.rpu, renaming it to its final filename, and adds an
        entry to the filelist.
        """

        if self.new_rpu is None:
            return

        self.new_rpu.close()
        self.new_rpu = None

        filename = common.hash_list([ i.hash for i in self.segments ]) + ".rpu"

        os.rename(self.path("new.rpu"), self.path(filename))

        if self.filelist is not None:
            self.filelist.blocks.append(common.File(filename, segments=self.segments))

        self.segments = [ ]

    def generate_segment(self, f, seg):
        """
        Generates a segment into new.rpu.
        """

        if seg.hash in self.current_seen_hashes:
            return

        self.current_seen_hashes.add(seg.hash)

        if seg.hash in self.seen_hashes:
            self.segments.append(self.seen_hashes[seg.hash])
            return

        f.seek(seg.offset)
        data = f.read(seg.size)

        if self.new_rpu and self.new_rpu.tell() + len(data) > self.max_rpu_size:
            self.close_new_rpu()

        self.open_new_rpu()

        compressed = common.COMPRESS_NONE

        cdata = zlib.compress(data, 3)

        if len(cdata) < len(data) * .95:
            data = cdata
            compressed = common.COMPRESS_ZLIB

        offset = self.new_rpu.tell()
        size = len(data)

        self.new_rpu.write(data)

        seg = common.Segment(offset, size, seg.hash, compressed)
        self.seen_hashes[seg.hash] = seg
        self.segments.append(seg)

    def generate(self, name, filelist, progress=None):

        with self.lock:

            self.filelist = common.FileList()

            self.segments = [ ]
            self.current_seen_hashes = set()

            # Create a list of files by reverse mtime. The idea is that the newer
            # files will appear before the older ones, and so we won't have to pull
            # from older files to create a new one.
            files = list(filelist.files)
            files.sort(key=lambda x: (x.mtime, x.name))
            files.reverse()

            for i, file in enumerate(files):

                if progress:
                    progress(i + 1, len(files))

                file.scan()

                with open(file.data_filename or file.name, "rb") as f:
                    for seg in file.segments:
                        self.generate_segment(f, seg)

            self.close_new_rpu()

            # Write the filelist to a file.
            with open(self.path(name + ".files.rpu"), "wb") as f:
                f.write(self.filelist.encode())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sourcedir")
    ap.add_argument("targetdir")

    args = ap.parse_args()

    from pathlib import Path

    targetdir = Path(args.targetdir)
    targetdir.mkdir(exist_ok=True)

    for i in targetdir.glob("*.rpu"):
        i.unlink()

    fl = common.FileList()
    fl.scan(args.sourcedir)

    BlockGenerator("game", fl, args.targetdir)

if __name__ == "__main__":
    main()
