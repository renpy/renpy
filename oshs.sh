#!/bin/bash

rm -Rf /tmp/oshs
./run.sh launcher set_projects_directory /tmp
mkdir -p /tmp/oshs/game
./run.sh launcher generate_gui /tmp/oshs --width 1920 --height 1080 --start
cp /tmp/oshs/game/gui.rpy sphinx/source/oshs/game/gui.rpy
cp /tmp/oshs/game/screens.rpy sphinx/source/oshs/game/screens.rpy
./run.sh sphinx/source/oshs

