#!/usr/bin/env python

# Given two zip files, shows how files have changed in size between
# them.

from __future__ import print_function
import argparse
import zipfile
import collections


def size_zip(fn):
    zf = zipfile.ZipFile(fn)
    rv = { }

    for zi in zf.infolist():
        _basedir, _, filename = zi.filename.partition("/")

        rv[filename] = zi.compress_size

    return rv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zip")
    args = ap.parse_args()

    files = size_zip(args.zip)

    dirsizes = collections.defaultdict(int)

    for k, v in files.items():
        while k:
            k, _, _ = k.rpartition('/')
            dirsizes[k] += v

    sizes = [ (v, k) for (k, v) in dirsizes.items() ]
    sizes.sort()

    for v, k in sizes:
        print("{: 9d} {}".format(v, k))


if __name__ == "__main__":
    main()
