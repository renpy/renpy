﻿# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

# Ren'Py archiver. This builds a Ren'Py archive file, and the
# associated index file. These files are really easy to
# reverse-engineer, but are probably better than nothing.

init python in archiver:

    import sys
    import random
    import glob

    from cPickle import dumps, HIGHEST_PROTOCOL


    class Archive(object):
        """
        Adds files from disk to a rpa archive.
        """

        def __init__(self, filename):

            # The archive file.
            self.f = open(filename, "wb")

            # The index to the file.
            self.index = _dict()

            # A fixed key minimizes difference between archive versions.
            self.key = 0x42424242

            padding = "RPA-3.0 XXXXXXXXXXXXXXXX XXXXXXXX\n"
            self.f.write(padding)

        def add(self, name, path):
            """
            Adds a file to the archive.
            """

            self.index[name] = _list()

            with open(path, "rb") as df:
                data = df.read()
                dlen = len(data)

            # Pad.
            padding = "Made with Ren'Py."
            self.f.write(padding)

            offset = self.f.tell()

            self.f.write(data)

            self.index[name].append((offset ^ self.key, dlen ^ self.key, ""))

        def close(self):

            indexoff = self.f.tell()

            self.f.write(dumps(self.index, HIGHEST_PROTOCOL).encode("zlib"))

            self.f.seek(0)
            self.f.write("RPA-3.0 %016x %08x\n" % (indexoff, self.key))

            self.f.close()

