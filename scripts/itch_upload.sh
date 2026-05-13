#!/bin/bash

set -e

if [ -z "$1" ]; then
    echo "$0 requires a version."
    exit 1
fi

RENPY="$(dirname $0)/.."

butler () {
    "$RENPY/tmp/butler-linux-amd64/butler" "$@"
}

D="$RENPY/dl/$1"
P=renpytom/renpy-mirror

butler push "$D/renpy-$1-sdk.zip" $P:sdk-windows
butler push "$D/renpy-$1-sdk.tar.bz2" $P:sdk-linux
butler push "$D/renpy-$1-sdkarm.tar.bz2" $P:sdkarm-linux
butler push "$D/renpy-$1-sdk.dmg" $P:sdk-mac

butler push "$D/renpy-$1-rapt.zip" $P:rapt
butler push "$D/renpy-$1-renios.zip" $P:renios
