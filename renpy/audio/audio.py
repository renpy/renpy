# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
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

import renpy.audio
import renpy.display

import time
import pygame
import os
import atexit

# Import the appropriate modules, or set them to None if we cannot.

disable = os.environ.get("RENPY_DISABLE_SOUND", "")

pss = None

if 'pss' not in disable:
    try:
        import pysdlsound as pss
        pss.check_version(4)
        atexit.register(pss.quit)
    except:
        pass

    if pss is None:
        try:
            import android.sound as pss #@UnresolvedImport @Reimport
            print "Imported android.sound."
        except:
            pass


# Save the mixer, and restore it at exit.

old_wave = None
old_midi = None

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

    rv = renpy.loader.load(fn)
    return rv


class QueueEntry(object):
    """
    A queue entry object.
    """

    def __init__(self, filename, fadein, tight):
        self.filename = filename
        self.fadein = fadein
        self.tight = tight


class MusicContext(renpy.python.RevertableObject):
    """
    This stores information about the music in a game. This object
    participates in rollback, so when the user goes back in time, all
    the values get reverted as well.
    """

    __version__ = 0

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

        # The time the channel was ordered last changed.
        self.last_changed = 0

        # Was the last change tight?
        self.last_tight = False

        # What were the filenames we were ordered to loop last?
        self.last_filenames = [ ]

        # Should we force stop this channel?
        self.force_stop = False

    def copy(self):
        """
        Returns a shallow copy of this context.
        """

        rv = MusicContext()
        rv.__dict__.update(self.__dict__)

        return rv

# The next channel number to be assigned.
next_channel_number = 0

class Channel(object):
    """
    This stores information about the currently-playing music.
    """

    def __init__(self, name, default_loop, stop_on_mute, tight, file_prefix, file_suffix, buffer_queue):

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

        if default_loop is None:
            # By default, should we loop the music?
            self.default_loop = True
            # Was this set explicitly?
            self.default_loop_set = False

        else:
            self.default_loop = default_loop
            self.default_loop_set = True


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


    def periodic(self):
        """
        This is the periodic call that causes this channel to load new stuff
        into its queues, if necessary.
        """

        # Update the channel volume.
        vol = self.chan_volume * renpy.game.preferences.volumes[self.mixer]

        if vol != self.actual_volume:
            pss.set_volume(self.number, vol)
            self.actual_volume = vol


        # This should be set from something that checks to see if our
        # mixer is muted.
        force_stop = self.context.force_stop or (renpy.game.preferences.mute[self.mixer] and self.stop_on_mute)

        if self.playing and force_stop:
            pss.stop(self.number)
            self.playing = False
            self.wait_stop = False

        if force_stop:
            if self.loop:
                self.queue = self.queue[-len(self.loop):]
            else:
                self.queue = [ ]
            return

        # Should we do the callback?
        do_callback = False

        # This has been modified so we only queue a single sound file
        # per call, to prevent memory leaks with really short sound
        # files. So this loop will only execute once, in practice.
        while True:

            depth = pss.queue_depth(self.number)

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
            if pss.queue_depth(self.number) >= 2:
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
                topf = load(self.file_prefix + topq.filename + self.file_suffix)

                if depth == 0:
                    pss.play(self.number, topf, topq.filename, paused=self.synchro_start, fadein=topq.fadein, tight=topq.tight)
                else:
                    pss.queue(self.number, topf, topq.filename, fadein=topq.fadein, tight=topq.tight)

                self.playing = True

            except:

                # If playing failed, remove topq.filename from self.loop
                # so we don't keep trying.
                while topq.filename in self.loop:
                    self.loop.remove(topq.filename)

                if renpy.config.debug_sound:
                    raise
                else:
                    return

            break

        if self.loop and not self.queue:
            for i in self.loop:
                newq = QueueEntry(i, 0, topq.tight)
                self.queue.append(newq)
        else:
            do_callback = True

        # Queue empty callback.
        if do_callback and self.callback:
            self.callback() # E1102

    def dequeue(self, even_tight=False):
        """
        Clears the queued music.

        If the first item in the queue has not been started, then it is
        left in the queue unless all is given.
        """

        self.queue = self.queue[:self.keep_queue]
        self.loop = [ ]

        if not pcm_ok:
            return

        if self.keep_queue == 0:
            pss.dequeue(self.number, even_tight)

    def interact(self):
        """
        Called (mostly) once per interaction.
        """

        self.keep_queue = 0

        if pcm_ok:

            if self.pan_time != self.context.pan_time:
                self.pan_time = self.context.pan_time
                pss.set_pan(self.number,
                            self.context.pan,
                            0)


            if self.secondary_volume_time != self.context.secondary_volume_time:
                self.secondary_volume_time = self.context.secondary_volume_time
                pss.set_secondary_volume(self.number,
                                         self.context.secondary_volume,
                                         0)

        if not self.queue and self.callback:
            self.callback() # E1102


    def fadeout(self, secs):
        """
        Causes the playing music to be faded out for the given number
        of seconds. Also clears any queued music.
        """

        self.keep_queue = 0
        self.dequeue()

        if not pcm_ok:
            return

        if secs == 0:
            pss.stop(self.number)
        else:
            pss.fadeout(self.number, int(secs * 1000))

    def enqueue(self, filenames, loop=True, synchro_start=False, fadein=0, tight=None):

        for filename in filenames:
            renpy.game.persistent._seen_audio[filename] = True  # @UndefinedVariable

        if not pcm_ok:
            return

        if tight is None:
            tight = self.tight

        self.keep_queue += 1

        for filename in filenames:
            qe = QueueEntry(filename, int(fadein * 1000), tight)
            self.queue.append(qe)

            # Only fade the first thing in.
            fadein = 0

        if loop:
            self.loop = list(filenames)
        else:
            self.loop = [ ]

        self.wait_stop = synchro_start
        self.synchro_start = synchro_start

    def get_playing(self):

        if not pcm_ok:
            return None

        rv = pss.playing_name(self.number)

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

        return pss.get_pos(self.number)

    def set_pan(self, pan, delay):
        now = get_serial()
        self.context.pan_time = now
        self.context.pan = pan

        if pcm_ok:
            self.pan_time = self.context.pan_time
            pss.set_pan(self.number, self.context.pan, delay)

    def set_secondary_volume(self, volume, delay):
        now = get_serial()
        self.context.secondary_volume_time = now
        self.context.secondary_volume = volume

        if pcm_ok:
            self.secondary_volume_time = self.context.secondary_volume_time
            pss.set_secondary_volume(self.number, self.context.secondary_volume, delay)


################################################################################
# Android VideoPlayer Channel
################################################################################

if renpy.android:

    import jnius  # @UnresolvedImport

    VideoPlayer = jnius.autoclass("org.renpy.android.VideoPlayer")

    class AndroidVideoChannel(object):

        def __init__(self, name, file_prefix="", file_suffix="", default_loop=None):

            # A list of queued filenames.
            self.queue = [ ]

            # The filename that's currently playing.
            self.filename = None

            # The videoplayer that's currently playing.
            self.player = None

            # The name assigned to this channel. This is used to look up
            # information about the channel in the MusicContext object.
            self.name = name

            # The name of the mixer this channel uses. Set below, as there's
            # no good default.
            self.mixer = None

            # The time the music in this channel was last changed.
            self.last_changed = 0

            # The callback that is called if the queue becomes empty.
            self.callback = None

            # Ignored.
            self.synchro_start = False
            self.wait_stop = False
            self.loop = [ ]

            # A prefix and suffix that are used to create the full filenames.
            self.file_prefix = file_prefix
            self.file_suffix = file_suffix

            if default_loop is None:
                # By default, should we loop the music?
                self.default_loop = True
                # Was this set explicitly?
                self.default_loop_set = False

            else:
                self.default_loop = default_loop
                self.default_loop_set = True


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


        def start(self):
            """
            Starts playing the first video in the queue.
            """

            if not self.queue:
                return

            filename = self.queue.pop(0)

            f = renpy.loader.load(filename)

            real_fn = f.name
            base = getattr(f, "base", -1)
            length = getattr(f, "length", -1)

            self.filename = filename
            self.player = VideoPlayer(real_fn, base, length)

        def stop(self):

            if self.player is not None:
                self.player.stop()
                self.player = None

            self.filename = None

        def get_playing(self):

            if self.player is None:
                return None

            if self.player.isPlaying():
                return self.filename

        def periodic(self):

            # This should be set from something that checks to see if our
            # mixer is muted.
            force_stop = self.context.force_stop

            if force_stop:
                self.dequeue()
                self.stop()
                return

            if self.get_playing():
                return

            if self.queue:
                self.start()


        def dequeue(self, even_tight=False):
            """
            Clears the queued music, except for a first item that has
            not been started.
            """

            if self.get_playing():
                self.queue = [ ]
            else:
                self.queue = self.queue[:1]


        def interact(self):
            """
            Called (mostly) once per interaction.
            """

            self.periodic()


        def fadeout(self, secs):
            """
            Causes the playing music to be faded out for the given number
            of seconds. Also clears any queued music.
            """

            self.stop()
            self.queue = [ ]

        def enqueue(self, filenames, loop=True, synchro_start=False, fadein=0, tight=None):
            self.queue.extend(filenames)

        def set_volume(self, volume):
            pass

        def get_pos(self):
            pass

        def set_pan(self, pan, delay):
            pass

        def set_secondary_volume(self, volume, delay):
            pass


# A list of channels we know about.
all_channels = [ ]

# A map from channel name to Channel object.
channels = { }


def register_channel(name, mixer=None, loop=None, stop_on_mute=True, tight=False, file_prefix="", file_suffix="", buffer_queue=True):
    """
    :doc: other

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
        If true, sounds will loop even when fadeout is occuring. This should
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
    """

    if not renpy.game.context().init_phase:
        raise Exception("Can't register channel outside of init phase.")

    if renpy.android and name == "movie":
        c = AndroidVideoChannel(name, default_loop=loop, file_prefix=file_prefix, file_suffix=file_suffix)
    else:
        c = Channel(name, loop, stop_on_mute, tight, file_prefix, file_suffix, buffer_queue)

    c.mixer = mixer

    all_channels.append(c)
    channels[name] = c


def alias_channel(name, newname):
    if not renpy.game.context().init_phase:
        raise Exception("Can't alias channel outside of init phase.")

    c = get_channel(name)
    channels[newname] = c


def get_channel(name):

    rv = channels.get(name)
    if rv is None:
        raise Exception("Audio channel %r is unknown." % name)

    return rv

def set_force_stop(name, value):
    get_channel(name).context.force_stop = value

def init():

    global pcm_ok
    global mix_ok

    if not renpy.config.sound:
        pcm_ok = False
        mix_ok = False
        return

    if pcm_ok is None and pss:
        bufsize = 2048

        if 'RENPY_SOUND_BUFSIZE' in os.environ:
            bufsize = int(os.environ['RENPY_SOUND_BUFSIZE'])

        try:
            pss.init(renpy.config.sound_sample_rate, 2, bufsize, False)
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


def quit(): #@ReservedAssignment

    global pcm_ok
    global mix_ok

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

    pss.quit()

    pcm_ok = None
    mix_ok = None

# The last-set pcm volume.
pcm_volume = None


def periodic():
    """
    The periodic sound callback. This is called at around 20hz, and is
    responsible for adjusting the volume of the playing music if
    necessary, and also for calling the periodic functions of midi and
    the various channels, which then may play music.
    """

    global pcm_volume

    if not pcm_ok:
        return False

    try:

        for c in all_channels:
            c.periodic()

        pss.periodic()

        # Perform a synchro-start if necessary.
        need_ss = False

        for c in all_channels:

            if c.synchro_start and c.wait_stop:
                need_ss = False
                break

            if c.synchro_start and not c.wait_stop:
                need_ss = True

        if need_ss:
            pss.unpause_all()

            for c in all_channels:
                c.synchro_start = False

    except:
        if renpy.config.debug_sound:
            raise


def interact():
    """
    Called at least once per interaction.
    """

    if not pcm_ok:
        return

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

            if c.default_loop:
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

    for c in all_channels:
        if not c.loop:
            c.fadeout(0)
