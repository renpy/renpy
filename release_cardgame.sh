#!/bin/sh

rm -Rf cardgame/*~
rm -Rf cardgame/game/*~
rm -Rf cardgame/game/*.rpyc
rm -Rf cardgame/game/*.rpyb
rm -Rf cardgame/game/saves

rm cardgame-$1.zip
zip -9r cardgame-$1.zip cardgame -x \*.svn\* 



