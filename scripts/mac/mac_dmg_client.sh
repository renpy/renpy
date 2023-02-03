#!/bin/bash

set -e

IDENTITY="$1"
VOLNAME="$2"
DMGDIR="$3"
DMGDIRBASE=$(basename $3)
DMG="$4"
DMGBASE=$(basename $4)

TARBALL=$DMGDIRBASE.tar

HOST=mary21.local

pushd $(dirname $DMGDIR)
rm -f /tmp/$TARBALL
tar cf /tmp/$TARBALL $DMGDIRBASE
popd

rsync -a $(dirname $0)/ tom@$HOST:/tmp/renpy-mac-scripts/

rsync -a /tmp/$TARBALL tom@$HOST:/tmp

ssh -t tom@$HOST "'/tmp/renpy-mac-scripts/mac_dmg_server.sh' '$IDENTITY' '$VOLNAME' '$DMGDIRBASE' '$DMGBASE'"

rsync -a tom@$HOST:/tmp/$DMGBASE $DMG
