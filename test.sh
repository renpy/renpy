#!/bin/bash

set -e


S=$(realpath $(dirname $0))
T="/tmp/test-rénpy/rénpy"


rmln () {
    if [ -L "$T/$1" ]; then
        rm "$T/$1"
    fi

    ln -s "$S/$1" "$T/$1"
}

rmcp () {
    if [ -e "$T/$1" ]; then
        chmod -R 0755 "$T/$1"
        rm -Rf "$T/$1"
    fi

    cp -a "$S/$1" "$T/$1"
    chmod -R 0555 "$T/$1"
}

mkdir -p "$T"
mkdir -p "$T/../Ren'Py Data"

chmod 0755 "$T"

rmln module
rmln renpy
rmcp run.sh
rmcp renpy.py
rmcp launcher
rmcp tutorial
rmcp the_question
rmcp gui

if [ -e "$S/testing" ]; then
    rmcp testing
fi

chmod 0555 "$T"

export RENPY_MULTIPERSISTENT="$T/persistent"

exec "$T/run.sh" "$@"

