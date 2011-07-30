#!/bin/sh

DIR="`readlink -f $0`"
DIR="`dirname $DIR`"
echo $DIR

cd $DIR

sphinx-build -a developer ../developer/html

echo Not uploading.

