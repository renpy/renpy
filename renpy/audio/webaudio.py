# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
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


def check_error():
    """
    This is called by Ren'Py to check for an error. This function should raise
    a meaningful exception if an error has occurred in a background thread,
    or do nothing if an error has not occured. (It should clear any error that
    it raises.)
    """


def play(channel, file, name, paused=False, fadein=0, tight=False, start=0, end=0):
    """
    Plays `file` on `channel`. This clears the playing and queued samples and
    replaces them with this file.

    `name`
        A python object giving a readable name for the file.

    `paused`
        If True, playback is paused rather than started.

    `fadein`
        The time it should take the fade the music in.

    `tight`
        If true, the file is played in tight mode. This means that fadeouts
        can span between this file and the file queued after it.

    `start`
        A time in the file to start playing.

    `end`
        A time in the file to end playing.    `
    """


def queue(channel, file, name, fadein=0, tight=False, start=0, end=0):
    """
    Queues `file` on `channel` to play when the current file ends. If no file is
    playing, plays it.

    The other arguments are as for play.
    """


def stop(channel):
    """
    Immediately stops `channel`, and unqueues any queued audio file.
    """


def dequeue(channel, even_tight=False):
    """
    Dequeues the queued sound file.

    `even_tight`
        If true, a queued sound file that is tight is not dequeued. If false,
        a file marked as tight is dequeued.
    """


def queue_depth(channel):
    """
    Returns the queue depth of the channel. 0 if no file is playing, 1 if
    a files is playing but there is no queued file, and 2 if a file is playing
    and one is queued.
    """


def playing_name(channel):
    """
    Returns the `name`  argument of the playing sound. This was passed into
    `play` or `queue`.
    """


def pause(channel):
    """
    Pauses `channel`.
    """


def unpause(channel):
    """
    Unpauses `channel`.
    """


def unpause_all():
    """
    Unpauses all channels that are paused.
    """


def fadeout(channel, delay):
    """
    Fades out `channel` over `delay` seconds.
    """


def busy(channel):
    """
    Returns true if `channel` is currently playing something, and false
    otherwise
    """


def get_pos(channel):
    """
    Returns the position of the audio file playing in `channel`. Returns None
    if not file is is playing or it is not known.
    """


def get_duration(channel):
    """
    Reutrns the duration of the audio file playing in `channel`, or None if no
    file is playing or it is not known.
    """


def set_volume(channel, volume):
    """
    Sets the primary volume for `channel` to `volume`, a number between
    0 and 1. This volume control is perceptual, taking into account the
    logarithmic nature of human hearing.
    """


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


def set_secondary_volume(channel, volume, delay):
    """
    Sets the secondary volume for channel. This is linear, and is multiplied
    with the primary volume and scale factors derived from pan to find the
    actual multiplier used on the samples.

    `delay`
        The time it takes for the change in volume to happen.
    """


def get_volume(channel):
    """
    Gets the primary volume associated with `channel`.
    """


def video_ready(channel):
    """
    Returns true if the video playing on `channel` has a frame ready for
    presentation.
    """

    return False


def read_video(channel):
    """
    Returns the frame of video playing on `channel`. This should be returned
    as an SDL surface with 2px of padding on all sides.
    """

    return None


# No video will be played from this channel.
NO_VIDEO = 0

# The video will be played while avoiding framedrops.
NODROP_VIDEO = 1

# The video will be played, allowing framedrops.
DROP_VIDEO = 2


def set_video(channel, video):
    """
    Sets a flag that determines if this channel will attempt to decode video.
    """

    return


def init(freq, stereo, samples, status=False, equal_mono=False):
    """
    Initializes the audio system with the given parameters. The parameter are
    just informational - the audio system should be able to play all supported
    files.

    `freq`
        The sample frequency to play back at.

    `stereo`
        Should we play in stereo (generally true).

    `samples`
        The length of the sample buffer.

    `status`
        If true, the sound system will print errors out to the console.
    `
    """

    return


def quit(): # @ReservedAssignment
    """
    De-initializes the audio system.
    """


def periodic():
    """
    Called periodically (at 20 Hz).
    """


def advance_time():
    """
    Called to advance time at the start of a frame.
    """


def sample_surfaces(rgb, rgba):
    """
    Called to provide sample surfaces to the display system. The surfaces
    returned by read_video should be in the same format as these.
    """

    return

