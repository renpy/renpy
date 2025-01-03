#!/usr/bin/env python3

from __future__ import print_function

import os.path
import re
import codecs

import datetime
year = datetime.date.today().year

ENDINGS = [
    ".rpy",
    ".rpym",
    ".py",
    ".pyx",
    ".pxd",
    ".pyi",
    ".pxf",
    ]

full_copyright="""\
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
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""


def process_file(fn):

    for i in ENDINGS:
        if fn.endswith(i):
            break
    else:
        return

    print("Processing", fn)

    lines = [ ]

    has_copyright = False
    first = True

    with open(fn, "r") as f:
        for l in f:
            l = re.sub(
                r"Copyright (\d{4})-\d{4} Tom Rothamel",
                r"Copyright \1-{} Tom Rothamel".format(year),
                l)

            if re.search(r"Copyright .* Tom Rothamel", l):
                if has_copyright:
                    continue

                has_copyright = True

            l = l.replace("# See LICENSE.txt for license details.", full_copyright)

            if first:
                if fn.endswith(".rpy") or fn.endswith(".rpym"):
                    if "\ufeff" not in l:
                        l = "\ufeff" + l

                first = False

            lines.append(l)

    with open(fn, "w") as f:
        f.write("".join(lines))


def process(root):

    for dirname, _dirs, files in os.walk(root): #type: ignore
        for fn in files:
            fn = os.path.join(dirname, fn)
            process_file(fn)


process_file("renpy.py")
process("renpy")
process("module")
process("launcher/game")
