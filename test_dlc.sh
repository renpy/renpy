#!/bin/sh

./distribute.py --fast $1
rm -Rf /tmp/renpy-$1-sdk
unzip -d /tmp dl/$1/renpy-$1-sdk.zip
/tmp/renpy-$1-sdk/renpy.sh
