#!/bin/bash
# This builds out of date modules using the default C compiler, and then
# runs them.

export RENPY_CYTHON=cython

try () {
    "$@" || exit -1
}

QUIET=${RENPY_QUIET- --quiet}

if [ -n "$RENPY_COVERAGE" ]; then
    variant="renpy-coverage"
else
    variant="renpy-run"
fi

if [ -n "$RENPY_VIRTUAL_ENV" ] ; then
    . "$RENPY_VIRTUAL_ENV/bin/activate"
fi

if [ -z "$PYTHONPATH" -a -z "$VIRTUAL_ENV" ] ; then
    echo Neither PYTHONPATH nor VIRTUAL_ENV is set.
    exit 1
fi

ROOT="$(dirname $(realpath $0))"

setup () {
    pushd $1 >/dev/null

    if [ -n "$PYTHONPATH" ]; then
        try python setup.py $QUIET \
            build -b build/lib.$variant -t build/tmp.$variant \
            $RENPY_BUILD_ARGS install_lib -d "$PYTHONPATH"
    else
        try python setup.py $QUIET \
            build -b build/lib.$variant -t build/tmp.$variant \
            $RENPY_BUILD_ARGS install
    fi

    popd >/dev/null
}

if [ -e "$ROOT/pygame_sdl2" ]; then
    setup "$ROOT/pygame_sdl2/"
fi

setup "$ROOT/module/"

if  [ "$1" = "--build" ] ; then
    echo "Ren'Py build complete."
else
    exec $RENPY_GDB python -O $ROOT/renpy.py "$@"
fi
