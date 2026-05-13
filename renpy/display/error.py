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

# This file contains code to handle GUI-based error reporting.

import os

import renpy

error_handled = False

##############################################################################
# Initialized approach.


def call_exception_screen(screen_name, **kwargs):
    old_quit = renpy.config.quit_action

    try:
        renpy.config.quit_action = renpy.exports.quit

        for i in renpy.config.layers:
            renpy.game.context().scene_lists.clear(i)

        renpy.exports.show_screen(screen_name, _transient=True, **kwargs)
        return renpy.ui.interact(mouse="screen", type="screen", suppress_overlay=True, suppress_underlay=True)

    finally:
        renpy.config.quit_action = old_quit


def rollback_action():
    renpy.exports.rollback(force=True)


def init_display():
    """
    The minimum amount of code required to init the display.
    """

    # Ensure we have correctly-typed preferences.
    renpy.game.preferences.check()

    if renpy.config.init_system_styles is not None:
        renpy.config.init_system_styles()

    if not renpy.game.interface:
        renpy.display.core.Interface()
        renpy.loader.index_files()
        renpy.display.im.cache.init()

    renpy.game.interface.start()

    renpy.ui.reset()


def error_dump():
    """
    Handles dumps in the case where an error occurs.
    """

    renpy.dump.dump(True)


def report_exception(traceback_exception: renpy.error.TracebackException) -> bool:
    """
    Reports an exception to the user. Returns True if the exception should
    be raised by the normal reporting mechanisms. Otherwise, should raise
    the appropriate exception to cause a reload or quit or rollback.
    """

    global error_handled
    error_handled = True

    error_dump()

    if renpy.game.args.command != "run":
        return True

    if "RENPY_SIMPLE_EXCEPTIONS" in os.environ:
        return True

    if not renpy.exports.has_screen("_exception"):
        return True

    try:
        init_display()
    except Exception:
        return True

    if renpy.display.draw is None:
        return True

    ignore_action = None
    rollback_action = None
    reload_action = None

    renpy.store.te = traceback_exception

    try:
        if not renpy.game.context().init_phase:
            if renpy.config.rollback_enabled:
                rollback_action = renpy.display.error.rollback_action

            reload_action = renpy.exports.curried_call_in_new_context("_save_reload_game")

        else:
            reload_action = renpy.exports.utter_restart

        # If next node is known, allow to advance to it.
        if renpy.game.context().next_node is not None:
            ignore_action = renpy.ui.returns(False)

    except Exception:
        pass

    renpy.game.invoke_in_new_context(
        call_exception_screen,
        "_exception",
        traceback_exception=traceback_exception,
        rollback_action=rollback_action,
        reload_action=reload_action,
        ignore_action=ignore_action,
    )

    # Don't report images that failed to load.
    renpy.display.im.ignored_images |= renpy.display.im.images_to_ignore
    renpy.config.raise_image_exceptions = False
    renpy.config.raise_image_load_exceptions = False

    # If creator overrides ignore action, run it.
    if renpy.store._ignore_action is not None:
        renpy.display.behavior.run(renpy.store._ignore_action)

    return False


def report_parse_errors(errors: list[str], error_fn: str) -> bool:
    """
    Reports an exception to the user. Returns True if the exception should
    be raised by the normal reporting mechanisms. Otherwise, should raise
    the appropriate exception.
    """

    global error_handled
    error_handled = True

    error_dump()

    if renpy.game.args.command != "run":
        return True

    if "RENPY_SIMPLE_EXCEPTIONS" in os.environ:
        return True

    if not renpy.exports.has_screen("_parse_errors"):
        return True

    # ParseError before finishing loading the script
    if renpy.config.savedir is None:
        return True

    init_display()

    reload_action = renpy.exports.utter_restart

    try:
        renpy.game.invoke_in_new_context(
            call_exception_screen,
            "_parse_errors",
            reload_action=reload_action,
            errors=errors,
            error_fn=error_fn,
        )

    except renpy.game.CONTROL_EXCEPTIONS:
        raise

    except Exception:
        renpy.display.log.write("While handling exception:")
        renpy.display.log.exception()
        raise

    return False
