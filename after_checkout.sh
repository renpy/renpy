#!/bin/bash

ROOT="$(dirname $(python -c "import os;print(os.path.realpath('$0'))"))"

ln -s "$ROOT/help.html" "$ROOT/tutorial/README.html"
ln -s "$ROOT/help.html" "$ROOT/the_question/README.html"
ln -s "$ROOT/help.html" "$ROOT/templates/english/README.html"

ln -s "$ROOT/sphinx/source/license.rst" "$ROOT/LICENSE.txt"

if [ "$1" != "" ]; then
    ln -s "$1/lib" "$ROOT/lib"
    ln -s "$1/renpy.app" "$ROOT"

    # renpy.sh and renpy.exe have to be copies. Both find the directory to
    # run from by looking at their own location, and renpy.sh resolves
    # symlinks first, so a symlinked renpy.sh runs the nightly's copy of
    # Ren'Py rather than this checkout.
    cp "$1/renpy.exe" "$ROOT"
    cp "$1/renpy.sh" "$ROOT"
fi
