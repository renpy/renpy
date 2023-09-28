import hashlib
import json
import os
import pickle
import zlib

from .util import dump, hash_data

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
            "mtime" : self.mtime,
            "xbit" : self.xbit,
        }

    @staticmethod
    def from_json(d):
        rv = File(d["name"], segments=[ Segment.from_json(i) for i in d["segments"] ], mtime=d["mtime"], xbit=d["xbit"])
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
                f = File(relfn, data_filename=fn if data_filename else None)
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
