# Copyright 2004-2020 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import *

from renpy.minstore import *

# But please note that this will not be available in the body
# of user code, unless we re-import it.
import renpy.display
import renpy.audio
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

# Should beginning a new rollback be allowed?
_begin_rollback = True

# Should skipping be allowed?
_skipping = True

# Should dismissing pauses and transitions be allowed?
_dismiss_pause = True

# config.
_config = renpy.config

# Used by the ui functions.
_widget_by_id = None
_widget_properties = { }

# The text rectangle, or None to use the automatic code.
_text_rect = None

# Are we in various menus?
_menu = False
main_menu = False

# Is autosaving allowed?
_autosave = True

# Should live2d fading happen?
_live2d_fade = True


class _Config(object):

    def __getstate__(self):
        return None

    def __setstate__(self, data):
        return

    def register(self, name, default, cat=None, help=None): # @ReservedAssignment
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

        if name == "developer":
            if value == "auto":
                renpy.config.original_developer = value
                renpy.config.developer = renpy.config.default_developer
                return

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

eval = renpy.python.py_eval # @ReservedAssignment

# Displayables.
Bar = renpy.display.behavior.Bar
Button = renpy.display.behavior.Button
ImageButton = renpy.display.behavior.ImageButton
Input = renpy.display.behavior.Input
TextButton = renpy.display.behavior.TextButton

ImageReference = renpy.display.image.ImageReference
DynamicImage = renpy.display.image.DynamicImage

Image = renpy.display.im.image

Frame = renpy.display.imagelike.Frame
Borders = renpy.display.imagelike.Borders
Solid = renpy.display.imagelike.Solid
FileCurrentScreenshot = renpy.display.imagelike.FileCurrentScreenshot

LiveComposite = renpy.display.layout.LiveComposite
LiveCrop = renpy.display.layout.LiveCrop
LiveTile = renpy.display.layout.LiveTile

Composite = renpy.display.layout.Composite
Crop = renpy.display.layout.Crop
Tile = renpy.display.layout.Tile

Flatten = renpy.display.layout.Flatten

Null = renpy.display.layout.Null
Window = renpy.display.layout.Window
Viewport = renpy.display.viewport.Viewport
DynamicDisplayable = renpy.display.layout.DynamicDisplayable
ConditionSwitch = renpy.display.layout.ConditionSwitch
ShowingSwitch = renpy.display.layout.ShowingSwitch
AlphaMask = renpy.display.layout.AlphaMask

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

Matrix = renpy.display.matrix.Matrix # @UndefinedVariable

Live2D = renpy.gl2.live2d.Live2D

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
PushMove = renpy.curry.curry(renpy.display.transition.PushMove)
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

AudioData = renpy.audio.audio.AudioData

# NOTE: When exporting something from here, decide if we need to add it to
# renpy.pyanalysis.pure_functions.

Style = renpy.style.Style # @UndefinedVariable

NoRollback = renpy.python.NoRollback


class _layout_class(__builtins__["object"]):
    """
    This is used to generate declarative versions of MultiBox and Grid.
    """

    def __init__(self, cls, doc, nargs=0, **extra_kwargs):
        self.cls = cls
        self.nargs = nargs
        self.extra_kwargs = extra_kwargs

        self.__doc__ = doc

    def __call__(self, *args, **properties):

        conargs = args[:self.nargs]
        kids = args[self.nargs:]

        kwargs = self.extra_kwargs.copy()
        kwargs.update(properties)

        rv = self.cls(*conargs, **kwargs)
        for i in kids:
            rv.add(renpy.easy.displayable(i))

        return rv


Fixed = _layout_class(renpy.display.layout.MultiBox, """
:name: Fixed
:doc: disp_box
:args: (*args, **properties)

A box that fills the screen. Its members are laid out
from back to front, with their position properties
controlling their position.
""", layout="fixed")

HBox = _layout_class(renpy.display.layout.MultiBox, """
:doc: disp_box
:args: (*args, **properties)

A box that lays out its members from left to right.
""", layout='horizontal')

VBox = _layout_class(renpy.display.layout.MultiBox, """
:doc: disp_box
:args: (*args, **properties)

A layout that lays out its members from top to bottom.
""", layout='vertical')

Grid = _layout_class(renpy.display.layout.Grid, """
:doc: disp_grid
:args: (cols, rows, *args, **properties)

Lays out displayables in a grid. The first two positional arguments
are the number of columns and rows in the grid. This must be followed
by `columns * rows` positional arguments giving the displayables that
fill the grid.
""", nargs=2, layout='vertical')


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

        if isinstance(i, renpy.display.motion.Transform):
            rv = i(child=rv)
        else:
            rv = i(rv)

    return rv


# The color class/function.
Color = renpy.color.Color
color = renpy.color.Color

# Conveniently get rid of all the packages we had imported before.
import renpy.exports as renpy # @Reimport

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
                   advance=True,

                   who_style='say_label',
                   what_style='say_dialogue',
                   window_style='say_window',
                   screen='say',
                   mode='say',
                   voice_tag=None,

                   kind=False)

# predict_say and who are defined in 00library.rpy, but we add default
# versions here in case there is a problem with initialization. (And
# for pickling purposes.)


def predict_say(who, what):
    who = Character(who, kind=adv)
    try:
        who.predict(what)
    except:
        pass


def say(who, what, interact=True, *args, **kwargs):
    who = Character(who, kind=adv)
    who(what, interact=interact, *args, **kwargs)


# Used by renpy.reshow_say and extend.
_last_say_who = None
_last_say_what = None
_last_say_args = ()
_last_say_kwargs = { }

# Used to store the things pinned into the cache.
_cache_pin_set = set()

# Used to store displayables that should be predicted.
_predict_set = set()

# A map from a screen name to an (args, kwargs) tuple. The arguments and
# keyword arguments can be
_predict_screen = dict()

# Should the default screens be shown?
_overlay_screens = None

# If we're in a replay, the label of the start of the replay.
_in_replay = None

# Used to store the side image attributes.
_side_image_attributes = None
_side_image_attributes_reset = False

# True if we're in the main_menu, False otherwise. This controls autosave,
# among other things.
main_menu = False

# The action that's used when the player clicks the ignore button on the
# error handling screen.
_ignore_action = None

# The save slot that Ren'Py saves to on quit.
_quit_slot = None

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
