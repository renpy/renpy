#!/bin/bash

ROOT="$(dirname $(python -c "import os;print(os.path.realpath('$0'))"))"

ln -s "$ROOT/help.html" "$ROOT/tutorial/README.html"
ln -s "$ROOT/help.html" "$ROOT/the_question/README.html"
ln -s "$ROOT/help.html" "$ROOT/templates/english/README.html"

ln -s "$ROOT/sphinx/source/license.rst" "$ROOT/LICENSE.txt"

if [ "$1" != "" ]; then
    ln -s "$1/lib" "$ROOT/lib"
    ln -s "$1/renpy.app" "$ROOT"
    ln -s "$1/renpy.exe" "$ROOT"
    ln -s "$1/renpy.sh" "$ROOT"
fi
