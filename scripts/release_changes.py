#!/usr/bin/env python3

import argparse
import zipfile
import re
import pathlib
import collections


def index_file(index, fn):

    m = re.search(r'((atom-)?\w+).zip', str(fn))
    if not m:
        return

    base = m.group(1)

    zf = zipfile.ZipFile(fn)
    for zi in zf.infolist():
        _basedir, _, filename = zi.filename.partition("/")
        index[base + "/" + filename] = zi.compress_size




def index_directory(dn):
    rv = collections.defaultdict(int)

    p = pathlib.Path(dn)

    if not p.exists():
        p = pathlib.Path(__file__).parent / "../dl" / dn


    for i in p.iterdir():
        index_file(rv, i)

    return rv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("old", help="Either a path to a directory containing the Ren'Py downloads, or a version.")
    ap.add_argument("new", help="Either a path to a directory containing the Ren'Py downloads, or a version.")
    ap.add_argument("prefix", default="", nargs='?', help="If given, only show results with this prefix.")
    ap.add_argument("--all", action="store_true", help="If given, show files that didn't change.")
    ap.add_argument("--dirs", action="store_true", help="If given, show directories.")
    ap.add_argument("--changed", action="store_true", help="If given, show files that have changed size.")

    args = ap.parse_args()

    old_index = index_directory(args.old)
    new_index = index_directory(args.new)

    all_files = list(set(old_index) | set(new_index))
    all_files.sort()

    print("{:>12s} {:>12s}".format("Old Size", "New Size"))
    print()

    for fn in all_files:
        old_size = old_index[fn]
        new_size = new_index[fn]

        if args.changed:
            if old_size == new_size:
                continue
        elif not args.all:
            if bool(old_size) == bool(new_size):
                continue

        if not args.dirs:
            if fn.endswith("/"):
                continue

        if not fn.startswith(args.prefix):
            continue

        print(f"{old_size:12,d} {new_size:12,d} {fn}")


if __name__ == "__main__":
    main()
