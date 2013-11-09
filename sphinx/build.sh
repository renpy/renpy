#!/bin/sh

SPHINX="$(dirname $(python -c "import os;print(os.path.realpath('$0'))"))"
cd $SPHINX

# This has to be run with python (and not renpy.sh, or python -OO) since
# optimization will remove the docstrings.
../renpy.sh . || exit 1

sphinx-build -a source ../doc || exit 1

echo Not uploading.

