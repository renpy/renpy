#!/bin/sh

# We assume Darwin means Mac OS X. Sorry, Darwin guys.
if [ "x`uname -s`" = "xDarwin" ]; then
    dir=`dirname "$0"`
    dir=`cd "$dir"; pwd`
    base=`basename "$0"`

    export RENPY_LAUNCHER_DIR="$dir"

    if [ -e "$dir/${base%.sh}.app/Contents/MacOS/${base%.sh}" ] ; then
        launcher="$dir/${base%.sh}.app/Contents/MacOS/${base%.sh}"
    else
        launcher="$dir/${base%.sh}.app/Contents/MacOS/Ren'Py Launcher"
    fi

    exec "$launcher" "${0%.sh}.py" "$@"
fi

exec "`dirname \"$0\"`/lib/python" "-OO" "${0%.sh}.py" "$@"
