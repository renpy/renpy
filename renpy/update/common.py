# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

import hashlib
import json
import os
import pickle
import zlib

def hash_data(data):
    """
    Given `data` (bytes), returns a hexadecimal hash of the data.
    """

    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def hash_list(data):
    """
    Hashes a list of strings.
    """

    return hash_data("\n".join(data).encode("utf-8"))


def dump(d):
    """
    Dumps a dictionary to a JSON string.
    """

    print(json.dumps(d, indent=2))


# Constants used for the compressed field of segments.
COMPRESS_NONE = 0
COMPRESS_ZLIB = 1

class Segment(object):
    """
    This represents a segment of a file conaining the data with the given
    hash.
    """

    def __init__(self, offset, size, hash, compressed):

        # The offset within the file.
        self.offset = offset

        # The size of the data.
        self.size = size

        # The hash of the data
        self.hash = hash

        # Determines if the data is compressed. This should be one of the
        # COMPRESS_* constants.
        self.compressed = compressed

    def __eq__(self, other):
        if not isinstance(other, Segment):
            return False

        return self.offset == other.offset and self.size == other.size and self.hash == other.hash and self.compressed == other.compressed

    def to_json(self):
        return {
            "offset" : self.offset,
            "size" : self.size,
            "hash" : self.hash,
            "compressed" : self.compressed }

    @staticmethod
    def from_json(d):
        rv = Segment(d["offset"], d["size"], d["hash"], d["compressed"])
        return rv


class Directory(object):
    """
    Represents a directory.
    """

    def __init__(self, name):
        self.name = name.replace("\\", "/")

    def to_json(self):
        return { "name" : self.name }

    @staticmethod
    def from_json(d):
        rv = Directory(d["name"])
        return rv

class File(object):
    """
    Represents a file.
    """

    def __init__(self, name, data_filename=None, segments=None, mtime=0, xbit=False):

        # The name of the file. This is the name that can be stored.
        self.name = name.replace("\\", "/")

        # If the actual content of the file is stored somewhere else, this is
        # the name of the file it is stored in.
        self.data_filename = data_filename.replace("\\", "/") if data_filename else None

        # The segments of the file. This is a list of Segment objects.
        self.segments = segments or [ ]

        # The modification time of the file.
        self.mtime = mtime

        # If true, the file is executable.
        self.xbit = xbit

    def to_json(self):
        return {
            "name" : self.name,
            "segments" : [ i.to_json() for i in self.segments ],
            "xbit" : self.xbit,
        }

    @staticmethod
    def from_json(d):
        rv = File(d["name"], segments=[ Segment.from_json(i) for i in d["segments"] ], xbit=d["xbit"])
        return rv

    def scan_segments(self, f, offset, size):
        """
        Split a file into segments that are less than 2MB in size.

        `f`
            The open file.

        `offset`
            The offset of the file within the file.

        `size`
            The size of the data to divide into segments.
        """

        f.seek(offset)

        while size > 0:
            segment_size = min(size, 2 * 1024 * 1024)

            data = f.read(segment_size)

            seg = Segment(offset, len(data), hash_data(data), COMPRESS_NONE)
            self.segments.append(seg)

            offset += len(data)
            size -= len(data)


    def scan_rpa(self, f, total_size):
        """
        Scans an RPA archive, segmenting it into the underlying files.
        """

        # Read the header.
        l = f.read(40)
        offset = int(l[8:24], 16)
        key = int(l[25:33], 16)
        f.seek(offset)
        index = pickle.loads(zlib.decompress(f.read()))


        # This is a list of offset, size tuples for each of the files
        # in the archive. These will be sorted into the order the segments
        # appear in the archive.
        segments = [ ]

        for v in index.values():
            for i in v:
                segments.append((i[0] ^ key, i[1] ^ key))

        segments.sort()

        # Iterate through, adding a segment for each block in the .rpa.
        pos = 0

        for offset, size in segments:
            self.scan_segments(f, pos, offset - pos)
            self.scan_segments(f, offset, size)
            pos = offset + size

        self.scan_segments(f, pos, total_size - pos)


    def scan(self):
        """
        Separate the file into segments. This may be done in a content-aware
        way, if required.
        """

        fn = self.data_filename or self.name

        self.mtime = os.path.getmtime(fn)

        self.segments = [ ]

        with open(fn, "rb") as f:

            start = f.read(1024)

            # Determine the size of the file.
            f.seek(0, 2)
            size = f.tell()
            f.seek(0)

            if self.name.endswith(".rpa") and start[:8] == b'RPA-3.0 ':
                try:
                    self.scan_rpa(f, size)
                    return
                except Exception:
                    pass

            self.scan_segments(f, 0, size)

    def add_data_filename(self, path):
        """
        Sets the data_filename of this file to the name of the file, relative
        to `path`.
        """

        self.data_filename = os.path.join(path, self.name)


class FileList(object):
    """
    Represents a list of files and directories.
    """

    def __init__(self):
        self.directories = [ ]
        self.files = [ ]
        self.blocks = [ ]

    def to_json(self):
        return {
            "directories" : [ i.to_json() for i in self.directories ],
            "files" : [ i.to_json() for i in self.files ],
            "blocks" : [ i.to_json() for i in self.blocks ],
        }

    @staticmethod
    def from_json(d):
        rv = FileList()
        rv.directories = [ Directory.from_json(i) for i in d["directories"] ]
        rv.files = [ File.from_json(i) for i in d["files"] ]
        rv.blocks = [ File.from_json(i) for i in d["blocks"] ]
        return rv

    def to_current_json(self):
        """
        Returns a JSON representation of the file list that can be used
        in the current.json files.
        """

        return {
            "directories" : [ i.name for i in self.directories ],
            "files" : [ i.name for i in self.files ],
            "xbit" : [ i.name for i in self.files if i.xbit ],
        }

    @staticmethod
    def from_current_json(d):
        xbit = set(d["xbit"])

        rv = FileList()

        for i in d["directories"]:
            rv.directories.append(Directory(i))

        for i in d["files"]:
            rv.files.append(File(i, xbit=i in xbit))

        return rv

    def add_directory(self, name):
        """
        Called from the launcher to add a directory to this file list.
        """
        self.directories.append(Directory(name))

    def add_file(self, name, path, xbit):
        """
        Called from the launcher to add a file to this file list.
        """

        self.files.append(File(name, data_filename=path, xbit=xbit))


    def scan(self, root, data_filename=True):
        """
        Scan a directory, recursively, and add the files and directories
        found to this file test. This is intended for testing. This does
        not call .scan on the files.
        """

        for dn, dirs, files in os.walk(root):

            for d in dirs:
                d = os.path.relpath(os.path.join(dn, d), root)
                self.directories.append(Directory(d))

            for fn in files:
                fn = os.path.join(dn, fn)
                relfn = os.path.relpath(fn, root)

                if data_filename:
                    xbit = os.access(fn, os.X_OK)
                else:
                    xbit = False

                f = File(relfn, data_filename=fn if data_filename else None, xbit=xbit)
                self.files.append(f)

        self.directories.sort(key=lambda x : x.name)
        self.files.sort(key=lambda x : x.name)

    def encode(self):
        """
        Encode the file list into a file.
        """

        data = json.dumps(self.to_json()).encode("utf-8")
        return zlib.compress(data, 3)

    @staticmethod
    def decode(data):
        """
        Decode the file list from a file.
        """

        data = zlib.decompress(data)
        return FileList.from_json(json.loads(data.decode("utf-8")))
