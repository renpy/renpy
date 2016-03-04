# Copyright 2004-2016 Tom Rothamel <pytom@bishoujo.us>
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

init -1510 python:

    @renpy.pure
    class _InputValueAction(Action, FieldEquality):
        identity_fields = [ "input_value" ]
        equality_fields = [ "action" ]

        def __init__(self, input_value, action):
            self.input_value = input_value
            self.action = action

        def __call__(self):

            current, editable = renpy.get_editable_input_value()

            if self.action == "enable":

                renpy.set_editable_input_value(self.input_value, True)

            elif self.action == "disable":

                if current is self.input_value:
                    renpy.set_editable_input_value(self.input_value, False)

            elif self.action == "toggle":

                if current is self.input_value and editable:
                    renpy.set_editable_input_value(self.input_value, False)
                else:
                    renpy.set_editable_input_value(self.input_value, True)

            renpy.restart_interaction()

        def get_selected(self):

            current, editable = renpy.get_editable_input_value()

            rv = (current is self.input_value) and editable

            if self.action == "disable":
                rv = not rv

            return rv

    @renpy.pure
    class InputValue(renpy.object.Object):

        default = True
        editable = True

        def get_text(self):
            raise Exception("Not implemented.")

        def set_text(self, s):
            raise Exception("Not implemented.")

        def enter(self):
            return None

        def Enable(self):
            if self.editable:
                return _InputValueAction(self, "enable")
            else:
                return None

        def Disable(self):
            if self.editable:
                return _InputValueAction(self, "disable")
            else:
                return None

        def Toggle(self):
            if self.editable:
                return _InputValueAction(self, "toggle")
            else:
                return None

    @renpy.pure
    class VariableInputValue(InputValue, FieldEquality):
        """
        :doc: input_value

        An input value that updates `variable`.

        `variable`
            A string giving the name of the variable to update.

        `default`
            If true, this input can be editable by default.
        """

        identity_fields = [ ]
        equality_fields = [ "variable", "value" ]

        def __init__(self, variable, default=True):
            self.variable = variable
            self.default = default

        def get_text(self):
            return globals()[self.variable]

        def set_text(self, s):
            globals()[self.variable] = s
            renpy.restart_interaction()

    @renpy.pure
    class ScreenVariableInputValue(InputValue, FieldEquality):
        """
        :doc: input_value

        An input value that updates variable.

        `variable`
            A string giving the name of the variable to update.

        `default`
            If true, this input can be editable by default.
        """

        identity_fields = [ ]
        equality_fields = [ "variable", "value" ]

        def __init__(self, variable, default=True):
            self.variable = variable
            self.default = default

        def get_text(self):
            cs = renpy.current_screen()
            return cs.scope[self.variable]

        def set_text(self, s):
            cs = renpy.current_screen()
            cs.scope[self.variable] = s
            renpy.restart_interaction()

    @renpy.pure
    class FieldInputValue(InputValue, FieldEquality):
        """
        :doc: input_value

        An input value that updates `field` on `object`.

        `field`
            A string giving the name of the field.

        `default`
            If true, this input can be editable by default.
        """

        identity_fields = [ "object"]
        equality_fields = [ "field" ]

        def __init__(self, object, field, default=True):
            self.object = object
            self.field = field

            self.default = default

        def get_text(self):
            return getattr(self.object, self.field)

        def set_text(self, s):
            setattr(self.object, self.field, s)
            renpy.restart_interaction()

    @renpy.pure
    class DictInputValue(InputValue, FieldEquality):
        """
        :doc: input_value

        An input value that updates `key` in `dict`.

        `default`
            If true, this input can be editable by default.
        """

        identity_fields = [ "dict", "key" ]
        equality_fields = [ ]

        def __init__(self, dict, key, default=True):
            self.dict = dict
            self.key = key

            self.default = default

        def get_text(self):
            return self.dict[self.key]

        def set_text(self, s):
            self.dict[self.key] = s
            renpy.restart_interaction()
