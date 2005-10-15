#!/usr/bin/env python

# The Ren'Py archiver. This builds a Ren'Py archive file, and the
# associated index file. These files are really easy to reverse-engineer,
# but are probably better than nothing.

import sys
import os
import encodings.zlib_codec
import random
import glob

from cPickle import loads, dumps, HIGHEST_PROTOCOL

# The most we will go without inserting some padding. 10k.
padding_every = 10240

# The amount of padding we will add.
padding_max = 4

def randpadding():

    plen = random.randint(1, padding_max)

    rv = ""

    for i in range(0, plen):
        rv += chr(random.randint(1, 255))

    return rv

def main():
    if len(sys.argv) < 3:
        print "Usage: %s <file-prefix> <files ...>" % sys.argv[0]
        return

    prefix = sys.argv[1]

    # Archive file.
    archivef = file(prefix + ".rpa", "wb")

    # Index file.
    indexf = file(prefix + ".rpi", "wb")

    index = { }

    random.seed()

    offset = 0

    # Needed because windows sucks. It doesn't do globbing on the
    # command line.
    files = [ ]
    for i in sys.argv[2:]:
        files.extend(glob.glob(i))

    for fn in files:
        index[fn] = [ ]

        print "Adding %s..." % fn

        datafile = file(fn, "rb")

        while True:

            # Pad with junk.
            padding = randpadding()
            archivef.write(padding)
            offset += len(padding)

            # Pick a random block size.
            block = random.randint(1, padding_every)

            data = datafile.read(block)

            if not data:
                break

            dlen = len(data)

            archivef.write(data)

            index[fn].append((offset, dlen))
            offset += dlen
                      
        datafile.close()

    archivef.close()

    indexf.write(dumps(index, HIGHEST_PROTOCOL).encode("zlib"))
    indexf.close()
    
    

if __name__ == "__main__":
    main()
