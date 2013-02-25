#!/bin/bash

ROOT="$(dirname $(readlink -f $0))"

ln -s "$ROOT/help.html" "$ROOT/tutorial/README.html"
ln -s "$ROOT/help.html" "$ROOT/the_question/README.html"
ln -s "$ROOT/help.html" "$ROOT/template/README.html"

ln -s "$ROOT/sphinx/source/license.rst" "$ROOT/LICENSE.txt"
ln -s "$ROOT/sphinx/build/html" "$ROOT/doc"

if [ "$1" != "" ]; then
    ln -s "$1/lib" "$ROOT/lib"
    ln -s "$1/renpy.app" "$ROOT"
    ln -s "$1/renpy.exe" "$ROOT"
fi