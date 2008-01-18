# This file contains code that sets up the various mixers, based on how
# the user sets config.has_music, .has_sound, and .has_voice.

init -1130:

    # Set to true in the very unlikely event you want to manually init
    # the sound system.
    $ config.force_sound = False

    # basics: True if the game will have music.
    $ config.has_music = True

    # basics: True if the game will have sound effects.
    $ config.has_sound = True
    
init 1130:

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
        
