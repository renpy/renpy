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
Tests for renpy/display/error.py: which actions the exception screen is offered.
"""

from types import SimpleNamespace

import pytest

import renpy
import renpy.display.error


@pytest.fixture
def exception_screen_kwargs(mocker):
    """
    Stubs out the display, the error dump, and the screen interaction, so report_exception runs as it would in a
    game, and returns the dict that receives the keyword arguments the exception screen would be shown with.
    """

    shown = {}

    def invoke_in_new_context(fn, screen_name, **kwargs):
        shown.update(kwargs)

    mocker.patch.object(renpy.display.error, "error_dump")
    mocker.patch.object(renpy.display.error, "init_display")
    mocker.patch.object(renpy.display, "draw", object())
    mocker.patch.object(renpy.game, "args", SimpleNamespace(command="run"))
    mocker.patch.object(renpy.exports, "has_screen", return_value=True)
    mocker.patch.object(renpy.game, "invoke_in_new_context", invoke_in_new_context)
    mocker.patch.object(renpy.store, "_ignore_action", None, create=True)
    mocker.patch.object(renpy.store, "te", None, create=True)
    mocker.patch.object(renpy.display.error, "error_handled", renpy.display.error.error_handled)
    mocker.patch.object(renpy.config, "raise_image_exceptions", renpy.config.raise_image_exceptions)
    mocker.patch.object(
        renpy.display.im.thread_local,
        "raise_image_load_exceptions",
        renpy.display.im.thread_local.raise_image_load_exceptions,
    )
    mocker.patch.object(renpy.display.im, "ignored_images", set(renpy.display.im.ignored_images))
    mocker.patch.dict(renpy.display.error.os.environ)
    renpy.display.error.os.environ.pop("RENPY_SIMPLE_EXCEPTIONS", None)

    return shown


@pytest.mark.parametrize(
    ("top_init_phase", "current_init_phase", "init_exception_ignore", "offered"),
    [
        (False, False, False, True),
        (True, True, False, False),
        (True, True, True, True),
        (True, False, False, False),
        (False, True, False, False),
    ],
)
def test_ignore_offered_outside_init(
    mocker, exception_screen_kwargs, top_init_phase, current_init_phase, init_exception_ignore, offered
):
    """
    The Ignore button is offered for an exception during the game, but not for one during init, since ignoring
    it leaves the game partly initialized, unless config.init_exception_ignore opts back in. The last case is a
    context created by renpy.call_in_new_context during init, which isn't itself marked as in the init phase but
    must still hide Ignore; the one after it is init code run by renpy.load_string on top of a running game. Contexts are stand-ins because report_exception only reads whether they are in init
    and whether there is a next node.
    """

    top = SimpleNamespace(init_phase=top_init_phase, next_node=object())
    current = SimpleNamespace(init_phase=current_init_phase, next_node=object())
    mocker.patch.object(renpy.game, "contexts", [top, current])
    mocker.patch.object(renpy.game, "context", return_value=current)
    mocker.patch.object(renpy.config, "init_exception_ignore", init_exception_ignore)

    assert renpy.display.error.report_exception(mocker.Mock()) is False
    assert (exception_screen_kwargs["ignore_action"] is not None) == offered
