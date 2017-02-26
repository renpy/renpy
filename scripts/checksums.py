#!/usr/bin/env python3

import argparse
import hashlib
import os
import subprocess


def hash_all(f, hash_name, hash_func, directory):
    f.write("\n")
    f.write("# {}\n".format(hash_name))

    extensions = [ ".zip", ".tar.gz", ".tar.bz2", ".exe" ]

    for fn in sorted(os.listdir(directory)):

        for e in extensions:
            if fn.endswith(e):
                break
        else:
            continue

        fullfn = os.path.join(directory, fn)

        with open(fullfn, "rb") as df:
            data = df.read()

        h = hash_func(data)
        f.write("{} {}\n".format(h.hexdigest(), fn))
        # print(h.hexdigest(), fn)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("directory")
    args = ap.parse_args()

    hashes = [ ("md5", hashlib.md5), ("sha1", hashlib.sha1), ("sha256", hashlib.sha256) ]

    checksum_fn = os.path.join(args.directory, "checksums.txt")

    with open(checksum_fn, "w") as f:

        for name, func in hashes:
            hash_all(f, name, func, args.directory)

        f.write("\n\n")

    if os.path.exists(checksum_fn + ".asc"):
        os.unlink(checksum_fn + ".asc")

    subprocess.check_call([ "gpg2", "--clearsign", checksum_fn ])
    os.rename(checksum_fn + ".asc", checksum_fn)

if __name__ == "__main__":
    main()
