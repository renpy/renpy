#!/bin/sh

lib/py3-linux-x86_64/python ./distribute.py --nosign --fast $1
rm -Rf /tmp/renpy-$1-sdk
unzip -d /tmp dl/$1/renpy-$1-sdk.zip
/tmp/renpy-$1-sdk/renpy.sh
