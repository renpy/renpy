#!/usr/bin/env python
#@PydevCodeAnalysisIgnore
# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
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
import sys
import warnings

# Functions to be customized by distributors. ################################

# Given the Ren'Py base directory (usually the directory containing
# this file), this is expected to return the path to the common directory.
def path_to_common(renpy_base):
    return renpy_base + "/renpy/common"

# Given a directory holding a Ren'Py game, this is expected to return
# the path to a directory that will hold save files.
def path_to_saves(gamedir):
    import renpy #@UnresolvedImport
    
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

    # Otherwise, put the saves in a platform-specific location.
    if renpy.android:
        return gamedir + "/saves"

    elif renpy.macintosh:
        rv = "~/Library/RenPy/" + renpy.config.save_directory
        return os.path.expanduser(rv)

    elif renpy.windows:
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
macos_version = (6, 14, 0)
linux_version = (6, 14, 0)

# Doing the version check this way also doubles as an import of ast,
# which helps py2exe et al.
try:
    import ast; ast
except:
    raise
    print "Ren'Py requires at least python 2.6."
    sys.exit(0)

android = ("ANDROID_PRIVATE" in os.environ)

# Android requires us to add code to the main module, and to command some
# renderers.
if android:
    __main__ = sys.modules["__main__"]
    __main__.path_to_renpy_base = path_to_renpy_base
    __main__.path_to_common = path_to_common
    __main__.path_to_saves = path_to_saves
    os.environ["RENPY_RENDERER"] = "gl"
    os.environ["RENPY_GL_ENVIRON"] = "limited"
    
def main():
    
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

    if android:
        renpy.linux = False
        renpy.android = True
    
    renpy.bootstrap.bootstrap(renpy_base)

if __name__ == "__main__":
    main()

    
