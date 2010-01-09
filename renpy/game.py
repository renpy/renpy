# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
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

# This module is intended to be used as a singleton object.
# It's purpose is to store in one global all of the data that would
# be to annoying to lug around otherwise. 
#
# Many modules will probablt want to import this using a command like:
#
# import renpy.game as game
#
# These modules will then be able to access the various globals defined
# in this module as fields on game.

import renpy

# The basepath.
basepath = None

# A list of paths that we search to load things. This is searched for
# everything that can be loaded, before archives are used.
searchpath = [ ]

# The options that were read off the command line.
options = None

# The game's script.
script = None

# A shallow copy of the store dictionary made at the end of the init
# phase. If a key in here points to the same value here as it does in
# the store, it is not saved.
clean_store = None

# A stack of execution contexts.
contexts = [ ]

# The interface that the game uses to interact with the user.
interface = None

# Are we still running init blocks?
init_phase = True

# Are we inside lint?
lint = False

# The RollbackLog that keeps track of changes to the game state
# and to the store.
log = None

# Some useful additional information about program execution that
# can be added to the exception.
exception_info = ''

# Used to store style information.
style = None

# The set of statements we've seen in this session.
seen_session = { }

# The set of statements we've ever seen.
seen_ever = { }

# True if we're in the first interaction after a rollback or rollforward.
after_rollback = False

# Code that's run after the init code.
post_init = [ ]

# Should we attempt to run in a mode that uses less memory?
less_memory = False

# Should we attempt to run in a mode that minimizes the number
# of screen updates?
less_updates = False

# Should we never show the mouse?
less_mouse = False

# The class that's used to hold the persistent data.
class Persistent(object):

    def __setstate__(self, data):
        vars(self).update(data)

    def __getstate__(self):
        return vars(self)

    # Undefined attributes return None.
    def __getattr__(self, attr):
        return None
        
# The persistent data that's kept from session to session
persistent = None

class Preferences(object):
    """
    Stores preferences that will one day be persisted.
    """
    def reinit(self):
        self.fullscreen = False # W0201
        self.skip_unseen = False # W0201
        self.text_cps = 0 # W0201
        self.afm_time = 0 # W0201
        self.afm_enable = True # W0201
        
        
        # These will be going away soon.
        self.sound = True # W0201
        self.music = True # W0201


        # 2 - All transitions.
        # 1 - Only non-default transitions.
        # 0 - No transitions.
        self.transitions = 2 # W0201

        self.skip_after_choices = False # W0201

        # Mixer channel info.
        self.volumes = { } # W0201
        self.mute = { } # W0201

        # Joystick mappings.
        self.joymap = dict( # W0201
            joy_left="Axis 0.0 Negative",
            joy_right="Axis 0.0 Positive",
            joy_up="Axis 0.1 Negative",
            joy_down="Axis 0.1 Positive",
            joy_dismiss="Button 0.0")

    def set_volume(self, mixer, volume):
        if volume == 0:
            self.mute[mixer] = True
        else:
            self.mute[mixer] = False

        self.volumes[mixer] = volume

    def get_volume(self, mixer):
        return self.volumes[mixer]
        
    def __setstate__(self, state):
        self.reinit()
        vars(self).update(state)

    def __init__(self):
        self.reinit()

# The current preferences.
preferences = None

class RestartException(Exception):
    """
    This class will be used to convey to the system that the context has
    been changed, and therefore execution needs to be restarted.
    """

    def __init__(self, contexts, label): # W0231
        self.contexts = contexts
        self.label = label
    
class FullRestartException(Exception):
    """
    An exception of this type forces a hard restart, completely
    destroying the store and config and so on.
    """

    def __init__(self, reason="end_game"): # W0231
        self.reason = reason

    
class UtterRestartException(Exception):
    """
    An exception of this type forces an even harder restart, causing
    Ren'Py and the script to be reloaded.
    """

class QuitException(Exception):
    """
    An exception of this class will let us force a safe quit, from
    anywhere in the program. Do not pass go, do not collect $200.
    """

class JumpException(Exception):
    """
    This should be raised with a label as the only argument. This causes
    the current statement to terminate, and execution to be transferred
    to the named label.
    """

class JumpOutException(Exception):
    """
    This should be raised with a label as the only argument. This exits
    the current context, and then raises a JumpException.
    """

class ParseErrorException(Exception):
    """
    This is raised when a parse error occurs, after it has been
    reported to the user.
    """
    
def context(index=-1):
    """
    Return the current execution context, or the context at the
    given index if one is specified.
    """

    return contexts[index]

def invoke_in_new_context(callable, *args, **kwargs):
    """
    This pushes the current context, and invokes the given python
    function in a new context. When that function returns or raises an
    exception, it removes the new context, and restores the current
    context.

    Additional arguments and keyword arguments are passed to the
    callable.

    Please note that the context so created cannot execute renpy
    code. So exceptions that change the flow of renpy code (like
    the one created by renpy.jump) cause this context to terminate,
    and are handled by the next higher context.

    If you want to execute renpy code from the function, you can call
    it with renpy.call_in_new_context.

    Use this to begin a second interaction with the user while
    inside an interaction.
    """

    context = renpy.execution.Context(False, contexts[-1])
    contexts.append(context)

    try:
        return callable(*args, **kwargs)
    finally:
        contexts.pop()

        if interface.restart_interaction:
            contexts[-1].scene_lists.focused = None

        
def call_in_new_context(label, *args, **kwargs):
    """
    This code creates a new context, and starts executing code from
    that label in the new context. Rollback is disabled in the
    new context. (Actually, it will just bring you back to the
    real context.)

    Use this to begin a second interaction with the user while
    inside an interaction.
    """

    context = renpy.execution.Context(False, contexts[-1])
    contexts.append(context)

    
    if args:
        renpy.store._args = args
    else:
        renpy.store._args = None

    if kwargs:    
        renpy.store._kwargs = renpy.python.RevertableDict(kwargs)
    else:
        renpy.store._kwargs = None
    
    try:
            
        context.goto_label(label)
        context.run()

        rv = renpy.store._return        
        context.pop_all_dynamic()
        contexts.pop()

        return rv
        
    except renpy.game.JumpOutException, e:        

        context.pop_all_dynamic()
        contexts.pop()
        raise renpy.game.JumpException(e.args[0])

    finally:
        if interface.restart_interaction:
            contexts[-1].scene_lists.focused = None
    
        
