# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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

import renpy.display
import renpy.game as game
import os
import sys
import time
import zipfile
import __main__


def run(restart):
    """
    This is called during a single run of the script. Restarting the script
    will cause this to change.
    """

    # Reset the store to a clean version of itself.
    renpy.python.clean_stores()

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

    # Perhaps warp.
    warp_label = renpy.warp.warp()

    if warp_label is not None:

        game.context().goto_label(warp_label)

        if game.script.has_label('after_warp'):
            game.context().call('after_warp')

        renpy.config.skipping = None

    try:
        renpy.exports.log("--- " + time.ctime())
        renpy.exports.log("")
    except:
        pass

    # Note if this is a restart.
    renpy.store._restart = restart

    # We run until we get an exception.
    renpy.display.interface.enter_context()
    renpy.execution.run_context(True)


def load_rpe(fn):

    zfn = zipfile.ZipFile(fn)
    autorun = zfn.read("autorun.py")
    zfn.close()

    sys.path.insert(0, fn)
    exec autorun in dict()

def choose_variants():

    if "RENPY_VARIANT" in os.environ:
        renpy.config.variants = list(os.environ["RENPY_VARIANT"].split()) + [ None ]
        return

    renpy.config.variants = [ None ]

    if renpy.android: #@UndefinedVariable

        renpy.config.variants.insert(0, 'android')

        import android #@UnresolvedImport
        import math
        import pygame

        from jnius import autoclass  # @UnresolvedImport

        # Are we running on an OUYA?
        try:
            OuyaFacade = autoclass("tv.ouya.console.api.OuyaFacade")
            of = OuyaFacade.getInstance()

            if of.isRunningOnOUYAHardware():
                print "Running on an OUYA."
                renpy.config.variants.insert(0, "ouya")
        except:
            pass

        # Are we running on OUYA or Google TV or something similar?
        PythonActivity = autoclass('org.renpy.android.PythonActivity')
        mActivity = PythonActivity.mActivity
        package_manager = mActivity.getPackageManager()

        if package_manager.hasSystemFeature("android.hardware.type.television"):
            print "Running on a television."
            renpy.config.variants.insert(0, "tv")
            renpy.config.variants.insert(0, "small")
            return

        # Otherwise, a phone or tablet.
        renpy.config.variants.insert(0, 'touch')

        pygame.display.init()

        info = pygame.display.Info()
        diag = math.hypot(info.current_w, info.current_h) / android.get_dpi()
        print "Screen diagonal is", diag, "inches."

        if diag >= 6:
            renpy.config.variants.insert(0, 'tablet')
            renpy.config.variants.insert(0, 'medium')
        else:
            renpy.config.variants.insert(0, 'phone')
            renpy.config.variants.insert(0, 'small')

    else:
        renpy.config.variants.insert(0, 'pc')
        renpy.config.variants.insert(0, 'large')


def main():

    renpy.game.exception_info = 'Before loading the script.'

    # Get ready to accept new arguments.
    renpy.arguments.pre_init()

    # Init the config after load.
    renpy.config.init()

    # Set up variants.
    choose_variants()
    renpy.display.touch = "touch" in renpy.config.variants


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

    if renpy.android:
        renpy.config.searchpath = [ ]
        renpy.config.commondir = None

    # Load Ren'Py extensions.
    for dir in renpy.config.searchpath: #@ReservedAssignment
        for fn in os.listdir(dir):
            if fn.lower().endswith(".rpe"):
                load_rpe(dir + "/" + fn)


    # The basename is the final component of the path to the gamedir.
    for i in sorted(os.listdir(renpy.config.gamedir)):

        if not i.endswith(".rpa"):
            continue

        i = i[:-4]
        renpy.config.archives.append(i)

    renpy.config.archives.reverse()

    # Initialize archives.
    renpy.loader.index_archives()

    # Initialize the log.
    game.log = renpy.python.RollbackLog()

    # Initialize the store.
    renpy.store.store = sys.modules['store']

    # Set up styles.
    renpy.style.reset()
    game.style = renpy.style.StyleManager()
    renpy.store.style = game.style

    # Run init code in its own context. (Don't log.)
    game.contexts = [ renpy.execution.Context(False) ]
    game.contexts[0].init_phase = True

    # Load the script.
    renpy.game.exception_info = 'While loading the script.'
    renpy.game.script = renpy.script.Script()

    # Set up error handling.
    renpy.exports.load_module("_errorhandling")
    renpy.style.build_styles()

    # Load all .rpy files.
    renpy.game.script.load_script() # sets renpy.game.script.

    renpy.game.exception_info = 'After loading the script.'

    # Find the save directory.
    if renpy.config.savedir is None:
        renpy.config.savedir = __main__.path_to_saves(renpy.config.gamedir) # E1101 @UndefinedVariable

    if renpy.game.args.savedir: #@UndefinedVariable
        renpy.config.savedir = renpy.game.args.savedir #@UndefinedVariable

    # Init preferences.
    game.persistent = renpy.persistent.init()
    game.preferences = game.persistent._preferences

    # Init save locations.
    renpy.savelocation.init()

    # We need to be 100% sure we kill the savelocation thread.
    try:

        # Load persistent data from all save locations.
        renpy.persistent.update()

        # Clear the list of seen statements in this game.
        game.seen_session = { }

        # Initialize persistent variables.
        renpy.store.persistent = game.persistent
        renpy.store._preferences = game.preferences

        if renpy.parser.report_parse_errors():
            raise renpy.game.ParseErrorException()

        renpy.game.exception_info = 'While executing init code:'

        for _prio, node in game.script.initcode:
            game.context().run(node)

        renpy.game.exception_info = 'After initialization, but before game start.'

        # Save the bytecode in a cache.
        renpy.game.script.save_bytecode()

        # Check if we should simulate android.
        renpy.android = renpy.android or renpy.config.simulate_android #@UndefinedVariable

        # Run the post init code, if any.
        for i in renpy.game.post_init:
            i()

        # Init translation.
        renpy.translation.init_translation()

        # Rebuild the various style caches.
        renpy.style.build_styles()

        # Index the archive files. We should not have loaded an image
        # before this point. (As pygame will not have been initialized.)
        # We need to do this again because the list of known archives
        # may have changed.
        renpy.loader.index_archives()

        # Check some environment variables.
        renpy.game.less_memory = "RENPY_LESS_MEMORY" in os.environ
        renpy.game.less_mouse = "RENPY_LESS_MOUSE" in os.environ
        renpy.game.less_updates = "RENPY_LESS_UPDATES" in os.environ

        renpy.dump.dump(False)

        # Handle arguments and commands.
        if not renpy.arguments.post_init():
            return

        # Remove the list of all statements from the script.
        game.script.all_stmts = None

        # Make a clean copy of the store.
        renpy.python.make_clean_stores()

        # Initialize image cache.
        renpy.display.im.cache.init()

        # (Perhaps) Initialize graphics.
        if not game.interface:
            renpy.display.core.Interface()

        # Start things running.
        restart = None

        renpy.game.exception_info = 'While running game code:'
        renpy.first_utter_start = False


        while True:

            if restart:
                renpy.display.screen.before_restart()

            try:
                try:
                    run(restart)
                finally:
                    restart = (renpy.config.end_game_transition, "_invoke_main_menu", "_main_menu")
                    renpy.persistent.update(True)

            except game.FullRestartException, e:
                restart = e.reason

            finally:

                # Flush any pending interface work.
                renpy.display.interface.finish_pending()

                # Give Ren'Py a couple of seconds to finish saving.
                renpy.loadsave.autosave_not_running.wait(3.0)

    finally:

        renpy.savelocation.quit()
        renpy.translation.write_updated_strings()

    # This is stuff we do on a normal, non-error return.
    if not renpy.display.error.error_handled:
        renpy.display.render.check_at_shutdown()

