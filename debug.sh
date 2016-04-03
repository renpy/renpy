#!/bin/bash
# This builds out of date modules using the default C compiler, and then
# runs them.


ROOT="$(dirname $(realpath $0))"


export RENPY_GDB="gdb --args"
. "$ROOT/run.sh" "$@"
