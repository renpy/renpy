# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
# See LICENSE.txt for license details.

# This file contains code that creates a few new statements. We'll
# also describe here the API for defining your own statements.
#
# Statements can be defined by calling renpy.statements.register. This
# function takes a string giving the keywords at the start of the
# statement, and then up to 4 functions defining the behavior of the
# statement: parse, execute, predict, and lint
#
# The parse function takes a lexer object as an argument, and is
# expected to return some parser data. The lexer has the following
# methods.
#
# l.eol() - True if we are at the end of the line.
# l.match(re) - Matches an arbitrary regexp string.
# l.keyword(s) - Matches s.
# l.name() - Matches any non-keyword name. Note that this only
# counts built-in keywords.
# l.word() - Matches any word, period.
# l.string() - Matches a renpy string.
# l.integer() - Matches an integer, returns a string containing the
# integer.
# l.float() - Matches a floating point number.
# l.simple_expression() - Matches a simple python expression, returns
# it as a string.
# l.rest() - Skips whitespace, then returns the rest of the line.
# l.checkpoint() - Returns an opaque object representing the current
# point in the parse.
# l.revert(o) - Given the object returned by l.checkpoint(), returns
# there.
#
# The parse function is expected to return an object, which is passed
# to the other functions. Parse should call renpy.error with the error
# message to report an error.
#
# The execute function is passed the object returned from parse, and
# is expected to execute the statement.
#
# The predict function is passed the object returned from parse, and
# is expected to return a list of images that are used by the
# statement.
#
# The lint function is called at lint time, after the init code is
# run. It should check the statement for errors, and report them by
# calling renpy.error with the appropriate error message.
#
# The scry function is called with a scry object. It may mutate that
# object, but it is then expected to return it. See 00nvlmode.rpy for
# details.
# 
# The next function is expected to return a string giving the label of
# the next statement to execute, or None to indicate that next
# statement in the block should be executed. The next function is
# called during predict, scry, and execute, and should always return
# the same value. (Or scrying may be incorrect.)


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
            channel = 7
        
        renpy.music.play(eval(p["file"]),
                         fadeout=eval(p["fadeout"]),
                         fadein=eval(p["fadein"]),
                         channel=channel,
                         loop=p.get("loop", None),
                         if_changed=p.get("if_changed", False))

    def predict_play_music(p):
        return [ ]

    def lint_play_music(p):

        file = _try_eval(p["file"], 'filename')
        if p["channel"] is not None:
            _try_eval(p["channel"], 'channel')

        if not isinstance(file, list):
            file = [ file ]

        for fn in file:
            if isinstance(fn, basestring) and not renpy.loadable(fn):
                renpy.error("%r is not loadable" % fn)
    
    renpy.statements.register('play music',
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
            channel = 7
        
        renpy.music.queue(
            eval(p["file"]),
            channel=channel,
            loop=p.get("loop", None))


    renpy.statements.register('queue music',
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
            channel = 7
        
        renpy.music.stop(fadeout=eval(p["fadeout"]), channel=channel)

    renpy.statements.register('stop music',
                              parse=parse_stop_music,
                              execute=execute_stop_music)


    # Sound statements. They share alot with the equivalent music
    # statements.

    def execute_play_sound(p):
        
        if p["channel"] is not None:
            channel = eval(p["channel"])
        else:
            channel = 0

        fadeout = eval(p["fadeout"]) or 0
            
        renpy.sound.play(eval(p["file"]),
                         fadeout=fadeout,
                         fadein=eval(p["fadein"]),
                         channel=channel)
                       
    renpy.statements.register('play sound',
                              parse=parse_play_music,
                              execute=execute_play_sound,
                              lint=lint_play_music)

    def execute_queue_sound(p):
        if p["channel"] is not None:
            channel = eval(p["channel"])
        else:
            channel = 0

        renpy.sound.queue(eval(p["file"]), channel=channel)


    renpy.statements.register('queue sound',
                              parse=parse_queue_music,
                              execute=execute_queue_sound,
                              lint=lint_play_music)

    def execute_stop_sound(p):
        if p["channel"] is not None:
            channel = eval(p["channel"])
        else:
            channel = 0

        fadeout = eval(p["fadeout"]) or 0

        renpy.sound.stop(fadeout=fadeout, channel=channel)

    renpy.statements.register('stop sound',
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

        lint_play_music(p)

    def lint_stop_generic(p):
        channel = eval(p["channel"])
        
        if not renpy.music.channel_defined(channel):
            renpy.error("channel %r is not defined" % channel)

    renpy.statements.register('play',
                              parse=parse_play_generic,
                              execute=execute_play_music,
                              predict=predict_play_music,
                              lint=lint_play_generic)
    
    renpy.statements.register('queue',
                              parse=parse_queue_generic,
                              execute=execute_queue_music,
                              lint=lint_play_generic)
            
    renpy.statements.register('stop',
                              parse=parse_stop_generic,
                              execute=execute_stop_music,
                              lint=lint_stop_generic)


    ##########################################################################
    # "window show" and "window hide" statements.

    def parse_window(l):
        p = l.simple_expression()
        if not l.eol():
            renpy.error('expected end of line')

        return p
            
    def lint_window(p):
        if p is not None:
            _try_eval(p, 'window transition')

    def execute_window_show(p):
        if store._window:
            return

        if p is not None:
            trans = eval(p)
        else:
            trans = config.window_show_transition
            
        renpy.with_statement(None)
        store._window = True
        renpy.with_statement(trans)
        
    def execute_window_hide(p):
        if not _window:
            return
        
        if p is not None:
            trans = eval(p)
        else:
            trans = config.window_hide_transition

        renpy.with_statement(None)
        store._window = False
        renpy.with_statement(trans)

    renpy.statements.register('window show',
                              parse=parse_window,
                              execute=execute_window_show,
                              lint=lint_window)

    renpy.statements.register('window hide',
                              parse=parse_window,
                              execute=execute_window_hide,
                              lint=lint_window)

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


    renpy.statements.register('pause',
                              parse=parse_pause,
                              lint=lint_pause,
                              execute=execute_pause)
            
    
                              
init -1200 python:

    config.window_show_transition = None
    config.window_hide_transition = None
    
    def _try_eval(e, what):
        try:
            return eval(e)
        except:
            renpy.error('unable to evaluate %s %r' % (what, e))
    
