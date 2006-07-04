# This is the Ren'Py store. It's the module in which the user code
# is executed.

# But please note that this will not be available in the body
# of user code, unless we re-import it.
import renpy

import renpy.ui as ui
import renpy.display.im as im
import renpy.display.anim as anim

# config.
_config = renpy.config

class _Config(object):

    def __getattr__(self, name):
        cvars = vars(_config)

        if name not in cvars:
            raise Exception('config.%s is not a known configuration variable.' % name)

        return cvars[name]

    def __setattr__(self, name, value):
        cvars = vars(_config)

        if name not in cvars:
            raise Exception('config.%s is not a known configuration variable.' % name)

        cvars[name] = value

    def __delattr__(self, name):
        raise Exception('Deleting configuration variables is not supported.')
        
config = _Config()

_list = list
_dict = dict
_object = object

from renpy.python import RevertableList as __renpy__list__
list = __renpy__list__

from renpy.python import RevertableDict as __renpy__dict__
dict = __renpy__dict__

from renpy.python import RevertableSet as set
Set = set
from renpy.python import RevertableObject as object


# Set up symbols.
Image = renpy.display.image.Image
ImageReference = renpy.display.image.ImageReference
Solid = renpy.display.image.Solid
Frame = renpy.display.image.Frame
Null = renpy.display.layout.Null
LiveComposite = renpy.display.layout.LiveComposite
# Animation = renpy.display.image.Animation
Animation = anim.Animation
Movie = renpy.display.video.Movie
Particles = renpy.display.particle.Particles
SnowBlossom = renpy.display.particle.SnowBlossom
DynamicDisplayable = renpy.display.layout.DynamicDisplayable
Text = renpy.display.text.Text
ParameterizedText = renpy.display.text.ParameterizedText

Position = renpy.curry.curry(renpy.display.layout.Position)
Pan = renpy.curry.curry(renpy.display.layout.Pan)
Move = renpy.curry.curry(renpy.display.layout.Move)
Motion = renpy.curry.curry(renpy.display.layout.Motion)
Zoom = renpy.curry.curry(renpy.display.layout.Zoom)
Fade = renpy.curry.curry(renpy.display.transition.Fade)
Dissolve = renpy.curry.curry(renpy.display.transition.Dissolve)
ImageDissolve = renpy.curry.curry(renpy.display.transition.ImageDissolve)
CropMove = renpy.curry.curry(renpy.display.transition.CropMove)
Pixellate = renpy.curry.curry(renpy.display.transition.Pixellate)
MoveTransition = renpy.curry.curry(renpy.display.transition.MoveTransition)

def layout(cls, doc, **extra_kwargs):

    def f(*args, **properties):
        kwargs = extra_kwargs.copy()
        kwargs.update(properties)

        rv = cls(**kwargs)
        for i in args:
            rv.add(Image(i, loose=True))

        return rv

    f.__doc__ = doc + """

    This function takes both positional and keyword
    arguments. Positional arguments should be displayables or images
    to be laid out. Keyword arguments are interpreted as style properties,
    except for the style keyword argument, which is the name of the parent
    style of this layout.
    """

    return f

Fixed = layout(renpy.display.layout.Fixed, """
A layout that expands to take the size allotted to it.  Each
displayable is allocated the entire size of the layout, with the first
displayable further from the user than the second, and so on. Within
""")

HBox = layout(renpy.display.layout.MultiBox, """
A layout that lays out displayables from left to right.
""", layout='horizontal')

VBox = layout(renpy.display.layout.MultiBox, """
A layout that lays out displayables from top to bottom.
""", layout='vertical')

del layout
        

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

    # Properties beginning with what or window that are treated
    # specially.
    special_properties = [
        'what_prefix',
        'what_suffix',
        'show_function',
        ]
    
    def __init__(self, name,
                 who_style='say_label',
                 what_style='say_dialogue',
                 window_style='say_window',
                 function=renpy.exports.display_say,
                 predict_function=renpy.exports.predict_display_say, 
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

        @param show_function: A function that is called to show each
        step of this dialogue to the user. It should have the same
        signature as renpy.show_display_say.
        
        @param predict_function: The function that is called to
        predict the images from this dialogue. It is called with the
        same signature as display_say (although some of the
        parameters, such as what, may be inaccurate), and is expected
        to return a list of displayables that should be loaded.

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

        @param ctc: If present, this is interpreted as a widget that
        is displayed when all text is shown to the user, prompting the
        user to click to continue. Animation or anim.Blink is a good
        choice for this sort of widget, as is Image.

        @param ctc_position: If "nestled", the ctc widget is
        displayed nestled in with the end of the text. If
        "fixed", the ctc widget is displayed directly on the screen,
        with its various position properties determining where it is
        actually shown.

        @param interact: If True, the default, an interaction will
        take place when the character speaks. Otherwise, no such
        interaction will take place.

        In addition, Character objects also take properties. If a
        property is prefixed with window_, it is applied to the
        window. If prefixed with what_, it is applied to the text
        being spoken. If prefixed with show_, properties are passed as keyword arguments
        to the show_ and predict_ functions. Unprefixed properties are applied to the who
        label, the name of the character speaking.
        """
        
        self.name = name
        self.who_style = who_style
        self.what_style = what_style
        self.window_style = window_style
        self.properties = properties
        self.what_properties = { }
        self.window_properties = { }
        self.show_args = { }
        self.function = function
        self.predict_function = predict_function
        self.condition = condition
        self.dynamic = dynamic

        for k in list(self.properties):
            if k in self.special_properties:
                continue

            if k.startswith("show_"):
                self.show_args[k[len("show_"):]] = self.properties[k]
                del self.properties[k]
                continue

            if k.startswith("what_"):
                self.what_properties[k[len("what_"):]] = self.properties[k]
                del self.properties[k]
                continue

            if k.startswith("window_"):
                self.window_properties[k[len("window_"):]] = self.properties[k]
                del self.properties[k]
                continue
                

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

    def __call__(self, what, **properties):

        props = self.properties.copy()
        props.update(properties)

        if not self.check_condition():
            return

        name = self.name

        if self.dynamic:
            import renpy.python as python            
            name = python.py_eval(name)

        self.function(name, what,
                      who_style=self.who_style,
                      what_style=self.what_style,
                      window_style=self.window_style,
                      what_properties=self.what_properties,
                      window_properties=self.window_properties,
                      show_args=self.show_args,
                      **props)

        self.store_readback(name, what)
        
    def predict(self, what):

        if self.dynamic and self.image:
            return [ ]

        if self.dynamic:
            name = "<Dynamic>"
        else:
            name = self.name

        return self.predict_function(
            name,
            what,
            who_style=self.who_style,
            what_style=self.what_style,
            window_style=self.window_style,
            what_properties=self.what_properties,
            window_properties=self.window_properties,
            show_args=self.show_args,
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

# The default menu functions.
menu = renpy.display_menu
predict_menu = renpy.predict_menu

# The function that is called when anonymous text is said.
def say(who, what, interact=True):
    renpy.display_say(who, what, interact=True)

def predict_say(who, what):
    return renpy.predict_display_say(who, what)

# The default transition.
default_transition = None

_globals = globals().copy()

def reload():
    globals().update(_globals)
