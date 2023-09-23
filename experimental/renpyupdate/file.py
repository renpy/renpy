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

def dump(d):
    """
    Dumps a dictionary to a JSON string.
    """

    print(json.dumps(d, indent=2))

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

    def to_json(self):
        return {
            "offset" : self.offset,
            "size" : self.size,
            "hash" : self.hash,
            "compressed" : self.compressed }


class Directory(object):
    """
    Represents a directory.
    """

    def __init__(self, name):
        self.name = name.replace("\\", "/")

    def to_json(self):
        return { "name" : self.name }

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
                self.scan_rpa(f, size)
                return

            self.scan_segments(f, 0, size)

class FileList(object):
    """
    Represents a list of files and directories.
    """

    def __init__(self):
        self.directories = [ ]
        self.files = [ ]

    def to_json(self):
        return {
            "directories" : [ i.to_json() for i in self.directories ],
            "files" : [ i.to_json() for i in self.files ]
        }

    def scan(self, root):
        """
        Scan a directory, recursively.
        """

        for dn, dirs, files in os.walk(root):

            for d in dirs:
                d = os.path.relpath(os.path.join(dn, d), root)
                self.directories.append(Directory(d))

            for fn in files:
                fn = os.path.join(dn, fn)
                relfn = os.path.relpath(fn, root)
                f = File(relfn, data_filename=fn)
                f.scan()
                self.files.append(f)

        self.directories.sort(key=lambda x : x.name)
        self.files.sort(key=lambda x : x.name)


if __name__ == "__main__":
    import sys

    fl = FileList()
    fl.scan(sys.argv[1])
    dump(fl.to_json())
