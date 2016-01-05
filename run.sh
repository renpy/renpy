# This builds out of date modules using the default C compiler, and then
# runs them.

export RENPY_CYTHON=cython

try () {
    "$@" || exit -1
}

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

setup () {
    if [ -n "$PYTHONPATH" ]; then
        try python $1 --quiet \
            build -b build/lib.$variant -t build/tmp.$variant \
            $RENPY_BUILD_ARGS install_lib -d "$PYTHONPATH"
    else
        try python $1 --quiet \
            build -b build/lib.$variant -t build/tmp.$variant \
            $RENPY_BUILD_ARGS install
    fi
}

ROOT="$(dirname $(realpath $0))"

if [ -e "$ROOT/pygame_sdl2" ]; then
    setup "$ROOT/pygame_sdl2/setup.py"
fi

setup "$ROOT/module/setup.py"

if  [ "$1" = "--build" ] ; then
    echo "Ren'Py build complete."
else
    exec python -O ./renpy.py "$@"
fi
