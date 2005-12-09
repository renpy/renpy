#!/usr/bin/env python

import os
import os.path
import sys

if __name__ == "__main__":

    # Figure out the base directory.
    renpy_base = os.path.dirname(sys.argv[0])
    renpy_base = os.environ.get('RENPY_BASE', renpy_base)
    renpy_base = os.path.abspath(renpy_base)

    # Add paths.
    sys.path.append(renpy_base + "/module")
    sys.path.append(renpy_base)

    # Start Ren'Py proper.
    import renpy.bootstrap
    renpy.bootstrap.bootstrap(renpy_base)

