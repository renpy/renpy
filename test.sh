#!/bin/bash

set -e


S=$(realpath $(dirname $0))
T="/tmp/rénpy/rénpy"


rmln () {
    if [ -L "$T/$1" ]; then
        rm "$T/$1"
    fi

    ln -s "$S/$1" "$T/$1"
}

rmcp () {
    if [ -L "$T/$1" ]; then
        rm "$T/$1"
    fi

    cp "$S/$1" "$T/$1"

}

mkdir -p "$T"
mkdir -p "$T/../Ren'Py Data"

rmln module
rmln renpy
rmcp run.sh
rmcp renpy.py
rmln launcher
rmln tutorial
rmln the_question

exec "$T/run.sh" "$@"

