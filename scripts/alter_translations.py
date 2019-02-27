#!/usr/bin/env python

from __future__ import print_function

import os.path
import codecs
import argparse

ENDINGS = [
    ".rpy",
    ".rpym",
    ]


def process_file(fn):

    for i in ENDINGS:
        if fn.endswith(i):
            break
    else:
        return

    print("Processing", fn)

    lines = [ ]
    with open(fn, "rb") as f:
        for l in f:

            l = l.replace(codecs.BOM_UTF8, "")

            l = l.replace(args.old, args.new)

            l = l.rstrip()
            l = l + "\n"

            lines.append(l)

    with open(fn, "wb") as f:
        f.write(codecs.BOM_UTF8 + "".join(lines))


def process(root):

    for dirname, _dirs, files in os.walk(root):
        for fn in files:
            fn = os.path.join(dirname, fn)
            process_file(fn)


os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


ap = argparse.ArgumentParser()
ap.add_argument("old")
ap.add_argument("new")
args = ap.parse_args()


process("launcher/game/tl")
process("templates")
process("tutorial/game/tl")
process("the_question/game/tl")
process("gui")
