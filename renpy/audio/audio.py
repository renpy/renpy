# Copyright 2004-2020 Tom Rothamel <pytom@bishoujo.us>
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

# The latest and greatest Ren'Py audio system.

# Invariants: The periodic callback assumes pcm_ok. If we don't have
# at least pcm_ok, we have no sound whatsoever.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import *
from future.utils import raise_

import renpy.audio # @UnusedImport
import renpy.display # @UnusedImport

import time
import pygame_sdl2 # @UnusedImport
import os
import re
import threading
import sys
import io

# Import the appropriate modules, or set them to None if we cannot.

disable = os.environ.get("RENPY_DISABLE_SOUND", "")

if not disable:
    import renpy.audio.renpysound as renpysound
else:
    renpysound = None

# This is True if we were able to sucessfully enable the pcm audio.
pcm_ok = None

unique = time.time()
serial = 0


def get_serial():
    """
    Gets a globally unique serial number for each music change.
    """

    global serial
    serial += 1
    return (unique, serial)


def load(fn):
    """
    Returns a file-like object for the given filename.
    """

    try:
        rv = renpy.loader.load(fn)
    except renpy.webloader.DownloadNeeded as exception:
        if exception.rtype == 'music':
            renpy.webloader.enqueue(exception.relpath, 'music', None)
        elif exception.rtype == 'voice':
            # prediction failed, too late
            pass
        # temporary 1s placeholder, will retry loading when looping:
        rv = open(os.path.join(renpy.config.commondir, '_dl_silence.ogg'), 'rb')
    return rv


class AudioData(str):
    """
    :doc: audio

    This class wraps a bytes object containing audio data, so it can be
    passed to the audio playback system. The audio data should be contained
    in some format Ren'Py supports. (For examples RIFF WAV format headers,
    not unadorned samples.)

    `data`
        A bytes object containing the audio file data.

    `filename`
        A synthetic filename associated with this data. It can be used to
        suggest the format `data` is in, and is reported as part of
        error messages.

    Once created, this can be used wherever an audio filename is allowed. For
    example::

        define audio.easteregg = AudioData(b'...', 'sample.wav')
        play sound easteregg
    """

    def __new__(cls, data, filename):
        rv = str.__new__(cls, filename)
        rv.data = data
        return rv

    def __init__(self, data, filename):
        pass

    def __reduce__(self):
        return(AudioData, (self.data, str(self)))


class QueueEntry(object):
    """
    A queue entry object.
    """

    def __init__(self, filename, fadein, tight, loop, relative_volume):
        self.filename = filename
        self.fadein = fadein
        self.tight = tight
        self.loop = loop
        self.relative_volume = relative_volume


class MusicContext(renpy.python.RevertableObject):
    """
    This stores information about the music in a game. This object
    participates in rollback, so when the user goes back in time, all
    the values get reverted as well.
    """

    __version__ = 0

    pause = False
    tertiary_volume = 1.0

    def __init__(self):

        super(MusicContext, self).__init__()

        # The time this channel was last ordered panned.
        self.pan_time = None

        # The pan this channel was ordered to.
        self.pan = 0

        # The time the secondary volume was last ordered changed.
        self.secondary_volume_time = None

        # The secondary volume.
        self.secondary_volume = 1.0

        # The tertiary volume.
        self.tertiary_volume = 1.0

        # The time the channel was ordered last changed.
        self.last_changed = 0

        # Was the last change tight?
        self.last_tight = False

        # What were the filenames we were ordered to loop last?
        self.last_filenames = [ ]

        # Should we force stop this channel?
        self.force_stop = False

        # Should we pause this channel?
        self.pause = False

    def copy(self):
        """
        Returns a shallow copy of this context.
        """

        rv = MusicContext()
        rv.__dict__.update(self.__dict__)

        return rv


# The next channel number to be assigned.
next_channel_number = 0

# the lock that mediates between the periodic and main threads.
lock = threading.RLock()


class Channel(object):
    """
    This stores information about the currently-playing music.
    """

    def __init__(self, name, default_loop, stop_on_mute, tight, file_prefix, file_suffix, buffer_queue, movie, framedrop):

        # The name assigned to this channel. This is used to look up
        # information about the channel in the MusicContext object.
        self.name = name

        # The number this channel has been assigned, or None if we've yet
        # to assign a number to the channel. We only assign a channel
        # number when there's an operation on the channel other than
        # setting the mixer.
        self._number = None

        # The name of the mixer this channel uses. Set below, as there's
        # no good default.
        self.mixer = None

        # The volume imparted to this channel, as a fraction of the
        # mixer volume.
        self.chan_volume = 1.0

        # The actual volume we imparted onto this channel.
        self.actual_volume = 1.0

        # The QueueEntries queued for playback on this channel.
        self.queue = [ ]

        # If true, we loop the music. This entails adding everything in this
        # variable to the end of the queue.
        self.loop = [ ]

        # Are we playing anything at all?
        self.playing = False

        # If True, we'll wait for this channel to stop before
        # loading in more music from the queue. (This is necessary to
        # do a synchro-start.)
        self.wait_stop = False

        # If True, then this channel will participate in a synchro-start
        # once all channels are ready.
        self.synchro_start = False

        # The time the music in this channel was last changed.
        self.last_changed = 0

        # The callback that is called if the queue becomes empty.
        self.callback = None

        # The time this channel was last panned.
        self.pan_time = None

        # The time the secondary volume of this channel was last set.
        self.secondary_volume_time = None

        # Should we stop playing on mute?
        self.stop_on_mute = stop_on_mute

        # Is this channel tight?
        self.tight = tight

        # The number of items in the queue that should be kept
        # on queue clear.
        self.keep_queue = 0

        # A prefix and suffix that are used to create the full filenames.
        self.file_prefix = file_prefix
        self.file_suffix = file_suffix

        # Should we buffer upcoming music/video in the queue?
        self.buffer_queue = buffer_queue

        # Are we paused?
        self.paused = None

        if default_loop is None:
            # By default, should we loop the music?
            self.default_loop = True
            # Was this set explicitly?
            self.default_loop_set = False

        else:
            self.default_loop = default_loop
            self.default_loop_set = True

        # Is this a movie channel?

        if movie:
            if framedrop:
                self.movie = renpy.audio.renpysound.DROP_VIDEO
            else:
                self.movie = renpy.audio.renpysound.NODROP_VIDEO
        else:
            self.movie = renpy.audio.renpysound.NO_VIDEO

    def get_number(self):
        """
        Returns the number of this channel, allocating a number if that
        proves necessary.
        """
        global next_channel_number

        rv = self._number
        if rv is None:
            rv = self._number = next_channel_number
            next_channel_number += 1

        return rv

    number = property(get_number)

    def get_context(self):
        """
        Returns the MusicContext corresponding to this channel, taken from
        the context object. Allocates a MusicContext if none exists.
        """

        mcd = renpy.game.context().music

        rv = mcd.get(self.name)
        if rv is None:
            rv = mcd[self.name] = MusicContext()

        return rv

    context = property(get_context)

    def copy_context(self):
        """
        Copies the MusicContext associated with this channel, updates the
        ExecutionContext to point to the copy, and returns the copy.
        """

        mcd = renpy.game.context().music

        ctx = self.get_context().copy()
        mcd[self.name] = ctx
        return ctx

    def split_filename(self, filename, looped):
        """
        Splits a filename into a filename, start time, and end time.
        """

        def exception(msg):
            return Exception("Parsing audio spec {!r}: {}.".format(filename, msg))

        def expect_float():
            if not spec:
                raise exception("expected float at end.")

            v = spec.pop(0)

            try:
                return float(v)
            except:
                raise exception("expected float, got {!r}.".format(v))

        m = re.match(r'<(.*)>(.*)', filename)
        if not m:
            return filename, 0, -1

        spec = m.group(1)
        fn = m.group(2)

        spec = spec.split()

        start = 0
        loop = None
        end = -1

        while spec:
            clause = spec.pop(0)

            if clause == "from":
                start = expect_float()
            elif clause == "to":
                end = expect_float()
            elif clause == "loop":
                loop = expect_float()
            elif clause == "silence":
                end = expect_float()
                fn = "_silence.ogg"

            else:
                raise exception("expected keyword, got {!r}.".format(clause))

        if (loop is not None) and looped:
            start = loop

        return fn, start, end

    def periodic(self):
        """
        This is the periodic call that causes this channel to load new stuff
        into its queues, if necessary.
        """

        # Update the channel volume.

        mixer_volume = renpy.game.preferences.volumes.get(self.mixer, 1.0)

        if renpy.game.preferences.self_voicing:
            if self.mixer not in renpy.config.voice_mixers:
                mixer_volume = mixer_volume * renpy.game.preferences.self_voicing_volume_drop

        vol = self.chan_volume * mixer_volume

        if vol != self.actual_volume:
            renpysound.set_volume(self.number, vol)
            self.actual_volume = vol

        # This should be set from something that checks to see if our
        # mixer is muted.
        force_stop = self.context.force_stop or (renpy.game.preferences.mute.get(self.mixer, False) and self.stop_on_mute)

        if self.playing and force_stop:
            renpysound.stop(self.number)
            self.playing = False

        if force_stop:
            self.wait_stop = False

            if self.loop:
                self.queue = self.queue[-len(self.loop):]
            else:
                self.queue = [ ]
            return

        topq = None

        # This has been modified so we only queue a single sound file
        # per call, to prevent memory leaks with really short sound
        # files. So this loop will only execute once, in practice.
        while True:

            depth = renpysound.queue_depth(self.number)

            if depth == 0:
                self.wait_stop = False
                self.playing = False

            # Need to check this, so we don't do pointless work.
            if not self.queue:
                break

            # If the pcm_queue is full, then we can't queue
            # anything, regardless of if it is midi or pcm.
            if depth >= 2:
                break

            # If we can't buffer things, and we're playing something
            # give up here.
            if not self.buffer_queue and depth >= 1:
                break

            # We can't queue anything if the depth is > 0 and we're
            # waiting for a synchro_start.
            if self.synchro_start and depth:
                break

            # If the queue is full, return.
            if renpysound.queue_depth(self.number) >= 2:
                break

            # Otherwise, we might be able to enqueue something.
            topq = self.queue.pop(0)

            # Blacklist of old file formats we used to support, but we now
            # ignore.
            lfn = topq.filename.lower() + self.file_suffix.lower()
            for i in (".mod", ".xm", ".mid", ".midi"):
                if lfn.endswith(i):
                    topq = None

            if not topq:
                continue

            try:
                filename, start, end = self.split_filename(topq.filename, topq.loop)

                self.set_tertiary_volume(topq.relative_volume)

                if (end >= 0) and ((end - start) <= 0) and self.queue:
                    continue

                if isinstance(topq.filename, AudioData):
                    topf = io.BytesIO(topq.filename.data)
                else:
                    topf = load(self.file_prefix + filename + self.file_suffix)

                renpysound.set_video(self.number, self.movie)

                if depth == 0:
                    renpysound.play(self.number, topf, topq.filename, paused=self.synchro_start, fadein=topq.fadein, tight=topq.tight, start=start, end=end)
                else:
                    renpysound.queue(self.number, topf, topq.filename, fadein=topq.fadein, tight=topq.tight, start=start, end=end)

                self.playing = True

            except:

                # If playing failed, remove topq.filename from self.loop
                # so we don't keep trying.
                while topq.filename in self.loop:
                    self.loop.remove(topq.filename)

                if renpy.config.debug_sound and not renpy.game.after_rollback:
                    raise
                else:
                    return

            break

        # Empty queue?
        if not self.queue:
            # Re-loop:
            if self.loop:
                for i in self.loop:
                    if topq is not None:
                        newq = QueueEntry(i, 0, topq.tight, True, topq.relative_volume)
                    else:
                        newq = QueueEntry(i, 0, False, True, 1.0)

                    self.queue.append(newq)
            # Try callback:
            elif self.callback:
                self.callback() # E1102

        want_pause = self.context.pause or global_pause

        if self.paused != want_pause:

            if want_pause:
                self.pause()
            else:
                self.unpause()

            self.paused = want_pause

    def dequeue(self, even_tight=False):
        """
        Clears the queued music.

        If the first item in the queue has not been started, then it is
        left in the queue unless all is given.
        """

        with lock:

            self.queue = self.queue[:self.keep_queue]
            self.loop = [ ]

            if not pcm_ok:
                return

            if self.keep_queue == 0:
                renpysound.dequeue(self.number, even_tight)
                self.wait_stop = False
                self.synchro_start = False

    def interact(self):
        """
        Called (mostly) once per interaction.
        """

        self.keep_queue = 0

        if pcm_ok:

            if self.pan_time != self.context.pan_time:
                self.pan_time = self.context.pan_time
                renpysound.set_pan(self.number,
                                   self.context.pan,
                                   0)

            if self.secondary_volume_time != self.context.secondary_volume_time:
                self.secondary_volume_time = self.context.secondary_volume_time
                result_volume = self.context.secondary_volume * self.context.tertiary_volume
                renpysound.set_secondary_volume(self.number,
                                                result_volume,
                                                0)

        if not self.queue and self.callback:
            self.callback() # E1102

    def fadeout(self, secs):
        """
        Causes the playing music to be faded out for the given number
        of seconds. Also clears any queued music.
        """

        with lock:

            self.keep_queue = 0
            self.dequeue()

            if not pcm_ok:
                return

            if secs == 0:
                renpysound.stop(self.number)
            else:
                renpysound.fadeout(self.number, secs)

    def reload(self):
        """
        Causes this channel to be stopped in a way that looped audio will be
        reloaded and restarted.
        """

        with lock:
            renpysound.dequeue(self.number, True)
            renpysound.stop(self.number)

    def enqueue(self, filenames, loop=True, synchro_start=False, fadein=0, tight=None, loop_only=False, relative_volume=1.0):

        with lock:

            for filename in filenames:
                filename, _, _ = self.split_filename(filename, False)
                renpy.game.persistent._seen_audio[filename] = True # @UndefinedVariable

            if not loop_only:

                if tight is None:
                    tight = self.tight

                self.keep_queue += 1

                for filename in filenames:
                    qe = QueueEntry(filename, int(fadein * 1000), tight, False, relative_volume)
                    self.queue.append(qe)

                    # Only fade the first thing in.
                    fadein = 0

                self.wait_stop = synchro_start
                self.synchro_start = synchro_start

            if loop:
                self.loop = list(filenames)
            else:
                self.loop = [ ]

    def get_playing(self):

        if not pcm_ok:
            return None

        rv = renpysound.playing_name(self.number)

        with lock:

            rv = renpysound.playing_name(self.number)

            if rv is None and self.queue:
                rv = self.queue[0].filename

            if rv is None and self.loop:
                rv = self.loop[0]

        return rv

    def set_volume(self, volume):
        self.chan_volume = volume

    def get_pos(self):

        if not pcm_ok:
            return -1

        return renpysound.get_pos(self.number)

    def get_duration(self):

        if not pcm_ok:
            return 0.0

        return renpysound.get_duration(self.number)

    def set_pan(self, pan, delay):

        with lock:

            now = get_serial()
            self.context.pan_time = now
            self.context.pan = pan

            if pcm_ok:
                self.pan_time = self.context.pan_time
                renpysound.set_pan(self.number, self.context.pan, delay)

    def set_secondary_volume(self, volume, delay):

        with lock:

            now = get_serial()
            self.context.secondary_volume_time = now
            self.context.secondary_volume = volume

            if pcm_ok:
                self.secondary_volume_time = self.context.secondary_volume_time
                result_volume = self.context.secondary_volume * self.context.tertiary_volume
                renpysound.set_secondary_volume(self.number, result_volume, delay)

    def set_tertiary_volume(self, volume):
        self.context.tertiary_volume = volume
        self.set_secondary_volume(self.context.secondary_volume, 0)

    def pause(self):
        with lock:
            renpysound.pause(self.number)

    def unpause(self):
        with lock:
            renpysound.unpause(self.number)

    def read_video(self):
        if pcm_ok:
            return renpysound.read_video(self.number)

        return None

    def video_ready(self):

        if not pcm_ok:
            return 1

        return renpysound.video_ready(self.number)

# Use unconditional imports so these files get compiled during the build
# process.


try:
    from renpy.audio.androidhw import AndroidVideoChannel
except:
    pass

try:
    from renpy.audio.ioshw import IOSVideoChannel
except:
    pass

# A list of channels we know about.
all_channels = [ ]

# A map from channel name to Channel object.
channels = { }


def register_channel(name, mixer=None, loop=None, stop_on_mute=True, tight=False, file_prefix="", file_suffix="", buffer_queue=True, movie=False, framedrop=True):
    """
    :doc: audio

    This registers a new audio channel named `name`. Audio can then be
    played on the channel by supplying the channel name to the play or
    queue statements.

    `mixer`
        The name of the mixer the channel uses. By default, Ren'Py
        knows about the "music", "sfx", and "voice" mixers. Using
        other names is possible, but may require changing the
        preferences screens.

    `loop`
        If true, sounds on this channel loop by default.

    `stop_on_mute`
        If true, music on the channel is stopped when the channel is muted.

    `tight`
        If true, sounds will loop even when fadeout is occurring. This should
        be set to True for a sound effects or seamless music channel, and False
        if the music fades out on its own.

    `file_prefix`
        A prefix that is prepended to the filenames of the sound files being
        played on this channel.

    `file_suffix`
        A suffix that is appended to the filenames of the sound files being
        played on this channel.

    `buffer_queue`
        Should we buffer the first second or so of a queued file? This should
        be True for audio, and False for movie playback.

    `movie`
        If true, this channel will be set up to play back videos.

    `framedrop`
        This controls what a video does when lagging. If true, frames will
        be dropped to keep up with realtime and the soundtrack. If false,
        Ren'Py will display frames late rather than dropping them.
    """

    if name == "movie":
        movie = True

    if not renpy.game.context().init_phase and (" " not in name):
        raise Exception("Can't register channel outside of init phase.")

    if renpy.android and renpy.config.hw_video and name == "movie":
        c = AndroidVideoChannel(name, default_loop=loop, file_prefix=file_prefix, file_suffix=file_suffix)
    elif renpy.ios and renpy.config.hw_video and name == "movie":
        c = IOSVideoChannel(name, default_loop=loop, file_prefix=file_prefix, file_suffix=file_suffix)
    else:
        c = Channel(name, loop, stop_on_mute, tight, file_prefix, file_suffix, buffer_queue, movie=movie, framedrop=framedrop)

    c.mixer = mixer

    all_channels.append(c)
    channels[name] = c


def alias_channel(name, newname):
    if not renpy.game.context().init_phase:
        raise Exception("Can't alias channel outside of init phase.")

    c = get_channel(name)
    channels[newname] = c


def get_channel(name):

    rv = channels.get(name, None)

    if rv is None:

        # Do we want to auto-define a new channel?
        if name in renpy.config.auto_channels:

            i = 0

            while True:
                c = get_channel("{} {}".format(name, i))

                if not c.get_playing():
                    return c

                # Limit to one channel while skipping, to prevent sounds from
                # piling up.
                if renpy.config.skipping:
                    return c

                i += 1

        # One of the channels that was just defined.
        elif " " in name:

            base = name.split()[0]
            mixer, file_prefix, file_suffix = renpy.config.auto_channels[base]

            register_channel(
                name,
                loop=False,
                mixer=mixer,
                file_prefix=file_prefix,
                file_suffix=file_suffix,
                )

            return channels[name]

        else:
            raise Exception("Audio channel %r is unknown." % name)

    return rv


def set_force_stop(name, value):
    get_channel(name).context.force_stop = value


# The thread that call periodic.
periodic_thread = None

# True if we need it to quit.
periodic_thread_quit = True


def init():
    global periodic_thread
    global periodic_thread_quit

    global pcm_ok
    global mix_ok

    if not renpy.config.sound:
        pcm_ok = False
        mix_ok = False
        return

    if pcm_ok is None and renpysound:
        bufsize = 2048
        if renpy.emscripten:
            # Large buffer (and latency) as compromise to avoid sound jittering
            bufsize = 8192 # works for me
            # bufsize = 16384  # jitter/silence right after starting a sound

        if 'RENPY_SOUND_BUFSIZE' in os.environ:
            bufsize = int(os.environ['RENPY_SOUND_BUFSIZE'])

        try:
            renpysound.init(renpy.config.sound_sample_rate, 2, bufsize, False, renpy.config.equal_mono)
            pcm_ok = True
        except:
            if renpy.config.debug_sound:
                raise
            pcm_ok = False

    # Find all of the mixers in the game.
    mixers = [ ]

    for c in all_channels:
        if c.mixer not in mixers:
            mixers.append(c.mixer)

    default_volume = 1.0

    for m in mixers:
        renpy.game.preferences.volumes.setdefault(m, default_volume)
        renpy.game.preferences.mute.setdefault(m, False)

    with periodic_condition:

        periodic_thread_quit = False

        periodic_thread = threading.Thread(target=periodic_thread_main)
        periodic_thread.daemon = True
        periodic_thread.start()


def quit(): # @ReservedAssignment

    global periodic_thread
    global periodic_thread_quit

    global pcm_ok
    global mix_ok

    if periodic_thread is not None:
        with periodic_condition:

            periodic_thread_quit = True
            periodic_condition.notify()

        periodic_thread.join()

    if not pcm_ok:
        return

    for c in all_channels:
        c.dequeue()
        c.fadeout(0)

        c.queue = [ ]
        c.loop = [ ]
        c.playing = False
        c.playing_midi = False
        c.wait_stop = False
        c.synchro_start = False

    renpysound.quit()

    pcm_ok = None
    mix_ok = None


# The last-set pcm volume.
pcm_volume = None

old_emphasized = False


def periodic_pass():
    """
    The periodic sound callback. This is called at around 20hz, and is
    responsible for adjusting the volume of the playing music if
    necessary, and also for calling the periodic functions of midi and
    the various channels, which then may play music.
    """

    global pcm_volume
    global old_emphasized

    if not pcm_ok:
        return False

    try:

        # A list of emphasized channels.
        emphasize_channels = [ ]
        emphasized = False

        for i in renpy.config.emphasize_audio_channels:
            c = get_channel(i)
            emphasize_channels.append(c)

            if c.get_playing():
                emphasized = True

        if not renpy.game.preferences.emphasize_audio:
            emphasized = False

        if emphasized and not old_emphasized:
            vol = renpy.config.emphasize_audio_volume
        elif not emphasized and old_emphasized:
            vol = 1.0
        else:
            vol = None

        old_emphasized = emphasized

        if vol is not None:
            for c in all_channels:
                if c in emphasize_channels:
                    continue

                c.set_secondary_volume(vol, renpy.config.emphasize_audio_time)

        for c in all_channels:
            c.periodic()

        renpysound.periodic()

        # Perform a synchro-start if necessary.
        need_ss = False

        for c in all_channels:

            if c.synchro_start and c.wait_stop:
                need_ss = False
                break

            if c.synchro_start and not c.wait_stop:
                need_ss = True

        if need_ss:
            renpysound.unpause_all()

            for c in all_channels:
                c.synchro_start = False

    except:
        if renpy.config.debug_sound:
            raise


# The exception that's been thrown by the periodic thread.
periodic_exc = None

# Should we run the periodic thread now?
run_periodic = False

# The condition the perodic thread runs on.
periodic_condition = threading.Condition()


def periodic_thread_main():

    global periodic_exc
    global run_periodic

    while True:
        with periodic_condition:
            if not run_periodic:
                periodic_condition.wait(.05)

            if periodic_thread_quit:
                return

            if not run_periodic:
                continue

            run_periodic = False

        with lock:

            try:
                periodic_pass()
            except Exception:
                periodic_exc = sys.exc_info()


def periodic():
    global periodic_exc
    global run_periodic

    if not renpy.config.audio_periodic_thread:
        periodic_pass()
        return

    with periodic_condition:

        for c in all_channels:
            c.get_context()

        if periodic_exc is not None:
            exc = periodic_exc
            periodic_exc = None

            raise_(exc[0], exc[1], exc[2])

        run_periodic = True
        periodic_condition.notify()


def interact():
    """
    Called at least once per interaction.
    """

    if not pcm_ok:
        return

    with lock:

        try:
            for c in all_channels:

                c.interact()

                # if _music_volumes.get(i, 1.0) != c.chan_volume:
                #    c.set_volume(_music_volumes.get(i, 1.0))

                ctx = c.context

                # If we're in the same music change, then do nothing with the
                # music.
                if c.last_changed == ctx.last_changed:
                    continue

                filenames = ctx.last_filenames
                tight = ctx.last_tight

                if c.loop:
                    if not filenames or c.get_playing() not in filenames:
                        c.fadeout(renpy.config.fade_music)

                if filenames:
                    c.enqueue(filenames, loop=True, synchro_start=True, tight=tight)

                c.last_changed = ctx.last_changed

        except:
            if renpy.config.debug_sound:
                raise

    periodic()


def rollback():
    """
    On rollback, we want to stop all the channels with non-empty sounds.
    """

    with lock:

        for c in all_channels:
            if not c.loop:
                c.fadeout(0)


def autoreload(_fn):
    """
    After a sound file has been changed, stop all sound (and let Ren'Py restart
    the channels, as needed.)
    """

    for c in all_channels:
        c.reload()

    renpy.exports.restart_interaction()


global_pause = False


def pause_all():
    """
    Pause all playback channels.
    """

    global global_pause
    global_pause = True

    periodic()


def unpause_all():
    """
    Unpause all playback channels.
    """

    global global_pause
    global_pause = False

    periodic()


def sample_surfaces(rgb, rgba):
    if not renpysound:
        return

    renpysound.sample_surfaces(rgb, rgba)


def advance_time():
    if not renpysound:
        return

    renpysound.advance_time()
