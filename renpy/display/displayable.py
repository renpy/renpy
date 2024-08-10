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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import copy

import renpy

def place(width, height, sw, sh, placement):
    """
    Performs the Ren'Py placement algorithm.

    `width`, `height`
        The width and height of the area the image will be
        placed in.

    `sw`, `sh`
        The size of the image to be placed.

    `placement`
        The tuple returned by Displayable.get_placement().
    """

    xpos, ypos, xanchor, yanchor, xoffset, yoffset, _subpixel = placement

    compute_raw = renpy.display.core.absolute.compute_raw

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

    xpos = compute_raw(xpos, width)

    xanchor = compute_raw(xanchor, sw)

    x = xpos + xoffset - xanchor

    ypos = compute_raw(ypos, height)

    yanchor = compute_raw(yanchor, sh)

    y = ypos + yoffset - yanchor

    return x, y


class DisplayableArguments(renpy.object.Object):
    """
    Represents a set of arguments that can be passed to a duplicated
    displayable.
    """

    # The name of the displayable without any arguments.
    name = () # type: tuple

    # Arguments supplied.
    args = () # type: tuple

    # The style prefix in play. This is used by DynamicImage to figure
    # out the prefix list to apply.
    prefix = None # Optional[str]

    # True if lint is in use.
    lint = False

    def copy(self, **kwargs):
        """
        Returns a copy of this object with the various fields set to the
        values they were given in kwargs.
        """

        rv = DisplayableArguments()
        rv.__dict__.update(self.__dict__)
        rv.__dict__.update(kwargs)

        return rv

    def extraneous(self):
        if renpy.config.developer and renpy.config.report_extraneous_attributes:
            raise Exception("Image '{}' does not accept attributes '{}'.".format(
                " ".join(self.name),
                " ".join(self.args),
                ))


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

    # Should hbox and vbox skip this displayable?
    _box_skip = False

    # If not None, this should be a (width, height) tuple that overrides the
    # amount of space offered to the displayable.
    _offer_size = None

    # If true, this displayable will be treated as draggable in its own right.
    # This is used by viewport to decide if a drag is meant for the viewport
    # or for its child.
    _draggable = False

    # Used by a transition (or transition-like object) to determine how long to
    # delay for.
    delay = None # type: float|None

    # An id that can be used to identify this displayable.
    id = None # type: str|None

    def __ne__(self, o):
        return not (self == o)

    def __init__(self, focus=None, default=False, style='default', _args=None, tooltip=None, default_focus=False, **properties):

        global default_style

        if (style == "default") and (not properties):
            self.style = default_style
        else:
            self.style = renpy.style.Style(style, properties) # @UndefinedVariable

        self.focus_name = focus
        self.default = default or default_focus
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

        if args and args.args:
            args.extraneous()

        return self

    def _get_tooltip(self):
        """
        Returns the tooltip of this displayable.
        """

        return self._tooltip

    def _in_current_store(self):
        """
        Returns a version of this displayable that will not change as it is
        rendered.
        """

        return self

    def _unique(self):
        """
        This is called when a displayable is "unique", meaning there will
        only be one reference to it, ever, from the tree of displayables.
        """

        self._duplicatable = False

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

    def _repr_info(self):
        return None

    def __repr__(self):
        rep = object.__repr__(self)
        reprinfo = self._repr_info()
        if reprinfo is None:
            return rep
        if reprinfo and not ((reprinfo[0] == '(') and (reprinfo[-1] == ')')):
            reprinfo = "".join(("(", reprinfo, ")"))
        parto = rep.rpartition(" at ")
        return " ".join((parto[0],
                         reprinfo,
                         "at",
                         parto[2]))

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

    def visit_all(self, callback, seen=None):
        """
        Calls the callback on this displayable, and then on all children
        of this displayable.
        """

        if seen is None:
            seen = set()

        for d in self.visit():

            if d is None:
                continue

            id_d = id(d)
            if id_d in seen:
                continue

            seen.add(id_d)
            d.visit_all(callback, seen)

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
        quite yet.

        Kind may be "hide", "replace", or "cancel", with the latter
        being called when the hide is being hidden itself because
        another displayable is shown.
        """

        return None

    def _show(self):
        """
        No longer used.
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

    def _tts_common(self, default_alt=None, reverse=False):

        rv = [ ]

        if reverse:
            order = -1
        else:
            order = 1

        speech = ""

        for i in self.visit()[::order]:
            if i is not None:
                speech = i._tts()

                if isinstance(speech, renpy.display.tts.TTSDone):
                    if speech.strip():
                        rv = [ speech ]
                    else:
                        rv = [ ]
                    break

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

        rv = type(speech)(rv)

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
