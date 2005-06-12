# This module contains code that handles the playing of sound and
# music files.

# NOTE TO SELF:
#
# Remember to code defensively against mikey's computer that
# doesn't have the sound card in it.

import pygame
import renpy
import sys # to detect windows.
import os

# The Windows Volume Management Strategy (tm).

# We keep a master music volume, which is the volume we use directly
# when playing music as mp3, ogg, etc. When we start up, we compute
# a midi music scaling factor. This midi music scaling factor is
# computed from the current master music volume such that when we are not
# fading, if we pygame.mixer.music.set_volume() to the mmv * mmsv, we get
# read the same value from midiOutGetVolume() as we did before we tried
# doing that.

# True if the mixer works, False if it doesn't, None if we have no
# idea yet.
mixer_works = None

# Common stuff.
mixer_enabled = True
playing_midi = True
fading = False
master_music_volume = 1.0

# Windows stuff.
midi_msf = 0.0
last_raw_volume = -1

def init():

    global mixer_works
    global read_raw_volume
    global compute_midi_msf
    global set_music_volume
    global playing_midi

    if mixer_works is not None:
        return

    if 'RENPY_DISABLE_SOUND' in os.environ:
        mixer_works = False
        return

    try:
        bufsize = 4096

        if 'RENPY_SOUND_BUFSIZE' in os.environ:
            bufsize = int(os.environ['RENPY_SOUND_BUFSIZE'])
        
        pygame.mixer.init(renpy.config.sound_sample_rate, -16, 2, bufsize)
        pygame.mixer.music.get_volume()
        mixer_works = True
    except:
        if renpy.config.debug_sound:
            raise
        else:
            mixer_works = False

    windows_magic = False

    if hasattr(sys, 'winver') and mixer_works:

        try:        
            from ctypes import windll, c_uint, byref
            winmm = windll.winmm

            def _read_raw_volume():
                res = c_uint()

                for i in range(0, winmm.midiOutGetNumDevs()):
                    rv = winmm.midiOutGetVolume(i, byref(res))

                    if not rv:
                        return res.value
                else:
                    print "Couldn't read raw midi volume."
                    return -1

            read_raw_volume = _read_raw_volume

            def _compute_midi_msf():
                """
                Computes the Midi MSF. Returns True if successful, False if otherwise.
                """

                # Don't update the MSF when fading is going on, or when not
                # playing a midi. (Except before playing any music whatsoever.)
                if fading or not playing_midi:
                    return False

                global last_raw_volume

                raw_vol = read_raw_volume()

                if raw_vol < 0:
                    return False

                # The case in which the volume hasn't changed recently.
                if raw_vol == last_raw_volume:
                    return True

                last_raw_volume = raw_vol

                # print "raw_vol", raw_vol

                # The fraction that the midi mixer is at.
                mixfrac = 1.0 * ( raw_vol & 0xffff ) / 0xffff

                global midi_msf
                midi_msf = mixfrac / master_music_volume

                # print "Midi msf is now:", midi_msf

                return True

            compute_midi_msf = _compute_midi_msf

            # This should get called after the music starts playing.
            def _set_music_volume(vol):

                global master_music_volume
                master_music_volume = vol

                if playing_midi:

                    vol *= midi_msf
                    if vol > 1.0:
                        vol = 1.0

                try:
                    pygame.mixer.music.set_volume(vol)
                except:
                    if renpy.config.debug_sound:
                        raise

                global last_raw_volume
                last_raw_volume = read_raw_volume()

            set_music_volume = _set_music_volume

            # Figure out the default msf, and set it up.
            windows_magic = compute_midi_msf()
            playing_midi = False

        except Exception, e:
            print "Exception when trying to init music:", str(e)
            print "Falling back to Unix mode."

    if not windows_magic:

        def _compute_midi_msf():
            return

        compute_midi_msf = _compute_midi_msf

        def _set_music_volume(vol):
            if not mixer_works:
                return

            global master_music_volume
            master_music_volume = vol

            try:
                pygame.mixer.music.set_volume(vol)
            except:
                if renpy.config.debug_sound:
                    raise

        set_music_volume = _set_music_volume
    
        playing_midi = False

    if mixer_works:
        pygame.mixer.music.set_endevent(renpy.display.core.MUSICEND)

        
def disable_mixer():
    """
    This function is called by the video code to disable the
    pygame mixer.
    """

    if not mixer_works:
        return

    global mixer_enabled
    
    if mixer_enabled:
        try:
            music_stop()
            pygame.mixer.quit()
        except:
            if renpy.config.debug_sound:
                raise
        
    mixer_enabled = False

def enable_mixer():
    """
    This function is called by the video code to enable the
    pygame mixer.
    """

    if not mixer_works:
        return

    global mixer_enabled

    if not mixer_enabled:
        try:
            pygame.mixer.init()
        except:
            if renpy.config.debug_sound:
                raise
            
    mixer_enabled = True


# This detects if the filename is a midi, and sets playing_midi
# appropriately.
def detect_midi(fn):

    fn = fn.lower()

    global playing_midi
    playing_midi = fn.endswith(".mid") or fn.endswith(".midi")
    

def music_delay(offset):
    """
    Returns the time left until the current music has been playing for
    offset seconds. If music is not playing, return None. May return
    a negative time.
    """

    if not mixer_works:
        return None

    mo = pygame.mixer.music.get_pos()
    if mo < 0:
        return None

    mo /= 1000.0

    return offset - mo

    

# def music_start(filename, loops=-1, startpos=0.0):
#     """
#     This starts music playing. If a music track is already playing,
#     stops that track in favor of this one.

#     @param filename: The file that the music will be played from. This
#     is relative to the game directory, and must be a real file (so it
#     cannot be stored in an archive.)

#     @param loops: The number of times the music will loop after it
#     finishes playing. If negative, the music will loop indefinitely.
#     Please note that even once the song has finished, rollback or load
#     may cause it to start playing again. So it may not be safe to have
#     this set to a non-negative value.

#     @param startpos: The number of seconds into the music to start playing.
#     """

#     if not mixer_works:
#         return

#     music_stop()
#     renpy.game.context().scene_lists.music = (filename, loops, startpos)
#     restore_music()


# def music_stop():
#     """
#     Stops the currently playing music track.
#     """

#     if not mixer_works:
#         return

#     renpy.game.context().scene_lists.music = None
#     restore_music()


# The filename of the currently playing piece of music.
playing_filename = None

# The filename of the currently queued piece of music.
queued_filename = None

# True if the music is in the process of fading out, or
# False otherwise.
fading = False

def music_update_volume():
    """
    Sets the volume as appropriate for a midi.
    """

    if not playing_filename:
        return

    detect_midi(playing_filename)
    set_music_volume(master_music_volume)

def music_end_event():
    """
    This is called by renpy.display.core when a track of music has
    endend. 
    """

    if not music_enabled():
        return

    try:

        # shift the filenames.
        global playing_filename
        global queued_filename
        global fading

        playing_filename = queued_filename
        queued_filename = None
        fading = False

        music_update_volume()

        # Call the appropriate function.
        if renpy.config.music_end_event:
            renpy.config.music_end_event()
    
    except:
        if renpy.config.debug_sound:
            raise

def music_enabled():
    """
    This should be called to check to see if music is enabled. If this
    returns False, then no music call should be made. Please note that
    this does not check preferences.music_enabled, so user code should
    also check that to see if music should be played.

    This will return True if the mixer works and it has not been
    pre-empted by the video player, and False otherwise.

    If this does not return True, none of the other music functions should
    be called.
    """

    return mixer_works and mixer_enabled

def music_play(filename):
    """
    This causes the named music filename to be loaded in and played.
    Music loaded in this way immediately replaces the currently
    playing music.

    The track is played once, and then stops. It's up to the higher-level
    music layer to ensure that a track that needs to be looped actually
    is.

    The filename must refer to a real file, and not a file hidden in an
    archive.
    """

    if not music_enabled():
        return

    try:

        global playing_filename
        global queued_filename
        global fading
        
        playing_filename = filename
        queued_filename = None
        fading = False

        fn = renpy.loader.transfn(filename)
        fn = str(fn)

        pygame.mixer.music.load(fn)

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
            
        music_update_volume()

    except:
        if renpy.config.debug_sound:
            raise

def music_queue(filename):
    """
    This causes the given filename to be placed into the queue, to be
    played immediately after the currently playing track finishes. 

    The filename must refer to a real file, and not a file hidden in an
    archive.
    """

    if not music_enabled():
        return

    try:
        global queued_filename
        queued_filename = filename
        
        pygame.mixer.music.queue(renpy.loader.transfn(filename))


    except:
        if renpy.config.debug_sound:
            raise

def music_stop():
    """
    This causes the music to be stopped immediately.
    """

    if not music_enabled():
        return

    try:

        global playing_filename
        global queued_filename
        global fading

        playing_filename = None
        queued_filename = None
        fading = False

        pygame.mixer.music.stop()

    except:

        if renpy.config.debug_sound:
            raise

def music_fadeout(seconds):
    """
    This causes the music to be faded out over a period of
    time.
    """

    # This works around a race condition in pygame/SDL_mixer.
    if seconds <= 0.0:
        music_stop()

    if not music_enabled():
        return

    try:
        global queued_filename
        global fading

        queued_filename = None
        fading = True

        pygame.mixer.music.fadeout(int(1000 * seconds))

    except:
        if renpy.config.debug_sound:
            raise

def music_filenames():
    """
    Returns a tuple giving the currently playing music filename and
    the filename of the track in the queue. It returns None if there
    is no filename in either slot.
    """

    if not music_enabled():
        return None, None

    try:

        return playing_filename, queued_filename

    except:
        if renpy.config.debug_sound:
            raise
        else:
            return None, None

def music_fading():
    """
    Returns True if the music is in the process of fading out, or False
    otherwise.
    """

    return fading

def music_pause():
    """
    Causes the currently playing music to be paused.
    """

    if not music_enabled():
        return

    try:

        pygame.mixer.music.pause()

    except:
        if renpy.config.debug_sound:
            raise

def music_unpause():
    """
    Causes the currently playing music to be unpaused, if it is
    currently paused.
    """

    if not music_enabled():
        return

    try:

        pygame.mixer.music.unpause()

    except:
        if renpy.config.debug_sound:
            raise

def sound_enabled():
    """
    Returns True if it's possible to play sound, or False if sound
    should not be played.

    Please note that this does not check preferences.sound. It's up
    to higher-level code (like renpy.play) to do that.
    """

    return mixer_works and mixer_enabled

def sound_play(filename, loops=0, channel=0):
    """
    This causes the sound contained in the given filename to be played.

    @param loops: The number of extra times that the sound will be
    played. If -1, the sound is played forever (until stopped).

    @param channel: The channel that the sound will be played on, an
    integer from 0 to 7. This allows us to support playing up to 8
    sounds at once.
    """

    if not sound_enabled():
        return

    try:
        chan = pygame.mixer.Channel(channel)
        chan.play(pygame.mixer.Sound(renpy.loader.load(filename)), loops)
    except:
        if renpy.config.debug_sound:
            raise
                                                          

def sound_stop(channel=0):
    """
    This causes the sound currently playing in the specified channel
    to be stopped.
    """

    if not music_enabled():
        return

    try:
        chan = pygame.mixer.Channel(channel)
        chan.stop()
    except:
        if renpy.config.debug_sound:
            raise

def play(fn, loops=0):
    """
    This plays the given sound. The sound must be in a wav file,
    and expected to have a sample rate 44100hz (changeable with
    config.sound_sample_rate), 16 bit, stereo. These expectations may
    be violated, but that may lead to conversion delays.

    Once a sound has been started, there's no way to stop it.

    @param fn: The name of the file that the sound is read from. This
    file may be contained in a game directory or an archive.

    @param loops: The number of extra times the sound will be
    played. (The default, 0, will play the sound once.)

    This plays the sound on channel 0.
    """

    if not fn:
        return

    if not renpy.game.preferences.sound:
        return

    sound_play(fn, loops=loops)
