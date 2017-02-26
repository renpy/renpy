# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
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

         Causes control to transfer to the given label. This can be used in
         conjunction with renpy.run_screen to define an imagemap that jumps
         to a label when run.
         """

        def __init__(self, label):
            self.label = label

        def __call__(self):
            renpy.jump(self.label)

    @renpy.pure
    class Show(Action, DictEquality):
        """
         :doc: control_action

         This causes another screen to be shown. `screen` is a string
         giving the name of the screen. The keyword arguments are
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
            return renpy.get_screen(self.screen) is not None

    @renpy.pure
    def ShowTransient(screen, *args, **kwargs):
        """
         :doc: control_action

         Shows a transient screen. A transient screen will be hidden when
         the current interaction completes.
         """

        return Show(screen, _transient=True, *args, **kwargs)

    @renpy.pure
    class Hide(Action, DictEquality):
        """
         :doc: control_action

         This causes the screen named `screen` to be hidden, if it is shown.

         `transition`
             If not None, a transition that occurs when hiding the screen.
         """

        def __init__(self, screen, transition=None):
            self.screen = screen
            self.transition = transition

        def __call__(self):
            renpy.hide_screen(self.screen)

            if self.transition is not None:
                renpy.transition(self.transition)

            renpy.restart_interaction()

