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
    if [ -n "$PYTHONPATH" ]; then
        try python $1 $QUIET \
            build -b $ROOT/build/lib.$variant -t $ROOT/build/tmp.$variant \
            $RENPY_BUILD_ARGS install_lib -d "$PYTHONPATH"
    else
        try python $1 $QUIET \
            build -b $ROOT/build/lib.$variant -t $ROOT/build/tmp.$variant \
            $RENPY_BUILD_ARGS install
    fi
}

if [ -e "$ROOT/pygame_sdl2" ]; then
    setup "$ROOT/pygame_sdl2/setup.py"
fi

setup "$ROOT/module/setup.py"

if  [ "$1" = "--build" ] ; then
    echo "Ren'Py build complete."
else
    exec python -O $ROOT/renpy.py "$@"
fi
