#!/bin/bash

dmg="/Users/tom/magnetic/ab/website/renpy/dl/$1/renpy-$1-sdk.dmg"

if [ ! -e "$dmg" ]; then
    echo "$dmg" not found.
    exit 1
else
    echo "$dmg" found.
fi

xcrun stapler staple --verbose "$dmg"
