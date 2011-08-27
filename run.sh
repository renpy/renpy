# This builds out of date modules using the default C compiler, and then
# runs them.

export RENPY_CYTHON=cython

try () {
    "$@" || exit -1
}

try python module/setup.py --quiet build $RENPY_BUILD_ARGS install 

exec ./renpy.py "$@"
