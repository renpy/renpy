﻿# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains code that sets up the various mixers, based on how
# the user sets config.has_music, .has_sound, and .has_voice.

init -1600 python hide:

    # Set to true in the very unlikely event you want to manually init
    # the sound system.
    config.force_sound = False

    # basics: True if the game will have music.
    config.has_music = True

    # basics: True if the game will have sound effects.
    config.has_sound = True

    # Sample sounds for various channels.
    config.sample_sound = None
    config.sample_voice = None


    # Register 8 channels by default, for compatiblity with older version
    # of Ren'Py.
    for i in xrange(0, 8):
        renpy.music.register_channel(i)

    renpy.music.register_channel("movie", "music", False, stop_on_mute=False, buffer_queue=False)

    # Set up default names for some of the channels.
    renpy.music.alias_channel(0, "sound")
    renpy.music.alias_channel(7, "music")
    renpy.music.alias_channel(2, "voice")

init 1600:

    python hide:

        if not config.has_music and not config.has_sound:
            mixers = None

        elif not config.has_music and config.has_sound:
            mixers = [ 'sfx' ] * 8

        elif config.has_music and not config.has_sound:
            mixers = [ 'music' ] * 8

        else:
            mixers = [ 'sfx' ] * 3 + [ 'music' ] * 5

        if config.has_voice:
            if not mixers:
                mixers = [ 'voice' ] * 8
            else:
                mixers[2] = 'voice'

        if not mixers:
            config.sound = config.force_sound

        else:
            for i, m in enumerate(mixers):
                renpy.sound.set_mixer(i, m, default=True)
                if m == 'music':
                    renpy.music.set_music(i, True, default=True)
                else:
                    renpy.music.set_music(i, False, default=True)

        _preferences.init_mixers()
