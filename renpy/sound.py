# Plays sounds.

import renpy

import pygame
from pygame.constants import *

def init():
    try:
        pygame.mixer.init(renpy.config.sound_sample_rate)
    except:
        if renpy.config.debug_sound:
            raise
        
def play(fn, loops=0):
    """
    This plays the given sound. The sound must be in a wav file,
    and expected to have a sample rate 44100hz (changable with
    config.sound_sample_rate), 16 bit, stereo. These expectations may
    be violated, but that may lead to conversion delays.

    Once a sound has been started, there's no way to stop it.

    @param fn: The name of the file that the sound is read from. This
    file may be contained in a game directory or an archive.

    @param loops: The number of extra times the sound will be
    played. (The default, 0, will play the sound once.)
    """

    if not fn:
        return

    if not renpy.game.preferences.sound:
        return

    try:
        sound = pygame.mixer.Sound(renpy.loader.load(fn))
        sound.play()
    except:
        if renpy.config.debug_sound:
            raise
        
