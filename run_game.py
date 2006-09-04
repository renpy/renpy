#!/usr/bin/env python

import os
import os.path
import sys

# The version of the Mac Launcher and py4renpy that we use.
mac_linux_version = (5, 6, 0)

if __name__ == "__main__":

    # Check for mac compatibility.
    if "mac_version" in globals():
        mac_version(mac_linux_version)

    # Check py4renpy compatibility.
    try:
        import py4renpy
        if py4renpy.version < mac_linux_version:
            print "The version of py4renpy that you are using is too old. Please go to"
            print "http://www.bishoujo.us/renpy/linux.html, and download the latest"
            print "version."
            sys.exit(-1)
    except ImportError:
        pass

    # Figure out the base directory.
    renpy_base = os.path.dirname(sys.argv[0])
    renpy_base = os.environ.get('RENPY_BASE', renpy_base)
    renpy_base = os.path.abspath(renpy_base)

    # Add paths.
    if os.path.exists(renpy_base + "/module"):
        sys.path.append(renpy_base + "/module")

    sys.path.append(renpy_base)

    # This is looked for by the mac launcher.
    if os.path.exists(renpy_base + "/renpy.zip"):
        sys.path.append(renpy_base + "/renpy.zip")


    # Start Ren'Py proper.
    import renpy.bootstrap
    renpy.bootstrap.bootstrap(renpy_base)
