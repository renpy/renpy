#!/usr/bin/env python

import sys
sys.path.append('/home/tom/ab/keys/')

import argparse
import os
import zlib
import bz2
import hashlib
import public
import private
import time

def sha(s):
    """
    Hashes s into a string.
    """

    hash = hashlib.sha256()
    hash.update(s)
    return hash.hexdigest()


ap = argparse.ArgumentParser()
ap.add_argument("root")
args = ap.parse_args()

root = args.root

# A list of command strings.
commands = [ ]

for dir, dirs, files in os.walk(root):

    for fn in dirs + files:

        path = os.path.join(dir, fn)
        relpath = os.path.relpath(path, root)

        if relpath in [ "version", "catalog1.bz2" ]:
            continue
        
        if os.path.isdir(path):
            commands.append(('dir', "base", relpath))

        elif relpath.endswith(".bz2"):

            hash = sha(bz2.BZ2File(path, "r").read())
            size = "%d" % (os.path.getsize(path))

            commands.append(('file', hash, size, "base", relpath[:-4]))

            if os.access(path, os.X_OK):
                commands.append(('xbit', relpath[:-4]))
            
        else:
            print "Unknown non-directory, non-bz2-file:", path

out = bz2.BZ2File(os.path.join(root, "catalog1.bz2"), "w")
hash = hashlib.sha256()

for i in commands:

    line = "\t".join(i) + "\n"
    hash.update(line)
    out.write(line)

unsigned = int("01" + hash.hexdigest(), 16)
signed = pow(unsigned, private.exponent, public.modulus)

out.write("-\n")
out.write("signature\t%x\n" % signed)

out.close()
            
f = file(os.path.join(root, "version"), "w")
f.write(str(int(time.time())))
f.write("\n")
f.write("Test Update.")
f.close()

