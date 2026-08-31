#!/usr/bin/env bash
#
# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Runs Ren'Py in a headless environment by creating a virtual Wayland
# (preferred) or X11 display server, configuring dummy audio, and invoking
# run.sh in the repository root.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
RUN_SH="$ROOT_DIR/run.sh"

if [ ! -f "$RUN_SH" ]; then
    echo "Error: run.sh not found in $ROOT_DIR" >&2
    exit 1
fi

# Configure dummy audio driver so audio operations succeed silently without sound hardware.
export SDL_AUDIODRIVER=dummy

# Process cleanup handler for virtual display servers and temporary runtime directories.
cleanup() {
    local exit_code=$?
    if [ -n "$SERVER_PID" ]; then
        kill "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
    fi
    if [ -n "$TEMP_RUNTIME_DIR" ] && [ -d "$TEMP_RUNTIME_DIR" ]; then
        rm -rf "$TEMP_RUNTIME_DIR"
    fi
    exit $exit_code
}

trap cleanup EXIT INT TERM HUP

if command -v weston >/dev/null 2>&1; then
    # Wayland preferred: use Weston with the headless backend.
    if [ -z "$XDG_RUNTIME_DIR" ] || [ ! -d "$XDG_RUNTIME_DIR" ] || [ ! -w "$XDG_RUNTIME_DIR" ]; then
        TEMP_RUNTIME_DIR="$(mktemp -d /tmp/renpy-xdg-runtime-XXXXXX)"
        chmod 0700 "$TEMP_RUNTIME_DIR"
        export XDG_RUNTIME_DIR="$TEMP_RUNTIME_DIR"
    fi

    SOCKET_NAME="wayland-renpy-$$"
    SOCKET_PATH="$XDG_RUNTIME_DIR/$SOCKET_NAME"

    # Start Weston headless compositor
    weston -B headless --no-config --socket="$SOCKET_NAME" >/dev/null 2>&1 &
    SERVER_PID=$!

    # Wait for the Wayland socket to become available
    MAX_WAIT=50
    WAITED=0
    while [ ! -S "$SOCKET_PATH" ]; do
        if ! kill -0 "$SERVER_PID" 2>/dev/null; then
            echo "Error: Weston failed to start in headless mode." >&2
            exit 1
        fi
        sleep 0.1
        WAITED=$((WAITED + 1))
        if [ "$WAITED" -ge "$MAX_WAIT" ]; then
            echo "Error: Timed out waiting for Weston Wayland socket at $SOCKET_PATH" >&2
            exit 1
        fi
    done

    export WAYLAND_DISPLAY="$SOCKET_NAME"
    export SDL_VIDEODRIVER=wayland
    export SDL_VIDEO_DRIVER=wayland
    unset DISPLAY

    set +e
    "$RUN_SH" "$@"
    EXIT_CODE=$?
    exit $EXIT_CODE

elif command -v xvfb-run >/dev/null 2>&1; then
    # X11 fallback: use xvfb-run with 24-bit color depth for OpenGL support.
    export SDL_VIDEODRIVER=x11
    export SDL_VIDEO_DRIVER=x11
    unset WAYLAND_DISPLAY

    exec xvfb-run -a -s "-screen 0 1920x1080x24" "$RUN_SH" "$@"

elif command -v Xvfb >/dev/null 2>&1; then
    # X11 fallback: start Xvfb directly if xvfb-run is not installed.
    DISP=99
    while [ -e "/tmp/.X${DISP}-lock" ] || [ -e "/tmp/.X11-unix/X${DISP}" ]; do
        DISP=$((DISP + 1))
    done

    Xvfb ":$DISP" -screen 0 1920x1080x24 >/dev/null 2>&1 &
    SERVER_PID=$!

    MAX_WAIT=50
    WAITED=0
    while [ ! -e "/tmp/.X11-unix/X${DISP}" ]; do
        if ! kill -0 "$SERVER_PID" 2>/dev/null; then
            echo "Error: Xvfb failed to start." >&2
            exit 1
        fi
        sleep 0.1
        WAITED=$((WAITED + 1))
        if [ "$WAITED" -ge "$MAX_WAIT" ]; then
            echo "Error: Timed out waiting for Xvfb display :$DISP" >&2
            exit 1
        fi
    done

    export DISPLAY=":$DISP"
    export SDL_VIDEODRIVER=x11
    export SDL_VIDEO_DRIVER=x11
    unset WAYLAND_DISPLAY

    set +e
    "$RUN_SH" "$@"
    EXIT_CODE=$?
    exit $EXIT_CODE

else
    echo "Error: No Wayland (weston) or X11 (xvfb-run/Xvfb) virtual display server found." >&2
    echo "Please install weston or xvfb (e.g. 'sudo apt install weston' or 'sudo apt install xvfb')." >&2
    exit 1
fi
