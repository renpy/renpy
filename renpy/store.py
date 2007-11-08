# Copyright 2004-2007 PyTom <pytom@bishoujo.us>
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

# Used by the call/return mechanism.
_return = None
_args = None
_kwargs = None

# config.
_config = renpy.config

class _Config(object):

    def __init__(self, name):
        vars(self)["_name"] = name
    
    def __getattr__(self, name):
        cvars = vars(_config)

        if name not in cvars:
            raise Exception('%s.%s is not a known configuration variable.' % (self._name, name))

        return cvars[name]

    def __setattr__(self, name, value):
        cvars = vars(_config)

        if name not in cvars and renpy.config.locked:
            raise Exception('%s.%s is not a known configuration variable.' % (self._name, name))

        if name == "script_version":
            renpy.store._set_script_version(value)
        
        cvars[name] = value

    def __delattr__(self, name):
        if renpy.config.locked:
            raise Exception('Deleting configuration variables is not supported.')
        else:
            delattr(renpy.config, name)
        
config = _Config("config")
library = _Config("library")

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

from renpy.python import revertable_range as range

eval = renpy.python.py_eval

# Displayables.
Bar = renpy.display.behavior.Bar
Button = renpy.display.behavior.Button
Input = renpy.display.behavior.Input

Frame = renpy.display.image.Frame
Image = renpy.display.image.Image
ImageReference = renpy.display.image.ImageReference
Solid = renpy.display.image.Solid

LiveComposite = renpy.display.layout.LiveComposite
LiveCrop = renpy.display.layout.LiveCrop
Null = renpy.display.layout.Null
Window = renpy.display.layout.Window
Viewport = renpy.display.layout.Viewport
DynamicDisplayable = renpy.display.layout.DynamicDisplayable
ConditionSwitch = renpy.display.layout.ConditionSwitch
ShowingSwitch = renpy.display.layout.ShowingSwitch

Animation = anim.Animation
Movie = renpy.display.video.Movie
Particles = renpy.display.particle.Particles
SnowBlossom = renpy.display.particle.SnowBlossom

Text = renpy.display.text.Text
ParameterizedText = renpy.display.text.ParameterizedText

# Currying things.
Position = renpy.curry.curry(renpy.display.layout.Position)
Pan = renpy.curry.curry(renpy.display.layout.Pan)
Move = renpy.curry.curry(renpy.display.layout.Move)
Motion = renpy.curry.curry(renpy.display.layout.Motion)
Revolve = renpy.curry.curry(renpy.display.layout.Revolve)
Zoom = renpy.curry.curry(renpy.display.layout.Zoom)
RotoZoom = renpy.curry.curry(renpy.display.layout.RotoZoom)
FactorZoom = renpy.curry.curry(renpy.display.layout.FactorZoom)
Fade = renpy.curry.curry(renpy.display.transition.Fade)
Dissolve = renpy.curry.curry(renpy.display.transition.Dissolve)
ImageDissolve = renpy.curry.curry(renpy.display.transition.ImageDissolve)
CropMove = renpy.curry.curry(renpy.display.transition.CropMove)
Pixellate = renpy.curry.curry(renpy.display.transition.Pixellate)
MoveTransition = renpy.curry.curry(renpy.display.transition.MoveTransition)
MoveIn = renpy.curry.curry(renpy.display.transition.MoveIn)
MoveOut = renpy.curry.curry(renpy.display.transition.MoveOut)
ZoomInOut = renpy.curry.curry(renpy.display.transition.ZoomInOut)
RevolveInOut = renpy.curry.curry(renpy.display.transition.RevolveInOut)
MultipleTransition = renpy.curry.curry(renpy.display.transition.MultipleTransition)
ComposeTransition = renpy.curry.curry(renpy.display.transition.ComposeTransition)
Pause = renpy.curry.curry(renpy.display.transition.NoTransition)
SubTransition = renpy.curry.curry(renpy.display.transition.SubTransition)

# Misc.
ADVCharacter = renpy.character.ADVCharacter
Character = renpy.character.Character
DynamicCharacter = renpy.character.DynamicCharacter
MultiPersistent = renpy.loadsave.MultiPersistent

Style = renpy.style.Style


def layout(cls, doc, nargs=0, **extra_kwargs):

    def f(*args, **properties):

        conargs = args[:nargs]
        kids = args[nargs:]
        
        kwargs = extra_kwargs.copy()
        kwargs.update(properties)

        rv = cls(**kwargs)
        for i in kids:
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

Fixed = layout(renpy.display.layout.MultiBox, """
A layout that expands to take the size allotted to it.  Each
displayable is allocated the entire size of the layout, with the first
displayable further from the user than the second, and so on. Within
""", layout="fixed")

HBox = layout(renpy.display.layout.MultiBox, """
A layout that lays out displayables from left to right.
""", layout='horizontal')

VBox = layout(renpy.display.layout.MultiBox, """
A layout that lays out displayables from top to bottom.
""", layout='vertical')

Grid = layout(renpy.display.layout.Grid, """
A layout that lays out displayables in a grid.
""", nargs=2, layout='vertical')

del layout
        
def At(disp, *at_list):
    rv = renpy.easy.displayable(disp)

    for i in at_list:
        rv = i(rv)

    return rv


# The color function. (Moved, since text needs it, too.)
color = renpy.easy.color

# Conveniently get rid of all the packages we had imported before.
import renpy.exports as renpy

# The default menu functions.
menu = renpy.display_menu
predict_menu = renpy.predict_menu

# The default transition.
default_transition = None

# Is the mouse visible?
_mouse_visible = True

__name__ = 'store'
