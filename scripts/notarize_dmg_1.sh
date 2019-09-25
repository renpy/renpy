#!/bin/sh

dmg="/Users/tom/magnetic/ab/website/renpy/dl/$1/renpy-$1-sdk.dmg"

if [ ! -e "$dmg" ]; then
    echo "$dmg" not found.
    exit 1
else
    echo "$dmg" found.
fi

xcrun altool --asc-provider XHTE5H7Z79 -u tom@rothamel.us -p "@keychain:altool"  \
    --notarize-app \
    --primary-bundle-id org.renpy.renpy.dmg \
    -f "$dmg"

