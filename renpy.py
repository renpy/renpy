#!/usr/bin/env python

# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import os.path
import sys
import platform
import warnings

# Functions to be customized by distributors. ################################

# Given the Ren'Py base directory (usually the directory containing
# this file), this is expected to return the path to the common directory.
def path_to_common(renpy_base):
    return renpy_base + "/common"

# Given a directory holding a Ren'Py game, this is expected to return
# the path to a directory that will hold save files.
def path_to_saves(gamedir):
    import renpy
    
    if not renpy.config.save_directory:
        return gamedir + "/saves"

    # Search the path above Ren'Py for a directory named "Ren'Py Data".
    # If it exists, then use that for our save directory.
    path = renpy.config.renpy_base

    while True:
        if os.path.isdir(path + "/Ren'Py Data"):
            return path + "/Ren'Py Data/" + renpy.config.save_directory

        newpath = os.path.dirname(path)
        if path == newpath:
            break
        path = newpath

    # Otherwise, put the saves in a standard place.
    if platform.mac_ver()[0]:
        rv = "~/Library/RenPy/" + renpy.config.save_directory
        return os.path.expanduser(rv)
    elif sys.platform == "win32":
        if 'APPDATA' in os.environ:
            return os.environ['APPDATA'] + "/RenPy/" + renpy.config.save_directory
        else:
            rv = "~/RenPy/" + renpy.config.save_directory
            return os.path.expanduser(rv)
    else:
        rv = "~/.renpy/" + renpy.config.save_directory
        return os.path.expanduser(rv)

        
# Returns the path to the Ren'Py base directory (containing common and
# the launcher, usually.)
def path_to_renpy_base():
    renpy_base = os.path.dirname(sys.argv[0])
    renpy_base = os.environ.get('RENPY_BASE', renpy_base)
    renpy_base = os.path.abspath(renpy_base)

    return renpy_base


##############################################################################

# The version of the Mac Launcher and py4renpy that we require.
macos_version = (6, 10, 1)
linux_version = (6, 10, 1)

if __name__ == "__main__":

    if not 'RENPY_NO_VERSION_CHECK' in os.environ:

        # Check for mac compatibility.
        if "mac_version" in globals():
            globals()["mac_version"](macos_version)

        # Check py4renpy compatibility.
        try:
            import py4renpy
            if py4renpy.version < linux_version:
                print "The version of py4renpy that you are using is too old. Please go to"
                print "http://www.bishoujo.us/renpy/linux.html, and download the latest"
                print "version."
                sys.exit(-1)
        except ImportError:
            pass

    renpy_base = path_to_renpy_base()

    # Add paths.
    if os.path.exists(renpy_base + "/module"):
        sys.path.append(renpy_base + "/module")

    sys.path.append(renpy_base)

    # This is looked for by the mac launcher.
    if os.path.exists(renpy_base + "/renpy.zip"):
        sys.path.append(renpy_base + "/renpy.zip")

    # Ignore warnings that happen.
    warnings.simplefilter("ignore", DeprecationWarning)
        
        
    # Start Ren'Py proper.
    try:
        import renpy.bootstrap
    except ImportError:
        print >>sys.stderr, "Could not import renpy.bootstrap. Please ensure you decompressed Ren'Py"
        print >>sys.stderr, "correctly, preserving the directory structure."
        raise

    renpy.bootstrap.bootstrap(renpy_base)
