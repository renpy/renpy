#!/bin/bash

set -e

cd $(dirname $(dirname $(readlink -f $0)))

git status
sleep 2

(
    set -e
    cd sphinx
    ./build.sh
)

rpy pull
rpy build --python 3

lib/py3-linux-x86_64/python distribute.py
