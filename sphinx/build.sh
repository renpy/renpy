#!/bin/sh

set -e

SPHINX="$(dirname $(python -c "import os;print(os.path.realpath('$0'))"))"

cd "$SPHINX"

# Make the inc folder.
mkdir -p source/inc

# Run a Ren'Py game that generates documentation.
python ../renpy.py . || ../renpy3.sh .

# Clear out generated images.
rm -Rf ../doc-web/_images || true
rm -Rf ../doc/_images || true

sphinx-build -E -a source ../doc-web &

# Build the included-with-Ren'Py documentation, if not running interactively.
RENPY_NO_FIGURES=1 sphinx-build -E -a source ../doc 2>/dev/null

# Wait for both builds to finish.
wait

# Run some checks.
python checks.py
