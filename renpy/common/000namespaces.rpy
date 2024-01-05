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

python early hide:

    class _ObjectNamespace(object):
        pure = True
        allow_child_namespaces = False
        repeat_at_default_time = False

        def __init__(self, nso, name):
            self.nso = nso
            self.name = name

        def set(self, name, value):
            setattr(self.nso, name, value)

        def set_default(self, name, value):
            raise Exception("The default statement can not be used with the {} namespace.".format(self.name))

        def get(self, name):
            return getattr(self.nso, name)

    class _PersistentNamespace(object):
        pure = False
        allow_child_namespaces = False
        repeat_at_default_time = True

        def set(self, name, value):
            if getattr(persistent, name) is None:
                setattr(persistent, name, value)

        def set_default(self, name, value):
            if getattr(persistent, name) is None:
                setattr(persistent, name, value)

        def get(self, name):
            if config.developer:
                raise Exception("Using define with the persistent namespace is obsolete - use `default.persistent = ...` instead. Updating persistent variables with define is not supported.")

            return getattr(persistent, name)

    class _ErrorNamespace(object):
        pure = False
        allow_child_namespaces = False
        repeat_at_default_time = False

        def __init__(self, name):
            self.name = name

        def set(self, name, value):
            raise Exception("The define statement can not be used with the {} namespace.".format(self.name))

        def set_default(self, name, value):
            raise Exception("The default statement can not be used with the {} namespace.".format(self.name))

        def get(self, name):
            raise Exception("The default and define statements can not be used with the {} namespace.".format(self.name))

    class _PreferencesNamespace(object):
        pure = False
        allow_child_namespaces = False
        repeat_at_default_time = True

        def set(self, name, value):
            raise Exception("The define statement can not be used with the preferences namespace.")

        def set_default(self, name, value):

            undefined = object()

            if not isinstance(persistent._preference_default, dict):
                persistent._preference_default = { }

            old_default = persistent._preference_default.get(name, undefined)

            if old_default != value:
                setattr(_preferences, name, value)
                persistent._preference_default[name] = value

            default_field = "default_" + name

            # This ensures we don't conflict with the old way of doing
            # things.
            try:
                has_default_field = hasattr(config, default_field)
            except Exception:
                has_default_field = False

            if has_default_field:
                setattr(config, default_field, value)

        def get(self, name):
            raise Exception("The define statement can not be used with the preferences namespace.")

    class _GuiNamespace(object):
        pure = True
        allow_child_namespaces = True
        repeat_at_default_time = False

        def set(self, name, value):
            setattr(gui, name, value)

        def set_default(self, name, value):
            setattr(gui, name, value)

        def get(self, name):
            return getattr(gui, name)

    config.special_namespaces["store.config"] = _ObjectNamespace(config, "config")
    config.special_namespaces["store.persistent"] = _PersistentNamespace()
    config.special_namespaces["store.preferences"] =  _PreferencesNamespace()
    config.special_namespaces["store.gui"] = _GuiNamespace()
    config.special_namespaces["store.renpy"] = _ErrorNamespace("renpy")
