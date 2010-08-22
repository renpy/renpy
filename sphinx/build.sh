#!/bin/sh

DIR="`readlink -f $0`"
DIR="`dirname $DIR`"
echo $DIR

cd $DIR

../renpy.py .

sphinx-build -a source ../doc
