#!/bin/sh

try () { "$@" || exit 1; }

SPHINX="$(dirname $(python -c "import os;print(os.path.realpath('$0'))"))"

try cd "$SPHINX"

# Delete .pyo files, which could not include docstrings.
try find ../renpy -name \*.pyo -delete

try ../renpy.sh .

try sphinx-build -a source ../doc-web &
try sphinx-build -a source ../doc 2>/dev/null
wait
try python checks.py

