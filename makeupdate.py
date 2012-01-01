#!/usr/bin/env python

import sys
sys.path.append('/home/tom/ab/keys/')

import os
import bz2
import hashlib
import public #@UnresolvedImport
import private #@UnresolvedImport
import shutil
import time

def sha(s):
    """
    Hashes s into a string.
    """

    hash = hashlib.sha256() #@ReservedAssignment
    hash.update(s)
    return hash.hexdigest()


def make_update(root, version):

    # A list of command strings.
    commands = [ ]

    for dir, dirs, files in os.walk(root): #@ReservedAssignment
        for fn in files:
            fn = os.path.join(dir, fn)

            oldf = file(fn, "rb")
            bzf = bz2.BZ2File(fn + ".bz2", "wb")
            bzf.write(oldf.read())
            bzf.close()
            oldf.close()

            shutil.copymode(fn, fn + ".bz2")
            os.unlink(fn)
            
    for dir, dirs, files in os.walk(root): #@ReservedAssignment

        all = set(dirs + files) #@ReservedAssignment

        for fn in dirs + files:

            path = os.path.join(dir, fn)
            relpath = os.path.relpath(path, root)

            if relpath in [ "version", "catalog1.bz2" ]:
                continue

            if os.path.isdir(path):
                commands.append(('dir', "base", relpath))

            elif relpath.endswith(".rpyc.bz2"):
                continue            
            elif relpath.endswith(".rpymc.bz2"):
                continue            
            elif relpath.endswith(".rpyb.bz2"):
                continue            

            elif relpath.endswith(".pyo.bz2") and relpath.replace(".pyo", ".py") in all:
                continue            
                
            elif relpath.endswith(".bz2"):

                hash = sha(bz2.BZ2File(path, "r").read()) #@ReservedAssignment
                size = "%d" % (os.path.getsize(path))

                commands.append(('file', hash, size, "base", relpath[:-4]))

                if os.access(path, os.X_OK):
                    commands.append(('xbit', relpath[:-4]))


    out = bz2.BZ2File(os.path.join(root, "catalog1.bz2"), "w")
    hash = hashlib.sha256() #@ReservedAssignment

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
    f.write(version + "-" + str(time.time()))
    f.write("\n")
    f.write("the latest Ren'Py pre-release")
    f.close()

