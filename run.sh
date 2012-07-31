# This builds out of date modules using the default C compiler, and then
# runs them.

export RENPY_CYTHON=cython

try () {
    "$@" || exit -1
}

if [ -z "$PYTHONPATH" ] ; then
    echo PYTHONPATH not set
    exit 1
fi

try python module/setup.py --quiet build $RENPY_BUILD_ARGS install_lib -d "$PYTHONPATH"

exec ./renpy.py "$@"
