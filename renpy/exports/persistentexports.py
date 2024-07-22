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

import re

import renpy


def seen_label(label):
    """
    :doc: label

    Returns true if the named label has executed at least once on the current user's
    system, and false otherwise. This can be used to unlock scene galleries, for
    example.
    """
    return label in renpy.game.persistent._seen_ever # type: ignore


def mark_label_seen(label):
    """
    :doc: label

    Marks the named label as if it has been already executed on the current user's
    system.
    """
    renpy.game.persistent._seen_ever[str(label)] = True # type: ignore


def mark_label_unseen(label):
    """
    :doc: label

    Marks the named label as if it has not been executed on the current user's
    system yet.
    """
    if label in renpy.game.persistent._seen_ever: # type: ignore
        del renpy.game.persistent._seen_ever[label] # type: ignore


def seen_audio(filename):
    """
    :doc: audio

    Returns True if the given filename has been played at least once on the current
    user's system.
    """
    filename = re.sub(r'^<.*?>', '', filename)

    return filename in renpy.game.persistent._seen_audio # type: ignore


def mark_audio_seen(filename):
    """
    :doc: audio

    Marks the given filename as if it has been already played on the current user's
    system.
    """
    filename = re.sub(r'^<.*?>', '', filename)

    renpy.game.persistent._seen_audio[filename] = True # type: ignore


def mark_audio_unseen(filename):
    """
    :doc: audio

    Marks the given filename as if it has not been played on the current user's
    system yet.
    """
    filename = re.sub(r'^<.*?>', '', filename)

    if filename in renpy.game.persistent._seen_audio: # type: ignore
        del renpy.game.persistent._seen_audio[filename] # type: ignore


def seen_image(name):
    """
    :doc: image_func

    Returns True if the named image has been seen at least once on the user's
    system. An image has been seen if it's been displayed using the show statement,
    scene statement, or :func:`renpy.show` function. (Note that there are cases
    where the user won't actually see the image, like a show immediately followed by
    a hide.)
    """
    if not isinstance(name, tuple):
        name = tuple(name.split())

    return name in renpy.game.persistent._seen_images # type: ignore


def mark_image_seen(name):
    """
    :doc: image_func

    Marks the named image as if it has been already displayed on the current user's
    system.
    """
    if not isinstance(name, tuple):
        name = tuple(name.split())

    renpy.game.persistent._seen_images[tuple(str(i) for i in name)] = True


def mark_image_unseen(name):
    """
    :doc: image_func

    Marks the named image as if it has not been displayed on the current user's
    system yet.
    """
    if not isinstance(name, tuple):
        name = tuple(name.split())

    if name in renpy.game.persistent._seen_images: # type: ignore
        del renpy.game.persistent._seen_images[name] # type: ignore


def save_persistent():
    """
    :doc: persistent

    Saves the persistent data to disk.
    """

    renpy.persistent.update(True)


def is_seen(ever=True):
    """
    :doc: other

    Returns true if the current line has been seen by the player.

    If `ever` is true, we check to see if the line has ever been seen by the
    player. If false, we check if the line has been seen in the current
    play-through.
    """

    return renpy.game.context().seen_current(ever)
