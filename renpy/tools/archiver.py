# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
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

#!/usr/bin/env python

# The Ren'Py archiver. This builds a Ren'Py archive file, and the
# associated index file. These files are really easy to reverse-engineer,
# but are probably better than nothing.

import sys
import encodings.zlib_codec; encodings.zlib_codec # E0601
import random
import glob

from cPickle import dumps, HIGHEST_PROTOCOL

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

    key = random.randint(0, 0x7ffffffe)
    
    padding = "RPA-3.0 XXXXXXXXXXXXXXXX XXXXXXXX\n" # W0511

    archivef.write(padding)
    offset = len(padding)

    # Needed because windows sucks. It doesn't do globbing on the
    # command line.

    for fullfn, shortfn in files:

        # if shortfn.lower().endswith(".ttf"):
        #    continue
        
        shortfn = shortfn.replace("\\", "/")

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
            start = data[:16]
            rest = data[16:]
            
            archivef.write(rest)

            index[shortfn].append((offset ^ key, dlen ^ key, start))
            offset += len(rest)
                      
        datafile.close()

    indexoff = offset

    archivef.write(dumps(index, HIGHEST_PROTOCOL).encode("zlib"))

    archivef.seek(0)
    archivef.write("RPA-3.0 %016x %08x\n" % (indexoff, key))

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
