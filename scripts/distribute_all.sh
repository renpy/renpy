#!/bin/bash

set -e

cd "$(dirname "$(dirname "$(readlink -f "$0")")")"

PYTHON=lib/py3-linux-x86_64/python

# Fail before the slow steps if the tree can't be released.
$PYTHON distribute.py --check-tree "$@"

rpy pull
rpy build

# The documentation includes the version, so this has to happen first.
$PYTHON distribute.py --vc-version-only "$@"

(
    set -e
    cd sphinx
    ./build.sh
)

$PYTHON distribute.py "$@"
