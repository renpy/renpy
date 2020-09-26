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

butler push "$D/renpy-$1-sdk.zip" $P:sdk-windows-mac-linux

butler push "$D/renpy-$1-rapt.zip" $P:rapt
butler push "$D/renpy-$1-raspi.tar.bz2" $P:raspi
butler push "$D/renpy-$1-renios.zip" $P:renios

butler push "$D/renpy-$1-atom-linux.tar.bz2" $P:atom-linux
butler push "$D/renpy-$1-atom-mac.zip" $P:atom-mac
butler push "$D/renpy-$1-atom-windows.zip" $P:atom-windows

butler push "$D/renpy-$1-editra-linux.tar.bz2" $P:editra-linux
butler push "$D/renpy-$1-editra-mac.zip" $P:editra-mac
butler push "$D/renpy-$1-editra-windows.zip" $P:editra-windows
