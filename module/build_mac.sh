#!/bin/sh 

try () {
    "$@" || exit -1
}



BASE=/Users/tom

. $BASE/newbuild.i386/env.sh
try ./build.sh 
. $BASE/newbuild.ppc/env.sh
try ./build.sh 

try chmod -R a+rX $BASE/newbuild.i386/install
try chmod -R a+rX $BASE/newbuild.ppc/install
