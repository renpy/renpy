#!/bin/sh
# Sets up this checkout for development, using a nightly build for the
# compiled parts. See dev_setup.py for the details and options.

ROOT="$(cd "$(dirname "$0")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
    exec python3 "$ROOT/dev_setup.py" "$@"
elif command -v python >/dev/null 2>&1; then
    exec python "$ROOT/dev_setup.py" "$@"
else
    echo "dev_setup.sh: python3 is needed to run dev_setup.py. Install it from https://www.python.org/ or your package manager."
    exit 1
fi
