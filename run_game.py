#!/usr/bin/env python

import os
import os.path
import sys

if __name__ == "__main__":

    # Check for mac compatibility.
    if "mac_version" in globals():
        mac_version((5, 3, 2))

    # Figure out the base directory.
    renpy_base = os.path.dirname(sys.argv[0])
    renpy_base = os.environ.get('RENPY_BASE', renpy_base)
    renpy_base = os.path.abspath(renpy_base)

    # Add paths.
    if os.path.exists(renpy_base + "/module"):
        sys.path.append(renpy_base + "/module")

    sys.path.append(renpy_base)

    if os.path.exists(renpy_base + "/renpy.zip"):
        sys.path.append(renpy_base + "/renpy.zip")
    

    # Start Ren'Py proper.
    import renpy.bootstrap
    renpy.bootstrap.bootstrap(renpy_base)

