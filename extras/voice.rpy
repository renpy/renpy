# This extra contains a basic implementation of voice support. Right
# now, voice is given its own toggle, and can either be turned on or
# turned off. In the future, we'll probably provide some way of
# toggling it on or off for individual characters.
#
# To use it, place a voice "<wavfile>" line before each voiced line of
# dialogue.
#
#     voice "e_1001.wav"
#     e "Voice support lets you add the spoken word to your games."
#
# Normally, a voice is cancelled at the start of the next
# interaction. If you want a voice to span interactions, call
# voice_sustain.
#
#     voice "e_1002.wav"
#     e "Voice sustain is a technique that allows the same voice file.."
#
#     $ voice_sustain()
#     e "...to play for two lines of dialogue."

init -440:

    python:

        # Ensure the voice preference exists.
        if persistent.voice is None:
            persistent.voice = True

        _voice = object()
        _voice.play = None
        _voice.sustain = False

        # Call this to specify the voice file that will be played for
        # the user.
        def voice(file):
            _voice.play = file

        # Call this to specify that the currently playing voice file
        # should be sustained through the current interaction.
        def voice_sustain(ignored=""):
            _voice.sustain = True

    python hide:

        renpy.sound.set_mixer(2, "voice")
        library.has_voice = True
        library.sample_voice = None
        
        vp = _VolumePreference('Voice Volume',
                               'voice',
                               'library.has_voice',
                               'library.sample_voice')

        library.preferences['prefs_right'].insert(1, vp)

        # This is called on each interaction, to ensure that the
        # appropriate voice file is played for the user.        
        def voice_interact():

            if not persistent.voice:
                return
            
            if _voice.play and not config.skipping:
                renpy.sound.play(_voice.play, channel=2)
            elif not _voice.sustain:
                renpy.sound.stop(channel=2)

            _voice.play = None
            _voice.sustain = False
        
        config.start_interact_callbacks.append(voice_interact)
