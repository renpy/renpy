﻿# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

init -1500 python:

    @renpy.pure
    class InvertSelected(Action, DictEquality):
        """
         :doc: other_action

         This inverts the selection state of the provided action, while
         proxying over all of the other methods.
         """

        def __init__(self, action):
            self.action = action

        def __call__(self):
            return self.action.__call__()

        def get_selected(self):
            return not self.action.get_selected()

        def get_sensitive(self):
            return self.action.get_sensitive()

        def periodic(self, st):
            return self.action.periodic(st)

        def predict(self):
            self.action.predict()

    @renpy.pure
    def If(expression, true=None, false=None):
        """
         :doc: other_action

         This returns `true` if `expression` is true, and `false`
         otherwise. Use this to select an action based on an expression.
         Note that the default, None, can be used as an action that causes
         a button to be disabled.
         """

        if expression:
            return true
        else:
            return false

    @renpy.pure
    class SelectedIf(Action, DictEquality):
        """
        :doc: other_action

        This allows an expression to control if a button should be marked
        as selected. It should be used as part of a list with one or more
        actions. For example::

            # The button is selected if mars_flag is True
            textbutton "Marsopolis":
                action [ Jump("mars"), SelectedIf(mars_flag) ]
        """

        def __init__(self, expression):
            self.expression = expression

        def __call__(self):
            return None

        def get_selected(self):
            return self.expression

    @renpy.pure
    class SensitiveIf(Action, DictEquality):
        """
        :doc: other_action

        This allows an expression to control if a button should be marked
        as sensitive. It should be used as part of a list with one or more
        actions. For example::

            # The button is sensitive if mars_flag is True
            textbutton "Marsopolis":
                action [ Jump("mars"), SensitiveIf(mars_flag) ]
        """

        def __init__(self, expression):
            self.expression = expression

        def __call__(self):
            return None

        def get_sensitive(self):
            return self.expression

    @renpy.pure
    class Screenshot(Action, DictEquality):
        """
         :doc: other_action

         Takes a screenshot.
         """

        def __call__(self):
            _screenshot()

    @renpy.pure
    class HideInterface(Action, DictEquality):
        """
         :doc: other_action

         Causes the interface to be hidden until the user clicks.
         """

        def __call__(self):
            renpy.call_in_new_context("_hide_windows")


    @renpy.pure
    class OpenURL(Action, DictEquality):
        """
        :doc: other_action

        Causes `url` to be opened in a web browser.
        """

        def __init__(self, url):
            self.url = url

        def __call__(self):
            try:
                import webbrowser
                webbrowser.open_new(self.url)
            except:
                pass

    class With(Action, DictEquality):
        """
         :doc: other_action

         Causes `transition` to occur.
         """

        def __init__(self, transition):
            self.transition = transition

        def __call__(self):
            renpy.transition(self.transition)
            renpy.restart_interaction()

    @renpy.pure
    class Notify(Action, DictEquality):
        """
         :doc: other_action

         Displays `message` using :func:`renpy.notify`.
         """

        def __init__(self, message):
            self.message = message

        def predict(self):
            renpy.predict_screen("notify")

        def __call__(self):
            renpy.notify(self.message)

    @renpy.pure
    class Rollback(Action, DictEquality):
        """
        :doc: other_action

        This action causes a rollback to occur, when a rollback is possible.
        Otherwise, nothing happens.
        """

        def __call__(self):
            renpy.rollback()

        def get_sensitive(self):
            return renpy.can_rollback()

    @renpy.pure
    class RollForward(Action, DictEquality):
        """
        :doc: other_action

        This action causes a rollforward to occur, if a roll forward is
        possible. Otherwise, it is insensitive.
        """

        def __call__(self):
            return renpy.exports.roll_forward_core()

        def get_sensitive(self):
            return renpy.roll_forward_info() is not None


    #########################################################################

    class __TooltipAction(Action, FieldEquality):

        identity_fields = [ "tooltip", "value" ]

        def __init__(self, tooltip, value):
            self.tooltip = tooltip
            self.value = value

        def __call__(self):
            if self.tooltip.value != self.value:
                self.tooltip.value = self.value
                renpy.restart_interaction()

        def unhovered(self):
            if self.tooltip.value != self.tooltip.default:
                self.tooltip.value = self.tooltip.default
                renpy.restart_interaction()

    _m1_00screen__TooltipAction = __TooltipAction

    class Tooltip(object):
        """
        :doc: tooltips class

        A tooltip object can be used to define a portion of a screen that is
        updated when the mouse hovers an area.

        A tooltip object has a ``value`` field, which is set to the `default`
        value passed to the constructor when the tooltip is created. When
        a button using an action created by the tooltip is hovered, the
        value field changes to the value associated with the action.
        """

        def __init__(self, default):
            self.value = default
            self.default = default

        def Action(self, value):
            """
            :doc: tooltips method
            :name: Action

            Returns an action that is generally used as the hovered property
            of a button. When the button is hovered, the value field of this
            tooltip is set to `value`. When the buttton loses focus, the
            value field of this tooltip reverts to the default.
            """

            return __TooltipAction(self, value)

        action = Action


    #########################################################################

    @renpy.pure
    class Language(Action, DictEquality):
        """
        :doc: language_action

        Changes the language of the game to `language`.

        `language`
            A string giving the language to translate to, or None to use
            the default language of the game script.
        """

        alt = "Language [text]"

        def __init__(self, language):
            self.language = language

        def __call__(self):
            renpy.change_language(self.language)

        def get_selected(self):
            return _preferences.language == self.language

        def get_sensitive(self):
            if self.language is None:
                return True

            return self.language in renpy.known_languages()


    #########################################################################

    # Transitions used when entering and leaving replays.
    config.enter_replay_transition = None
    config.exit_replay_transition = None

    @renpy.pure
    class Replay(Action, DictEquality):
        """
        :doc: replay

        An action that starts `label` as a replay.

        `scope`
            A dictionary mapping variable name to value. These variables are set
            when entering the replay.

        `locked`
            If true, this replay is locked. If false, it is unlocked. If None, the
            replay is locked if the label has not been seen in any playthrough.
        """

        def __init__(self, label, scope={}, locked=None):
            self.label = label
            self.scope = scope
            self.locked = locked

        def __call__(self):

            if self.locked:
                return

            if config.enter_replay_transition:
                renpy.transition(config.enter_replay_transition)

            renpy.call_replay(self.label, self.scope)

            if config.exit_replay_transition:
                renpy.transition(config.exit_replay_transition)

        def get_sensitive(self):
            if self.locked is not None:
                return not self.locked

            return renpy.seen_label(self.label)

    @renpy.pure
    class EndReplay(Action, DictEquality):
        """
        :doc: replay

        An action that ends the current memory.
        """

        def __call__(self):
            renpy.end_replay()

        def get_sensitive(self):
            return _in_replay

    @renpy.pure
    class MouseMove(Action, DictEquality):
        """
        :doc: other_action

        Move the mouse pointer to `x`, `y`. If the device does not have a mouse
        pointer or _preferences.mouse_move is False, this does nothing.

        `duration`
            The time it will take to perform the move, in seconds. During
            this time, the mouse may be unresponsive.
        """
        def __init__(self, x, y, duration=0):
            self.x = x
            self.y = y
            self.duration = duration

        def __call__(self):
            if _preferences.mouse_move:
                renpy.set_mouse_pos(self.x, self.y, self.duration)

    class Function(Action, DictEquality):
        """
        :doc: other_action

        This Action calls `callable` with `args` and `kwargs`.

        `callable`
            Callable object.
        `args`
            position arguments to be passed to `callable`.
        `kwargs`
            keyword arguments to be passed to `callable`.
        """
        def __init__(self, callable, *args, **kwargs):
            self.callable = callable
            self.args = args
            self.kwargs = kwargs

        def __call__(self):
            self.callable(*self.args, **self.kwargs)


transform _notify_transform:
    # These control the position.
    xalign .02 yalign .015

    # These control the actions on show and hide.
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0

screen notify:
    zorder 100

    text message at _notify_transform

    # This controls how long it takes between when the screen is
    # first shown, and when it begins hiding.
    timer 3.25 action Hide('notify')
