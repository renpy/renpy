#!/bin/bash
# This builds out of date modules using the default C compiler, and then
# runs them.

set -e

export RENPY_CYTHON=cython

ROOT="$(dirname $(realpath $0))"
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

BUILD_J="-j $(nproc)"

setup () {
    pushd $1 >/dev/null

    python setup.py $QUIET \
        build_ext -b tmp/build/lib.$variant -t tmp/build/tmp.$variant --inplace $BUILD_J \

    popd >/dev/null
}

if [ -e "$ROOT/cubism" ]; then
    export CUBISM="$ROOT/cubism"
    export CUBISM_PLATFORM=${CUBISM_PLATFORM:-linux/x86_64}
    export LD_LIBRARY_PATH="$CUBISM/Core/dll/$CUBISM_PLATFORM"
fi

setup "$ROOT/"

python "$ROOT/distribute.py" --link-directories

if  [ "$1" = "--build" ] ; then
    echo "Ren'Py build complete."
else
    exec $RENPY_GDB python $ROOT/renpy.py "$@"
fi
