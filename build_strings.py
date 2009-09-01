#!/usr/bin/env python

import collections
import glob
import re
import sys
import time
import os

# A map from string to filename, line number where the string is found.
strings = collections.defaultdict(list)

def process(fn):

    lineno = 0
    
    for data in file(fn, "r"):

        lineno += 1

        matches = [ ]
        
        matches += re.finditer(r'\bu\"(\\"|[^"])+\"', data)
        matches += re.finditer(r"\bu\'(\\'|[^'])+\'", data)

        for m in matches:
            s = m.group(0)[2:-1]

            if "\\u" in s:
                continue

            if len(s) == 1:
                continue
            
            strings[s].append("%s:%d" % (fn, lineno))

if __name__ == "__main__":

    files = [ ]

    files += glob.glob("launcher/*.rpy")
    files += glob.glob("common/*.rpy")
    files += glob.glob("common/_layout/*.rpym")
    files += glob.glob("common/_compat/*.rpym")

    if "launcher/strings.rpy" in files:
        files.remove("launcher/strings.rpy")
    
    for fn in files:
        process(fn)

    converse = [ ]
        
    for k, v in strings.iteritems():
        v = " ".join(sorted(v))
        converse.append((v, k))

    converse.sort()

    f = file("launcher/strings.rpy", "w")

    files = set(i for i in os.listdir("launcher") if i.endswith(".rpy"))
    
    print >>f, """\
init python:
    LAUNCHER_RPYS = %r

    TRANSLATION_STRINGS = [
""" % files
    
    for v, k in converse:
        # print
        # print "#:", v
        # print "#, python-format"

        print >>f, "        u\"%s\"," % unicode(k)

    print >>f, """\
    ]
"""
