# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals # type: ignore
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import renpy
from renpy.exports.commonexports import renpy_pure


def movie_cutscene(filename, delay=None, loops=0, stop_music=True):
    """
    :doc: movie_cutscene

    This displays a movie cutscene for the specified number of
    seconds. The user can click to interrupt the cutscene.
    Overlays and Underlays are disabled for the duration of the cutscene.

    `filename`
        The name of a file containing any movie playable by Ren'Py.

    `delay`
        The number of seconds to wait before ending the cutscene.
        Normally the length of the movie, in seconds. If None, then the
        delay is computed from the number of loops (that is, loops + 1) *
        the length of the movie. If -1, we wait until the user clicks.

    `loops`
        The number of extra loops to show, -1 to loop forever.

    Returns True if the movie was terminated by the user, or False if the
    given delay elapsed uninterrupted.
    """

    renpy.exports.mode('movie')

    if stop_music:
        renpy.audio.audio.set_force_stop("music", True)

    renpy.exports.movie_start_fullscreen(filename, loops=loops)

    renpy.ui.saybehavior()

    if delay is None or delay < 0:
        renpy.ui.soundstopbehavior("movie")
    else:
        renpy.ui.pausebehavior(delay, False)

    if renpy.game.log.forward:
        roll_forward = True
    else:
        roll_forward = None

    rv = renpy.ui.interact(suppress_overlay=True,
                           roll_forward=roll_forward)

    # We don't want to put a checkpoint here, as we can't roll back while
    # playing a cutscene.

    renpy.exports.movie_stop()

    if stop_music:
        renpy.audio.audio.set_force_stop("music", False)

    return rv


def toggle_music():
    """
    :undocumented:
    Does nothing.
    """


def music_start(filename, loops=True, fadeout=None, fadein=0):
    """
    Deprecated music start function, retained for compatibility. Use
    renpy.music.play() or .queue() instead.
    """

    renpy.audio.music.play(filename, loop=loops, fadeout=fadeout, fadein=fadein)


def music_stop(fadeout=None):
    """
    Deprecated music stop function, retained for compatibility. Use
    renpy.music.stop() instead.
    """

    renpy.audio.music.stop(fadeout=fadeout)


def play(filename, channel=None, **kwargs):
    """
    :doc: audio

    Plays a sound effect. If `channel` is None, it defaults to
    :var:`config.play_channel`. This is used to play sounds defined in
    styles, :propref:`hover_sound` and :propref:`activate_sound`.
    """

    if filename is None:
        return

    if channel is None:
        channel = renpy.config.play_channel

    renpy.audio.music.play(filename, channel=channel, loop=False, **kwargs)
