# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
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

import sys
import os

# Version numbers.
try:
    from renpy.vc_version import vc_version; vc_version
except ImportError:
    vc_version = 0

# The tuple giving the version. This needs to be updated when
# we bump the version.
#
# Be sure to change config.version in tutorial/game/options.rpy.
version_tuple = (6, 16, 5, vc_version)

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

    for i in [ "display", "gl", "angle", "text" ]:

        displaypath = os.path.join(libexec, "renpy", i)

        if os.path.exists(displaypath):
            modulefinder.AddPackagePath('renpy.' + i, displaypath)

def import_cython():
    """
    Never called, but necessary to ensure that modulefinder will properly
    grab the various cython modules.
    """

    import renpy.arguments #@UnresolvedImport

    import renpy.display.accelerator #@UnresolvedImport
    import renpy.display.render #@UnresolvedImport

    import renpy.gl.gldraw #@UnresolvedImport
    import renpy.gl.glenviron_fixed #@UnresolvedImport
    import renpy.gl.glenviron_limited #@UnresolvedImport
    import renpy.gl.glenviron_shader #@UnresolvedImport
    import renpy.gl.glrtt_copy #@UnresolvedImport
    import renpy.gl.glrtt_fbo #@UnresolvedImport
    import renpy.gl.gltexture #@UnresolvedImport

    import renpy.angle.gldraw #@UnresolvedImport
    import renpy.angle.glenviron_shader #@UnresolvedImport
    import renpy.angle.glrtt_copy #@UnresolvedImport
    import renpy.angle.glrtt_fbo #@UnresolvedImport
    import renpy.angle.gltexture #@UnresolvedImport


def import_all():

    import renpy.log #@UnresolvedImport

    import renpy.display #@UnresolvedImport

    # Should probably be early, as we will add it as a base to serialized things.
    import renpy.object #@UnresolvedImport

    import renpy.game #@UnresolvedImport
    import renpy.preferences #@UnresolvedImport

    # Adds in the Ren'Py loader.
    import renpy.loader #@UnresolvedImport

    import renpy.ast #@UnresolvedImport
    import renpy.atl #@UnresolvedImport
    import renpy.curry #@UnresolvedImport
    import renpy.easy #@UnresolvedImport
    import renpy.execution #@UnresolvedImport
    import renpy.loadsave #@UnresolvedImport
    import renpy.savelocation  # @UnresolvedImport
    import renpy.persistent #@UnresolvedImport
    import renpy.parser #@UnresolvedImport
    import renpy.python #@UnresolvedImport
    import renpy.script #@UnresolvedImport
    import renpy.statements #@UnresolvedImport
    import renpy.style #@UnresolvedImport
    import renpy.substitutions #@UnresolvedImport
    import renpy.translation #@UnresolvedImport

    import renpy.display.presplash #@UnresolvedImport
    import renpy.display.pgrender #@UnresolvedImport
    import renpy.display.scale #@UnresolvedImport
    import renpy.display.module #@UnresolvedImport

    def update_path(package):
        """
        Update the __path__ of package, to import binary modules from a libexec
        directory.
        """

        name = package.__name__.split(".")

        import _renpy #@UnresolvedImport
        libexec = os.path.dirname(_renpy.__file__)
        package.__path__.append(os.path.join(libexec, *name))

        # Also find encodings, to deal with the way py2exe lays things out.
        import encodings
        libexec = os.path.dirname(encodings.__path__[0])
        package.__path__.append(os.path.join(libexec, *name))

    update_path(renpy.display)

    import renpy.display.render # Most display stuff depends on this. @UnresolvedImport
    import renpy.display.core # object @UnresolvedImport

    import renpy.text #@UnresolvedImport
    update_path(renpy.text)

    import renpy.text.ftfont #@UnresolvedImport
    import renpy.text.font #@UnresolvedImport
    import renpy.text.textsupport #@UnresolvedImport
    import renpy.text.texwrap #@UnresolvedImport
    import renpy.text.text #@UnresolvedImport
    import renpy.text.extras #@UnresolvedImport

    sys.modules['renpy.display.text'] = renpy.text.text

    import renpy.gl #@UnresolvedImport
    update_path(renpy.gl)

    import renpy.angle #@UnresolvedImport
    update_path(renpy.angle)

    import renpy.display.layout # core @UnresolvedImport
    import renpy.display.motion # layout @UnresolvedImport
    import renpy.display.behavior # layout @UnresolvedImport
    import renpy.display.transition # core, layout @UnresolvedImport
    import renpy.display.movetransition # core @UnresolvedImport
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
    import renpy.display.emulator # @UnresolvedImport

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

    import renpy.editor #@UnresolvedImport
    import renpy.exports #@UnresolvedImport
    import renpy.character # depends on exports. @UnresolvedImport

    import renpy.dump #@UnresolvedImport

    import renpy.config # depends on lots. @UnresolvedImport
    import renpy.minstore # depends on lots. @UnresolvedImport
    import renpy.defaultstore  # depends on everything. @UnresolvedImport
    import renpy.main #@UnresolvedImport

    # Create the store.
    renpy.python.create_store("store")

    # Import the contents of renpy.defaultstore into renpy.store, and set
    # up an alias as we do.
    renpy.store = sys.modules['store']
    sys.modules['renpy.store'] = sys.modules['store']

    import subprocess
    sys.modules['renpy.subprocess'] = subprocess

    for k, v in renpy.defaultstore.__dict__.iteritems():
        renpy.store.__dict__.setdefault(k, v)

    # Import everything into renpy.exports, provided it isn't
    # already there.
    for k, v in globals().iteritems():
        vars(renpy.exports).setdefault(k, v)

# Fool the analyzer.
if False:
    import renpy.defaultstore as store

# This reloads all modules.
def reload_all():

    import renpy #@UnresolvedImport

    # Shut down the cache thread.
    renpy.display.im.cache.quit()

    # Shut down the importer.
    renpy.loader.quit_importer()

    blacklist = [ "renpy",
                  "renpy.log",
                  "renpy.bootstrap",
                  "renpy.display",
                  "renpy.display.pgrender",
                  "renpy.display.scale" ]

    for i in sys.modules.keys():
        if i.startswith("renpy") and i not in blacklist:
            del sys.modules[i]

        if i.startswith("store"):
            del sys.modules[i]

    import gc
    gc.collect()

    renpy.display.draw = None

    import_all()

    renpy.loader.init_importer()

# Information about the platform we're running on. We break the platforms
# up into 4 groups - windows-like, mac-like, linux-like, and android-like.
windows = False
macintosh = False
linux = False
android = False

import platform

if platform.win32_ver()[0]:
    windows = True
elif platform.mac_ver()[0]:
    macintosh = True
else:
    linux = True

# The android init code in renpy.py will set linux=False and android=True.
