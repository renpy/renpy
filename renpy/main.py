# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

from typing import Tuple, List, Dict, Set, Optional, Iterable, Any

import os
import sys
import time
import zipfile
import gc
import linecache
import json

import renpy
import renpy.game as game

last_clock = time.time()


def log_clock(s):
    global last_clock
    now = time.time()
    s = "{} took {:.2f}s".format(s, now - last_clock)

    renpy.display.log.write(s)
    if renpy.android and not renpy.config.log_to_stdout:
        print(s)

    # Pump the presplash window to prevent marking
    # our process as unresponsive by OS
    renpy.display.presplash.pump_window()

    last_clock = now


def reset_clock():
    global last_clock
    last_clock = time.time()


def run(restart):
    """
    This is called during a single run of the script. Restarting the script
    will cause this to change.
    """

    reset_clock()

    # Reset the store to a clean version of itself.
    renpy.python.clean_stores()
    log_clock("Cleaning stores")

    # Init translation.
    renpy.translation.init_translation()
    log_clock("Init translation")

    # Rebuild the various style caches.
    renpy.style.build_styles() # @UndefinedVariable
    log_clock("Build styles")

    renpy.sl2.slast.load_cache()
    log_clock("Load screen analysis")

    # Analyze the screens.
    renpy.display.screen.analyze_screens()
    log_clock("Analyze screens")

    if not restart:
        renpy.sl2.slast.save_cache()
        log_clock("Save screen analysis")

    # Prepare the screens.
    renpy.display.screen.prepare_screens()

    log_clock("Prepare screens")

    if not restart:
        renpy.pyanalysis.save_cache()
        log_clock("Save pyanalysis.")

        renpy.game.script.save_bytecode()
        log_clock("Save bytecode.")

    # Handle arguments and commands.
    if not renpy.arguments.post_init():
        # We use 'exception' instead of exports.quit
        # to not call quit label since it's not nessesary.
        raise renpy.game.QuitException()

    # Clear obsolete image manipulators.
    renpy.display.im.ImageBase.obsolete_list = [ ]

    if renpy.config.clear_lines:
        renpy.scriptedit.lines.clear()

    # Sleep to finish the presplash.
    renpy.display.presplash.sleep()

    # Re-Initialize the log.
    game.log = renpy.python.RollbackLog()

    # Switch contexts, begin logging.
    game.contexts = [ renpy.execution.Context(True) ]

    # Jump to an appropriate start label.
    if game.script.has_label("_start"):
        start_label = '_start'
    else:
        start_label = 'start'

    game.context().goto_label(start_label)

    try:
        renpy.exports.log("--- " + time.ctime())
        renpy.exports.log("")
    except Exception:
        pass

    # Note if this is a restart.
    renpy.store._restart = restart

    # We run until we get an exception.
    renpy.display.interface.enter_context()

    log_clock("Running {}".format(start_label))

    renpy.execution.run_context(True)


def load_rpe(fn):

    with zipfile.ZipFile(fn) as zfn:
        autorun = zfn.read("autorun.py")

    if fn in sys.path:
        sys.path.remove(fn)
    sys.path.insert(0, fn)
    exec(autorun, {'__file__': os.path.join(fn, "autorun.py")})


def load_rpe_py(fn):

    with open(fn) as f:
        autorun = f.read()

    exec(autorun, {'__file__': fn})


def choose_variants():

    if "RENPY_VARIANT" in os.environ:
        renpy.config.variants = list(os.environ["RENPY_VARIANT"].split()) + [ None ] # type: ignore
        renpy.display.emulator.early_init_emulator()
        return

    renpy.config.variants = [ None ]

    if renpy.android: # @UndefinedVariable

        renpy.config.variants.insert(0, 'mobile') # type: ignore
        renpy.config.variants.insert(0, 'android') # type: ignore

        import android # type: ignore
        import math
        import pygame_sdl2 as pygame

        from jnius import autoclass # type: ignore

        # Manufacturer/Model-specific variants.
        try:
            Build = autoclass("android.os.Build")

            manufacturer = Build.MANUFACTURER
            model = Build.MODEL

            print("Manufacturer", manufacturer, "model", model)

            if manufacturer == "Amazon" and model.startswith("AFT"):
                print("Running on a Fire TV.")
                renpy.config.variants.insert(0, "firetv") # type: ignore
        except Exception:
            pass

        # Are we running on OUYA or Google TV or something similar?
        package_manager = android.activity.getPackageManager()

        if package_manager.hasSystemFeature("android.hardware.type.television"):
            print("Running on a television.")
            renpy.config.variants.insert(0, "tv") # type: ignore
            renpy.config.variants.insert(0, "small") # type: ignore
            return

        # Running on a chromebook.
        try:
            PythonSDLActivity = autoclass("org.renpy.android.PythonSDLActivity")
            if PythonSDLActivity.isChromebook():
                print("Running on ChromeOS.")
                renpy.config.variants.insert(0, 'chromeos') # type: ignore
        except Exception:
            pass

        # Otherwise, a phone or tablet.
        renpy.config.variants.insert(0, 'touch') # type: ignore

        pygame.display.init()

        info = renpy.display.get_info()
        diag = math.hypot(info.current_w, info.current_h) / android.get_dpi() # type: ignore
        print("Screen diagonal is", diag, "inches.")

        if diag >= 6:
            renpy.config.variants.insert(0, 'tablet') # type: ignore
            renpy.config.variants.insert(0, 'medium') # type: ignore
        else:
            renpy.config.variants.insert(0, 'phone') # type: ignore
            renpy.config.variants.insert(0, 'small') # type: ignore

    elif renpy.ios:
        renpy.config.variants.insert(0, 'mobile') # type: ignore
        renpy.config.variants.insert(0, 'ios') # type: ignore
        renpy.config.variants.insert(0, 'touch') # type: ignore

        from pyobjus import autoclass # type: ignore
        UIDevice = autoclass("UIDevice")

        idiom = UIDevice.currentDevice().userInterfaceIdiom

        print("iOS device idiom", idiom)

        # idiom 0 is iPhone, 1 is iPad. We assume any bigger idiom will
        # be tablet-like.
        if idiom >= 1:
            renpy.config.variants.insert(0, 'tablet') # type: ignore
            renpy.config.variants.insert(0, 'medium') # type: ignore
        else:
            renpy.config.variants.insert(0, 'phone') # type: ignore
            renpy.config.variants.insert(0, 'small') # type: ignore

    elif renpy.emscripten:
        import emscripten # type: ignore
        import re

        # web
        renpy.config.variants.insert(0, 'web') # type: ignore

        # mobile
        mobile = emscripten.run_script_int(
            r'''/Mobile|Android|iPad|iPhone/.test(navigator.userAgent)
            || (navigator.userAgent.indexOf("Mac") != -1 && navigator.maxTouchPoints > 1)''')
        if mobile:
            renpy.config.variants.insert(0, 'mobile') # type: ignore
        # Reserve android/ios for when the OS API is exposed
        # if re.search('Android', userAgent):
        #    renpy.config.variants.insert(0, 'android')
        # if re.search('iPad|iPhone', userAgent):
        #    renpy.config.variants.insert(0, 'ios')

        # touch
        touch = emscripten.run_script_int(r'''
          ('ontouchstart' in window) ||
            (navigator.maxTouchPoints > 0) ||
            (navigator.msMaxTouchPoints > 0)''')
        if touch == 1:
            # mitigate hybrids (e.g. ms surface) by restricting touch to mobile
            if mobile:
                renpy.config.variants.insert(0, 'touch') # type: ignore

        # large/medium/small
        # tablet/phone
        # screen.width/height is auto-adjusted by browser,
        # so it can be used as a physical sizereference
        # (see also window.devicePixelRatio)
        # e.g. Galaxy S5:
        # - physical / OpenGL: 1080x1920
        # - web screen: 360x640 w/ devicePixelRatio=3
        ref_width = emscripten.run_script_int(r'''screen.width''')
        ref_height = emscripten.run_script_int(r'''screen.height''')
        # medium reference point: ipad 1024x768, ipad pro 1336x1024 (browser "pixels")
        if mobile:
            if (ref_width < 768 or ref_height < 768):
                renpy.config.variants.insert(0, 'small') # type: ignore
                renpy.config.variants.insert(0, 'phone') # type: ignore
            else:
                renpy.config.variants.insert(0, 'medium') # type: ignore
                renpy.config.variants.insert(0, 'tablet') # type: ignore
        else:
            renpy.config.variants.insert(0, 'large') # type: ignore

    else:
        renpy.config.variants.insert(0, 'pc') # type: ignore

        renpy.config.variants.insert(0, 'large') # type: ignore


def load_build_info():
    """
    Loads cache/build_info.json, and uses it to initialize the
    renpy.game.build_info dictionary.
    """

    try:
        f = renpy.exports.open_file("cache/build_info.json", "utf-8")
        renpy.game.build_info = json.load(f)
    except Exception:
        renpy.game.build_info = { "info" : { } }


def main():

    gc.set_threshold(*renpy.config.gc_thresholds)

    renpy.game.exception_info = 'Before loading the script.'

    # Clear the line cache, since the script may have changed.
    linecache.clearcache()

    # Get ready to accept new arguments.
    renpy.arguments.pre_init()

    # Init the screen language parser.
    renpy.sl2.slparser.init()

    # Init the config after load.
    renpy.config.init()

    # Reset live2d if it exists.
    try:
        renpy.gl2.live2d.reset()
    except Exception:
        pass

    # Set up variants.
    choose_variants()
    renpy.display.touch = "touch" in renpy.config.variants

    if (renpy.android or renpy.ios) and not renpy.config.log_to_stdout:
        print("Version:", renpy.version)

    # Note the game directory.
    game.basepath = renpy.config.gamedir
    renpy.config.commondir = renpy.__main__.path_to_common(renpy.config.renpy_base) # E1101 @UndefinedVariable
    renpy.config.searchpath = renpy.__main__.predefined_searchpath(renpy.config.commondir) # E1101 @UndefinedVariable

    # Load Ren'Py extensions.
    for dir in [ renpy.config.renpy_base ] + renpy.config.searchpath: # @ReservedAssignment

        if not os.path.isdir(dir):
            continue

        for fn in sorted(os.listdir(dir)):
            if fn.lower().endswith(".rpe"):
                load_rpe(dir + "/" + fn)

            if fn.lower().endswith(".rpe.py"):
                load_rpe_py(dir + "/" + fn)

    # Generate a list of extensions for each archive handler.
    archive_extensions = [ ]
    for handler in renpy.loader.archive_handlers:
        for ext in handler.get_supported_extensions():
            if not (ext in archive_extensions):
                archive_extensions.append(ext)

    # Find archives.
    for dn in renpy.config.searchpath:

        if not os.path.isdir(dn):
            continue

        for i in sorted(os.listdir(dn)):
            base, ext = os.path.splitext(i)

            # Check if the archive does not have any of the extensions in archive_extensions
            if not (ext in archive_extensions):
                continue

            renpy.config.archives.append(base)

    renpy.config.archives.reverse()

    # Initialize archives.
    renpy.loader.index_archives()

    # Start auto-loading.
    renpy.loader.auto_init()

    load_build_info()

    log_clock("Early init")

    # Initialize the log.
    game.log = renpy.python.RollbackLog()

    # Initialize the store.
    renpy.store.store = sys.modules['store'] # type: ignore

    # Set up styles.
    game.style = renpy.style.StyleManager() # @UndefinedVariable
    renpy.store.style = game.style

    # Run init code in its own context. (Don't log.)
    game.contexts = [ renpy.execution.Context(False) ]
    game.contexts[0].init_phase = True

    renpy.execution.not_infinite_loop(60)

    # Load the script.
    renpy.game.exception_info = 'While loading the script.'
    renpy.game.script = renpy.script.Script()

    if renpy.session.get("compile", False):
        renpy.game.args.compile = True # type: ignore

    # Set up error handling.
    renpy.exports.load_module("_errorhandling")

    if renpy.exports.loadable("tl/None/common.rpym") or renpy.exports.loadable("tl/None/common.rpymc"):
        renpy.exports.load_module("tl/None/common")

    renpy.config.init_system_styles()
    renpy.style.build_styles() # @UndefinedVariable

    log_clock("Loading error handling")

    # If recompiling everything, remove orphan .rpyc files.
    # Otherwise, will fail in case orphan .rpyc have same
    # labels as in other scripts (usually happens on script rename).
    if (renpy.game.args.command == 'compile') and not (renpy.game.args.keep_orphan_rpyc): # type: ignore

        for (fn, dn) in renpy.game.script.script_files:

            if dn is None:
                continue

            if not os.path.isfile(os.path.join(dn, fn + ".rpy")) and not os.path.isfile(os.path.join(dn, fn + "_ren.py")):

                try:
                    name = os.path.join(dn, fn + ".rpyc")
                    os.rename(name, name + ".bak")
                except OSError:
                    # This perhaps shouldn't happen since either .rpy or .rpyc should exist
                    pass

        # Update script files list, so that it doesn't contain removed .rpyc's
        renpy.loader.cleardirfiles()
        renpy.game.script.scan_script_files()

    # Load all .rpy files.
    renpy.game.script.load_script() # sets renpy.game.script.
    log_clock("Loading script")

    if renpy.game.args.command == 'load-test': # type: ignore
        start = time.time()

        for i in range(5):
            print(i)
            renpy.game.script = renpy.script.Script()
            renpy.game.script.load_script()

        print(time.time() - start)
        sys.exit(0)

    renpy.game.exception_info = 'After loading the script.'

    # Find the save directory.
    if renpy.config.savedir is None:
        renpy.config.savedir = renpy.__main__.path_to_saves(renpy.config.gamedir) # E1101 @UndefinedVariable

    if renpy.game.args.savedir: # type: ignore
        renpy.config.savedir = renpy.game.args.savedir # type: ignore

    # Init the save token system.
    renpy.savetoken.init()

    # Init preferences.
    game.persistent = renpy.persistent.init()
    game.preferences = game.persistent._preferences

    for i in renpy.game.persistent._seen_translates: # type: ignore
        if i in renpy.game.script.translator.default_translates:
            renpy.game.seen_translates_count += 1

    if game.persistent._virtual_size:
        renpy.config.screen_width, renpy.config.screen_height = game.persistent._virtual_size

    # Init save locations and loadsave.
    renpy.savelocation.init()

    try:
        # Init save slots and save tokens.
        renpy.loadsave.init()
        renpy.savetoken.upgrade_all_savefiles()
        log_clock("Loading save slot metadata")

        # Load persistent data from all save locations.
        renpy.persistent.update()
        game.preferences = game.persistent._preferences
        log_clock("Loading persistent")

        # Clear the list of seen statements in this game.
        game.seen_session = { }

        # Initialize persistent variables.
        renpy.store.persistent = game.persistent # type: ignore
        renpy.store._preferences = game.preferences # type: ignore
        renpy.store._test = renpy.test.testast._test # type: ignore

        if renpy.parser.report_parse_errors():
            raise renpy.game.ParseErrorException()

        renpy.game.exception_info = 'While executing init code:'

        for id_, (_prio, node) in enumerate(game.script.initcode):

            renpy.game.initcode_ast_id = id_

            if isinstance(node, renpy.ast.Node):
                node_start = time.time()

                renpy.game.context().run(node)

                node_duration = time.time() - node_start

                if node_duration > renpy.config.profile_init:
                    renpy.display.log.write(" - Init at %s:%d took %.5f s.", node.filename, node.linenumber, node_duration)

            else:
                # An init function.
                node()

        renpy.game.exception_info = 'After initialization, but before game start.'

        # Check if we should simulate android.
        renpy.android = renpy.android or renpy.config.simulate_android # @UndefinedVariable

        # Re-set up the logging.
        renpy.log.post_init()

        # Run the post init code, if any.
        for i in renpy.game.post_init:
            i()

        renpy.config.post_init()

        renpy.game.script.report_duplicate_labels()

        # Sort the images.
        renpy.display.image.image_names.sort()

        game.persistent._virtual_size = renpy.config.screen_width, renpy.config.screen_height # type: ignore

        log_clock("Running init code")

        renpy.pyanalysis.load_cache()
        log_clock("Loading analysis data")

        # Analyze the script and compile ATL.
        renpy.game.script.analyze()
        renpy.atl.compile_all()
        log_clock("Analyze and compile ATL")

        renpy.savelocation.init()
        renpy.loadsave.init()
        log_clock("Reloading save slot metadata")

        # Index the archive files. We should not have loaded an image
        # before this point. (As pygame will not have been initialized.)
        # We need to do this again because the list of known archives
        # may have changed.
        renpy.loader.index_archives()
        log_clock("Index archives")

        # Check some environment variables.
        renpy.game.less_memory = "RENPY_LESS_MEMORY" in os.environ
        renpy.game.less_mouse = "RENPY_LESS_MOUSE" in os.environ
        renpy.game.less_updates = "RENPY_LESS_UPDATES" in os.environ

        renpy.dump.dump(False)
        renpy.game.script.make_backups()
        log_clock("Dump and make backups")

        # Initialize image cache.
        renpy.display.im.cache.init()
        log_clock("Cleaning cache")

        # Make a clean copy of the store.
        renpy.python.make_clean_stores()
        log_clock("Making clean stores")

        # Init the keymap.
        renpy.display.behavior.init_keymap()

        gc.collect(2)

        if gc.garbage:
            del gc.garbage[:]

        if renpy.config.manage_gc:
            gc.set_threshold(*renpy.config.gc_thresholds)

            gc_debug = int(os.environ.get("RENPY_GC_DEBUG", 0))

            if renpy.config.gc_print_unreachable:
                gc_debug |= gc.DEBUG_SAVEALL

            gc.set_debug(gc_debug)

        else:
            gc.set_threshold(700, 10, 10)

        log_clock("Initial gc")

        # Start debugging file opens.
        renpy.debug.init_main_thread_open()

        # (Perhaps) Initialize graphics.
        if not game.interface:
            renpy.display.core.Interface()
            log_clock("Creating interface object")

        # Start things running.
        restart = None

        while True:

            if restart:
                renpy.display.screen.before_restart()

            try:
                try:
                    run(restart)
                finally:
                    restart = (renpy.config.end_game_transition, "_invoke_main_menu", "_main_menu")

            except renpy.game.QuitException:

                renpy.audio.audio.fadeout_all()
                raise

            except game.FullRestartException as e:
                restart = e.reason

            finally:

                renpy.persistent.update(True)
                renpy.persistent.save_on_quit_MP()

                # Reset live2d if it exists.
                try:
                    renpy.gl2.live2d.reset_states()
                except Exception:
                    pass

                # Flush any pending interface work.
                renpy.display.interface.finish_pending()

                # Give Ren'Py a couple of seconds to finish saving.
                renpy.loadsave.autosave_not_running.wait(3.0)

                # Run the at exit callbacks.
                for cb in renpy.config.at_exit_callbacks:
                    cb()

    finally:

        gc.set_debug(0)

        for i in renpy.config.quit_callbacks:
            i()

        renpy.loader.auto_quit()
        renpy.savelocation.quit()
        renpy.translation.write_updated_strings()

    # This is stuff we do on a normal, non-error return.
    if not renpy.display.error.error_handled:
        renpy.display.render.check_at_shutdown()
