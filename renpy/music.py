# This module contains code that handles the playing of music.

import pygame
import renpy
import sys # to detect windows.

# The Windows Volume Management Strategy (tm).

# We keep a master music volume, which is the volume we use directly
# when playing music as mp3, ogg, etc. When we start up, we compute
# a midi music scaling factor. This midi music scaling factor is
# computed from the current master music volume such that when we are not
# fading, if we pygame.mixer.music.set_volume() to the mmv * mmsv, we get
# read the same value from midiOutGetVolume() as we did before we tried
# doing that.


playing_midi = True
fading = False
master_music_volume = 1.0


windows_magic = False

if hasattr(sys, 'winver'):

    midi_msf = 0.0

    last_raw_volume = -1
    
    def read_raw_volume():
        res = c_uint()
        
        for i in range(0, winmm.midiOutGetNumDevs()):
            rv = winmm.midiOutGetVolume(i, byref(res))

            if not rv:
                return res.value
        else:
            print "Couldn't read raw midi volume."
            return -1

        

    try:        
        from ctypes import windll, c_uint, byref
        winmm = windll.winmm
            

        def compute_midi_msf():
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

        # This should get called after the music starts playing.
        def set_music_volume(vol):

            global master_music_volume
            master_music_volume = vol

            if playing_midi:
                
                vol *= midi_msf
                if vol > 1.0:
                    vol = 1.0

            pygame.mixer.music.set_volume(vol)

            global last_raw_volume
            last_raw_volume = read_raw_volume()

        # Figure out the default msf, and set it up.
        windows_magic = compute_midi_msf()
        playing_midi = False

    except Exception, e:
        print "Exception when trying to init music:", str(e)
        print "Falling back to Unix mode."
            
if not windows_magic:

    def compute_midi_msf():
        return

    def set_music_volume(vol):        
        global master_music_volume
        master_music_volume = vol
            
        pygame.mixer.music.set_volume(vol)

    playing_midi = False

# This detects if the filename is a midi, and sets playing_midi
# appropriately.
def detect_midi(fn):

    fn = fn.lower()

    global playing_midi
    playing_midi = fn.endswith(".mid") or fn.endswith(".midi")
    

# Information about the currently playing track.
current_music = None

def music_delay(offset):
    """
    Returns the time left until the current music has been playing for
    offset seconds. If music is not playing, return None. May return
    a negative time.
    """

    mo = pygame.mixer.music.get_pos()
    if mo < 0:
        return None

    mo /= 1000.0

    return offset - mo

    

def music_start(filename, loops=-1, startpos=0.0):
    """
    This starts music playing. If a music track is already playing,
    stops that track in favor of this one.

    @param filename: The file that the music will be played from. This
    is relative to the game directory, and must be a real file (so it
    cannot be stored in an archive.)

    @param loops: The number of times the music will loop after it
    finishes playing. If negative, the music will loop indefinitely.
    Please note that even once the song has finished, rollback or load
    may cause it to start playing again. So it may not be safe to have
    this set to a non-negative value.

    @param startpos: The number of seconds into the music to start playing.
    """

    music_stop()
    renpy.game.context().scene_lists.music = (filename, loops, startpos)
    restore()


def music_stop():
    """
    Stops the currently playing music track.
    """

    renpy.game.context().scene_lists.music = None
    restore()

def restore():
    """
    This makes sure that the current music matches the music found in
    the context.
    """

    global current_music
    global fading

    compute_midi_msf()
    set_music_volume(1.0)

    new_music = renpy.game.context().scene_lists.music

    if not renpy.game.preferences.music:
        new_music = None

    if current_music == new_music:
        return

    # Usually, ignore errors.
    try:
        if current_music != new_music and current_music:
            current_music = None
            pygame.mixer.music.fadeout(int(renpy.config.fade_music * 1000))
            fading = True
        else:
            if not pygame.mixer.music.get_busy():
                fn, loops, startpos = new_music

                fading = False
                detect_midi(fn)

                pygame.mixer.music.load(renpy.game.basepath + "/" + fn)
                pygame.mixer.music.play(loops, startpos)

                set_music_volume(master_music_volume)

                current_music = new_music

    except pygame.error, e:
        if renpy.config.debug_sound:
            raise
        else:
            print "Error while trying to play music:", str(e)
