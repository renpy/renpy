# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
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

from renpy.minstore import *

# But please note that this will not be available in the body
# of user code, unless we re-import it.
import renpy.display
import renpy.text

import renpy.display.im as im
import renpy.display.anim as anim

_restart = None

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

# Used by the ui functions.
_widget_by_id = None
_widget_properties = { }

class _Config(object):

    def __setstate__(self, data):
        return

    def register(self, name, default, cat=None, help=None): #@ReservedAssignment
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
            renpy.store._set_script_version(value) # E1101 @UndefinedVariable

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

eval = renpy.python.py_eval #@ReservedAssignment

# Displayables.
Bar = renpy.display.behavior.Bar
Button = renpy.display.behavior.Button
Input = renpy.display.behavior.Input

ImageReference = renpy.display.image.ImageReference
Image = renpy.display.im.image

Frame = renpy.display.imagelike.Frame
Solid = renpy.display.imagelike.Solid

LiveComposite = renpy.display.layout.LiveComposite
LiveCrop = renpy.display.layout.LiveCrop
LiveTile = renpy.display.layout.LiveTile
Flatten = renpy.display.layout.Flatten

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

Text = renpy.text.text.Text
ParameterizedText = renpy.text.extras.ParameterizedText
FontGroup = renpy.text.font.FontGroup

Drag = renpy.display.dragdrop.Drag
DragGroup = renpy.display.dragdrop.DragGroup

Sprite = renpy.display.particle.Sprite
SpriteManager = renpy.display.particle.SpriteManager


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
AlphaDissolve = renpy.curry.curry(renpy.display.transition.AlphaDissolve)
CropMove = renpy.curry.curry(renpy.display.transition.CropMove)
Pixellate = renpy.curry.curry(renpy.display.transition.Pixellate)


OldMoveTransition = renpy.curry.curry(renpy.display.movetransition.OldMoveTransition)
MoveTransition = renpy.curry.curry(renpy.display.movetransition.MoveTransition)
MoveFactory = renpy.curry.curry(renpy.display.movetransition.MoveFactory)
MoveIn = renpy.curry.curry(renpy.display.movetransition.MoveIn)
MoveOut = renpy.curry.curry(renpy.display.movetransition.MoveOut)
ZoomInOut = renpy.curry.curry(renpy.display.movetransition.ZoomInOut)
RevolveInOut = renpy.curry.curry(renpy.display.movetransition.RevolveInOut)

MultipleTransition = renpy.curry.curry(renpy.display.transition.MultipleTransition)
ComposeTransition = renpy.curry.curry(renpy.display.transition.ComposeTransition)
Pause = renpy.curry.curry(renpy.display.transition.NoTransition)
SubTransition = renpy.curry.curry(renpy.display.transition.SubTransition)

# Misc.
ADVSpeaker = ADVCharacter = renpy.character.ADVCharacter
Speaker = Character = renpy.character.Character
DynamicCharacter = renpy.character.DynamicCharacter
MultiPersistent = renpy.persistent.MultiPersistent

Action = renpy.ui.Action
BarValue = renpy.ui.BarValue

Style = renpy.style.Style

absolute = renpy.display.core.absolute

NoRollback = renpy.python.NoRollback

def _layout(cls, doc, nargs=0, **extra_kwargs):

    def f(*args, **properties):

        conargs = args[:nargs]
        kids = args[nargs:]

        kwargs = extra_kwargs.copy()
        kwargs.update(properties)

        rv = cls(*conargs, **kwargs)
        for i in kids:
            rv.add(renpy.easy.displayable(i))

        return rv

    f.__doc__ = doc

    return f

Fixed = _layout(renpy.display.layout.MultiBox, """
:doc: disp_box
:args: (*args, **properties)

A box that fills the screen. Its members are laid out
from back to front, with their position properties
controlling their position.
""", layout="fixed")

HBox = _layout(renpy.display.layout.MultiBox, """
:doc: disp_box
:args: (*args, **properties)

A box that lays out its members from left to right.
""", layout='horizontal')

VBox = _layout(renpy.display.layout.MultiBox, """
:doc: disp_box
:args: (*args, **properties)

A layout that lays out its members from top to bottom.
""", layout='vertical')

Grid = _layout(renpy.display.layout.Grid, """
:doc: disp_grid

Lays out displayables in a a grid. The first two positional arguments
are the number of columns and rows in the grid. This must be followed
by `columns * rows` positional arguments giving the displayables that
fill the grid.
""", nargs=2, layout='vertical')

del _layout

def AlphaBlend(control, old, new, alpha=False):
    """
    :doc: disp_effects

    This transition uses a `control` displayable (almost always some sort of
    animated transform) to transition from one displayable to another. The
    transform is evaluated. The `new` displayable is used where the transform
    is opaque, and the `old` displayable is used when it is transparent.

    `alpha`
        If true, the image is composited with what's behind it. If false,
        the default, the image is opaque and overwrites what's behind it.
    """

    return renpy.display.transition.AlphaDissolve(control, 0.0, old_widget=old, new_widget=new, alpha=alpha)

def At(d, *args):
    """
    :doc: disp_at

    Given a displayable `d`, applies each of the transforms in `args`
    to it. The transforms are applied in left-to-right order, so that
    the outermost transform is the rightmost argument. ::

        transform birds_transform:
             xpos -200
             linear 10 xpos 800
             pause 20
             repeat

        image birds = At("birds.png", birds_transform)
        """

    rv = renpy.easy.displayable(d)

    for i in args:
        rv = i(rv)

    return rv


# The color function. (Moved, since text needs it, too.)
color = renpy.easy.color

# Conveniently get rid of all the packages we had imported before.
import renpy.exports as renpy #@Reimport

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
                   image=None,

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
                   screen='say',
                   mode='say',
                   voice_tag=None,

                   kind=False)

def predict_say(who, what):
    who = Character(who, kind=name_only)
    try:
        who.predict(what)
    except:
        pass

def say(who, what, interact=True):
    who = Character(who, kind=name_only)
    who(what, interact=interact)

# Used by renpy.reshow_say.
_last_say_who = None
_last_say_what = None

# Used to store the things pinned into the cache.
_cache_pin_set = set()

# If we're in a replay, the label of the start of the replay.
_in_replay = None

# Used to store the side image attributes.
_side_image_attributes = None

# True if we're in the main_menu, False otherwise. This controls autosave,
# among other things.
main_menu = False

# Make these available to user code.
import sys
import os

def public_api():
    ui
    im
    object
    range
    sorted
    os
    sys

del public_api
