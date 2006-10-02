# Copyright 2004-2006 PyTom <pytom@bishoujo.us>
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

# This is the Ren'Py store. It's the module in which the user code
# is executed.

# NOTE: This should not include any objects that will have fields
# changed by the user, as we only do a shallow copy.

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
Animation = anim.Animation
Movie = renpy.display.video.Movie
Particles = renpy.display.particle.Particles
SnowBlossom = renpy.display.particle.SnowBlossom
DynamicDisplayable = renpy.display.layout.DynamicDisplayable
Text = renpy.display.text.Text
ParameterizedText = renpy.display.text.ParameterizedText
MultiPersistent = renpy.loadsave.MultiPersistent

Position = renpy.curry.curry(renpy.display.layout.Position)
Pan = renpy.curry.curry(renpy.display.layout.Pan)
Move = renpy.curry.curry(renpy.display.layout.Move)
Motion = renpy.curry.curry(renpy.display.layout.Motion)
Zoom = renpy.curry.curry(renpy.display.layout.Zoom)
FactorZoom = renpy.curry.curry(renpy.display.layout.FactorZoom)
Fade = renpy.curry.curry(renpy.display.transition.Fade)
Dissolve = renpy.curry.curry(renpy.display.transition.Dissolve)
ImageDissolve = renpy.curry.curry(renpy.display.transition.ImageDissolve)
CropMove = renpy.curry.curry(renpy.display.transition.CropMove)
Pixellate = renpy.curry.curry(renpy.display.transition.Pixellate)
MoveTransition = renpy.curry.curry(renpy.display.transition.MoveTransition)
MultipleTransition = renpy.curry.curry(renpy.display.transition.MultipleTransition)
Pause = renpy.curry.curry(renpy.display.transition.NoTransition)


Character = renpy.character.Character
DynamicCharacter = renpy.character.DynamicCharacter

def layout(cls, doc, **extra_kwargs):

    def f(*args, **properties):
        kwargs = extra_kwargs.copy()
        kwargs.update(properties)

        rv = cls(**kwargs)
        for i in args:
            rv.add(renpy.easy.displayable(i))

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


# The color function. (Moved, since text needs it, too.)
color = renpy.easy.color

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

