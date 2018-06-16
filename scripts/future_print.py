#!/usr/bin/env python3

import sys


def process(fn):

    with open(fn) as f:
        lines = f.readlines()

    for i in lines:
        if "__future__" in i:
            print("Already in", fn)
            return

    line = 0

    for line, l in enumerate(lines):
        if "#" in l:
            continue

        if not l.strip():
            continue

        break

    print(fn, line)

    lines.insert(line, "from __future__ import print_function\n")
    lines.insert(line + 1, "\n")

    with open(fn, "w") as f:
        f.write(''.join(lines))


def main():

    for i in sys.argv[1:]:
        process(i)


if __name__ == "__main__":
    main()
