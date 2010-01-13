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

# Should the in-game window be shown?
_window = False

# The window subtitle.
_window_subtitle = ''

# Should rollback be allowed?
_rollback = True

# config.
_config = renpy.config

# The special character used for name-only dialogue.
name_only = None

class _Config(object):

    def register(self, name, default, cat=None, help=None):
        setattr(self, name, default)
        _config.help.append((cat, name, help))

    def __getattr__(self, name):
        cvars = vars(_config)

        if name not in cvars:
            raise Exception('config.%s is not a known configuration variable.' % (name))

        return cvars[name]

    def __setattr__(self, name, value):
        cvars = vars(_config)

        if name not in cvars and renpy.config.locked:
            raise Exception('config.%s is not a known configuration variable.' % (name))

        if name == "script_version":
            renpy.store._set_script_version(value) # E1101
        
        cvars[name] = value

    def __delattr__(self, name):
        if renpy.config.locked:
            raise Exception('Deleting configuration variables is not supported.')
        else:
            delattr(renpy.config, name)

# The styles object.
style = None
            
config = _Config()
library = config

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
from renpy.python import revertable_sorted as sorted

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

Transform = renpy.display.motion.Transform

Animation = anim.Animation
Movie = renpy.display.video.Movie
Particles = renpy.display.particle.Particles
SnowBlossom = renpy.display.particle.SnowBlossom

Text = renpy.display.text.Text
ParameterizedText = renpy.display.text.ParameterizedText

# Currying things.
Alpha = renpy.curry.curry(renpy.display.layout.Alpha)
Position = renpy.curry.curry(renpy.display.layout.Position)
Pan = renpy.curry.curry(renpy.display.motion.Pan)
Move = renpy.curry.curry(renpy.display.motion.Move)
Motion = renpy.curry.curry(renpy.display.motion.Motion)
Revolve = renpy.curry.curry(renpy.display.motion.Revolve)
Zoom = renpy.curry.curry(renpy.display.motion.Zoom)
RotoZoom = renpy.curry.curry(renpy.display.motion.RotoZoom)
FactorZoom = renpy.curry.curry(renpy.display.motion.FactorZoom)
SizeZoom = renpy.curry.curry(renpy.display.motion.SizeZoom)
Fade = renpy.curry.curry(renpy.display.transition.Fade)
Dissolve = renpy.curry.curry(renpy.display.transition.Dissolve)
ImageDissolve = renpy.curry.curry(renpy.display.transition.ImageDissolve)
CropMove = renpy.curry.curry(renpy.display.transition.CropMove)
Pixellate = renpy.curry.curry(renpy.display.transition.Pixellate)
MoveTransition = renpy.curry.curry(renpy.display.transition.MoveTransition)
MoveFactory = renpy.curry.curry(renpy.display.transition.MoveFactory)
MoveIn = renpy.curry.curry(renpy.display.transition.MoveIn)
MoveOut = renpy.curry.curry(renpy.display.transition.MoveOut)
ZoomInOut = renpy.curry.curry(renpy.display.transition.ZoomInOut)
RevolveInOut = renpy.curry.curry(renpy.display.transition.RevolveInOut)
MultipleTransition = renpy.curry.curry(renpy.display.transition.MultipleTransition)
ComposeTransition = renpy.curry.curry(renpy.display.transition.ComposeTransition)
Pause = renpy.curry.curry(renpy.display.transition.NoTransition)
SubTransition = renpy.curry.curry(renpy.display.transition.SubTransition)

# Misc.
ADVSpeaker = ADVCharacter = renpy.character.ADVCharacter
Speaker = Character = renpy.character.Character
DynamicCharacter = renpy.character.DynamicCharacter
MultiPersistent = renpy.loadsave.MultiPersistent

Style = renpy.style.Style

absolute = renpy.display.core.absolute

def layout(cls, doc, nargs=0, **extra_kwargs):

    def f(*args, **properties):

        conargs = args[:nargs]
        kids = args[nargs:]
        
        kwargs = extra_kwargs.copy()
        kwargs.update(properties)

        rv = cls(*conargs, **kwargs)
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
mouse_visible = True

# Is the overlay suppressed?
suppress_overlay = False

# The default ADVCharacter.
adv = ADVCharacter(None,
                   who_prefix='',
                   who_suffix='',
                   what_prefix='',
                   what_suffix='',

                   show_function=renpy.show_display_say,
                   predict_function=renpy.predict_show_display_say,

                   condition=None,
                   dynamic=False,
                   image=False,

                   interact=True,
                   slow=True,
                   slow_abortable=True,
                   afm=True,
                   ctc=None,
                   ctc_pause=None,
                   ctc_timedpause=None,
                   ctc_position="nestled",
                   all_at_once=False,
                   with_none=None,
                   callback=None,
                   type='say',

                   who_style='say_label',
                   what_style='say_dialogue',
                   window_style='say_window',

                   kind=False)

def predict_say(who, what):
    who = Character(who, kind=name_only)
    try:
        return who.predict(what)
    except:
        return [ ]
    
def say(who, what, interact=True):
    who = Character(who, kind=name_only)
    who(what, interact=interact)

# Used by renpy.reshow_say.
_last_say_who = None
_last_say_what = None

# Used to store the things pinned into the cache.
_cache_pin_set = set()
    
__name__ = 'store'

import sys
sys.modules['store'] = sys.modules['renpy.store']

def public_api():
    ui
    im
    object
    range
    sorted
    
del public_api
