# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains code that creates a few new statements.

init -1200 python in audio:
    pass

init -1200 python:

    config.default_sound_loop = None

    def _audio_eval(expr):
        return eval(expr, locals=store.audio.__dict__)

    def _try_eval(e, what):
        try:
            return _audio_eval(e)
        except:
            renpy.error('unable to evaluate %s %r' % (what, e))

python early hide:

    # Music play - The example of a full statement.

    def parse_play_music(l):

        file = l.simple_expression()
        if not file:
            renpy.error("play requires a file")

        fadeout = "None"
        fadein = "0"
        channel = None
        loop = None
        if_changed = False

        while True:

            if l.eol():
                break

            if l.keyword('fadeout'):
                fadeout = l.simple_expression()
                if fadeout is None:
                    renpy.error('expected simple expression')

                continue

            if l.keyword('fadein'):
                fadein = l.simple_expression()
                if fadein is None:
                    renpy.error('expected simple expression')

                continue

            if l.keyword('channel'):
                channel = l.simple_expression()
                if channel is None:
                    renpy.error('expected simple expression')

                continue

            if l.keyword('loop'):
                loop = True
                continue

            if l.keyword('noloop'):
                loop = False
                continue

            if l.keyword('if_changed'):
                if_changed = True
                continue

            renpy.error('could not parse statement.')

        return dict(file=file,
                    fadeout=fadeout,
                    fadein=fadein,
                    channel=channel,
                    loop=loop,
                    if_changed=if_changed)

    def execute_play_music(p):

        if p["channel"] is not None:
            channel = eval(p["channel"])
        else:
            channel = "music"

        renpy.music.play(_audio_eval(p["file"]),
                         fadeout=eval(p["fadeout"]),
                         fadein=eval(p["fadein"]),
                         channel=channel,
                         loop=p.get("loop", None),
                         if_changed=p.get("if_changed", False))

    def predict_play_music(p):
        return [ ]

    def lint_play_music(p, channel="music"):

        file = _try_eval(p["file"], 'filename')

        if p["channel"] is not None:
            channel = _try_eval(p["channel"], 'channel')

        if not isinstance(file, list):
            file = [ file ]

        for fn in file:
            if isinstance(fn, basestring):
                try:
                    if not renpy.music.playable(fn, channel):
                        renpy.error("%r is not loadable" % fn)
                except:
                    pass

    renpy.register_statement('play music',
                              parse=parse_play_music,
                              execute=execute_play_music,
                              predict=predict_play_music,
                              lint=lint_play_music)

    # From here on, we'll steal bits of other statements when defining other
    # statements.

    def parse_queue_music(l):

        file = l.simple_expression()
        if not file:
            renpy.error("queue requires a file")

        channel = None
        loop = None

        while not l.eol():

            if l.keyword('channel'):
                channel = l.simple_expression()
                if channel is None:
                    renpy.error('expected simple expression')

            if l.keyword('loop'):
                loop = True
                continue

            if l.keyword('noloop'):
                loop = False
                continue

            renpy.error('expected end of line')

        return dict(file=file, channel=channel, loop=loop)

    def execute_queue_music(p):
        if p["channel"] is not None:
            channel = eval(p["channel"])
        else:
            channel = "music"

        renpy.music.queue(
            _audio_eval(p["file"]),
            channel=channel,
            loop=p.get("loop", None))


    renpy.register_statement('queue music',
                              parse=parse_queue_music,
                              execute=execute_queue_music,
                              lint=lint_play_music)

    def parse_stop_music(l):
        fadeout = "None"

        if l.keyword("fadeout"):
            fadeout = l.simple_expression()

        channel = None

        if l.keyword('channel'):
            channel = l.simple_expression()
            if channel is None:
                renpy.error('expected simple expression')

        if not l.eol():
            renpy.error('expected end of line')

        if fadeout is None:
            renpy.error('expected simple expression')

        return dict(fadeout=fadeout, channel=channel)

    def execute_stop_music(p):
        if p["channel"] is not None:
            channel = eval(p["channel"])
        else:
            channel = "music"

        renpy.music.stop(fadeout=eval(p["fadeout"]), channel=channel)

    renpy.register_statement('stop music',
                              parse=parse_stop_music,
                              execute=execute_stop_music)


    # Sound statements. They share alot with the equivalent music
    # statements.

    def execute_play_sound(p):

        if p["channel"] is not None:
            channel = eval(p["channel"])
        else:
            channel = "sound"

        fadeout = eval(p["fadeout"]) or 0

        loop = p.get("loop", False)

        if loop is None:
            loop = config.default_sound_loop

        renpy.sound.play(_audio_eval(p["file"]),
                         fadeout=fadeout,
                         fadein=eval(p["fadein"]),
                         loop=loop,
                         channel=channel)

    def lint_play_sound(p, lint_play_music=lint_play_music):
        return lint_play_music(p, channel="sound")

    renpy.register_statement('play sound',
                              parse=parse_play_music,
                              execute=execute_play_sound,
                              lint=lint_play_sound)

    def execute_queue_sound(p):
        if p["channel"] is not None:
            channel = eval(p["channel"])
        else:
            channel = "sound"

        loop = p.get("loop", False)

        if loop is None:
            loop = config.default_sound_loop

        renpy.sound.queue(_audio_eval(p["file"]), channel=channel, loop=loop)


    renpy.register_statement('queue sound',
                              parse=parse_queue_music,
                              execute=execute_queue_sound,
                              lint=lint_play_sound)

    def execute_stop_sound(p):
        if p["channel"] is not None:
            channel = eval(p["channel"])
        else:
            channel = "sound"

        fadeout = eval(p["fadeout"]) or 0

        renpy.sound.stop(fadeout=fadeout, channel=channel)

    renpy.register_statement('stop sound',
                              parse=parse_stop_music,
                              execute=execute_stop_sound)


    # Generic play/queue/stop statements. These take a channel name as
    # the second thing.

    def parse_play_generic(l, parse_play_music=parse_play_music):
        channel = l.name()

        if channel is None:
            renpy.error('play requires a channel')

        rv = parse_play_music(l)
        if rv["channel"] is None:
            rv["channel"] = repr(channel)

        return rv

    def parse_queue_generic(l, parse_queue_music=parse_queue_music):
        channel = l.name()

        if channel is None:
            renpy.error('queue requires a channel')

        rv = parse_queue_music(l)
        if rv["channel"] is None:
            rv["channel"] = repr(channel)

        return rv

    def parse_stop_generic(l, parse_stop_music=parse_stop_music):
        channel = l.name()

        if channel is None:
            renpy.error('stop requires a channel')

        rv = parse_stop_music(l)
        if rv["channel"] is None:
            rv["channel"] = repr(channel)

        return rv

    def lint_play_generic(p, lint_play_music=lint_play_music):
        channel = eval(p["channel"])

        if not renpy.music.channel_defined(channel):
            renpy.error("channel %r is not defined" % channel)

        lint_play_music(p, channel)

    def lint_stop_generic(p):
        channel = eval(p["channel"])

        if not renpy.music.channel_defined(channel):
            renpy.error("channel %r is not defined" % channel)

    renpy.register_statement('play',
                              parse=parse_play_generic,
                              execute=execute_play_music,
                              predict=predict_play_music,
                              lint=lint_play_generic)

    renpy.register_statement('queue',
                              parse=parse_queue_generic,
                              execute=execute_queue_music,
                              lint=lint_play_generic)

    renpy.register_statement('stop',
                              parse=parse_stop_generic,
                              execute=execute_stop_music,
                              lint=lint_stop_generic)



    ##########################################################################
    # Pause statement.

    def parse_pause(l):

        delay = l.simple_expression()

        if not l.eol():
            renpy.error("expected end of line.")

        return { "delay" : delay }

    def lint_pause(p):

        if p["delay"]:
            _try_eval(p["delay"], 'pause statement')

    def execute_pause(p):

        if p["delay"]:
            delay = eval(p["delay"])
            renpy.with_statement(Pause(delay))
        else:
            renpy.pause()


    renpy.register_statement('pause',
                              parse=parse_pause,
                              lint=lint_pause,
                              execute=execute_pause)


##############################################################################
# Screen-related statements.

python early hide:

    # Should we predict screens?
    config.predict_screen_statements = True

    def parse_show_call_screen(l):

        # Parse a name.
        name = l.require(l.name)

        # Parse the list of arguments.
        arguments = renpy.parser.parse_arguments(l)

        predict = True
        transition_expr = None

        while True:

            if l.keyword('nopredict'):
                predict = False

            elif l.keyword('with'):
                transition_expr = l.require(l.simple_expression)

            else:
                break

        l.expect_eol()

        return dict(name=name, arguments=arguments, predict=predict, transition_expr=transition_expr)

    def parse_hide_screen(l):
        name = l.require(l.name)

        l.expect_eol()

        return dict(name=name)

    def predict_screen(p):

        if not config.predict_screen_statements:
            return

        predict = p.get("predict", False)

        if not predict:
            return

        name = p["name"]
        a = p["arguments"]

        if a is not None:
            args, kwargs = a.evaluate()
        else:
            args = [ ]
            kwargs = { }

        renpy.predict_screen(name, *args, **kwargs)

    def execute_show_screen(p):

        name = p["name"]
        a = p["arguments"]

        if a is not None:
            args, kwargs = a.evaluate()
        else:
            args = [ ]
            kwargs = { }

        renpy.show_screen(name, *args, **kwargs)

    def execute_call_screen(p):

        name = p["name"]
        a = p["arguments"]

        transition_expr = p.get("transition_expr", None)

        if transition_expr is not None:
            renpy.transition(eval(transition_expr))

        if a is not None:
            args, kwargs = a.evaluate()
        else:
            args = [ ]
            kwargs = { }

        store._return = renpy.call_screen(name, *args, **kwargs)

    def execute_hide_screen(p):
        name = p["name"]
        renpy.hide_screen(name)

    def lint_screen(p):
        name = p["name"]
        if not renpy.has_screen(name):
            renpy.error("Screen %s does not exist." % name)


    renpy.register_statement("show screen",
                              parse=parse_show_call_screen,
                              execute=execute_show_screen,
                              predict=predict_screen,
                              lint=lint_screen)

    renpy.register_statement("call screen",
                              parse=parse_show_call_screen,
                              execute=execute_call_screen,
                              predict=predict_screen,
                              lint=lint_screen)

    renpy.register_statement("hide screen",
                              parse=parse_hide_screen,
                              execute=execute_hide_screen)
