#!/bin/bash

set -e

IDENTITY="$1"
TARBALL="$2"
APP="$3"

security unlock-keychain -p "$(cat ~/.password)"

pushd /tmp
rm -Rf "$APP" || true
tar xf "$TARBALL"

codesign --entitlements="$(dirname $0)/entitlements.plist" --options=runtime --timestamp --verbose -s "$1" -f --deep --no-strict "$APP"
rm -f /tmp/renpy.app.zip
zip -r /tmp/renpy.app.zip "$APP"

date
echo "Submitting for notarization."

xcrun notarytool submit --keychain-profile developer-signing --wait /tmp/renpy.app.zip
xcrun stapler staple "$APP"

tar cf "signed-$TARBALL" "$APP"
popd
