#!/bin/bash

set -e

IDENTITY="$1"
VOLNAME="$2"
DMGDIRBASE="$3"
DMGBASE="$4"

security unlock-keychain -p "$(cat ~/.password)"

pushd /tmp

rm -Rf "$DMGDIRBASE" || true
tar xf "$DMGDIRBASE.tar"

hdiutil create -fs 'HFS+' -format UDBZ -ov -volname "$VOLNAME" -srcfolder "$DMGDIRBASE" "$DMGBASE"
codesign --timestamp --verbose -s "$1" "$DMGBASE"

date
echo "Submitting for notarization."

xcrun notarytool submit --keychain-profile developer-signing --wait "$DMGBASE"

xcrun stapler staple "$DMGBASE"

popd
