﻿# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

# This extra contains a basic implementation of voice support. Right
# now, voice is given its own toggle, and can either be turned on or
# turned off. In the future, we'll probably provide some way of
# toggling it on or off for individual characters.
#
# To use it, place a voice "<sndfile>" line before each voiced line of
# dialogue.
#
#     voice "e_1001.ogg"
#     e "Voice support lets you add the spoken word to your games."
#
# Normally, a voice is cancelled at the start of the next
# interaction. If you want a voice to span interactions, call
# voice_sustain.
#
#     voice "e_1002.ogg"
#     e "Voice sustain is a technique that allows the same voice file.."
#
#     $ voice_sustain()
#     e "...to play for two lines of dialogue."

init -1500:

    python:

        _voice = object()
        _voice.play = None
        _voice.sustain = False
        _voice.seen_in_lint = False

        # Call this to specify the voice file that will be played for
        # the user.
        def voice(file, **kwargs):

            if not config.has_voice:
                return
            
            _voice.play = file
            _last_voice_play = file 
            
        # Call this to specify that the currently playing voice file
        # should be sustained through the current interaction.
        def voice_sustain(ignored="", **kwargs):
            if not config.has_voice:
                return
            
            _voice.sustain = True

        # Call this to replay the last bit of voice.
        def voice_replay():
            renpy.sound.play(_last_voice_play, channel="voice")

        # Returns true if we can replay the voice.
        def voice_can_replay():
            return _last_voice_play != None
            
    python hide:

        # basics: True if the game will have voice.
        config.has_voice = True

        # This is called on each interaction, to ensure that the
        # appropriate voice file is played for the user.        
        def voice_interact():
            
            if not config.has_voice:
                return
            
            if _voice.play and not config.skipping:
                renpy.sound.play(_voice.play, channel="voice")
                store._last_voice_play = _voice.play        
            elif not _voice.sustain:
                renpy.sound.stop(channel="voice")
                store._last_voice_play = _voice.play        

            _voice.play = None
            _voice.sustain = False
        
        config.start_interact_callbacks.append(voice_interact)
        config.say_sustain_callbacks.append(voice_sustain)

        def voice_afm_callback():
            return not renpy.sound.is_playing(channel="voice")

        config.afm_callback = voice_afm_callback
                       
python early hide:

    def parse_voice(l):
        fn = l.simple_expression()
        if fn is None:
            renpy.error('expected simple expression (string)')

        if not l.eol():
            renpy.error('expected end of line')

        return fn

    def execute_voice(fn):
        fn = eval(fn)
        voice(fn)

    def lint_voice(fn):
        _voice.seen_in_lint = True

        fn = _try_eval(fn, 'voice filename')
        if isinstance(fn, basestring) and not renpy.loadable(fn):
            renpy.error('voice file %r is not loadable' % fn)

    renpy.statements.register('voice',
                              parse=parse_voice,
                              execute=execute_voice,
                              lint=lint_voice,
                              translatable=True)

    def parse_voice_sustain(l):
        if not l.eol():
            renpy.error('expected end of line')

        return None

    def execute_voice_sustain(parsed):
        voice_sustain()

    renpy.statements.register('voice sustain',
                              parse=parse_voice_sustain,
                              execute=execute_voice_sustain,
                              translatable=True)


