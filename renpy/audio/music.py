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

# The public API for music in games.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *



import renpy

from renpy.audio.audio import get_channel, get_serial

# Part of the public api:
from renpy.audio.audio import register_channel, alias_channel


def play(filenames, channel="music", loop=None, fadeout=None, synchro_start=False, fadein=0, tight=None, if_changed=False, relative_volume=1.0):
    """
    :doc: audio

    This stops the music currently playing on the numbered channel, dequeues
    any queued music, and begins playing the specified file or files.

    `filenames`
        This may be a single file, or a list of files to be played.

    `channel`
        The channel to play the sound on.

    `loop`
        If this is True, the tracks will loop while they are the last thing
        in the queue.

    `fadeout`
        If not None, this is a time in seconds to fade for. Otherwise the
        fadeout time is taken from config.fadeout_audio. This is ignored if
        the channel is paused when the music is played.

    `synchro_start`
        Ren'Py will ensure that all channels of with synchro_start set to true
        will start playing at exactly the same time. Synchro_start should be
        true when playing two audio files that are meant to be synchronized
        with each other.

    `fadein`
        This is the number of seconds to fade the music in for, on the
        first loop only.

    `tight`
        If this is True, then fadeouts will span into the next-queued sound. If
        None, this is true when loop is True, and false otherwise.

    `if_changed`
        If this is True, and the music file is currently playing,
        then it will not be stopped/faded out and faded back in again, but
        instead will be kept playing. (This will always queue up an additional
        loop of the music.)

    `relative_volume`
        This is the volume relative to the current channel volume.
        The specified file will be played at that relative volume. If not
        specified, it will always default to 1.0, which plays the file at the
        original volume as determined by the mixer, channel and secondary volume.

    This clears the pause flag for `channel`.
    """

    if renpy.game.context().init_phase:
        raise Exception("Can't play music during init phase.")

    if filenames is None:
        return

    if isinstance(filenames, basestring):
        filenames = [ filenames ]

    if get_pause(channel=channel):
        fadeout = 0

    with renpy.audio.audio.lock:

        try:
            c = get_channel(channel)
            ctx = c.copy_context()

            if loop is None:
                loop = c.default_loop

            if (tight is None) and renpy.config.tight_loop_default:
                tight = loop

            loop_is_filenames = (c.loop == filenames)

            if fadeout is None:
                fadeout = renpy.config.fadeout_audio

            if if_changed and c.get_playing() in filenames:
                fadein = 0
                loop_only = loop_is_filenames
                if not loop_is_filenames:
                    c.dequeue()
            else:
                c.dequeue()
                c.fadeout(fadeout)
                loop_only = False

            if renpy.config.skip_sounds and renpy.config.skipping and (not loop):
                enqueue = False
            else:
                enqueue = True

            if enqueue:
                c.enqueue(filenames, loop=loop, synchro_start=synchro_start, fadein=fadein, tight=tight, loop_only=loop_only, relative_volume=relative_volume)

            t = get_serial()
            ctx.last_changed = t
            c.last_changed = t

            if loop:
                ctx.last_filenames = filenames
                ctx.last_tight = tight
                ctx.last_relative_volume = relative_volume
            else:
                ctx.last_filenames = [ ]
                ctx.last_tight = False
                ctx.last_relative_volume = 1.0

            ctx.pause = False

        except Exception:
            if renpy.config.debug_sound:
                raise


def queue(filenames, channel="music", loop=None, clear_queue=True, fadein=0, tight=None, relative_volume=1.0):
    """
    :doc: audio

    This queues the given filenames on the specified channel.

    `filenames`
        This may be a single file, or a list of files to be played.

    `channel`
        The channel to play the sound on.

    `loop`
        If this is True, the tracks will loop while they are the last thing
        in the queue.

    `clear_queue`
        If True, then the queue is cleared, making these files the files that
        are played when the currently playing file finishes. If it is False,
        then these files are placed at the back of the queue. In either case,
        if no music is playing these files begin playing immediately.

    `fadein`
        This is the number of seconds to fade the music in for, on the
        first loop only.

    `tight`
        If this is True, then fadeouts will span into the next-queued sound. If
        None, this is true when loop is True, and false otherwise.

    `relative_volume`
        This is the volume relative to the current channel volume.
        The specified file will be played at that relative volume. If not
        specified, it will always default to 1.0, which plays the file at the
        original volume as determined by the mixer, channel and secondary volume.

    This clears the pause flag for `channel`.
    """

    if renpy.game.context().init_phase:
        raise Exception("Can't play music during init phase.")

    if filenames is None:
        filenames = [ ]
        loop = False

    if isinstance(filenames, basestring):
        filenames = [ filenames ]

    if renpy.config.skipping == "fast":
        stop(channel)

    set_pause(False, channel=channel)

    with renpy.audio.audio.lock:

        try:

            c = get_channel(channel)
            ctx = c.copy_context()

            if loop is None:
                loop = c.default_loop

            if (tight is None) and renpy.config.tight_loop_default:
                tight = loop

            if clear_queue:
                c.dequeue(True)

            if renpy.config.skip_sounds and renpy.config.skipping and (not loop):
                enqueue = False
            else:
                enqueue = True

            if enqueue:
                c.enqueue(filenames, loop=loop, fadein=fadein, tight=tight, relative_volume=relative_volume)

            t = get_serial()
            ctx.last_changed = t
            c.last_changed = t

            if loop:
                ctx.last_filenames = filenames
                ctx.last_tight = tight
                ctx.last_relative_volume = relative_volume
            else:
                ctx.last_filenames = [ ]
                ctx.last_tight = False
                ctx.last_relative_volume = 1.0

            ctx.pause = False

        except Exception:
            if renpy.config.debug_sound:
                raise


def playable(filename, channel="music"):
    """
    Return true if the given filename is playable on the channel. This
    takes into account the prefix and suffix, and ignores a preceding
    specifier.
    """

    c = get_channel(channel)

    filename, _, _ = c.split_filename(filename, False)

    return renpy.loader.loadable(filename, directory="audio")


def stop(channel="music", fadeout=None):
    """
    :doc: audio

    This stops the music that is currently playing, and dequeues all
    queued music. If fadeout is None, the music is faded out for the
    time given in config.fadeout_audio, otherwise it is faded for fadeout
    seconds.

    This sets the last queued file to None.

    `channel`
        The channel to stop the sound on.

    `fadeout`
        If not None, this is a time in seconds to fade for. Otherwise the
        fadeout time is taken from config.fadeout_audio. This is ignored if
        the channel is paused.


    """

    if renpy.game.context().init_phase:
        return

    if get_pause(channel=channel):
        fadeout = 0.0

    with renpy.audio.audio.lock:

        try:
            c = get_channel(channel)
            ctx = c.copy_context()

            if fadeout is None:
                fadeout = renpy.config.fadeout_audio

            c.fadeout(fadeout)

            t = get_serial()
            ctx.last_changed = t
            c.last_changed = t
            ctx.last_filenames = [ ]
            ctx.last_tight = False

        except Exception:
            if renpy.config.debug_sound:
                raise

    set_pause(False, channel=channel)


def set_music(channel, flag, default=False):
    """
    Determines if channel will loop by default.
    """

    c = get_channel(channel)

    if default and c.default_loop_set:
        return

    c.default_loop = flag
    c.default_loop_set = True


def is_music(channel):
    """
    Returns true if "channel" will loop by default.
    """

    c = get_channel(channel)
    return c.default_loop


def get_delay(time, channel="music"):
    """
    Returns the number of seconds left until the given time in the
    music.
    """

    try:
        c = renpy.audio.audio.get_channel(channel)
        t = c.get_pos()

        if not t or t < 0:
            return None

        if t > time:
            return 0

        return time - t

    except Exception:
        if renpy.config.debug_sound:
            raise

        return None


def get_pos(channel="music"):
    """
    :doc: audio

    Returns the current position of the audio or video file on `channel`, in
    seconds. Returns None if no audio is playing on `channel`.

    As this may return None before a channel starts playing, or if the audio
    channel involved has been muted, callers of this function should
    always handle a None value.
    """

    try:
        c = renpy.audio.audio.get_channel(channel)
        t = c.get_pos()

        if not t or t < 0:
            return None

        return t

    except Exception:
        if renpy.config.debug_sound:
            raise

        return None


def get_duration(channel="music"):
    """
    :doc: audio

    Returns the duration of the audio or video file on `channel`. Returns
    0.0 if no file is playing on `channel`, or the duration is unknown.
    Some formats - notably MP3 - do not include duration information in a
    format Ren'Py can access.
    """

    try:
        c = renpy.audio.audio.get_channel(channel)
        return c.get_duration()

    except Exception:
        if renpy.config.debug_sound:
            raise

        return 0.0


def get_playing(channel="music"):
    """
    :doc: audio

    If the given channel is playing, returns the playing file name.
    Otherwise, returns None.
    """

    try:
        c = renpy.audio.audio.get_channel(channel)
        return c.get_playing()
    except Exception:
        if renpy.config.debug_sound:
            raise

        return None


def is_playing(channel="music"):
    """
    :doc: audio

    Returns True if the channel is currently playing a sound, False if
    it is not, or if the sound system isn't working.
    """

    return (get_playing(channel=channel) is not None)


def get_loop(channel="music"):
    """
    :doc: audio

    Return a list of filenames that are being looped on `channel`, or None
    if no files are being looped. In the case where a loop is queued, but
    is not yet playing, the loop is returned, not the currently playing
    music.
    """

    c = get_channel(channel)
    ctx = c.get_context()

    return ctx.last_filenames or None


def set_volume(volume, delay=0, channel="music"):
    """
    :doc: audio

    Sets the volume of this channel, as a fraction of the volume of the
    mixer controlling the channel.

    `volume`
        This is a number between 0.0 and 1.0, and is interpreted as a fraction
        of the mixer volume for the channel.

    `delay`
        It takes delay seconds to change/fade the volume from the old to
        the new value. This value is persisted into saves, and participates
        in rollback.

    `channel`
        The channel to be set
    """

    try:
        c = renpy.audio.audio.get_channel(channel)
        c.set_secondary_volume(volume, delay)
    except Exception:
        if renpy.config.debug_sound:
            raise


def set_pan(pan, delay, channel="music"):
    """
    :doc: audio

    Sets the pan of this channel.

    `pan`
        A number between -1 and 1 that control the placement of the audio.
        If this is -1, then all audio is sent to the left channel.
        If it's 0, then the two channels are equally balanced. If it's 1,
        then all audio is sent to the right ear.

    `delay`
        The amount of time it takes for the panning to occur.

    `channel`
        The channel the panning takes place on, defaulting to the music channel.
    """

    try:
        c = renpy.audio.audio.get_channel(channel)
        c.set_pan(pan, delay)
    except Exception:
        if renpy.config.debug_sound:
            raise


def set_queue_empty_callback(callback, channel="music"):
    """
    :doc: audio

    This sets a callback that is called when the queue is empty. This
    callback is called when the queue first becomes empty, and at
    least once per interaction while the queue is empty.

    The callback is called with no parameters. It can queue sounds by
    calling renpy.music.queue with the appropriate arguments. Please
    note that the callback may be called while a sound is playing, as
    long as a queue slot is empty.
    """
    try:
        c = renpy.audio.audio.get_channel(channel)
        c.callback = callback
    except Exception:
        if renpy.config.debug_sound:
            raise


def set_pause(value, channel="music"):
    """
    :doc: audio

    Sets the pause flag for `channel` to `value`. If True, the channel
    will pause, otherwise it will play normally.
    """
    try:
        c = renpy.audio.audio.get_channel(channel)
        c.copy_context().pause = value
    except Exception:
        if renpy.config.debug_sound:
            raise


def get_pause(channel="music"):
    """
    :doc: audio

    Returns the pause flag for `channel`.
    """
    try:
        c = renpy.audio.audio.get_channel(channel)
        return c.context.pause
    except Exception:

        return False

def pump():
    """
    :doc: audio

    This 'pumps' the audio system. Normally, the effects of the ``play``,
    ``queue``, and ``stop`` statements and the function equivalents take
    place at the start of the next interaction. In some cases, the effects
    of multiple statements can cancel each other out - for example, a
    play followed by a stop causes the track to never be played.

    If this function is called between the play and stop, the track will
    begin playing before this function returns, which then allows the track
    to be faded out. ::

        play music "mytrack.opus"
        $ renpy.music.pump()
        stop music fadeout 4
    """

    renpy.audio.audio.pump()


def set_mixer(channel, mixer, default=False):
    """
    This sets the name of the mixer associated with a given
    channel. By default, there are two mixers, 'sfx' and
    'music'. 'sfx' is on channels 0 to 3, and 'music'
    on 3 to 7. The voice module calls this function to set channel 2 to voice.
    You can create your own mixer, but will need to add a preference if you
    wish to allow the user to set it.

    This function should only be called in an init block.
    """

    try:
        c = renpy.audio.audio.get_channel(channel)

        if not default or c.mixer is None:
            c.mixer = mixer

    except Exception:
        if renpy.config.debug_sound:
            raise


def get_all_mixers():
    """
    This gets all mixers in use.
    """

    rv = set()

    for i in renpy.audio.audio.all_channels:
        rv.add(i.mixer)

    return list(rv)


def channel_defined(channel):
    """
    Returns True if the channel exists, or False otherwise.
    """

    try:
        renpy.audio.audio.get_channel(channel)
        return True
    except Exception:
        return False

# Music change logic:

# Use the queueing time to determine what should or should not be
# queued

# m_filenames - music filenames from info object
# m_loop - music loop from info object
# c_filenames - music filenames from channel
# c_filenames - music loop from channel

# if m_filenames == c_filenames and m_loop == c_loop:
#     do nothing, the music is right.

# otherwise,
#     dequeue music from the channel.

# if m_filenames != c_playing_filenames:
#     stop the music with fade. The music is wrong, change it.

# if m_loop:
#     queue m_filenames looping
