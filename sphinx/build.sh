#!/bin/sh

set -e

SPHINX="$(dirname $(python -c "import os;print(os.path.realpath('$0'))"))"

cd "$SPHINX"

# Delete .pyo files, which could not include docstrings.
find ../renpy -name \*.pyo -delete

../renpy.sh .

sphinx-build -a source ../doc-web &
RENPY_NO_FIGURES=1 sphinx-build -a source ../doc 2>/dev/null
wait
python checks.py

