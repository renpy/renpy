#!/bin/bash

set -e
cd $(dirname $(dirname $(readlink -f $0)))

translate () {
    ./run.sh launcher translate $1 --empty --no-todo
    ./scripts/automatic_translate.py $2 launcher/game/tl/$1/*.rpy
}

translate finnish FI
translate french FR
translate german DE
translate greek EL
translate indonesian ID
translate italian IT
translate japanese JA
translate korean KO
translate polish PL
translate portuguese PT-BR
translate russian RU
translate schinese ZH
translate spanish ES
translate turkish TR
translate ukrainian UK

# Not supported

# translate arabic
# translate malay
# translate piglatin
# translate tchinese
# translate vietnamese
