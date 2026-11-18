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

from types import SimpleNamespace

import pytest

import renpy
from renpy.display import video


class FakeMovie:
    """
    Stands in for a Movie displayable in update_playing, recording the play and stop calls it receives.

    update_playing only calls play, stop, and release_channel and reads loop, so a real Movie (which
    needs audio channels and a renderer) is not required to check which movies get restarted.
    """

    def __init__(self, loop: bool = True) -> None:
        self.loop = loop
        self.calls: list[tuple[str, object]] = []

    def play(self, old: object) -> None:
        self.calls.append(("play", old))

    def stop(self) -> None:
        self.calls.append(("stop", None))

    def release_channel(self) -> None:
        pass


@pytest.fixture
def playing_state(mocker):
    """
    Isolates update_playing's module state and the current context, restoring both afterwards.

    Returns a function that sets the movies shown this interaction, the movies shown in the last
    interaction, and the movies the current context remembers.
    """

    context = SimpleNamespace(movie={})
    mocker.patch.object(renpy.game, "context", return_value=context)
    mocker.patch.object(video, "channel_movie", {})
    mocker.patch.object(video, "last_channel_movie", {})
    mocker.patch.object(video, "reset_channels", set())

    def setup(current: dict, last: dict, old: dict) -> SimpleNamespace:
        video.channel_movie.update(current)
        video.last_channel_movie = dict(last)
        context.movie = dict(old)
        return context

    return setup


def test_movie_continues_after_leaving_context(playing_state):
    """
    A movie still shown after leaving the main menu context keeps playing instead of restarting.

    Starting or loading a game jumps out of the main menu context into one that doesn't remember the
    movie, while the movie stays on screen (for example, during the transition). Restarting it there
    makes the video visibly jump back to its start.
    """

    m = FakeMovie()
    context = playing_state({"c": m}, last={"c": m}, old={})

    video.update_playing()

    assert m.calls == []
    assert context.movie == {"c": m}


@pytest.mark.parametrize(
    "loop, replayed",
    [
        (True, True),
        (False, False),
    ],
)
def test_rollback_to_other_movie_on_shared_channel(playing_state, loop, replayed):
    """
    Rolling back to a looping movie plays it when another movie has taken over its channel.

    After the rollback the context remembers the movie again, but a different movie sharing the channel
    (an explicit channel, or config.single_movie_channel) was shown in the last interaction, so the
    channel is still playing that movie's file. A non-looping movie is left alone, so that rollback
    doesn't replay it from the beginning.
    """

    m = FakeMovie(loop=loop)
    other = FakeMovie()
    playing_state({"c": m}, last={"c": other}, old={"c": m})

    video.update_playing()

    assert m.calls == ([("play", other)] if replayed else [])


def test_movie_replaces_movie_remembered_by_context(playing_state):
    """
    A movie differing from the one the context remembers is played, even if it was shown last interaction.

    Only a context with no movie on the channel counts as not knowing about it; a different remembered
    movie means the context's state and the shown movie disagree, so the movie is played against it.
    """

    m = FakeMovie()
    remembered = FakeMovie()
    playing_state({"c": m}, last={"c": m}, old={"c": remembered})

    video.update_playing()

    assert m.calls == [("play", remembered)]


def test_newly_shown_movie_plays(playing_state):
    """A movie shown for the first time, unknown to both the context and the last interaction, starts playing."""

    m = FakeMovie()
    playing_state({"c": m}, last={}, old={})

    video.update_playing()

    assert m.calls == [("play", None)]


def test_hidden_movie_stops(playing_state):
    """A movie shown in the last interaction but not in this one is stopped."""

    m = FakeMovie()
    context = playing_state({}, last={"c": m}, old={"c": m})

    video.update_playing()

    assert m.calls == [("stop", None)]
    assert context.movie == {}
