#!/bin/bash
# This builds out of date modules using the default C compiler, and then
# runs them.

set -e

export RENPY_CYTHON=cython

ROOT="$(cd "$(dirname "$0")" && pwd)"
QUIET=${RENPY_QUIET- --quiet}
BUILD_ONLY=false
SKIP_BUILD=false
CLEAN=false

while [ "$#" -gt 0 ]; do
    case "$1" in
        --build)
            BUILD_ONLY=true
            shift
            ;;
        --no-build)
            SKIP_BUILD=true
            shift
            ;;
        --clean)
            CLEAN=true
            shift
            ;;
        --)
            shift
            break
            ;;
        -*)
            break
            ;;
        *)
            break
            ;;
    esac
done

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

    if $CLEAN; then
        find "$ROOT" -maxdepth 1 -type f -name '*.cpython*.so' -delete
        find "$ROOT/renpy" -type f -name '*.cpython*.so' -delete
        rm -Rf "$ROOT/tmp/gen"
    fi

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
    export LD_LIBRARY_PATH="$CUBISM/Core/dll/$CUBISM_PLATFORM${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
fi

if ! $SKIP_BUILD || $BUILD_ONLY || $CLEAN; then
    if [ -n "$RENPY_SERIALIZE_BUILD" ]; then
        # The shell keeps the locked file descriptor open until setup finishes.
        {
            python -c 'import fcntl; fcntl.flock(9, fcntl.LOCK_EX)'
            setup "$ROOT/"
        } 9<"$ROOT/setup.py"
    else
        setup "$ROOT/"
    fi
fi

if $BUILD_ONLY; then
    echo "Ren'Py build complete."
    exit 0
else
    exec $RENPY_GDB python -X utf8 $ROOT/renpy.py "$@"
fi
