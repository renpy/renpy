# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
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

# This file ensures that renpy packages will be imported in the right
# order.

# Some version numbers and things.

# ***** ***** ***** ***** ***** ***** **** ***** ***** ***** *****
# Be sure to change script_version in launcher/script_version.rpy, too!
# Also check to see if we have to update renpy.py.
version = "Ren'Py 6.10.2e"
script_version = 5003000
savegame_suffix = "-LT1.save"

def import_all():

    import renpy.game

    # Should probably be early, as we will add it as a base to serialized things.
    import renpy.object 

    # Adds in the Ren'Py loader.
    import renpy.loader

    import renpy.ast
    import renpy.atl
    import renpy.curry
    import renpy.easy
    import renpy.execution
    import renpy.loadsave
    import renpy.parser
    import renpy.python # object
    import renpy.remote
    import renpy.script
    import renpy.statements
    import renpy.style

    import renpy.display
    import renpy.display.presplash
    import renpy.display.iliad # Must be before scale and pgrender.
    import renpy.display.pgrender
    import renpy.display.scale # Must be before module.
    import renpy.display.module
    import renpy.display.render # Most display stuff depends on this.
    import renpy.display.core # object
    import renpy.display.font
    import renpy.display.text # core, font
    import renpy.display.layout # core
    import renpy.display.motion # layout
    import renpy.display.behavior # layout
    import renpy.display.transition # core, layout
    import renpy.display.im
    import renpy.display.image # core, behavior, im
    import renpy.display.video
    import renpy.display.focus
    import renpy.display.anim
    import renpy.display.particle
    import renpy.display.joystick
    import renpy.display.minigame
    import renpy.display.error
    
    # Note: For windows to work, renpy.audio.audio needs to be after
    # renpy.display.module. 
    import renpy.audio.audio
    import renpy.audio.music
    import renpy.audio.sound

    import renpy.ui

    import renpy.lint
    import renpy.warp

    import renpy.exports
    import renpy.character # depends on exports.

    import renpy.config # depends on lots.
    import renpy.store  # depends on everything.
    import renpy.main

    # Import everything into renpy.exports, provided it isn't
    # already there.
    for k, v in globals().iteritems():
        vars(renpy.exports).setdefault(k, v)

# This reloads all modules.
def reload_all():
    
    import renpy
    
    # Shut down the cache thread.
    renpy.display.im.cache.quit()
        
    # Cleans out the RenpyImporter.
    import sys
    sys.meta_path.pop()

    blacklist = [ "renpy",
                  "renpy.bootstrap",
                  "renpy.display",
                  "renpy.display.iliad",
                  "renpy.display.pgrender",
                  "renpy.display.scale" ]
    
    for i in sys.modules.keys():
        if i.startswith("renpy") and i not in blacklist:
            del sys.modules[i]

    import gc
    gc.collect()

    import_all()

