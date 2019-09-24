#!/bin/bash

set -e

cd "$(dirname $0)/.."

pushd notarized/in
rm -Rf /tmp/notarize
unzip -d /tmp/notarize renpy.zip
popd

pushd /tmp/notarize
mv renpy-*-sdk/renpy.app .
rm -Rf renpy-*-sdk
zip -r renpy.app.zip renpy.app

xcrun altool --asc-provider XHTE5H7Z79 -u tom@rothamel.us -p "@keychain:altool"  \
    --notarize-app \
    --primary-bundle-id org.renpy.renpy \
    -f renpy.app.zip

popd

