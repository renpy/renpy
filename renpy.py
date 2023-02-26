#!/usr/bin/env python

# This file is part of Ren'Py. The license below applies to Ren'Py only.
# Games and other projects that use Ren'Py may use a different license.

# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function, absolute_import

import os
import sys
import warnings

# Functions to be customized by distributors. ################################

def path_to_gamedir(basedir, name):
    """
    Returns the absolute path to the directory containing the game
    scripts an assets. (This becomes config.gamedir.)

    `basedir`
        The base directory (config.basedir)
    `name`
        The basename of the executable, with the extension removed.
    """

    # A list of candidate game directory names.
    candidates = [ name ]

    # Add candidate names that are based on the name of the executable,
    # split at spaces and underscores.
    game_name = name

    while game_name:
        prefix = game_name[0]
        game_name = game_name[1:]

        if prefix == ' ' or prefix == '_':
            candidates.append(game_name)

    # Add default candidates.
    candidates.extend([ 'game', 'data', 'launcher/game' ])

    # Take the first candidate that exists.
    for i in candidates:

        if i == "renpy":
            continue

        gamedir = os.path.join(basedir, i)

        if os.path.isdir(gamedir):
            break

    else:
        gamedir = basedir

    return gamedir


def path_to_common(renpy_base):
    """
    Returns the absolute path to the Ren'Py common directory.

    `renpy_base`
        The absolute path to the Ren'Py base directory, the directory
        containing this file.
    """

    return renpy_base + "/renpy/common"


def path_to_saves(gamedir, save_directory=None): # type: (str, str|None) -> str
    """
    Given the path to a Ren'Py game directory, and the value of config.
    save_directory, returns absolute path to the directory where save files
    will be placed.

    `gamedir`
        The absolute path to the game directory.

    `save_directory`
        The value of config.save_directory.
    """

    import renpy # @UnresolvedImport

    if save_directory is None:
        save_directory = renpy.config.save_directory
        save_directory = renpy.exports.fsencode(save_directory) # type: ignore

    # Makes sure the permissions are right on the save directory.
    def test_writable(d):
        try:
            fn = os.path.join(d, "test.txt")
            open(fn, "w").close()
            open(fn, "r").close()
            os.unlink(fn)
            return True
        except Exception:
            return False

    # Android.
    if renpy.android:
        paths = [
            os.path.join(os.environ["ANDROID_OLD_PUBLIC"], "game/saves"),
            os.path.join(os.environ["ANDROID_PRIVATE"], "saves"),
            os.path.join(os.environ["ANDROID_PUBLIC"], "saves"),
            ]

        for rv in paths:
            if os.path.isdir(rv) and test_writable(rv):
                break
        else:
            rv = paths[-1]

        print("Saving to", rv)
        return rv

    if renpy.ios:
        from pyobjus import autoclass # type: ignore
        from pyobjus.objc_py_types import enum # type: ignore

        NSSearchPathDirectory = enum("NSSearchPathDirectory", NSDocumentDirectory=9)
        NSSearchPathDomainMask = enum("NSSearchPathDomainMask", NSUserDomainMask=1)

        NSFileManager = autoclass('NSFileManager')
        manager = NSFileManager.defaultManager()
        url = manager.URLsForDirectory_inDomains_(
            NSSearchPathDirectory.NSDocumentDirectory,
            NSSearchPathDomainMask.NSUserDomainMask,
            ).lastObject()

        # url.path seems to change type based on iOS version, for some reason.
        try:
            rv = url.path().UTF8String()
        except Exception:
            rv = url.path.UTF8String()


        if isinstance(rv, bytes):
            rv = rv.decode("utf-8")

        print("Saving to", rv)
        return rv

    # No save directory given.
    if not save_directory:
        return os.path.join(gamedir, "saves")

    if "RENPY_PATH_TO_SAVES" in os.environ:
        return os.environ["RENPY_PATH_TO_SAVES"] + "/" + save_directory

    # Search the path above Ren'Py for a directory named "Ren'Py Data".
    # If it exists, then use that for our save directory.
    path = renpy.config.renpy_base

    while True:
        if os.path.isdir(path + "/Ren'Py Data"):
            return path + "/Ren'Py Data/" + save_directory

        newpath = os.path.dirname(path)
        if path == newpath:
            break
        path = newpath

    # Otherwise, put the saves in a platform-specific location.
    if renpy.macintosh:
        rv = "~/Library/RenPy/" + save_directory
        return os.path.expanduser(rv)

    elif renpy.windows:
        if 'APPDATA' in os.environ:
            return os.environ['APPDATA'] + "/RenPy/" + save_directory
        else:
            rv = "~/RenPy/" + renpy.config.save_directory # type: ignore
            return os.path.expanduser(rv)

    else:
        rv = "~/.renpy/" + save_directory
        return os.path.expanduser(rv)


# Returns the path to the Ren'Py base directory (containing common and
# the launcher, usually.)
def path_to_renpy_base():
    """
    Returns the absolute path to thew Ren'Py base directory.
    """

    renpy_base = os.path.dirname(os.path.realpath(sys.argv[0]))
    renpy_base = os.path.abspath(renpy_base)

    return renpy_base

##############################################################################


android = ("ANDROID_PRIVATE" in os.environ)

def main():

    renpy_base = path_to_renpy_base()

    sys.path.append(renpy_base)

    # Ignore warnings.
    warnings.simplefilter("ignore", DeprecationWarning)

    # Start Ren'Py proper.
    try:
        import renpy.bootstrap
    except ImportError:
        print("Could not import renpy.bootstrap. Please ensure you decompressed Ren'Py", file=sys.stderr)
        print("correctly, preserving the directory structure.", file=sys.stderr)
        raise

    # Set renpy.__main__ to this module.
    renpy.__main__ = sys.modules[__name__] # type: ignore

    renpy.bootstrap.bootstrap(renpy_base)


if __name__ == "__main__":
    main()
