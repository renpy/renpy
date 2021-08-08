# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
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
from renpy.compat import *

import renpy.display
import renpy.style
import renpy.sl2
import renpy.test

import renpy.game as game

import os
import sys
import time
import zipfile
import gc
import linecache

import __main__

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
    except:
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

    sys.path.insert(0, fn)
    exec(autorun, dict())


def choose_variants():

    if "RENPY_VARIANT" in os.environ:
        renpy.config.variants = list(os.environ["RENPY_VARIANT"].split()) + [ None ]
        return

    renpy.config.variants = [ None ]

    if renpy.android: # @UndefinedVariable

        renpy.config.variants.insert(0, 'mobile')
        renpy.config.variants.insert(0, 'android')

        import android # @UnresolvedImport
        import math
        import pygame_sdl2 as pygame

        from jnius import autoclass # @UnresolvedImport

        # Manufacturer/Model-specific variants.
        try:
            Build = autoclass("android.os.Build")

            manufacturer = Build.MANUFACTURER
            model = Build.MODEL

            print("Manufacturer", manufacturer, "model", model)

            if manufacturer == "Amazon" and model.startswith("AFT"):
                print("Running on a Fire TV.")
                renpy.config.variants.insert(0, "firetv")
        except:
            pass

        # Are we running on OUYA or Google TV or something similar?
        package_manager = android.activity.getPackageManager()

        if package_manager.hasSystemFeature("android.hardware.type.television"):
            print("Running on a television.")
            renpy.config.variants.insert(0, "tv")
            renpy.config.variants.insert(0, "small")
            return

        # Otherwise, a phone or tablet.
        renpy.config.variants.insert(0, 'touch')

        pygame.display.init()

        info = renpy.display.get_info()
        diag = math.hypot(info.current_w, info.current_h) / android.get_dpi()
        print("Screen diagonal is", diag, "inches.")

        if diag >= 6:
            renpy.config.variants.insert(0, 'tablet')
            renpy.config.variants.insert(0, 'medium')
        else:
            renpy.config.variants.insert(0, 'phone')
            renpy.config.variants.insert(0, 'small')

    elif renpy.ios:
        renpy.config.variants.insert(0, 'mobile')
        renpy.config.variants.insert(0, 'ios')
        renpy.config.variants.insert(0, 'touch')

        from pyobjus import autoclass # @UnresolvedImport @Reimport
        UIDevice = autoclass("UIDevice")

        idiom = UIDevice.currentDevice().userInterfaceIdiom

        print("iOS device idiom", idiom)

        # idiom 0 is iPhone, 1 is iPad. We assume any bigger idiom will
        # be tablet-like.
        if idiom >= 1:
            renpy.config.variants.insert(0, 'tablet')
            renpy.config.variants.insert(0, 'medium')
        else:
            renpy.config.variants.insert(0, 'phone')
            renpy.config.variants.insert(0, 'small')

    elif renpy.emscripten:
        import emscripten
        import re

        # web
        renpy.config.variants.insert(0, 'web')

        # mobile
        userAgent = emscripten.run_script_string(r'''navigator.userAgent''')
        mobile = re.search('Mobile|Android|iPad|iPhone', userAgent)
        if mobile:
            renpy.config.variants.insert(0, 'mobile')
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
                renpy.config.variants.insert(0, 'touch')

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
                renpy.config.variants.insert(0, 'small')
                renpy.config.variants.insert(0, 'phone')
            else:
                renpy.config.variants.insert(0, 'medium')
                renpy.config.variants.insert(0, 'tablet')
        else:
            renpy.config.variants.insert(0, 'large')

    else:
        renpy.config.variants.insert(0, 'pc')

        renpy.config.variants.insert(0, 'large')


def main():

    gc.set_threshold(*renpy.config.gc_thresholds)

    log_clock("Bootstrap to the start of init.init")

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
    except:
        pass

    # Set up variants.
    choose_variants()
    renpy.display.touch = "touch" in renpy.config.variants

    log_clock("Early init")

    # Note the game directory.
    game.basepath = renpy.config.gamedir
    renpy.config.searchpath = [ renpy.config.gamedir ]

    # Find the common directory.
    commondir = __main__.path_to_common(renpy.config.renpy_base) # E1101 @UndefinedVariable

    if os.path.isdir(commondir):
        renpy.config.searchpath.append(commondir)
        renpy.config.commondir = commondir
    else:
        renpy.config.commondir = None

    # Add path from env variable, if any
    if "RENPY_SEARCHPATH" in os.environ:
        renpy.config.searchpath.extend(os.environ["RENPY_SEARCHPATH"].split("::"))

    if renpy.android:
        renpy.config.searchpath = [ ]
        renpy.config.commondir = None

        if "ANDROID_PUBLIC" in os.environ:
            android_game = os.path.join(os.environ["ANDROID_PUBLIC"], "game")

            print("Android searchpath: ", android_game)

            if os.path.exists(android_game):
                renpy.config.searchpath.insert(0, android_game)

    # Load Ren'Py extensions.
    for dir in renpy.config.searchpath: # @ReservedAssignment
        for fn in os.listdir(dir):
            if fn.lower().endswith(".rpe"):
                load_rpe(dir + "/" + fn)

    # Generate a list of extensions for each archive handler.
    archive_extensions = [ ]
    for handler in renpy.loader.archive_handlers:
        for ext in handler.get_supported_extensions():
            if not (ext in archive_extensions):
                archive_extensions.append(ext)

    # The basename is the final component of the path to the gamedir.
    for i in sorted(os.listdir(renpy.config.gamedir)):
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

    log_clock("Loader init")

    # Initialize the log.
    game.log = renpy.python.RollbackLog()

    # Initialize the store.
    renpy.store.store = sys.modules['store']

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
        renpy.game.args.compile = True

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
    if (renpy.game.args.command == 'compile') and not (renpy.game.args.keep_orphan_rpyc): # @UndefinedVariable

        for (fn, dn) in renpy.game.script.script_files:

            if dn is None:
                continue

            if not os.path.isfile(os.path.join(dn, fn + ".rpy")):

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

    if renpy.game.args.command == 'load-test': # @UndefinedVariable
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
        renpy.config.savedir = __main__.path_to_saves(renpy.config.gamedir) # E1101 @UndefinedVariable

    if renpy.game.args.savedir: # @UndefinedVariable
        renpy.config.savedir = renpy.game.args.savedir # @UndefinedVariable

    # Init preferences.
    game.persistent = renpy.persistent.init()
    game.preferences = game.persistent._preferences

    for i in renpy.game.persistent._seen_translates: # @UndefinedVariable
        if i in renpy.game.script.translator.default_translates:
            renpy.game.seen_translates_count += 1

    if game.persistent._virtual_size:
        renpy.config.screen_width, renpy.config.screen_height = game.persistent._virtual_size

    # Init save locations and loadsave.
    renpy.savelocation.init()

    # We need to be 100% sure we kill the savelocation thread.
    try:

        # Init save slots.
        renpy.loadsave.init()

        log_clock("Loading save slot metadata.")

        # Load persistent data from all save locations.
        renpy.persistent.update()
        game.preferences = game.persistent._preferences
        log_clock("Loading persistent")

        # Clear the list of seen statements in this game.
        game.seen_session = { }

        # Initialize persistent variables.
        renpy.store.persistent = game.persistent
        renpy.store._preferences = game.preferences
        renpy.store._test = renpy.test.testast._test

        if renpy.parser.report_parse_errors():
            raise renpy.game.ParseErrorException()

        renpy.game.exception_info = 'While executing init code:'

        for _prio, node in game.script.initcode:

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

        renpy.game.script.report_duplicate_labels()

        # Sort the images.
        renpy.display.image.image_names.sort()

        game.persistent._virtual_size = renpy.config.screen_width, renpy.config.screen_height

        log_clock("Running init code")

        renpy.pyanalysis.load_cache()
        log_clock("Loading analysis data")

        # Analyze the script and compile ATL.
        renpy.game.script.analyze()
        renpy.atl.compile_all()
        log_clock("Analyze and compile ATL")

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
        log_clock("Dump and make backups.")

        # Initialize image cache.
        renpy.display.im.cache.init()
        log_clock("Cleaning cache")

        # Make a clean copy of the store.
        renpy.python.make_clean_stores()
        log_clock("Making clean stores")

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

        log_clock("Initial gc.")

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
                    renpy.persistent.update(True)
                    renpy.persistent.save_MP()

            except game.FullRestartException as e:
                restart = e.reason

            finally:

                # Reset live2d if it exists.
                try:
                    renpy.gl2.live2d.reset_states()
                except:
                    pass

                # Flush any pending interface work.
                renpy.display.interface.finish_pending()

                # Give Ren'Py a couple of seconds to finish saving.
                renpy.loadsave.autosave_not_running.wait(3.0)

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
