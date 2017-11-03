from __future__ import print_function
# Fixes line endings and adds UTF-8 BOM to all rpy files in a
# directory.

import sys

def process(fn):
    with open(fn, "rb") as f:
        data = f.read()

    data = data.decode("utf-8")
    data = data.replace("\r", "")
    data = data.replace(u"\ufeff", "")
    data = u"\ufeff" + data
    data = data.encode("utf-8")

    with open(fn, "wb") as f:
        f.write(data)

import os

for directory, dirs, files in os.walk(sys.argv[1]):
    for fn in files:
        fn = os.path.join(directory, fn)

        if not fn.endswith(".rpy"):
            continue

        print(fn)
        process(fn)
