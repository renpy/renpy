#!/usr/bin/env python3

from __future__ import print_function

import os
import codecs

ENDINGS = [
    ".rpy",
    ".rpym",
    ]

BOM = "\ufeff"

def process_file(fn):

    for i in ENDINGS:
        if fn.endswith(i):
            break
    else:
        return

    print("Processing", fn)

    lines = [ ]
    with open(fn, "r") as f:
        for l in f:

            l = l.replace(BOM, "")

            if l.startswith("# TO" + "DO: Translation updated"):
                continue

            l = l.rstrip()
            l = l + "\n"

            lines.append(l)

    with open(fn, "w") as f:
        f.write(BOM + "".join(lines))


def process(root):

    for dirname, _dirs, files in os.walk(root):
        for fn in files:
            fn = os.path.join(dirname, fn)
            process_file(fn)


os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


process("launcher/game/tl")
process("templates")
process("tutorial/game/tl")
process("the_question/game/tl")
process("gui")
