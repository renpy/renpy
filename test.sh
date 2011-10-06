# Test-build Ren'Py. 

try () {
    "$@" || exit -1
}

rm -Rf "/tmp/renpy-$1"
try tar xjf "dists/renpy-$1-sdk.tar.bz2" -C /tmp
try cd "/tmp/renpy-$1/module"
try python setup.py build_ext -i

echo Build test finished.
