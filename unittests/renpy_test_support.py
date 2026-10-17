import renpy

_initialized = False


def initialize_renpy():
    global _initialized

    if not _initialized:
        renpy.import_all()
        _initialized = True
