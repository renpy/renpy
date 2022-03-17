# Copyright 2004-2022 Tom Rothamel <pytom@bishoujo.us>
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

# The public API for sound playback from games.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *



import renpy.audio

# This is basically a thin wrapper around music, with the default
# channel set to "sound".


def play(filename, channel="sound", fadeout=0, fadein=0, tight=False, loop=False, relative_volume=1.0):
    renpy.audio.music.play(filename,
                           channel=channel,
                           fadeout=fadeout,
                           fadein=fadein,
                           tight=tight,
                           loop=loop,
                           relative_volume=relative_volume)


def queue(filename, channel="sound", clear_queue=True, fadein=0, tight=False, loop=False, relative_volume=1.0):
    renpy.audio.music.queue(filename,
                            channel=channel,
                            clear_queue=clear_queue,
                            fadein=fadein,
                            tight=tight,
                            loop=loop,
                            relative_volume=relative_volume)


def stop(channel="sound", fadeout=0):
    renpy.audio.music.stop(channel=channel,
                           fadeout=fadeout)


set_mixer = renpy.audio.music.set_mixer
set_queue_empty_callback = renpy.audio.music.set_queue_empty_callback


def set_volume(volume, delay=0, channel="sound"):
    renpy.audio.music.set_volume(volume, delay, channel=channel)


def set_pan(pan, delay, channel="sound"):
    renpy.audio.music.set_pan(pan, delay, channel=channel)


def is_playing(channel="sound"):
    return renpy.audio.music.is_playing(channel=channel)


def get_playing(channel="sound"):
    return renpy.audio.music.get_playing(channel=channel)
