#!/bin/bash
# This builds out of date modules using the default C compiler, and then
# runs them.

set -e

export RENPY_CYTHON=cython

ROOT="$(cd "$(dirname "$0")" && pwd)"
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
    if [ -d "$ROOT/.venv" ] ; then
        . "$ROOT/.venv/bin/activate"
    else
        echo "Please use 'uv sync' to creat the virtual environment."
        exit 1
    fi
fi

if [[ "$OSTYPE" == "darwin"* ]]; then
    CPUS=$(sysctl -n hw.logicalcpu)
else
    CPUS=$(nproc)
fi

BUILD_J="-j $CPUS"

setup () {
    pushd $1 >/dev/null

    if ! python setup.py $QUIET build_ext -b tmp/build/lib.$variant -t tmp/build/tmp.$variant --inplace $BUILD_J; then
        if [ "$(which python)" != "$ROOT/.venv/bin/python" ]; then
            echo "Warning: Running using $(which python)"
        fi

        exit 1
    fi

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
    exit 0
else
    exec $RENPY_GDB python $ROOT/renpy.py "$@"
fi
