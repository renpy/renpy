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

# This file contains support for a transition after a sequence of
# scene, show, and hide statements, with no intervening statements.

import renpy.exports as renpy
from renpy.defaultstore import config

# This should run after 00window.rpy, which might need to clear the
# flag.
"""renpy
init -1150 python:
"""

# Statements that are considered scene, show, or hide statements.
config.scene_show_hide_statements = [ "scene", "show", "hide" ]

# Statements that are considered with statements.
config.scene_show_hide_end_statements = [ "with", "window show", "window hide", "window auto" ]

# The transition to use after show, scene, and hide statements.
_scene_show_hide_transition = None

# Are we right after a show, scene, or hide statement?
_after_scene_show_hide = False


def _scene_show_hide_transition_callback(statement):
    """Runs the show, scene, and hide transition, if one is defined."""

    global _after_scene_show_hide

    if statement in config.scene_show_hide_statements:
        if renpy.get_filename_line()[0].startswith("renpy/common/"):
            return

        if renpy.context()._menu:
            return

        _after_scene_show_hide = True
        return

    if statement in config.scene_show_hide_end_statements:
        _after_scene_show_hide = False
        return

    if _after_scene_show_hide:
        _after_scene_show_hide = False

        if _scene_show_hide_transition and not renpy.game.after_rollback:
            renpy.with_statement(_scene_show_hide_transition)

        return


config.statement_callbacks.append(_scene_show_hide_transition_callback)
