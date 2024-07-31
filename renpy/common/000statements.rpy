# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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
    # Do not participate in saves.
    _constant = True

init -1200 python:

    config.default_sound_loop = None

    def _audio_eval(expr):
        return eval(expr, locals=store.audio.__dict__)

    def _try_eval(e, what):
        try:
            return _audio_eval(e)
        except Exception:
            renpy.error('unable to evaluate %s %r' % (what, e))

python early hide:

    def warp_audio(p):
        """
        Determines if we should play this statement while warping.
        """

        if p.get("channel", None) is not None:
            channel = eval(p["channel"])
        else:
            channel = "music"

        return renpy.music.is_music(channel)

    def parse_play_music(l):

        file = l.simple_expression()
        if not file:
            renpy.error("play requires a file")

        fadeout = "None"
        fadein = "0"
        channel = None
        loop = None
        if_changed = False
        volume = "1.0"

        while not l.eol():

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

            if l.keyword('volume'):
                volume = l.simple_expression()
                continue

            renpy.error('expected end of line')

        return dict(file=file,
                    fadeout=fadeout,
                    fadein=fadein,
                    channel=channel,
                    loop=loop,
                    if_changed=if_changed,
                    volume=volume)

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
                         if_changed=p.get("if_changed", False),
                         relative_volume=eval(p.get("volume", "1.0")))

    def predict_play_music(p):
        if renpy.emscripten or os.environ.get('RENPY_SIMULATE_DOWNLOAD', False):
            fn = _audio_eval(p["file"])
            try:
                with renpy.loader.load(fn, directory="audio") as f:
                    pass
            except renpy.webloader.DownloadNeeded as exception:
                renpy.webloader.enqueue(exception.relpath, 'music', None)
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
                except Exception:
                    pass

    renpy.register_statement('play music',
                              parse=parse_play_music,
                              execute=execute_play_music,
                              predict=predict_play_music,
                              lint=lint_play_music,
                              warp=warp_audio)

    # From here on, we'll steal bits of other statements when defining other
    # statements.

    def parse_queue_music(l):

        file = l.simple_expression()
        if not file:
            renpy.error("queue requires a file")

        channel = None
        loop = None
        volume = "1.0"
        fadein = "0"

        while not l.eol():

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

            if l.keyword('volume'):
                volume = l.simple_expression()
                continue

            if l.keyword('fadein'):
                fadein = l.simple_expression()
                if fadein is None:
                    renpy.error('expected simple expression')

                continue

            renpy.error('expected end of line')

        return dict(file=file, channel=channel, loop=loop, volume=volume, fadein=fadein)

    def execute_queue_music(p):
        if p["channel"] is not None:
            channel = eval(p["channel"])
        else:
            channel = "music"

        renpy.music.queue(
            _audio_eval(p["file"]),
            channel=channel,
            loop=p.get("loop", None),
            relative_volume=eval(p.get("volume", "1.0")),
            fadein=eval(p.get("fadein", "0")),
            )


    renpy.register_statement('queue music',
                              parse=parse_queue_music,
                              execute=execute_queue_music,
                              lint=lint_play_music,
                              warp=warp_audio)

    def parse_stop_music(l):
        channel = None
        fadeout = "None"

        while not l.eol():

            if l.keyword("fadeout"):
                fadeout = l.simple_expression()
                if fadeout is None:
                    renpy.error('expected simple expression')

                continue

            if l.keyword('channel'):
                channel = l.simple_expression()
                if channel is None:
                    renpy.error('expected simple expression')

                continue

            renpy.error('expected end of line')

        return dict(fadeout=fadeout, channel=channel)

    def execute_stop_music(p):
        if p["channel"] is not None:
            channel = eval(p["channel"])
        else:
            channel = "music"

        renpy.music.stop(fadeout=eval(p["fadeout"]), channel=channel)

    renpy.register_statement('stop music',
                              parse=parse_stop_music,
                              execute=execute_stop_music,
                              warp=warp_audio)


    # Sound statements. They share alot with the equivalent music
    # statements.

    def warp_sound(p):
        """
        Determines if we should play this statement while warping.
        """

        if p.get("channel", None) is not None:
            channel = eval(p["channel"])
        else:
            channel = "sound"

        return renpy.music.is_music(channel)

    def execute_play_sound(p):

        if p["channel"] is not None:
            channel = eval(p["channel"])
        else:
            channel = "sound"

        fadeout = eval(p["fadeout"]) or None

        loop = p.get("loop", False)

        if loop is None:
            loop = config.default_sound_loop

        renpy.sound.play(_audio_eval(p["file"]),
                         fadeout=fadeout,
                         fadein=eval(p["fadein"]),
                         loop=loop,
                         channel=channel,
                         relative_volume=eval(p.get("volume", "1.0")))

    def lint_play_sound(p, lint_play_music=lint_play_music):
        return lint_play_music(p, channel="sound")

    renpy.register_statement('play sound',
                              parse=parse_play_music,
                              execute=execute_play_sound,
                              lint=lint_play_sound,
                              warp=warp_sound)

    def execute_queue_sound(p):
        if p["channel"] is not None:
            channel = eval(p["channel"])
        else:
            channel = "sound"

        loop = p.get("loop", False)

        if loop is None:
            loop = config.default_sound_loop

        renpy.sound.queue(
            _audio_eval(p["file"]),
            channel=channel,
            fadein=eval(p.get("fadein", "0")),
            loop=loop,
            relative_volume=eval(p.get("volume", "1.0"))
            )


    renpy.register_statement('queue sound',
                              parse=parse_queue_music,
                              execute=execute_queue_sound,
                              lint=lint_play_sound,
                              warp=warp_sound)

    def execute_stop_sound(p):
        if p["channel"] is not None:
            channel = eval(p["channel"])
        else:
            channel = "sound"

        fadeout = eval(p["fadeout"]) or None

        renpy.sound.stop(fadeout=fadeout, channel=channel)

    renpy.register_statement('stop sound',
                              parse=parse_stop_music,
                              execute=execute_stop_sound,
                              warp=warp_sound)


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
                              lint=lint_play_generic,
                              warp=warp_audio)

    renpy.register_statement('queue',
                              parse=parse_queue_generic,
                              execute=execute_queue_music,
                              lint=lint_play_generic,
                              warp=warp_audio)

    renpy.register_statement('stop',
                              parse=parse_stop_generic,
                              execute=execute_stop_music,
                              lint=lint_stop_generic,
                              warp=warp_audio)



    ##########################################################################
    # Pause statement.

    # Should the pause statement use the pause Transition?
    config.pause_with_transition = False

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
            if config.pause_with_transition:
                renpy.with_statement(Pause(delay))
            else:
                renpy.pause(delay)
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

    def _get_screen_name(p):
        """
        Returns screen name from the parsed data, evals it
        if it's an expression
        """
        name = p["name"]
        if p.get("expression", False):
            return eval(name)

        return name

    def _parse_screen_name(l):
        """
        Parses screen name from the lexer, returns tuple of 2 items

        OUT:
            tuple:
                (name, is_expression)
        """
        # Check if this screen name is an expression
        if l.keyword("expression"):
            is_expression = True
            name = l.require(l.simple_expression)

        # Otherwise just parse a name
        else:
            is_expression = False
            name = l.require(l.name)

        return (name, is_expression)

    def _get_screen_props(p):
        """
        Returns screen properties from the parsed data,
        they keys are prefixed with _ and can be used as arguments
        to the appropriate functions

        OUT:
            dict
        """
        layer = p.get("layer", None)
        zorder = p.get("zorder", None)
        if zorder is not None:
            zorder = eval(zorder)
        tag = p.get("tag", None)

        return dict(_layer=layer, _zorder=zorder, _tag=tag)

    def warp_true(p):
        return True

    def parse_show_call_screen(l):
        # Parse a name
        name, expression = _parse_screen_name(l)

        # Add pass between name and arguments if the name is an expression
        # so it works akin to "call expression 'label_name' pass (count=1)"
        if expression:
            l.keyword('pass')

        # Parse the list of arguments.
        arguments = renpy.parser.parse_arguments(l)

        predict = True
        transition_expr = None
        layer = None
        zorder = None
        tag = None

        while True:

            if l.keyword('nopredict'):
                predict = False

            elif l.keyword('with'):
                transition_expr = l.require(l.simple_expression)

            elif l.keyword("onlayer"):
                layer = l.require(l.name)

            elif l.keyword("zorder"):
                zorder = l.require(l.simple_expression)

            elif l.keyword("as"):
                tag = l.require(l.name)

            else:
                break

        l.expect_eol()

        return dict(
            name=name,
            arguments=arguments,
            predict=predict,
            transition_expr=transition_expr,
            layer=layer,
            zorder=zorder,
            tag=tag,
            expression=expression
        )

    def parse_hide_screen(l):
        # Parse a name
        name, expression = _parse_screen_name(l)

        transition_expr = None
        layer = None

        while True:
            if l.keyword('with'):
                transition_expr = l.require(l.simple_expression)

            elif l.keyword("onlayer"):
                layer = l.require(l.name)

            else:
                break

        l.expect_eol()

        return dict(name=name, transition_expr=transition_expr, layer=layer, expression=expression)

    def predict_screen(p):

        if not config.predict_screen_statements:
            return

        predict = p.get("predict", False)

        if not predict:
            return

        try:
            name = _get_screen_name(p)
        except Exception:
            return

        a = p["arguments"]

        if a is not None:
            args, kwargs = a.evaluate()
        else:
            args = [ ]
            kwargs = { }

        screen_props = _get_screen_props(p)
        kwargs.update(screen_props)

        renpy.predict_screen(name, *args, **kwargs)

    def execute_show_screen(p):

        name = _get_screen_name(p)
        a = p["arguments"]

        if a is not None:
            args, kwargs = a.evaluate()
        else:
            args = [ ]
            kwargs = { }

        screen_props = _get_screen_props(p)
        kwargs.update(screen_props)

        transition_expr = p.get("transition_expr", None)
        if transition_expr is not None:
            renpy.with_statement(None)

        renpy.show_screen(name, *args, **kwargs)

        if transition_expr is not None:
            renpy.with_statement(eval(transition_expr))

    def execute_call_screen(p):

        name = _get_screen_name(p)
        a = p["arguments"]

        transition_expr = p.get("transition_expr", None)

        if transition_expr is not None:
            renpy.transition(eval(transition_expr))

        if a is not None:
            args, kwargs = a.evaluate()
        else:
            args = [ ]
            kwargs = { }

        screen_props = _get_screen_props(p)
        kwargs.update(screen_props)

        store._return = renpy.call_screen(name, *args, **kwargs)

    def execute_hide_screen(p):
        name = _get_screen_name(p)

        transition_expr = p.get("transition_expr", None)
        if transition_expr is not None:
            renpy.with_statement(None)

        layer = p.get("layer", None)

        renpy.hide_screen(name, layer=layer)

        if transition_expr is not None:
            renpy.with_statement(eval(transition_expr))


    def lint_show_call_screen(p):
        is_expression = p.get("expression", False)

        name = p["name"]
        if not is_expression and not renpy.has_screen(name):
            renpy.error("Screen %s does not exist." % name)

        layer = p.get("layer", None)
        if (
            layer is not None
            and layer not in renpy.display.scenelists.layers
        ):
            renpy.error("Screen is being shown on unknown layer %s." % layer)

    def lint_hide_screen(p):
        layer = p.get("layer", None)
        if (
            layer is not None
            and layer not in renpy.display.scenelists.layers
        ):
            renpy.error("Screen is being hidden on unknown layer %s." % layer)


    renpy.register_statement("show screen",
                              parse=parse_show_call_screen,
                              execute=execute_show_screen,
                              predict=predict_screen,
                              lint=lint_show_call_screen,
                              warp=warp_true)

    renpy.register_statement("call screen",
                              parse=parse_show_call_screen,
                              execute=execute_call_screen,
                              predict=predict_screen,
                              lint=lint_show_call_screen,
                              force_begin_rollback=True)

    renpy.register_statement("hide screen",
                              parse=parse_hide_screen,
                              execute=execute_hide_screen,
                              lint=lint_hide_screen,
                              warp=warp_true)
