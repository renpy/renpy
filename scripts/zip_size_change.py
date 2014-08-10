#!/usr/bin/env python

# Given two zip files, shows how files have changed in size between
# them.

import argparse
import zipfile

def size_zip(fn):
    zf = zipfile.ZipFile(fn)
    rv = { }

    for zi in zf.infolist():
        _basedir, _, filename = zi.filename.partition("/")

        rv[filename] = zi.compress_size

    return rv

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("old")
    ap.add_argument("new")

    args = ap.parse_args()

    old = size_zip(args.old)
    new = size_zip(args.new)

    all = list(set(old) | set(new))
    all.sort()

    for fn in all:
        old_size = old.get(fn, 0)
        new_size = new.get(fn, 0)

        if old_size == new_size:
            continue

        print "{: 6d} {}".format((new_size - old_size), fn)

if __name__ == "__main__":
    main()

