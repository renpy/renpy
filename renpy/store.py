# This is the Ren'Py store. It's the module in which the user code
# is executed.

# But please note that this will not be available in the body
# of user code, unless we re-import it.
import renpy

import renpy.ui as ui

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
Animation = renpy.display.image.Animation
Movie = renpy.display.video.Movie

Position = renpy.curry.curry(renpy.display.layout.Position)
Pan = renpy.curry.curry(renpy.display.layout.Pan)
Move = renpy.curry.curry(renpy.display.layout.Move)
Fade = renpy.curry.curry(renpy.display.transition.Fade)
Dissolve = renpy.curry.curry(renpy.display.transition.Dissolve)
CropMove = renpy.curry.curry(renpy.display.transition.CropMove)

def _return(v):
    """
    Returns its input. This is pretty useless, but comes in handy
    when curried.
    """
    
    return v

_return = renpy.curry.curry(_return)

# Note that this is really a RevertableObject.
# TODO: Move this someplace saner. Like perhaps to .exports. But
# be sure to change the base class after the move!

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

        @param properties: Additional style properties, that are
        applied to the label containing the character's name.

        In addition to the parameters given above, there are also a
        few other keyword parameters:

        @param who_prefix: A prefix that is prepended to the name.
     
        @param who_suffix: A suffix that is appended to the name. (Defaults to ':')

        @param what_prefix: A prefix that is prepended to the text body.

        @param what_suffix: A suffix that is appended to the text body.

        @param interact: If True (the default), then each line said
        through this character causes an interaction. If False, then
        the window is added to the screen, but control immediately
        proceeds. You'll need to call ui.interact yourself to show it.
        """
        
        self.name = name
        self.who_style = who_style
        self.what_style = what_style
        self.window_style = window_style
        self.properties = properties

    def __call__(self, what):
        renpy.display_say(self.name, what,
                          who_style=self.who_style,
                          what_style=self.what_style,
                          window_style=self.window_style,
                          **self.properties)

class DynamicCharacter(object):
    """
    A DynamicCharacter is similar to a Character, except that instead
    of having a fixed name, it has an expression that is evaluated to
    produce a name before each line of dialogue is displayed. This allows
    one to have a character with a name that is read from the user, as
    may be the case for the POV character.
    """

    import renpy.config as config

    def __init__(self, name_expr,
                 who_style='say_label',
                 what_style='say_dialogue',
                 window_style='say_window',
                 **properties):
        """
        @param name_expr: An expression that, when evaluated, should yield
        the name of the character, as a string. 

        All other parameters are as for Character.
        """
        
        self.name_expr = name_expr
        self.who_style = who_style
        self.what_style = what_style
        self.window_style = window_style
        self.properties = properties

    def __call__(self, what):
        import renpy.python as python

        renpy.display_say(python.py_eval(self.name_expr),
                          what,
                          who_style=self.who_style,
                          what_style=self.what_style,
                          window_style=self.window_style,
                          **self.properties)

# Conveniently get rid of all the packages we had imported before.
import renpy.exports as renpy

def narrator(what):
    renpy.display_say(None, what, what_style='say_thought')

menu = renpy.display_menu

def color(s):
    """
    This function converts a hexcode into a color/alpha tuple. Leading
    # marks are ignored. Colors can be rgb or rgba, with each element having
    either one or two digits. (So the strings can be 3, 4, 6, or 8 digits long,
    not including the optional #.) A missing alpha is interpreted as 255,
    fully opaque.

    For example, color('#123a') returns (17, 34, 51, 170), while
    color('c0c0c0') returns (192, 192, 192, 255).
    """

    if s[0] == '#':
        s = s[1:]

    if len(s) == 6:
        r = int(s[0]+s[1], 16)
        g = int(s[2]+s[3], 16)
        b = int(s[4]+s[5], 16)
        a = 255
    elif len(s) == 8:
        r = int(s[0]+s[1], 16)
        g = int(s[2]+s[3], 16)
        b = int(s[4]+s[5], 16)
        a = int(s[6]+s[7], 16)
    elif len(s) == 3:
        r = int(s[0], 16) * 0x11
        g = int(s[1], 16) * 0x11
        b = int(s[2], 16) * 0x11
        a = 255
    elif len(s) == 4:
        r = int(s[0], 16) * 0x11
        g = int(s[1], 16) * 0x11
        b = int(s[2], 16) * 0x11
        a = int(s[3], 16) * 0x11
    else:
        raise Exception("Argument to color() must be 3, 4, 6, or 8 hex digits long.")

    return (r, g, b, a)

# The default transition.
default_transition = None

_globals = globals().copy()

def reload():
    globals().update(_globals)
