#!/bin/sh

SPHINX="$(dirname $(python -c "import os;print(os.path.realpath('$0'))"))"
cd $SPHINX

sphinx-build -a developer ../developer/html

echo Not uploading.

