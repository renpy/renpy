#!/bin/sh

SCRIPT="$0"

# Resolve the chain of symlinks leading to this script.
while [ -L "$SCRIPT" ] ; do
    LINK=$(readlink "$SCRIPT")

    case "$LINK" in
        /*)
            SCRIPT="$LINK"
            ;;
        *)
            SCRIPT="$(dirname "$SCRIPT")/$LINK"
            ;;
    esac
done

# The directory containing this shell script - an absolute path.
ROOT=$(dirname "$SCRIPT")
ROOT=$(cd "$ROOT"; pwd)

# The name of this shell script without the .sh on the end.
BASEFILE=$(basename "$SCRIPT" .sh)

if [ -z "$RENPY_PLATFORM" ] ; then
    RENPY_PLATFORM="$(uname -s)-$(uname -m)"

    case "$RENPY_PLATFORM" in
        Darwin-*)
            RENPY_PLATFORM="darwin-x86_64"
            ROOT1="$ROOT/../Resources/autorun"
            ROOT2="$ROOT/../../.."
            export DYLD_INSERT_LIBRARIES="${DYLD_INSERT_LIBRARIES:-${STEAM_DYLD_INSERT_LIBRARIES}}"
                        ;;
        *-x86_64|amd64)
            RENPY_PLATFORM="linux-x86_64"
            ROOT1="$ROOT"
            ROOT2="$ROOT"
            ;;
        *-i*86)
            RENPY_PLATFORM="linux-i686"
            ROOT1="$ROOT"
            ROOT2="$ROOT"
            ;;
        Linux-*)
            RENPY_PLATFORM="linux-$(uname -m)"
            ROOT1="$ROOT"
            ROOT2="$ROOT"
            ;;
        *)
            ROOT1="$ROOT"
            ROOT2="$ROOT"
            ;;
    esac
fi


for BASE in "$ROOT" "$ROOT1" "$ROOT2"; do
    LIB="$BASE/lib/$RENPY_PLATFORM"
    if test -d "$LIB"; then
        break
    fi
done

for BASE in "$ROOT" "$ROOT1" "$ROOT2"; do
    if test -e "$BASE/$BASEFILE.py"; then
        break
    fi
done

if ! test -d "$LIB"; then
    echo "Ren'Py platform files not found in:"
    echo
    echo "$ROOT/lib/$RENPY_PLATFORM"
    echo
    echo "Please compile the platform files using the instructions in README.md"
    echo "or point them to an existing installation using ./after_checkout.sh <path>."
    echo
    echo "Alternatively, please set RENPY_PLATFORM to a different platform."
    exit 1
fi

if test -n "$LD_LIBRARY_PATH"; then
    export LD_LIBRARY_PATH="$LIB:$LD_LIBRARY_PATH"
fi

exec $RENPY_GDB "$LIB/$BASEFILE" $RENPY_PYARGS -EO "$BASE/$BASEFILE.py" "$@"
