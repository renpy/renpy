# This builds out of date modules using the default C compiler, and then
# runs them.

# A sensible default for RENPY_DEPS_INSTALL
export RENPY_DEPS_INSTALL=${RENPY_DEPS_INSTALL:-/usr}

try () {
    "$@" || exit -1
}

# build <package> <module>
# Builds the module in renpy/package named module.
build () {

    build=0

    for i in renpy/$1/*.pxd; do
        if [ $i -nt module/$2.c ]; then
           build=1
        fi
    done
        
    if [ renpy/$1/$2.pyx -nt module/$2.c ]; then
        build=1
    fi

    if [ $build != 0 ]; then    
        echo renpy.$1.$2 is out of date.
        try cython -Imodule -a renpy/$1/$2.pyx -o module/$2.c
    fi
}

# Build the modules. To build a new module, it must be listed here
# and in module/setup.py
build display render
build display accelerator

build display gldraw
build display gltexture
build display glenviron
build display glenviron_fixed
build display glenviron_shader
build display glenviron_limited
build display glshader
build display glrtt_copy
build display glrtt_fbo

build text ftfont
build text textsupport
build text texwrap

echo Compiling...

# Build the module, then come back here and run Ren'Py.
try cd module
try python setup.py install # > /dev/null
try cd ..

exec ./renpy.py "$@"
