#!/bin/sh

set -e

SPHINX="$(dirname $(python -c "import os;print(os.path.realpath('$0'))"))"


cd "$SPHINX"
export PATH="../.venv/bin:$PATH"

# Make the inc folder.
mkdir -p source/inc

# Get the dependencies.
(cd ..; uv sync)

# Run a Ren'Py game that generates documentation.
../run.sh . || ../renpy.sh .

# Clear out generated images.
rm -Rf ../doc-web/_images || true
rm -Rf ../doc/_images || true

sphinx-build -E -a source ../doc-web &
DOC_WEB_PID=$!

# Build the included-with-Ren'Py documentation, if not running interactively. The
# warnings repeat those of the web build, so they're only shown if the build fails.
DOC_LOG="$(mktemp)"

if ! RENPY_NO_FIGURES=1 sphinx-build -E -a source ../doc 2>"$DOC_LOG"; then
    cat "$DOC_LOG" >&2
    rm -f "$DOC_LOG"
    wait "$DOC_WEB_PID" || true
    exit 1
fi

rm -f "$DOC_LOG"

# Wait for the web build to finish, and fail if it did.
wait "$DOC_WEB_PID"

# Run some checks.
python checks.py
