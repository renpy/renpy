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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals # type: ignore
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import renpy
from renpy.exports.commonexports import renpy_pure


def full_restart(transition=False, label="_invoke_main_menu", target="_main_menu", save=False):
    """
    :doc: other
    :args: (transition=False, *, save=False)

    Causes Ren'Py to restart, returning the user to the main menu.

    `transition`
        If given, the transition to run, or None to not run a transition.
        False uses :var:`config.end_game_transition`.

    `save`
        If true, the game is saved in :var:`_quit_slot` before Ren'Py
        restarts and returns the user to the main menu.
    """

    if save and (renpy.store._quit_slot is not None):
        renpy.loadsave.save(renpy.store._quit_slot, getattr(renpy.store, "save_name", ""))

    if transition is False:
        transition = renpy.config.end_game_transition

    raise renpy.game.FullRestartException((transition, label, target)) # type: ignore


def utter_restart(keep_renderer=False):
    """
    :undocumented: Used in the implementation of shift+R.

    Causes an utter restart of Ren'Py. This reloads the script and
    re-runs initialization.
    """

    renpy.session["_keep_renderer"] = keep_renderer

    raise renpy.game.UtterRestartException()


def reload_script():
    """
    :doc: reload

    Causes Ren'Py to save the game, reload the script, and then load the
    save.

    This should only be called during development. It works on Windows, macOS,
    and Linux, but may not work on other platforms.
    """

    # Avoid reloading in a replay.
    if renpy.store._in_replay:
        return

    s = renpy.exports.get_screen("menu")

    session = renpy.session
    session["_reload"] = True

    # If one of these variables is already in session, we're recovering from
    # a failed reload.
    if ("_reload_screen" in session) or ("_main_menu_screen" in session):
        utter_restart()

    if not renpy.store.main_menu:

        if s is not None:
            session["_reload_screen"] = s.screen_name[0]
            session["_reload_screen_args"] = s.scope.get("_args", ())
            session["_reload_screen_kwargs"] = s.scope.get("_kwargs", { })

        renpy.game.call_in_new_context("_save_reload_game")

    else:

        if s is not None:
            session["_main_menu_screen"] = s.screen_name[0]
            session["_main_menu_screen_args"] = s.scope.get("_args", ())
            session["_main_menu_screen_kwargs"] = s.scope.get("_kwargs", { })

        utter_restart()


def quit(relaunch=False, status=0, save=False): # @ReservedAssignment
    """
    :doc: other

    This causes Ren'Py to exit entirely.

    `relaunch`
        If true, Ren'Py will run a second copy of itself before quitting.

    `status`
        The status code Ren'Py will return to the operating system.
        Generally, 0 is success, and positive integers are failure.

    `save`
        If true, the game is saved in :var:`_quit_slot` before Ren'Py
        terminates.
    """

    if save and (renpy.store._quit_slot is not None):
        renpy.loadsave.save(renpy.store._quit_slot, getattr(renpy.store, "save_name", ""))

    if renpy.exports.has_label("quit"):
        renpy.exports.call_in_new_context("quit")

    raise renpy.game.QuitException(relaunch=relaunch, status=status)


def set_autoreload(autoreload):
    """
    :doc: reload

    Sets the autoreload flag, which determines if the game will be
    automatically reloaded after file changes. Autoreload will not be
    fully enabled until the game is reloaded with :func:`renpy.reload_script`.
    """

    renpy.autoreload = autoreload


def get_autoreload():
    """
    :doc: reload

    Gets the autoreload flag.
    """

    return renpy.autoreload
