#!/bin/bash

# Find Ren'Py.
cd "$(realpath $(dirname $0))/.."

rm -Rf launcher/game/tl/piglatin
rm -Rf tutorial/game/tl/piglatin

./run.sh launcher translate piglatin --piglatin --no-todo
./run.sh tutorial translate piglatin --piglatin --no-todo



