# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

                if current == self.input_value:
                    renpy.set_editable_input_value(self.input_value, False)

            elif self.action == "toggle":

                if current == self.input_value and editable:
                    renpy.set_editable_input_value(self.input_value, False)
                else:
                    renpy.set_editable_input_value(self.input_value, True)

            renpy.restart_interaction()

        def get_selected(self):

            current, editable = renpy.get_editable_input_value()

            rv = (current == self.input_value) and editable

            if self.action == "disable":
                rv = not rv

            return rv

    @renpy.pure
    class DisableAllInputValues(Action):
        """
        :doc: other_action

        Disables all active InputValue. This will re-focus the default
        InputValue, if there is one. Otherwise, no InputValue will be
        focused.
        """

        def __call__(self):
            renpy.set_editable_input_value(None, False)
            renpy.restart_interaction()

    @renpy.pure
    class InputValue(renpy.object.Object):
        """
        Subclassable by creators, documented in Sphinx.
        """

        default = True
        editable = True
        returnable = False

        def get_text(self):
            raise NotImplementedError

        def set_text(self, s):
            raise NotImplementedError

        def enter(self):
            if self.returnable:
                return self.get_text()
            else:
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

    class __GenericInputValue(InputValue, FieldEquality):
        """
        Not subclassable by creators, not documented, meant to factorize
        common features of the documented input value classes.
        """

        equality_fields = ("default", "returnable")

        def __init__(self, default=True, returnable=False):
            self.default = default
            self.returnable = returnable

    class ScreenVariableInputValue(__GenericInputValue):
        """
        :doc: input_value
        :args: {args}

        An input value that updates a variable in a screen.

        In a ``use``\ d screen, this targets a variable in the context of the
        screen containing the ``use``\ d one(s). To target variables within a
        ``use``\ d screen, and only in that case, use
        :func:`LocalVariableInputValue` instead.

        `variable`
            A string giving the name of the variable to update.
        """

        identity_fields = ("screen",)
        equality_fields = __GenericInputValue.equality_fields+("variable",)

        def __init__(self, variable, *args, **kwargs):
            super(ScreenVariableInputValue, self).__init__(*args, **kwargs)
            self.variable = variable
            self.screen = renpy.current_screen()

        def get_text(self):
            cs = self.screen
            return cs.scope[self.variable]

        def set_text(self, s):
            cs = self.screen
            cs.scope[self.variable] = s
            renpy.restart_interaction()

    @renpy.pure
    class FieldInputValue(__GenericInputValue):
        """
        :doc: input_value
        :args: {args}

        An input value that updates `field` on `object`.

        `field`
            A string giving the name of the field.
        """

        identity_fields = ("object",)
        equality_fields = __GenericInputValue.equality_fields+("field",)

        kind = "field"

        def __init__(self, object, field, *args, **kwargs):
            super(FieldInputValue, self).__init__(*args, **kwargs)
            self.object = object
            self.field = field

        def get_text(self):
            return _get_field(self.object, self.field, self.kind)

        def set_text(self, s):
            _set_field(self.object, self.field, s, self.kind)
            renpy.restart_interaction()

    @renpy.pure
    class VariableInputValue(FieldInputValue):
        """
        :doc: input_value
        :args: {args}

        An input value that updates `variable`.

        `variable`
            A string giving the name of the variable to update.

            The `variable` parameter must be a string, and can be a simple name like "strength", or
            one with dots separating the variable from fields, like "hero.strength"
            or "persistent.show_cutscenes".
        """

        __version__ = 1

        kind = "variable"

        def after_upgrade(self, version):
            if version < 1:
                self.field = self.variable
                self.object = store
                del self.variable

        def __init__(self, variable, *args, **kwargs):
            super(VariableInputValue, self).__init__(store, variable, *args, **kwargs)

    @renpy.pure
    class DictInputValue(__GenericInputValue):
        """
        :doc: input_value
        :args: {args}

        An input value that updates ``dict[key]``.

        `dict`
            May be a dict object or a list.
        """

        identity_fields = ("dict",)
        equality_fields = __GenericInputValue.equality_fields+("key",)

        def __init__(self, dict, key, *args, **kwargs):
            super(DictInputValue, self).__init__(*args, **kwargs)
            self.dict = dict
            self.key = key

        def get_text(self):
            return self.dict[self.key]

        def set_text(self, s):
            self.dict[self.key] = s
            renpy.restart_interaction()

    # not pure
    class LocalVariableInputValue(DictInputValue):
        """
        :doc: input_value
        :args: {args}

        An input value that updates a local variable in a ``use``\ d screen.

        To target a variable in a top-level screen, prefer using
        :func:`ScreenVariableInputValue`.

        For more information, see :ref:`sl-use`.

        This must be created in the context that the variable is set in - it
        can't be passed in from somewhere else.

        `variable`
            A string giving the name of the variable to update.
        """

        def __init__(self, variable, *args, **kwargs):
            super(LocalVariableInputValue, self).__init__(sys._getframe(1).f_locals, variable, *args, **kwargs)

        def get_text(self):
            try:
                return super(LocalVariableInputValue, self).get_text()
            except LookupError:
                raise Exception("The {!r} local variable does not exist.".format(self.key)) # from e # PY3 only

init -1510 python hide:
    if config.generating_documentation:
        import inspect
        import itertools

        generic_params = tuple(inspect.signature(__GenericInputValue.__init__).parameters.values())[1:]
        suffix = inspect.cleandoc("""
        `default`
            If true, this input can be editable by default.
        `returnable`
            If true, the value of this input will be returned when the
            user presses enter.
        """)

        for ivalue in (ScreenVariableInputValue, FieldInputValue, VariableInputValue, DictInputValue, LocalVariableInputValue):
            docstr = inspect.cleandoc(ivalue.__doc__)

            params = []
            for param in itertools.islice(inspect.signature(ivalue.__init__).parameters.values(), 1, None):
                if param.kind not in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                    params.append(param)

            params.extend(generic_params)

            ivalue.__doc__ = (docstr+"\n"+suffix).format(
                args=inspect.Signature(parameters=params),
            )
