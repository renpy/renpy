# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
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

    __FieldNotFound = object()

    def __get_field(obj, name, kind):

        if not name:
            return obj

        rv = obj

        for i in name.split("."):
            rv = getattr(rv, i, __FieldNotFound)
            if rv is __FieldNotFound:
                raise NameError("The {} {} does not exist.".format(kind, name))

        return rv

    def __set_field(obj, name, value, kind):
        fields, _, attr = name.rpartition(".")

        try:
            obj = __get_field(obj, fields, kind)
            setattr(obj, attr, value)
        except:
            raise NameError("The {} {} does not exist.".format(kind, name))

    @renpy.pure
    class SetField(Action, FieldEquality):
        """
         :doc: data_action
         :args: (object, field, value)

         Causes the a field on an object to be set to a given value.
         `object` is the object, `field` is a string giving the name of the
         field to set, and `value` is the value to set it to.
         """

        identity_fields = [ "object" ]
        equality_fields = [ "field", "value" ]

        kind = "field"

        def __init__(self, object, field, value, kind="field"):
            self.object = object
            self.field = field
            self.value = value
            self.kind = kind

        def __call__(self):
            __set_field(self.object, self.field, self.value, self.kind)
            renpy.restart_interaction()

        def get_selected(self):
            return __get_field(self.object, self.field, self.kind) == self.value

    @renpy.pure
    def SetVariable(name, value):
        """
        :doc: data_action

        Causes the variable with `name` to be set to `value`.

        The `name` argument must be a string, and can be a simple name like "strength", or
        one with dots separating the variable from fields, like "hero.strength"
        or "persistent.show_cutscenes".
        """

        return SetField(store, name, value, kind="variable")

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

    # Not pure.
    def SetLocalVariable(name, value):
        """
        :doc: data_action

        Causes the variable `name` to be set to `value` in the current
        local context.

        This function is only useful in a screen that has been use by
        another scene, as it provides a way of setting the value of a
        variable inside the used screen. In all other cases,
        :func:`SetScreenVariable` should be preferred, as it allows more
        of the screen to be cached.

        This must be created in the context that the variable is set
        in - it can't be passed in from somewhere else.
        """

        return SetDict(sys._getframe(1).f_locals, name, value)


    @renpy.pure
    class ToggleField(Action, FieldEquality):
        """
         :doc: data_action
         :args: (object, field, true_value=None, false_value=None)

         Toggles `field` on `object`. Toggling means to invert the boolean
         value of that field when the action is performed.

         `true_value`
             If not None, then this is the true value we use.
         `false_value`
             If not None, then this is the false value we use.
         """

        identity_fields = [ "object"]
        equality_fields = [ "field", "true_value", "false_value"  ]

        kind = "field"

        def __init__(self, object, field, true_value=None, false_value=None, kind="field"):
            self.object = object
            self.field = field
            self.true_value = true_value
            self.false_value = false_value
            self.kind = kind

        def __call__(self):
            value = __get_field(self.object, self.field, self.kind)

            if self.true_value is not None:
                value = (value == self.true_value)

            value = not value

            if self.true_value is not None:
                if value:
                    value = self.true_value
                else:
                    value = self.false_value

            __set_field(self.object, self.field, value, self.kind)
            renpy.restart_interaction()

        def get_selected(self):
            rv = __get_field(self.object, self.field, self.kind)

            if self.true_value is not None:
                rv = (rv == self.true_value)

            return rv


    @renpy.pure
    def ToggleVariable(variable, true_value=None, false_value=None):
        """
        :doc: data_action

        Toggles `variable`.

        The `variable` argument must be a string, and can be a simple name like "strength", or
        one with dots separating the variable from fields, like "hero.strength"
        or "persistent.show_cutscenes".


        `true_value`
            If not None, then this is the true value used.
        `false_value`
            If not None, then this is the false value used.
        """

        return ToggleField(store, variable, true_value=true_value, false_value=false_value, kind="variable")


    @renpy.pure
    class ToggleDict(Action, FieldEquality):
        """
         :doc: data_action

         Toggles the value of `key` in `dict`. Toggling means to invert the
         value when the action is performed.

         `true_value`
             If not None, then this is the true value used.
         `false_value`
             If not None, then this is the false value used.
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

    # Not pure.
    def ToggleLocalVariable(name, true_value=None, false_value=None):
        """
        :doc: data_action

        Toggles the value of `name` in the current local context.

        This function is only useful in a screen that has been use by
        another scene, as it provides a way of setting the value of a
        variable inside the used screen. In all other cases,
        :func:`ToggleScreenVariable` should be preferred, as it allows more
        of the screen to be cached.

        This must be created in the context that the variable is set
        in - it can't be passed in from somewhere else.

        `true_value`
            If not None, then this is the true value used.
        `false_value`
            If not None, then this is the false value used.
        """

        return ToggleDict(sys._getframe(1).f_locals, name, true_value=true_value, false_value=false_value)

    @renpy.pure
    class ToggleScreenVariable(Action, FieldEquality):
        """
         :doc: data_action

         Toggles the value of the variable `name` in the current screen.

         `true_value`
             If not None, then this is the true value used.
         `false_value`
             If not None, then this is the false value used.
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
            The set to add to. This may be a Python set or list, in which
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
            The value to remove.
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
