#!/usr/bin/env python3

# Fixes line endings and adds UTF-8 BOM to all rpy files in a
# directory.

from __future__ import print_function
import os
import sys


def process(fn):
    with open(fn, "rb") as f:
        data = f.read()

    data = data.decode("utf-8")
    data = data.replace("\r", "")
    data = data.replace("\ufeff", "")
    data = "\ufeff" + data
    data = data.encode("utf-8")

    with open(fn, "wb") as f:
        f.write(data)


for dn in sys.argv[1:]:
    for directory, dirs, files in os.walk(dn):
        for fn in files:
            fn = os.path.join(directory, fn)

            if not fn.endswith(".rpy") or fn.endswith(".rpym") or fn.endswith(".py"):
                continue

            print(fn)
            process(fn)
