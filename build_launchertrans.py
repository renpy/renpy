1#!/usr/bin/env python

import glob
import re
from sets import Set as set
import sys

seen_files = set()
seen_strings = set()

def tl(fn, s):

    s = eval(s)

    if len(s) < 3:
        return
    
    if s in seen_strings:
        return

    if fn not in seen_files:
        print >>out
        print >>out, "    # Translatable strings found in", fn
        print >>out
        seen_files.add(fn)

    print >>out, "    config.translations[%r] = %r" % (s, s)
    seen_strings.add(s)

def process(fn):
    
    data = file(fn).read()

    for m in re.finditer(r'\bu\"(\\"|[^"])+\"', data):
        tl(fn, m.group(0))

    for m in re.finditer(r"\bu\'(\\'|[^'])+\'", data):
        tl(fn, m.group(0))

if __name__ == "__main__":

    # out = file("extras/translations.rpy", "w")
    out = sys.stdout
    
    print >>out, "# This file contains a list of all of the phrases you can translate"
    print >>out, "# from the Ren'Py launcher."
    print >>out, ""
    print >>out, "init python:"

    for fn in glob.glob("launcher/*.rpy"):
        process(fn)
