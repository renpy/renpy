# Copyright 2004-2011 Tom Rothamel <pytom@bishoujo.us>
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

import os

# Some version numbers and things.

# ***** ***** ***** ***** ***** ***** **** ***** ***** ***** *****
# Be sure to change script_version in launcher/script_version.rpy, too!
# Be sure to change _renpy.pyx and module.py, if necessary.

try:
    from renpy.vc_version import vc_version; vc_version
except ImportError:
    vc_version = 0

# The tuple giving the version. This needs to be updated when
# we bump the version.
version_tuple = (6, 12, 1, vc_version)

# A verbose string computed from that version.
version = "Ren'Py " + ".".join(str(i) for i in version_tuple)

# Other versions.
script_version = 5003000
savegame_suffix = "-LT1.save"
bytecode_version = 1

# True if this is the first time we've started - even including
# utter restarts.
first_utter_start = True

def setup_modulefinder(modulefinder):
    import _renpy
    libexec = os.path.dirname(_renpy.__file__)
    displaypath = os.path.join(libexec, "renpy", "display")
    modulefinder.AddPackagePath('renpy.display', displaypath)

def import_cython():
    """
    Never called, but necessary to ensure that modulefinder will properly
    grab the various cython modules.
    """

    import renpy.display.accelerator
    import renpy.display.gldraw
    import renpy.display.glenviron
    import renpy.display.glenviron_fixed
    import renpy.display.glenviron_limited
    import renpy.display.glenviron_shader
    import renpy.display.glrtt_copy
    import renpy.display.glrtt_fbo
    import renpy.display.glshader
    import renpy.display.gltexture
    import renpy.display.render

    # Prevent a pyflakes warning.
    renpy
    
    
def import_all():

    # Should probably be early, as we will add it as a base to serialized things.
    import renpy.object 

    import renpy.game

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

    # Now that render is pre-compiled, we want to use the
    # location of renpy.display.module to find it.
    import _renpy
    libexec = os.path.dirname(_renpy.__file__)
    renpy.display.__path__.insert(0, os.path.join(libexec, "renpy", "display"))

    # Also find encodings, to deal with the way py2exe lays things out.
    import encodings
    libexec = os.path.dirname(encodings.__path__[0])
    renpy.display.__path__.insert(1, os.path.join(libexec, "renpy", "display"))
    
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
    import renpy.display.screen
    import renpy.display.dragdrop
    import renpy.display.imagemap
    import renpy.display.predict
    
    import renpy.display.error
    
    # Note: For windows to work, renpy.audio.audio needs to be after
    # renpy.display.module. 
    import renpy.audio.audio
    import renpy.audio.music
    import renpy.audio.sound

    import renpy.ui
    import renpy.screenlang

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
    renpy.log.info("Reloading.")
    
    # Shut down the cache thread.
    renpy.display.im.cache.quit()
        
    # Cleans out the RenpyImporter.
    import sys
    sys.meta_path.pop()

    blacklist = [ "renpy",
                  "renpy.log",
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

    renpy.display.draw = None
    
    import_all()

