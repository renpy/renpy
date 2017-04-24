#!/bin/bash

D="$1"

if [ -z "$D" ]; then
    echo "usage: $0 <unpacked sdk>"
    exit 1
fi

rm -Rf "$D/launcher"
rm -Rf "$D/renpy"

cp -a renpy "$D"
cp -a launcher "$D"

exec "$D/renpy.sh" "$D" test android
