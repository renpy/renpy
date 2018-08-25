# Copyright 2004-2018 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import print_function
import sys
import os
import copy
import types
import threading
import cPickle

################################################################################
# Version information
################################################################################

# Version numbers.
try:
    from renpy.vc_version import vc_version; vc_version
except ImportError:
    vc_version = 0

# The tuple giving the version number.
version_tuple = (7, 1, 0, vc_version)

# The name of this version.
version_name = "On the road again."

# A string giving the version number only (7.0.1.123).
version_only = ".".join(str(i) for i in version_tuple)

# A verbose string giving the version.
version = "Ren'Py " + version_only

# Other versions.
script_version = 5003000
savegame_suffix = "-LT1.save"
bytecode_version = 1


################################################################################
# Platform Information
################################################################################

# Information about the platform we're running on. We break the platforms
# up into 5 groups - windows-like, mac-like, linux-like, android-like,
# and ios-like.
windows = False
macintosh = False
linux = False
android = False
ios = False

# Should we enable experimental features and debugging?
experimental = "RENPY_EXPERIMENTAL" in os.environ

import platform


def get_windows_version():
    """
    When called on windows, returns the windows version.
    """

    import ctypes

    class OSVERSIONINFOEXW(ctypes.Structure):
        _fields_ = [('dwOSVersionInfoSize', ctypes.c_ulong),
                    ('dwMajorVersion', ctypes.c_ulong),
                    ('dwMinorVersion', ctypes.c_ulong),
                    ('dwBuildNumber', ctypes.c_ulong),
                    ('dwPlatformId', ctypes.c_ulong),
                    ('szCSDVersion', ctypes.c_wchar*128),
                    ('wServicePackMajor', ctypes.c_ushort),
                    ('wServicePackMinor', ctypes.c_ushort),
                    ('wSuiteMask', ctypes.c_ushort),
                    ('wProductType', ctypes.c_byte),
                    ('wReserved', ctypes.c_byte)]

    try:

        os_version = OSVERSIONINFOEXW()
        os_version.dwOSVersionInfoSize = ctypes.sizeof(os_version)
        retcode = ctypes.windll.Ntdll.RtlGetVersion(ctypes.byref(os_version))

        # Om failure, assume we have a newer version of windows
        if retcode != 0:
            return (10, 0)

        return (os_version.dwMajorVersion, os_version.dwMinorVersion)

    except:
        return (10, 0)


if platform.win32_ver()[0]:
    windows = get_windows_version()
elif "RENPY_IOS" in os.environ:
    ios = True
elif platform.mac_ver()[0]:
    macintosh = True
elif "ANDROID_PRIVATE" in os.environ:
    android = True
else:
    linux = True

# A flag that's true if we're on a smartphone or tablet-like platform.
mobile = android or ios

# A flag that's set to true if the game directory is bundled inside a mac app.
macapp = False


################################################################################
# Backup Data for Reload
################################################################################

# True if we're done with safe mode checks.
safe_mode_checked = False

# True if autoreload mode is enabled. This has to live here, because it
# needs to survive through an utter restart.
autoreload = False


# A dict that persists through utter restarts. Accessible to all code as
# renpy.session.
session = { }

# A list of modules beginning with "renpy" that we don't want
# to backup.
backup_blacklist = {
    "renpy",
    "renpy.object",
    "renpy.log",
    "renpy.bootstrap",
    "renpy.debug",
    "renpy.display",
    "renpy.display.pgrender",
    "renpy.display.scale",
    "renpy.display.presplash",
    "renpy.display.test",
    "renpy.text.ftfont",
    "renpy.test",
    "renpy.test.testast",
    "renpy.test.testexecution",
    "renpy.test.testkey",
    "renpy.test.testmouse",
    "renpy.test.testparser",
    "renpycoverage",
    }

type_blacklist = (
    types.ModuleType,
    )

name_blacklist = {
    "renpy.loadsave.autosave_not_running",
    "renpy.python.unicode_re",
    "renpy.python.string_re",
    "renpy.python.store_dicts",
    "renpy.python.store_modules",
    "renpy.text.text.VERT_FORWARD",
    "renpy.text.text.VERT_REVERSE",
    "renpy.savelocation.scan_thread_condition",
    "renpy.savelocation.disk_lock",
    "renpy.character.TAG_RE",
    "renpy.display.im.cache",
    "renpy.display.render.blit_lock",
    "renpy.display.render.IDENTITY",
    "renpy.loader.auto_lock",
    "renpy.display.screen.cprof",
    "renpy.audio.audio.lock",
    "renpy.audio.audio.periodic_condition",
    }


class Backup():
    """
    This represents a backup of all of the fields in the python modules
    comprising Ren'Py, shortly after they were imported.

    This attempts to preserve object aliasing, but not object identity. If
    renpy.mod.a is renpy.mod.b before the restore, the same will be true
    after the restore - even though renpy.mod.a will have changed identity.
    """

    def __init__(self):

        # A map from (module, field) to the id of the object in that field.
        self.variables = { }

        # A map from id(object) to objects. This is discarded after being
        # pickled.
        self.objects = { }

        # A map from module to the set of names in that module.
        self.names = { }

        if mobile:
            return

        for m in sys.modules.values():
            if m is None:
                continue

            self.backup_module(m)

        # A pickled version of self.objects.
        self.objects_pickle = cPickle.dumps(self.objects, cPickle.HIGHEST_PROTOCOL)

        self.objects = None

    def backup_module(self, mod):
        """
        Makes a backup of `mod`, which must be a Python module.
        """

        try:
            name = mod.__name__
        except:
            return

        if not name.startswith("renpy"):
            return

        if name in backup_blacklist:
            return

        if name.startswith("renpy.styledata"):
            return

        self.names[mod] = set(vars(mod).keys())

        for k, v in vars(mod).iteritems():

            if k.startswith("__") and k.endswith("__"):
                continue

            if isinstance(v, type_blacklist):
                continue

            if name + "." + k in name_blacklist:
                continue

            idv = id(v)

            self.variables[mod, k] = idv
            self.objects[idv] = v

            # If we have a problem pickling things, uncomment the next block.

            try:
                cPickle.dumps(v, cPickle.HIGHEST_PROTOCOL)
            except:
                print("Cannot pickle", name + "." + k, "=", repr(v))
                print("Reduce Ex is:", repr(v.__reduce_ex__(cPickle.HIGHEST_PROTOCOL)))

    def restore(self):
        """
        Restores the modules to a state similar to the state of the modules
        when the backup was created.
        """

        if not self.names:
            return

        # Remove new variables from the module.
        for mod, names in self.names.iteritems():
            modvars = vars(mod)
            for name in set(modvars.keys()) - names:
                del modvars[name]

        objects = cPickle.loads(self.objects_pickle)

        for k, v in self.variables.iteritems():
            mod, field = k
            setattr(mod, field, objects[v])


# A backup of the Ren'Py modules after initial import.
backup = None

################################################################################
# Import
################################################################################


def update_path(package):
    """
    Update the __path__ of package, to import binary modules from a libexec
    directory.
    """

    name = package.__name__.split(".")

    import _renpy
    libexec = os.path.dirname(_renpy.__file__)
    package.__path__.append(os.path.join(libexec, *name))

    # Also find encodings, to deal with the way py2exe lays things out.
    import encodings
    libexec = os.path.dirname(encodings.__path__[0])
    package.__path__.append(os.path.join(libexec, *name))

# Replaced below.


def plog(level, even, *args):
    return


def import_all():

    # Note: If we add a new update_path, we have to add an equivalent
    # hook in the renpython hooks dir.

    # Note: If we add a new module, we need to add it to iOS.

    import renpy  # @UnresolvedImport

    update_path(renpy)

    import renpy.arguments  # @UnresolvedImport

    import renpy.config
    import renpy.log

    import renpy.display

    import renpy.debug

    # Should probably be early, as we will add it as a base to serialized things.
    import renpy.object

    import renpy.game
    import renpy.preferences

    # Adds in the Ren'Py loader.
    import renpy.loader

    import renpy.pyanalysis

    import renpy.ast
    import renpy.atl
    import renpy.curry
    import renpy.color
    import renpy.easy
    import renpy.execution
    import renpy.loadsave
    import renpy.savelocation  # @UnresolvedImport
    import renpy.persistent
    import renpy.scriptedit
    import renpy.parser
    import renpy.performance
    import renpy.pydict
    import renpy.python
    import renpy.script
    import renpy.statements

    global plog
    plog = renpy.performance.log

    import renpy.styledata  # @UnresolvedImport
    update_path(renpy.styledata)

    import renpy.style
    renpy.styledata.import_style_functions()

    sys.modules['renpy.styleclass'] = renpy.style

    import renpy.substitutions
    import renpy.translation
    import renpy.translation.scanstrings
    import renpy.translation.generation
    import renpy.translation.dialogue
    import renpy.translation.extract
    import renpy.translation.merge

    import renpy.display  # @UnresolvedImport @Reimport

    update_path(renpy.display)

    import renpy.display.presplash
    import renpy.display.pgrender
    import renpy.display.scale
    import renpy.display.module
    import renpy.display.render  # Most display stuff depends on this. @UnresolvedImport
    import renpy.display.core  # object @UnresolvedImport

    import renpy.text

    update_path(renpy.text)

    import renpy.text.ftfont
    import renpy.text.font
    import renpy.text.textsupport
    import renpy.text.texwrap
    import renpy.text.text
    import renpy.text.extras

    sys.modules['renpy.display.text'] = renpy.text.text

    import renpy.gl
    update_path(renpy.gl)

    import renpy.angle
    update_path(renpy.angle)

    import renpy.display.layout
    import renpy.display.viewport
    import renpy.display.transform
    import renpy.display.motion  # layout @UnresolvedImport
    import renpy.display.behavior  # layout @UnresolvedImport
    import renpy.display.transition  # core, layout @UnresolvedImport
    import renpy.display.movetransition  # core @UnresolvedImport
    import renpy.display.im
    import renpy.display.imagelike
    import renpy.display.image  # core, behavior, im, imagelike @UnresolvedImport
    import renpy.display.video
    import renpy.display.focus
    import renpy.display.anim
    import renpy.display.particle
    import renpy.display.joystick
    import renpy.display.controller
    import renpy.display.minigame
    import renpy.display.screen
    import renpy.display.dragdrop
    import renpy.display.imagemap
    import renpy.display.predict
    import renpy.display.emulator
    import renpy.display.tts
    import renpy.display.gesture

    import renpy.display.error

    # Note: For windows to work, renpy.audio.audio needs to be after
    # renpy.display.module.

    import renpy.audio
    update_path(renpy.audio)

    import renpy.audio.audio
    import renpy.audio.music
    import renpy.audio.sound

    import renpy.ui
    import renpy.screenlang

    import renpy.sl2
    update_path(renpy.sl2)

    import renpy.sl2.slast
    import renpy.sl2.slparser
    import renpy.sl2.slproperties
    import renpy.sl2.sldisplayables

    import renpy.lint
    import renpy.warp

    import renpy.editor

    import renpy.memory

    import renpy.exports
    import renpy.character  # depends on exports. @UnresolvedImport

    import renpy.add_from
    import renpy.dump

    import renpy.minstore  # depends on lots. @UnresolvedImport
    import renpy.defaultstore  # depends on everything. @UnresolvedImport

    import renpy.test
    import renpy.test.testmouse
    import renpy.test.testfocus
    import renpy.test.testkey
    import renpy.test.testast
    import renpy.test.testparser
    import renpy.test.testexecution

    import renpy.main

    # Back up the Ren'Py modules.

    global backup

    if not mobile:
        backup = Backup()

    post_import()


def post_import():
    """
    This is called after import or reload, to do further initialization
    of various modules.
    """

    import renpy  # @UnresolvedImport

    # Create the store.
    renpy.python.create_store("store")

    # Import the contents of renpy.defaultstore into renpy.store, and set
    # up an alias as we do.
    renpy.store = sys.modules['store']
    renpy.exports.store = renpy.store
    sys.modules['renpy.store'] = sys.modules['store']

    import subprocess
    sys.modules['renpy.subprocess'] = subprocess

    for k, v in renpy.defaultstore.__dict__.iteritems():
        renpy.store.__dict__.setdefault(k, v)

    renpy.store.eval = renpy.defaultstore.eval

    # Import everything into renpy.exports, provided it isn't
    # already there.
    for k, v in globals().iteritems():
        vars(renpy.exports).setdefault(k, v)


def reload_all():
    """
    Resets all modules to the state they were in right after import_all
    returned.
    """

    if mobile:
        raise Exception("Reloading is not supported on mobile platforms.")

    import renpy.style
    import renpy.display

    # Clear all pending exceptions.
    sys.exc_clear()

    # Reset the styles.
    renpy.style.reset()  # @UndefinedVariable

    # Shut down the cache thread.
    renpy.display.im.cache.quit()

    # Shut down the importer.
    renpy.loader.quit_importer()

    # Free memory.
    renpy.exports.free_memory()

    # GC renders.
    renpy.display.render.screen_render = None
    renpy.display.render.mark_sweep()

    # Get rid of the draw module and interface.
    renpy.display.draw.deinit()
    renpy.display.draw = None
    renpy.display.interface = None

    py_compile_cache = renpy.python.py_compile_cache

    # Delete the store modules.
    for i in sys.modules.keys():
        if i.startswith("store") or i == "renpy.store":
            m = sys.modules[i]

            if m is not None:
                m.__dict__.reset()

            del sys.modules[i]

    # Restore the state of all modules from backup.
    backup.restore()

    renpy.python.old_py_compile_cache = py_compile_cache

    renpy.display.im.reset_module()

    post_import()

    # Re-initialize the importer.
    renpy.loader.init_importer()


################################################################################
# Fix things for code analysis
################################################################################

def setup_modulefinder(modulefinder):
    """
    Informs modulefinder about the location of modules in nonstandard places.
    """

    import _renpy

    libexec = os.path.dirname(_renpy.__file__)

    for i in [ "display", "gl", "angle", "text", "styledata" ]:

        displaypath = os.path.join(libexec, "renpy", i)

        if os.path.exists(displaypath):
            modulefinder.AddPackagePath('renpy.' + i, displaypath)


def import_cython():
    """
    Never called, but necessary to ensure that modulefinder will properly
    grab the various cython modules.
    """

    import renpy.arguments

    import renpy.display.accelerator
    import renpy.display.render

    import renpy.gl.gl
    import renpy.gl.gl1
    import renpy.gl.gldraw
    import renpy.gl.glenviron_fixed
    import renpy.gl.glenviron_limited
    import renpy.gl.glenviron_shader
    import renpy.gl.glrtt_copy
    import renpy.gl.glrtt_fbo
    import renpy.gl.gltexture

    import renpy.angle.gl
    import renpy.angle.gldraw
    import renpy.angle.glenviron_shader
    import renpy.angle.glrtt_copy
    import renpy.angle.glrtt_fbo
    import renpy.angle.gltexture


if False:
    import renpy.defaultstore as store
