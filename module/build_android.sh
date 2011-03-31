#!/bin/sh

A="$RENPY_ANDROID"

CFLAGS="$CFLAGS -DANDROID"
CFLAGS="$CFLAGS -I$A/sdl/sdl-1.2/include"
CFLAGS="$CFLAGS -I$A/jni/png"
CFLAGS="$CFLAGS -I$A/jni/freetype/include"

LDFLAGS="$LDFLAGS -L$A/libs/armeabi -L$A/obj/local/armeabi"

export CFLAGS
export LDFLAGS

$A/python-install/bin/python.host setup.py build_ext -b build/lib.android -t build/tmp.android build_ext
