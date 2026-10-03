# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode  # *


import os

import renpy.pygame as pygame

from renpy.pygame import CONTROLLERDEVICEADDED, CONTROLLERDEVICEREMOVED
from renpy.pygame import CONTROLLERAXISMOTION, CONTROLLERBUTTONDOWN, CONTROLLERBUTTONUP
from renpy.pygame.controller import Controller, get_string_for_axis, get_string_for_button


import renpy


def load_mappings():
    try:
        with renpy.loader.load("renpycontrollerdb.txt", tl=False) as f:
            pygame.controller.add_mappings(f)
    except Exception:
        pass

    try:
        with renpy.loader.load("gamecontrollerdb.txt", tl=False) as f:
            pygame.controller.add_mappings(f)
    except Exception:
        pass

    try:
        with open(os.path.join(renpy.config.renpy_base, "gamecontrollerdb.txt"), "rb") as f:
            pygame.controller.add_mappings(f)
    except Exception:
        pass


def init():
    """
    Initialize gamepad support.
    """

    if not renpy.game.preferences.pad_enabled:
        return

    try:
        pygame.controller.init()
        load_mappings()
    except Exception:
        renpy.display.log.exception()

    if not renpy.display.interface.safe_mode:
        try:
            for instance_id in pygame.joystick.get_joystick_ids():
                start(instance_id)
        except Exception:
            renpy.display.log.exception()


# A map from controller index to controller object.
controllers = {}

# A map from (controller, axis) to "pos", "neg", None position.
axis_positions = {}

# The axis threshold.
THRESHOLD = 8192 + 4096
ZERO_THRESHOLD = 8192

# Should we ignore events?
ignore = False


ps_alias = {
    "cross": "a",
    "circle": "b",
    "square": "x",
    "triangle": "y",
}


def post_event(control, state, repeat):
    """
    Creates an EVENTNAME event for the given state and name, and post it
    to the event queue.
    """

    if not renpy.display.interface.keyboard_focused:
        return None

    if ignore:
        return None

    name = "pad_{}_{}".format(control, state)

    if repeat:
        name = "repeat_" + name

    names = [name]

    alias_name = None
    if control in ps_alias:
        alias_name = "pad_{}_{}".format(ps_alias[control], state)
        if repeat:
            alias_name = "repeat_" + alias_name
        names.append(alias_name)

    if renpy.config.map_pad_event:
        names.extend(renpy.config.map_pad_event(name))
        if alias_name:
            names.extend(renpy.config.map_pad_event(alias_name))
    else:
        names.extend(renpy.config.pad_bindings.get(name, ()))
        if alias_name:
            names.extend(renpy.config.pad_bindings.get(alias_name, ()))

    ev = pygame.event.Event(renpy.display.core.EVENTNAME, {"eventnames": names, "controller": name, "up": False})

    pygame.event.post(ev)


def exists():
    """
    Returns true if a controller exists, and False otherwise.
    """

    if controllers:
        return True
    else:
        return False


def get_controller(index=None):
    """
    Returns the Controller object at `index`, or the first connected controller if `index` is None.
    Returns None if no controller is found.
    """

    if not controllers:
        return None

    if index is None:
        return next(iter(controllers.values()))

    c = controllers.get(index, None)
    if c is not None:
        return c

    for v in controllers.values():
        if v.instance_id == index:
            return v

    return None


def get_controller_type(index=None):
    """
    Returns the string type of the controller (e.g. 'nintendo_switch_pro', 'xbox360', 'ps5'),
    or None if no controller is connected.
    """

    c = get_controller(index)
    if c is not None:
        return c.get_type_name()

    return None


def get_controller_real_type(index=None):
    """
    Returns the real string type of the controller (e.g. 'nintendo_switch_pro', 'xbox360', 'ps5'),
    ignoring any driver remappings, or None if no controller is connected.
    """

    c = get_controller(index)
    if c is not None:
        return renpy.pygame.controller.get_string_for_type(c.get_real_type())

    return None


def get_controller_button_label(button, index=None):
    """
    Returns the button label string ("a", "b", "x", "y", "cross", "circle", etc.)
    for the given `button` on the controller, or None if unknown or no controller is connected.
    `button` can be an integer button index or string ("a", "b", "x", "y", etc.).
    """

    c = get_controller(index)
    if c is not None:
        return c.get_button_label_string(button)

    return None



def quit(index):
    """
    Quits the controller at index.
    """

    if index in controllers:
        controllers[index].quit()
        del controllers[index]

        renpy.exports.restart_interaction()


def start(index):
    """
    Starts the controller at index.
    """

    quit(index)
    c = Controller(index)

    if not c.is_controller():
        return

    renpy.exports.write_log("controller: %r %r %r" % (c.get_guid_string(), c.get_name(), c.is_controller()))

    if renpy.game.preferences.pad_enabled != "all":
        for prefix in renpy.config.controller_blocklist:
            if c.get_guid_string().startswith(prefix):
                renpy.exports.write_log("Controller found in blocklist, not using.")
                return

    try:
        c.init()
        controllers[index] = c
    except Exception:
        renpy.display.log.exception()

    renpy.exports.restart_interaction()


class PadEvent(object):
    """
    This stores the information about a PadEvent, to trigger repeats.
    """

    def __init__(self, control):
        # The control this corresponds to.
        self.control = control

        # The current state of the control.
        self.state = None

        # When should the repeat occur?
        self.repeat_time = 0

    def event(self, state):
        self.state = state
        self.repeat_time = renpy.display.core.get_time() + renpy.config.controller_first_repeat

        post_event(self.control, self.state, False)

        if renpy.display.interface is not None:
            renpy.display.interface.hide_mouse()

    def repeat(self):
        if self.state not in renpy.config.controller_repeat_states:
            return

        now = renpy.display.core.get_time()

        if now < self.repeat_time:
            return

        self.repeat_time = self.repeat_time + renpy.config.controller_repeat

        if self.repeat_time < now:
            self.repeat_time = now + renpy.config.controller_repeat

        post_event(self.control, self.state, True)


# A map from the pad event name to the pad event object.
pad_events = {}


def controller_event(control, state):
    pe = pad_events.get(control, None)
    if pe is None:
        pe = pad_events[control] = PadEvent(control)

    pe.event(state)


def periodic():
    for pe in pad_events.values():
        pe.repeat()


def event(ev):
    """
    Processes an event and returns the same event, a new event, or None if
    the event has been processed and should be ignored.
    """

    if renpy.config.pass_controller_events:
        rv = ev
    else:
        rv = None

    if ev.type == CONTROLLERDEVICEADDED:
        start(ev.which)
        return rv

    elif ev.type == CONTROLLERDEVICEREMOVED:
        for k, v in controllers.items():
            if v.instance_id == ev.which:
                quit(k)
                break

        return rv

    elif ev.type == CONTROLLERAXISMOTION:
        pygame.event.pump()
        events = [ev] + pygame.event.get(CONTROLLERAXISMOTION)

        for ev in events:
            old_pos = axis_positions.get((ev.which, ev.axis), None)

            if ev.value > THRESHOLD:
                pos = "pos"
            elif ev.value < -THRESHOLD:
                pos = "neg"
            elif abs(ev.value) < ZERO_THRESHOLD:
                pos = "zero"
            else:
                pos = old_pos

            if pos == old_pos:
                continue

            axis_positions[(ev.which, ev.axis)] = pos

            controller_event(get_string_for_axis(ev.axis), pos)

        return rv

    elif ev.type in (CONTROLLERBUTTONDOWN, CONTROLLERBUTTONUP):
        if ev.type == CONTROLLERBUTTONDOWN:
            pr = "press"
        else:
            pr = "release"

        button_name = None
        c = controllers.get(ev.which, None)
        if c is None:
            for v in controllers.values():
                if v.instance_id == ev.which:
                    c = v
                    break

        if c is not None:
            use_labels = getattr(renpy.game.preferences, "pad_use_button_labels", None)
            if use_labels is None:
                use_labels = getattr(renpy.config, "controller_use_button_labels", "auto")

            if use_labels is True or use_labels == "auto":
                lbl = c.get_button_label_string(ev.button)
                if lbl in ("a", "b", "x", "y", "cross", "circle", "square", "triangle"):
                    button_name = lbl


        if not button_name:
            button_name = get_string_for_button(ev.button)

        if button_name:
            controller_event(button_name, pr)
        return rv

    elif ev.type in (
        pygame.JOYAXISMOTION,
        pygame.JOYHATMOTION,
        pygame.JOYBALLMOTION,
        pygame.JOYBUTTONDOWN,
        pygame.JOYBUTTONUP,
        pygame.JOYDEVICEADDED,
        pygame.JOYDEVICEREMOVED,
    ):
        if not renpy.config.pass_joystick_events:
            return None

    return ev
