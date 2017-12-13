python early hide:

    class _ObjectNamespace(object):
        def __init__(self, nso, name):
            self.nso = nso
            self.name = name

        def set(self, name, value):
            setattr(self.nso, name, value)

        def set_default(self, name, value):
            raise Exception("The default statement can not be used with the {} namespace.".format(self.name))

    class _PersistentNamespace(object):
        def set(self, name, value):
            if getattr(persistent, name) is None:
                setattr(persistent, name, value)

        def set_default(self, name, value):
            if getattr(persistent, name) is None:
                setattr(persistent, name, value)

    class _PreferencesNamespace(object):

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
            if hasattr(config, default_field):
                setattr(config, default_field, value)

    class _GuiNamespace(object):
        def set(self, name, value):
            setattr(gui, name, value)

        def set_default(self, name, value):
            setattr(gui, name, value)


    config.special_namespaces["store.config"] = _ObjectNamespace(config, "config")
    config.special_namespaces["store.persistent"] = _PersistentNamespace()
    config.special_namespaces["store.preferences"] =  _PreferencesNamespace()
    config.special_namespaces["store.gui"] = _GuiNamespace()

