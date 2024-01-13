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

init -1600 python:

    __Sentinel = object()

    def _get_field(obj, name, kind):

        if not name:
            return obj

        rv = obj

        for i in name.split("."):
            rv = getattr(rv, i, __Sentinel)
            if rv is __Sentinel:
                raise Exception("The {!r} {} does not exist.".format(name, kind))

        return rv

    def _set_field(obj, name, value, kind):
        fields, _, attr = name.rpartition(".")
        obj = _get_field(obj, fields, kind)

        try:
            setattr(obj, attr, value)
        except Exception:
            raise Exception("The {!r} {} cannot be set.".format(name, kind))


init -1600 python hide:

    Accessor = Manager = python_object
    # clarify the role of each class without adding to the mro
    # and without having ancestors placed between RevertableObject and python_object in the mro

    # Accessor mixins : manage how the data is accessed
    # defines a __call__ which gets the value to set from the value_to_set() method
    # defines a current_value() method which returns the current value of the accessed data or raise an exception
    # may define the `kind` class attribute, which is used in error messages
    class Field(Accessor):
        """
        An Accessor mixin class for Actions setting a field on an object.
        """

        identity_fields = ("object",)
        equality_fields = ("field",)
        kind = "field"

        def __init__(self, object, field, *args, **kwargs):
            super(Field, self).__init__(*args, **kwargs)
            self.object = object
            self.field = field

        def __call__(self):
            _set_field(self.object, self.field, self.value_to_set(), self.kind)
            renpy.restart_interaction()

        def current_value(self):
            return _get_field(self.object, self.field, self.kind)

    class Variable(Field):
        """
        An Accessor mixin class for Actions setting a global variable.
        """

        kind = "global variable"

        def __init__(self, name, *args, **kwargs):
            super(Variable, self).__init__(store, name, *args, **kwargs)

    class Dict(Accessor):
        """
        An Accessor mixin class for Actions setting an index on a sequence or a key on a mapping.
        """

        identity_fields = ("dict",)
        equality_fields = ("key",)
        kind = "key or index"

        def __init__(self, dict, key, *args, **kwargs):
            super(Dict, self).__init__(*args, **kwargs)
            self.dict = dict
            self.key = key

        def __call__(self):
            self.dict[self.key] = self.value_to_set()
            renpy.restart_interaction()

        def current_value(self):
            key = self.key
            try:
                return self.dict[self.key]
            except LookupError as e:
                raise Exception("The {!r} {} does not exist.".format(key, self.kind)) # from e # PY3 only

    class ScreenVariable(Accessor):
        """
        An Accessor mixin class for Actions setting a screen variable.
        """

        identity_fields = ()
        equality_fields = ("name",)
        kind = "screen variable"

        def __init__(self, name, *args, **kwargs):
            super(ScreenVariable, self).__init__(*args, **kwargs)
            self.name = name

        def __call__(self):
            cs = renpy.current_screen()

            if cs is None:
                return

            cs.scope[self.name] = self.value_to_set()
            renpy.restart_interaction()

        def current_value(self):
            cs = renpy.current_screen()
            if cs is None:
                raise Exception("No current screen.")

            rv = cs.scope.get(self.name, __Sentinel)
            if rv is __Sentinel:
                raise Exception("The {!r} {} does not exist.".format(self.name, self.kind))

            return rv

    class LocalVariable(Dict):
        """
        An Accessor mixin class for Actions setting a local variable.
        """

        kind = "local variable"

        def __init__(self, name, *args, **kwargs):
            super(LocalVariable, self).__init__(sys._getframe(1).f_locals,
                                                name,
                                                *args, **kwargs)

    # Manager mixins : manage what value gets written
    # defines a value_to_set() method which returns the value to be set
    # may define get_selected and such methods
    # both of these may call the current_value() method
    class Set(Manager):
        """
        A Manager mixin class for Actions setting a single value
        """

        identity_fields = ()
        equality_fields = ("value",)

        def __init__(self, value, *args, **kwargs):
            super(Set, self).__init__(*args, **kwargs)
            self.value = value

        def value_to_set(self):
            return self.value

        def get_selected(self):
            try:
                val = self.current_value()
            except Exception:
                return False

            return val == self.value

    class Toggle(Manager):
        """
        A Manager mixin class for Actions toggling between two values.
        """

        identity_fields = ()
        equality_fields = ("true_value", "false_value")

        def __init__(self, true_value=None, false_value=None, *args, **kwargs):
            super(Toggle, self).__init__(*args, **kwargs)
            self.true_value = true_value
            self.false_value = false_value

        def value_to_set(self):
            value = self.current_value()

            tv = self.true_value
            if tv is not None:
                value = (value == tv)

            value = not value

            if tv is not None:
                if value:
                    return tv
                else:
                    return self.false_value

            return value

        def get_selected(self):
            try:
                val = self.current_value()
            except Exception:
                return False

            tv = self.true_value
            if tv is not None:
                return val == tv

            return bool(val)

    class Cycle(Manager):
        """
        A Manager mixin class for Actions cycling through a list of values.

        Warning : the provided values must not be duplicated, otherwise some values can never be set.
        """

        identity_fields = ()
        equality_fields = ("values", "loop")

        def __init__(self, values, *args, **kwargs):
            if kwargs.pop("reverse", False):
                values = values[::-1]
                # the reversed builtin returns a non-indexable iterator
                # and we only support sequences anyway - iterators are not picklable
            self.loop = kwargs.pop("loop", True)

            super(Cycle, self).__init__(*args, **kwargs)

            self.values = renpy.easy.to_tuple(values)

        def value_to_set(self):
            values = self.values
            value = self.current_value()

            if value in values:
                idx = values.index(value) + 1

                lnv = len(values)
                if self.loop and idx >= lnv:
                    idx -= lnv

            else:
                idx = 0

            return values[idx]

        def get_sensitive(self):
            values = self.values
            if not values:
                return False

            if self.loop:
                return True

            try:
                value = self.current_value()
            except Exception:
                return False

            if value in values:
                idx = values.index(value)+1
                if idx >= len(values):
                    return False

            return True

    class Increment(Manager):
        """
        A Manager mixin class for Actions incrementing a value by a set amount.
        """

        identity_fields = ()
        equality_fields = ("amount",)

        def __init__(self, amount=1, *args, **kwargs):
            super(Increment, self).__init__(*args, **kwargs)
            self.amount = amount

        def value_to_set(self):
            return self.current_value() + self.amount

        def get_sensitive(self):
            try:
                value = self.current_value()
            except Exception:
                return False

            try:
                value + self.amount
            except Exception:
                return False

            return True


    for accessor in (Field, Variable, Dict, ScreenVariable, LocalVariable):
        for manager in (Set, Toggle, Cycle, Increment):
            name = manager.__name__ + accessor.__name__
            doc = ":doc: generated_data_action"

            if config.generating_documentation:
                from inspect import signature, Signature, Parameter

                params = []
                for bas in (accessor, manager):
                    sig = signature(bas.__init__)
                    for k, param in enumerate(sig.parameters.values()):
                        if k and (param.kind not in (param.VAR_POSITIONAL, param.VAR_KEYWORD)):
                            params.append(param)

                if manager is Cycle:
                    params.append(Parameter("reverse", Parameter.KEYWORD_ONLY, default=False))
                    params.append(Parameter("loop", Parameter.KEYWORD_ONLY, default=True))

                doc += "\n:args: " + str(Signature(parameters=params)) + "\n\nSee :ref:`data-actions`."

            clsdict = python_dict(
                identity_fields=manager.identity_fields+accessor.identity_fields,
                equality_fields=manager.equality_fields+accessor.equality_fields,
                __doc__=doc,
            )

            cls = type(name, (accessor, manager, Action, FieldEquality), clsdict)

            if accessor is not LocalVariable:
                renpy.pure(name)
            setattr(store, name, cls)


init -1600 python:

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
