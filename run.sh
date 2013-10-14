# This builds out of date modules using the default C compiler, and then
# runs them.

export RENPY_CYTHON=cython

try () {
    "$@" || exit -1
}

if [ -n "$RENPY_VIRTUAL_ENV" ] ; then
    . "$RENPY_VIRTUAL_ENV/bin/activate"
fi

if [ -z "$PYTHONPATH" -a -z "$VIRTUAL_ENV" ] ; then
    echo Neither PYTHONPATH nor VIRTUAL_ENV is set.
    exit 1
fi

if [ -n "$PYTHONPATH" ]; then
    try python module/setup.py --quiet \
        build -b build/lib.renpy-run -t build/tmp.renpy-run \
        $RENPY_BUILD_ARGS install_lib -d "$PYTHONPATH"
else
    try python module/setup.py --quiet \
        build -b build/lib.renpy-run -t build/tmp.renpy-run \
        $RENPY_BUILD_ARGS install
fi

if  [ "$1" = "--build" ] ; then
    echo "Ren'Py build complete."
else
    exec python -OO ./renpy.py "$@"
fi
