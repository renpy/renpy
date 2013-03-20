#!/usr/bin/env python

import os.path
import sys
import re

ENDINGS = [
    ".rpy",
    ".rpym",
    ".py",
    ".pyx",
    ]


def process(root):

    for dirname, _dirs, files in os.walk("renpy"):
        for fn in files:
            fn = os.path.join(dirname, fn)

            for i in ENDINGS:
                if fn.endswith(i):
                    break
            else:
                continue

            lines = []

            with open(fn, "rb") as f:
                for l in f:
                    l = re.sub(
                        r"Copyright (\d{4})-\d{4} Tom Rothamel",
                        r"Copyright \1-2013 Tom Rothamel",
                        l)

                    lines.append(l)

            with open(fn, "wb") as f:
                f.write("".join(lines))

process("root")
process("module")
