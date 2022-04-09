#!/usr/bin/env python

import sys
import os
import re

import pathlib
base = pathlib.Path(__file__).absolute().parent.parent


def main():

    with open(base / "launcher" / "game" / "installer.rpy", "w") as out:
        out.write("""
# This file imports the extensions API into the default store, and makes it
# also contains the strings used by the extensions API, so the Ren'Py translation
# framework can find them.

init python:
    import installer

init python hide:
""")

        fn = base / "launcher" / "game" / "installer.py"

        with open(fn) as f:
            data = f.read()

        for m in re.finditer(r'__?\(".*?"\)', data):
            out.write("    " + m.group(0) + "\n")


if __name__ == "__main__":
    main()
