# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains functions that can be used to display a UI on the
# screen.  The UI isn't implemented here (rather, in
# renpy.display). Instead, these functions provide a simple interface
# that allows a user to procedurally create a UI.

# All functions in the is file should be documented in the wiki.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import sys

import renpy
from renpy.display.behavior import is_selected, is_sensitive

##############################################################################
# Special classes that can be subclassed from the outside.


class Action(renpy.object.Object):
    """
    Subclassable by creators, documented in Sphinx.
    """

    # Alt text.
    alt = None

    def get_sensitive(self):
        return True

    def get_selected(self):
        return False

    def get_tooltip(self):
        return None

    def periodic(self, st):
        return

    def predict(self):
        return

    def __call__(self):
        raise NotImplementedError


class BarValue(renpy.object.Object):
    """
    Subclassable by creators, documented in Sphinx.
    """

    # Alt text.
    alt = "Bar"

    force_step = False

    def replaces(self, other):
        return

    def periodic(self, st):
        return

    def get_adjustment(self): # type: (BarValue) -> renpy.display.behavior.Adjustment
        raise NotImplementedError

    def get_style(self):
        return "bar", "vbar"

    def get_tooltip(self):
        return None

##############################################################################
# Things we can add to. These have two methods: add is called with the
# widget we're adding. close is called when the thing is ready to be
# closed.


class Addable(object):
    # A style_prefix associates with this addable.
    style_prefix = None

    def add(self, d, key):
        raise NotImplementedError

    def close(self, d):
        raise NotImplementedError

    def get_layer(self):
        return Exception("Operation can only be performed on a layer.")


class Layer(Addable):

    def __init__(self, name):
        self.name = name

    def add(self, d, key):
        renpy.game.context(-1).scene_lists.add(self.name, d, key=key)

    def close(self, d):
        stack.pop()

        if d and d != self.name:
            raise Exception("ui.close closed layer %s, not the expected %r." % (self.name, d))

    def get_layer(self):
        return self.name

    def __repr__(self):
        return "<Layer: %r>" % self.name


class Many(Addable):
    """
    A widget that takes many children.
    """

    def __init__(self, displayable, imagemap, style_prefix):
        self.displayable = displayable
        self.imagemap = imagemap
        self.style_prefix = style_prefix

    def add(self, d, key):
        self.displayable.add(d)

    def close(self, d):
        stack.pop()

        if self.imagemap:
            imagemap = imagemap_stack.pop()
            imagemap.cache.finish()

        if d and d != self.displayable:
            raise Exception("ui.close closed %r, not the expected %r." % (self.displayable, d))

    def __repr__(self):
        return "<Many: %r>" % self.displayable


class One(Addable):
    """
    A widget that expects exactly one child.
    """

    def __init__(self, displayable, style_prefix):
        self.displayable = displayable
        self.style_prefix = style_prefix

    def add(self, d, key):
        self.displayable.add(d)
        stack.pop()

    def close(self, d):
        raise Exception("Widget %r expects a child." % self.displayable)

    def __repr__(self):
        return "<One: %r>" % self.displayable


class Detached(Addable):
    """
    Used to indicate a widget is detached from the stack.
    """

    def __init__(self, style_prefix):
        self.style_prefix = style_prefix

    def add(self, d, key):
        self.child = d
        stack.pop()

    def close(self, d):
        raise Exception("Detached expects to be given a child.")


class ChildOrFixed(Addable):
    """
    If one widget is added, then it is added directly to our
    parent. Otherwise, a fixed is added to our parent, and all
    the widgets are added to that.
    """

    def __init__(self, style_prefix):
        self.queue = [ ]
        self.style_prefix = style_prefix

    def add(self, d, key):
        self.queue.append(d)

    def close(self, d):
        stack.pop()

        if len(self.queue) == 1:
            implicit_add(self.queue[0])
        else:
            fixed()

            for i in self.queue:
                implicit_add(i)

            close()

        if d is not None:
            raise Exception("Did not expect to close %r." % d)


# A stack of things we can add to.
stack = [ ] # type: list[Addable]

# A stack of open ui.ats.
at_stack = [ ]

# The tag for the displayble being added to the layer.
add_tag = None

# A stack of Imagemap objects.
imagemap_stack = [ ]


# Called at the end of the init phase, and from the screen
# prediction code.
def reset():
    global stack
    global at_stack
    global imagemap_stack

    stack = [ Layer('transient') ]
    at_stack = [ ]
    imagemap_stack = [ ]


renpy.game.post_init.append(reset)


def interact(type='misc', roll_forward=None, **kwargs):
    """
    :doc: ui
    :args: (*, roll_forward=None, mouse='default')

    Causes an interaction with the user, and returns the result of that
    interaction. This causes Ren'Py to redraw the screen and begin processing
    input events. When a displayable returns a value in response to an event,
    that value is returned from ui.interact, and the interaction ends.

    This function is rarely called directly. It is usually called by other
    parts of Ren'Py, including the say statement, menu statement, with statement,
    pause statement, call screen, :func:`renpy.input`, among many other
    functions. However, it can be called directly if necessary.

    When an interaction ends, the transient layer and all screens shown with
    `_transient` as true are cleared from the scene lists.

    The following arguments are documented. As other, undocumented arguments
    exist for Ren'Py's internal use, please pass all arguments as keyword
    arguments.

    `roll_forward`
        The information that will be returned by this function when a
        roll forward occurs. (If None, the roll forward is ignored.) This
        should usually be passed the result of the :func:`renpy.roll_forward_info`
        function.

    `mouse`
        The style of mouse cursor to use during this function.
    """

    if stack is None:
        raise Exception("Interaction not allowed during init phase.")

    if renpy.config.skipping == "fast":
        renpy.config.skipping = None

    if len(stack) != 1:
        raise Exception("ui.interact called with non-empty widget/layer stack. Did you forget a ui.close() somewhere?\nStack was " + ('\n'.join([str(item) for item in stack])))

    if at_stack:
        raise Exception("ui.interact called with non-empty at stack.")

    renpy.game.context().info._current_interact_type = type
    rv = renpy.game.interface.interact(roll_forward=roll_forward, **kwargs)
    renpy.game.context().info._last_interact_type = type

    if renpy.exports.in_fixed_rollback() and roll_forward is not None:
        return roll_forward
    else:
        return rv


def tag(name):
    global add_tag
    add_tag = name


def child_or_fixed():
    """
    Causes the current widget to be given child-fixed semantics. This
    means that we will queue up children added to it. If there is one
    child, that child will be added to the widget directly. Otherwise,
    a fixed will be created, and the children will be added to that.
    """

    stack.append(ChildOrFixed(stack[-1].style_prefix))


def remove(d):
    layer = stack[-1].get_layer()
    renpy.game.context(-1).scene_lists.remove(layer, d)


def remove_above(d):
    layer = stack[-1].get_layer()
    renpy.game.context(-1).scene_lists.remove_above(layer, d)


def at(transform):
    """
    :undocumented:

    Specifies a transform that is applied to the next displayable to
    be created. This is largely obsolete, as all UI functions now take
    an `at` argument.
    """

    at_stack.append(transform)


def clear():
    layer = stack[-1].get_layer()
    renpy.game.context(-1).scene_lists.clear(layer)


def detached():
    """
    :undocumented:

    Do not add the next displayable to any later or container. Use this if
    you want to assign the result of a ui function to a variable.
    """

    rv = Detached(stack[-1].style_prefix)
    stack.append(rv)
    return rv


def layer(name):
    """
    :undocumented:

    Adds displayables to the layer named `name`. The later must be
    closed with :func:`ui.close`.
    """

    stack.append(Layer(name))


def close(d=None):
    """
    :undocumented:
    :args: ()

    Closes a displayable created with by a UI function. When a
    displayable is closed, we add new displayables to its parent,
    or to the layer if no displayable is open.
    """

    stack[-1].close(d)

    if not stack:
        raise Exception("ui.close() called when no layer or widget is open.")


def reopen(w, clear):

    stack.append(Many(w, None, None))

    if clear:
        w.children[:] = [ ]


def context_enter(w):
    if isinstance(renpy.ui.stack[-1], renpy.ui.Many) and renpy.ui.stack[-1].displayable is w: # type: ignore
        return

    raise Exception("%r cannot be used as a context manager." % type(w).__name__)


def context_exit(w):
    close(w)


NoStylePrefixGiven = renpy.object.Sentinel("NoStylePrefixGiven")


def combine_style(style_prefix, style_suffix):
    """
    Combines a style prefix and style suffix to create a style name, then
    returns the style object corresoinding to that name.
    """

    if style_prefix is None:
        new_style = style_suffix
    else:
        new_style = style_prefix + "_" + style_suffix

    return renpy.style.get_style(new_style)


def prefixed_style(style_suffix):
    """
    Combines the default style prefix with a style suffix.
    """

    return combine_style(stack[-1].style_prefix, style_suffix)


# The screen we're using as we add widgets. None if there isn't a
# screen.
screen = None # type: renpy.display.screen.ScreenDisplayable|None


class Wrapper(renpy.object.Object):

    def __reduce__(self):
        if PY2:
            return bytes(self.name) # type: ignore
        else:
            return self.name

    def __init__(self, function, one=False, many=False, imagemap=False, replaces=False, style=None, **kwargs):

        # The name assigned to this wrapper. This is used to serialize us correctly.
        self.name = ''

        # The function to call.
        self.function = function

        # Should we add one or many things to this wrapper?
        self.one = one
        self.many = many or imagemap
        self.imagemap = imagemap

        # Should the function be given the replaces parameter,
        # specifiying the displayable it replaced?
        self.replaces = replaces

        # Default keyword arguments to the function.
        self.kwargs = kwargs

        # Default style (suffix).
        self.style = style

    def __call__(self, *args, **kwargs):

        global add_tag

        if not stack:
            raise Exception("Can't add displayable during init phase.")

        # Pull out the special kwargs, widget_id, at, and style_prefix.

        widget_id = kwargs.pop("id", None)

        at_list = kwargs.pop("at", [ ]) # type: list
        if not isinstance(at_list, (list, tuple)):
            at_list = [ at_list ]

        style_prefix = stack[-1].style_prefix

        if "style_group" in kwargs:
            style_prefix = kwargs.pop("style_group")

        if "style_prefix" in kwargs:
            style_prefix = kwargs.pop("style_prefix")

        # Figure out the keyword arguments, based on the parameters.
        if self.kwargs:
            keyword = self.kwargs.copy()
            keyword.update(kwargs)
        else:
            keyword = kwargs

        # Should we transfer data from an old version of this screen?
        old_transfers = screen and screen.old_transfers

        # Should we add?
        do_add = True

        if screen:
            if widget_id in screen.widget_properties:
                keyword.update(screen.widget_properties[widget_id])

            if widget_id in screen.hidden_widgets:
                do_add = False

        if old_transfers:
            old_main = screen.old_widgets.get(widget_id, None) # type: ignore

            if self.replaces and old_main is not None:
                keyword["replaces"] = old_main
        else:
            old_main = None

        style_suffix = keyword.pop("style_suffix", None) or self.style

        if style_suffix and ("style" not in keyword):
            keyword["style"] = combine_style(style_prefix, style_suffix)

        try:
            w = self.function(*args, **keyword)
        except TypeError as e:
            _etype, e, tb = sys.exc_info()

            if tb.tb_next is None:
                e.args = (e.args[0].replace("__call__", "ui." + self.name),) # type: ignore

            del tb # Important! Prevents memory leaks via our frame.
            raise

        main = w._main or w

        # Migrate the focus.
        if (old_main is not None) and (not screen.hiding): # type: ignore
            renpy.display.focus.replaced_by[id(old_main)] = main

        # Wrap the displayable based on the at_list and at_stack.
        atw = w

        while at_stack:
            at_list.append(at_stack.pop())

        for atf in at_list:
            if isinstance(atf, renpy.display.motion.Transform):
                atw = atf(child=atw)
            else:
                atw = atf(atw)

        # Add to the displayable at the bottom of the stack.
        if do_add:
            stack[-1].add(atw, add_tag)

        # Update the stack, as necessary.
        if self.one:
            stack.append(One(w, style_prefix)) # type: ignore
        elif self.many:
            stack.append(Many(w, self.imagemap, style_prefix)) # type:ignore

        # If we have an widget_id, record the displayable, the transform,
        # and maybe take the state from a previous transform.
        if screen and widget_id is not None:
            screen.widgets[widget_id] = main

            if isinstance(atw, renpy.display.motion.Transform):
                screen.transforms[widget_id] = atw

                if old_transfers:
                    oldt = screen.old_transforms.get(widget_id, None)
                else:
                    oldt = None

                atw.take_state(oldt)
                atw.take_execution_state(oldt)

        # Clear out the add_tag.
        add_tag = None

        return main

##############################################################################
# Widget functions.


def _add(d, **kwargs):
    d = renpy.easy.displayable(d)

    if d._duplicatable:
        d = d._duplicate(None)
        d._unique()

    rv = d

    if kwargs:
        rv = renpy.display.motion.Transform(child=d, **kwargs)

    return rv


add = Wrapper(_add)


def _implicit_add(d):
    """
    A faster version of add to use when we know `d` is a displayable and isn't
    transformed.
    """

    return d


implicit_add = Wrapper(_implicit_add)


def _image(im, **properties):
    d = renpy.display.im.image(im, loose=True, **properties)

    if d._duplicatable:
        d = d._duplicate(None)
        d._unique()

    return d


image = Wrapper(_image)

null = Wrapper(renpy.display.layout.Null)
text = Wrapper(renpy.text.text.Text, style="text", replaces=True)
hbox = Wrapper(renpy.display.layout.MultiBox, layout="horizontal", style="hbox", many=True)
vbox = Wrapper(renpy.display.layout.MultiBox, layout="vertical", style="vbox", many=True)
fixed = Wrapper(renpy.display.layout.MultiBox, layout="fixed", style="fixed", many=True)
default_fixed = Wrapper(renpy.display.layout.MultiBox, layout="fixed", many=True)
grid = Wrapper(renpy.display.layout.Grid, style="grid", many=True)
side = Wrapper(renpy.display.layout.Side, style="side", many=True)


def _sizer(maxwidth=None, maxheight=None, **properties):
    return renpy.display.layout.Container(xmaximum=maxwidth, ymaximum=maxheight, **properties)


sizer = Wrapper(_sizer, one=True)
window = Wrapper(renpy.display.layout.Window, style="window", one=True, child=None)
frame = Wrapper(renpy.display.layout.Window, style="frame", one=True, child=None)

keymap = Wrapper(renpy.display.behavior.Keymap)
saybehavior = Wrapper(renpy.display.behavior.SayBehavior)
pausebehavior = Wrapper(renpy.display.behavior.PauseBehavior)
soundstopbehavior = Wrapper(renpy.display.behavior.SoundStopBehavior)


def _key(key, action=None, activate_sound=None, capture=True):

    if isinstance(key, (list, tuple)):
        keymap = {k: action for k in key}
    else:
        keymap = {key: action}

    return renpy.display.behavior.Keymap(activate_sound=activate_sound, capture=capture, **keymap)


key = Wrapper(_key)


class ChoiceActionBase(Action):
    """
    Base class for choice actions. The choice is identified by a label
    and value. The class will automatically determine the rollback state
    and supply correct "sensitive" and "selected" information to the
    widget.
    If a location is supplied, it will check whether the choice was
    previously visited and mark it so if it is chosen.
    """

    sensitive = True

    def __init__(self, label, value, location=None, block_all=None, sensitive=True, args=None, kwargs=None):
        self.label = label
        self.value = value
        self.location = location
        self.sensitive = sensitive

        if block_all is None:
            self.block_all = renpy.config.fix_rollback_without_choice
        else:
            self.block_all = block_all

        # The arguments passed to a menu choice.
        self.args = args
        self.kwargs = kwargs

    def get_sensitive(self):
        return (self.sensitive and
                not renpy.exports.in_fixed_rollback() or (not self.block_all and self.get_selected()))

    def get_selected(self):
        roll_forward = renpy.exports.roll_forward_info()
        return renpy.exports.in_fixed_rollback() and roll_forward == self.value

    @property
    def chosen(self):
        if not self.location:
            return None

        return renpy.game.persistent._chosen # type: ignore

    def get_chosen(self):
        if self.chosen is None:
            return False

        return (self.location, self.label) in self.chosen


class ChoiceReturn(ChoiceActionBase):
    """
    :doc: blockrollback

    A menu choice action that returns `value`, while managing the button
    state in a manner consistent with fixed rollback. (See block_all for
    a description of the behavior.)


    `label`
        The label text of the button. For imagebuttons and hotspots this
        can be anything. This label is used as a unique identifier of
        the options within the current screen. Together with `location`
        it is used to store whether this option has been chosen.

    `value`
        The value this is returned when the choice is chosen.

    `location`
        A unique location identifier for the current choices screen.

    `block_all`
        If false, the button is given the selected role if it was
        the chosen choice, and insensitive if it was not selected.

        If true, the button is always insensitive during fixed
        rollback.

        If None, the value is taken from the :var:`config.fix_rollback_without_choice`
        variable.

        When true is given to all items in a screen, it will
        become unclickable (rolling forward will still work).
    """

    def __call__(self):
        if self.chosen is not None:
            self.chosen[(self.location, self.label)] = True

        return self.value


class ChoiceJump(ChoiceActionBase):
    """
    :doc: blockrollback

    A menu choice action that returns `value`, while managing the button
    state in a manner consistent with fixed rollback. (See block_all for
    a description of the behavior.)


    `label`
        The label text of the button. For imagebuttons and hotspots this
        can be anything. This label is used as a unique identifier of
        the options within the current screen. Together with `location`
        it is used to store whether this option has been chosen.

    `value`
        The location to jump to.

    `location`
        A unique location identifier for the current choices screen.

    `block_all`
        If false, the button is given the selected role if it was
        the chosen choice, and insensitive if it was not selected.

        If true, the button is always insensitive during fixed
        rollback.

        If None, the value is taken from the :var:`config.fix_rollback_without_choice`
        variable.

        When true is given to all items in a screen, it will
        become unclickable (rolling forward will still work).
    """

    def get_selected(self):
        roll_forward = renpy.exports.roll_forward_info()

        # renpy.exports.call_screen create a checkpoint with the jump exception
        if isinstance(roll_forward, renpy.game.JumpException):
            roll_forward = roll_forward.args[0]

        return renpy.exports.in_fixed_rollback() and roll_forward == self.value

    def __call__(self):
        if self.chosen is not None:
            self.chosen[(self.location, self.label)] = True

        renpy.exports.jump(self.value)


class Choice(object):
    """
    :doc: se_menu
    :name: renpy.Choice
    :args: (value, /, *args, **kwargs)

    This encapsulates a menu choice with with arguments. The first positional argument is is the value
    that will be returned, and the other arguments are the arguments that will be passed to the choice
    screen.

    This is intended for use in the items list of :func:`renpy.display_menu` to supply arguments to
    that screen.

    `value`
        The value that will be given to the choice screen.

    Positional arguments and keyword arguments are stored in this object and used by renpy.display_menu.
    """

    def __init__(self, _value, *args, **kwargs):
        self.value = _value
        self.args = args
        self.kwargs = kwargs


def menu(menuitems,
         style='menu',
         caption_style='menu_caption',
         choice_style='menu_choice',
         choice_chosen_style='menu_choice_chosen',
         choice_button_style='menu_choice_button',
         choice_chosen_button_style='menu_choice_chosen_button',
         location=None,
         focus=None,
         default=False,
         **properties):

    renpy.ui.vbox(style=style, **properties)

    for label, val in menuitems:
        if val is None:
            renpy.ui.text(label, style=caption_style)
        else:

            text = choice_style
            button = choice_button_style

            if isinstance(val, ChoiceReturn):
                clicked = val
            else:
                clicked = ChoiceReturn(label, val, location)

            if clicked.get_chosen():
                text = choice_chosen_style
                button = choice_chosen_button_style

            if isinstance(button, basestring):
                button = getattr(renpy.game.style, button)
            if isinstance(text, basestring):
                text = getattr(renpy.game.style, text)

            button = button[label]
            text = text[label]

            renpy.ui.textbutton(label,
                                style=button,
                                text_style=text,
                                clicked=clicked,
                                focus=focus,
                                default=default)

    close()


input = Wrapper(renpy.display.behavior.Input, exclude='{}', style="input", replaces=True)


def imagemap_compat(ground,
                    selected,
                    hotspots,
                    unselected=None,
                    style='imagemap',
                    button_style='hotspot',
                    **properties):

    if isinstance(button_style, basestring):
        button_style = getattr(renpy.game.style, button_style)

    fixed(style=style, **properties)

    if unselected is None:
        unselected = ground

    add(ground)

    for x0, y0, x1, y1, result in hotspots:

        if result is None:
            continue

        action = ChoiceReturn(result, result)

        selected_img = renpy.display.layout.LiveCrop((x0, y0, x1 - x0, y1 - y0), selected)

        imagebutton(renpy.display.layout.LiveCrop((x0, y0, x1 - x0, y1 - y0), unselected),
                    selected_img,
                    selected_idle_image=selected_img,
                    selected_insensitive_image=selected_img,
                    clicked=action,
                    style=button_style[result],
                    xpos=x0,
                    xanchor=0,
                    ypos=y0,
                    yanchor=0,
                    focus_mask=True,
                    )

    close()


button = Wrapper(renpy.display.behavior.Button, style='button', one=True)


def _imagebutton(idle_image=None,
                 hover_image=None,
                 insensitive_image=None,
                 activate_image=None,
                 selected_idle_image=None,
                 selected_hover_image=None,
                 selected_insensitive_image=None,
                 selected_activate_image=None,
                 idle=None,
                 hover=None,
                 insensitive=None,
                 selected_idle=None,
                 selected_hover=None,
                 selected_insensitive=None,
                 image_style=None,
                 auto=None,
                 **properties):

    def choice(a, b, name, required=False):
        if a:
            return a

        if b:
            return b

        if auto is not None:
            rv = renpy.config.imagemap_auto_function(auto, name)
            if rv is not None:
                return rv

        if required:
            if auto:
                raise Exception("Imagebutton does not have a %s image. (auto=%r)." % (name, auto))
            else:
                raise Exception("Imagebutton does not have a %s image." % (name,))

        return None

    idle = choice(idle, idle_image, "idle", required=True)
    hover = choice(hover, hover_image, "hover")
    insensitive = choice(insensitive, insensitive_image, "insensitive")
    selected_idle = choice(selected_idle, selected_idle_image, "selected_idle")
    selected_hover = choice(selected_hover, selected_hover_image, "selected_hover")
    selected_insensitive = choice(selected_insensitive, selected_insensitive_image, "selected_insensitive")

    return renpy.display.behavior.ImageButton(
        idle,
        hover,
        insensitive_image=insensitive,
        activate_image=activate_image,
        selected_idle_image=selected_idle,
        selected_hover_image=selected_hover,
        selected_insensitive_image=selected_insensitive,
        selected_activate_image=selected_activate_image,
        **properties)


imagebutton = Wrapper(_imagebutton, style="image_button")


def _textbutton(label, clicked=None, style=None, text_style=None, substitute=True, scope=None, **kwargs):

    text_kwargs, button_kwargs = renpy.easy.split_properties(kwargs, "text_", "")

    # Deal with potentially bad keyword arguments. (We'd get these if the user
    # writes text_align instead of text_text_align.)
    if "align" in text_kwargs:
        if isinstance(text_kwargs["align"], float):
            text_kwargs.pop("align")
    text_kwargs.pop("y_fudge", None)

    if style is None:
        style = prefixed_style("button")

    if text_style is None:
        text_style = renpy.style.get_text_style(style, prefixed_style('button_text'))

    rv = renpy.display.behavior.Button(style=style, clicked=clicked, **button_kwargs)
    text = renpy.text.text.Text(label, style=text_style, substitute=substitute, scope=scope, **text_kwargs)
    rv.add(text)
    rv._main = text # type: ignore
    rv._composite_parts = [ text ]
    return rv


textbutton = Wrapper(_textbutton)


def _label(label, style=None, text_style=None, substitute=True, scope=None, **kwargs):

    text_kwargs, label_kwargs = renpy.easy.split_properties(kwargs, "text_", "")

    if style is None:
        style = prefixed_style('label')

    if text_style is None:
        text_style = renpy.style.get_text_style(style, prefixed_style('label_text'))

    rv = renpy.display.layout.Window(None, style=style, **label_kwargs)
    text = renpy.text.text.Text(label, style=text_style, substitute=substitute, scope=scope, **text_kwargs)
    rv.add(text)
    rv._main = text # type: ignore
    rv._composite_parts = [ text ]
    return rv


label = Wrapper(_label)

adjustment = renpy.display.behavior.Adjustment


def _bar(*args, **properties):

    if len(args) == 4:
        width, height, range, value = args
    if len(args) == 2:
        range, value = args
        width = None
        height = None
    else:
        range = 1
        value = 0
        width = None
        height = None

    if "width" in properties:
        width = properties.pop("width")

    if "height" in properties:
        height = properties.pop("height")

    if "range" in properties:
        range = properties.pop("range")

    if "value" in properties:
        value = properties.pop("value")

    if "style" not in properties:
        if isinstance(value, BarValue):
            if properties["vertical"]:
                style = value.get_style()[1]
            else:
                style = value.get_style()[0]

            if isinstance(style, basestring):
                style = prefixed_style(style)

            properties["style"] = style

    return renpy.display.behavior.Bar(range, value, width, height, **properties)


bar = Wrapper(_bar, vertical=False, replaces=True)
vbar = Wrapper(_bar, vertical=True, replaces=True)
slider = Wrapper(_bar, style='slider', replaces=True)
vslider = Wrapper(_bar, style='vslider', replaces=True)
scrollbar = Wrapper(_bar, style='scrollbar', replaces=True)
vscrollbar = Wrapper(_bar, style='vscrollbar', replaces=True)


def _autobar_interpolate(range, start, end, time, st, at, **properties):

    if st > time:
        t = 1.0
        redraw = None
    else:
        t = st / time
        redraw = 0

    value = start + t * (end - start)
    return renpy.display.behavior.Bar(range, value, None, None, **properties), redraw


autobar_interpolate = renpy.curry.curry(_autobar_interpolate)


def _autobar(range, start, end, time, **properties):
    return renpy.display.layout.DynamicDisplayable(autobar_interpolate(range, start, end, time, **properties))


autobar = Wrapper(_autobar)
transform = Wrapper(renpy.display.motion.Transform, one=True, style='transform')

_viewport = Wrapper(renpy.display.viewport.Viewport, one=True, replaces=True, style='viewport')
_vpgrid = Wrapper(renpy.display.viewport.VPGrid, many=True, replaces=True, style='vpgrid')

VIEWPORT_SIZE = 32767


def viewport_common(vpfunc, _spacing_to_side, scrollbars=None, **properties):

    if scrollbars is None:
        return vpfunc(**properties)

    (vscrollbar_properties, scrollbar_properties, side_properties, viewport_properties, core_properties) = \
        renpy.easy.split_properties(properties, "vscrollbar_", "scrollbar_", "side_", "viewport_", "")

    if renpy.config.position_viewport_side:
        from renpy.sl2.slproperties import position_property_names

        for k, v in core_properties.items():
            if (renpy.config.compat_viewport_minimum) and (k in { "minimum", "xminimum", "yminimum" }):
                viewport_properties[k] = v
            elif k in position_property_names:
                side_properties[k] = v
            elif _spacing_to_side and (k == "spacing"):
                side_properties[k] = v
            else:
                viewport_properties[k] = v

    else:
        viewport_properties.update(core_properties)

    if renpy.config.prefix_viewport_scrollbar_styles and (scrollbars != "vertical"):
        scrollbar_properties.setdefault("style", prefixed_style("scrollbar"))
    else:
        scrollbar_properties.setdefault("style", "scrollbar")

    if renpy.config.prefix_viewport_scrollbar_styles and (scrollbars != "horizontal"):
        vscrollbar_properties.setdefault("style", prefixed_style("vscrollbar"))
    else:
        vscrollbar_properties.setdefault("style", "vscrollbar")

    alt = viewport_properties.get("alt", "viewport")
    scrollbar_properties.setdefault("alt", renpy.minstore.__(alt) + " " + renpy.minstore.__("horizontal scroll"))
    vscrollbar_properties.setdefault("alt", renpy.minstore.__(alt) + " " + renpy.minstore.__("vertical scroll"))

    if scrollbars == "vertical":

        if renpy.config.scrollbar_child_size:
            viewport_properties.setdefault("child_size", (None, VIEWPORT_SIZE))

        side("c r", **side_properties)

        rv = vpfunc(**viewport_properties)
        addable = stack.pop()

        vscrollbar(adjustment=rv.yadjustment, **vscrollbar_properties)
        close()

        stack.append(addable)

        return rv

    elif scrollbars == "horizontal":

        if renpy.config.scrollbar_child_size:
            viewport_properties.setdefault("child_size", (VIEWPORT_SIZE, None))

        side("c b", **side_properties)

        rv = vpfunc(**viewport_properties)
        addable = stack.pop()

        scrollbar(adjustment=rv.xadjustment, **scrollbar_properties)
        close()

        stack.append(addable)

        return rv

    else:

        if renpy.config.scrollbar_child_size:
            viewport_properties.setdefault("child_size", (VIEWPORT_SIZE, VIEWPORT_SIZE))

        side("c r b", **side_properties)

        rv = vpfunc(**viewport_properties)
        addable = stack.pop()

        vscrollbar(adjustment=rv.yadjustment, **vscrollbar_properties)
        scrollbar(adjustment=rv.xadjustment, **scrollbar_properties)
        close()

        stack.append(addable)

        return rv


def viewport(**properties):
    return viewport_common(_viewport, True, **properties)


def vpgrid(**properties):
    return viewport_common(_vpgrid, False, **properties)


conditional = Wrapper(renpy.display.behavior.Conditional, one=True)
timer = Wrapper(renpy.display.behavior.Timer, replaces=True)
drag = Wrapper(renpy.display.dragdrop.Drag, replaces=True, one=True)
draggroup = Wrapper(renpy.display.dragdrop.DragGroup, replaces=True, many=True)
mousearea = Wrapper(renpy.display.behavior.MouseArea, replaces=True)

##############################################################################
# New-style imagemap related functions.


class Imagemap(object):
    """
    Stores information about the images used by an imagemap.
    """

    alpha = True
    cache_param = True

    def __init__(self, insensitive, idle, selected_idle, hover, selected_hover, selected_insensitive, alpha, cache):
        self.insensitive = renpy.easy.displayable(insensitive)
        self.idle = renpy.easy.displayable(idle)
        self.selected_idle = renpy.easy.displayable(selected_idle)
        self.hover = renpy.easy.displayable(hover)
        self.selected_hover = renpy.easy.displayable(selected_hover)
        self.selected_insensitive = renpy.easy.displayable(selected_insensitive)

        self.alpha = alpha

        self.cache_param = cache
        self.cache = renpy.display.imagemap.ImageMapCache(cache)

    def reuse(self):
        self.cache = renpy.display.imagemap.ImageMapCache(self.cache_param)


def _imagemap(ground=None, hover=None, insensitive=None, idle=None, selected_hover=None, selected_idle=None, selected_insensitive=None, auto=None, alpha=True, cache=True, style='imagemap', **properties):

    def pick(variable, name, other):
        if variable:
            return variable

        if auto:
            for i in name:
                fn = renpy.config.imagemap_auto_function(auto, i)
                if fn is not None:
                    return fn

        if other is not None:
            return other

        raise Exception("Could not find a %s image for imagemap." % name[0])

    ground = pick(ground, ("ground", "idle"), idle)
    idle = pick(idle, ("idle",), ground)
    selected_idle = pick(selected_idle, ("selected_idle",), idle)
    hover = pick(hover, ("hover",), ground)
    selected_hover = pick(selected_hover, ("selected_hover",), hover)
    insensitive = pick(insensitive, ("insensitive",), ground)
    selected_insensitive = pick(selected_insensitive, ("selected_insensitive",), hover)

    imagemap_stack.append(
        Imagemap(
            insensitive,
            idle,
            selected_idle,
            hover,
            selected_hover,
            selected_insensitive,
            alpha,
            cache))

    properties.setdefault('fit_first', True)

    rv = renpy.display.layout.MultiBox(layout='fixed', **properties)
    parts = [ ]

    if ground:
        rv.add(renpy.easy.displayable(ground))
        parts.append(ground)

    box = renpy.display.layout.MultiBox(layout='fixed')
    rv.add(box)
    parts.append(box)

    rv._main = box # type: ignore
    rv._composite_parts = parts

    return rv


imagemap = Wrapper(_imagemap, imagemap=True, style='imagemap')


def _hotspot(spot, style='hotspot', **properties):

    if not imagemap_stack:
        raise Exception("hotspot expects an imagemap to be defined.")

    imagemap = imagemap_stack[-1]

    x, y, w, h = spot

    idle = imagemap.idle
    hover = imagemap.hover
    selected_idle = imagemap.selected_idle
    selected_hover = imagemap.selected_hover
    insensitive = imagemap.insensitive
    selected_insensitive = imagemap.selected_insensitive

    idle = imagemap.cache.crop(idle, spot)
    hover = imagemap.cache.crop(hover, spot)
    selected_idle = imagemap.cache.crop(selected_idle, spot)
    selected_hover = imagemap.cache.crop(selected_hover, spot)
    insensitive = imagemap.cache.crop(insensitive, spot)
    selected_insensitive = imagemap.cache.crop(selected_insensitive, spot)

    properties.setdefault("xpos", x)
    properties.setdefault("xanchor", 0)
    properties.setdefault("ypos", y)
    properties.setdefault("yanchor", 0)
    properties.setdefault("xminimum", w)
    properties.setdefault("xmaximum", w)
    properties.setdefault("yminimum", h)
    properties.setdefault("ymaximum", h)

    if imagemap.alpha:
        focus_mask = hover
    else:
        focus_mask = None

    properties.setdefault("focus_mask", focus_mask)

    return renpy.display.behavior.Button(
        None,
        idle_background=idle,
        selected_idle_background=selected_idle,
        hover_background=hover,
        selected_hover_background=selected_hover,
        insensitive_background=insensitive,
        selected_insensitive_background=selected_insensitive,
        style=style,
        **properties)


hotspot_with_child = Wrapper(_hotspot, style="hotspot", one=True)


def hotspot(*args, **kwargs):
    hotspot_with_child(*args, **kwargs)
    null()


def _hotbar(spot, adjustment=None, range=None, value=None, **properties):

    if (adjustment is None) and (range is None) and (value is None):
        raise Exception("hotbar requires either an adjustment or a range and value.")

    if not imagemap_stack:
        raise Exception("hotbar expects an imagemap to be defined.")

    imagemap = imagemap_stack[-1]

    x, y, w, h = spot

    properties.setdefault("xpos", x)
    properties.setdefault("ypos", y)
    properties.setdefault("xanchor", 0)
    properties.setdefault("yanchor", 0)

    fore_bar = imagemap.cache.crop(imagemap.selected_idle, spot)
    aft_bar = imagemap.cache.crop(imagemap.idle, spot)
    hover_fore_bar = imagemap.cache.crop(imagemap.selected_hover, spot)
    hover_aft_bar = imagemap.cache.crop(imagemap.hover, spot)

    if h > w:
        properties.setdefault("bar_vertical", True)
        properties.setdefault("bar_invert", True)

        fore_bar, aft_bar = aft_bar, fore_bar
        hover_fore_bar, hover_aft_bar = hover_aft_bar, hover_fore_bar

    return renpy.display.behavior.Bar(
        adjustment=adjustment,
        range=range,
        value=value,
        fore_bar=fore_bar,
        aft_bar=aft_bar,
        hover_fore_bar=hover_fore_bar,
        hover_aft_bar=hover_aft_bar,
        fore_gutter=0,
        aft_gutter=0,
        bar_resizing=False,
        thumb=None,
        thumb_shadow=None,
        thumb_offset=0,
        xmaximum=w,
        ymaximum=h,
        **properties)


hotbar = Wrapper(_hotbar, style="hotbar", replaces=True)

##############################################################################
# Curried functions, for use in clicked, hovered, and unhovered.


def _returns(v):

    return v


returns = renpy.curry.curry(_returns)


def _jumps(label, transition=None):

    if isinstance(transition, basestring):
        transition = getattr(renpy.config, transition) # type: ignore

    if transition is not None:
        renpy.exports.transition(transition)

    renpy.exports.jump(label)


jumps = renpy.curry.curry(_jumps)


def _jumpsoutofcontext(label):

    raise renpy.game.JumpOutException(label)


jumpsoutofcontext = renpy.curry.curry(_jumpsoutofcontext)


def callsinnewcontext(*args, **kwargs):
    return renpy.exports.curried_call_in_new_context(*args, **kwargs)


def invokesinnewcontext(*args, **kwargs):
    return renpy.exports.curried_invoke_in_new_context(*args, **kwargs)


def gamemenus(*args):

    if args:
        return callsinnewcontext("_game_menu", _game_menu_screen=args[0])
    else:
        return callsinnewcontext("_game_menu")

##############################################################################
# The on statement.


on = Wrapper(renpy.display.behavior.OnEvent)

##############################################################################
# A utility function so CDD components can be given an id.


def screen_id(id_, d):
    """
    :undocumented:

    Assigns the displayable `d` the screen widget id `id_`, as if it had
    been created by a screen statement with that id.
    """

    if screen is None:
        raise Exception("ui.screen_id must be called from within a screen.")

    screen.widgets[id_] = d._main or d
    screen.base_widgets[id_] = d



##############################################################################
# Postamble


# Update the wrappers to have names.
k, v = None, None
for k, v in globals().items():
    if isinstance(v, Wrapper):
        v.name = k
