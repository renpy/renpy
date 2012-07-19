# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

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
            
