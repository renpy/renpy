#!/bin/sh 

. ~/newbuild.i386/env.sh
./build.sh 
. ~/newbuild.ppc/env.sh
./build.sh 

chmod -R a+rX ~/newbuild.i386/install
chmod -R a+rX ~/newbuild.ppc/install
