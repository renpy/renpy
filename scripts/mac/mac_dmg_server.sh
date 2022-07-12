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

# --transport Aspera \

xcrun altool --asc-provider XHTE5H7Z79 -u tom@rothamel.us -p "@keychain:altool"  \
    --notarize-app \
    --primary-bundle-id org.renpy.renpy.dmg \
    -f "$DMGBASE"

date
echo "Submitted dmg for notarization."

$(dirname $0)/wait_notarization.py

sleep 60

xcrun stapler staple "$DMGBASE"

popd
