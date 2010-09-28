# This builds out of date modules using the default C compiler, and then
# runs them.

# A sensible default for RENPY_DEPS_INSTALL
export RENPY_DEPS_INSTALL=${RENPY_DEPS_INSTALL:-/usr}

try () {
    "$@" || exit -1
}

# Builds the module in renpy/display named name.
display () {

    if [ renpy/display/$1.pyx -nt module/$1.c ]; then
        echo renpy.display.$1 is out of date.
        try cython renpy/display/$1.pyx -o module/$1.c
    fi
}

# Build the modules. To build a new module, it must be listed here
# and in module/setup.py
display render

# Build the module, then come back here and run Ren'Py.
try cd module
try python setup.py install > /dev/null
try cd ..

exec ./renpy.py "$@"
