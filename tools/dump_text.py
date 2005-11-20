#!/usr/bin/env python

# This program dumps all the text found in the script to stdout.

import codecs
import sys
import os
import re
import glob

import renpy

def process_block(block, out):

    for fn, ln, text, child in block:

        if text.startswith("$") or text.startswith("python"):
            continue

        if text.startswith("init"):
            continue

        if text.startswith("if") or text.startswith("while"):
            process_block(child, out)
            continue

        for m in re.finditer(r'"((?:[^\\"]+|\\.)+)"|' +
                             r"'((?:[^\\']+|\\.)+)'", text):

            s = m.group(1) or m.group(2)

            s = re.sub(r'\s+', ' ', s)
            s = re.sub(r'\\.', ' ', s)

            s = re.sub(r'\{.*?\}', '', s)

            print >>out, s.encode('utf-8')
            print >>out

        process_block(child, out)
        

def process(fn, out):

    block = renpy.parser.group_logical_lines(renpy.parser.list_logical_lines(fn))

    process_block(block, out)


def main():

    pattern = "game/*.rpy"

    if len(sys.argv) >= 2:
        pattern = sys.argv[1]

    files = glob.glob(pattern)
    files = [ i for i in files if not i.startswith("common/") ]

    out = sys.stdout
    out.write(codecs.BOM_UTF8)

    for fn in files:
        process(fn, out)

    out.close()


if __name__ == "__main__":
    main()
