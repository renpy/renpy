#!/bin/sh

set -e

SPHINX="$(dirname $(python -c "import os;print(os.path.realpath('$0'))"))"

cd "$SPHINX"

# Make the inc folder.
mkdir -p source/inc

# Delete .pyo files, which could not include docstrings.
find ../renpy -name \*.pyo -delete

# Run a Ren'Py game that generates documentation.
../renpy.sh .

# Clear out generated images.
rm -Rf ../doc-web/_images || true
rm -Rf ../doc/_images || true

# Build the full web documentation.
sphinx-build -E -a source ../doc-web &

# Build the included-with-Ren'Py documentation.
RENPY_NO_FIGURES=1 sphinx-build -E -a source ../doc 2>/dev/null

# Wait for both builds to finish.
wait

# Run some checks.
python checks.py

