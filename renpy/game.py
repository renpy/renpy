# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
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

import renpy.display

# The basepath.
basepath = None

# A list of paths that we search to load things. This is searched for
# everything that can be loaded, before archives are used.
searchpath = [ ]

# The options that were read off the command line.
args = None

# The game's script.
script = None

# A stack of execution contexts.
contexts = [ ]

# The interface that the game uses to interact with the user.
interface = None

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

# Should we not imagedissiolve?
less_imagedissolve = False

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
persistent = Persistent()

class Preferences(renpy.object.Object):
    """
    Stores preferences that will one day be persisted.
    """
    __version__ = 4

    def after_upgrade(self, version):
        if version < 1:
            self.mute_volumes = 0
        if version < 2:
            self.using_afm_enable = False
        if version < 3:
            self.physical_size = None
        if version < 4:
            self.renderer = "auto"
            self.performance_test = True
            
    def __init__(self):
        self.fullscreen = False 
        self.skip_unseen = False
        self.text_cps = 0
        self.afm_time = 0
        self.afm_enable = True
        
        # These will be going away soon.
        self.sound = True
        self.music = True

        # 2 - All transitions.
        # 1 - Only non-default transitions.
        # 0 - No transitions.
        self.transitions = 2

        self.skip_after_choices = False

        # Mixer channel info.

        # A map from channel name to the current volume (between 0 and 1).
        self.volumes = { }

        # True if the channel should not play music. False
        # otherwise. (Not used anymore.)
        self.mute = { }

        # Joystick mappings.
        self.joymap = dict(
            joy_left="Axis 0.0 Negative",
            joy_right="Axis 0.0 Positive",
            joy_up="Axis 0.1 Negative",
            joy_down="Axis 0.1 Positive",
            joy_dismiss="Button 0.0")
        
        # The size of the window, or None if we don't know it yet.
        self.physical_size = None
        
        # The graphics renderer we use.
        self.renderer = "auto"
        
        # Should we do a performance test on startup?
        self.performance_test = True
        
    def set_volume(self, mixer, volume):
        self.volumes[mixer] = volume

    def get_volume(self, mixer):
        return self.volumes.get(mixer, 0)
        
    def set_mute(self, mixer, mute):
        self.mute[mixer] = mute

    def get_mute(self, mixer):
        return self.mute[mixer]
    
# The current preferences.
preferences = Preferences()

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
    anywhere in the program.
    
    `relaunch`
        If given, the program will run another copy of itself, with the
        same arguments.
    """

    def __init__(self, relaunch=False):
        Exception.__init__(self)
        self.relaunch = relaunch

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

class CallException(Exception):
    """
    Raise this exception to cause the current statement to terminate, 
    and control to be transferred to the named label.
    """

    def __init__(self, label, args, kwargs):
        Exception.__init__(self)
        
        self.label = label
        self.args = args
        self.kwargs = kwargs

class ParseErrorException(Exception):
    """
    This is raised when a parse error occurs, after it has been
    reported to the user.
    """

# A tuple of exceptions that should not be caught by the 
# exception reporting mechanism.
CONTROL_EXCEPTIONS = (
    RestartException,
    FullRestartException,
    UtterRestartException,
    QuitException,
    JumpException,
    JumpOutException,
    CallException,
    ParseErrorException,
    KeyboardInterrupt,
    )

    
def context(index=-1):
    """
    Return the current execution context, or the context at the
    given index if one is specified.
    """

    return contexts[index]

def invoke_in_new_context(callable, *args, **kwargs): #@ReservedAssignment
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

    context = renpy.execution.Context(False, contexts[-1], clear=True)
    contexts.append(context)

    try:
        return callable(*args, **kwargs)
    finally:
        contexts.pop()

        if interface.restart_interaction and contexts:
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

    context = renpy.execution.Context(False, contexts[-1], clear=True)
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

        rv = renpy.store._return #@UndefinedVariable
        context.pop_all_dynamic()
        contexts.pop()

        return rv
        
    except renpy.game.JumpOutException, e:        

        context.pop_all_dynamic()
        contexts.pop()
        raise renpy.game.JumpException(e.args[0])

    finally:
        if interface.restart_interaction and contexts:
            contexts[-1].scene_lists.focused = None
    
# Type information.       
if False:
    script = renpy.script.Script()
    interface = renpy.display.core.Interface()
    log = renpy.python.RollbackLog()
