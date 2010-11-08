#!/bin/sh

A="$RENPY_ANDROID"

CFLAGS="$CFLAGS -DANDROID"
CFLAGS="$CFLAGS -I$A/android-sdl/sdl/sdl-1.2/include"
CFLAGS="$CFLAGS -I$A/android-sdl/jni/png"
CFLAGS="$CFLAGS -I$A/android-sdl/jni/freetype/include"

LDFLAGS="$LDFLAGS -L$A/android-sdl/libs/armeabi -L$A/android-sdl/obj/local/armeabi"
LDFLAGS="$LDFLAGS -Wl,--no-allow-shlib-undefined"

export CFLAGS
export LDFLAGS

$A/python-install/bin/python.host setup.py build_ext -b build/lib.android -t build/tmp.android build_ext
