#!/bin/bash

set -e

IDENTITY="$1"
VOLNAME="$2"
DMGDIRBASE="$3"
DMGBASE="$4"

# The tarball and the dmg are removed by the client once it has the dmg.
trap 'rm -rf "/tmp/${DMGDIRBASE:?}"' EXIT

# Sed writes the command for security's interactive mode, so that the password is only
# ever on stdin, and isn't in the arguments of any process.
sed -e 's/^/unlock-keychain -p "/' -e 's/$/"/' ~/.password | security -i

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
