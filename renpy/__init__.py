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

    import renpy.display.accelerator #@UnresolvedImport
    import renpy.display.gldraw #@UnresolvedImport
    import renpy.display.glenviron #@UnresolvedImport
    import renpy.display.glenviron_fixed #@UnresolvedImport
    import renpy.display.glenviron_limited #@UnresolvedImport
    import renpy.display.glenviron_shader #@UnresolvedImport
    import renpy.display.glrtt_copy #@UnresolvedImport
    import renpy.display.glrtt_fbo #@UnresolvedImport
    import renpy.display.glshader #@UnresolvedImport
    import renpy.display.gltexture #@UnresolvedImport
    import renpy.display.render #@UnresolvedImport

    # Prevent a pyflakes warning.
    renpy
    
    
def import_all():
    import renpy.log #@UnresolvedImport
    
    import renpy.display #@UnresolvedImport

    # Should probably be early, as we will add it as a base to serialized things.
    import renpy.object #@UnresolvedImport

    import renpy.game #@UnresolvedImport

    # Adds in the Ren'Py loader.
    import renpy.loader #@UnresolvedImport

    import renpy.ast #@UnresolvedImport
    import renpy.atl #@UnresolvedImport
    import renpy.curry #@UnresolvedImport
    import renpy.easy #@UnresolvedImport
    import renpy.execution #@UnresolvedImport
    import renpy.loadsave #@UnresolvedImport
    import renpy.parser #@UnresolvedImport
    import renpy.python #@UnresolvedImport
    import renpy.remote #@UnresolvedImport
    import renpy.script #@UnresolvedImport
    import renpy.statements #@UnresolvedImport
    import renpy.style #@UnresolvedImport

    import renpy.display.presplash #@UnresolvedImport
    import renpy.display.iliad # Must be before scale and pgrender. @UnresolvedImport
    import renpy.display.pgrender #@UnresolvedImport
    import renpy.display.scale # Must be before module. @UnresolvedImport
    import renpy.display.module #@UnresolvedImport

    # Now that render is pre-compiled, we want to use the
    # location of renpy.display.module to find it.
    import _renpy
    libexec = os.path.dirname(_renpy.__file__)
    renpy.display.__path__.insert(0, os.path.join(libexec, "renpy", "display")) #@UndefinedVariable

    # Also find encodings, to deal with the way py2exe lays things out.
    import encodings
    libexec = os.path.dirname(encodings.__path__[0])
    renpy.display.__path__.insert(1, os.path.join(libexec, "renpy", "display")) #@UndefinedVariable
    
    import renpy.display.render # Most display stuff depends on this. @UnresolvedImport

    import renpy.display.core # object @UnresolvedImport
    import renpy.display.font #@UnresolvedImport
    import renpy.display.text # core, font @UnresolvedImport
    import renpy.display.layout # core @UnresolvedImport
    import renpy.display.motion # layout @UnresolvedImport
    import renpy.display.behavior # layout @UnresolvedImport
    import renpy.display.transition # core, layout @UnresolvedImport
    import renpy.display.im #@UnresolvedImport
    import renpy.display.imagelike #@UnresolvedImport
    import renpy.display.image # core, behavior, im, imagelike @UnresolvedImport
    import renpy.display.video #@UnresolvedImport
    import renpy.display.focus #@UnresolvedImport
    import renpy.display.anim #@UnresolvedImport
    import renpy.display.particle #@UnresolvedImport
    import renpy.display.joystick #@UnresolvedImport
    import renpy.display.minigame #@UnresolvedImport
    import renpy.display.screen #@UnresolvedImport
    import renpy.display.dragdrop #@UnresolvedImport
    import renpy.display.imagemap #@UnresolvedImport
    import renpy.display.predict #@UnresolvedImport
    
    import renpy.display.error #@UnresolvedImport
    
    # Note: For windows to work, renpy.audio.audio needs to be after
    # renpy.display.module. 
    import renpy.audio.audio #@UnresolvedImport
    import renpy.audio.music #@UnresolvedImport
    import renpy.audio.sound #@UnresolvedImport

    import renpy.ui #@UnresolvedImport
    import renpy.screenlang #@UnresolvedImport

    import renpy.lint #@UnresolvedImport
    import renpy.warp #@UnresolvedImport

    import renpy.exports #@UnresolvedImport
    import renpy.character # depends on exports. @UnresolvedImport

    import renpy.config # depends on lots. @UnresolvedImport
    import renpy.store  # depends on everything. @UnresolvedImport
    import renpy.main #@UnresolvedImport

    # Import everything into renpy.exports, provided it isn't
    # already there.
    for k, v in globals().iteritems():
        vars(renpy.exports).setdefault(k, v)

# This reloads all modules.
def reload_all():
    
    import renpy #@UnresolvedImport

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
