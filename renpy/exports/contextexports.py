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


def context():
    """
    :doc: context

    Returns an object that is unique to the current context. The object
    is copied when entering a new context, but changes to the copy do
    not change the original.

    The object is saved and participates in rollback.
    """

    return renpy.game.context().info


def context_nesting_level():
    """
    :doc: context

    Returns the nesting level of the current context. This is 0 for the
    outermost context (the context that is saved, loaded, and rolled-back),
    and is non-zero in other contexts, such as menu and replay contexts.
    """

    return len(renpy.game.contexts) - 1


def jump_out_of_context(label):
    """
    :doc: context

    Causes control to leave the current context, and then to be
    transferred in the parent context to the given label.
    """

    raise renpy.game.JumpOutException(label)


def current_interact_type():
    return getattr(renpy.game.context().info, "_current_interact_type", None)


def last_interact_type():
    return getattr(renpy.game.context().info, "_last_interact_type", None)


def dynamic(*variables, **kwargs):
    """
    :doc: label

    This can be given one or more variable names as arguments. This makes the
    variables dynamically scoped to the current call. When the call returns, the
    variables will be reset to the value they had when this function was called.

    Variables in :ref:`named stores <named-stores>` are supported.

    If the variables are given as keyword arguments, the value of the argument
    is assigned to the variable name.

    Example calls are::

        $ renpy.dynamic("x", "y", "z")
        $ renpy.dynamic("mystore.serial_number")
        $ renpy.dynamic(players=2, score=0)
    """

    variables = variables + tuple(kwargs)
    renpy.game.context().make_dynamic(variables)

    for k, v in kwargs.items():
        setattr(renpy.store, k, v)


def context_dynamic(*variables):
    """
    :doc: context

    This can be given one or more variable names as arguments. This makes the
    variables dynamically scoped to the current context. When returning to the
    prior context, the variables will be reset to the value they had when this
    function was called.

    Variables in :ref:`named stores <named-stores>` are supported.

    Example calls are::

        $ renpy.context_dynamic("x", "y", "z")
        $ renpy.context_dynamic("mystore.serial_number")
    """

    renpy.game.context().make_dynamic(variables, context=True)
