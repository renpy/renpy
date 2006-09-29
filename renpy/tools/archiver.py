#!/usr/bin/env python

# The Ren'Py archiver. This builds a Ren'Py archive file, and the
# associated index file. These files are really easy to reverse-engineer,
# but are probably better than nothing.

import sys
import os
import encodings.zlib_codec
import random
import glob

from pickle import loads, dumps, HIGHEST_PROTOCOL

# The amount of padding we will add.
padding_max = 64

def randpadding():

    plen = random.randint(1, padding_max)

    rv = ""

    for i in range(0, plen):
        rv += chr(random.randint(1, 255))

    return rv


# prefix is the path to the archive file, without the trailing .rpa.
# files is a list of (full filename, inside-archive filename) pairs.
def archive(prefix, files):
    
    # Archive file.
    archivef = file(prefix + ".rpa", "wb")

    index = { }

    random.seed()
    
    padding = "RPA-2.0 XXXXXXXXXXXXXXXX direct\n"

    archivef.write(padding)
    offset = len(padding)

    # Needed because windows sucks. It doesn't do globbing on the
    # command line.

    for fullfn, shortfn in files:
        index[shortfn] = [ ]

        print "Adding %s..." % shortfn

        datafile = file(fullfn, "rb")

        while True:

            # Pad with junk.
            padding = randpadding()
            archivef.write(padding)
            offset += len(padding)

            data = datafile.read()

            if not data:
                break

            dlen = len(data)

            archivef.write(data)

            index[shortfn].append((offset, dlen))
            offset += dlen
                      
        datafile.close()

    indexoff = offset

    archivef.write(dumps(index, HIGHEST_PROTOCOL).encode("zlib"))

    archivef.seek(0)
    archivef.write("RPA-2.0 %016x\n" % indexoff)

    archivef.close()
    
    
def main():

    if len(sys.argv) < 3:
        print "Usage: %s <file-prefix> <files ...>" % sys.argv[0]
        return

    prefix = sys.argv[1]

    # Needed because windows sucks. It doesn't do globbing on the
    # command line.
    files = [ ]
    for i in sys.argv[2:]:
        files.extend(glob.glob(i))

    files = [ (i, i) for i in files ]

    archive(prefix, files)
     
if __name__ == "__main__":
    main()
