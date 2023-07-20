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

"""
This file defines the API that Ren'Py uses to communicate with an audio and video
backend, and the default implementation of the API. This API is not intended
to be stable between multiple Ren'Py releases, and so is more intended for use
in ports to different platforms.

There are a few common variables with specific datatypes here.

`channel`
    An integer giving  the number of an audio channel.  These integers are
    allocated densely, but there's no limit to how many channels may be
    present at one time.

`file`
    This is an object representing an open file. This may be a Python file
    object, or a Ren'Py subfile object. All objects past to this have a
    `name` field, giving the name of the file. SubFiles also have `base`
    and length. Base is the offset from the start of the file where the data
    begins, while length is the amount of data in total.

Times and durations are represented as floats giving the number of seconds.

A channel may have up to two files associated with it, the playing file and
the queued file. The queued file begins playing when the current file ends
or is stopped.
"""

# When changing this API, change webaudio.py, too!

from __future__ import print_function

from libc.stdint cimport uintptr_t

from pygame_sdl2 cimport *
import_pygame_sdl2()

cdef extern from "renpysound_core.h":

    void RPS_play(int channel, SDL_RWops *rw, char *ext, char* name, int fadein, int tight, int paused, double start, double end, float volume)
    void RPS_queue(int channel, SDL_RWops *rw, char *ext, char *name, int fadein, int tight, double start, double end, float volume)
    void RPS_stop(int channel)
    void RPS_dequeue(int channel, int even_tight)
    int RPS_queue_depth(int channel)
    object RPS_playing_name(int channel)
    void RPS_fadeout(int channel, int ms)
    void RPS_pause(int channel, int pause)
    void RPS_unpause_all_at_start()
    int RPS_get_pos(int channel)
    double RPS_get_duration(int channel)
    void RPS_set_endevent(int channel, int event)
    void RPS_set_volume(int channel, float volume)
    float RPS_get_volume(int channel)
    void RPS_set_pan(int channel, float pan, float delay)
    void RPS_set_secondary_volume(int channel, float vol2, float delay)

    void RPS_advance_time()
    int RPS_video_ready(int channel)
    object RPS_read_video(int channel)
    void RPS_set_video(int channel, int video)

    void RPS_sample_surfaces(object, object)
    void RPS_init(int freq, int stereo, int samples, int status, int equal_mono, int linear_fades)
    void RPS_quit()

    void RPS_periodic()
    char *RPS_get_error()

    void (*RPS_generate_audio_c_function)(float *stream, int length)

def check_error():
    """
    This is called by Ren'Py to check for an error. This function should raise
    a meaningful exception if an error has occurred in a background thread,
    or do nothing if an error has not occured. (It should clear any error that
    it raises.)
    """

    e = RPS_get_error();
    if len(e):
        raise Exception(unicode(e, "utf-8", "replace"))

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
        A float giving the relative volume of the file.
    """

    cdef SDL_RWops *rw

    rw = RWopsFromPython(file)

    if rw == NULL:
        raise Exception("Could not create RWops.")

    if paused:
        pause = 1
    else:
        pause = 0

    if tight:
        tight = 1
    else:
        tight = 0

    name = name.encode("utf-8")
    RPS_play(channel, rw, name, name, fadein * 1000, tight, pause, start, end, relative_volume)
    check_error()

def queue(channel, file, name, fadein=0, tight=False, start=0, end=0, relative_volume=1.0):
    """
    Queues `file` on `channel` to play when the current file ends. If no file is
    playing, plays it.

    The other arguments are as for play.
    """

    cdef SDL_RWops *rw

    rw = RWopsFromPython(file)

    if rw == NULL:
        raise Exception("Could not create RWops.")

    if tight:
        tight = 1
    else:
        tight = 0

    name = name.encode("utf-8")
    RPS_queue(channel, rw, name, name, fadein * 1000, tight, start, end, relative_volume)
    check_error()

def stop(channel):
    """
    Immediately stops `channel`, and unqueues any queued audio file.
    """

    RPS_stop(channel)
    check_error()

def dequeue(channel, even_tight=False):
    """
    Dequeues the queued sound file.

    `even_tight`
        If true, a queued sound file that is tight is not dequeued. If false,
        a file marked as tight is dequeued.
    """

    RPS_dequeue(channel, even_tight)

def queue_depth(channel):
    """
    Returns the queue depth of the channel. 0 if no file is playing, 1 if
    a files is playing but there is no queued file, and 2 if a file is playing
    and one is queued.
    """

    return RPS_queue_depth(channel)

def playing_name(channel):
    """
    Returns the `name`  argument of the playing sound. This was passed into
    `play` or `queue`.
    """

    rv = RPS_playing_name(channel)

    if rv is not None:
        rv = rv.decode("utf-8")

    return rv

def pause(channel):
    """
    Pauses `channel`.
    """

    RPS_pause(channel, 1)
    check_error()

def unpause(channel):
    """
    Unpauses `channel`.
    """

    RPS_pause(channel, 0)
    check_error()

def unpause_all_at_start():
    """
    Unpauses all channels that are paused at the start.
    """

    RPS_unpause_all_at_start()

def fadeout(channel, delay):
    """
    Fades out `channel` over `delay` seconds.
    """

    RPS_fadeout(channel, int(delay * 1000))
    check_error()

def busy(channel):
    """
    Returns true if `channel` is currently playing something, and false
    otherwise
    """

    return RPS_get_pos(channel) != -1

def get_pos(channel):
    """
    Returns the position of the audio file playing in `channel`, in seconds.
    Returns None if not file is is playing or it is not known.
    """

    return RPS_get_pos(channel) / 1000.0

def get_duration(channel):
    """
    Returns the duration of the audio file playing in `channel`, in seconds, or
    None if no file is playing or it is not known.
    """

    return RPS_get_duration(channel)

def set_volume(channel, volume):
    """
    Sets the primary volume for `channel` to `volume`, a number between
    0 and 1. This volume control is linear.
    """

    if volume == 0:
        RPS_set_volume(channel, 0)
    else:
        RPS_set_volume(channel, volume)

    check_error()

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

    RPS_set_pan(channel, pan, delay)
    check_error()

def set_secondary_volume(channel, volume, delay):
    """
    Sets the secondary volume for channel. This is linear, and is multiplied
    with the primary volume and scale factors derived from pan to find the
    actual multiplier used on the samples.

    `delay`
        The time it takes for the change in volume to happen.
    """

    RPS_set_secondary_volume(channel, volume, delay)
    check_error()

def get_volume(channel):
    """
    Gets the primary volume associated with `channel`.
    """

    return RPS_get_volume(channel)

def video_ready(channel):
    """
    Returns true if the video playing on `channel` has a frame ready for
    presentation.
    """

    return RPS_video_ready(channel)

def read_video(channel):
    """
    Returns the frame of video playing on `channel`. This should be returned
    as an SDL surface with 2px of padding on all sides.
    """

    rv = RPS_read_video(channel)

    if rv is None:
        return rv

    # Remove padding from the edges of the surface.
    w, h = rv.get_size()

    # This has to be set to the same number it is in ffmedia.c
    FRAME_PADDING = 4
    return rv.subsurface((FRAME_PADDING, FRAME_PADDING, w - FRAME_PADDING * 2, h - FRAME_PADDING * 2))

# No video will be played from this channel.
NO_VIDEO = 0

# The video will be played while avoiding framedrops.
NODROP_VIDEO = 1

# The video will be played, allowing framedrops.
DROP_VIDEO = 2

def set_video(channel, video, loop=False):
    """
    Sets a flag that determines if this channel will attempt to decode video.

    `video`
        One of `NO_VIDEO`, `NODROP_VIDEO`, or `DROP_VIDEO`.

    `loop`
        If true, the video file will loop.
    """

    if video == NODROP_VIDEO:
        RPS_set_video(channel, NODROP_VIDEO)
    elif video:
        RPS_set_video(channel, DROP_VIDEO)
    else:
        RPS_set_video(channel, NO_VIDEO)

def init(freq, stereo, samples, status=False, equal_mono=False, linear_fades=False):
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

    `equal_mono`
        If true, the sound system will play mono files at the same volume as
        stereo files.

    `linear_fades`
        If true, the sound system will use linear fades.
    """

    if status:
        status = 1
    else:
        status = 0

    RPS_init(freq, stereo, samples, status, equal_mono, linear_fades)
    check_error()

def quit(): # @ReservedAssignment
    """
    De-initializes the audio system.
    """

    RPS_quit()

def periodic():
    """
    Called periodically (at 20 Hz).
    """

    RPS_periodic()

def advance_time():
    """
    Called to advance time at the start of a frame.
    """


    RPS_advance_time()

def set_generate_audio_c_function(fn):
    """
    This can be use to set a C function that totally replaces the Ren'Py
    audio system.

    The function is expected to have the signature void (*)(short *buf, int samples,
    and fill buf with samples samples of audio, where each sample consists of two
    shorts.
    """

    global RPS_generate_audio_c_function

    if not isinstance(fn, int):
        import ctypes
        fn = ctypes.cast(fn, ctypes.c_void_p).value

    RPS_generate_audio_c_function = <void (*)(float *, int)> <uintptr_t> fn

# Store the sample surfaces so they stay alive.
rgb_surface = None
rgba_surface = None

def sample_surfaces(rgb, rgba):
    """
    Called to provide sample surfaces to the display system. The surfaces
    returned by read_video should be in the same format as these.
    """

    global rgb_surface
    global rgba_surface

    rgb_surface = rgb
    rgba_surface = rgb

    RPS_sample_surfaces(rgb, rgba)

# Is this the webaudio module?
is_webaudio = False

# When changing this API, change webaudio.py, too!
