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

"""
Tests for renpy.pygame.display: reporting whether an OpenGL context is current, which the interaction loop uses
to avoid touching the display while SDL has released the context (as it does while an Android app is paused).
"""

import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

# The root of the Ren'Py checkout, so the subprocess can import renpy.
ROOT: Path = Path(__file__).resolve().parents[2]

# Opens a GL window and prints whether a context is current before, after, and on another thread. It runs in a
# subprocess so the window and SDL video initialization don't affect the engine the other tests share.
SCRIPT: str = textwrap.dedent(
    """
    import threading
    from renpy import pygame

    try:
        pygame.display.init()
        before = pygame.display.gl_has_current_context()
        pygame.display.set_mode((64, 64), pygame.OPENGL)
    except pygame.error as e:
        print("NOGL", e)
        raise SystemExit(0)

    after = pygame.display.gl_has_current_context()

    other = []
    thread = threading.Thread(target=lambda: other.append(pygame.display.gl_has_current_context()))
    thread.start()
    thread.join()

    print(before, after, other[0])
    """
)


def test_gl_has_current_context() -> None:
    """
    gl_has_current_context is False before a GL window is opened, True on the thread that opened one, and False
    on another thread, since the current context is per thread. This uses SDL's offscreen video driver, and skips
    if that driver or an OpenGL context isn't available on this machine.
    """
    env = dict(os.environ, SDL_VIDEO_DRIVER="offscreen", PYTHONPATH=str(ROOT))

    result = subprocess.run(
        [sys.executable, "-c", SCRIPT], check=False, cwd=ROOT, env=env, capture_output=True, text=True, timeout=60
    )

    assert result.returncode == 0, result.stderr

    output = result.stdout.strip().splitlines()[-1]

    if output.startswith("NOGL"):
        pytest.skip(f"The offscreen video driver can't open an OpenGL window here: {output}")

    assert output == "False True False"
