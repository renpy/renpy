# This is the Ren'Py store. It's the module in which the user code
# is executed.

# But please note that this will not be available in the body
# of user code, unless we re-import it.
import renpy

import renpy.ui as ui
import renpy.display.im as im
import renpy.display.anim as anim
import renpy.display.audio as audio

from renpy.python import RevertableList as __renpy__list__
list = __renpy__list__

from renpy.python import RevertableDict as __renpy__dict__
dict = __renpy__dict__

from renpy.python import RevertableObject as object

# Set up symbols.

config = renpy.config
Image = renpy.display.image.Image
Solid = renpy.display.image.Solid
Frame = renpy.display.image.Frame
Null = renpy.display.layout.Null
# Animation = renpy.display.image.Animation
Animation = anim.Animation
Movie = renpy.display.video.Movie

Position = renpy.curry.curry(renpy.display.layout.Position)
Pan = renpy.curry.curry(renpy.display.layout.Pan)
Move = renpy.curry.curry(renpy.display.layout.Move)
Motion = renpy.curry.curry(renpy.display.layout.Motion)
Fade = renpy.curry.curry(renpy.display.transition.Fade)
Dissolve = renpy.curry.curry(renpy.display.transition.Dissolve)
CropMove = renpy.curry.curry(renpy.display.transition.CropMove)
Pixellate = renpy.curry.curry(renpy.display.transition.Pixellate)
MoveTransition = renpy.curry.curry(renpy.display.transition.MoveTransition)

def _return(v):
    """
    Returns its input. This is pretty useless, but comes in handy
    when curried.
    """
    
    return v

_return = renpy.curry.curry(_return)

# Note that this is really a RevertableObject.

class Character(object):
    """
    The character object contains information about a character. When
    passed as the first argument to a say statement, it can control
    the name that is displayed to the user, and the style of the label
    showing the name, the text of the dialogue, and the window
    containing both the label and the dialogue.
    """

    import renpy.config as config

    def __init__(self, name,
                 who_style='say_label',
                 what_style='say_dialogue',
                 window_style='say_window',
                 function = renpy.exports.display_say,
                 condition=None,
                 dynamic=False,
                 **properties):
        """
        @param name: The name of the character, as shown to the user.

        @param who_style: The name of the style that is applied to the
        characters name when it is shown to the user.

        @param what_style: The name of the style that is applied to
        the body of the character's dialogue, when it is shown to the
        user.

        @param window_style: The name of the style of the window
        containing all the dialogue.

        @param who_prefix: A prefix that is prepended to the name.
     
        @param who_suffix: A suffix that is appended to the name. (Defaults to ':')

        @param what_prefix: A prefix that is prepended to the text body.

        @param what_suffix: A suffix that is appended to the text body.

        @param function: The function that is called to actually display
        this dialogue. This should either be renpy.display_say, or a function
        with the same signature as it.

        @param condition: A string containing a python expression, or
        None. If not None, the condition is evaluated when each line
        of dialogue is said. If it evaluates to False, the dialogue is
        not shown to the user.

        @param interact: If True (the default), then each line said
        through this character causes an interaction. If False, then
        the window is added to the screen, but control immediately
        proceeds. You'll need to call ui.interact yourself to show it.

        @param properties: Additional style properties, that are
        applied to the label containing the character's name.

        @param dynamic: If true, the name is interpreted as a python
        expression, which is evaluated to get the name that will be
        used by the rest of the code.

        @param image: If true, the name is considered to be the name
        of an image, which is rendered in place of the who label.
        """
        
        self.name = name
        self.who_style = who_style
        self.what_style = what_style
        self.window_style = window_style
        self.properties = properties
        self.function = function
        self.condition = condition
        self.dynamic = dynamic

    def check_condition(self):
        """
        Returns true if we should show this line of dialogue.
        """

        if self.condition is None:
            return True

        import renpy.python as python

        return python.py_eval(self.condition)
        

    def store_readback(self, who, what):
        """
        This is called when a say occurs, to store the information
        about what is said into the readback buffers.
        """

        return

    def __call__(self, what, interact=True):

        if not self.check_condition():
            return

        name = self.name

        if self.dynamic:
            import renpy.python as python            
            name = python.py_eval(name)

        self.store_readback(name, what)
        
        self.function(name, what,
                      who_style=self.who_style,
                      what_style=self.what_style,
                      window_style=self.window_style,
                      interact=interact,
                      **self.properties)

def DynamicCharacter(name_expr, **properties):
    """
    A DynamicCharacter is similar to a Character, except that instead
    of having a fixed name, it has an expression that is evaluated to
    produce a name before each line of dialogue is displayed. This allows
    one to have a character with a name that is read from the user, as
    may be the case for the POV character.

    This is now exactly the same as constructing a character with
    dynamic=True.
    """

    return Character(name_expr, dynamic=True, **properties)

# The color function. (Moved, since text needs it, too.)
color = renpy.display.text.color

# Conveniently get rid of all the packages we had imported before.
import renpy.exports as renpy

# The default narrator.
def narrator(what, interact=True):
    renpy.display_say(None, what, what_style='say_thought', interact=interact)

# The default menu function.
menu = renpy.display_menu

# The function that is called when anonymous text is said.
def say(who, what):
    renpy.display_say(who, what)

# The default transition.
default_transition = None

_globals = globals().copy()

def reload():
    globals().update(_globals)
