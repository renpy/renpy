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

if [ -z "$VIRTUAL_ENV" ] ; then
    echo Please install into a virtualenv.
    exit 1
fi

PY_VERSION=$(python -c 'import sys; print(sys.version_info.major)')

if [ $PY_VERSION != "2" ]; then
    BUILD_J="-j $(nproc)"
    ADAPT_TO_SETUPTOOLS="--old-and-unmanageable"
fi

ROOT="$(dirname $(realpath $0))"

setup () {
    pushd $1 >/dev/null

    try python setup.py $QUIET \
        build -b build/lib.$variant -t build/tmp.$variant $BUILD_J \
        $RENPY_BUILD_ARGS install $ADAPT_TO_SETUPTOOLS

    popd >/dev/null
}

if [ -e "$ROOT/pygame_sdl2" ]; then
    setup "$ROOT/pygame_sdl2/"
fi

if [ -e "$ROOT/cubism" ]; then
    export CUBISM="$ROOT/cubism"
    export CUBISM_PLATFORM=${CUBISM_PLATFORM:-linux/x86_64}
    export LD_LIBRARY_PATH="$CUBISM/Core/dll/$CUBISM_PLATFORM"
fi

setup "$ROOT/module/"

python "$ROOT/distribute.py" --link-directories

if  [ "$1" = "--build" ] ; then
    echo "Ren'Py build complete."
else
    exec $RENPY_GDB python -O $ROOT/renpy.py "$@"
fi
