# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import annotations

from typing import Any, NamedTuple
import sys
import os
import types
import site

# Set up the hook for any renpy __init__ modules to import binary modules from
# a libexec directory if it available.
# This is relevant only for development RenPy itself, when compiled binaries
# are stored in the libexec directory.
try:
    import _renpy  # type: ignore

    if getattr(_renpy, "__file__", "built-in") != "built-in":
        import importlib.util

        libexec: str = os.path.dirname(_renpy.__file__)

        class _LibExecFinder:
            def __init__(self):
                self.in_find_spec: bool = False

            def find_spec(self, fullname: str, path, target=None, /):
                if not fullname.startswith("renpy."):
                    return None

                if self.in_find_spec:
                    return None

                self.in_find_spec = True

                try:
                    spec = importlib.util.find_spec(fullname)
                finally:
                    self.in_find_spec = False

                if spec is None:
                    return None

                # Is a package.
                if spec.submodule_search_locations is not None:
                    name = fullname.split(".")
                    spec.submodule_search_locations.append(os.path.join(libexec, *name))

                return spec

        sys.meta_path.insert(0, _LibExecFinder())

        # Add the libexec directory to this module.
        try:
            __spec__.submodule_search_locations.append(os.path.join(libexec, "renpy"))
            __path__ = list(__spec__.submodule_search_locations)
        except Exception:
            pass

except ImportError:
    pass

# All imports should go below renpy.compat.
import renpy.compat.pickle as pickle

# Initial import of the __main__ module. This gets replaced in renpy.py
# whatever that module has been imported as.
import __main__

################################################################################
# Version information
################################################################################

# Version numbers.
official: bool
nightly: bool
version_name: str
version: str
try:
    from renpy.vc_version import (  # type: ignore
        official,
        nightly,
        version_name,
        version,
    )

except ImportError:
    import renpy.versions

    version_dict = renpy.versions.get_version()

    official = version_dict["official"]
    nightly = version_dict["nightly"]
    version_name = version_dict["version_name"]
    version = version_dict["version"]

official = official and getattr(site, "renpy_build_official", False)


class VersionTuple(NamedTuple):
    major: int
    minor: int
    patch: int
    commit: int


version_tuple = VersionTuple(*(int(i) for i in version.split(".")))

# A string giving the version number only (8.0.1.123), with a suffix if needed.
version_only = ".".join(str(i) for i in version_tuple)

if not official:
    version_only += "+unofficial"
elif nightly:
    version_only += "+nightly"

# A verbose string giving the version.
version = "Ren'Py " + version_only

# Other versions.
script_version: int = 5003000
savegame_suffix: str = "-LT1.save"
bytecode_version: int = 1

################################################################################
# Platform Information
################################################################################

# Information about the platform we're running on. We break the platforms
# up into 6 groups - windows-like, mac-like, linux-like, android-like,
# ios-like and web (aka. emscripten).
windows: bool = False
macintosh: bool = False
linux: bool = False
android: bool = False
ios: bool = False
emscripten: bool = False

# Should we enable experimental features and debugging?
experimental = "RENPY_EXPERIMENTAL" in os.environ

import platform

if platform.win32_ver()[0]:
    windows = True
elif os.environ.get("RENPY_PLATFORM", "").startswith("ios"):
    ios = True
elif platform.mac_ver()[0]:
    macintosh = True
elif "ANDROID_PRIVATE" in os.environ:
    android = True
elif sys.platform == "emscripten" or "RENPY_EMSCRIPTEN" in os.environ:
    emscripten = True
else:
    linux = True

arch: str = os.environ.get("RENPY_PLATFORM", "unknown-unknown-unknown").rpartition("-")[2]

# A flag that's true if we're on a smartphone or tablet-like platform.
mobile: bool = android or ios or emscripten

# A flag that's set to true if the game directory is bundled inside a mac app.
macapp: bool = False

################################################################################
# Backup Data for Reload
################################################################################

# True if we're done with safe mode checks.
safe_mode_checked: bool = False

# True if autoreload mode is enabled. This has to live here, because it
# needs to survive through an utter restart.
autoreload: bool = False

# A dict that persists through utter restarts. Accessible to all code as
# renpy.session.
session: dict[str, Any] = {}

# A list of modules beginning with "renpy" that we don't want
# to backup.
backup_blacklist = {
    "renpy",
    "renpy.compat",
    "renpy.compat.dictviews",
    "renpy.object",
    "renpy.log",
    "renpy.bootstrap",
    "renpy.debug",
    "renpy.display",
    "renpy.display.pgrender",
    "renpy.display.presplash",
    "renpy.display.scale",
    "renpy.display.swdraw",
    "renpy.display.test",
    "renpy.six",
    "renpy.text.ftfont",
    "renpy.text.hbfont",
    "renpy.text.bidi",
    "renpy.test",
    "renpy.test.testast",
    "renpy.test.testexecution",
    "renpy.test.testkey",
    "renpy.test.testmouse",
    "renpy.test.testparser",
    "renpy.test.testreporter",
    "renpy.test.testsettings",
    "renpy.tfd",
    "renpy.gl2",
    "renpycoverage",
}

type_blacklist = (types.ModuleType,)

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
    "renpy.display.render.main_thread",
    "renpy.display.render.blit_lock",
    "renpy.display.render.IDENTITY",
    "renpy.loader.auto_lock",
    "renpy.display.screen.cprof",
    "renpy.audio.audio.lock",
    "renpy.audio.audio.periodic_condition",
    "renpy.webloader.queue_lock",
    "renpy.persistent.MP_instances",
    "renpy.exports.sdl_dll",
    "renpy.sl2.slast.serial",
    "renpy.gl2.assimp.loader",
    "renpy.gl2.assimp.loader_lock",
    "renpy.gl2.gl2draw.default_position",
}


class Backup:
    """
    This represents a backup of all of the fields in the python modules
    comprising Ren'Py, shortly after they were imported.

    This attempts to preserve object aliasing, but not object identity. If
    renpy.mod.a is renpy.mod.b before the restore, the same will be true
    after the restore - even though renpy.mod.a will have changed identity.
    """

    def __init__(self):
        # A map from (module, field) to the id of the object in that field.
        self.variables = {}

        # A map from id(object) to objects. This is discarded after being
        # pickled.
        self.objects = {}

        # A map from module to the set of names in that module.
        self.names = {}

    def backup(self):
        for m in sys.modules.values():
            if m is None:
                continue

            self.backup_module(m)

        # A pickled version of self.objects.
        self.objects_pickle = pickle.dumps(self.objects, highest=True)

        self.objects = {}

    def backup_module(self, mod):
        """
        Makes a backup of `mod`, which must be a Python module.
        """

        try:
            name = mod.__name__
        except Exception:
            return

        if not name.startswith("renpy"):
            return

        if name.startswith("renpy.pygame"):
            return

        if name in backup_blacklist:
            return

        if name.startswith("renpy.styledata"):
            return

        self.names[mod] = set(vars(mod).keys())

        for k, v in vars(mod).items():
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
                pickle.dumps(v, highest=True)
            except Exception:
                print("Cannot pickle", name + "." + k, "=", repr(v))
                print("Reduce Ex is:", repr(v.__reduce_ex__(pickle.PROTOCOL)))

    def restore(self):
        """
        Restores the modules to a state similar to the state of the modules
        when the backup was created.
        """

        if not self.names:
            return

        # Remove new variables from the module.
        for mod, names in self.names.items():
            modvars = mod.__dict__
            for name in set(modvars.keys()) - names:
                del modvars[name]

        objects = pickle.loads(self.objects_pickle)

        for k, v in self.variables.items():
            mod, field = k
            setattr(mod, field, objects[v])


# A backup of the Ren'Py modules after initial import.
backup = Backup()

################################################################################
# Import
################################################################################


def plog(depth, event, *args):
    """
    Empty version of renpy.plog that is replaced by the real implementation
    in import_all.
    """

    return


def import_all():
    # Note: If we add a new update_path, we have to add an equivalent
    # hook in the renpython hooks dir.

    # Note: If we add a new module, we need to add it to iOS.

    # Note: If we add a new module, it should be added at the bottom of this file so it shows up in
    # code analysis.

    import renpy

    import renpy.types

    import renpy.error
    import renpy.config
    import renpy.log

    import renpy.arguments

    import renpy.compat.fixes

    import renpy.display

    import renpy.debug

    # Should probably be early, as we will add these as a base to serialized things.
    import renpy.object

    import renpy.game
    import renpy.preferences

    # Adds in the Ren'Py loader.
    import renpy.loader
    import renpy.importer

    import renpy.pyanalysis

    sys.modules["renpy.py3analysis"] = renpy.pyanalysis

    import renpy.astsupport

    import renpy.parameter
    import renpy.ast
    import renpy.atl
    import renpy.curry
    import renpy.color
    import renpy.easy
    import renpy.encryption
    import renpy.execution
    import renpy.lexer
    import renpy.loadsave
    import renpy.savelocation
    import renpy.savetoken
    import renpy.persistent
    import renpy.scriptedit
    import renpy.parser
    import renpy.performance
    import renpy.pydict
    import renpy.revertable
    import renpy.rollback
    import renpy.python
    import renpy.script
    import renpy.statements
    import renpy.util
    import renpy.versions

    global plog
    plog = renpy.performance.log

    import renpy.styledata

    import renpy.style

    renpy.styledata.import_style_functions()

    sys.modules["renpy.styleclass"] = renpy.style

    import renpy.substitutions
    import renpy.translation
    import renpy.translation.scanstrings
    import renpy.translation.generation
    import renpy.translation.dialogue
    import renpy.translation.extract
    import renpy.translation.merge

    import renpy.display

    import renpy.display.position
    import renpy.display.presplash
    import renpy.display.pgrender
    import renpy.display.scale
    import renpy.display.module
    import renpy.display.render
    import renpy.display.displayable
    import renpy.display.core
    import renpy.display.scenelists
    import renpy.display.swdraw

    import renpy.text

    import renpy.text.ftfont
    import renpy.text.font
    import renpy.text.textsupport
    import renpy.text.texwrap
    import renpy.text.text
    import renpy.text.extras
    import renpy.text.shader

    sys.modules["renpy.display.text"] = renpy.text.text

    import renpy.gl2

    import renpy.display.layout
    import renpy.display.viewport
    import renpy.display.transform
    import renpy.display.motion
    import renpy.display.behavior
    import renpy.display.transition
    import renpy.display.movetransition
    import renpy.display.im
    import renpy.display.imagelike
    import renpy.display.image
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
    import renpy.display.model
    import renpy.display.quaternion

    import renpy.display.error

    renpy.atl.late_imports()

    # Note: For windows to work, renpy.audio.audio needs to be after
    # renpy.display.module.

    import renpy.audio

    import renpy.audio.audio
    import renpy.audio.music
    import renpy.audio.sound
    import renpy.audio.filter

    import renpy.ui
    import renpy.screenlang

    import renpy.sl2
    import renpy.sl2.slast
    import renpy.sl2.slparser
    import renpy.sl2.slproperties
    import renpy.sl2.sldisplayables

    import renpy.lint
    import renpy.warp

    import renpy.editor

    import renpy.memory

    import renpy.exports
    import renpy.character

    import renpy.add_from
    import renpy.dump

    import renpy.gl2.gl2draw
    import renpy.gl2.gl2mesh
    import renpy.gl2.gl2model
    import renpy.gl2.gl2polygon
    import renpy.gl2.gl2shader
    import renpy.gl2.gl2texture
    import renpy.gl2.live2d
    import renpy.gl2.assimp

    import renpy.minstore
    import renpy.defaultstore

    import renpy.test
    import renpy.test.testsettings
    import renpy.test.testmouse
    import renpy.test.testfocus
    import renpy.test.testkey
    import renpy.test.testast
    import renpy.test.testparser
    import renpy.test.testreporter
    import renpy.test.testexecution

    import renpy.update
    import renpy.update.deferred


    try:
        import renpy.tfd
        sys.modules["_renpytfd"] = renpy.tfd
    except ImportError:
        pass

    import renpy.main

    global six
    import six

    sys.modules["renpy.six"] = six

    # Back up the Ren'Py modules.
    backup.backup()

    post_import()


def post_import():
    """
    This is called after import or reload, to do further initialization
    of various modules.
    """

    import renpy

    # Create the store.
    renpy.python.create_store("store")

    # Import the contents of renpy.defaultstore into renpy.store, and set
    # up an alias as we do.
    renpy.store = sys.modules["store"]  # type: ignore
    renpy.exports.store = renpy.store  # type: ignore
    sys.modules["renpy.store"] = sys.modules["store"]

    import subprocess

    sys.modules["renpy.subprocess"] = subprocess

    for k, v in renpy.defaultstore.__dict__.items():
        if k in ("__all__", "__name__", "__doc__", "__package__", "__loader__", "__spec__", "__file__", "__cached__"):
            continue

        renpy.store.__dict__.setdefault(k, v)  # type: ignore

    renpy.store.eval = renpy.defaultstore.eval  # type: ignore

    # Import everything into renpy.exports, provided it isn't
    # already there.
    for k, v in globals().items():
        renpy.exports.__dict__.setdefault(k, v)


def issubmodule(sub, module):
    return sub == module or sub.startswith(module + ".")


def reload_all():
    """
    Resets all modules to the state they were in right after import_all
    returned.
    """

    import renpy

    # Quit audio.
    renpy.audio.audio.quit()

    # Reset the styles.
    renpy.style.reset()  # type: ignore

    # Shut down the cache thread.
    renpy.display.im.cache.quit()

    # Shut down the importer.
    renpy.importer.quit_importer()

    # Free memory.
    renpy.exports.free_memory()

    # GC renders.
    renpy.display.render.screen_render = None
    renpy.display.render.mark_sweep()

    # Get rid of the draw module and interface.
    renpy.display.interface = None

    if not renpy.session.get("_keep_renderer", False):
        renpy.display.draw.quit()  # type: ignore
        renpy.display.draw = None

    py_compile_cache = renpy.python.py_compile_cache
    reload_modules = renpy.config.reload_modules

    # Delete the store modules.
    for i in list(sys.modules.keys()):
        if issubmodule(i, "store") or i == "renpy.store":
            m = sys.modules[i]

            if m is not None:
                m.__dict__.reset()  # type: ignore

            del sys.modules[i]

        elif any(issubmodule(i, m) for m in reload_modules):
            del sys.modules[i]

    # Restore the state of all modules from backup.
    backup.restore()

    renpy.python.old_py_compile_cache = py_compile_cache

    renpy.display.im.reset_module()

    post_import()

    # Re-initialize the importer.
    renpy.importer.init_importer()

    renpy.test.testexecution.on_reload()

    # Reset main log clock.
    renpy.main.reset_clock()


# renpy.store and sub-modules can have names of any type inside.
store: Any = None


# Generated by scripts/relative_imports.py, do not edit below this line.
import typing

if typing.TYPE_CHECKING:
    from . import add_from as add_from
    from . import arguments as arguments
    from . import ast as ast
    from . import astsupport as astsupport
    from . import atl as atl
    from . import audio as audio
    from . import bootstrap as bootstrap
    from . import character as character
    from . import color as color
    from . import compat as compat
    from . import config as config
    from . import cslots as cslots
    from . import curry as curry
    from . import debug as debug
    from . import defaultstore as defaultstore
    from . import display as display
    from . import dump as dump
    from . import easy as easy
    from . import editor as editor
    from . import encryption as encryption
    from . import error as error
    from . import execution as execution
    from . import exports as exports
    from . import game as game
    from . import gl2 as gl2
    from . import importer as importer
    from . import lexer as lexer
    from . import lexersupport as lexersupport
    from . import lint as lint
    from . import loader as loader
    from . import loadsave as loadsave
    from . import log as log
    from . import main as main
    from . import memory as memory
    from . import minstore as minstore
    from . import object as object
    from . import parameter as parameter
    from . import parser as parser
    from . import performance as performance
    from . import persistent as persistent
    from . import preferences as preferences
    from . import pyanalysis as pyanalysis
    from . import pydict as pydict
    from . import pygame as pygame
    from . import python as python
    from . import revertable as revertable
    from . import rollback as rollback
    from . import savelocation as savelocation
    from . import savetoken as savetoken
    from . import screenlang as screenlang
    from . import script as script
    from . import scriptedit as scriptedit
    from . import sl2 as sl2
    from . import statements as statements
    from . import style as style
    from . import styledata as styledata
    from . import substitutions as substitutions
    from . import test as test
    from . import text as text
    from . import tfd as tfd
    from . import translation as translation
    from . import types as types
    from . import uguu as uguu
    from . import ui as ui
    from . import update as update
    from . import util as util
    from . import vc_version as vc_version
    from . import versions as versions
    from . import warp as warp
    from . import webloader as webloader
