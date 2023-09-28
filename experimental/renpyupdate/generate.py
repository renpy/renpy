import argparse
import json
import os
import zlib

from . import filetypes
from .util import dump, hash_list


class BlockGenerator(object):
    """
    This generates the block file containing the segments for an update.
    """

    def __init__(self, name, filelist, targetdir, max_rpu_size=50 * 1024 * 1024):

        # The filelist being created.
        self.filelist = filelist

        # The current segment list.
        self.segments = [ ]

        # The target directory in which the segments will be stored.
        self.targetdir = targetdir

        # The hashes that have been seen alread,.
        self.seen_hashes = set()

        # The maximum size of an rpu file.
        self.max_rpu_size = max_rpu_size

        # If new.rpu is open, a file object for it.
        self.new_rpu = None

        # The filelist being created.
        self.generate()

        # Write the filelist to a file.
        with open(self.path(name + ".index.rpu"), "wb") as f:
            f.write(self.filelist.encode())

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

    def close_new_rpu(self):
        """
        Closes new.rpu, renaming it to its final filename, and adds an
        entry to the filelist.
        """

        if self.new_rpu is None:
            return

        self.new_rpu.close()
        self.new_rpu = None

        filename = hash_list([ i.hash for i in self.segments ]) + ".rpu"

        os.rename(self.path("new.rpu"), self.path(filename))

        self.filelist.blocks.append(filetypes.File(filename, segments=self.segments))
        self.segments = [ ]

    def generate_segment(self, f, seg):
        """
        Generates a segment into new.rpu.
        """

        if seg.hash in self.seen_hashes:
            return

        self.seen_hashes.add(seg.hash)

        f.seek(seg.offset)
        data = f.read(seg.size)

        # TODO: Determine if we should compress the data.

        self.open_new_rpu()

        offset = self.new_rpu.tell()
        size = len(data)
        compressed = filetypes.COMPRESS_NONE

        self.new_rpu.write(data)
        self.segments.append(filetypes.Segment(offset, size, seg.hash, compressed))

        if self.new_rpu.tell() > self.max_rpu_size:
            self.close_new_rpu()

    def generate(self):

        # Create a list of files by reverse mtime. The idea is that the newer
        # files will appear before the older ones, and so we won't have to pull
        # from older files to create a new one.
        files = list(self.filelist.files)
        files.sort(key=lambda x: (x.mtime, x.name))
        files.reverse()

        for file in files:
            file.scan()

            with open(file.data_filename or file.name, "rb") as f:
                for seg in file.segments:
                    self.generate_segment(f, seg)

        self.close_new_rpu()


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

    fl = filetypes.FileList()
    fl.scan(args.sourcedir)

    BlockGenerator("game", fl, args.targetdir)

if __name__ == "__main__":
    main()
