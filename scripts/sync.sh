#!/bin/bash

set -e

default="tom@192.168.1.2:/home/tom/ab/renpy"
source=${1:-$default}

if [ -e .git ]; then
    echo "The .git directory is present, not updating."
    exit 1
fi

sync () {
    echo "Synchronize $1"
    rsync -a "$source/$1" .
}

sync gui
sync launcher
sync lib
sync renpy
sync renpy2.sh
sync renpy3.sh
sync renpy.py
sync scripts
sync the_question
sync sdk-fonts
sync tutorial
sync typings
