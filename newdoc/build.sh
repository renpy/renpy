#!/bin/sh

DIR="`readlink -f $0`"
DIR="`dirname $DIR`"
echo $DIR

cd $DIR

../renpy.py .
make html
