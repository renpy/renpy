#!/bin/bash

if [ -z "$RENPY_COVERAGE" ]; then
    echo "$0 needs to be run with RENPY_COVERAGE set, probably in a virtualenv."
    exit 1
fi

./run.sh --build || exit 1
coverage run renpy.py "$@"
coverage html
xdg-open htmlcov/index.html
