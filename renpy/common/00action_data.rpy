# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init -1600 python:

   ##########################################################################
    # Functions that set variables or fields.

    class SetField(Action):
        """
         :doc: data_action

         Causes the a field on an object to be set to a given value.
         `object` is the object, `field` is a string giving the name of the
         field to set, and `value` is the value to set it to.
         """

        def __init__(self, object, field, value):
            self.object = object
            self.field = field
            self.value = value

        def __call__(self):
            setattr(self.object, self.field, self.value)
            renpy.restart_interaction()

        def get_selected(self):
            return getattr(self.object, self.field) == self.value


    def SetVariable(variable, value):
        """
         :doc: data_action

         Causes `variable` to be set to `value`.
         """

        return SetField(store, variable, value)


    class SetDict(Action):
        """
         :doc: data_action

         Causes the value of `key` in `dict` to be set to `value`.
         """

        def __init__(self, dict, key, value):
            self.dict = dict
            self.key = key
            self.value = value

        def __call__(self):
            self.dict[self.key] = self.value
            renpy.restart_interaction()

        def get_selected(self):
            if self.key not in self.dict:
                return False

            return self.dict[self.key] == self.value

    def SetScreenVariable(name, value):
        """
        :doc: data_action

        Causes the variable `name` associated with the current screen to
        be set to `value`.
        """

        cs = renpy.current_screen()
        if cs is not None:
            return SetDict(cs.scope, name, value)
        else:
            return None

    class ToggleField(Action):
        """
         :doc: data_action

         Toggles `field` on `object`. Toggling means to invert the boolean
         value of that field when the action is performed.

         `true_value`
             If not None, then this is the true value we use.
         `false_value`
             If not None, then this is the false value we use.
         """

        def __init__(self, object, field, true_value=None, false_value=None):
            self.object = object
            self.field = field
            self.true_value = true_value
            self.false_value = false_value

        def __call__(self):
            value = getattr(self.object, self.field)

            if self.true_value is not None:
                value = (value == self.true_value)

            value = not value

            if self.true_value is not None:
                if value:
                    value = self.true_value
                else:
                    value = self.false_value

            setattr(self.object, self.field, value)
            renpy.restart_interaction()

        def get_selected(self):
            rv = getattr(self.object, self.field)

            if self.true_value is not None:
                rv = (rv == self.true_value)

            return rv


    def ToggleVariable(variable, true_value=None, false_value=None):
        """
         :doc: data_action

         Toggles `variable`.

         `true_value`
             If not None, then this is the true value we use.
         `false_value`
             If not None, then this is the false value we use.
         """

        return ToggleField(store, variable, true_value=true_value, false_value=false_value)


    class ToggleDict(Action):
        """
         :doc: data_action

         Toggles the value of `key` in `dict`. Toggling means to invert the
         value when the action is performed.

         `true_value`
             If not None, then this is the true value we use.
         `false_value`
             If not None, then this is the false value we use.
         """

        def __init__(self, dict, key, true_value=None, false_value=None):
            self.dict = dict
            self.key = key
            self.true_value = true_value
            self.false_value = false_value

        def __call__(self):
            value = self.dict[self.key]

            if self.true_value is not None:
                value = (value == self.true_value)

            value = not value

            if self.true_value is not None:
                if value:
                    value = self.true_value
                else:
                    value = self.false_value

            self.dict[self.key] = value
            renpy.restart_interaction()

        def get_selected(self):
            rv = self.dict[self.key]

            if self.true_value is not None:
                rv = (rv == self.true_value)

            return rv

    def ToggleScreenVariable(name, true_value=None, false_value=None):
        """
         :doc: data_action

         Toggles the value of the variable `name` in the current screen.

         `true_value`
             If not None, then this is the true value we use.
         `false_value`
             If not None, then this is the false value we use.
         """

        cs = renpy.current_screen()

        if cs is not None:
            return ToggleDict(cs.scope, name, true_value=true_value, false_value=None)
        else:
            return None

