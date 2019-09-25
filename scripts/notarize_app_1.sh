#!/bin/bash

set -e

cd "$(dirname $0)/.."

pushd notarized/in
rm -Rf /tmp/notarize
mkdir -p /tmp/notarize
tar xjf renpy.tar.bz2 -C /tmp/notarize
popd

pushd /tmp/notarize
mv renpy-*-sdk/renpy.app .
rm -Rf renpy-*-sdk

codesign --verify --verbose renpy.app

zip -r renpy.app.zip renpy.app

xcrun altool --asc-provider XHTE5H7Z79 -u tom@rothamel.us -p "@keychain:altool"  \
    --notarize-app \
    --primary-bundle-id org.renpy.renpy \
    -f renpy.app.zip

popd

