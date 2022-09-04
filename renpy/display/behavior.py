# Copyright 2004-2022 Tom Rothamel <pytom@bishoujo.us>
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

# This contains various Displayables that handle events.

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *


import math
import re

import pygame_sdl2 as pygame
import renpy
from renpy.display.render import render, Render


def compile_event(key, keydown):
    """
    Compiles a keymap entry into a python expression.

    keydown determines if we are dealing with keys going down (press),
    or keys going up (release).
    """

    # Lists or tuples get turned into or expressions.
    if isinstance(key, (list, tuple)):
        if not key:
            return "(False)"

        return "(" + " or ".join([compile_event(i, keydown) for i in key]) + ")"

    # If it's in config.keymap, compile what's in config.keymap.
    if key in renpy.config.keymap:
        return compile_event(renpy.config.keymap[key], keydown)

    if key in renpy.config.default_keymap:
        return compile_event(renpy.config.default_keymap[key], keydown)

    if key is None:
        return "(False)"

    part = key.split("_")

    # Deal with the mouse.
    if part[0] == "mousedown":
        if keydown:
            return "(ev.type == %d and ev.button == %d)" % (pygame.MOUSEBUTTONDOWN, int(part[1]))
        else:
            return "(False)"

    if part[0] == "mouseup":
        if keydown:
            return "(ev.type == %d and ev.button == %d)" % (pygame.MOUSEBUTTONUP, int(part[1]))
        else:
            return "(False)"


    MODIFIERS = { "keydown", "keyup", "repeat", "alt", "meta", "shift", "noshift", "ctrl", "osctrl" }
    modifiers = set()

    while part[0] in MODIFIERS:
        modifiers.add(part.pop(0))

    # Deal with the Joystick / Gamepad.
    if part[0] == "joy" or part[0] == "pad":
        return "(False)"

    key = "_".join(part)

    if "keydown" in modifiers:
        keydown = True
    elif "keyup" in modifiers:
        keydown = False

    # Otherwise, deal with it as a key.
    if keydown:
        rv = "(ev.type == %d" % pygame.KEYDOWN
    else:
        rv = "(ev.type == %d" % pygame.KEYUP

    if "repeat" in modifiers:
        rv += " and (ev.repeat)"
    else:
        rv += " and (not ev.repeat)"

    if key not in [ "K_LALT", "K_RALT" ]:

        if "alt" in modifiers or (renpy.macintosh and "osctrl" in modifiers):
            rv += " and (ev.mod & %d)" % pygame.KMOD_ALT
        else:
            rv += " and not (ev.mod & %d)" % pygame.KMOD_ALT

    if key not in [ "K_LGUI", "K_RGUI" ]:

        if "meta" in modifiers:
            rv += " and (ev.mod & %d)" % pygame.KMOD_META
        else:
            rv += " and not (ev.mod & %d)" % pygame.KMOD_META

    if key not in [ "K_LCTRL", "K_RCTRL" ]:

        if "ctrl" in modifiers or (not renpy.macintosh and "osctrl" in modifiers):
            rv += " and (ev.mod & %d)" % pygame.KMOD_CTRL
        else:
            rv += " and not (ev.mod & %d)" % pygame.KMOD_CTRL

    if key not in [ "K_LSHIFT", "K_RSHIFT" ]:

        if "shift" in modifiers:
            rv += " and (ev.mod & %d)" % pygame.KMOD_SHIFT

        if "noshift" in modifiers:
            rv += " and not (ev.mod & %d)" % pygame.KMOD_SHIFT

    if len(part) == 1:
        if len(part[0]) != 1:
            if renpy.config.developer:
                raise Exception("Invalid key specifier %s" % key)
            else:
                return "(False)"

        rv += " and ev.unicode == %r)" % part[0]

    else:
        if part[0] != "K":
            if renpy.config.developer:
                raise Exception("Invalid key specifier %s" % key)
            else:
                return "(False)"

        rv += " and ev.key == %d)" % (getattr(pygame.constants, key)) # type: ignore

    return rv


# These store a lambda for each compiled key in the system.
event_cache = { }
keyup_cache = { }


def clear_keymap_cache():
    """
    :doc: other

    Clears the keymap cache. This allows changes to :var:`config.keymap` to
    take effect without restarting Ren'Py.
    """

    event_cache.clear()
    keyup_cache.clear()


def queue_event(name, up=False, **kwargs):
    """
    :doc: other

    Queues an event with the given name. `Name` should be one of the event
    names in :var:`config.keymap`, or a list of such names.

    `up`
        This should be false when the event begins (for example, when a keyboard
        button is pressed.) It should be true when the event ends (when the
        button is released.)

    The event is queued at the time this function is called. This function will
    not work to replace an event with another - doing so will change event order.
    (Use :var:`config.keymap` instead.)

    This method is threadsafe.
    """

    # Avoid queueing events before we're ready.
    if not renpy.display.interface:
        return

    if not isinstance(name, (list, tuple)):
        name = [ name ]

    data = { "eventnames" : name, "up" : up }
    data.update(kwargs)

    ev = pygame.event.Event(renpy.display.core.EVENTNAME, data)
    pygame.event.post(ev)


def map_event(ev, keysym):
    """
    :doc: udd_utility

    Returns true if the pygame event `ev` matches `keysym`

    `keysym`
        One of:

        * The name of a keybinding in :var:`config.keymap`.
        * A keysym, as documented in the :ref:`keymap` section.
        * A list containing one or more keysyms.
    """

    if ev.type == renpy.display.core.EVENTNAME:
        if (keysym in ev.eventnames) and not ev.up:
            return True

        return False

    if isinstance(keysym, list):
        keysym = tuple(keysym)

    check_code = event_cache.get(keysym, None)
    if check_code is None:
        check_code = eval("lambda ev : " + compile_event(keysym, True), globals())
        event_cache[keysym] = check_code

    return check_code(ev)


def map_keyup(ev, keysym):
    """Returns true if the event matches the named keycode being released."""

    if ev.type == renpy.display.core.EVENTNAME:
        if (keysym in ev.eventnames) and ev.up:
            return True

    if isinstance(keysym, list):
        keysym = tuple(keysym)

    check_code = keyup_cache.get(keysym, None)
    if check_code is None:
        check_code = eval("lambda ev : " + compile_event(keysym, False), globals())
        keyup_cache[keysym] = check_code

    return check_code(ev)


def skipping(ev):
    """
    This handles setting skipping in response to the press of one of the
    CONTROL keys. The library handles skipping in response to TAB.
    """

    if not renpy.config.allow_skipping:
        return

    if not renpy.store._skipping:
        return

    if map_event(ev, "skip"):

        if (renpy.game.interface.text_rect is None) or renpy.config.skip_during_text:
            renpy.config.skipping = "slow"
            renpy.exports.restart_interaction()

    if map_keyup(ev, "skip") or map_event(ev, "stop_skipping"):
        renpy.config.skipping = None
        renpy.exports.restart_interaction()

    return


def inspector(ev):
    return map_event(ev, "inspector")

##############################################################################
# Utility functions for dealing with actions.


def predict_action(var):
    """
    Predicts some of the actions that may be caused by a variable.
    """

    if var is None:
        return

    if isinstance(var, renpy.ui.Action):
        var.predict()

    if isinstance(var, (list, tuple)):
        for i in var:
            predict_action(i)


def run(action, *args, **kwargs):
    """
    :doc: run
    :name: renpy.run
    :args: (action)

    Run an action or list of actions. A single action is called with no
    arguments, a list of actions is run in order using this function, and
    None is ignored.

    Returns the result of the last action to return a value.
    """

    if action is None:
        return None

    if isinstance(action, (list, tuple)):
        rv = None

        for i in action:
            new_rv = run(i, *args, **kwargs)

            if new_rv is not None:
                rv = new_rv

        return rv

    return action(*args, **kwargs)


def run_unhovered(var):
    """
    Calls the unhovered method on the variable, if it exists.
    """

    if var is None:
        return None

    if isinstance(var, (list, tuple)):
        for i in var:
            run_unhovered(i)

        return

    f = getattr(var, "unhovered", None)
    if f is not None:
        f()


def run_periodic(var, st):

    if isinstance(var, (list, tuple)):
        rv = None

        for i in var:
            v = run_periodic(i, st)

            if (v is not None) and (rv is None or v < rv):
                rv = v

        return rv

    if isinstance(var, renpy.ui.Action):
        return var.periodic(st)


def get_tooltip(action):

    if isinstance(action, (list, tuple)):
        for i in action:
            rv = get_tooltip(i)
            if rv is not None:
                return rv

        return None

    func = getattr(action, "get_tooltip", None)
    if func is None:
        return None

    return func()


def is_selected(action):
    """
    :name: renpy.is_selected
    :doc: run

    Returns a true value if the provided action or list of actions
    indicates it is selected, and false otherwise.
    """

    if isinstance(action, (list, tuple)):
        for i in action:
            if isinstance(i, renpy.store.SelectedIf): # type: ignore
                return i.get_selected()
        return any(is_selected(i) for i in action)

    elif isinstance(action, renpy.ui.Action):
        return action.get_selected()
    else:
        return False


def is_sensitive(action):
    """
    :name: renpy.is_sensitive
    :doc: run

    Returns a true value if the provided action or list of actions
    indicates it is sensitive, and false otherwise.
    """

    if isinstance(action, (list, tuple)):
        for i in action:
            if isinstance(i, renpy.store.SensitiveIf): # type: ignore
                return i.get_sensitive()
        return all(is_sensitive(i) for i in action)

    elif isinstance(action, renpy.ui.Action):
        return action.get_sensitive()
    else:
        return True


def alt(clicked):

    if isinstance(clicked, (list, tuple)):
        rv = [ ]

        for i in clicked:
            t = alt(i)
            if t is not None:
                rv.append(t)

        if rv:
            return " ".join(rv)
        else:
            return None

    if isinstance(clicked, renpy.ui.Action):
        return clicked.alt
    else:
        return None

##############################################################################
# Special-Purpose Displayables


class Keymap(renpy.display.layout.Null):
    """
    This is a behavior that maps keys to actions that are called when
    the key is pressed. The keys are specified by giving the appropriate
    k_constant from pygame.constants, or the unicode for the key.
    """

    capture = True
    _box_skip = True

    def __init__(self, replaces=None, activate_sound=None, capture=True, **keymap):
        if activate_sound is not None:
            super(Keymap, self).__init__(style='default', activate_sound=activate_sound)
        else:
            super(Keymap, self).__init__(style='default')

        self.keymap = keymap
        self.capture = capture

    def event(self, ev, x, y, st):

        for name, action in self.keymap.items():

            if map_event(ev, name):

                renpy.exports.play(self.style.activate_sound)

                rv = run(action)

                if rv is not None:
                    return rv

                if self.capture:
                    raise renpy.display.core.IgnoreEvent()

    def predict_one_action(self):
        for i in self.keymap.values():
            predict_action(i)


class RollForward(renpy.display.layout.Null):
    """
    This behavior implements rollforward.
    """

    def __init__(self, value, **properties):
        super(RollForward, self).__init__(**properties)
        self.value = value

    def event(self, ev, x, y, st):
        if map_event(ev, "rollforward"):
            return renpy.exports.roll_forward_core(self.value)


class PauseBehavior(renpy.display.layout.Null):
    """
    This is a class implementing the Pause behavior, which is to
    return a value after a certain amount of time has elapsed.
    """

    voice = False
    modal = False

    def __init__(self, delay, result=False, voice=False, modal=None, **properties):
        super(PauseBehavior, self).__init__(**properties)

        self.delay = delay
        self.result = result
        self.voice = voice
        self.modal = (renpy.config.modal_blocks_pause) if (modal is None) else modal

    def event(self, ev, x, y, st):

        if ev.type == renpy.display.core.TIMEEVENT:

            if ev.modal and self.modal:
                renpy.game.interface.timeout(max(self.delay - st, 0))
                return

            if st >= self.delay:

                if self.voice and renpy.config.nw_voice:
                    if (not renpy.config.afm_callback()) or renpy.display.tts.is_active():
                        renpy.game.interface.timeout(0.05)
                        return

                # If we have been drawn since the timeout, simply return
                # true. Otherwise, force a redraw, and return true when
                # it comes back.
                if renpy.game.interface.drawn_since(st - self.delay):
                    return self.result
                else:
                    renpy.game.interface.force_redraw = True

        renpy.game.interface.timeout(max(self.delay - st, 0))


class PredictPauseBehavior(renpy.display.layout.Null):
    """
    This behavior implements a pause that will last until Interface.force_prediction
    becomes False, meaning that everything that can be predicted has been predicted
    and loaded.
    """

    def __init__(self, **properties):
        super(PredictPauseBehavior, self).__init__(**properties)

    def event(self, ev, x, y, st):

        if not renpy.display.interface.force_prediction:
            return False

        renpy.game.interface.timeout(0)

class SoundStopBehavior(renpy.display.layout.Null):
    """
    This is a class implementing the sound stop behavior,
    which is to return False when a sound is no longer playing
    on the named channel.
    """

    def __init__(self, channel, result=False, **properties):
        super(SoundStopBehavior, self).__init__(**properties)

        self.channel = channel
        self.result = result

    def event(self, ev, x, y, st):

        if not renpy.audio.music.get_playing(self.channel):
            return self.result

        renpy.game.interface.timeout(.025)


class SayBehavior(renpy.display.layout.Null):
    """
    This is a class that implements the say behavior,
    which is to return True (ending the interaction) if
    the user presses space or enter, or clicks the left
    mouse button.
    """

    focusable = True
    text_tuple = None

    dismiss_unfocused = [ 'dismiss_unfocused' ]

    def __init__(self, default=True, afm=None, dismiss=[ 'dismiss' ], allow_dismiss=None, dismiss_unfocused=[ 'dismiss_unfocused' ], **properties):
        super(SayBehavior, self).__init__(default=default, **properties)

        if not isinstance(dismiss, (list, tuple)):
            dismiss = [ dismiss ]

        if not isinstance(dismiss_unfocused, (list, tuple)):
            dismiss_unfocused = [ dismiss_unfocused ]

        if afm is not None:
            self.afm_length = len(afm)
        else:
            self.afm_length = None

        # What keybindings lead to dismissal?
        self.dismiss = dismiss
        self.dismiss_unfocused = dismiss_unfocused

        self.allow_dismiss = allow_dismiss

    def _tts_all(self):
        raise renpy.display.tts.TTSRoot()

    def set_text(self, *args):
        self.text_tuple = args

        self.afm_length = 1
        self.text_time = 0

        for text in args:

            try:
                afm_text = text.text[0][text.start:text.end]
                afm_text = renpy.text.extras.filter_text_tags(afm_text, allow=[])
                self.afm_length += max(len(afm_text), 1)
            except Exception:
                self.afm_length += max(text.end - text.start, 1)

    def event(self, ev, x, y, st):

        if self.afm_length and renpy.game.preferences.afm_time and renpy.game.preferences.afm_enable:

            afm_delay = (1.0 * (renpy.config.afm_bonus + self.afm_length) / renpy.config.afm_characters) * renpy.game.preferences.afm_time

            if self.text_tuple is not None:
                max_time = 0

                for t in self.text_tuple:
                    max_time = max(max_time, t.get_time())

                afm_delay += max_time

            if ev.type == renpy.display.core.TIMEEVENT and ev.modal:
                return None

            if st > afm_delay:
                if renpy.config.afm_callback:
                    if renpy.config.afm_callback() and not renpy.display.tts.is_active():
                        return True
                    else:
                        renpy.game.interface.timeout(0.1)
                else:
                    return True
            else:
                renpy.game.interface.timeout(afm_delay - st)

        dismiss = [ (i, True) for i in self.dismiss ] + [ (i, False) for i in self.dismiss_unfocused ] # type: ignore

        for dismiss_event, check_focus in dismiss:

            if map_event(ev, dismiss_event):

                if check_focus and not self.is_focused():
                    continue

                if renpy.config.skipping:
                    renpy.config.skipping = None
                    renpy.exports.restart_interaction()
                    raise renpy.display.core.IgnoreEvent()

                if not renpy.config.enable_rollback_side:
                    rollback_side = "disable"
                if renpy.exports.variant("mobile"):
                    rollback_side = renpy.game.preferences.mobile_rollback_side
                else:
                    rollback_side = renpy.game.preferences.desktop_rollback_side

                if ev.type == pygame.MOUSEBUTTONUP:

                    percent = 1.0 * x / renpy.config.screen_width

                    if rollback_side == "left":

                        if percent < renpy.config.rollback_side_size:
                            renpy.exports.rollback()
                            raise renpy.display.core.IgnoreEvent()

                    elif rollback_side == "right":

                        if (1.0 - percent) < renpy.config.rollback_side_size:
                            renpy.exports.rollback()
                            raise renpy.display.core.IgnoreEvent()

                if renpy.game.preferences.using_afm_enable and \
                        renpy.game.preferences.afm_enable and \
                        not renpy.game.preferences.afm_after_click:

                    renpy.game.preferences.afm_enable = False
                    renpy.exports.restart_interaction()
                    raise renpy.display.core.IgnoreEvent()

                if self.allow_dismiss:
                    if not self.allow_dismiss():
                        raise renpy.display.core.IgnoreEvent()

                return True

        skip_delay = renpy.config.skip_delay / 1000.0

        if renpy.config.skipping and renpy.config.allow_skipping and renpy.store._skipping:

            if ev.type == renpy.display.core.TIMEEVENT and st >= skip_delay:

                if ev.modal:
                    return None
                elif renpy.game.preferences.skip_unseen:
                    return True
                elif renpy.config.skipping == "fast":
                    return True
                elif renpy.game.context().seen_current(True):
                    return True
                else:
                    renpy.config.skipping = None
                    renpy.exports.restart_interaction()

            else:
                renpy.game.interface.timeout(skip_delay - st)

        return None


class DismissBehavior(renpy.display.core.Displayable):
    """
    This is used to implement the dismiss screen language statement.
    """

    focusable = True

    def __init__(self, action=None, modal=True, **properties):
        super(DismissBehavior, self).__init__(**properties)


        if action is None:
            raise Exception("Dismiss requires an action.")

        self.action = action
        self.modal = modal

    def _tts(self):
        return ""

    def _tts_all(self):
        rv = self._tts_common(alt(self.action))
        return rv

    def find_focusable(self, callback, focus_name):
        if self.modal and not callable(self.modal):
            renpy.display.focus.mark_modal()

        super(DismissBehavior, self).find_focusable(callback, focus_name)

    def render(self, width, height, st, at):
        rv = renpy.display.render.Render(0, 0)

        rv.add_focus(self, None, None, None, None, None) # type: ignore

        if self.modal and not callable(self.modal):
            rv.modal = "default" # type: ignore

        return rv

    def event(self, ev, x, y, st):

        if self.is_focused() and map_event(ev, "dismiss"):
            renpy.exports.play(self.style.activate_sound)
            rv = run(self.action)

            if rv is not None:
                return rv
            else:
                raise renpy.display.core.IgnoreEvent()

        if renpy.display.layout.check_modal(self.modal, ev, x, y, None, None):
            raise renpy.display.layout.IgnoreLayers()


##############################################################################
# Button


KEY_EVENTS = (
    pygame.KEYDOWN,
    pygame.KEYUP,
    pygame.TEXTEDITING,
    pygame.TEXTINPUT
    )


class Button(renpy.display.layout.Window):

    keymap = { }
    action = None
    alternate = None

    longpress_start = None
    longpress_x = None
    longpress_y = None

    role_parameter = None

    keysym = None
    alternate_keysym = None

    # This locks the displayable against further change.
    locked = False

    def __init__(self, child=None, style='button', clicked=None,
                 hovered=None, unhovered=None, action=None, role=None,
                 time_policy=None, keymap={}, alternate=None,
                 selected=None, sensitive=None, keysym=None, alternate_keysym=None,
                 **properties):

        if isinstance(clicked, renpy.ui.Action):
            action = clicked

        super(Button, self).__init__(child, style=style, **properties)

        self.action = action
        self.selected = selected
        self.sensitive = sensitive
        self.clicked = clicked
        self.hovered = hovered
        self.unhovered = unhovered
        self.alternate = alternate

        self.focusable = True # (clicked is not None) or (action is not None)
        self.role_parameter = role

        self.keymap = keymap

        self.keysym = keysym
        self.alternate_keysym = alternate_keysym

        self.time_policy_data = None

        self._duplicatable = False

    def _get_tooltip(self):
        if self._tooltip is not None:
            return self._tooltip

        return get_tooltip(self.action)

    def _in_current_store(self):
        rv = self._copy()
        rv.style = self.style.copy()
        rv.set_style_prefix(self.style.prefix, True)
        rv.focusable = False
        rv.locked = True
        return rv

    def predict_one_action(self):
        predict_action(self.clicked)
        predict_action(self.hovered)
        predict_action(self.unhovered)
        predict_action(self.alternate)

        if self.keymap:
            for v in self.keymap.values():
                predict_action(v)

    def render(self, width, height, st, at):

        if self.style.time_policy:
            st, self.time_policy_data = self.style.time_policy(st, self.time_policy_data, self.style)

        rv = super(Button, self).render(width, height, st, at)

        if self.clicked:

            rect = self.style.focus_rect
            if rect is not None:
                fx, fy, fw, fh = rect
            else:
                fx = self.style.left_margin
                fy = self.style.top_margin
                fw = rv.width - self.style.right_margin
                fh = rv.height - self.style.bottom_margin

            mask = self.style.focus_mask

            if mask is True:
                mask = rv
            elif mask is not None:
                try:
                    mask = renpy.display.render.render(mask, rv.width, rv.height, st, at)
                except Exception:
                    if callable(mask):
                        mask = mask
                    else:
                        raise Exception("Focus_mask must be None, True, a displayable, or a callable.")

            if mask is not None:
                fmx = 0
                fmy = 0
            else:
                fmx = None
                fmy = None

            rv.add_focus(self, None,
                         fx, fy, fw, fh,
                         fmx, fmy, mask)

        return rv

    def focus(self, default=False):
        super(Button, self).focus(default)

        rv = None

        if not default:
            rv = run(self.hovered)

        self.set_transform_event(self.role + "hover")

        if self.child is not None:
            self.child.set_transform_event(self.role + "hover")

        return rv

    def unfocus(self, default=False):
        super(Button, self).unfocus(default)

        self.longpress_start = None

        if not default:
            run_unhovered(self.hovered)
            run(self.unhovered)

        self.set_transform_event(self.role + "idle")

        if self.child is not None:
            self.child.set_transform_event(self.role + "idle")

    def is_selected(self):
        if self.selected is not None:
            return self.selected
        return is_selected(self.action)

    def is_sensitive(self):
        if self.sensitive is not None:
            return self.sensitive
        return is_sensitive(self.action)

    def per_interact(self):

        if not self.locked:

            if self.action is not None:
                if self.is_selected():
                    role = 'selected_'
                else:
                    role = ''

                if self.is_sensitive():
                    clicked = self.action
                else:
                    clicked = None
                    role = ''

            else:
                role = ''
                clicked = self.clicked

            if self.role_parameter is not None:
                role = self.role_parameter

            if (role != self.role) or (clicked is not self.clicked):
                renpy.display.render.invalidate(self)
                self.role = role
                self.clicked = clicked

            if self.clicked is not None:
                self.set_style_prefix(self.role + "idle_", True)
                self.focusable = True
            else:
                self.set_style_prefix(self.role + "insensitive_", True)
                self.focusable = False

        super(Button, self).per_interact()

    def event(self, ev, x, y, st):

        if self.locked:
            return None

        def handle_click(action):
            renpy.exports.play(self.style.activate_sound)

            rv = run(action)

            if rv is not None:
                return rv
            else:
                raise renpy.display.core.IgnoreEvent()

        # Call self.action.periodic()
        timeout = run_periodic(self.action, st)

        if timeout is not None:
            renpy.game.interface.timeout(timeout)

        # If we have a child, try passing the event to it. (For keyboard
        # events, this only happens if we're focused.)
        if (not (ev.type in KEY_EVENTS)) or self.style.key_events:
            rv = super(Button, self).event(ev, x, y, st)
            if rv is not None:
                return rv

        if (self.keysym is not None) and (self.clicked is not None):
            if map_event(ev, self.keysym):
                return handle_click(self.clicked)

        if (self.alternate_keysym is not None) and (self.alternate is not None):
            if map_event(ev, self.alternate_keysym):
                return handle_click(self.alternate)

        # If not focused, ignore all events.
        if not self.is_focused():
            return None

        # Check the keymap.
        for name, action in self.keymap.items():
            if map_event(ev, name):
                return run(action)

        # Handle the longpress event, if necessary.
        if (self.alternate is not None) and renpy.display.touch:

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.longpress_start = st
                self.longpress_x = x
                self.longpress_y = y

                renpy.game.interface.timeout(renpy.config.longpress_duration)

            if self.longpress_start is not None:
                if math.hypot(x - self.longpress_x, y - self.longpress_y) > renpy.config.longpress_radius:
                    self.longpress_start = None
                elif st >= (self.longpress_start + renpy.config.longpress_duration):
                    renpy.exports.vibrate(renpy.config.longpress_vibrate)
                    renpy.display.interface.after_longpress()

                    return handle_click(self.alternate)

        # Ignore as appropriate:
        if (self.clicked is not None) and map_event(ev, "button_ignore"):
            raise renpy.display.core.IgnoreEvent()

        if (self.alternate is not None) and map_event(ev, "button_alternate_ignore"):
            raise renpy.display.core.IgnoreEvent()

        # If clicked,
        if (self.clicked is not None) and map_event(ev, "button_select"):
            return handle_click(self.clicked)

        if (self.alternate is not None) and map_event(ev, "button_alternate"):
            return handle_click(self.alternate)

        return None

    def set_style_prefix(self, prefix, root):
        if root:
            super(Button, self).set_style_prefix(prefix, root)

    def _tts(self):
        return ""

    def _tts_all(self):
        rv = self._tts_common(alt(self.action))

        if self.is_selected():
            rv += " " + renpy.minstore.__("selected")

        return rv

# Reimplementation of the TextButton widget as a Button and a Text
# widget.


def TextButton(text, style='button', text_style='button_text',
               clicked=None, **properties):

    text_properties, button_properties = renpy.easy.split_properties(properties, "text_", "")

    text = renpy.text.text.Text(text, style=text_style, **text_properties) # @UndefinedVariable
    return Button(text, style=style, clicked=clicked, **button_properties)


class ImageButton(Button):
    """
    Used to implement the guts of an image button.
    """

    imagebutton_child = None
    imagebutton_raw_child = None

    def __init__(self,
                 idle_image,
                 hover_image=None,
                 insensitive_image=None,
                 activate_image=None,
                 selected_idle_image=None,
                 selected_hover_image=None,
                 selected_insensitive_image=None,
                 selected_activate_image=None,
                 style='image_button',
                 clicked=None,
                 hovered=None,
                 **properties):

        hover_image = hover_image or idle_image
        insensitive_image = insensitive_image or idle_image
        activate_image = activate_image or hover_image

        selected_idle_image = selected_idle_image or idle_image
        selected_hover_image = selected_hover_image or hover_image
        selected_insensitive_image = selected_insensitive_image or insensitive_image
        selected_activate_image = selected_activate_image or activate_image

        self.state_children = dict(
            idle_=renpy.easy.displayable(idle_image),
            hover_=renpy.easy.displayable(hover_image),
            insensitive_=renpy.easy.displayable(insensitive_image),
            activate_=renpy.easy.displayable(activate_image),

            selected_idle_=renpy.easy.displayable(selected_idle_image),
            selected_hover_=renpy.easy.displayable(selected_hover_image),
            selected_insensitive_=renpy.easy.displayable(selected_insensitive_image),
            selected_activate_=renpy.easy.displayable(selected_activate_image),
            )

        super(ImageButton, self).__init__(None,
                                          style=style,
                                          clicked=clicked,
                                          hovered=hovered,
                                          **properties)

    def visit(self):
        if self.imagebutton_child is None:
            return list(self.state_children.values())
        else:
            return list(self.state_children.values()) + [ self.imagebutton_child ]

    def get_child(self):

        raw_child = self.style.child or self.state_children[self.style.prefix]

        if raw_child is not self.imagebutton_raw_child:
            self.imagebutton_raw_child = raw_child

            if raw_child._duplicatable:
                self.imagebutton_child = raw_child._duplicate(None)
                self.imagebutton_child._unique()
            else:
                self.imagebutton_child = raw_child

            self.imagebutton_child.per_interact()

        return self.imagebutton_child


# This is used for an input that takes its focus from a button.
class HoveredProxy(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self):
        self.a()
        if self.b:
            return self.b()


# The currently editable input value.
current_input_value = None

# Is the current input value active?
input_value_active = False

# The default input value to use if the currently editable value doesn't
# exist.
default_input_value = None

# A list of input values that exist.
input_values = [ ]

# A list of inputs that exist in the current interaction.
inputs = [ ]


def input_pre_per_interact():
    global input_values
    global inputs
    global default_input_value

    input_values = [ ]
    inputs = [ ]
    default_input_value = None


def input_post_per_interact():

    global current_input_value
    global input_value_active

    for i in input_values:
        if i is current_input_value:
            break

    else:

        current_input_value = default_input_value

        input_value_active = True

    for i in inputs:

        editable = (i.value is current_input_value) and input_value_active and i.value.editable

        content = i.value.get_text()

        if (i.editable != editable) or (content != i.content):
            i.update_text(content, editable)
            i.caret_pos = len(content)


class CaretBlink(renpy.display.core.Displayable):
    """
    A displayable that renders the caret.
    """

    def __init__(self, caret, caret_blink, **properties):

        properties.setdefault("yalign", 0.0)

        super(CaretBlink, self).__init__(**properties)
        caret = renpy.easy.displayable(caret)

        if caret._duplicatable:
            caret = caret._duplicate(None)
            caret._unique()

        self.caret = caret
        self.caret_blink = caret_blink

        self.st_base = 0

    def get_placement(self):
        return self.caret.get_placement()

    def visit(self):
        return [ self.caret ]

    def render(self, width, height, st, at):
        st -= self.st_base

        cr = renpy.display.render.render(self.caret, width, height, st, at)
        rv = renpy.display.render.Render(1, height)

        ttl = self.caret_blink - st % self.caret_blink

        if ttl > self.caret_blink / 2.0:
            rv.blit(cr, (0, 0))

        renpy.display.render.redraw(self, ttl % (self.caret_blink / 2.))

        return rv


class Input(renpy.text.text.Text): # @UndefinedVariable
    """
    This is a Displayable that takes text as input.
    """

    changed = None
    prefix = ""
    suffix = ""
    caret_pos = 0
    old_caret_pos = 0
    pixel_width = None
    default = u""
    edit_text = u""
    value = None
    shown = False

    st = 0

    def __init__(self,
                 default="",
                 length=None,
                 style='input',
                 allow=None,
                 exclude=None,
                 prefix="",
                 suffix="",
                 changed=None,
                 button=None,
                 replaces=None,
                 editable=True,
                 pixel_width=None,
                 value=None,
                 copypaste=False,
                 caret_blink=None,
                 **properties):

        super(Input, self).__init__("", style=style, replaces=replaces, substitute=False, **properties)

        if caret_blink is None:
            caret_blink = renpy.config.input_caret_blink

        if value:
            self.value = value
            changed = value.set_text
            default = value.get_text()

        self.default = str(default)
        self.content = self.default

        self.length = length

        self.allow = allow
        self.exclude = exclude
        self.prefix = prefix
        self.suffix = suffix
        self.copypaste = copypaste

        self.changed = changed

        self.editable = editable
        self.pixel_width = pixel_width

        caretprops = { 'color' : None }

        for i in properties:
            if i.endswith("color"):
                caretprops[i] = properties[i]

        caret = renpy.display.image.Solid(xysize=(1, renpy.store.preferences.font_size), style=style, **caretprops)

        if caret_blink:
            caret = CaretBlink(caret, caret_blink)

        self.caret = caret
        self.caret_pos = len(self.content)
        self.old_caret_pos = self.caret_pos

        if button:
            self.editable = False
            button.hovered = HoveredProxy(self.enable, button.hovered)
            button.unhovered = HoveredProxy(self.disable, button.unhovered)

        if isinstance(replaces, Input):
            self.content = replaces.content
            self.editable = replaces.editable
            self.caret_pos = replaces.caret_pos
            self.shown = replaces.shown

        self.update_text(self.content, self.editable)

    def update_text(self, new_content, editable, check_size=False):

        edit = renpy.display.interface.text_editing

        old_content = self.content

        if new_content != self.content or editable != self.editable or edit:

            renpy.display.render.redraw(self, 0)

        self.editable = editable

        # Choose the caret.
        caret = self.style.caret

        if caret is None:
            caret = self.caret

        # Format text being edited by the IME.
        if edit:

            self.edit_text = edit.text

            edit_text_0 = edit.text[:edit.start]
            edit_text_1 = edit.text[edit.start:edit.start + edit.length]
            edit_text_2 = edit.text[edit.start + edit.length:]

            edit_text = ""

            if edit_text_0:
                edit_text += "{u=1}" + edit_text_0.replace("{", "{{") + "{/u}"

            if edit_text_1:
                edit_text += "{u=2}" + edit_text_1.replace("{", "{{") + "{/u}"

            if edit_text_2:
                edit_text += "{u=1}" + edit_text_2.replace("{", "{{") + "{/u}"

        else:
            self.edit_text = ""
            edit_text = ""

        def set_content(content):

            if content == "":
                content = u" "

            if editable:
                l = len(content)
                self.set_text([self.prefix, content[0:self.caret_pos].replace("{", "{{"), edit_text, caret,
                               content[self.caret_pos:l].replace("{", "{{"), self.suffix])
            else:
                self.set_text([self.prefix, content.replace("{", "{{"), self.suffix ])

            if isinstance(self.caret, CaretBlink):
                self.caret.st_base = self.st
                renpy.display.render.redraw(self.caret, 0)

        set_content(new_content)

        if check_size and self.pixel_width:
            w, _h = self.size()
            if w > self.pixel_width:
                self.caret_pos = self.old_caret_pos
                set_content(old_content)
                return

        if new_content != old_content:
            self.content = new_content

            if self.changed:
                self.changed(new_content)

    # This is needed to ensure the caret updates properly.
    def set_style_prefix(self, prefix, root):
        if prefix != self.style.prefix:
            self.update_text(self.content, self.editable)

        super(Input, self).set_style_prefix(prefix, root)

    def enable(self):
        self.update_text(self.content, True)

    def disable(self):
        self.update_text(self.content, False)

    def per_interact(self):

        global default_input_value

        if self.value is not None:

            inputs.append(self)
            input_values.append(self.value)

            if self.value.default and (default_input_value is None):
                default_input_value = self.value

        if not self.shown:

            if self.value is not None:
                default = self.value.get_text()
                self.default = str(default)

            self.content = self.default
            self.caret_pos = len(self.content)
            self.update_text(self.content, self.editable)

            self.shown = True

    def event(self, ev, x, y, st):

        self.st = st
        self.old_caret_pos = self.caret_pos

        if not self.editable:
            return None

        edit_controls = any([
            map_event(ev, "input_jump_word_left"),
            map_event(ev, "input_jump_word_right"),
            map_event(ev, "input_delete_word"),
            map_event(ev, "input_delete_full"),
        ])

        if (ev.type == pygame.KEYDOWN) and (pygame.key.get_mods() & pygame.KMOD_LALT) and (not ev.unicode) and not edit_controls:
            return None

        l = len(self.content)

        raw_text = None

        if map_event(ev, "input_backspace"):

            if self.content and self.caret_pos > 0:
                content = self.content[0:self.caret_pos - 1] + self.content[self.caret_pos:l]
                self.caret_pos -= 1
                self.update_text(content, self.editable)

            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif map_event(ev, "input_enter"):

            content = self.content

            if self.edit_text:
                content = content[0:self.caret_pos] + self.edit_text + self.content[self.caret_pos:]

            if self.value:
                return self.value.enter()

            if not self.changed:
                return content

        elif map_event(ev, "input_left"):
            if self.caret_pos > 0:
                self.caret_pos -= 1
                self.update_text(self.content, self.editable)

            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif map_event(ev, "input_jump_word_left"):
            if self.caret_pos > 0:
                space_pos = 0
                for item in re.finditer(r"\s+", self.content[:self.caret_pos]):
                    start, end = item.span()
                    if end != self.caret_pos:
                        space_pos = end
                self.caret_pos = space_pos
                self.update_text(self.content, self.editable)

            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif map_event(ev, "input_right"):
            if self.caret_pos < l:
                self.caret_pos += 1
                self.update_text(self.content, self.editable)

            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif map_event(ev, "input_jump_word_right"):
            if self.caret_pos < l:
                space_pos = l
                for item in re.finditer(r"\s+", self.content[self.caret_pos + 1:]):
                    start, end = item.span()
                    space_pos = end
                    break
                self.caret_pos = min(space_pos + self.caret_pos + 1, l)
                self.update_text(self.content, self.editable)

            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif map_event(ev, "input_delete"):
            if self.caret_pos < l:
                content = self.content[0:self.caret_pos] + self.content[self.caret_pos + 1:l]
                self.update_text(content, self.editable)

            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif map_event(ev, "input_delete_word"):
            if self.caret_pos <= l:
                space_pos = 0
                for item in re.finditer(r"\s+", self.content[:self.caret_pos]):
                    start, end = item.span()
                    if end != self.caret_pos:
                        space_pos = end
                content = self.content[0:space_pos] + self.content[self.caret_pos:l]
                self.caret_pos = space_pos
                self.update_text(content, self.editable)

            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif map_event(ev, "input_delete_full"):
            if self.caret_pos <= l:
                content = self.content[self.caret_pos:l]
                self.caret_pos = 0
                self.update_text(content, self.editable)

            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif map_event(ev, "input_home"):
            self.caret_pos = 0
            self.update_text(self.content, self.editable)
            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif map_event(ev, "input_end"):
            self.caret_pos = l
            self.update_text(self.content, self.editable)
            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif self.copypaste and map_event(ev, "input_copy"):
            text = self.content.encode("utf-8")
            pygame.scrap.put(pygame.scrap.SCRAP_TEXT, text)
            raise renpy.display.core.IgnoreEvent()

        elif self.copypaste and map_event(ev, "input_paste"):
            text = pygame.scrap.get(pygame.scrap.SCRAP_TEXT)
            text = text.decode("utf-8")
            raw_text = ""
            for c in text:
                if ord(c) >= 32:
                    raw_text += c

        elif ev.type == pygame.TEXTEDITING:
            self.update_text(self.content, self.editable, check_size=True)

            raise renpy.display.core.IgnoreEvent()

        elif ev.type == pygame.TEXTINPUT:
            self.edit_text = ""
            raw_text = ev.text

        elif ev.type == pygame.KEYDOWN:

            if ev.unicode and ord(ev.unicode[0]) >= 32:
                raw_text = ev.unicode
            elif renpy.display.interface.text_event_in_queue():
                raise renpy.display.core.IgnoreEvent()
            elif (32 <= ev.key < 127) and not (ev.mod & (pygame.KMOD_ALT | pygame.KMOD_META)):
                # Ignore printable keycodes without unicode.
                raise renpy.display.core.IgnoreEvent()

        if raw_text is not None:

            text = ""

            for c in raw_text:

                # Allow is given
                if self.allow:

                    # Allow is regex
                    if isinstance(self.allow, re.Pattern):

                        # Character doesn't match
                        if self.allow.search(c) is None:
                            continue

                    # Allow is string
                    elif c not in self.allow:
                        continue

                # Exclude is given
                if self.exclude:

                    # Exclude is regex
                    if isinstance(self.exclude, re.Pattern):

                        # Character matches
                        if self.exclude.search(c) is not None:
                            continue

                    # Exclude is string
                    elif c in self.exclude:
                        continue

                text += c

            if self.length:
                remaining = self.length - len(self.content)
                text = text[:remaining]

            if text:

                content = self.content[0:self.caret_pos] + text + self.content[self.caret_pos:l]
                self.caret_pos += len(text)

                self.update_text(content, self.editable, check_size=True)

            raise renpy.display.core.IgnoreEvent()

    def render(self, width, height, st, at):
        self.st = st

        rv = super(Input, self).render(width, height, st, at)

        if self.editable:
            rv.text_input = True

        return rv


# A map from adjustment to lists of displayables that want to be redrawn
# if the adjustment changes.
adj_registered = { }

# This class contains information about an adjustment that can change the
# position of content.


class Adjustment(renpy.object.Object):
    """
    :doc: ui
    :name: ui.adjustment class

    Adjustment objects represent a value that can be adjusted by a bar
    or viewport. They contain information about the value, the range
    of the value, and how to adjust the value in small steps and large
    pages.


    """

    force_step = False

    def __init__(self, range=1, value=0, step=None, page=None, changed=None, adjustable=None, ranged=None, force_step=False): # @ReservedAssignment
        """
        The following parameters correspond to fields or properties on
        the adjustment object:

        `range`
            The range of the adjustment, a number.

        `value`
            The value of the adjustment, a number.

        `step`
            The step size of the adjustment, a number. If None, then
            defaults to 1/10th of a page, if set. Otherwise, defaults
            to the 1/20th of the range.

            This is used when scrolling a viewport with the mouse wheel.

        `page`
            The page size of the adjustment. If None, this is set
            automatically by a viewport. If never set, defaults to 1/10th
            of the range.

            It's can be used when clicking on a scrollbar.

        The following parameters control the behavior of the adjustment.

        `adjustable`
            If True, this adjustment can be changed by a bar. If False,
            it can't.

            It defaults to being adjustable if a `changed` function
            is given or if the adjustment is associated with a viewport,
            and not adjustable otherwise.

        `changed`
            This function is called with the new value when the value of
            the adjustment changes.

        `ranged`
            This function is called with the adjustment object when
            the range of the adjustment is set by a viewport.

            This function may be called multiple times, as part of the layout
            process.

        `force_step`
            If True and this adjustment changes by dragging associated
            viewport or a bar, value will be changed only if the drag
            reached next step.
            If "release" and this adjustment changes by dragging associated
            viewport or a bar, after the release, value will be
            rounded to the nearest step.
            If False, this adjustment will changes by dragging, ignoring
            the step value.

        .. method:: change(value)

            Changes the value of the adjustment to `value`, updating
            any bars and viewports that use the adjustment.
         """

        super(Adjustment, self).__init__()

        if adjustable is None:
            if changed:
                adjustable = True

        self._range = range
        self._value = type(range)(value)
        self._page = page
        self._step = step
        self.changed = changed
        self.adjustable = adjustable
        self.ranged = ranged
        self.force_step = force_step

    def round_value(self, value, release):
        # Prevent deadlock border points
        if value <= 0:
            return type(self._value)(0)
        elif value >= self._range:
            return self._range

        if self.force_step is False:
            return value

        if (not release) and self.force_step == "release":
            return value

        return type(self._value)(self.step * round(float(value) / self.step))

    def get_value(self):
        if self._value <= 0:
            return type(self._value)(0)
        if self._value >= self._range:
            return self._range

        return self._value

    def set_value(self, v):
        self._value = v

    value = property(get_value, set_value)

    def get_range(self):
        return self._range

    def set_range(self, v):
        self._range = v
        if self.ranged:
            self.ranged(self)

    range = property(get_range, set_range) # @ReservedAssignment

    def get_page(self):
        if self._page is not None:
            return self._page

        return self._range / 10

    def set_page(self, v):
        self._page = v

    page = property(get_page, set_page)

    def get_step(self):
        if self._step is not None:
            return self._step

        if self._page is not None and self.page > 0:
            return self._page / 10

        if isinstance(self._range, float):
            return self._range / 10
        else:
            return 1

    def set_step(self, v):
        self._step = v

    step = property(get_step, set_step)

    # Register a displayable to be redrawn when this adjustment changes.
    def register(self, d):
        adj_registered.setdefault(self, [ ]).append(d)

    def change(self, value):

        if value < 0:
            value = 0
        if value > self._range:
            value = self._range

        if value != self._value:
            self._value = value
            for d in adj_registered.setdefault(self, [ ]):
                renpy.display.render.redraw(d, 0)
            if self.changed:
                return self.changed(value)

        return None

    def update(self):
        """
        Updates things that depend on this adjustment without firing the
        changed handler.
        """

        for d in adj_registered.setdefault(self, [ ]):
            renpy.display.render.invalidate(d)


class Bar(renpy.display.core.Displayable):
    """
    Implements a bar that can display an integer value, and respond
    to clicks on that value.
    """

    __version__ = 2

    def after_upgrade(self, version):

        if version < 1:
            self.adjustment = Adjustment(self.range, self.value, changed=self.changed) # type: ignore
            self.adjustment.register(self)
            del self.range # type: ignore
            del self.value # type: ignore
            del self.changed # type: ignore

        if version < 2:
            self.value = None

    def __init__(self,
                 range=None, # @ReservedAssignment
                 value=None,
                 width=None,
                 height=None,
                 changed=None,
                 adjustment=None,
                 step=None,
                 page=None,
                 bar=None,
                 style=None,
                 vertical=False,
                 replaces=None,
                 hovered=None,
                 unhovered=None,
                 released=None,
                 **properties):

        self.value = None

        if adjustment is None:
            if isinstance(value, renpy.ui.BarValue):

                if isinstance(replaces, Bar):
                    value.replaces(replaces.value)

                self.value = value
                adjustment = value.get_adjustment()
                renpy.game.interface.timeout(0)

                tooltip = value.get_tooltip()
                if tooltip is not None:
                    properties.setdefault("tooltip", tooltip)

            else:
                adjustment = Adjustment(range, value, step=step, page=page, changed=changed)

        if style is None:
            if self.value is not None:
                if vertical:
                    style = self.value.get_style()[1]
                else:
                    style = self.value.get_style()[0]
            else:
                if vertical:
                    style = 'vbar'
                else:
                    style = 'bar'

        if width is not None:
            properties['xmaximum'] = width

        if height is not None:
            properties['ymaximum'] = height

        super(Bar, self).__init__(style=style, **properties)

        self.adjustment = adjustment
        self.focusable = True

        # These are set when we are first rendered.
        self.thumb_dim = 0
        self.height = 0
        self.width = 0
        self.hidden = False

        self.hovered = hovered
        self.unhovered = unhovered

        self.released = released

    def per_interact(self):
        if self.value is not None:
            adjustment = self.value.get_adjustment()

            if adjustment.value != self.value:
                renpy.display.render.invalidate(self)

            self.adjustment = adjustment

        self.focusable = self.adjustment.adjustable
        self.adjustment.register(self)

    def visit(self):
        rv = [ ]
        self.style._visit_bar(rv.append)
        return rv

    def render(self, width, height, st, at):

        # Handle redrawing.
        if self.value is not None:
            redraw = self.value.periodic(st)

            if redraw is not None:
                renpy.display.render.redraw(self, redraw)

        xminimum, yminimum = renpy.display.layout.xyminimums(self.style, width, height)

        if xminimum is not None:
            width = max(width, xminimum)

        if yminimum is not None:
            height = max(height, yminimum)

        # Store the width and height for the event function to use.
        self.width = width
        self.height = height
        range = self.adjustment.range # @ReservedAssignment
        value = self.adjustment.value
        page = self.adjustment.page

        if range <= 0:
            if self.style.unscrollable == "hide":
                self.hidden = True
                return renpy.display.render.Render(width, height)
            elif self.style.unscrollable == "insensitive":
                self.set_style_prefix("insensitive_", True)

        self.hidden = False

        if self.style.bar_invert ^ self.style.bar_vertical:
            value = range - value

        bar_vertical = self.style.bar_vertical

        if bar_vertical:
            dimension = height
        else:
            dimension = width

        fore_gutter = self.style.fore_gutter
        aft_gutter = self.style.aft_gutter

        active = dimension - fore_gutter - aft_gutter
        if range:
            thumb_dim = active * page // (range + page)
        else:
            thumb_dim = active

        thumb_offset = abs(self.style.thumb_offset)

        if bar_vertical:
            thumb = render(self.style.thumb, width, thumb_dim, st, at)
            thumb_shadow = render(self.style.thumb_shadow, width, thumb_dim, st, at)
            thumb_dim = thumb.height
        else:
            thumb = render(self.style.thumb, thumb_dim, height, st, at)
            thumb_shadow = render(self.style.thumb_shadow, thumb_dim, height, st, at)
            thumb_dim = thumb.width

        # Remove the offset from the thumb.
        thumb_dim -= thumb_offset * 2
        self.thumb_dim = thumb_dim

        active -= thumb_dim

        if range:
            fore_size = active * value // range
        else:
            fore_size = active

        fore_size = int(fore_size)

        aft_size = active - fore_size

        fore_size += fore_gutter
        aft_size += aft_gutter

        rv = renpy.display.render.Render(width, height)

        if bar_vertical:

            if self.style.bar_resizing:
                foresurf = render(self.style.fore_bar, width, fore_size, st, at)
                aftsurf = render(self.style.aft_bar, width, aft_size, st, at)
                rv.blit(thumb_shadow, (0, fore_size - thumb_offset))
                rv.blit(foresurf, (0, 0), main=False)
                rv.blit(aftsurf, (0, height - aft_size), main=False)
                rv.blit(thumb, (0, fore_size - thumb_offset))

            else:
                foresurf = render(self.style.fore_bar, width, height, st, at)
                aftsurf = render(self.style.aft_bar, width, height, st, at)

                rv.blit(thumb_shadow, (0, fore_size - thumb_offset))
                rv.blit(foresurf.subsurface((0, 0, width, fore_size)), (0, 0), main=False)
                rv.blit(aftsurf.subsurface((0, height - aft_size, width, aft_size)), (0, height - aft_size), main=False)
                rv.blit(thumb, (0, fore_size - thumb_offset))

        else:
            if self.style.bar_resizing:
                foresurf = render(self.style.fore_bar, fore_size, height, st, at)
                aftsurf = render(self.style.aft_bar, aft_size, height, st, at)
                rv.blit(thumb_shadow, (fore_size - thumb_offset, 0))
                rv.blit(foresurf, (0, 0), main=False)
                rv.blit(aftsurf, (width - aft_size, 0), main=False)
                rv.blit(thumb, (fore_size - thumb_offset, 0))

            else:
                foresurf = render(self.style.fore_bar, width, height, st, at)
                aftsurf = render(self.style.aft_bar, width, height, st, at)

                rv.blit(thumb_shadow, (fore_size - thumb_offset, 0))
                rv.blit(foresurf.subsurface((0, 0, fore_size, height)), (0, 0), main=False)
                rv.blit(aftsurf.subsurface((width - aft_size, 0, aft_size, height)), (width - aft_size, 0), main=False)
                rv.blit(thumb, (fore_size - thumb_offset, 0))

        if self.focusable:
            rv.add_focus(self, None, 0, 0, width, height)

        return rv

    def focus(self, default=False):
        super(Bar, self).focus(default)
        self.set_transform_event("hover")

        if not default:
            run(self.hovered)

    def unfocus(self, default=False):
        super(Bar, self).unfocus()
        self.set_transform_event("idle")

        if not default:
            run_unhovered(self.hovered)
            run(self.unhovered)

    def event(self, ev, x, y, st):

        if not self.focusable:
            return None

        if not self.is_focused():
            return None

        if self.hidden:
            return None

        range = self.adjustment.range # @ReservedAssignment
        old_value = self.adjustment.value
        value = old_value

        vertical = self.style.bar_vertical
        invert = self.style.bar_invert ^ vertical
        if invert:
            value = range - value

        grabbed = (renpy.display.focus.get_grab() is self)
        just_grabbed = False

        ignore_event = False

        if not grabbed and map_event(ev, "bar_activate"):
            renpy.display.tts.speak(renpy.minstore.__("activate"))
            renpy.display.focus.set_grab(self)
            self.set_style_prefix("selected_hover_", True)
            just_grabbed = True
            grabbed = True
            ignore_event = True
            renpy.exports.play(self.style.activate_sound)

        if grabbed:

            if vertical:
                increase = "bar_down"
                decrease = "bar_up"
            else:
                increase = "bar_right"
                decrease = "bar_left"

            if map_event(ev, decrease):
                renpy.display.tts.speak(renpy.minstore.__("decrease"))
                value -= self.adjustment.step
                ignore_event = True

            if map_event(ev, increase):
                renpy.display.tts.speak(renpy.minstore.__("increase"))
                value += self.adjustment.step
                ignore_event = True

            if ev.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):

                if vertical:

                    tgutter = self.style.fore_gutter
                    bgutter = self.style.aft_gutter
                    zone_height = self.height - tgutter - bgutter - self.thumb_dim
                    if zone_height:
                        value = (y - tgutter - self.thumb_dim / 2) * range / zone_height
                    else:
                        value = 0

                else:
                    lgutter = self.style.fore_gutter
                    rgutter = self.style.aft_gutter
                    zone_width = self.width - lgutter - rgutter - self.thumb_dim
                    if zone_width:
                        value = (x - lgutter - self.thumb_dim / 2) * range / zone_width
                    else:
                        value = 0

                ignore_event = True

            if isinstance(range, int):
                value = int(value)

            if value < 0:
                renpy.display.tts.speak("")
                value = 0

            if value > range:
                renpy.display.tts.speak("")
                value = range

        if invert:
            value = range - value

        if grabbed and not just_grabbed and map_event(ev, "bar_deactivate"):
            renpy.display.tts.speak(renpy.minstore.__("deactivate"))
            self.set_style_prefix("hover_", True)
            renpy.display.focus.set_grab(None)

            # Invoke rounding adjustment on bar release
            value = self.adjustment.round_value(value, release=True)
            if value != old_value:
                rv = self.adjustment.change(value)
                if rv is not None:
                    return rv

            rv = run(self.released)
            if rv is not None:
                return rv

            raise renpy.display.core.IgnoreEvent()

        if value != old_value:
            value = self.adjustment.round_value(value, release=False)
            rv = self.adjustment.change(value)
            if rv is not None:
                return rv

        if ignore_event:
            raise renpy.display.core.IgnoreEvent()
        else:
            return None

    def set_style_prefix(self, prefix, root):
        if root:
            super(Bar, self).set_style_prefix(prefix, root)

    def _tts(self):
        return ""

    def _tts_all(self):

        if self.value is not None:
            alt = self.value.alt
        else:
            alt = ""

        return self._tts_common(alt) + renpy.minstore.__("bar")


class Conditional(renpy.display.layout.Container):
    """
    This class renders its child if and only if the condition is
    true. Otherwise, it renders nothing. (Well, a Null).

    Warning: the condition MUST NOT update the game state in any
    way, as that would break rollback.
    """

    def __init__(self, condition, *args, **properties):
        super(Conditional, self).__init__(*args, **properties)

        self.condition = condition
        self.null = renpy.display.layout.Null()

        self.state = eval(self.condition, vars(renpy.store))

    def render(self, width, height, st, at):
        if self.state:
            return render(self.child, width, height, st, at)
        else:
            return render(self.null, width, height, st, at)

    def event(self, ev, x, y, st):

        state = eval(self.condition, vars(renpy.store))

        if state != self.state:
            renpy.display.render.redraw(self, 0)

        self.state = state

        if state:
            return self.child.event(ev, x, y, st)


class TimerState(renpy.python.AlwaysRollback):
    """
    Stores the state of the timer, which may need to be rolled back.
    """

    started = False
    next_event = None


class Timer(renpy.display.layout.Null):

    __version__ = 1

    started = False
    _box_skip = True
    modal = False

    def after_upgrade(self, version):
        if version < 1:
            self.state = TimerState()
            self.state.started = self.started
            self.state.next_event = self.next_event

    def __init__(self, delay, action=None, repeat=False, args=(), kwargs={}, replaces=None, modal=None, **properties):
        super(Timer, self).__init__(**properties)

        if delay <= 0:
            raise Exception("A timer's delay must be > 0.")

        # The delay.
        self.delay = delay

        # Should we repeat the event?
        self.repeat = repeat

        # The time the next event should occur.
        self.next_event = None

        # The function and its arguments.
        self.function = action
        self.args = args
        self.kwargs = kwargs

        # Did we start the timer?
        self.started = False

        # Should this timer trigger on modal events.
        self.modal = (renpy.config.modal_blocks_timer) if (modal is None) else modal

        if isinstance(replaces, Timer):
            self.state = replaces.state
        else:
            self.state = TimerState()

    def render(self, width, height, st, at):

        if not self.state.started:
            self.state.started = True
            self.state.next_event = st + self.delay
            renpy.game.interface.timeout(st)

        return super(Timer, self).render(width, height, st, at)

    def event(self, ev, x, y, st):

        if ev.type == renpy.display.core.TIMEEVENT and self.modal and ev.modal:
            return

        state = self.state

        if not state.started:
            state.started = True
            state.next_event = st + self.delay

        if state.next_event is None:
            return

        if st < state.next_event:
            renpy.game.interface.timeout(state.next_event - st)
            return

        if not self.repeat:
            state.next_event = None
        else:
            state.next_event = state.next_event + self.delay
            if state.next_event < st:
                state.next_event = st + self.delay

            renpy.game.interface.timeout(state.next_event - st)

        return run(self.function, *self.args, **self.kwargs)


class MouseArea(renpy.display.core.Displayable):

    # The offset between st and at.
    at_st_offset = 0

    def __init__(self, hovered=None, unhovered=None, replaces=None, **properties):
        super(MouseArea, self).__init__(**properties)

        self.hovered = hovered
        self.unhovered = unhovered

        # Are we hovered right now?
        self.is_hovered = False

        if isinstance(replaces, MouseArea):
            self.is_hovered = replaces.is_hovered

        # Taken from the render.
        self.width = 0
        self.height = 0

    def render(self, width, height, st, at):
        self.width = width
        self.height = height

        self.at_st_offset = at - st

        return Render(width, height)

    def event(self, ev, x, y, st):

        # Mouseareas should not handle events when something else is grabbing.
        if renpy.display.focus.get_grab():
            return

        if renpy.display.focus.pending_focus_type == 'keyboard':
            is_hovered = False

        elif (ev.type == renpy.display.core.TIMEEVENT) and ev.modal:
            is_hovered = False

        else:
            if self.style.focus_mask is not None:
                crend = renpy.display.render.render(self.style.focus_mask, self.width, self.height, st, self.at_st_offset + st)
                is_hovered = crend.is_pixel_opaque(x, y)
            elif 0 <= x < self.width and 0 <= y < self.height:
                is_hovered = True
            else:
                is_hovered = False

        if is_hovered and not self.is_hovered:
            self.is_hovered = True

            return run(self.hovered)

        elif not is_hovered and self.is_hovered:
            self.is_hovered = False

            run_unhovered(self.hovered)
            run(self.unhovered)


class OnEvent(renpy.display.core.Displayable):
    """
    This is a displayable that runs an action in response to a transform
    event. It's used to implement the screen language on statement.
    """

    def __init__(self, event, action=[ ]):
        """
        `event`
            A string giving the event name.

        `action`
            An action or list of actions that are run when the event occurs.
        """

        super(OnEvent, self).__init__()

        self.event_name = event
        self.action = action

    def is_event(self, event):
        if isinstance(self.event_name, basestring):
            return self.event_name == event
        else:
            return event in self.event_name

    def _handles_event(self, event):
        if self.is_event(event):
            return True
        else:
            return False

    def set_transform_event(self, event):
        if self.is_event(event):
            run(self.action)

    def render(self, width, height, st, at):
        return renpy.display.render.Render(0, 0)
