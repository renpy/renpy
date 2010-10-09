# This builds out of date modules using the default C compiler, and then
# runs them.

# A sensible default for RENPY_DEPS_INSTALL
export RENPY_DEPS_INSTALL=${RENPY_DEPS_INSTALL:-/usr}

try () {
    "$@" || exit -1
}

# Builds the module in renpy/display named name.
display () {

    build=0

    for i in renpy/display/*.pxd; do
        if [ $i -nt module/$1.c ]; then
           build=1
        fi
    done
        
    if [ renpy/display/$1.pyx -nt module/$1.c ]; then
        build=1
    fi

    if [ $build != 0 ]; then    
        echo renpy.display.$1 is out of date.
        try cython -a renpy/display/$1.pyx -o module/$1.c
    fi
}

# Build the modules. To build a new module, it must be listed here
# and in module/setup.py
display render
display accelerator

display gldraw
display gltexture
display glenviron
display glenviron_fixed
display glenviron_shader
display glshader
display glrtt_copy


echo Compiling...

# Build the module, then come back here and run Ren'Py.
try cd module
try python setup.py install # > /dev/null
try cd ..

exec ./renpy.py "$@"
