#!/bin/sh

# We assume Darwin means Mac OS X. Sorry, Darwin guys.
if [ "x`uname -s`" = "xDarwin" ]; then
    dir=`dirname "$0"`
    dir=`cd $dir; pwd`
    base=`basename "$0"`

    export RENPY_LAUNCHER_DIR="`pwd`"
    exec "${0%.sh}.app/Contents/MacOS/Ren'Py Launcher" "$dir/${base%.sh}.py" "$@"
fi

exec "`dirname \"$0\"`/lib/python" "-O" "${0%.sh}.py" "$@"
