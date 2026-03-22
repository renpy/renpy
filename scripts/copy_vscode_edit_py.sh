#!/bin/bash

set -e

cd "$(dirname "$0")/.."
cd launcher


cp -v "Visual Studio Code.edit.py" "Visual Studio Code (System).edit.py"
cp -v "Visual Studio Code.edit.py" "VSCodium (System).edit.py"
