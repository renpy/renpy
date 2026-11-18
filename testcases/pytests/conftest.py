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
Shared pytest configuration for Ren'Py's Python tests.

Importing this module starts the engine with ``renpy.import_all()``. pytest imports conftest.py before it
collects the test modules, so the tests can import engine names at module level. Engine startup runs once
per process and records the reload backup, so tests must never call ``renpy.import_all()`` themselves.
"""

import os

import pytest

import renpy

renpy.import_all()


@pytest.fixture
def surface_deallocation():
    """
    Gives the test a freshly initialized surface-deallocation tracker.

    Teardown shuts the tracker down to discard any state from the test, then initializes it again so later
    tests and engine code find it in its normal running state.
    """

    renpy.pygame.surface._init_surface_deallocation()
    yield
    renpy.pygame.surface._quit_surface_deallocation()
    renpy.pygame.surface._init_surface_deallocation()


@pytest.fixture
def windows_replace(mocker):
    """
    Patches os.replace to refuse an existing destination, as Windows does when another program has it open.

    The program is assumed to allow deletion, so moving the file to an unused name still works. Returns the mock, so
    a test can extend its behavior. os.replace is patched module-wide, so the real function is captured first.
    """

    replace = os.replace

    def refuse_existing(source, destination):
        if os.path.exists(destination):
            raise PermissionError("destination is open")
        replace(source, destination)

    return mocker.patch("renpy.loadsave.os.replace", side_effect=refuse_existing)


@pytest.fixture
def audio():
    """
    Provide an AudioHarness with SDL's dummy audio driver and an initialized renpysound mixer.

    Shared by the test_audio_renpysound_*.py modules. The SDL_AUDIO_DRIVER hint is restored after the test,
    and renpysound.quit() runs before the restore. The harness module is imported here, rather than at the
    top of this file, so that it is loaded after the engine has been started.
    """

    from renpy.audio import renpysound

    from .audio_harness import AudioHarness

    harness = AudioHarness()
    hint = b"SDL_AUDIO_DRIVER"
    original = harness.native.SDL_GetHint(hint)
    assert harness.native.SDL_SetHint(hint, b"dummy")
    try:
        harness.initialize()
        try:
            yield harness
        finally:
            renpysound.quit()
    finally:
        if original is None:
            harness.native.SDL_ResetHint(hint)
        else:
            harness.native.SDL_SetHint(hint, original)
