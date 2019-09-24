#!/bin/bash

set -e

cd "$(dirname $0)/.."

pushd /tmp/notarize

result="$(xcrun altool --notarization-history 0 --asc-provider XHTE5H7Z79 -u tom@rothamel.us -p '@keychain:altool' | head -6 | tail -1)"
echo $result
status="$(echo $result | cut -d ' ' -f 5)"

if [ $status = "success" ]; then
    echo "Success... now stapling."
else
    exit
fi

xcrun stapler staple -v renpy.app

popd

rm -Rf notarized/out/renpy.app || true
cp -a /tmp/notarize/renpy.app notarized/out/

echo "Done."
