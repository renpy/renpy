# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init -1500 python:

    class NullAction(Action):
        """
        :doc: control_action

        Does nothing.

        This can be used to make a button responsive to hover/unhover events,
        without actually doing anything.
        """

        def __call__(self):
            return

    class Return(Action):
        """
         :doc: control_action

         Causes the current interaction to return the supplied value. This is
         often used with menus and imagemaps, to select what the return value
         of the interaction is.

         When in a menu, this returns from the menu.
         """

        def __init__(self, value=None):
            self.value = value

        def __call__(self):

            if self.value is None:
                if renpy.context()._main_menu:
                    ShowMenu("main_menu")()
                else:
                    return True

            else:
                return self.value


    class Jump(Action):
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


    class Show(Action):
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
            return renpy.showing(self.screen)


    def ShowTransient(screen, *args, **kwargs):
        """
         :doc: control_action

         Shows a transient screen. A transient screen will be hidden when
         the current interaction completes.
         """

        return Show(screen, _transient=True, *args, **kwargs)


    class Hide(Action):
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

