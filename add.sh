#!/bin/sh

if [ "x$1" = "x" ]; then
    echo need version
    exit
fi

mkdir ~/ab/website/renpy/dl/$1
cp dists/renpy-$1-* ~/ab/website/renpy/dl/$1
cp CHANGELOG.txt ~/ab/website/renpy/dl/$1

cd ~/ab/website
./upload.sh
