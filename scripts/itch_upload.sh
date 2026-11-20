#!/bin/bash

# Uploads a Ren'Py release from dl/<version> to itch.io. The version defaults to the
# current major.minor.patch version, and can be given as the first argument.

set -e

RENPY="$(cd "$(dirname "$0")/.." && pwd)"

if [ -n "$1" ]; then
    VERSION="$1"
else
    VERSION="$("$RENPY/lib/py3-linux-x86_64/python" "$RENPY/distribute.py" --print-version=short)"
fi

D="$RENPY/dl/$VERSION"

if [ ! -d "$D" ]; then
    echo "$0: $D does not exist."
    exit 1
fi

echo "Uploading Ren'Py $VERSION to itch.io."

butler () {
    "$RENPY/tmp/butler-linux-amd64/butler" "$@"
}

P=renpytom/renpy-mirror

butler push "$D/renpy-$VERSION-sdk.zip" $P:sdk-windows
butler push "$D/renpy-$VERSION-sdk.tar.bz2" $P:sdk-linux
butler push "$D/renpy-$VERSION-sdkarm.tar.bz2" $P:sdkarm-linux
butler push "$D/renpy-$VERSION-sdk.dmg" $P:sdk-mac

butler push "$D/renpy-$VERSION-rapt.zip" $P:rapt
butler push "$D/renpy-$VERSION-renios.zip" $P:renios
