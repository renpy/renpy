#!/usr/bin/env python3

import sys
import re
import subprocess

# Things to check on an ongoing basis:
#
# * No .iter methods.
# * No print(file=...)



VERBOTEN0 = [
    "keys",
    "items",
    "values",
    ]

VERBOTEN = [
    "six",
    "cPickle",

    "iteritems",
    "itervalues",
    "iterkeys",
    "has_key",

    "unichr",
    "chr",

    "unicode",

    ]

def process(fn):
    subprocess.call(["futurize", "-x", "lib2to3.fixes.fix_dict", fn])

    print("--------------------------")

    with open(fn) as f:

        for i, l in enumerate(f):
            found = False
            i += 1

            for j in VERBOTEN0:
                if re.search(r'\b' + j + r'\b', l):
                    found = True

            if found:
                l = l.rstrip()
                print(f"{i:04d} {l}")

    print("--------------------------")

    with open(fn) as f:

        for i, l in enumerate(f):
            found = False
            i += 1

            for j in VERBOTEN:
                if re.search(r'\b' + j + r'\b', l):
                    found = True

            if found:
                l = l.rstrip()
                print(f"{i:04d} {l}")




def main():
    for fn in sys.argv[1:]:
        process(fn)


if __name__ == "__main__":
    main()
