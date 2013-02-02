#!/bin/sh

# The directory containing this shell script - an absolute path.
ROOT=$(dirname "$0")
ROOT=$(cd "$ROOT"; pwd)

# The name of this shell script without the .sh on the end.
BASEFILE=$(basename "$0" .sh)

# The full path to the shell script, without the .sh at the end of it.
BASE="$ROOT/$BASEFILE"

# Otherwise, assume we're on linux, or an OS that can run Linux binaries.
# If that's not the case, you'll have to change this script.

if [ -z "$RENPY_PLATFORM" ] ; then
    case "$(uname -s)-$(uname -m)" in
        Darwin-*)
            RENPY_PLATFORM="darwin-x86_64"
            ;;        
        *-x86_64|amd64)
            RENPY_PLATFORM="linux-x86_64"
            ;;
        *-i*86)
            RENPY_PLATFORM="linux-i686"
            ;;
        *)
            echo "Ren'Py could not detect that platform it's running on. Please set"
            echo "the RENPY_PLATFORM environment variable to one of \"linux-i686\" or"
            echo "\"linux-x86_64\", or \"darwin-x86_64\" and run this command again."
            exit 1
            ;;
    esac
fi

LIB="$ROOT/lib/$RENPY_PLATFORM"
exec $RENPY_GDB "$LIB/python" $RENPY_PYARGS -OO "$BASE.py" "$@"
