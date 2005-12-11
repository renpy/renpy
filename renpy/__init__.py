# This file ensures that renpy packages will be imported in the right
# order.

# Some version numbers and things.
version = "Ren'Py 5.2.1"
script_version = 5002001
savegame_suffix = "-5.2.1.save"

def import_all():

    import renpy.game

    # Should probably be early, as we will add it as a base to serialized things.
    import renpy.object 

    # Adds in the Ren'Py loader.
    import renpy.loader

    import renpy.ast
    import renpy.curry
    import renpy.execution
    import renpy.loadsave
    import renpy.parser
    import renpy.python # object
    import renpy.script
    import renpy.style

    import renpy.display
    import renpy.display.presplash
    import renpy.display.module
    import renpy.display.render # Most display stuff depends on this.
    import renpy.display.core # object
    import renpy.display.text # core
    import renpy.display.layout # core
    import renpy.display.behavior # layout
    import renpy.display.transition # core
    import renpy.display.im
    import renpy.display.image # core, behavior, im
    import renpy.display.video
    import renpy.display.focus
    import renpy.display.anim

    # Note: For windows to work, renpy.audio.audio needs to be after
    # renpy.display.module. 
    import renpy.audio.audio
    import renpy.audio.sound
    import renpy.audio.music

    import renpy.ui

    import renpy.lint
    import renpy.warp

    import renpy.exports
    import renpy.config # depends on lots.
    import renpy.store  # depends on everything.
    import renpy.main

    # Import everything into renpy.exports, provided it isn't
    # already there.
    for k, v in globals().iteritems():
        vars(renpy.exports).setdefault(k, v)
