#!/usr/bin/env python

# The Ren'Py archiver. This builds a Ren'Py archive file, and the
# associated index file. These files are really easy to reverse-engineer,
# but are probably better than nothing.

import sys
import os
import encodings.zlib_codec

from cPickle import loads, dumps, HIGHEST_PROTOCOL

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

    offset = 0

    for fn in sys.argv[2:]:
        print "Adding %s..." % fn

        data = file(fn, "rb").read()
        dlen = len(data)

        archivef.write(data)

        index[fn] = (offset, dlen)
        offset += dlen

    archivef.close()

    indexf.write(dumps(index, HIGHEST_PROTOCOL).encode("zlib"))
    indexf.close()
    
    

if __name__ == "__main__":
    main()
