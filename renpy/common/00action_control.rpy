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

init -1500 python:

    @renpy.pure
    class NullAction(Action, DictEquality):
        """
        :doc: control_action

        Does nothing.

        This can be used to make a button responsive to hover/unhover events,
        without actually doing anything.
        """

        def __call__(self):
            return

    @renpy.pure
    class Return(Action, DictEquality):
        """
         :doc: control_action

         Causes the current interaction to return the supplied value, which
         must not be None. This is often used with menus and imagemaps, to
         select what the return value of the interaction is. If the screen
         was called using the ``call screen`` statement, the return value
         is placed in the `_return` variable.

         When in a menu, this returns from the menu. (The value should be
         None in this case.)
         """

        def __init__(self, value=None):
            self.value = value

        def __call__(self):

            if self.value is None:
                if main_menu:
                    ShowMenu("main_menu")()
                else:
                    return True

            else:
                return self.value

    @renpy.pure
    class Jump(Action, DictEquality):
        """
        :doc: control_action

        Causes control to transfer to `label`.
        """

        def __init__(self, label):
            self.label = label

        def __call__(self):
            renpy.jump(self.label)

    @renpy.pure
    class Call(Action, DictEquality):
        """
        :doc: control_action

        Ends the current statement, and calls `label`. Arguments and
        keyword arguments are passed to :func:`renpy.call`.
        """

        args = tuple()
        kwargs = dict()

        def __init__(self, label, *args, **kwargs):
            self.label = label
            self.args = args
            self.kwargs = kwargs

        def __call__(self):
            renpy.call(self.label, *self.args, **self.kwargs)

    @renpy.pure
    class Show(Action, DictEquality):
        """
         :doc: control_action

         This causes another screen to be shown. `screen` is a string
         giving the name of the screen. The arguments are
         passed to the screen being shown.

         If not None, `transition` is use to show the new screen.
         """


        args = None

        def __init__(self, screen, transition=None, *args, **kwargs):
            self.screen = screen
            self.transition = transition
            self.args = args
            self.kwargs = kwargs

        def predict(self):
            renpy.predict_screen(self.screen, *self.args, **self.kwargs)

        def __call__(self):
            renpy.show_screen(self.screen, *self.args, **self.kwargs)

            if self.transition is not None:
                renpy.transition(self.transition)

            renpy.restart_interaction()

        def get_selected(self):
            return renpy.get_screen(self.screen, self.kwargs.get("_layer", None)) is not None

    @renpy.pure
    class ToggleScreen(Action, DictEquality):
        """
        :doc: control_action

        This toggles the visibility of `screen`. If it is not currently
        shown, the screen is shown with the provided arguments. Otherwise,
        the screen is hidden.

        If not None, `transition` is use to show and hide the screen.
        """

        args = None

        def __init__(self, screen, transition=None, *args, **kwargs):
            self.screen = screen
            self.transition = transition
            self.args = args
            self.kwargs = kwargs

        def predict(self):
            renpy.predict_screen(self.screen, *self.args, **self.kwargs)

        def __call__(self):
            if renpy.get_screen(self.screen, layer=self.kwargs.get("_layer", None)):
                renpy.hide_screen(self.screen, layer=self.kwargs.get("_layer", None))
            else:
                renpy.show_screen(self.screen, *self.args, **self.kwargs)

            if self.transition is not None:
                renpy.transition(self.transition)

            renpy.restart_interaction()

        def get_selected(self):
            return renpy.get_screen(self.screen, self.kwargs.get("_layer", None)) is not None


    @renpy.pure
    def ShowTransient(screen, transition=None, *args, **kwargs):
        """
         :doc: control_action

         Shows a transient screen. A transient screen will be hidden when
         the current interaction completes. The arguments are
         passed to the screen being shown.

         If not None, `transition` is use to show the new screen.
         """

        return Show(screen, transition, _transient=True, *args, **kwargs)

    @renpy.pure
    class Hide(Action, DictEquality):
        """
        :doc: control_action

        This causes the screen named `screen` to be hidden, if it is shown.

        `transition`
            If not None, a transition that occurs when hiding the screen.

        `_layer`
            This is passed as the layer argument to :func:`renpy.hide_screen`.
        """

        _layer = None

        def __init__(self, screen, transition=None, _layer=None):
            self.screen = screen
            self.transition = transition
            self._layer = _layer

        def __call__(self):
            renpy.hide_screen(self.screen, layer=self._layer)

            if self.transition is not None:
                renpy.transition(self.transition)

            renpy.restart_interaction()

