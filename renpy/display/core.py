# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

# This file contains code for initializing and managing the display
# window.

from __future__ import print_function
import renpy.display
import renpy.audio
import renpy.text
import renpy.test

import pygame_sdl2 as pygame

import sys
import os
import time
import cStringIO
import threading
import copy
import gc
import inspect

import_time = time.time()

try:
    import android  # @UnresolvedImport
except:
    android = None

TIMEEVENT = pygame.event.register("TIMEEVENT")
PERIODIC = pygame.event.register("PERIODIC")
REDRAW = pygame.event.register("REDRAW")
EVENTNAME = pygame.event.register("EVENTNAME")

# All events except for TIMEEVENT and REDRAW
ALL_EVENTS = set(pygame.event.get_standard_events())  # @UndefinedVariable
ALL_EVENTS.add(PERIODIC)
ALL_EVENTS.add(EVENTNAME)

enabled_events = {
    pygame.QUIT,

    pygame.APP_TERMINATING,
    pygame.APP_LOWMEMORY,
    pygame.APP_WILLENTERBACKGROUND,
    pygame.APP_DIDENTERBACKGROUND,
    pygame.APP_WILLENTERFOREGROUND,
    pygame.APP_DIDENTERFOREGROUND,

    pygame.WINDOWEVENT,
    pygame.SYSWMEVENT,

    pygame.KEYDOWN,
    pygame.KEYUP,

    pygame.TEXTEDITING,
    pygame.TEXTINPUT,

    pygame.MOUSEMOTION,
    pygame.MOUSEBUTTONDOWN,
    pygame.MOUSEBUTTONUP,
    pygame.MOUSEWHEEL,

    pygame.JOYAXISMOTION,
    pygame.JOYHATMOTION,
    pygame.JOYBALLMOTION,
    pygame.JOYBUTTONDOWN,
    pygame.JOYBUTTONUP,
    pygame.JOYDEVICEADDED,
    pygame.JOYDEVICEREMOVED,

    pygame.CONTROLLERAXISMOTION,
    pygame.CONTROLLERBUTTONDOWN,
    pygame.CONTROLLERBUTTONUP,
    pygame.CONTROLLERDEVICEADDED,
    pygame.CONTROLLERDEVICEREMOVED,

    pygame.RENDER_TARGETS_RESET,

    TIMEEVENT,
    PERIODIC,
    REDRAW,
    EVENTNAME,
    }

# The number of msec between periodic events.
PERIODIC_INTERVAL = 50

# Time management.
time_base = 0.0
time_mult = 1.0


def init_time():
    warp = os.environ.get("RENPY_TIMEWARP", "1.0")

    global time_base
    global time_mult

    time_base = time.time()
    time_mult = float(warp)


def get_time():
    t = time.time()
    return time_base + (t - time_base) * time_mult


def displayable_by_tag(layer, tag):
    """
    Get the displayable on the given layer with the given tag.
    """

    return renpy.game.context().scene_lists.get_displayable_by_tag(layer, tag)


class IgnoreEvent(Exception):
    """
    Exception that is raised when we want to ignore an event, but
    also don't want to return anything.
    """

    pass


class EndInteraction(Exception):
    """
    Exception that can be raised (for example, during the render method of
    a displayable) to end the current interaction immediately.
    """

    def __init__(self, value):
        self.value = value


class absolute(float):
    """
    This represents an absolute float coordinate.
    """
    __slots__ = [ ]


def place(width, height, sw, sh, placement):
    """
    Performs the Ren'Py placement algorithm.

    `width`, `height`
        The width and height of the area the image will be
        placed in.

    `size`
        The size of the image to be placed.

    `placement`
        The tuple returned by Displayable.get_placement().
    """

    xpos, ypos, xanchor, yanchor, xoffset, yoffset, _subpixel = placement

    if xpos is None:
        xpos = 0
    if ypos is None:
        ypos = 0
    if xanchor is None:
        xanchor = 0
    if yanchor is None:
        yanchor = 0
    if xoffset is None:
        xoffset = 0
    if yoffset is None:
        yoffset = 0

    # We need to use type, since isinstance(absolute(0), float).
    if xpos.__class__ is float:
        xpos *= width

    if xanchor.__class__ is float:
        xanchor *= sw

    x = xpos + xoffset - xanchor

    if ypos.__class__ is float:
        ypos *= height

    if yanchor.__class__ is float:
        yanchor *= sh

    y = ypos + yoffset - yanchor

    return x, y


class DisplayableArguments(renpy.object.Object):
    """
    Represents a set of arguments that can be passed to a duplicated
    displayable.
    """

    # The name of the displayable without any arguments.
    name = ()

    # Arguments supplied.
    args = ()

    # This gets set to true if the arguments are consumed.
    consumed = False

    # The style prefix in play. This is used by DynamicImage to figure
    # out the prefix list to apply.
    prefix = None

    def copy(self, **kwargs):
        """
        Returns a copy of this object with the various fields set to the
        values they were given in kwargs.
        """

        rv = DisplayableArguments()
        rv.__dict__.update(self.__dict__)
        rv.__dict__.update(kwargs)

        return rv


default_style = renpy.style.Style("default")


class Displayable(renpy.object.Object):
    """
    The base class for every object in Ren'Py that can be
    displayed to the screen.

    Drawables will be serialized to a savegame file. Therefore, they
    shouldn't store non-serializable things (like pygame surfaces) in
    their fields.
    """

    # Some invariants about method call order:
    #
    # per_interact is called before render.
    # render is called before event.
    #
    # get_placement can be called at any time, so can't
    # assume anything.

    # If True this displayable can accept focus.
    # If False, it can't, but it keeps its place in the focus order.
    # If None, it does not have a place in the focus order.
    focusable = None

    # This is the focus named assigned by the focus code.
    full_focus_name = None

    # A role ('selected_' or '' that prefixes the style).
    role = ''

    # The event we'll pass on to our parent transform.
    transform_event = None

    # Can we change our look in response to transform_events?
    transform_event_responder = False

    # The main displayable, if this displayable is the root of a composite
    # displayable. (This is used by SL to figure out where to add children
    # to.) If None, it is itself.
    _main = None

    # A list of the children that make up this composite displayable.
    _composite_parts = [ ]

    # The location the displayable was created at, if known.
    _location = None

    # Does this displayable use the scope?
    _uses_scope = False

    # Arguments supplied to this displayable.
    _args = DisplayableArguments()

    # Set to true of the displayable is duplicatable (has a non-trivial
    # duplicate method), or one of its children is.
    _duplicatable = False

    # Does this displayable require clipping?
    _clipping = False

    # Does this displayable have a tooltip?
    _tooltip = None

    def __init__(self, focus=None, default=False, style='default', _args=None, tooltip=None, **properties):

        global default_style

        if (style == "default") and (not properties):
            self.style = default_style
        else:
            self.style = renpy.style.Style(style, properties)  # @UndefinedVariable

        self.focus_name = focus
        self.default = default
        self._tooltip = tooltip

        if _args is not None:
            self._args = _args

    def _copy(self, args=None):
        """
        Makes a shallow copy of the displayable. If `args` is provided,
        replaces the arguments with the stored copy.
        """

        rv = copy.copy(self)

        if args is not None:
            rv._args = args

        return rv

    def _duplicate(self, args):
        """
        Makes a duplicate copy of the following kids of displayables:

        * Displayables that can accept arguments.
        * Displayables that maintain state that should be reset before being
          shown to the user.
        * Containers that contain (including transitively) one of the other
          kinds of displayables.

        Displayables that contain state that can be manipulated by the user
        are never copied.

        This should call _unique on children that have been copied before
        setting its own _duplicatable flag.
        """

        return self

    def _in_current_store(self):
        """
        Returns a version of this displayable that will not change as it is
        rendered.
        """

        return self

    def _unique(self):
        """
        This is called when a displayable is "born" unique, which occurs
        when there is only a single reference to it. What it does is to
        manage the _duplicatable flag - setting it false unless one of
        the displayable's children happens to be duplicatable.
        """

        return

    def parameterize(self, name, parameters):
        """
        Obsolete alias for _duplicate.
        """

        a = self._args.copy(name=name, args=parameters)
        return self._duplicate(a)

    def _equals(self, o):
        """
        This is a utility method that can be called by a Displayable's
        __eq__ method, to compare displayables for type and displayable
        component equality.
        """

        if type(self) is not type(o):
            return False

        if self.focus_name != o.focus_name:
            return False

        if self.style != o.style:
            return False

        if self.default != o.default:
            return False

        return True

    def __unicode__(self):
        return self.__class__.__name__

    def __repr__(self):
        return "<{} at {:x}>".format(unicode(self).encode("utf-8"), id(self))

    def find_focusable(self, callback, focus_name):

        focus_name = self.focus_name or focus_name

        if self.focusable:
            callback(self, focus_name)
        elif self.focusable is not None:
            callback(None, focus_name)

        for i in self.visit():
            if i is None:
                continue

            i.find_focusable(callback, focus_name)

    def focus(self, default=False):
        """
        Called to indicate that this widget has the focus.
        """

        self.set_style_prefix(self.role + "hover_", True)

        if not default:
            renpy.exports.play(self.style.hover_sound)

    def unfocus(self, default=False):
        """
        Called to indicate that this widget has become unfocused.
        """

        self.set_style_prefix(self.role + "idle_", True)

    def is_focused(self):

        if renpy.display.focus.grab and renpy.display.focus.grab is not self:
            return

        return renpy.game.context().scene_lists.focused is self

    def set_style_prefix(self, prefix, root):
        """
        Called to set the style prefix of this widget and its child
        widgets, if any.

        `root` - True if this is the root of a style tree, False if this
        has been passed on to a child.
        """

        if prefix == self.style.prefix:
            return

        self.style.set_prefix(prefix)
        renpy.display.render.redraw(self, 0)

    def render(self, width, height, st, at):
        """
        Called to display this displayable. This is called with width
        and height parameters, which give the largest width and height
        that this drawable can be drawn to without overflowing some
        bounding box. It's also given two times. It returns a Surface
        that is the current image of this drawable.

        @param st: The time since this widget was first shown, in seconds.
        @param at: The time since a similarly named widget was first shown,
        in seconds.
        """

        raise Exception("Render not implemented.")

    def event(self, ev, x, y, st):
        """
        Called to report than an event has occured. Ev is the raw
        pygame event object representing that event. If the event
        involves the mouse, x and y are the translation of the event
        into the coordinates of this displayable. st is the time this
        widget has been shown for.

        @returns A value that should be returned from Interact, or None if
        no value is appropriate.
        """

        return None

    def get_placement(self):
        """
        Returns a style object containing placement information for
        this Displayable. Children are expected to overload this
        to return something more sensible.
        """

        return self.style.get_placement()

    def visit_all(self, callback):
        """
        Calls the callback on this displayable, and then on all children
        of this displayable.
        """

        for d in self.visit():
            if not d:
                continue
            d.visit_all(callback)

        callback(self)

    def visit(self):
        """
        Called to ask the displayable to return a list of its children
        (including children taken from styles). For convenience, this
        list may also include None values.
        """

        return [ ]

    def per_interact(self):
        """
        Called once per widget per interaction.
        """

        return None

    def predict_one(self):
        """
        Called to ask this displayable to call the callback with all
        the images it may want to load.
        """

        return

    def predict_one_action(self):
        """
        Called to ask this displayable to cause image prediction
        to occur for images that may be loaded by its actions.
        """

        return

    def place(self, dest, x, y, width, height, surf, main=True):
        """
        This places a render (which must be of this displayable)
        within a bounding area. Returns an (x, y) tuple giving the location
        the displayable was placed at.

        `dest`
            If not None, the `surf` will be blitted to `dest` at the
            computed coordinates.

        `x`, `y`, `width`, `height`
            The bounding area.

        `surf`
            The render to place.

        `main`
            This is passed to Render.blit().
        """

        placement = self.get_placement()
        subpixel = placement[6]

        xpos, ypos = place(width, height, surf.width, surf.height, placement)

        xpos += x
        ypos += y

        pos = (xpos, ypos)

        if dest is not None:
            if subpixel:
                dest.subpixel_blit(surf, pos, main, main, None)
            else:
                dest.blit(surf, pos, main, main, None)

        return pos

    def set_transform_event(self, event):
        """
        Sets the transform event of this displayable to event.
        """

        if event == self.transform_event:
            return

        self.transform_event = event

        if self.transform_event_responder:
            renpy.display.render.redraw(self, 0)

    def _handles_event(self, event):
        """
        Returns True if the displayable handles event, False otherwise.
        """

        return False

    def _hide(self, st, at, kind):
        """
        Returns None if this displayable is ready to be hidden, or
        a replacement displayable if it doesn't want to be hidden
        quite yet. Kind is either "hide" or "replaced".
        """

        return None

    def _show(self):
        """
        Called when the displayable is added to a scene list.
        """

    def _target(self):
        """
        If this displayable is part of a chain of one or more references,
        returns the ultimate target of those references. Otherwise, returns
        the displayable.
        """

        return self

    def _change_transform_child(self, child):
        """
        If this is a transform, makes a copy of the transform and sets
        the child of the innermost transform to this. Otherwise,
        simply returns child.
        """

        return child

    def _clear(self):
        """
        Clears out the children of this displayable, if any.
        """

        return

    def _tts_common(self, default_alt=None):

        rv = [ ]

        for i in self.visit():
            if i is not None:
                speech = i._tts()

                if speech.strip():
                    rv.append(speech)

        rv = ": ".join(rv)
        rv = rv.replace("::", ":")
        rv = rv.replace(": :", ":")

        alt = self.style.alt

        if alt is None:
            alt = default_alt

        if alt is not None:
            rv = renpy.substitutions.substitute(alt, scope={ "text" : rv })[0]

        return rv

    def _tts(self):
        """
        Returns the self-voicing text of this displayable and all of its
        children that cannot take focus. If the displayable can take focus,
        returns the empty string.
        """

        return self._tts_common()

    def _tts_all(self):
        """
        Returns the self-voicing text of this displayable and all of its
        children that cannot take focus.
        """
        return self._tts_common()


class SceneListEntry(renpy.object.Object):
    """
    Represents a scene list entry. Since this was replacing a tuple,
    it should be treated as immutable after its initial creation.
    """

    def __init__(self, tag, zorder, show_time, animation_time, displayable, name):
        self.tag = tag
        self.zorder = zorder
        self.show_time = show_time
        self.animation_time = animation_time
        self.displayable = displayable
        self.name = name

    def __iter__(self):
        return iter((self.tag, self.zorder, self.show_time, self.animation_time, self.displayable))

    def __getitem__(self, index):
        return (self.tag, self.zorder, self.show_time, self.animation_time, self.displayable)[index]

    def __repr__(self):
        return "<SLE: %r %r %r>" % (self.tag, self.name, self.displayable)

    def copy(self):
        return SceneListEntry(
            self.tag,
            self.zorder,
            self.show_time,
            self.animation_time,
            self.displayable,
            self.name)

    def update_time(self, time):

        rv = self

        if self.show_time is None or self.animation_time is None:
            rv = self.copy()
            rv.show_time = rv.show_time or time
            rv.animation_time = rv.animation_time or time

        return rv


class SceneLists(renpy.object.Object):
    """
    This stores the current scene lists that are being used to display
    things to the user.
    """

    __version__ = 7

    def after_setstate(self):
        for i in renpy.config.layers + renpy.config.top_layers:
            if i not in self.layers:
                self.layers[i] = [ ]
                self.at_list[i] = { }
                self.layer_at_list[i] = (None, [ ])

    def after_upgrade(self, version):

        if version < 1:

            self.at_list = { }
            self.layer_at_list = { }

            for i in renpy.config.layers + renpy.config.top_layers:
                self.at_list[i] = { }
                self.layer_at_list[i] = (None, [ ])

        if version < 3:
            self.shown_window = False

        if version < 4:
            for k in self.layers:
                self.layers[k] = [ SceneListEntry(*(i + (None,)) ) for i in self.layers[k] ]

            self.additional_transient = [ ]

        if version < 5:
            self.drag_group = None

        if version < 6:
            self.shown = self.image_predict_info

        if version < 7:
            self.layer_transform = { }

    def __init__(self, oldsl, shown):

        super(SceneLists, self).__init__()

        # Has a window been shown as part of these scene lists?
        self.shown_window = False

        # A map from layer name -> list(SceneListEntry)
        self.layers = { }

        # A map from layer name -> tag -> at_list associated with that tag.
        self.at_list = { }

        # A map from layer to (star time, at_list), where the at list has
        # been applied to the layer as a whole.
        self.layer_at_list = { }

        # The current shown images,
        self.shown = shown

        # A list of (layer, tag) pairs that are considered to be
        # transient.
        self.additional_transient = [ ]

        # Either None, or a DragGroup that's used as the default for
        # drags with names.
        self.drag_group = None

        # A map from a layer to the transform that applies to that
        # layer.
        self.layer_transform = { }

        if oldsl:

            for i in renpy.config.layers + renpy.config.top_layers:

                try:
                    self.layers[i] = oldsl.layers[i][:]
                except KeyError:
                    self.layers[i] = [ ]

                if i in oldsl.at_list:
                    self.at_list[i] = oldsl.at_list[i].copy()
                    self.layer_at_list[i] = oldsl.layer_at_list[i]
                else:
                    self.at_list[i] = { }
                    self.layer_at_list[i] = (None, [ ])

            for i in renpy.config.overlay_layers:
                self.clear(i)

            self.replace_transient(prefix=None)

            self.focused = None

            self.drag_group = oldsl.drag_group

            self.layer_transform.update(oldsl.layer_transform)

        else:
            for i in renpy.config.layers + renpy.config.top_layers:
                self.layers[i] = [ ]
                self.at_list[i] = { }
                self.layer_at_list[i] = (None, [ ])

            self.music = None
            self.focused = None

    def replace_transient(self, prefix="hide"):
        """
        Replaces the contents of the transient display list with
        a copy of the master display list. This is used after a
        scene is displayed to get rid of transitions and interface
        elements.

        `prefix`
            The prefix/event to use. Set this to None to prevent the hide
            from happening.
        """

        for i in renpy.config.transient_layers:
            self.clear(i, True)

        for layer, tag in self.additional_transient:
            self.remove(layer, tag, prefix=prefix)

        self.additional_transient = [ ]

    def transient_is_empty(self):
        """
        This returns True if all transient layers are empty. This is
        used by the rollback code, as we can't start a new rollback
        if there is something in a transient layer (as things in the
        transient layer may contain objects that cannot be pickled,
        like lambdas.)
        """

        for i in renpy.config.transient_layers:
            if self.layers[i]:
                return False

        return True

    def transform_state(self, old_thing, new_thing, execution=False):
        """
        If the old thing is a transform, then move the state of that transform
        to the new thing.
        """

        if old_thing is None:
            return new_thing

        # Don't bother wrapping screens, as they can't be transformed.
        if isinstance(new_thing, renpy.display.screen.ScreenDisplayable):
            return new_thing

        if renpy.config.take_state_from_target:
            old_transform = old_thing._target()
        else:
            old_transform = old_thing

        if not isinstance(old_transform, renpy.display.motion.Transform):
            return new_thing

        if renpy.config.take_state_from_target:
            new_transform = new_thing._target()
        else:
            new_transform = new_thing

        if not isinstance(new_transform, renpy.display.motion.Transform):
            new_thing = new_transform = renpy.display.motion.Transform(child=new_thing)

        new_transform.take_state(old_transform)

        if execution:
            new_transform.take_execution_state(old_transform)

        return new_thing

    def find_index(self, layer, tag, zorder, behind):
        """
        This finds the spot in the named layer where we should insert the
        displayable. It returns two things: an index at which the new thing
        should be added, and an index at which the old thing should be hidden.
        (Note that the indexes are relative to the current state of the list,
        which may change on an add or remove.)
        """

        add_index = None
        remove_index = None

        for i, sle in enumerate(self.layers[layer]):

            if remove_index is None:
                if (sle.tag and sle.tag == tag) or sle.displayable == tag:
                    remove_index = i

                    if zorder is None:
                        zorder = sle.zorder

        if zorder is None:
            zorder = renpy.config.tag_zorder.get(tag, 0)

        for i, sle in enumerate(self.layers[layer]):

            if add_index is None:

                if sle.zorder == zorder:
                    if sle.tag and (sle.tag == tag or sle.tag in behind):
                        add_index = i

                elif sle.zorder > zorder:
                    add_index = i

        if add_index is None:
            add_index = len(self.layers[layer])

        return add_index, remove_index, zorder

    def add(self,
            layer,
            thing,
            key=None,
            zorder=0,
            behind=[ ],
            at_list=[ ],
            name=None,
            atl=None,
            default_transform=None,
            transient=False,
            keep_st=False):
        """
        Adds something to this scene list. Some of these names are quite a bit
        out of date.

        `thing` - The displayable to add.

        `key` - A string giving the tag associated with this thing.

        `zorder` - Where to place this thing in the zorder, an integer
        A greater value means closer to the user.

        `behind` - A list of tags to place the thing behind.

        `at_list` - The at_list associated with this
        displayable. Counterintunitively, this is not actually
        applied, but merely stored for future use.

        `name` - The full name of the image being displayed. This is used for
        image lookup.

        `atl` - If not None, an atl block applied to the thing. (This actually is
        applied here.)

        `default_transform` - The default transform that is used to initialized
        the values in the other transforms.

        `keep_st`
            If true, we preserve the shown time of a replaced displayable.
        """

        if not isinstance(thing, Displayable):
            raise Exception("Attempting to show something that isn't a displayable:" + repr(thing))

        if layer not in self.layers:
            raise Exception("Trying to add something to non-existent layer '%s'." % layer)

        if key:
            self.remove_hide_replaced(layer, key)
            self.at_list[layer][key] = at_list

        if key and name:
            self.shown.predict_show(layer, name)

        if transient:
            self.additional_transient.append((layer, key))

        l = self.layers[layer]

        if atl:
            thing = renpy.display.motion.ATLTransform(atl, child=thing)

        add_index, remove_index, zorder = self.find_index(layer, key, zorder, behind)

        at = None
        st = None

        if remove_index is not None:
            sle = l[remove_index]
            old = sle.displayable

            at = sle.animation_time

            if keep_st:
                st = sle.show_time

            if (not atl and
                    not at_list and
                    renpy.config.keep_running_transform and
                    isinstance(old, renpy.display.motion.Transform)):

                thing = sle.displayable._change_transform_child(thing)
            else:
                thing = self.transform_state(l[remove_index].displayable, thing)

            thing.set_transform_event("replace")
            thing._show()

        else:

            if not isinstance(thing, renpy.display.motion.Transform):
                thing = self.transform_state(default_transform, thing)

            thing.set_transform_event("show")
            thing._show()

        sle = SceneListEntry(key, zorder, st, at, thing, name)
        l.insert(add_index, sle)

        if remove_index is not None:
            if add_index <= remove_index:
                remove_index += 1

            self.hide_or_replace(layer, remove_index, "replaced")

    def hide_or_replace(self, layer, index, prefix):
        """
        Hides or replaces the scene list entry at the given
        index. `prefix` is a prefix that is used if the entry
        decides it doesn't want to be hidden quite yet.
        """

        if index is None:
            return

        l = self.layers[layer]
        oldsle = l[index]

        now = get_time()

        st = oldsle.show_time or now
        at = oldsle.animation_time or now

        if renpy.config.fast_unhandled_event:
            if not oldsle.displayable._handles_event(prefix):
                prefix = None

        if (prefix is not None) and oldsle.tag:

            d = oldsle.displayable._hide(now - st, now - at, prefix)

            # _hide can mutate the layers, so we need to recompute
            # index.
            index = l.index(oldsle)

            if d is not None:

                sle = SceneListEntry(
                    prefix + "$" + oldsle.tag,
                    oldsle.zorder,
                    st,
                    at,
                    d,
                    None)

                l[index] = sle

                return

        l.pop(index)

    def get_all_displayables(self):
        """
        Gets all displayables reachable from this scene list.
        """

        rv = [ ]
        for l in self.layers.itervalues():
            for sle in l:
                rv.append(sle.displayable)

        return rv

    def remove_above(self, layer, thing):
        """
        Removes everything on the layer that is closer to the user
        than thing, which may be either a tag or a displayable. Thing must
        be displayed, or everything will be removed.
        """

        for i in reversed(xrange(len(self.layers[layer]))):

            sle = self.layers[layer][i]

            if thing:
                if sle.tag == thing or sle.displayable == thing:
                    break

            if sle.tag and "$" in sle.tag:
                continue

            self.hide_or_replace(layer, i, "hide")

    def remove(self, layer, thing, prefix="hide"):
        """
        Thing is either a key or a displayable. This iterates through the
        named layer, searching for entries matching the thing.
        When they are found, they are removed from the displaylist.

        It's not an error to remove something that isn't in the layer in
        the first place.
        """

        if layer not in self.layers:
            raise Exception("Trying to remove something from non-existent layer '%s'." % layer)

        _add_index, remove_index, _zorder = self.find_index(layer, thing, 0, [ ])

        if remove_index is not None:
            tag = self.layers[layer][remove_index].tag

            if tag:
                self.shown.predict_hide(layer, (tag,))
                self.at_list[layer].pop(tag, None)

            self.hide_or_replace(layer, remove_index, prefix)

    def clear(self, layer, hide=False):
        """
        Clears the named layer, making it empty.

        If hide is True, then objects are hidden. Otherwise, they are
        totally wiped out.
        """

        if layer not in self.layers:
            return

        if not hide:
            self.layers[layer] = [ ]

        else:

            # Have to iterate in reverse order, since otherwise
            # the indexes might change.
            for i in reversed(xrange(len(self.layers[layer]))):
                self.hide_or_replace(layer, i, hide)

        self.at_list[layer].clear()
        self.shown.predict_scene(layer)
        self.layer_at_list[layer] = (None, [ ])

    def set_layer_at_list(self, layer, at_list, reset=True):
        self.layer_at_list[layer] = (None, list(at_list))

        if reset:
            self.layer_transform[layer] = None

    def set_times(self, time):
        """
        This finds entries with a time of None, and replaces that
        time with the given time.
        """

        for l, (t, list) in self.layer_at_list.items():  # @ReservedAssignment
            self.layer_at_list[l] = (t or time, list)

        for l, ll in self.layers.iteritems():
            self.layers[l] = [ i.update_time(time) for i in ll ]

    def showing(self, layer, name):
        """
        Returns true if something with the prefix of the given name
        is found in the scene list.
        """

        return self.shown.showing(layer, name)

    def get_showing_tags(self, layer):
        return self.shown.get_showing_tags(layer)

    def make_layer(self, layer, properties):
        """
        Creates a Fixed with the given layer name and scene_list.
        """

        rv = renpy.display.layout.MultiBox(layout='fixed', focus=layer, **properties)
        rv.append_scene_list(self.layers[layer])
        rv.layer_name = layer
        rv._duplicatable = False

        time, at_list = self.layer_at_list[layer]

        old_transform = self.layer_transform.get(layer, None)
        new_transform = None

        if at_list:

            for a in at_list:

                if isinstance(a, renpy.display.motion.Transform):
                    rv = a(child=rv)
                    new_transform = rv
                else:
                    rv = a(rv)

            if (new_transform is not None) and (renpy.config.keep_show_layer_state):
                self.transform_state(old_transform, new_transform, execution=True)

            f = renpy.display.layout.MultiBox(layout='fixed')
            f.add(rv, time, time)
            f.layer_name = layer

            rv = f

        self.layer_transform[layer] = new_transform

        return rv

    def remove_hide_replaced(self, layer, tag):
        """
        Removes things that are hiding or replaced, that have the given
        tag.
        """

        hide_tag = "hide$" + tag
        replaced_tag = "replaced$" + tag

        l = self.layers[layer]
        self.layers[layer] = [ i for i in l if i.tag != hide_tag and i.tag != replaced_tag ]

    def remove_hidden(self):
        """
        Goes through all of the layers, and removes things that are
        hidden and are no longer being kept alive by their hide
        methods.
        """

        now = get_time()

        for l in self.layers:
            newl = [ ]

            for sle in self.layers[l]:

                if sle.tag:

                    if sle.tag.startswith("hide$"):
                        d = sle.displayable._hide(now - sle.show_time, now - sle.animation_time, "hide")
                        if not d:
                            continue

                    elif sle.tag.startswith("replaced$"):
                        d = sle.displayable._hide(now - sle.show_time, now - sle.animation_time, "replaced")
                        if not d:
                            continue

                newl.append(sle)

            self.layers[l] = newl

    def remove_all_hidden(self):
        """
        Removes everything hidden, even if it's not time yet. (Used when making a rollback copy).
        """

        for l in self.layers:
            newl = [ ]

            for sle in self.layers[l]:

                if sle.tag:

                    if "$" in sle.tag:
                        continue

                newl.append(sle)

            self.layers[l] = newl

    def get_displayable_by_tag(self, layer, tag):
        """
        Returns the displayable on the layer with the given tag, or None
        if no such displayable exists. Note that this will usually return
        a Transform.
        """

        if layer not in self.layers:
            raise Exception("Unknown layer %r." % layer)

        for sle in self.layers[layer]:
            if sle.tag == tag:
                return sle.displayable

        return None

    def get_displayable_by_name(self, layer, name):
        """
        Returns the displayable on the layer with the given name, or None
        if no such displayable exists. Note that this will usually return
        a Transform.
        """

        if layer not in self.layers:
            raise Exception("Unknown layer %r." % layer)

        for sle in self.layers[layer]:
            if sle.name == name:
                return sle.displayable

        return None

    def get_image_bounds(self, layer, tag, width, height):
        """
        Implements renpy.get_image_bounds().
        """

        if layer not in self.layers:
            raise Exception("Unknown layer %r." % layer)

        for sle in self.layers[layer]:
            if sle.tag == tag:
                break
        else:
            return None

        now = get_time()

        if sle.show_time is not None:
            st = now - sle.show_time
        else:
            st = 0

        if sle.animation_time is not None:
            at = now - sle.animation_time
        else:
            at = 0

        surf = renpy.display.render.render(sle.displayable, width, height, st, at)

        sw = surf.width
        sh = surf.height

        x, y = place(width, height, sw, sh, sle.displayable.get_placement())

        surf.kill()

        return (x, y, sw, sh)


def scene_lists(index=-1):
    """
    Returns either the current scenelists object, or the one for the
    context at the given index.
    """

    return renpy.game.context(index).scene_lists


class MouseMove(object):
    """
    This contains information about the current mouse move.
    """

    def __init__(self, x, y, duration):
        self.start = get_time()

        if duration is not None:
            self.duration = duration
        else:
            self.duration = 0

        self.start_x, self.start_y = renpy.display.draw.get_mouse_pos()

        self.end_x = x
        self.end_y = y

    def perform(self):
        """
        Performs the mouse move. Returns True if this should be called
        again, or False if the move has finished.
        """

        elapsed = get_time() - self.start

        if elapsed >= self.duration:
            renpy.display.draw.set_mouse_pos(self.end_x, self.end_y)
            return False

        done = 1.0 * elapsed / self.duration

        x = int(self.start_x + done * (self.end_x - self.start_x))
        y = int(self.start_y + done * (self.end_y - self.start_y))

        renpy.display.draw.set_mouse_pos(x, y)
        return True


def get_safe_mode():
    """
    Returns true if we should go into safe mode.
    """

    if renpy.safe_mode_checked:
        return False

    try:
        if renpy.windows:
            import ctypes

            VK_SHIFT      = 0x10

            ctypes.windll.user32.GetKeyState.restype = ctypes.c_ushort
            if ctypes.windll.user32.GetKeyState(VK_SHIFT) & 0x8000:
                return True
            else:
                return False

        # Safe mode doesn't work on other platforms.
        return False

    except:
        return False


# How long should we be in maximum framerate mode at the start of the game?
initial_maximum_framerate = 0.0


class Interface(object):
    """
    This represents the user interface that interacts with the user.
    It manages the Display objects that display things to the user, and
    also handles accepting and responding to user input.

    @ivar display: The display that we used to display the screen.

    @ivar profile_time: The time of the last profiling.

    @ivar screenshot: A screenshot, or None if no screenshot has been
    taken.

    @ivar old_scene: The last thing that was displayed to the screen.

    @ivar transition: A map from layer name to the transition that will
    be applied the next time interact restarts.

    @ivar transition_time: A map from layer name to the time the transition
    involving that layer started.

    @ivar transition_from: A map from layer name to the scene that we're
    transitioning from on that layer.

    @ivar suppress_transition: If True, then the next transition will not
    happen.

    @ivar force_redraw: If True, a redraw is forced.

    @ivar restart_interaction: If True, the current interaction will
    be restarted.

    @ivar pushed_event: If not None, an event that was pushed back
    onto the stack.

    @ivar mouse: The name of the mouse cursor to use during the current
    interaction.

    @ivar ticks: The number of 20hz ticks.

    @ivar frame_time: The time at which we began drawing this frame.

    @ivar interact_time: The time of the start of the first frame of the current interact_core.

    @ivar time_event: A singleton ignored event.

    @ivar event_time: The time of the current event.

    @ivar timeout_time: The time at which the timeout will occur.
    """

    def __init__(self):

        # PNG data and the surface for the current file screenshot.
        self.screenshot = None
        self.screenshot_surface = None

        self.old_scene = { }
        self.transition = { }
        self.ongoing_transition = { }
        self.transition_time = { }
        self.transition_from = { }
        self.suppress_transition = False
        self.quick_quit = False
        self.force_redraw = False
        self.restart_interaction = False
        self.pushed_event = None
        self.ticks = 0
        self.mouse = 'default'
        self.timeout_time = None
        self.last_event = None
        self.current_context = None
        self.roll_forward = None

        # Things to be preloaded.
        self.preloads = [ ]

        # The time at which this draw occurs.
        self.frame_time = 0

        # The time when this interaction occured.
        self.interact_time = None

        # The time we last tried to quit.
        self.quit_time = 0

        # Are we currently processing the quit event?
        self.in_quit_event = False

        self.time_event = pygame.event.Event(TIMEEVENT)
        self.redraw_event = pygame.event.Event(REDRAW)

        # Are we focused?
        self.mouse_focused = True
        self.keyboard_focused = True

        # Properties for each layer.
        self.layer_properties = { }

        # Have we shown the window this interaction?
        self.shown_window = False

        # Are we in fullscren mode?
        self.fullscreen = False

        # Should we ignore the rest of the current touch? Used to ignore the
        # rest of a mousepress after a longpress occurs.
        self.ignore_touch = False

        for layer in renpy.config.layers + renpy.config.top_layers:
            if layer in renpy.config.layer_clipping:
                x, y, w, h = renpy.config.layer_clipping[layer]
                self.layer_properties[layer] = dict(
                    xpos=x,
                    xanchor=0,
                    ypos=y,
                    yanchor=0,
                    xmaximum=w,
                    ymaximum=h,
                    xminimum=w,
                    yminimum=h,
                    clipping=True,
                    )

            else:
                self.layer_properties[layer] = dict()

        # A stack giving the values of self.transition and self.transition_time
        # for contexts outside the current one. This is used to restore those
        # in the case where nothing has changed in the new context.
        self.transition_info_stack = [ ]

        # The time when the event was dispatched.
        self.event_time = 0

        # The time we saw the last mouse event.
        self.mouse_event_time = None

        # Should we show the mouse?
        self.show_mouse = True

        # Should we reset the display?
        self.display_reset = False

        # The last size we were resized to.
        self.last_resize = None

        # The thread that can do display operations.
        self.thread = threading.current_thread()

        # Initialize audio.
        renpy.audio.audio.init()

        # Initialize pygame.
        try:
            pygame.display.init()
        except:
            pass

        # Init timing.
        init_time()
        self.mouse_event_time = get_time()

        # The current window caption.
        self.window_caption = None

        renpy.game.interface = self
        renpy.display.interface = self

        # Are we in safe mode, from holding down shift at start?
        self.safe_mode = False

        # Do we need a background screenshot?
        self.bgscreenshot_needed = False

        # Event used to signal background screenshot taken.
        self.bgscreenshot_event = threading.Event()

        # The background screenshot surface.
        self.bgscreenshot_surface = None

        # Mouse move. If not None, information about the current mouse
        # move.
        self.mouse_move = None

        # If in text editing mode, the current text editing event.
        self.text_editing = None

        # The text rectangle after the current draw.
        self.text_rect = None

        # The text rectangle after the previous draw.
        self.old_text_rect = None

        # Are we a touchscreen?
        self.touch = renpy.exports.variant("touch")

        # Should we restart the interaction?
        self.restart_interaction = True

        # For compatibility with older code.
        if renpy.config.periodic_callback:
            renpy.config.periodic_callbacks.append(renpy.config.periodic_callback)

        renpy.display.emulator.init_emulator()

        # Has start been called?
        self.started = False

        # Are we in fullscreen video mode?
        self.fullscreen_video = False

        self.safe_mode = get_safe_mode()
        renpy.safe_mode_checked = True

        # A scale factor used to compensate for the system DPI.
        self.dpi_scale = self.setup_dpi_scaling()

        renpy.display.log.write("DPI scale factor: %f", self.dpi_scale)

        # A time until which we should draw at maximum framerate.
        self.maximum_framerate_time = 0.0
        self.maximum_framerate(initial_maximum_framerate)

        # True if this is the first interact.
        self.start_interact = True

        # The time of each frame.
        self.frame_times = [ ]

        # The duration of each frame, in seconds.
        self.frame_duration = 1.0 / 60.0

    def setup_dpi_scaling(self):

        if "RENPY_HIGHDPI" in os.environ:
            return float(os.environ["RENPY_HIGHDPI"])

        if not renpy.windows:
            return 1.0

        try:
            import ctypes
            from ctypes import c_void_p, c_int

            ctypes.windll.user32.SetProcessDPIAware()

            GetDC = ctypes.windll.user32.GetDC
            GetDC.restype = c_void_p
            GetDC.argtypes = [ c_void_p ]

            ReleaseDC = ctypes.windll.user32.ReleaseDC
            ReleaseDC.argtypes = [ c_void_p, c_void_p ]

            GetDeviceCaps = ctypes.windll.gdi32.GetDeviceCaps
            GetDeviceCaps.restype = c_int
            GetDeviceCaps.argtypes = [ c_void_p, c_int ]

            LOGPIXELSX = 88

            dc = GetDC(None)
            rv = GetDeviceCaps(dc, LOGPIXELSX) / 96.0
            ReleaseDC(None, dc)

            if rv < renpy.config.de_minimus_dpi_scale:
                renpy.display.log.write("De minimus DPI scale, was %r", rv)
                rv = 1.0

            return rv

        except:
            renpy.display.log.write("Could not determine DPI scale factor:")
            renpy.display.log.exception()
            return 1.0

    def start(self):
        """
        Starts the interface, by opening a window and setting the mode.
        """

        if self.started:
            return

        gc.collect()

        if gc.garbage:
            gc.garbage[:] = [ ]

        renpy.display.render.render_ready()

        # Kill off the presplash.
        renpy.display.presplash.end()

        renpy.main.log_clock("Interface start")

        self.started = True

        self.set_mode()

        # Load the image fonts.
        renpy.text.font.load_fonts()

        # Setup periodic event.
        pygame.time.set_timer(PERIODIC, PERIODIC_INTERVAL)

        # Don't grab the screen.
        pygame.event.set_grab(False)

        if not self.safe_mode:
            renpy.display.controller.init()

        s = "Total time until interface ready: {}s".format(time.time() - import_time)

        renpy.display.log.write(s)

        if renpy.android and not renpy.config.log_to_stdout:
            print(s)

    def post_init(self):
        """
        This is called after display init, but before the window is created.
        """

        # Needed for Unity.
        wmclass = renpy.config.save_directory or os.path.basename(sys.argv[0])
        os.environ[b'SDL_VIDEO_X11_WMCLASS'] = wmclass.encode("utf-8")

        self.set_window_caption(force=True)
        self.set_icon()

        if renpy.config.key_repeat is not None:
            delay, repeat_delay = renpy.config.key_repeat
            pygame.key.set_repeat(int(1000 * delay), int(1000 * repeat_delay))

        if android:
            android.wakelock(True)

        # Block events we don't use.
        for i in pygame.event.get_standard_events():

            if i in enabled_events:
                continue

            if i in renpy.config.pygame_events:
                continue

            pygame.event.set_blocked(i)

    def set_icon(self):
        """
        This is called to set up the window icon.
        """

        # Window icon.
        icon = renpy.config.window_icon

        if icon:

            im = renpy.display.scale.image_load_unscaled(
                renpy.loader.load(icon),
                icon,
                )

            # Convert the aspect ratio to be square.
            iw, ih = im.get_size()
            imax = max(iw, ih)
            square_im = renpy.display.pgrender.surface_unscaled((imax, imax), True)
            square_im.blit(im, ( (imax-iw)/2, (imax-ih)/2 ))
            im = square_im

            pygame.display.set_icon(im)

    def set_window_caption(self, force=False):

        window_title = renpy.config.window_title

        if window_title is None:
            window_title = "A Ren'Py Game"

        caption = renpy.translation.translate_string(window_title) + renpy.store._window_subtitle

        if renpy.exports.get_autoreload():
            caption += " - autoreload"

        if not force and caption == self.window_caption:
            return

        self.window_caption = caption
        pygame.display.set_caption(caption.encode("utf-8"))

    def iconify(self):
        pygame.display.iconify()

    def get_draw_constructors(self):
        """
        Figures out the list of draw constructors to try.
        """

        renderer = renpy.game.preferences.renderer
        renderer = os.environ.get("RENPY_RENDERER", renderer)

        if self.safe_mode:
            renderer = "sw"

        renpy.config.renderer = renderer

        if renderer == "auto":
            if renpy.windows:
                renderers = [ "gl", "angle", "sw" ]
            else:
                renderers = [ "gl", "sw" ]
        else:
            renderers = [ renderer, "sw" ]

        draw_objects = { }

        def make_draw(name, mod, cls, *args):
            if name not in renderers:
                return False

            try:
                __import__(mod)
                module = sys.modules[mod]
                draw_class = getattr(module, cls)
                draw_objects[name] = draw_class(*args)
                return True

            except:
                renpy.display.log.write("Couldn't import {0} renderer:".format(name))
                renpy.display.log.exception()

                return False

        if renpy.windows:
            has_angle = make_draw("angle", "renpy.angle.gldraw", "GLDraw")
        else:
            has_angle = False

        make_draw("gl", "renpy.gl.gldraw", "GLDraw", not has_angle)
        make_draw("sw", "renpy.display.swdraw", "SWDraw")

        rv = [ ]

        def append_draw(name):
            if name in draw_objects:
                rv.append(draw_objects[name])
            else:
                renpy.display.log.write("Unknown renderer: {0}".format(name))

        for i in renderers:
            append_draw(i)

        return rv

    def kill_textures(self):
        renpy.display.render.free_memory()
        renpy.text.text.layout_cache_clear()

    def kill_textures_and_surfaces(self):
        """
        Kill all textures and surfaces that are loaded.
        """

        self.kill_textures()

        renpy.display.im.cache.clear()
        renpy.display.module.bo_cache = None

    def set_mode(self, physical_size=None):
        """
        This sets the video mode. It also picks the draw object.
        """

        # Ensure that we kill off the movie when changing screen res.
        if renpy.display.draw and renpy.display.draw.info["renderer"] == "sw":
            renpy.display.video.movie_stop(clear=False)

        if self.display_reset:

            pygame.key.stop_text_input()  # @UndefinedVariable
            pygame.key.set_text_input_rect(None)  # @UndefinedVariable
            self.text_rect = None

            renpy.display.draw.deinit()

            if renpy.display.draw.info["renderer"] == "angle":
                renpy.display.draw.quit()

                # This is necessary to fix a bug with restoring a window from
                # minimized state on windows.
                pygame.display.quit()

        renpy.display.render.free_memory()
        renpy.display.im.cache.clear()
        renpy.text.text.layout_cache_clear()

        renpy.display.module.bo_cache = None

        self.kill_textures_and_surfaces()

        self.old_text_rect = None
        self.display_reset = False

        virtual_size = (renpy.config.screen_width, renpy.config.screen_height)

        if physical_size is None:
            if renpy.mobile or renpy.game.preferences.physical_size is None:  # @UndefinedVariable
                physical_size = (None, None)
            else:
                physical_size = renpy.game.preferences.physical_size

        # Setup screen.
        fullscreen = renpy.game.preferences.fullscreen

        old_fullscreen = self.fullscreen
        self.fullscreen = fullscreen

        if os.environ.get('RENPY_DISABLE_FULLSCREEN', False):
            fullscreen = False
            self.fullscreen = renpy.game.preferences.fullscreen

        if renpy.display.draw:
            draws = [ renpy.display.draw ]
        else:
            draws = self.get_draw_constructors()

        for draw in draws:
            if draw.set_mode(virtual_size, physical_size, fullscreen):
                renpy.display.draw = draw
                break
            else:
                # pygame.display.quit()
                pass
        else:
            # Ensure we don't get stuck in fullscreen.
            renpy.game.preferences.fullscreen = False
            raise Exception("Could not set video mode.")

        # Save the video size.
        if renpy.config.save_physical_size and not fullscreen and not old_fullscreen:
            renpy.game.preferences.physical_size = renpy.display.draw.get_physical_size()

        if android:
            android.init()

        # We need to redraw the (now blank) screen.
        self.force_redraw = True

        # Assume we have focus until told otherwise.
        self.mouse_focused = True
        self.keyboard_focused = True

        # Assume we're not minimized.
        self.minimized = False

        # Force an interaction restart.
        self.restart_interaction = True

        # True if we're doing a one-time profile.
        self.profile_once = False

        # Clear the frame times.
        self.frame_times = [ ]

    def draw_screen(self, root_widget, fullscreen_video, draw):

        try:
            renpy.display.render.per_frame = True
            renpy.display.screen.per_frame()
        finally:
            renpy.display.render.per_frame = False

        surftree = renpy.display.render.render_screen(
            root_widget,
            renpy.config.screen_width,
            renpy.config.screen_height,
            )

        if draw:
            renpy.display.draw.draw_screen(surftree, fullscreen_video)

        now = time.time()

        self.frame_times.append(now)

        while (now - self.frame_times[0]) > renpy.config.performance_window:
            self.frame_times.pop(0)

        renpy.display.render.mark_sweep()
        renpy.display.focus.take_focuses()

        self.surftree = surftree
        self.fullscreen_video = fullscreen_video

    def take_screenshot(self, scale, background=False):
        """
        This takes a screenshot of the current screen, and stores it so
        that it can gotten using get_screenshot()

        `background`
           If true, we're in a background thread. So queue the request
           until it can be handled by the main thread.
        """

        # Do nothing before the first interaction.
        if not self.started:
            return

        if background:
            self.bgscreenshot_event.clear()
            self.bgscreenshot_needed = True

            if not self.bgscreenshot_event.wait(1.0):
                raise Exception("Screenshot timed out.")

            surf = self.bgscreenshot_surface
            self.bgscreenshot_surface = None

        else:

            surf = renpy.display.draw.screenshot(self.surftree, self.fullscreen_video)

        surf = renpy.display.scale.smoothscale(surf, scale)

        renpy.display.render.mutated_surface(surf)

        self.screenshot_surface = surf

        sio = cStringIO.StringIO()
        renpy.display.module.save_png(surf, sio, 0)
        self.screenshot = sio.getvalue()
        sio.close()

    def check_background_screenshot(self):
        """
        Handles requests for a background screenshot.
        """

        if self.bgscreenshot_needed:
            self.bgscreenshot_needed = False
            self.bgscreenshot_surface = renpy.display.draw.screenshot(self.surftree, self.fullscreen_video)
            self.bgscreenshot_event.set()

    def get_screenshot(self):
        """
        Gets the current screenshot, as a string. Returns None if there isn't
        a current screenshot.
        """

        if not self.started:
            self.start()

        rv = self.screenshot

        if not rv:
            self.take_screenshot(
                (renpy.config.thumbnail_width, renpy.config.thumbnail_height),
                background=(threading.current_thread() is not self.thread),
                )
            rv = self.screenshot
            self.lose_screenshot()

        return rv

    def lose_screenshot(self):
        """
        This deallocates the saved screenshot.
        """

        self.screenshot = None
        self.screenshot_surface = None

    def save_screenshot(self, filename):
        """
        Saves a full-size screenshot in the given filename.
        """

        window = renpy.display.draw.screenshot(self.surftree, self.fullscreen_video)

        if renpy.config.screenshot_crop:
            window = window.subsurface(renpy.config.screenshot_crop)

        try:
            renpy.display.scale.image_save_unscaled(window, filename)
            return True
        except:
            if renpy.config.debug:
                raise

            return False

    def show_window(self):

        if not renpy.store._window:
            return

        if not renpy.game.preferences.show_empty_window:
            return

        if renpy.game.context().scene_lists.shown_window:
            return

        if renpy.config.empty_window:

            old_history = renpy.store._history  # @UndefinedVariable
            renpy.store._history = False

            PPP("empty window")

            try:
                renpy.config.empty_window()
            finally:
                renpy.store._history = old_history

    def do_with(self, trans, paired, clear=False):

        if renpy.config.with_callback:
            trans = renpy.config.with_callback(trans, paired)

        if (not trans) or self.suppress_transition:
            self.with_none()
            return False
        else:
            self.set_transition(trans)
            return self.interact(trans_pause=True,
                                 suppress_overlay=not renpy.config.overlay_during_with,
                                 mouse='with',
                                 clear=clear)

    def with_none(self, overlay=True):
        """
        Implements the with None command, which sets the scene we will
        be transitioning from.
        """

        PPP("start of with none")

        renpy.game.context().say_attributes = None

        # Show the window, if that's necessary.
        self.show_window()

        # Compute the overlay.
        if overlay:
            self.compute_overlay()

        scene_lists = renpy.game.context().scene_lists

        # Compute the scene.
        for layer, d in self.compute_scene(scene_lists).iteritems():
            if layer not in self.transition:
                self.old_scene[layer] = d

        # Get rid of transient things.
        for i in renpy.config.overlay_layers:
            scene_lists.clear(i)

        scene_lists.replace_transient()
        scene_lists.shown_window = False

    def set_transition(self, transition, layer=None, force=False):
        """
        Sets the transition that will be performed as part of the next
        interaction.
        """

        if self.suppress_transition and not force:
            return

        if transition is None:
            self.transition.pop(layer, None)
        else:
            self.transition[layer] = transition

    def event_peek(self):
        """
        This peeks the next event. It returns None if no event exists.
        """

        if self.pushed_event:
            return self.pushed_event

        ev = pygame.event.poll()

        if ev.type == pygame.NOEVENT:
            # Seems to prevent the CPU from speeding up.
            renpy.display.draw.event_peek_sleep()
            return None

        self.pushed_event = ev

        return ev

    def event_poll(self):
        """
        Called to busy-wait for an event while we're waiting to
        redraw a frame.
        """

        if self.pushed_event:
            rv = self.pushed_event
            self.pushed_event = None
        else:
            rv = pygame.event.poll()

        self.last_event = rv

        return rv

    def event_wait(self):
        """
        This is in its own function so that we can track in the
        profiler how much time is spent in interact.
        """

        if self.pushed_event:
            rv = self.pushed_event
            self.pushed_event = None
            self.last_event = rv
            return rv

        self.check_background_screenshot()

        ev = pygame.event.wait()
        self.last_event = ev

        return ev

    def compute_overlay(self):

        if renpy.store.suppress_overlay:
            return

        # Figure out what the overlay layer should look like.
        renpy.ui.layer("overlay")

        for i in renpy.config.overlay_functions:
            i()

        if renpy.game.context().scene_lists.shown_window:
            for i in renpy.config.window_overlay_functions:
                i()

        renpy.ui.close()

    def compute_scene(self, scene_lists):
        """
        This converts scene lists into a dictionary mapping layer
        name to a Fixed containing that layer.
        """

        rv = { }

        for layer in renpy.config.layers + renpy.config.top_layers:
            rv[layer] = scene_lists.make_layer(layer, self.layer_properties[layer])

        root = renpy.display.layout.MultiBox(layout='fixed')
        root.layers = { }

        for layer in renpy.config.layers:
            root.layers[layer] = rv[layer]
            root.add(rv[layer])
        rv[None] = root

        return rv

    def quit_event(self):
        """
        This is called to handle the user invoking a quit.
        """

        if self.quit_time > (time.time() - .75):
            raise renpy.game.QuitException()

        if self.in_quit_event:
            raise renpy.game.QuitException()

        if renpy.config.quit_action is not None:
            self.quit_time = time.time()

            # Make the screen more suitable for interactions.
            renpy.exports.movie_stop(only_fullscreen=True)
            renpy.store.mouse_visible = True

            try:
                self.in_quit_event = True
                renpy.display.behavior.run(renpy.config.quit_action)
            finally:
                self.in_quit_event = False

        else:
            raise renpy.game.QuitException()

    def get_mouse_info(self):
        # Figure out if the mouse visibility algorithm is hiding the mouse.
        if (renpy.config.mouse_hide_time is not None) and (self.mouse_event_time + renpy.config.mouse_hide_time < renpy.display.core.get_time()):
            visible = False
        else:
            visible = renpy.store.mouse_visible and (not renpy.game.less_mouse)

        visible = visible and self.show_mouse and not (renpy.display.video.fullscreen)

        # If not visible, hide the mouse.
        if not visible:
            return False, 0, 0, None

        # Deal with a hardware mouse, the easy way.
        if not renpy.config.mouse:
            return True, 0, 0, None

        # Deal with the mouse going offscreen.
        if not self.mouse_focused:
            return False, 0, 0, None

        mouse_kind = renpy.display.focus.get_mouse() or self.mouse

        # Figure out the mouse animation.
        if mouse_kind in renpy.config.mouse:
            anim = renpy.config.mouse[mouse_kind]
        else:
            anim = renpy.config.mouse[getattr(renpy.store, 'default_mouse', 'default')]

        img, x, y = anim[self.ticks % len(anim)]
        tex = renpy.display.im.load_image(img)

        return False, x, y, tex

    def set_mouse_pos(self, x, y, duration):
        """
        Sets the mouse position. Duration can be a number of seconds or
        None.
        """

        self.mouse_move = MouseMove(x, y, duration)
        self.force_redraw = True

    def drawn_since(self, seconds_ago):
        """
        Returns true if the screen has been drawn in the last `seconds_ago`,
        and false otherwise.
        """

        return (get_time() - self.frame_time) <= seconds_ago

    def check_suspend(self, ev):
        """
        Handles the SDL2 suspend process.
        """

        def save():
            if renpy.config.save_on_mobile_background:
                renpy.loadsave.save("_reload-1")

            renpy.persistent.update(True)

        if ev.type == pygame.APP_TERMINATING:
            save()
            sys.exit(0)

        if ev.type != pygame.APP_WILLENTERBACKGROUND:
            return False

        # At this point, we're about to enter the background.

        renpy.audio.audio.pause_all()

        if android:
            android.wakelock(False)

        pygame.time.set_timer(PERIODIC, 0)
        pygame.time.set_timer(REDRAW, 0)
        pygame.time.set_timer(TIMEEVENT, 0)

        save()

        if renpy.config.quit_on_mobile_background:
            sys.exit(0)

        renpy.exports.free_memory()

        print("Entered background.")

        while True:
            ev = pygame.event.wait()

            if ev.type == pygame.APP_DIDENTERFOREGROUND:
                break

            if ev.type == pygame.APP_TERMINATING:
                sys.exit(0)

        print("Entering foreground.")

        # Since we came back to life, we can get rid of the
        # auto-reload.
        renpy.loadsave.unlink_save("_reload-1")

        pygame.time.set_timer(PERIODIC, PERIODIC_INTERVAL)

        renpy.audio.audio.unpause_all()

        if android:
            android.wakelock(True)

        # Reset the display so we get the GL context back.
        self.display_reset = True
        self.restart_interaction = True

        return True

    def iconified(self):
        """
        Called when we become an icon.
        """

        if self.minimized:
            return

        self.minimized = True

        renpy.display.log.write("The window was minimized.")

    def restored(self):
        """
        Called when we are restored from being an icon.
        """

        # This is necessary on Windows/DirectX/Angle, as otherwise we get
        # a blank screen.

        if not self.minimized:
            return

        self.minimized = False

        renpy.display.log.write("The window was restored.")

        if renpy.windows:
            self.display_reset = True
            self.set_mode(self.last_resize)

    def enter_context(self):
        """
        Called when we enter a new context.
        """

        # Stop ongoing transitions.
        self.ongoing_transition.clear()
        self.transition_from.clear()
        self.transition_time.clear()

    def post_time_event(self):
        """
        Posts a time_event object to the queue.
        """

        try:
            pygame.event.post(self.time_event)
        except:
            pass

    def after_longpress(self):
        """
        Called after a longpress, to ignore the mouse button release.
        """

        self.ignore_touch = True
        renpy.display.focus.mouse_handler(None, -1, -1, default=False)

    def text_event_in_queue(self):
        """
        Returns true if the next event in the queue is a text editing event.
        """

        ev = self.event_peek()
        if ev is None:
            return False
        else:
            return ev.type in (pygame.TEXTINPUT, pygame.TEXTEDITING)

    def update_text_rect(self):
        """
        Updates the text input state and text rectangle.
        """

        if renpy.store._text_rect is not None:  # @UndefinedVariable
            self.text_rect = renpy.store._text_rect  # @UndefinedVariable

        if self.text_rect is not None:

            not_shown = pygame.key.has_screen_keyboard_support() and not pygame.key.is_screen_keyboard_shown()  # @UndefinedVariable

            if not self.old_text_rect or not_shown:
                pygame.key.start_text_input()  # @UndefinedVariable

            if self.old_text_rect != self.text_rect:
                x, y, w, h = self.text_rect
                x0, y0 = renpy.display.draw.untranslate_point(x, y)
                x1, y1 = renpy.display.draw.untranslate_point(x + w, y + h)
                rect = (x0, y0, x1 - x0, y1 - y0)

                pygame.key.set_text_input_rect(rect)  # @UndefinedVariable

        else:
            if self.old_text_rect:
                pygame.key.stop_text_input()  # @UndefinedVariable
                pygame.key.set_text_input_rect(None)  # @UndefinedVariable

        self.old_text_rect = self.text_rect

    def maximum_framerate(self, t):
        """
        Forces Ren'Py to draw the screen at the maximum framerate for `t` seconds.
        """

        if t is None:
            self.maximum_framerate_time = 0
        else:
            self.maximum_framerate_time = max(self.maximum_framerate_time, get_time() + t)

    def interact(self, clear=True, suppress_window=False, trans_pause=False, **kwargs):
        """
        This handles an interaction, restarting it if necessary. All of the
        keyword arguments are passed off to interact_core.
        """

        renpy.plog(1, "start of new interaction")

        if not self.started:
            self.start()

        self.trans_pause = trans_pause

        # Cancel magic error reporting.
        renpy.bootstrap.report_error = None

        context = renpy.game.context()

        if context.interacting:
            raise Exception("Cannot start an interaction in the middle of an interaction, without creating a new context.")

        context.interacting = True

        # Show a missing window.
        if not suppress_window:
            self.show_window()

        # These things can be done once per interaction.

        preloads = self.preloads
        self.preloads = [ ]

        try:
            for i in renpy.config.start_interact_callbacks:
                i()

            repeat = True

            self.start_interact = True

            while repeat:
                repeat, rv = self.interact_core(preloads=preloads, trans_pause=trans_pause, **kwargs)
                self.start_interact = False

            return rv

        finally:

            context.interacting = False

            # Clean out transient stuff at the end of an interaction.
            if clear:
                scene_lists = renpy.game.context().scene_lists
                scene_lists.replace_transient()

            self.ongoing_transition = { }
            self.transition_time = { }
            self.transition_from = { }

            self.restart_interaction = True

            renpy.game.context().mark_seen()
            renpy.game.context().scene_lists.shown_window = False

            if renpy.game.log is not None:
                renpy.game.log.did_interaction = True

    def consider_gc(self):
        """
        Considers if we should peform a garbage collection.
        """

        if not renpy.config.manage_gc:
            return

        count = gc.get_count()

        if count[0] >= renpy.config.idle_gc_count:
            renpy.plog(2, "before gc")

            if count[2] >= renpy.config.gc_thresholds[2]:
                gen = 2
            elif count[1] >= renpy.config.gc_thresholds[1]:
                gen = 1
            else:
                gen = 0

            gc.collect(gen)

            if gc.garbage:
                renpy.memory.print_garbage(gen)
                gc.garbage[:] = [ ]

            renpy.plog(2, "after gc")

    def idle_frame(self, can_block, expensive):
        """
        Tasks that are run during "idle" frames.
        """

        if expensive:
            renpy.plog(1, "start idle_frame (expensive)")
        else:
            renpy.plog(1, "start idle_frame (inexpensive)")

        # We want this to include the GC time, so we don't predict on
        # frames where we GC.
        start = get_time()

        step = 1

        while True:

            if self.event_peek():
                break

            if not (can_block and expensive):
                if get_time() > (start + .0005):
                    break

            # Step 1: Run gc.
            if step == 1:
                self.consider_gc()
                step += 1

            # Step 2: Push textures to GPU.
            elif step == 2:
                renpy.display.draw.ready_one_texture()
                step += 1

            # Step 3: Predict more images.
            elif step == 3:

                if not self.prediction_coroutine:
                    step += 1
                    continue

                result = self.prediction_coroutine.send(expensive)

                if result is None:
                    self.prediction_coroutine = None
                    step += 1

                elif result is False:
                    if not expensive:
                        step += 1

            # Step 4: Autosave.
            elif step == 4:

                if not self.did_autosave:
                    renpy.loadsave.autosave()
                    renpy.persistent.check_update()
                    self.did_autosave = True

                step += 1

            else:
                break

        if expensive:
            renpy.plog(1, "end idle_frame (expensive)")
        else:
            renpy.plog(1, "end idle_frame (inexpensive)")

    def interact_core(self,
                      show_mouse=True,
                      trans_pause=False,
                      suppress_overlay=False,
                      suppress_underlay=False,
                      mouse='default',
                      preloads=[],
                      roll_forward=None,
                      ):
        """
        This handles one cycle of displaying an image to the user,
        and then responding to user input.

        @param show_mouse: Should the mouse be shown during this
        interaction? Only advisory, and usually doesn't work.

        @param trans_pause: If given, we must have a transition. Should we
        add a pause behavior during the transition?

        @param suppress_overlay: This suppresses the display of the overlay.
        @param suppress_underlay: This suppresses the display of the underlay.
        """

        renpy.plog(1, "start interact_core")

        suppress_overlay = suppress_overlay or renpy.store.suppress_overlay

        # Store the various parameters.
        self.suppress_overlay = suppress_overlay
        self.suppress_underlay = suppress_underlay
        self.trans_pause = trans_pause

        # Show default screens.
        renpy.display.screen.show_overlay_screens(suppress_overlay)

        # Prepare screens, if need be.
        renpy.display.screen.prepare_screens()

        self.roll_forward = roll_forward
        self.show_mouse = show_mouse

        suppress_transition = renpy.config.skipping or renpy.game.less_updates

        # The global one.
        self.suppress_transition = False

        # Figure out transitions.
        for k in self.transition:
            if k not in self.old_scene:
                continue

            self.ongoing_transition[k] = self.transition[k]
            self.transition_from[k] = self.old_scene[k]._in_current_store()
            self.transition_time[k] = None

        self.transition.clear()

        if suppress_transition:
            self.ongoing_transition.clear()
            self.transition_from.clear()
            self.transition_time.clear()

        # Safety condition, prevents deadlocks.
        if trans_pause:
            if not self.ongoing_transition:
                return False, None
            if None not in self.ongoing_transition:
                return False, None
            if suppress_transition:
                return False, None
            if not self.old_scene:
                return False, None

        # Check to see if the language has changed.
        renpy.translation.check_language()

        # We just restarted.
        self.restart_interaction = False

        # Setup the mouse.
        self.mouse = mouse

        # The start and end times of this interaction.
        start_time = get_time()
        end_time = start_time

        # frames = 0

        for i in renpy.config.interact_callbacks:
            i()

        # Set the window caption.
        self.set_window_caption()

        # Tick time forward.
        renpy.display.im.cache.tick()
        renpy.text.text.text_tick()
        renpy.display.predict.reset()

        # Clear the size groups.
        renpy.display.layout.size_groups.clear()

        # Clear the set of updated screens.
        renpy.display.screen.updated_screens.clear()

        # Clear some events.
        pygame.event.clear((pygame.MOUSEMOTION,
                            PERIODIC,
                            TIMEEVENT,
                            REDRAW))

        # Add a single TIMEEVENT to the queue.
        self.post_time_event()

        # Figure out the scene list we want to show.
        scene_lists = renpy.game.context().scene_lists

        # Remove the now-hidden things.
        scene_lists.remove_hidden()

        # Compute the overlay.
        if not suppress_overlay:
            self.compute_overlay()

        # The root widget of everything that is displayed on the screen.
        root_widget = renpy.display.layout.MultiBox(layout='fixed')
        root_widget.layers = { }

        # A list of widgets that are roots of trees of widgets that are
        # considered for focusing.
        focus_roots = [ ]

        # Add the underlay to the root widget.
        if not suppress_underlay:
            for i in renpy.config.underlay:
                root_widget.add(i)
                focus_roots.append(i)

            if roll_forward is not None:
                rfw = renpy.display.behavior.RollForward(roll_forward)
                root_widget.add(rfw)
                focus_roots.append(rfw)

        # Figure out the scene. (All of the layers, and the root.)
        scene = self.compute_scene(scene_lists)
        renpy.display.tts.set_root(scene[None])

        renpy.plog(1, "computed scene")

        # If necessary, load all images here.
        for w in scene.itervalues():
            try:
                renpy.display.predict.displayable(w)
            except:
                pass

        renpy.plog(1, "final predict")

        # The root widget of all of the layers.
        layers_root = renpy.display.layout.MultiBox(layout='fixed')
        layers_root.layers = { }

        def add_layer(where, layer):

            scene_layer = scene[layer]
            focus_roots.append(scene_layer)

            if (self.ongoing_transition.get(layer, None) and
                    not suppress_transition):

                trans = self.ongoing_transition[layer](
                    old_widget=self.transition_from[layer],
                    new_widget=scene_layer)

                if not isinstance(trans, Displayable):
                    raise Exception("Expected transition to be a displayable, not a %r" % trans)

                transition_time = self.transition_time.get(layer, None)

                where.add(trans, transition_time, transition_time)
                where.layers[layer] = trans

            else:
                where.layers[layer] = scene_layer
                where.add(scene_layer)

        # Add layers (perhaps with transitions) to the layers root.
        for layer in renpy.config.layers:
            add_layer(layers_root, layer)

        # Add layers_root to root_widget, perhaps through a transition.
        if (self.ongoing_transition.get(None, None) and
                not suppress_transition):

            old_root = renpy.display.layout.MultiBox(layout='fixed')
            old_root.layers = { }

            for layer in renpy.config.layers:
                d = self.transition_from[None].layers[layer]
                old_root.layers[layer] = d
                old_root.add(d)

            trans = self.ongoing_transition[None](
                old_widget=old_root,
                new_widget=layers_root)

            if not isinstance(trans, Displayable):
                raise Exception("Expected transition to be a displayable, not a %r" % trans)

            trans._show()

            transition_time = self.transition_time.get(None, None)
            root_widget.add(trans, transition_time, transition_time)

            if trans_pause:

                if renpy.store._dismiss_pause:
                    sb = renpy.display.behavior.SayBehavior()
                else:
                    sb = renpy.display.behavior.SayBehavior(dismiss='dismiss_hard_pause')

                root_widget.add(sb)
                focus_roots.append(sb)

                pb = renpy.display.behavior.PauseBehavior(trans.delay)
                root_widget.add(pb, transition_time, transition_time)
                focus_roots.append(pb)

        else:
            root_widget.add(layers_root)

        # Add top_layers to the root_widget.
        for layer in renpy.config.top_layers:
            add_layer(root_widget, layer)

        for i in renpy.display.emulator.overlay:
            root_widget.add(i)

        del add_layer

        self.prediction_coroutine = renpy.display.predict.prediction_coroutine(root_widget)
        self.prediction_coroutine.send(None)

        # Clean out the registered adjustments.
        renpy.display.behavior.adj_registered.clear()

        # Clean up some movie-related things.
        renpy.display.video.early_interact()

        # Call per-interaction code for all widgets.
        renpy.display.behavior.input_pre_per_interact()
        root_widget.visit_all(lambda i : i.per_interact())
        renpy.display.behavior.input_post_per_interact()

        # Now, update various things regarding scenes and transitions,
        # so we are ready for a new interaction or a restart.
        self.old_scene = scene

        # Okay, from here on we now have a single root widget (root_widget),
        # which we will try to show to the user.

        # Figure out what should be focused.
        renpy.display.focus.before_interact(focus_roots)

        # Something updated the screens. Deal with it now, so the player doesn't
        # see it.
        if self.restart_interaction:
            return True, None

        # Redraw the screen.
        renpy.display.render.process_redraws()
        needs_redraw = True

        # First pass through the while loop?
        first_pass = True

        # We don't yet know when the interaction began.
        self.interact_time = None

        # We only want to do autosave once.
        self.did_autosave = False

        old_timeout_time = None
        old_redraw_time = None

        rv = None

        # Start sound.
        renpy.audio.audio.interact()

        # How long until we redraw.
        _redraw_in = 3600

        # Have we drawn a frame yet?
        video_frame_drawn = False

        # We're no longer after rollback.
        renpy.game.after_rollback = False

        # How many frames have we shown so far?
        frame = 0

        can_block = False

        # This try block is used to force cleanup even on termination
        # caused by an exception propagating through this function.
        try:

            while rv is None:

                renpy.plog(1, "start of interact while loop")

                renpy.execution.not_infinite_loop(10)

                # Check for a change in fullscreen preference.
                if ((self.fullscreen != renpy.game.preferences.fullscreen) or
                        self.display_reset or (renpy.display.draw is None)):

                    self.set_mode()
                    needs_redraw = True

                # Check for autoreload.
                if renpy.loader.needs_autoreload:
                    renpy.loader.needs_autoreload = False
                    renpy.exports.reload_script()

                for i in renpy.config.needs_redraw_callbacks:
                    if i():
                        needs_redraw = True

                # Redraw the screen.
                if (self.force_redraw or
                    ((first_pass or not pygame.event.peek(ALL_EVENTS)) and
                     renpy.display.draw.should_redraw(needs_redraw, first_pass, can_block))):

                    self.force_redraw = False

                    # If we have a movie, start showing it.
                    fullscreen_video = renpy.display.video.interact()

                    # Clean out the redraws, if we have to.
                    # renpy.display.render.kill_redraws()

                    self.text_rect = None

                    # Draw the screen.
                    self.frame_time = get_time()

                    renpy.audio.audio.advance_time()  # Sets the time of all video frames.

                    self.draw_screen(root_widget, fullscreen_video, (not fullscreen_video) or video_frame_drawn)

                    if first_pass:
                        if not self.interact_time:
                            self.interact_time = max(self.frame_time, get_time() - self.frame_duration)

                        scene_lists.set_times(self.interact_time)

                        for k, v in self.transition_time.iteritems():
                            if v is None:
                                self.transition_time[k] = self.interact_time

                        renpy.display.render.adjust_render_cache_times(self.frame_time, self.interact_time)

                    frame += 1
                    renpy.config.frames += 1

                    # If profiling is enabled, report the profile time.
                    if renpy.config.profile or self.profile_once:

                        renpy.plog(0, "end frame")
                        renpy.performance.analyze()
                        renpy.performance.clear()
                        renpy.plog(0, "start frame")

                        self.profile_once = False

                    if first_pass and self.last_event and self.last_event.type in [ pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION ]:

                        x, y = renpy.display.draw.get_mouse_pos()
                        ev, x, y = renpy.display.emulator.emulator(self.last_event, x, y)

                        if self.ignore_touch:
                            x = -1
                            y = -1

                        if renpy.android and self.last_event.type == pygame.MOUSEBUTTONUP:
                            x = -1
                            y = -1

                        renpy.display.focus.mouse_handler(None, x, y, default=False)

                    needs_redraw = False
                    first_pass = False

                    pygame.time.set_timer(REDRAW, 0)
                    pygame.event.clear([REDRAW])
                    old_redraw_time = None

                    self.update_text_rect()

                    renpy.test.testexecution.execute()

                # Move the mouse, if necessary.
                if self.mouse_move is not None:
                    if not self.mouse_move.perform():
                        self.mouse_move = None

                # Draw the mouse, if it needs drawing.
                renpy.display.draw.update_mouse()

                # See if we want to restart the interaction entirely.
                if self.restart_interaction:
                    return True, None

                # Determine if we need a redraw. (We want to run these
                # functions, so we put them first to prevent short-circuiting.)

                if renpy.display.video.frequent():
                    needs_redraw = True
                    video_frame_drawn = True

                if renpy.display.render.process_redraws():
                    needs_redraw = True

                # How many seconds until we timeout.
                _timeout_in = 3600

                # Handle the redraw timer.
                redraw_time = renpy.display.render.redraw_time()

                # We only need to set the REDRAW timer if we can block.
                can_block = renpy.display.draw.can_block()

                if self.maximum_framerate_time > get_time():
                    can_block = False

                if (redraw_time is not None) and (not needs_redraw) and can_block:
                    if redraw_time != old_redraw_time:
                        time_left = redraw_time - get_time()
                        time_left = min(time_left, 3600)
                        _redraw_in = time_left

                        if time_left <= 0:
                            try:
                                pygame.event.post(self.redraw_event)
                            except:
                                pass
                            pygame.time.set_timer(REDRAW, 0)
                        else:
                            pygame.time.set_timer(REDRAW, max(int(time_left * 1000), 1))

                        old_redraw_time = redraw_time
                else:
                    _redraw_in = 3600
                    pygame.time.set_timer(REDRAW, 0)

                # Handle the timeout timer.
                if not self.timeout_time:
                    pygame.time.set_timer(TIMEEVENT, 0)
                else:
                    time_left = self.timeout_time - get_time()
                    time_left = min(time_left, 3600)
                    _timeout_in = time_left

                    if time_left <= 0:
                        self.timeout_time = None
                        pygame.time.set_timer(TIMEEVENT, 0)
                        self.post_time_event()
                    elif self.timeout_time != old_timeout_time:
                        # Always set to at least 1ms.
                        pygame.time.set_timer(TIMEEVENT, int(time_left * 1000 + 1))
                        old_timeout_time = self.timeout_time

                if can_block or (frame >= renpy.config.idle_frame):
                    expensive = not ( needs_redraw or (_redraw_in < .2) or (_timeout_in < .2) or renpy.display.video.playing() )
                    self.idle_frame(can_block, expensive)

                if needs_redraw or (not can_block) or self.mouse_move or renpy.display.video.playing():
                    renpy.plog(1, "pre peek")
                    ev = self.event_poll()
                    renpy.plog(1, "post peek {!r}", ev)
                else:
                    renpy.plog(1, "pre wait")
                    ev = self.event_wait()
                    renpy.plog(1, "post wait {!r}", ev)

                if ev.type == pygame.NOEVENT:

                    if can_block and (not needs_redraw) and (not self.prediction_coroutine) and (not self.mouse_move):
                        pygame.time.wait(1)

                    continue

                # Recognize and ignore AltGr on Windows.
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_LCTRL:

                        ev2 = self.event_peek()

                        if (ev2 is not None) and (ev2.type == pygame.KEYDOWN):
                            if ev2.key == pygame.K_RALT:
                                continue

                # Check to see if the OS is asking us to suspend (on Android
                # and iOS.)
                if self.check_suspend(ev):
                    continue

                # Try to merge an TIMEEVENT with other timeevents.
                if ev.type == TIMEEVENT:
                    old_timeout_time = None
                    pygame.event.clear([TIMEEVENT])

                # On Android, where we have multiple mouse buttons, we can
                # merge a mouse down and mouse up event with its successor. This
                # prevents us from getting overwhelmed with too many events on
                # a multitouch screen.
                if android and (ev.type == pygame.MOUSEBUTTONDOWN or ev.type == pygame.MOUSEBUTTONUP):
                    pygame.event.clear(ev.type)

                # Handle redraw timeouts.
                if ev.type == REDRAW:
                    pygame.event.clear([REDRAW])
                    old_redraw_time = None
                    continue

                # Handle periodic events. This includes updating the mouse timers (and through the loop,
                # the mouse itself), and the audio system periodic calls.
                if ev.type == PERIODIC:
                    events = 1 + len(pygame.event.get([PERIODIC]))
                    self.ticks += events

                    for i in renpy.config.periodic_callbacks:
                        i()

                    renpy.audio.audio.periodic()
                    renpy.display.tts.periodic()
                    continue

                # Handle quit specially for now.
                if ev.type == pygame.QUIT:
                    self.quit_event()
                    continue

                # Ignore KEY-events while text is being edited (usually with an IME).
                if ev.type == pygame.TEXTEDITING:
                    if ev.text:
                        self.text_editing = ev
                    else:
                        self.text_editing = None
                elif ev.type == pygame.TEXTINPUT:
                    self.text_editing = None
                elif self.text_editing and ev.type in [ pygame.KEYDOWN, pygame.KEYUP ]:
                    continue

                if ev.type == pygame.VIDEOEXPOSE:
                    # Needed to force the display to redraw after expose in
                    # the software renderer.
                    renpy.game.interface.full_redraw = True
                    renpy.game.interface.force_redraw = True

                    if isinstance(renpy.display.draw, renpy.display.swdraw.SWDraw):
                        renpy.display.draw.full_redraw = True

                    continue

                # Handle videoresize.
                if ev.type == pygame.VIDEORESIZE:
                    evs = pygame.event.get([pygame.VIDEORESIZE])

                    if len(evs):
                        ev = evs[-1]

                    # We seem to get a spurious event like this when leaving
                    # fullscreen mode on windows.
                    if ev.w == 1 and ev.h == 1:
                        continue

                    size = (ev.w // self.dpi_scale, ev.h // self.dpi_scale)

                    if pygame.display.get_surface().get_size() != ev.size:
                        self.set_mode(size)

                    if not self.fullscreen:
                        self.last_resize = size

                    continue

                # If we're ignoring touch events, and get a mouse up, stop
                # ignoring those events.
                if self.ignore_touch and \
                        ev.type == pygame.MOUSEBUTTONUP and \
                        ev.button == 1:

                    self.ignore_touch = False
                    continue

                # Merge mousemotion events.
                if ev.type == pygame.MOUSEMOTION:
                    evs = pygame.event.get([pygame.MOUSEMOTION])
                    if len(evs):
                        ev = evs[-1]

                    if renpy.windows:
                        self.mouse_focused = True

                # Handle mouse event time, and ignoring touch.
                if ev.type == pygame.MOUSEMOTION or \
                        ev.type == pygame.MOUSEBUTTONDOWN or \
                        ev.type == pygame.MOUSEBUTTONUP:

                    self.mouse_event_time = renpy.display.core.get_time()

                    if self.ignore_touch:
                        renpy.display.focus.mouse_handler(None, -1, -1, default=False)

                # Handle focus notifications.
                if ev.type == pygame.ACTIVEEVENT:

                    if ev.state & 1:
                        if not ev.gain:
                            renpy.display.focus.clear_focus()

                        self.mouse_focused = ev.gain

                    if ev.state & 2:
                        self.keyboard_focused = ev.gain

                    if ev.state & 4:
                        if ev.gain:
                            self.restored()
                        else:
                            self.iconified()

                    pygame.key.set_mods(0)

                # This returns the event location. It also updates the
                # mouse state as necessary.
                x, y = renpy.display.draw.mouse_event(ev)
                x, y = renpy.test.testmouse.get_mouse_pos(x, y)

                ev, x, y = renpy.display.emulator.emulator(ev, x, y)
                if ev is None:
                    continue

                if not self.mouse_focused or self.ignore_touch:
                    x = -1
                    y = -1

                # This can set the event to None, to ignore it.
                ev = renpy.display.controller.event(ev)
                if not ev:
                    continue

                # Handle skipping.
                renpy.display.behavior.skipping(ev)

                self.event_time = end_time = get_time()

                try:

                    if self.touch:
                        renpy.display.gesture.recognizer.event(ev, x, y)  # @UndefinedVariable

                    # Handle the event normally.
                    rv = renpy.display.focus.mouse_handler(ev, x, y)

                    if rv is None:
                        rv = root_widget.event(ev, x, y, 0)

                    if rv is None:
                        rv = renpy.display.focus.key_handler(ev)

                    if rv is not None:
                        break

                    # Handle displayable inspector.
                    if renpy.config.inspector:
                        if renpy.display.behavior.map_event(ev, "inspector"):
                            l = self.surftree.main_displayables_at_point(x, y, renpy.config.transient_layers + renpy.config.context_clear_layers + renpy.config.overlay_layers)
                            renpy.game.invoke_in_new_context(renpy.config.inspector, l)
                        elif renpy.display.behavior.map_event(ev, "full_inspector"):
                            l = self.surftree.main_displayables_at_point(x, y, renpy.config.layers)
                            renpy.game.invoke_in_new_context(renpy.config.inspector, l)

                except IgnoreEvent:
                    # An ignored event can change the timeout. So we want to
                    # process an TIMEEVENT to ensure that the timeout is
                    # set correctly

                    if ev.type != TIMEEVENT:
                        self.post_time_event()

                # Check again after handling the event.
                needs_redraw |= renpy.display.render.process_redraws()

                if self.restart_interaction:
                    return True, None

            # If we were trans-paused and rv is true, suppress
            # transitions up to the next interaction.
            if trans_pause and rv:
                self.suppress_transition = True

            # But wait, there's more! The finally block runs some cleanup
            # after this.
            return False, rv

        except EndInteraction as e:
            return False, e.value

        finally:

            renpy.game.context().say_attributes = None

            # Clean out the overlay layers.
            for i in renpy.config.overlay_layers:
                scene_lists.clear(i)

            # Stop ongoing preloading.
            renpy.display.im.cache.end_tick()

            # We no longer disable periodic between interactions.
            # pygame.time.set_timer(PERIODIC, 0)

            pygame.time.set_timer(TIMEEVENT, 0)
            pygame.time.set_timer(REDRAW, 0)

            self.consider_gc()

            renpy.game.context().runtime += end_time - start_time

            # Restart the old interaction, which also causes a
            # redraw if needed.
            self.restart_interaction = True

            renpy.plog(1, "end interact_core")

            # print "It took", frames, "frames."

    def timeout(self, offset):
        if offset < 0:
            return

        if self.timeout_time:
            self.timeout_time = min(self.event_time + offset, self.timeout_time)
        else:
            self.timeout_time = self.event_time + offset

    def finish_pending(self):
        """
        Called before a quit or restart to finish any pending work that might
        block other threads.
        """

        self.check_background_screenshot()
