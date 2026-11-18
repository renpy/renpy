#!/bin/bash

ROOT="$(dirname $(python3 -c "import os;print(os.path.realpath('$0'))"))"

ln -s "$ROOT/sphinx/source/license.rst" "$ROOT/LICENSE.txt"

if [ "$1" != "" ]; then
    ln -s "$1/lib" "$ROOT/lib"
    ln -s "$1/renpy.app" "$ROOT"
    ln -s "$1/renpy.exe" "$ROOT"
    ln -s "$1/renpy.sh" "$ROOT"
fi
