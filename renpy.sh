#!/bin/sh

# The directory containing this shell script - an absolute path.
ROOT=$(dirname "$0")
ROOT=$(cd "$ROOT"; pwd)

# The name of this shell script without the .sh on the end.
BASEFILE=$(basename "$0" .sh)

# The full path to the shell script, without the .sh at the end of it.
BASE="$ROOT/$BASEFILE"

# Assume Darwin means Mac OS X, and launch us using the OS X launcher.
if [ "$(uname -s)" = "Darwin" ] ; then

    RENPY_LAUNCHER_DIR="$ROOT"
    export RENPY_LAUNCHER_DIR
    
    if [ -e "${BASE}.app/Contents/MacOS/${BASEFILE}" ] ; then
        LAUNCHER="${BASE}.app/Contents/MacOS/${BASEFILE}"
    else
        LAUNCHER="${BASE}.app/Contents/MacOS/Ren'Py Launcher"
    fi

    exec $RENPY_GDB "${LAUNCHER}" "${BASE}.py" "$@"
fi 

# Otherwise, assume we're on linux, or an OS that can run Linux binaries.
# If that's not the case, you'll have to change this script.

if [ -z "$RENPY_PLATFORM" ] ; then
    case `uname -m` in
        x86_64|amd64)
            RENPY_PLATFORM="linux-x86_64"
            ;;
        i*86)
            RENPY_PLATFORM="linux-i686"
            ;;
        *)
            echo "Ren'Py could not detect that platform it's running on. Please set"
            echo "the RENPY_PLATFORM environment variable to one of \"linux-i686\" or"
            echo "\"linux-x86_64\", and run this command again."
            exit 1
            ;;
    esac
fi

LIB="$ROOT/lib/$RENPY_PLATFORM"

RENPY_ORIGINAL_LD_LIBRARY_PATH="$LD_LIBRARY_PATH"

if [ -z "$LD_LIBRARY_PATH" ] ; then
    LD_LIBRARY_PATH="$LIB"
else
    LD_LIBRARY_PATH="$LIB:$LD_LIBRARY_PATH"
fi

export LD_LIBRARY_PATH
export RENPY_PLATFORM
export RENPY_ORIGINAL_LD_LIBRARY_PATH

exec $RENPY_GDB "$LIB/python" $RENPY_PYARGS -OO "$BASE.py" "$@"
