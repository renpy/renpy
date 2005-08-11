# The latest and greatest Ren'Py audio system.

# Invariants: The periodic callback assumes pcm_ok. If we don't have
# at least pcm_ok, we have no sound whatsoever.

import renpy
import os
import atexit

# Import the appropriate modules, or set them to None if we cannot.
try:
    import pysdlsound as pss
    atexit.register(pss.quit)
except:
    pss = None

try:
    import nativemidi as nativemidi
except:
    nativemidi = None

try:
    import winmixer as mix
except:
    try:
        import linmixer as mix
    except:
        mix = None


# This is True if we were able to sucessfully enable the pcm audio.
pcm_ok = None

# This is True if we were able to succesfully enable native midi.
midi_ok = None

# True if we are managing the mixers ourselves.
mix_ok = None

def ismidi(s):
    """
    Returns true if s is the filename of a midi file.
    """

    return midi_ok and s is not None and s.endswith(".mid")

def load(fn):
    """
    Returns a file-like object for the given filename.
    """

    _f = file(fn, "r")
    print _f
    return _f

class Midi(object):
    """
    This is the object that manages the native midi playback. It ensures
    that only one channel can play midi at a time, and it keeps track
    of what's playing at any given time.
    """

    def __init__(self):

        # The filename of the music that is currently playing through
        # native midi.
        playing = None

        # The natural volume of the music that is playing through
        # native midi.
        volume = 1.0

    def play(self, f, filename):

        # Native midi must work for us to do anything.
        if not midi_ok:
            return

        # If the midi channel is still busy, then ignore this request
        # to play something new.
        if self.playing:
            return

        # Otherwise, immediately play this midi file,
        # replacing whatever is already playing.

        try:
            nativemidi.play(f)
            self.playing = filename
        except:
            self.playing = None
            if renpy.config.debug_sound:
                raise

    def busy(self):
        """
        Is midi busy?
        """
        
        return self.playing is not None
        
    def periodic(self):
        """
        The 20hz callback that checks on the status of midi. This should 
        be called before the updates for the various channel objects, below.
        """

        if not midi_ok:
            return

        if self.playing and not nativemidi.busy():
            self.playing = None

        # Eventually... add nativemidi fade code here.

    def stop(self):
        """
        Called to stop the native midi subsystem from playing music.
        """

        if not midi_ok:
            return

        midi.stop()
        self.playing = None

    def set_volume(self, volume):

        if midi_ok:
            midi.set_volume(volume)            

        self.volume = volume

# A singleton Midi object that manages hardware midi playback.
midi = Midi()

class Channel(object):

    def __init__(self, number):
        # The number of this channel.
        self.number = number

        # The name of the mixer this channel uses. Set below, as there's
        # no good default.
        self.mixer = None

        # The volume imparted to this channel, as a fraction of the
        # mixer volume.
        self.chan_volume = 1.0

        # The actual volume we imparted onto this channel.
        self.actual_volume = 1.0

        # The filenames that are being queued for playback on this
        # channel.
        self.queue = [ ]

        # If true, we loop the music. This entails re-adding the element to
        # the queue if it would make the queue empty. 
        self.loop = False

        # Are we playing anything at all?
        self.playing = False

        # If True, then this channel is playing midi. If False, it's
        # playing PCM instead.
        self.playing_midi = False

        # If True, we'll wait for this channel to stop before
        # loading in more music from the queue. (This is necessary to
        # do a synchro-start.)
        self.wait_stop = False

        # If True, then this channel will participate in a synchro-start
        # once all channels are ready.
        self.synchro_start = False

        # If we're a music channel, the time the music in this channel was
        # last changed.
        self.music_last_changed = 0

        # The callback that is called if the queue becomes empty.
        self.callback = None

    def periodic(self):
        """
        This is the periodic call that causes this channel to load new stuff
        into its queues, if necessary.
        """

        # This should be set from something that checks to see if our
        # mixer is muted.
        force_stop = renpy.game.preferences.mute[self.mixer]

        if self.playing and force_stop:
            if self.playing_midi:
                midi.stop()
                self.playing = False
                self.wait_stop = False
                self.playing_midi = False

            else:
                pss.stop(self.number)
                self.playing = False
                self.wait_stop = False

            return

        # If we're playing midi, and the midi device is busy, return.
        # Otherwise, it's stopped, so we can stop waiting.
        if self.playing_midi:
            if midi.busy():
                return
            else:
                self.playing = False
                self.wait_stop = False
                self.playing_midi = False


        # Should we do the callback?
        do_callback = False

        while True:

            depth = pss.queue_depth(self.number)

            if depth == 0:
                self.wait_stop = False
                self.playing = False

            # Need to check this, so we don't do pointless work.
            if not self.queue:
                break

            # If we're still playing midi, then we can't queue
            # anything up, so bail out now.
            if self.playing_midi:
                break

            # If the pcm_queue is full, then we can't queue
            # anything, regardless of if it is midi or pcm.
            if depth >= 2:
                break

            # If the queue is full, return.
            if pss.queue_depth(self.number) >= 2:
                break

            # Otherwise, we might be able to enqueue something.
            top = self.queue[0]

            # We can only play midi if we're not playing PCM.
            if ismidi(top):
                if depth != 0:
                    break

            # At this point, we've decided to try to play
            # top. So let's see how far we can get.

            # Update the queue
            self.queue = self.queue[1:]

            try:
                topf = load(top)

                if ismidi(top):

                    # If someone else is playing midi, then raise
                    # an error to that effect.
                    if midi.busy():
                        raise Exception, "We can only play one midi at a time."                        

                    # Play midi.
                    midi.play(topf, top)
                    self.playing = True
                    self.playing_midi = True

                else:
                    if depth == 0:
                        pss.play(self.number, topf, top, self.synchro_start)
                    else:
                        pss.queue(self.number, topf, top)

                    self.playing = True

            except:
                if renpy.config.debug_sound:
                    raise
                else:
                    return

            if self.loop and not self.queue:
                self.queue.append(top)
            else:
                do_callback = True

        # TODO: Queue empty callback.
        if do_callback and self.callback:
            self.callback()

    def dequeue(self):
        """
        Clears any queued music. Doesn't stop the playing music, if
        any, but will prevent looping from occuring.
        """

        self.queue = [ ]
        self.loop = False

        if not pcm_ok:
            return

        if not self.playing_midi:
            pss.dequeue(self.number)

    def interact(self):
        """
        Called (mostly) once per interaction. Calls the queue callback
        if it's becoming empty.
        """

        if not self.queue and self.callback:
            self.callback()


    def fadeout(self, ms):
        """
        Causes the playing music to be faded out for the given number
        of seconds. Also clears any queued music.
        """

        self.dequeue()

        if not pcm_ok:
            return

        if self.playing_midi:
            midi.stop()
        else:
            pss.fadeout(self.number, ms)


    def enqueue(self, filename, loop=True, synchro_start=False):

        if not pcm_ok:
            return

        self.queue.append(filename)
        self.loop = loop

        self.wait_stop = synchro_start
        self.syncro_start = synchro_start

    def set_volume(self, volume):
        self.chan_volume = volume
            
            

            
# The number of channels we support.
NUM_CHANNELS = 8

# A list of channels.
channels = [ Channel(i) for i in range(NUM_CHANNELS) ]
    
channels[0].mixer = 'sfx'
channels[1].mixer = 'sfx'
channels[2].mixer = 'voice'
channels[3].mixer = 'music'
channels[4].mixer = 'music'
channels[5].mixer = 'music'
channels[6].mixer = 'music'
channels[7].mixer = 'music'

def get_channel(number):
    if not 0 <= number < NUM_CHANNELS:
        raise Exception("Channel number %d out of bounds." % channel)

    return channels[number]
    

def init():

    global pcm_ok
    global midi_ok
    global mix_ok

    if 'RENPY_DISABLE_SOUND' in os.environ:
        return
        
    if pcm_ok is None and pss:
        bufsize = 4096
                
        if 'RENPY_SOUND_BUFSIZE' in os.environ:
            bufsize = int(os.environ['RENPY_SOUND_BUFSIZE'])


        try:
            pss.init(renpy.config.sound_sample_rate, 2, bufsize)
            pcm_ok = True
        except:
            if renpy.config.debug_sound:
                raise
            pcm_ok = False
            
    if midi_ok is None and nativemidi:

        try:
            nativemidi.init()
            midi_ok = True
        except:
            if renpy.config.debug_sound:
                raise
            midi_ok = False

    # Find all of the mixers in the game.
    mixers = [ ]

    for c in channels:
        if c.mixer not in mixers:
            mixers.append(c.mixer)

    default_volume = 1.0

    if mix and not 'RENPY_NOMIXER' in os.environ and mix.get_wave() is not None:
        default_volume = mix.get_wave()
        mix_ok = True

    
    for m in mixers:
        renpy.game.preferences.volumes.setdefault(m, default_volume)
        renpy.game.preferences.mute.setdefault(m, False)


def quit():
    """
    Deinitialize the mixer and the various libraries.
    """

    if not pcm_ok:
        return
    
    for c in channels:
        c.dequeue()
        c.fadeout(0)
        
        c.queue = [ ]
        c.loop = False
        c.playing = False
        c.playing_midi = False
        c.wait_stop = False
        c.synchro_start = False
        
    pss.quit()
    
    pcm_ok = None    
    midi_ok = None
    mix_ok = None
 
# The last-set pcm volume.
pcm_volume = None

# The last-set midi volume.
midi_volume = None

def periodic():
    """
    The periodic sound callback. This is called at around 20hz, and is
    responsible for adjusting the volume of the playing music if
    necessary, and also for calling the periodic functions of midi and
    the various channels, which then may play music.
    """

    global pcm_volume
    global midi_volume

    if not pcm_ok:
        return False

    try:

        for c in channels:
            c.periodic()

        midi.periodic()

        # Perform a synchro-start if necessary.
        need_ss = False

        for c in channels:
            if c.synchro_start and c.wait_stop:
                need_ss = False
                break

            if c.synchro_start and not c.wait_stop:
                need_ss = True

        if need_ss:
            pss.unpause_all()

        # Now, consider adjusting the volume of the channel. 

        max_volume = -1.0
        volumes = renpy.game.preferences.volumes

        if mix_ok:

            for c in channels:

                # if not c.playing:
                #    continue

                vol = c.chan_volume * volumes[c.mixer]
                max_volume = max(max_volume, vol)

            if max_volume == -1.0:
                return

            if max_volume != pcm_volume:    
                mix.set_wave(max_volume)
                pcm_volume = max_volume

            for c in channels:

                # if not c.playing:
                #    continue

                vol = c.chan_volume * volumes[c.mixer]

                if c.playing_midi:
                    if midi_volume != vol:
                        mix.set_midi(vol)
                        midi.set_volume(1.0)
                        midi_volume = vol
                else:
                    vol /= max_volume

                    if c.actual_volume != vol:
                        pss.set_volume(c.number, vol)
                        c.acutal_volume = vol

        else:

            for c in channels:

                if not c.playing:
                    continue

                vol = c.chan_volume * volumes[c.mixer]

                if c.playing_midi:
                    if vol != midi_volume:
                        midi.set_volume(vol)
                        midi_volume = vol
                else:
                    if vol != c.actual_volume:
                        pss.set_volume(c.number, vol)
                        c.actual_volume = vol

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

        for c in channels:
            c.interact()

    except:
        if renpy.config.debug_sound:
            raise

