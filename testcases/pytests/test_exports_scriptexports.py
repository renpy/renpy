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


"""Tests that renpy.load_string, load_module, and load_language restore engine state when they fail."""

from types import SimpleNamespace

import pytest

import renpy
from renpy.exports import scriptexports


@pytest.fixture
def script(mocker):
    """
    Replaces renpy.game.script with a mock and gives the test a known config.locked and context stack.

    Parsing and running real script would need a running game, and these tests only look at what the loaders do
    to config.locked and renpy.game.contexts. Both are restored on teardown.
    """

    old_contexts = list(renpy.game.contexts)
    old_locked = renpy.config.locked

    mocker.patch.object(renpy.game, "script", mocker.Mock())
    renpy.config.locked = True

    yield renpy.game.script

    renpy.config.locked = old_locked
    renpy.game.contexts[:] = old_contexts


def make_node(mocker, error=None):
    """Returns a fake init node whose execute_init raises `error`, if given."""

    return mocker.Mock(execute_init=mocker.Mock(side_effect=error))


def test_load_string_parse_error_relocks(script):
    """A parse error makes load_string return None, and config.locked must be restored, not left False."""

    script.load_string.return_value = (None, None)

    assert scriptexports.load_string("bogus") is None
    assert renpy.config.locked is True


def test_load_string_empty_raises(script):
    """A string with no statements raises ValueError instead of IndexError, and restores config.locked."""

    script.load_string.return_value = ([], [])

    with pytest.raises(ValueError):
        scriptexports.load_string("")

    assert renpy.config.locked is True


def test_load_string_returns_first_name(script, mocker):
    """On success load_string returns the first statement's name, runs init code, and restores state."""

    node = make_node(mocker)
    script.load_string.return_value = ([SimpleNamespace(name="first")], [(0, node)])
    depth = len(renpy.game.contexts)

    assert scriptexports.load_string("x") == "first"

    node.execute_init.assert_called_once()
    assert renpy.config.locked is True
    assert len(renpy.game.contexts) == depth


def test_load_string_init_error_restores_state(script, mocker):
    """An exception in init code propagates, but config.locked and the context stack are restored."""

    script.load_string.return_value = ([mocker.Mock()], [(0, make_node(mocker, RuntimeError("boom")))])
    depth = len(renpy.game.contexts)

    with pytest.raises(RuntimeError):
        scriptexports.load_string("x")

    assert renpy.config.locked is True
    assert len(renpy.game.contexts) == depth


def test_load_module_init_error_restores_state(script, mocker):
    """An exception in a module's init code restores config.locked and the context stack."""

    mocker.patch.object(scriptexports, "loaded_modules", set())
    mocker.patch.object(renpy.game, "context", return_value=mocker.Mock(init_phase=True))
    script.load_module.return_value = [(0, make_node(mocker, RuntimeError("boom")))]
    depth = len(renpy.game.contexts)

    with pytest.raises(RuntimeError):
        scriptexports.load_module("m")

    assert renpy.config.locked is True
    assert len(renpy.game.contexts) == depth


def test_load_language_init_error_restores_state(script, mocker):
    """An exception in a language's init code restores config.locked and the context stack."""

    mocker.patch.object(renpy.config, "defer_tl_scripts", True)
    script.load_languages = set()
    script.load_script.return_value = [(0, make_node(mocker, RuntimeError("boom")))]
    depth = len(renpy.game.contexts)

    with pytest.raises(RuntimeError):
        scriptexports.load_language("french")

    assert renpy.config.locked is True
    assert len(renpy.game.contexts) == depth


@pytest.mark.parametrize("error", [None, RuntimeError("boom")])
def test_load_module_kwargs_restored(script, mocker, error):
    """load_module kwargs are visible to init code and the store value is restored afterward, even on error."""

    mocker.patch.object(scriptexports, "loaded_modules", set())
    mocker.patch.object(renpy.game, "context", return_value=mocker.Mock(init_phase=True))
    mocker.patch.object(renpy.store, "_load_string_test", "old", create=True)

    seen = []

    def execute_init():
        seen.append(renpy.store._load_string_test)

        if error is not None:
            raise error

    script.load_module.return_value = [(0, mocker.Mock(execute_init=execute_init))]

    if error is None:
        scriptexports.load_module("m", _load_string_test="new")
    else:
        with pytest.raises(RuntimeError):
            scriptexports.load_module("m", _load_string_test="new")

    assert seen == ["new"]
    assert renpy.store._load_string_test == "old"
