# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

init -1600 python:

   ##########################################################################
    # Functions that set variables or fields.

    @renpy.pure
    class SetField(Action, FieldEquality):
        """
         :doc: data_action

         Causes the a field on an object to be set to a given value.
         `object` is the object, `field` is a string giving the name of the
         field to set, and `value` is the value to set it to.
         """

        identity_fields = [ "object" ]
        equality_fields = [ "field", "value" ]

        def __init__(self, object, field, value):
            self.object = object
            self.field = field
            self.value = value

        def __call__(self):
            setattr(self.object, self.field, self.value)
            renpy.restart_interaction()

        def get_selected(self):
            return getattr(self.object, self.field) == self.value

    @renpy.pure
    def SetVariable(variable, value):
        """
         :doc: data_action

         Causes `variable` to be set to `value`.
         """

        return SetField(store, variable, value)

    @renpy.pure
    class SetDict(Action, FieldEquality):
        """
         :doc: data_action

         Causes the value of `key` in `dict` to be set to `value`.
         """

        identity_fields = [ "dict" ]
        equality_fields = [ "key", "value" ]

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


    @renpy.pure
    class SetScreenVariable(Action, FieldEquality):
        """
        :doc: data_action

        Causes the variable `name` associated with the current screen to
        be set to `value`.
        """

        identity_fields = [ "value" ]
        equality_fields = [ "name" ]

        def __init__(self, name, value):
            self.name = name
            self.value = value

        def __call__(self):

            cs = renpy.current_screen()

            if cs is None:
                return

            cs.scope[self.name] = self.value
            renpy.restart_interaction()

        def get_selected(self):

            cs = renpy.current_screen()

            if cs is None:
                return False

            if self.name not in cs.scope:
                return False

            return cs.scope[self.name] == self.value


    @renpy.pure
    class ToggleField(Action, FieldEquality):
        """
         :doc: data_action

         Toggles `field` on `object`. Toggling means to invert the boolean
         value of that field when the action is performed.

         `true_value`
             If not None, then this is the true value we use.
         `false_value`
             If not None, then this is the false value we use.
         """

        identity_fields = [ "object"]
        equality_fields = [ "field", "true_value", "false_value"  ]

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


    @renpy.pure
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


    @renpy.pure
    class ToggleDict(Action, FieldEquality):
        """
         :doc: data_action

         Toggles the value of `key` in `dict`. Toggling means to invert the
         value when the action is performed.

         `true_value`
             If not None, then this is the true value we use.
         `false_value`
             If not None, then this is the false value we use.
         """

        identity_fields = [ "dict", ]
        equality_fields = [ "key", "true_value", "false_value" ]

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
            if self.key not in self.dict:
                return False

            rv = self.dict[self.key]

            if self.true_value is not None:
                rv = (rv == self.true_value)

            return rv


    @renpy.pure
    class ToggleScreenVariable(Action, FieldEquality):
        """
         :doc: data_action

         Toggles the value of the variable `name` in the current screen.

         `true_value`
             If not None, then this is the true value we use.
         `false_value`
             If not None, then this is the false value we use.
         """

        equality_fields = [ "name", "true_value", "false_value" ]

        def __init__(self, name, true_value=None, false_value=None):
            self.name = name
            self.true_value = true_value
            self.false_value = false_value

        def __call__(self):
            cs = renpy.current_screen()

            if cs is None:
                return

            value = cs.scope[self.name]

            if self.true_value is not None:
                value = (value == self.true_value)

            value = not value

            if self.true_value is not None:
                if value:
                    value = self.true_value
                else:
                    value = self.false_value

            cs.scope[self.name] = value
            renpy.restart_interaction()

        def get_selected(self):
            cs = renpy.current_screen()

            if cs is None:
                return False

            if self.name not in cs.scope:
                return False

            rv = cs.scope[self.name]

            if self.true_value is not None:
                rv = (rv == self.true_value)


            return rv

    @renpy.pure
    class AddToSet(Action, FieldEquality):
        """
        :doc: data_action

        Adds `value` to `set`.

        `set`
            The set to add to. This may be a python set or list, in which
            case the value is appended to the list.
        `value`
            The value to add or append.
        """

        identity_fields = [ 'set' ]
        equality_fields = [ 'value' ]

        def __init__(self, set, value):
            self.set = set
            self.value = value

        def get_sensitive(self):
            return self.value not in self.set

        def __call__(self):
            if isinstance(self.set, list):
                self.set.append(self.value)
            else:
                self.set.add(self.value)

            renpy.restart_interaction()

    @renpy.pure
    class RemoveFromSet(Action, FieldEquality):
        """
        :doc: data_action

        Removes `value` from `set`.

        `set`
            The set to remove from. This may be a set or list.
        `value`
            The value to add or append.
        """

        identity_fields = [ 'set' ]
        equality_fields = [ 'value' ]

        def __init__(self, set, value):
            self.set = set
            self.value = value

        def get_sensitive(self):
            return self.value in self.set

        def __call__(self):
            if self.value in self.set:
                self.set.remove(self.value)

            renpy.restart_interaction()

    @renpy.pure
    class ToggleSetMembership(Action, FieldEquality):
        """
        :doc: data_action

        Toggles the membership of `value` in `set`. If the value is not
        in the set, it's added. Otherwise, it is removed.

        Buttons with this action are marked as selected if and only if the
        value is in the set.

        `set`
            The set to add to or remove from. This may be a set or list. In the
            case of a list, new items are appended.
        `value`
            The value to add or append.
        """

        identity_fields = [ 'set' ]
        equality_fields = [ 'value' ]

        def __init__(self, set, value):
            self.set = set
            self.value = value

        def get_selected(self):
            return self.value in self.set

        def __call__(self):
            if self.value in self.set:
                self.set.remove(self.value)
            else:
                if isinstance(self.set, list):
                    self.set.append(self.value)
                else:
                    self.set.add(self.value)

            renpy.restart_interaction()
