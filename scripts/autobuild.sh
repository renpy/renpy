#!/bin/bash -e

pushd sphinx
./build.sh
popd

if git diff --name-only last-build | grep -q \.pyx; then
    $RENPY_BUILD_ALL
    git branch -d last-build
    git branch last-build HEAD
fi
