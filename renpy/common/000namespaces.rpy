python early hide:

    class _ObjectNamespace(object):
        def __init__(self, nso):
            self.nso = nso

        def set(self, name, value):
            setattr(self.nso, name, value)

    class _PersistentNamespace(object):
        def set(self, name, value):
            if getattr(persistent, name) is None:
                setattr(persistent, name, value)


    config.special_namespaces["store.config"] = _ObjectNamespace(config)
    config.special_namespaces["store.persistent"] = _PersistentNamespace()

