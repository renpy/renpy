# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import renpy
import emscripten # type: ignore
import pygame
from json import dumps

import renpy.audio.renpysound as renpysound

# True if the browser only supports video decoding (not audio)
video_only = False

def call(function, *args):
    """
    Calls a method on `function`.
    """

    emscripten.run_script("renpyAudio.{}.apply(null, {});".format(function, dumps(args)))


def call_int(function, *args):
    """
    Calls a method on `function`.
    """

    return emscripten.run_script_int("renpyAudio.{}.apply(null, {});".format(function, dumps(args)))


def call_str(function, *args):
    """
    Calls a method on `function`.
    """

    rv = emscripten.run_script_string("renpyAudio.{}.apply(null, {});".format(function, dumps(args)))

    return rv

# Set of channel IDs that are not video channels
audio_channels = set()

def set_movie_channel(channel, movie):
    if video_only and not movie:
        audio_channels.add(channel)

renpysound.set_movie_channel = set_movie_channel # type: ignore

# Map of renpysound functions that have been replaced with webaudio functions
renpysound_funcs = {}

def proxy_with_channel(func):
    """
    Call the webaudio function instead of the renpysound function for audio channels if browser
    supports audio decoding.
    Always call the webaudio function instead of the renpysound function for video channels.
    """

    def hook(channel, *args, **kwargs):
        if video_only and channel in audio_channels:
            return renpysound_funcs[func.__name__](channel, *args, **kwargs)

        return func(channel, *args, **kwargs)

    if func.__name__ not in renpysound_funcs:
        renpysound_funcs[func.__name__] = getattr(renpysound, func.__name__)
    setattr(renpysound, func.__name__, hook)

    return func

def proxy_call_both(func):
    """
    Call renpysound function followed by webaudio function if browser does not support
    audio decoding.
    Only call the webaudio function if browser supports audio decoding.
    """

    def hook(*args, **kwargs):
        if video_only:
            ret1 = renpysound_funcs[func.__name__](*args, **kwargs)
            ret2 = func(*args, **kwargs)
            # Combine both return value (for init() only)
            return ret1 and ret2

        return func(*args, **kwargs)

    if func.__name__ not in renpysound_funcs:
        renpysound_funcs[func.__name__] = getattr(renpysound, func.__name__)
    setattr(renpysound, func.__name__, hook)

    return func

@proxy_with_channel
def play(channel, file, name, paused=False, fadein=0, tight=False, start=0, end=0, relative_volume=1.0):
    """
    Plays `file` on `channel`. This clears the playing and queued samples and
    replaces them with this file.

    `name`
        A python object giving a readable name for the file.

    `paused`
        If True, playback is paused rather than started.

    `fadein`
        The time it should take the fade the music in, in seconds.

    `tight`
        If true, the file is played in tight mode. This means that fadeouts
        can span between this file and the file queued after it.

    `start`
        A time in the file to start playing.

    `end`
        A time in the file to end playing.    `

    `relative_volume`
        A number between 0 and 1 that controls the relative volume of this file
    """

    try:
        if not isinstance(file, basestring):
            file = file.name
    except Exception:
        return

    call("stop", channel)
    call("queue", channel, file, name, paused, fadein, tight, start, end, relative_volume)


@proxy_with_channel
def queue(channel, file, name, fadein=0, tight=False, start=0, end=0, relative_volume=1.0):
    """
    Queues `file` on `channel` to play when the current file ends. If no file is
    playing, plays it.

    The other arguments are as for play.
    """

    try:
        if not isinstance(file, basestring):
            file = file.name
    except Exception:
        return

    call("queue", channel, file, name, False, fadein, tight, start, end, relative_volume)


@proxy_with_channel
def stop(channel):
    """
    Immediately stops `channel`, and unqueues any queued audio file.
    """

    call("stop", channel)


@proxy_with_channel
def dequeue(channel, even_tight=False):
    """
    Dequeues the queued sound file.

    `even_tight`
        If true, a queued sound file that is tight is not dequeued. If false,
        a file marked as tight is dequeued.
    """

    call("dequeue", channel, even_tight)


@proxy_with_channel
def queue_depth(channel):
    """
    Returns the queue depth of the channel. 0 if no file is playing, 1 if
    a files is playing but there is no queued file, and 2 if a file is playing
    and one is queued.
    """

    return emscripten.run_script_int("renpyAudio.queue_depth({})".format(channel))


@proxy_with_channel
def playing_name(channel):
    """
    Returns the `name`  argument of the playing sound. This was passed into
    `play` or `queue`.
    """

    rv = call_str("playing_name", channel)

    if rv:
        return rv

    return None


@proxy_with_channel
def pause(channel):
    """
    Pauses `channel`.
    """

    call("pause", channel)


@proxy_with_channel
def unpause(channel):
    """
    Unpauses `channel`.
    """

    call("unpause", channel)


@proxy_call_both
def unpause_all_at_start():
    """
    Unpauses all channels that are paused.
    """

    call("unpauseAllAtStart")


@proxy_with_channel
def fadeout(channel, delay):
    """
    Fades out `channel` over `delay` seconds.
    """

    call("fadeout", channel, delay)


@proxy_with_channel
def busy(channel):
    """
    Returns true if `channel` is currently playing something, and false
    otherwise
    """

    return queue_depth(channel) > 0


@proxy_with_channel
def get_pos(channel):
    """
    Returns the position of the audio file playing in `channel`. Returns None
    if not file is is playing or it is not known.
    """

    rv = call_int("get_pos", channel)

    if rv >= 0:
        return rv / 1000.0
    else:
        return None


@proxy_with_channel
def get_duration(channel):
    """
    Returns the duration of the audio file playing in `channel`, or None if no
    file is playing or it is not known.
    """

    rv = call_int("get_duration", channel)

    if rv >= 0:
        return rv / 1000.0
    else:
        return None


@proxy_with_channel
def set_volume(channel, volume):
    """
    Sets the primary volume for `channel` to `volume`, a number between
    0 and 1. This volume control is perceptual, taking into account the
    logarithmic nature of human hearing.
    """

    call("set_volume", channel, volume)


@proxy_with_channel
def set_pan(channel, pan, delay):
    """
    Sets the pan for channel.

    `pan`
        A number between -1 and 1 that control the placement of the audio.
        If this is -1, then all audio is sent to the left channel.
        If it's 0, then the two channels are equally balanced. If it's 1,
        then all audio is sent to the right ear.

    `delay`
        The amount of time it takes for the panning to occur.
    """

    call("set_pan", channel, pan, delay)


@proxy_with_channel
def set_secondary_volume(channel, volume, delay):
    """
    Sets the secondary volume for channel. This is linear, and is multiplied
    with the primary volume and scale factors derived from pan to find the
    actual multiplier used on the samples.

    `delay`
        The time it takes for the change in volume to happen.
    """

    call("set_secondary_volume", channel, volume, delay)


@proxy_with_channel
def get_volume(channel):
    """
    Gets the primary volume associated with `channel`.
    """

    return call_int("get_volume", channel)


@proxy_with_channel
def video_ready(channel):
    """
    Returns true if the video playing on `channel` has a frame ready for
    presentation.
    """

    if not video_supported():
        return False

    return call_int("video_ready", channel)

channel_size = {}

@proxy_with_channel
def read_video(channel):
    """
    Returns the frame of video playing on `channel`. This is returned as a GLTexture.
    """

    if not video_supported():
        return None

    video_size = channel_size.get(channel)
    if video_size is None:
        info = call_str("get_video_size", channel)
        if len(info) == 0:
            # Video dimension not ready yet
            return None
        video_size = [int(s) for s in info.split('x')]
        channel_size[channel] = video_size

    # Generate a new texture and pass it to JS
    tex = renpy.gl2.gl2texture.Texture(video_size, renpy.display.draw.texture_loader, generate=True)

    res = call_int("read_video", channel, tex.get_number(), *video_size)
    if res == 0:
        return tex

    if res > 0:
        # No new video frame available
        return None

    if res == -1:
        # Video size has changed, try again but fetch new size first
        del channel_size[channel]
        return read_video(channel)

    # Other errors happened
    return None


# No video will be played from this channel.
NO_VIDEO = 0

# The video will be played while avoiding framedrops.
NODROP_VIDEO = 1

# The video will be played, allowing framedrops.
DROP_VIDEO = 2


@proxy_with_channel
def set_video(channel, video, loop=False):
    """
    Sets a flag that determines if this channel will attempt to decode video.
    """

    if video != renpysound.NO_VIDEO and not video_supported():
        import sys
        print('Warning: video playback is not supported on this browser', file=sys.stderr)

    call("set_video", channel, video, loop)

def video_supported():
    # Video only work with OpenGL v2 renderers (should be supported since WebGL v1,
    # but it falls back to OpenGL v1 on some configs)
    return renpy.session["renderer"] in ('gl2', 'gles2')

loaded = False

def load_script():
    """
    Loads the javascript required for webaudio to work.
    """

    global loaded

    if not loaded:
        js = renpy.loader.load("_audio.js").read().decode("utf-8")
        emscripten.run_script(js)

    loaded = True


@proxy_call_both
def init(freq, stereo, samples, status=False, equal_mono=False, linear_fades=False):
    """
    Initializes the audio system with the given parameters. The parameters are
    just informational - the audio system should be able to play all supported
    files.
    """

    load_script()

    return True


@proxy_call_both
def quit(): # @ReservedAssignment
    """
    De-initializes the audio system.
    """


@proxy_call_both
def periodic():
    """
    Called periodically (at 20 Hz).
    """


@proxy_call_both
def advance_time():
    """
    Called to advance time at the start of a frame.
    """


@proxy_call_both
def sample_surfaces(rgb, rgba):
    """
    Called to provide sample surfaces to the display system. The surfaces
    returned by read_video should be in the same format as these.
    """

    return


def can_play_types(types):
    """
    Webaudio-specific. Returns 1 if the audio system can play all the mime
    types in the list, 0 if it cannot.
    """

    load_script()

    return call_int("can_play_types", types)
