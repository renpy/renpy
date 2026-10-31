#!/bin/bash

set -e

IDENTITY="$1"
APP="$2"
APPBASE=$(basename $2)
APPDIR=$(dirname $2)
APPDIRBASE=$(basename $APPDIR)

TARBALL=$APPDIRBASE.tar

HOST=mary21.local

LOCALTMP=$(mktemp -d)

# Remove local and remote temporary files, even if a step fails.
cleanup() {
    rm -rf "$LOCALTMP"
    ssh tom@$HOST "rm -rf /tmp/renpy-mac-scripts '/tmp/${TARBALL:?}' '/tmp/signed-${TARBALL:?}'" || true
}

trap cleanup EXIT

pushd $APPDIR
tar cf $LOCALTMP/$TARBALL $APPBASE
rsync -a $LOCALTMP/$TARBALL tom@$HOST:/tmp

rsync -a $(dirname $0)/ tom@$HOST:/tmp/renpy-mac-scripts/

ssh -t tom@$HOST "'/tmp/renpy-mac-scripts/mac_sign_server.sh' '$IDENTITY' '$TARBALL' '$APPBASE'"

rsync -a tom@$HOST:/tmp/signed-$TARBALL $LOCALTMP
tar xf $LOCALTMP/signed-$TARBALL
popd
