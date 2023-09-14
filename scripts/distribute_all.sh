#!/bin/bash

set -e

cd $(dirname $(dirname $(readlink -f $0)))

git status
sleep 2

(
    set -e
    . ~/.virtualenvs/renpy3/bin/activate
    cd sphinx
    ./build.sh
)

rpy build --python 3
rpy build --python 2

lib/py3-linux-x86_64/python distribute.py
lib/py2-linux-x86_64/python distribute.py
