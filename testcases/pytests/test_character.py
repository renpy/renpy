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
Tests for how renpy.character.ADVCharacter behaves while warp is replaying dialogue: which say attributes it
applies, and what it records in the history.
"""

from types import SimpleNamespace

import pytest

import renpy
from renpy import character, warp


@pytest.fixture(autouse=True)
def warp_context(mocker):
    """
    Provides the script context that say and history code read and write, with ``rollback`` enabled, as the
    current context for every test in this module.
    """

    context = SimpleNamespace(
        say_attributes=None,
        temporary_attributes=None,
        rollback=True,
    )

    mocker.patch.object(renpy.game, "context", return_value=context)

    return context


@pytest.fixture
def warp_store(mocker):
    """
    Provides the store fields that history code touches, and makes it the script-visible store.
    """

    store = SimpleNamespace(_history=True, _history_list=[])
    mocker.patch.object(renpy, "store", store)

    return store


@pytest.mark.parametrize("warping", [True, False], ids=["warping", "not-warping"])
def test_character_applies_temporary_and_speaking_attributes_only_outside_warp(mocker, warp_context, warping):
    """
    A character resolves a say's permanent attributes in both cases, but its temporary attributes and the
    configured speaking attribute only when the say is really shown. During warp nothing is left to restore
    afterwards, so no attributes leak into the context.

    The image manager is a mock, and the character records what it is asked to resolve rather than showing
    anything. The not-warping case is the control: it shows that the same call does resolve the temporary
    and speaking attributes, so the warping case is not passing because they are ignored for some other reason.
    """

    c = character.ADVCharacter.__new__(character.ADVCharacter)
    c.image_tag = "speaker"
    warp_context.images = mocker.Mock()
    warp_context.images.get_attributes.return_value = ("permanent",)
    warp_context.say_attributes = ("permanent",)
    warp_context.temporary_attributes = ("temporary",)
    resolved = []

    def resolve(predicting, attrs):
        resolved.append(attrs)
        return True

    mocker.patch.object(c, "resolve_say_attributes", side_effect=resolve)
    mocker.patch.object(c, "handle_say_transition")
    mocker.patch.object(warp, "warping", warping)
    mocker.patch.object(renpy.config, "speaking_attribute", "speaking")

    state = c.handle_say_attributes(False, True)

    if warping:
        assert resolved == [("permanent",)]
        assert state is None
    else:
        assert resolved == [("permanent",), ["speaking", "temporary"]]
        assert state is not None

    assert warp_context.say_attributes is None
    assert warp_context.temporary_attributes is None


def test_reconstructed_history_has_no_rollback_identifier(mocker, warp_store):
    """
    History entries added during warp have no rollback identifier, and the history length limit still applies.
    """

    c = character.ADVCharacter.__new__(character.ADVCharacter)
    c.who_args = c.what_args = c.window_args = c.show_args = {}
    c.image_tag = None
    warping_patch = mocker.patch.object(warp, "warping", True)
    length_patch = mocker.patch.object(renpy.config, "history_length", 1)
    callbacks_patch = mocker.patch.object(renpy.config, "history_callbacks", [])
    c.do_done("Name", "one")
    c.do_done("Name", "two")
    mocker.stop(callbacks_patch)
    mocker.stop(length_patch)
    mocker.stop(warping_patch)

    assert [h.what for h in warp_store._history_list] == ["two"]
    assert warp_store._history_list[0].rollback_identifier is None


def test_disabled_history_stays_empty(mocker, warp_store):
    """
    With history disabled in config or in the store, reconstructed dialogue is not added to the history list.
    """

    c = character.ADVCharacter.__new__(character.ADVCharacter)
    history_length = mocker.patch.object(renpy.config, "history_length", None)
    c.do_done("Name", "line")
    mocker.stop(history_length)

    warp_store._history = False
    history_length = mocker.patch.object(renpy.config, "history_length", 10)
    c.do_done("Name", "line")
    mocker.stop(history_length)

    assert warp_store._history_list == []
