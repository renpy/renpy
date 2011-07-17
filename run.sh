# This builds out of date modules using the default C compiler, and then
# runs them.

try () {
    "$@" || exit -1
}

try python module/setup.py --quiet install

exec ./renpy.py "$@"
