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

LOCALTMP=$(mktemp -d)

# Remove local and remote temporary files, even if a step fails.
cleanup() {
    rm -rf "$LOCALTMP"
    ssh tom@$HOST "rm -rf /tmp/renpy-mac-scripts '/tmp/${TARBALL:?}' '/tmp/${DMGBASE:?}'" || true
}

trap cleanup EXIT

pushd $(dirname $DMGDIR)
tar cf $LOCALTMP/$TARBALL $DMGDIRBASE
popd

rsync -a $(dirname $0)/ tom@$HOST:/tmp/renpy-mac-scripts/

rsync -a $LOCALTMP/$TARBALL tom@$HOST:/tmp

ssh -t tom@$HOST "'/tmp/renpy-mac-scripts/mac_dmg_server.sh' '$IDENTITY' '$VOLNAME' '$DMGDIRBASE' '$DMGBASE'"

rsync -a tom@$HOST:/tmp/$DMGBASE $DMG
