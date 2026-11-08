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

"""Tests for renpy/display/presplash.py: ending the presplash on desktop and on the web."""

import renpy
from renpy.display import presplash


def test_web_overlay_remains_during_display_initialization(mocker) -> None:
    """On the web, ending presplash marks it done without asking the browser to remove the overlay."""
    browser = mocker.Mock()

    mocker.patch.object(renpy, "emscripten", True)
    mocker.patch.object(presplash, "emscripten", browser, create=True)
    mocker.patch.object(presplash, "window", None)
    mocker.patch.object(presplash, "done", False)

    presplash.end()

    assert presplash.done
    browser.run_script.assert_not_called()


def test_desktop_window_and_images_are_released(mocker) -> None:
    """On desktop, ending presplash destroys the window, quits pygame's display, and clears the window and progress bar."""
    window = mocker.Mock()

    mocker.patch.object(renpy, "emscripten", False)
    mocker.patch.object(presplash, "window", window)
    mocker.patch.object(presplash, "progress_bar", mocker.Mock())
    mocker.patch.object(presplash, "done", False)
    quit_display = mocker.patch.object(presplash.pygame.display, "quit")

    presplash.end()

    window.destroy.assert_called_once_with()
    quit_display.assert_called_once_with()
    assert presplash.window is None
    assert presplash.progress_bar is None
    assert presplash.done
