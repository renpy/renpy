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

import renpy.display
import time
import collections

import datetime

# Profiling ####################################################################

profile_log = renpy.log.open("profile_screen", developer=True, append=False, flush=False)

# A map from screen name to ScreenProfile object.
profile = { }


class ScreenProfile(renpy.object.Object):
    """
    :doc: profile_screen
    :name: renpy.profile_screen

    """

    def __init__(self, name, predict=False, show=False, update=False, request=False, time=False, debug=False, const=False):
        """
        Requests screen profiling for the screen named `name`, which
        must be a string.

        Apart from `name`, all arguments must be supplied as keyword
        arguments. This function takes three groups of arguments.


        The first group of arguments determines when profiling occurs.

        `predict`
            If true, profiling occurs when the screen is being predicted.

        `show`
            If true, profiling occurs when the screen is first shown.

        `update`
            If true, profiling occurs when the screen is updated.

        `request`
            If true, profiling occurs when requested by pressing F8.

        The second group of arguments controls what profiling output is
        produced when profiling occurs.

        `time`
            If true, Ren'Py will log the amount of time it takes to evaluate
            the screen.

        `debug`
            If true, Ren'Py will log information as to how screens are
            evaluated, including:

            * Which displayables Ren'Py considers constant.
            * Which arguments, if any, needed to be evaluated.
            * Which displayables were reused.

            Producing and saving this debug information takes a noticeable
            amount of time, and so the `time` output should not be considered
            reliable if `debug` is set.

        The last group of arguments controls what output is produced once
        per Ren'Py run.

        `const`
            Displays the variables in the screen that are marked as const and
            not-const.

        All profiling output will be logged to profile_screen.txt in the game
        directory.
        """

        self.predict = predict
        self.show = show
        self.update = update
        self.request = request

        self.time = time
        self.debug = debug

        self.const = const

        if name is not None:
            if isinstance(name, basestring):
                name = tuple(name.split())
                profile[name] = self


def get_profile(name):
    """
    Returns the profile object for the screen with `name`, or a default
    profile object if none exists.

    `name`
        A string or tuple.
    """

    if isinstance(name, basestring):
        name = tuple(name.split())

    if name in profile:
        return profile[name]
    else:
        return ScreenProfile(None)

# Cache ########################################################################


# A map from screen name to a list of ScreenCache objects. We ensure the cache
# does not exceed config.screen_cache_size for each screen.
predict_cache = collections.defaultdict(list)


class ScreenCache(object):
    """
    Represents an entry in the screen cache. Upon creation, puts itself into
    the screen cache.
    """

    def __init__(self, screen, args, kwargs, cache):

        if screen.ast is None:
            return

        self.args = args
        self.kwargs = kwargs
        self.cache = cache

        pc = predict_cache[screen]

        pc.append(self)

        if len(pc) > renpy.config.screen_cache_size:
            pc.pop(0)


cache_put = ScreenCache


def cache_get(screen, args, kwargs):
    """
    Returns the cache to use when `screen` is accessed with `args` and
    `kwargs`.
    """

    if screen.ast is None:
        return { }

    pc = predict_cache[screen]

    if not pc:
        return { }

    for sc in pc:

        # Reuse w/ same arguments.
        if sc.args == args and sc.kwargs == kwargs:
            pc.remove(sc)
            break
    else:

        # Reuse the oldest.
        sc = pc.pop(0)

    return sc.cache

# Screens #####################################################################


class Screen(renpy.object.Object):
    """
    A screen is a collection of widgets that are displayed together.
    This class stores information about the screen.
    """

    sensitive = "True"

    def __init__(self,
                 name,
                 function,
                 modal="False",
                 zorder="0",
                 tag=None,
                 predict=None,
                 variant=None,
                 parameters=False,
                 location=None,
                 layer="screens",
                 sensitive="True"):

        # The name of this screen.
        if isinstance(name, basestring):
            name = tuple(name.split())

        self.name = name

        if (variant is None) or isinstance(variant, basestring):
            variant = [ variant ]

        for v in variant:
            screens[name[0], v] = self
            screens_by_name[name[0]][v] = self

        # A function that can be called to display the screen.
        self.function = function

        # If this is a SL2 screen, the SLScreen node at the root of this
        # screen.
        if isinstance(function, renpy.sl2.slast.SLScreen): # @UndefinedVariable
            self.ast = function
        else:
            self.ast = None

        # Expression: Are we modal? (A modal screen ignores screens under it.)
        self.modal = modal

        # Expression: Our zorder.
        self.zorder = zorder

        # The tag associated with the screen.
        self.tag = tag or name[0]

        # Can this screen be predicted?
        if predict is None:
            predict = renpy.config.predict_screens

        self.predict = predict

        # True if this screen takes parameters via _args and _kwargs.
        self.parameters = parameters

        # The location (filename, linenumber) of this screen.
        self.location = location

        # The layer the screen will be shown on.
        self.layer = layer

        # Is this screen sensitive? An expression.
        self.sensitive = sensitive

        global prepared
        global analyzed

        prepared = False
        analyzed = False


# Phases we can be in.
PREDICT = 0 # Predicting the screen before it is shown.
SHOW = 1 # Showing the screen for the first time.
UPDATE = 2 # Showing the screen for the second and later times.
HIDE = 3 # After the screen has been hid with "hide screen" (or the end of call screen).
OLD = 4 # A copy of the screen in the old side of a transition.

phase_name = [
    "PREDICT",
    "SHOW",
    "UPDATE",
    "HIDE",
    "OLD",
    ]


class ScreenDisplayable(renpy.display.layout.Container):
    """
    A screen is a collection of widgets that are displayed together. This
    class is responsible for managing the display of a screen.
    """

    nosave = [
        'screen',
        'child',
        'children',
        'transforms',
        'widgets',
        'old_widgets',
        'hidden_widgets',
        'old_transforms',
        'cache',
        'miss_cache',
        'profile',
        'phase',
        'use_cache' ]

    restarting = False
    hiding = False
    transient = False

    def after_setstate(self):
        self.screen = get_screen_variant(self.screen_name[0])
        self.child = None
        self.children = [ ]
        self.transforms = { }
        self.widgets = { }
        self.old_widgets = None
        self.old_transforms = None
        self.hidden_widgets = { }
        self.cache = { }
        self.phase = UPDATE
        self.use_cache = { }
        self.miss_cache = { }

        self.profile = profile.get(self.screen_name, None)

    def __init__(self, screen, tag, layer, widget_properties={}, scope={}, transient=False, **properties):

        super(ScreenDisplayable, self).__init__(**properties)

        # Stash the properties, so we can re-create the screen.
        self.properties = properties

        # The screen, and it's name. (The name is used to look up the
        # screen on save.)
        self.screen = screen
        self.screen_name = screen.name

        self._location = self.screen.location

        # The profile object that determines when we profile.
        self.profile = profile.get(self.screen_name, None)

        # The tag and layer screen was displayed with.
        self.tag = tag
        self.layer = layer

        # The scope associated with this statement. This is passed in
        # as keyword arguments to the displayable.
        self.scope = renpy.python.RevertableDict(scope)

        # The child associated with this screen.
        self.child = None

        # Widget properties given to this screen the last time it was
        # shown.
        self.widget_properties = widget_properties

        # A map from name to the widget with that name.
        self.widgets = { }

        # The persistent cache.
        self.cache = { }

        if tag and layer:
            old_screen = get_screen(tag, layer)
        else:
            old_screen = None

        # A map from name to the transform with that name. (This is
        # taken from the old version of the screen, if it exists.
        if old_screen is not None:
            self.transforms = old_screen.transforms
        else:
            self.transforms = { }

        # A map from a (screen name, id) pair to cache. This is for use
        # statements with the id parameter.
        if old_screen is not None:
            self.use_cache = old_screen.use_cache
        else:
            self.use_cache = { }

        # A version of the cache that's used when we have a screen that is
        # being displayed with the same tag with a cached copy of the screen
        # we want to display.
        self.miss_cache = { }

        # What widgets and transforms were the last time this screen was
        # updated. Used to communicate with the ui module, and only
        # valid during an update - not used at other times.
        self.old_widgets = None
        self.old_transforms = None

        # Should we transfer data from the old_screen? This becomes
        # true once this screen finishes updating for the first time,
        # and also while we're using something.
        self.old_transfers = (old_screen and old_screen.screen_name == self.screen_name)

        # The current transform event, and the last transform event to
        # be processed.
        self.current_transform_event = None

        # A dict-set of widgets (by id) that have been hidden from us.
        self.hidden_widgets = { }

        # Are we restarting or hiding?
        self.restarting = False
        self.hiding = False

        # Is this a transient screen?
        self.transient = transient

        # Modal and zorder.
        self.modal = renpy.python.py_eval(self.screen.modal, locals=self.scope)
        self.zorder = renpy.python.py_eval(self.screen.zorder, locals=self.scope)

        # The lifecycle phase we are in - one of PREDICT, SHOW, UPDATE, or HIDE.
        self.phase = PREDICT

    def __unicode__(self):
        return "Screen {}".format(" ".join(self.screen_name))

    def visit(self):
        return [ self.child ]

    def visit_all(self, callback, seen=None):
        callback(self)

        try:
            push_current_screen(self)
            if self.child is not None:
                self.child.visit_all(callback, seen=None)
        finally:
            pop_current_screen()

    def per_interact(self):
        renpy.display.render.redraw(self, 0)
        self.update()

    def set_transform_event(self, event):
        super(ScreenDisplayable, self).set_transform_event(event)
        self.current_transform_event = event

    def find_focusable(self, callback, focus_name):

        hiding = (self.phase == OLD) or (self.phase == HIDE)

        try:
            push_current_screen(self)

            if self.child and not hiding:
                self.child.find_focusable(callback, focus_name)
        finally:
            pop_current_screen()

        if self.modal:
            raise renpy.display.layout.IgnoreLayers()

    def copy(self):
        rv = ScreenDisplayable(self.screen, self.tag, self.layer, self.widget_properties, self.scope, **self.properties)
        rv.transforms = self.transforms.copy()
        rv.widgets = self.widgets.copy()
        rv.old_transfers = True
        rv.child = self.child

        return rv

    def _handles_event(self, event):
        if self.child is None:

            if self.transient:
                return False

            self.update()

        return self.child._handles_event(event)

    def _hide(self, st, at, kind):

        if self.phase == HIDE:
            hid = self
        else:

            if (self.child is not None) and (not self.child._handles_event(kind)):
                return None

            updated_screens.discard(self)
            self.update()

            if self.screen is None:
                return None

            if self.child is None:
                return None

            if not self.child._handles_event(kind):
                return None

            if self.screen.ast is not None:
                self.screen.ast.copy_on_change(self.cache.get(0, {}))

            hid = self.copy()

            for i in self.child.children:
                i.set_transform_event(kind)

        hid.phase = HIDE

        rv = None

        old_child = hid.child

        if not isinstance(old_child, renpy.display.layout.MultiBox):
            return None

        renpy.ui.detached()
        hid.child = renpy.ui.default_fixed(focus="_screen_" + "_".join(self.screen_name))
        hid.children = [ hid.child ]
        renpy.ui.close()

        for d in old_child.children:
            c = d._hide(st, at, kind)

            if c is not None:
                renpy.display.render.redraw(c, 0)
                hid.child.add(c)

                rv = hid

        if hid is not None:
            renpy.display.render.redraw(hid, 0)

        return rv

    def _in_current_store(self):

        if self.screen is None:
            return self

        if self.child is None:
            return self

        if not renpy.config.transition_screens:
            return self

        if self.screen.ast is not None:
            self.screen.ast.copy_on_change(self.cache.get(0, {}))

        rv = self.copy()
        rv.phase = OLD
        rv.child = self.child._in_current_store()

        return rv

    def update(self):

        if self in updated_screens:
            return

        updated_screens.add(self)

        if self.screen is None:
            self.child = renpy.display.layout.Null()
            return { }

        # Do not update if restarting or hiding.
        if self.restarting or (self.phase == HIDE) or (self.phase == OLD):
            if not self.child:
                self.child = renpy.display.layout.Null()

            return self.widgets

        profile = False
        debug = False

        if self.profile:

            if self.phase == UPDATE and self.profile.update:
                profile = True
            elif self.phase == SHOW and self.profile.show:
                profile = True
            elif self.phase == PREDICT and self.profile.predict:
                profile = True

            if renpy.display.interface.profile_once and self.profile.request:
                profile = True

            if profile:
                profile_log.write("%s %s %s",
                                  phase_name[self.phase],
                                  " ".join(self.screen_name),
                                  datetime.datetime.now().strftime("%H:%M:%S.%f"))

                start = time.time()

                if self.profile.debug:
                    debug = True

        # Cycle widgets and transforms.
        self.old_widgets = self.widgets
        self.old_transforms = self.transforms
        self.widgets = { }
        self.transforms = { }

        push_current_screen(self)

        old_ui_screen = renpy.ui.screen
        renpy.ui.screen = self

        # The name of the root screen of this screen.
        NAME = 0

        old_cache = self.cache.get(NAME, None)

        # Evaluate the screen.
        try:

            renpy.ui.detached()
            self.child = renpy.ui.default_fixed(focus="_screen_" + "_".join(self.screen_name))
            self.children = [ self.child ]

            self.scope["_scope"] = self.scope
            self.scope["_name"] = NAME
            self.scope["_debug"] = debug

            self.screen.function(**self.scope)

            renpy.ui.close()

        finally:
            del self.scope["_scope"]

            renpy.ui.screen = old_ui_screen
            pop_current_screen()

        # Finish up.
        self.old_widgets = None
        self.old_transforms = None
        self.old_transfers = True

        if self.miss_cache:
            self.miss_cache.clear()

        # Deal with the case where the screen version changes.
        if (self.cache.get(NAME, None) is not old_cache) and (self.current_transform_event is None) and (self.phase == UPDATE):
            self.current_transform_event = "update"

        if self.current_transform_event:

            for i in self.child.children:
                i.set_transform_event(self.current_transform_event)

            self.current_transform_event = None

        if profile:
            end = time.time()

            if self.profile.time:
                profile_log.write("* %.2f ms", 1000 * (end - start))

            if self.profile.debug:
                profile_log.write("\n")

        return self.widgets

    def render(self, w, h, st, at):

        if not self.child:
            self.update()

        if self.phase == SHOW:
            self.phase = UPDATE

        try:
            push_current_screen(self)
            child = renpy.display.render.render(self.child, w, h, st, at)
        finally:
            pop_current_screen()

        rv = renpy.display.render.Render(w, h)
        rv.focus_screen = self

        hiding = (self.phase == OLD) or (self.phase == HIDE)

        if self.screen is None:
            sensitive = False
        else:
            sensitive = renpy.python.py_eval(self.screen.sensitive, locals=self.scope)

        rv.blit(child, (0, 0), focus=sensitive and not hiding, main=not hiding)
        rv.modal = self.modal and not hiding

        return rv

    def get_placement(self):
        if not self.child:
            self.update()

        return self.child.get_placement()

    def event(self, ev, x, y, st):

        if (self.phase == OLD) or (self.phase == HIDE):
            return

        if not self.screen:
            return None

        if not renpy.python.py_eval(self.screen.sensitive, locals=self.scope):
            ev = renpy.display.interface.time_event

        try:
            push_current_screen(self)

            rv = self.child.event(ev, x, y, st)
        finally:
            pop_current_screen()

        if rv is not None:
            return rv

        if self.modal:
            raise renpy.display.layout.IgnoreLayers()

    def get_phase_name(self):
        return phase_name[self.phase]


# The name of the screen that is currently being displayed, or
# None if no screen is being currently displayed.
_current_screen = None

# The stack of old current screens.
current_screen_stack = [ ]


def push_current_screen(screen):
    global _current_screen
    current_screen_stack.append(_current_screen)
    _current_screen = screen


def pop_current_screen():
    global _current_screen
    _current_screen = current_screen_stack.pop()


# A map from (screen_name, variant) tuples to screen.
screens = { }

# A map from screen name to map from variant to screen.
screens_by_name = collections.defaultdict(dict)

# The screens that were updated during the current interaction.
updated_screens = set()


def get_screen_variant(name, candidates=None):
    """
    Get a variant screen object for `name`.

    `candidates`
        A list of candidate variants.
    """

    if candidates is None:
        candidates = renpy.config.variants

    for i in candidates:
        rv = screens.get((name, i), None)
        if rv is not None:
            return rv

    return None


def get_all_screen_variants(name):
    """
    Gets all variants of the screen with `name`.

    Returns a list of (`variant`, `screen`) tuples, in no particular
    order.
    """

    if isinstance(name, basestring):
        name = tuple(name.split())

    name = name[0]

    if name not in screens_by_name:
        return [ ]

    return list(screens_by_name[name].items())


# Have all screens been analyzed?
analyzed = False

# Have the screens been prepared?
prepared = False

# Caches for sort_screens.
sorted_screens = [ ]
screens_at_sort = { }

# The list of screens that participate in a use cycle.
use_cycle = [ ]


def sort_screens():
    """
    Produces a list of SL2 screens in topologically sorted order.
    """

    global use_cycle
    global sorted_screens
    global screens_at_sort

    if screens_at_sort == screens:
        return sorted_screens

    # For each screen, the set of screens it uses.
    depends = collections.defaultdict(set)

    # For each screen, the set of screens that use it.
    reverse = collections.defaultdict(set)

    names = { i[0] for i in screens }

    for k, v in screens.items():

        name = k[0]

        # Ensure name exists.
        depends[name]

        if not v.ast:
            continue

        def callback(uses):

            if uses not in names:
                return

            depends[name].add(uses)
            reverse[uses].add(name)

        v.ast.used_screens(callback)

    rv = [ ]

    workset = { k for k, v in depends.items() if not len(v) }

    while workset:
        name = workset.pop()
        rv.append(name)

        for i in reverse[name]:
            d = depends[i]
            d.remove(name)

            if not d:
                workset.add(i)

        del reverse[name]

    # Store the use cycle for later reporting.
    use_cycle = list(reverse.keys())
    use_cycle.sort()

    sorted_screens = rv
    screens_at_sort = dict(screens)

    return rv


def sorted_variants():
    """
    Produces a list of screen variants in topological order.
    """

    rv = [ ]

    for name in sort_screens():
        rv.extend(screens_by_name[name].values())

    return rv


def analyze_screens():
    """
    Analyzes all screens.
    """

    global analyzed

    if analyzed:
        return

    for s in sorted_variants():
        if s.ast is None:
            continue

        s.ast.analyze_screen()

    analyzed = True


def prepare_screens():
    """
    Prepares all screens for use.
    """

    global prepared

    if prepared:
        return

    predict_cache.clear()

    old_predicting = renpy.display.predict.predicting
    renpy.display.predict.predicting = True

    try:

        if not analyzed:
            analyze_screens()

        for s in sorted_variants():
            if s.ast is None:
                continue

            s.ast.unprepare_screen()
            s.ast.prepare_screen()

        prepared = True

    finally:
        renpy.display.predict.predicting = old_predicting

    if renpy.config.developer and use_cycle:
        raise Exception("The following screens use each other in a loop: " + ", ".join(use_cycle) + ". This is not allowed.")


def define_screen(*args, **kwargs):
    """
    :doc: screens
    :args: (name, function, modal="False", zorder="0", tag=None, variant=None)

    Defines a screen with `name`, which should be a string.

    `function`
        The function that is called to display the screen. The
        function is called with the screen scope as keyword
        arguments. It should ignore additional keyword arguments.

        The function should call the ui functions to add things to the
        screen.

    `modal`
        A string that, when evaluated, determines of the created
        screen should be modal. A modal screen prevents screens
        underneath it from receiving input events.

    `zorder`
        A string that, when evaluated, should be an integer. The integer
        controls the order in which screens are displayed. A screen
        with a greater zorder number is displayed above screens with a
        lesser zorder number.

    `tag`
        The tag associated with this screen. When the screen is shown,
        it replaces any other screen with the same tag. The tag
        defaults to the name of the screen.

    `predict`
        If true, this screen can be loaded for image prediction. If false,
        it can't. Defaults to true.

    `variant`
        String. Gives the variant of the screen to use.

    """

    Screen(*args, **kwargs)


def get_screen_layer(name):
    """
    Returns the layer that the screen with `name` is part of.
    """

    if not isinstance(name, basestring):
        name = name[0]

    screen = get_screen_variant(name)

    if screen is None:
        return "screens"
    else:
        return screen.layer


def get_screen(name, layer=None):
    """
    :doc: screens

    Returns the ScreenDisplayable with the given `name` on layer. `name`
    is first interpreted as a tag name, and then a screen name. If the
    screen is not showing, returns None.

    This can also take a list of names, in which case the first screen
    that is showing is returned.

    This function can be used to check if a screen is showing::

        if renpy.get_screen("say"):
            text "The say screen is showing."
        else:
            text "The say screen is hidden."

    """

    if layer is None:
        layer = get_screen_layer(name)

    if isinstance(name, basestring):
        name = (name,)

    sl = renpy.exports.scene_lists()

    for tag in name:

        sd = sl.get_displayable_by_tag(layer, tag)
        if sd is not None:
            return sd

    for tag in name:

        sd = sl.get_displayable_by_name(layer, (tag,))
        if sd is not None:
            return sd

    return None


def has_screen(name):
    """
    Returns true if a screen with the given name exists.
    """

    if not isinstance(name, tuple):
        name = tuple(name.split())

    if not name:
        return False

    if get_screen_variant(name[0]):
        return True
    else:
        return False


def show_screen(_screen_name, *_args, **kwargs):
    """
    :doc: screens

    The programmatic equivalent of the show screen statement.

    Shows the named screen. This takes the following keyword arguments:

    `_screen_name`
        The name of the screen to show.
    `_layer`
        The layer to show the screen on.
    `_zorder`
        The zorder to show the screen on. If not specified, defaults to
        the zorder associated with the screen. It that's not specified,
        it is 0 by default.
    `_tag`
        The tag to show the screen with. If not specified, defaults to
        the tag associated with the screen. It that's not specified,
        defaults to the name of the screen.
    `_widget_properties`
        A map from the id of a widget to a property name -> property
        value map. When a widget with that id is shown by the screen,
        the specified properties are added to it.
    `_transient`
        If true, the screen will be automatically hidden at the end of
        the current interaction.

    Non-keyword arguments, and keyword arguments that do not begin with
    an underscore, are passed to the screen.
    """

    _layer = kwargs.pop("_layer", None)
    _tag = kwargs.pop("_tag", None)
    _widget_properties = kwargs.pop("_widget_properties", {})
    _transient = kwargs.pop("_transient", False)
    _zorder = kwargs.pop("_zorder", None)

    name = _screen_name

    if not isinstance(name, tuple):
        name = tuple(name.split())

    screen = get_screen_variant(name[0])

    if screen is None:
        raise Exception("Screen %s is not known.\n" % (name[0],))

    if _layer is None:
        _layer = get_screen_layer(name)

    if _tag is None:
        _tag = screen.tag

    scope = { }

    if screen.parameters:
        scope["_kwargs" ] = kwargs
        scope["_args"] = _args
    else:
        scope.update(kwargs)

    d = ScreenDisplayable(screen, _tag, _layer, _widget_properties, scope, transient=_transient)

    if _zorder is None:
        _zorder = d.zorder

    old_d = get_screen(_tag, _layer)

    if old_d and old_d.cache:
        d.cache = old_d.cache
        d.miss_cache = cache_get(screen, _args, kwargs)
        d.phase = UPDATE
    else:
        d.cache = cache_get(screen, _args, kwargs)
        d.phase = SHOW

    sls = renpy.display.core.scene_lists()

    sls.add(_layer, d, _tag, zorder=_zorder, transient=_transient, keep_st=True, name=name)


def predict_screen(_screen_name, *_args, **kwargs):
    """
    Predicts the displayables that make up the given screen.

    `_screen_name`
        The name of the  screen to show.
    `_widget_properties`
        A map from the id of a widget to a property name -> property
        value map. When a widget with that id is shown by the screen,
        the specified properties are added to it.

    Keyword arguments not beginning with underscore (_) are used to
    initialize the screen's scope.
    """

    _layer = kwargs.pop("_layer", None)
    _tag = kwargs.pop("_tag", None)
    _widget_properties = kwargs.pop("_widget_properties", {})
    _transient = kwargs.pop("_transient", False)

    name = _screen_name

    if renpy.config.debug_image_cache:
        renpy.display.ic_log.write("Predict screen %s", name)

    if not isinstance(name, tuple):
        name = tuple(name.split())

    screen = get_screen_variant(name[0])

    if screen is None:
        return

    if not screen.predict:
        return

    if _layer is None:
        _layer = get_screen_layer(name)

    scope = { }
    scope["_scope"] = scope

    if screen.parameters:
        scope["_kwargs" ] = kwargs
        scope["_args"] = _args
    else:
        scope.update(kwargs)

    try:

        d = ScreenDisplayable(screen, None, None, _widget_properties, scope)
        d.cache = cache_get(screen, _args, kwargs)
        d.update()
        cache_put(screen, _args, kwargs, d.cache)

        renpy.display.predict.displayable(d)

    except:
        if renpy.config.debug_image_cache:
            import traceback

            print("While predicting screen", _screen_name)
            traceback.print_exc()
            print()

    finally:
        del scope["_scope"]

    renpy.ui.reset()


def hide_screen(tag, layer=None):
    """
    :doc: screens

    The programmatic equivalent of the hide screen statement.

    Hides the screen with `tag` on `layer`.
    """

    if layer is None:
        layer = get_screen_layer((tag,))

    screen = get_screen(tag, layer)

    if screen is not None:
        renpy.exports.hide(screen.tag, layer=layer)


def use_screen(_screen_name, *_args, **kwargs):

    _name = kwargs.pop("_name", ())
    _scope = kwargs.pop("_scope", { })

    name = _screen_name

    if not isinstance(name, tuple):
        name = tuple(name.split())

    screen = get_screen_variant(name[0])

    if screen is None:
        raise Exception("Screen %r is not known." % (name,))

    old_transfers = _current_screen.old_transfers
    _current_screen.old_transfers = True

    if screen.parameters:
        scope = { }
        scope["_kwargs"] = kwargs
        scope["_args"] = _args
    else:
        scope = _scope.copy()
        scope.update(kwargs)

    scope["_scope"] = scope
    scope["_name"] = (_name, name)

    try:
        screen.function(**scope)
    finally:
        del scope["_scope"]

    _current_screen.old_transfers = old_transfers


def current_screen():
    return _current_screen


def get_widget(screen, id, layer=None): # @ReservedAssignment
    """
    :doc: screens

    From the `screen` on `layer`, returns the widget with
    `id`. Returns None if the screen doesn't exist, or there is no
    widget with that id on the screen.
    """

    if isinstance(screen, ScreenDisplayable):
        screen = screen.screen_name

    if screen is None:
        screen = current_screen()
    else:
        if layer is None:
            layer = get_screen_layer(screen)

        screen = get_screen(screen, layer)

    if not isinstance(screen, ScreenDisplayable):
        return None

    if screen.child is None:
        screen.update()

    rv = screen.widgets.get(id, None)
    return rv


def get_widget_properties(id, screen=None, layer=None): # @ReservedAssignment
    """
    :doc: screens

    Returns the properties for the widget with `id` in the `screen`
    on `layer`. If `screen` is None, returns the properties for the
    current screen. This can be used from Python or property code inside
    a screen.

    Note that this returns a dictionary containing the widget properties,
    and so to get an individual property, the dictionary must be accessed.
    """

    if screen is None:
        s = current_screen()
    else:
        if layer is None:
            layer = get_screen_layer(screen)

        s = get_screen(screen, layer)

    if s is None:
        return { }

    rv = s.widget_properties.get(id, None)

    if rv is None:
        rv = { }

    return rv


def before_restart():
    """
    This is called before Ren'Py restarts to put the screens into restart
    mode, which prevents crashes due to variables being used that are no
    longer defined.
    """

    for k, layer in renpy.display.interface.old_scene.items():
        if k is None:
            continue

        for i in layer.children:
            if isinstance(i, ScreenDisplayable):
                i.restarting = True


def show_overlay_screens(suppress_overlay):
    """
    Called from interact to show or hide the overlay screens.
    """

    show = not suppress_overlay

    if renpy.store._overlay_screens is None:
        show = show
    elif renpy.store._overlay_screens is True:
        show = True
    else:
        show = False

    if show:

        for i in renpy.config.overlay_screens:
            if get_screen(i) is None:
                show_screen(i)

    else:

        for i in renpy.config.overlay_screens:
            if get_screen(i) is not None:
                hide_screen(i)


def per_frame():
    """
    Called from interact once per frame to invalidate screens we want to
    update once per frame.
    """

    for i in renpy.config.per_frame_screens:
        s = get_screen(i)

        if s is None:
            continue

        updated_screens.discard(s)
        renpy.display.render.invalidate(s)
        s.update()
