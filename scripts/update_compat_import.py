#!/usr/bin/env python3

import pathlib
import collections
import re

ROOT = pathlib.Path(__file__).parent.parent

IMPORT_LINE = "from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *\n"

def main():

    modules = [ ]

    # .py modules.
    for p in (ROOT / "renpy").glob("**/*.py"):

        text = p.read_text()
        text = re.sub(r'^from renpy.compat import(.*)*$', IMPORT_LINE, text, flags=re.MULTILINE)
        p.write_text(text)

if __name__ == "__main__":
    main()
