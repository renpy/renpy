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

# This contains various Displayables that handle events.


import renpy.display
import renpy.audio

from renpy.display.render import render, Render

import pygame

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

    # Deal with the Joystick.
    if part[0] == "joy":
        if keydown:
            return "(ev.type == %d and ev.press and ev.press == renpy.game.preferences.joymap.get(%r, None))" % (renpy.display.core.JOYEVENT, key)
        else:
            return "(ev.type == %d and ev.release and ev.release == renpy.game.preferences.joymap.get(%r, None))" % (renpy.display.core.JOYEVENT, key)

    # Otherwise, deal with it as a key.
    if keydown:
        rv = "(ev.type == %d" % pygame.KEYDOWN
    else:
        rv = "(ev.type == %d" % pygame.KEYUP

    if part[0] == "alt":
        part.pop(0)
        rv += " and (ev.mod & %d)" % pygame.KMOD_ALT
    else:
        rv += " and not (ev.mod & %d)" % pygame.KMOD_ALT

    if part[0] == "meta":
        part.pop(0)
        rv += " and (ev.mod & %d)" % pygame.KMOD_META
    else:
        rv += " and not (ev.mod & %d)" % pygame.KMOD_META

    if part[0] == "shift":
        part.pop(0)
        rv += " and (ev.mod & %d)" % pygame.KMOD_SHIFT

    if part[0] == "noshift":
        part.pop(0)
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

        key = "_".join(part)

        rv += " and ev.key == %d)" % (getattr(pygame.constants, key))

    return rv

# These store a lambda for each compiled key in the system.
event_cache = { }
keyup_cache = { }

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

    check_code = event_cache.get(keysym, None)
    if check_code is None:
        check_code = eval("lambda ev : " + compile_event(keysym, True), globals())
        event_cache[keysym] = check_code

    return check_code(ev)

def map_keyup(ev, name):
    """Returns true if the event matches the named keycode being released."""

    check_code = keyup_cache.get(name, None)
    if check_code is None:
        check_code = eval("lambda ev : " + compile_event(name, False), globals())
        keyup_cache[name] = check_code

    return check_code(ev)


def skipping(ev):
    """
    This handles setting skipping in response to the press of one of the
    CONTROL keys. The library handles skipping in response to TAB.
    """

    if not renpy.config.allow_skipping:
        return

    if map_event(ev, "skip"):
        renpy.config.skipping = "slow"
        renpy.exports.restart_interaction()

    if map_keyup(ev, "skip"):
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

def run(var, *args, **kwargs):
    """
    Runs a variable. This is done by calling all the functions, and
    iterating over the lists and tuples.
    """

    if var is None:
        return None

    if isinstance(var, (list, tuple)):
        rv = None

        for i in var:
            new_rv = run(i, *args, **kwargs)

            if new_rv is not None:
                rv = new_rv

        return rv

    return var(*args, **kwargs)

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

            if rv is None or v < rv:
                rv = v

        return rv

    if isinstance(var, renpy.ui.Action):
        return var.periodic(st)


def is_selected(clicked):

    if isinstance(clicked, (list, tuple)):
        return any(is_selected(i) for i in clicked)

    elif isinstance(clicked, renpy.ui.Action):
        return clicked.get_selected()
    else:
        return False


def is_sensitive(clicked):

    if isinstance(clicked, (list, tuple)):
        return all(is_sensitive(i) for i in clicked)

    elif isinstance(clicked, renpy.ui.Action):
        return clicked.get_sensitive()
    else:
        return True


##############################################################################
# Special-Purpose Displayables

class Keymap(renpy.display.layout.Null):
    """
    This is a behavior that maps keys to actions that are called when
    the key is pressed. The keys are specified by giving the appropriate
    k_constant from pygame.constants, or the unicode for the key.
    """

    def __init__(self, replaces=None, **keymap):
        super(Keymap, self).__init__(style='default')
        self.keymap = keymap

    def event(self, ev, x, y, st):

        for name, action in self.keymap.iteritems():
            if map_event(ev, name):

                rv = run(action)

                if rv is not None:
                    return rv

                raise renpy.display.core.IgnoreEvent()

    def predict_one_action(self):
        for i in self.keymap.itervalues():
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
            renpy.game.interface.suppress_transition = True
            renpy.game.after_rollback = True
            renpy.game.log.rolled_forward = True
            return self.value


class PauseBehavior(renpy.display.layout.Null):
    """
    This is a class implementing the Pause behavior, which is to
    return a value after a certain amount of time has elapsed.
    """

    def __init__(self, delay, result=False, **properties):
        super(PauseBehavior, self).__init__(**properties)

        self.delay = delay
        self.result = result

    def event(self, ev, x, y, st):

        if st >= self.delay:

            # If we have been drawn since the timeout, simply return
            # true. Otherwise, force a redraw, and return true when
            # it comes back.
            if renpy.game.interface.drawn_since(st - self.delay):
                return self.result
            else:
                renpy.game.interface.force_redraw = True


        renpy.game.interface.timeout(max(self.delay - st, 0))

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

    def __init__(self, default=True, afm=None, dismiss=[ 'dismiss' ], allow_dismiss=None, **properties):
        super(SayBehavior, self).__init__(default=default, **properties)

        if not isinstance(dismiss, (list, tuple)):
            dismiss = [ dismiss ]

        if afm is not None:
            self.afm_length = len(afm)
        else:
            self.afm_length = None

        # What keybindings lead to dismissal?
        self.dismiss = dismiss

        self.allow_dismiss = allow_dismiss

    def set_afm_length(self, afm_length):
        self.afm_length = max(afm_length, 1)

    def event(self, ev, x, y, st):

        if self.afm_length and renpy.game.preferences.afm_time and renpy.game.preferences.afm_enable:

            afm_delay = ( 1.0 * ( renpy.config.afm_bonus + self.afm_length ) / renpy.config.afm_characters ) * renpy.game.preferences.afm_time

            if renpy.game.preferences.text_cps:
                afm_delay += 1.0 / renpy.game.preferences.text_cps * self.afm_length

            if st > afm_delay:
                if renpy.config.afm_callback:
                    if renpy.config.afm_callback():
                        return True
                    else:
                        renpy.game.interface.timeout(0.1)
                else:
                    return True
            else:
                renpy.game.interface.timeout(afm_delay - st)

        for dismiss in self.dismiss:

            if map_event(ev, dismiss) and self.is_focused():

                if renpy.config.skipping:
                    renpy.config.skipping = None
                    renpy.exports.restart_interaction()
                    raise renpy.display.core.IgnoreEvent()

                if renpy.game.preferences.using_afm_enable and renpy.game.preferences.afm_enable:
                    renpy.game.preferences.afm_enable = False
                    renpy.exports.restart_interaction()
                    raise renpy.display.core.IgnoreEvent()

                if self.allow_dismiss:
                    if not self.allow_dismiss():
                        raise renpy.display.core.IgnoreEvent()

                return True

        skip_delay = renpy.config.skip_delay / 1000.0

        if renpy.config.allow_skipping and renpy.config.skipping:

            if st >= skip_delay:
                if renpy.game.preferences.skip_unseen:
                    return True
                elif renpy.config.skipping == "fast":
                    return True
                elif renpy.game.context().seen_current(True):
                    return True
            else:
                renpy.game.interface.timeout(skip_delay - st)


        return None


##############################################################################
# Button

class Button(renpy.display.layout.Window):

    keymap = { }
    action = None

    def __init__(self, child=None, style='button', clicked=None,
                 hovered=None, unhovered=None, action=None, role=None,
                 time_policy=None, keymap={},
                 **properties):

        super(Button, self).__init__(child, style=style, **properties)

        if isinstance(clicked, renpy.ui.Action):
            action = clicked

        if action is not None:
            clicked = action

            if not is_sensitive(action):
                clicked = None

        if role is None:
            if action:
                if is_selected(action):
                    role = 'selected_'
                else:
                    role = ''
            else:
                role = ''

        self.action = action
        self.activated = False
        self.clicked = clicked
        self.hovered = hovered
        self.unhovered = unhovered
        self.focusable = clicked is not None
        self.role = role
        self.keymap = keymap

        self.time_policy_data = None

    def predict_one_action(self):
        predict_action(self.clicked)
        predict_action(self.hovered)
        predict_action(self.unhovered)

        if self.keymap:
            for v in self.keymap.itervalues():
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
                mask = renpy.easy.displayable(mask)
                mask = renpy.display.render.render(mask, rv.width, rv.height, st, at)

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

        if self.activated:
            return None

        rv = None

        if not default:
            rv = run(self.hovered)

        self.set_transform_event(self.role + "hover")
        self.child.set_transform_event(self.role + "hover")

        return rv


    def unfocus(self, default=False):
        super(Button, self).unfocus(default)

        if self.activated:
            return None

        if not default:
            run_unhovered(self.hovered)
            run(self.unhovered)

        self.set_transform_event(self.role + "idle")
        self.child.set_transform_event(self.role + "idle")


    def per_interact(self):
        if not self.clicked:
            self.set_style_prefix(self.role + "insensitive_", True)
        else:
            self.set_style_prefix(self.role + "idle_", True)

        super(Button, self).per_interact()

    def event(self, ev, x, y, st):

        # Call self.action.periodic()
        timeout = run_periodic(self.action, st)

        if timeout is not None:
            renpy.game.interface.timeout(timeout)

        # If we have a child, try passing the event to it. (For keyboard
        # events, this only happens if we're focused.)
        if self.is_focused() or not (ev.type == pygame.KEYDOWN or ev.type == pygame.KEYUP):
            rv = super(Button, self).event(ev, x, y, st)
            if rv is not None:
                return rv

        # If not focused, ignore all events.
        if not self.is_focused():
            return None

        # Check the keymap.
        for name, action in self.keymap.iteritems():
            if map_event(ev, name):
                return run(action)

        # Ignore as appropriate:
        if map_event(ev, "button_ignore") and self.clicked:
            raise renpy.display.core.IgnoreEvent()

        # If clicked,
        if map_event(ev, "button_select") and self.clicked:

            self.activated = True
            self.style.set_prefix(self.role + 'activate_')

            if self.style.sound:
                renpy.audio.music.play(self.style.sound, channel="sound")

            rv = run(self.clicked)

            if rv is not None:
                return rv
            else:
                self.activated = False

                if self.is_focused():
                    self.set_style_prefix(self.role + "hover_", True)
                else:
                    self.set_style_prefix(self.role + "idle_", True)

                raise renpy.display.core.IgnoreEvent()

        return None


    def set_style_prefix(self, prefix, root):
        if root:
            super(Button, self).set_style_prefix(prefix, root)


# Reimplementation of the TextButton widget as a Button and a Text
# widget.
def TextButton(text, style='button', text_style='button_text',
               clicked=None, **properties):

    text = renpy.text.text.Text(text, style=text_style) #@UndefinedVariable
    return Button(text, style=style, clicked=clicked, **properties)

class ImageButton(Button):
    """
    Used to implement the guts of an image button.
    """

    def __init__(self,
                 idle_image,
                 hover_image,
                 insensitive_image = None,
                 activate_image = None,
                 selected_idle_image = None,
                 selected_hover_image = None,
                 selected_insensitive_image = None,
                 selected_activate_image = None,
                 style='image_button',
                 clicked=None,
                 hovered=None,
                 **properties):

        insensitive_image = insensitive_image or idle_image
        activate_image = activate_image or hover_image

        selected_idle_image = selected_idle_image or idle_image
        selected_hover_image = selected_hover_image or hover_image
        selected_insensitive_image = selected_insensitive_image or insensitive_image
        selected_activate_image = selected_activate_image or activate_image

        self.state_children = dict(
            idle_ = renpy.easy.displayable(idle_image),
            hover_ = renpy.easy.displayable(hover_image),
            insensitive_ = renpy.easy.displayable(insensitive_image),
            activate_ = renpy.easy.displayable(activate_image),

            selected_idle_ = renpy.easy.displayable(selected_idle_image),
            selected_hover_ = renpy.easy.displayable(selected_hover_image),
            selected_insensitive_ = renpy.easy.displayable(selected_insensitive_image),
            selected_activate_ = renpy.easy.displayable(selected_activate_image),
            )

        super(ImageButton, self).__init__(renpy.display.layout.Null(),
                                          style=style,
                                          clicked=clicked,
                                          hovered=hovered,
                                          **properties)

    def visit(self):
        return self.state_children.values()

    def get_child(self):
        return self.style.child or self.state_children[self.style.prefix]


# This is used for an input that takes its focus from a button.
class HoveredProxy(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self):
        self.a()
        if self.b:
            return self.b()


class Input(renpy.text.text.Text): #@UndefinedVariable
    """
    This is a Displayable that takes text as input.
    """

    changed = None
    prefix = ""
    suffix = ""
    caret_pos = 0

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
                 **properties):

        super(Input, self).__init__("", style=style, replaces=replaces, substitute=False, **properties)

        self.content = unicode(default)
        self.length = length

        self.allow = allow
        self.exclude = exclude
        self.prefix = prefix
        self.suffix = suffix

        self.changed = changed

        self.editable = editable

        caretprops = { 'color' : None }

        for i in properties:
            if i.endswith("color"):
                caretprops[i] = properties[i]

        self.caret = renpy.display.image.Solid(xmaximum=1, style=style, **caretprops)
        self.caret_pos = len(self.content)

        if button:
            self.editable = False
            button.hovered = HoveredProxy(self.enable, button.hovered)
            button.unhovered = HoveredProxy(self.disable, button.unhovered)

        if isinstance(replaces, Input):
            self.content = replaces.content
            self.editable = replaces.editable
            self.caret_pos = replaces.caret_pos

        self.update_text(self.content, self.editable)


    def update_text(self, content, editable):

        if content != self.content or editable != self.editable:
            renpy.display.render.redraw(self, 0)

        if content != self.content:
            self.content = content

            if self.changed:
                self.changed(content)

        if content == "":
            content = u"\u200b"

        self.editable = editable

        # Choose the caret.
        caret = self.style.caret
        if caret is None:
            caret = self.caret

        if editable:
            l = len(content)
            self.set_text([self.prefix, content[0:self.caret_pos].replace("{", "{{"), caret,
                                        content[self.caret_pos:l].replace("{", "{{"), self.suffix])
        else:
            self.set_text([self.prefix, content.replace("{", "{{"), self.suffix ])

    # This is needed to ensure the caret updates properly.
    def set_style_prefix(self, prefix, root):
        if prefix != self.style.prefix:
            self.update_text(self.content, self.editable)

        super(Input, self).set_style_prefix(prefix, root)

    def enable(self):
        self.update_text(self.content, True)

    def disable(self):
        self.update_text(self.content, False)

    def event(self, ev, x, y, st):

        if not self.editable:
            return None

        l = len(self.content)

        if map_event(ev, "input_backspace"):

            if self.content and self.caret_pos > 0:
                content = self.content[0:self.caret_pos-1] + self.content[self.caret_pos:l]
                self.caret_pos -= 1
                self.update_text(content, self.editable)

            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif map_event(ev, "input_enter"):
            if not self.changed:
                return self.content

        elif map_event(ev, "input_left"):
            if self.caret_pos > 0:
                self.caret_pos -= 1
                self.update_text(self.content, self.editable)

            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif map_event(ev, "input_right"):
            if self.caret_pos < l:
                self.caret_pos += 1
                self.update_text(self.content, self.editable)

            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif map_event(ev, "input_delete"):
            if self.caret_pos < l:
                content = self.content[0:self.caret_pos] + self.content[self.caret_pos+1:l]
                self.update_text(content, self.editable)

            renpy.display.render.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        elif ev.type == pygame.KEYDOWN and ev.unicode:
            if ord(ev.unicode[0]) < 32:
                return None

            if self.length and len(self.content) >= self.length:
                raise renpy.display.core.IgnoreEvent()

            if self.allow and ev.unicode not in self.allow:
                raise renpy.display.core.IgnoreEvent()

            if self.exclude and ev.unicode in self.exclude:
                raise renpy.display.core.IgnoreEvent()

            content = self.content[0:self.caret_pos] + ev.unicode + self.content[self.caret_pos:l]
            self.caret_pos += 1

            self.update_text(content, self.editable)

            raise renpy.display.core.IgnoreEvent()

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

    def __init__(self, range=1, value=0, step=None, page=0, changed=None, adjustable=None, ranged=None): #@ReservedAssignment
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

        .. method:: change(value)

            Changes the value of the adjustment to `value`, updating
            any bars and viewports that use the adjustment.
         """


        super(Adjustment, self).__init__()

        if adjustable is None:
            if changed:
                adjustable = True

        self._value = value
        self._range = range
        self._page = page
        self._step = step
        self.changed = changed
        self.adjustable = adjustable
        self.ranged = ranged

    def get_value(self):
        if self._value > self._range:
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

    range = property(get_range, set_range) #@ReservedAssignment

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

class Bar(renpy.display.core.Displayable):
    """
    Implements a bar that can display an integer value, and respond
    to clicks on that value.
    """

    __version__ = 2

    def after_upgrade(self, version):

        if version < 1:
            self.adjustment = Adjustment(self.range, self.value, changed=self.changed) # E1101
            self.adjustment.register(self)
            del self.range # E1101
            del self.value # E1101
            del self.changed # E1101

        if version < 2:
            self.value = None

    def __init__(self,
                 range=None, #@ReservedAssignment
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
                 **properties):

        self.value = None

        if adjustment is None:
            if isinstance(value, renpy.ui.BarValue):

                if isinstance(replaces, Bar):
                    value.replaces(replaces.value)

                self.value = value
                adjustment = value.get_adjustment()
                renpy.game.interface.timeout(0)
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

    def per_interact(self):
        self.focusable = self.adjustment.adjustable
        self.adjustment.register(self)

    def predict_one(self):
        pd = renpy.display.predict.displayable
        style = self.style

        pd(style.insensitive_fore_bar)
        pd(style.idle_fore_bar)
        pd(style.hover_fore_bar)
        pd(style.selected_idle_fore_bar)
        pd(style.selected_hover_fore_bar)

        pd(style.insensitive_aft_bar)
        pd(style.idle_aft_bar)
        pd(style.hover_aft_bar)
        pd(style.selected_idle_aft_bar)
        pd(style.selected_hover_aft_bar)

        pd(style.insensitive_thumb)
        pd(style.idle_thumb)
        pd(style.hover_thumb)
        pd(style.selected_idle_thumb)
        pd(style.selected_hover_thumb)

        pd(style.insensitive_thumb_shadow)
        pd(style.idle_thumb_shadow)
        pd(style.hover_thumb_shadow)
        pd(style.selected_idle_thumb_shadow)
        pd(style.selected_hover_thumb_shadow)

    def render(self, width, height, st, at):

        # Handle redrawing.
        if self.value is not None:
            redraw = self.value.periodic(st)

            if redraw is not None:
                renpy.display.render.redraw(self, redraw)

        # Store the width and height for the event function to use.
        self.width = width
        self.height = height
        range = self.adjustment.range #@ReservedAssignment
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
            thumb_dim = active * page / (range + page)
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
            fore_size = active * value / range
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
                rv.blit(aftsurf, (0, height-aft_size), main=False)
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
                rv.blit(aftsurf, (width-aft_size, 0), main=False)
                rv.blit(thumb, (fore_size - thumb_offset, 0))

            else:
                foresurf = render(self.style.fore_bar, width, height, st, at)
                aftsurf = render(self.style.aft_bar, width, height, st, at)

                rv.blit(thumb_shadow, (fore_size - thumb_offset, 0))
                rv.blit(foresurf.subsurface((0, 0, fore_size, height)), (0, 0), main=False)
                rv.blit(aftsurf.subsurface((width - aft_size, 0, aft_size, height)), (width-aft_size, 0), main=False)
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

        range = self.adjustment.range #@ReservedAssignment
        old_value = self.adjustment.value
        value = old_value

        vertical = self.style.bar_vertical
        invert = self.style.bar_invert ^ vertical
        if invert:
            value = range - value

        grabbed = (renpy.display.focus.get_grab() is self)
        just_grabbed = False

        if not grabbed and map_event(ev, "bar_activate"):
            renpy.display.focus.set_grab(self)
            self.set_style_prefix("selected_hover_", True)
            just_grabbed = True
            grabbed = True

        if grabbed:

            if vertical:
                increase = "bar_down"
                decrease = "bar_up"
            else:
                increase = "bar_right"
                decrease = "bar_left"

            if map_event(ev, decrease):
                value -= self.adjustment.step

            if map_event(ev, increase):
                value += self.adjustment.step

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

            if isinstance(range, int):
                value = int(value)

            if value < 0:
                value = 0

            if value > range:
                value = range

        if invert:
            value = range - value

        if grabbed and not just_grabbed and map_event(ev, "bar_deactivate"):
            self.set_style_prefix("hover_", True)
            renpy.display.focus.set_grab(None)

        if value != old_value:
            return self.adjustment.change(value)

        return None


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


class TimerState(renpy.python.RevertableObject):
    """
    Stores the state of the timer, which may need to be rolled back.
    """

    # Prevents us from having to worry about our initialization being
    # rolled back.
    started = False
    next_event = None

class Timer(renpy.display.layout.Null):

    __version__ = 1

    started = False

    def after_upgrade(self, version):
        if version < 1:
            self.state = TimerState()
            self.state.started = self.started
            self.state.next_event = self.next_event

    def __init__(self, delay, action=None, repeat=False, args=(), kwargs={}, replaces=None, **properties):
        super(Timer, self).__init__(**properties)

        if action is None:
            raise Exception("A timer must have an action supplied.")

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

        if replaces is not None:
            self.state = replaces.state
        else:
            self.state = TimerState()


    def event(self, ev, x, y, st):

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

    def __init__(self, hovered=None, unhovered=None, replaces=None, **properties):
        super(MouseArea, self).__init__(**properties)

        self.hovered = hovered
        self.unhovered = unhovered

        # Are we hovered right now?
        self.is_hovered = False

        if replaces is not None:
            self.is_hovered = replaces.is_hovered

        # Taken from the render.
        self.width = 0
        self.height = 0


    def render(self, width, height, st, at):
        self.width = width
        self.height = height

        return Render(width, height)

    def event(self, ev, x, y, st):

        if 0 <= x < self.width and 0 <= y < self.height:
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
