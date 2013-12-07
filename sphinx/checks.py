from __future__ import print_function

import os
import re

def check_include():

    used = set()

    def scan_file(fn):
        f = open(fn)

        for l in f:
            m = re.search(r"\.\. include::(.+)", l)

            if not m:
                continue

            fn = m.group(1).strip()

            used.add(fn)

    for i in os.listdir("source"):
        if i.endswith(".rst"):
            scan_file(os.path.join("source", i))

    for i in os.listdir("source/inc"):
        scan_file(os.path.join("source", "inc", i))

    for i in os.listdir("source/inc"):
        fn = "inc/" + i
        if fn not in used:
            print("WARNING: source/{} is not used.".format(fn))

if __name__ == "__main__":
    check_include()
