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




# New context stuff.
call_in_new_context = renpy.game.call_in_new_context
curried_call_in_new_context = renpy.curry.curry(call_in_new_context)
invoke_in_new_context = renpy.game.invoke_in_new_context
curried_invoke_in_new_context = renpy.curry.curry(invoke_in_new_context)
call_replay = renpy.game.call_replay

renpy_pure("curried_call_in_new_context")
renpy_pure("curried_invoke_in_new_context")


def scry():
    """
    :doc: other

    Returns the scry object for the current statement. Returns None if
    there are no statements executing.

    The scry object tells Ren'Py about things that must be true in the
    future of the current statement. Right now, the scry object has the
    following fields:

    `nvl_clear`
        Is true if an ``nvl clear`` statement will execute before the
        next interaction.

    `say`
        Is true if an ``say`` statement will execute before the
        next interaction.

    `menu_with_caption`
        Is true if a ``menu`` statement with a caption will execute
        before the next interaction.

    `who`
        If a ``say`` or ``menu-with-caption`` statement will execute
        before the next interaction, this is the character object it will use.

    The scry object has a next() method, which returns the scry object of
    the statement after the current one, if only one statement will execute
    after the this one. Otherwise, it returns None.

    .. warning::

        Like other similar functions, the object this returns is meant to be used
        in the short term after the function is called. Including it in save data
        or making it participate in rollback is not advised.
    """

    name = renpy.game.context().current

    if name is None:
        return None

    node = renpy.game.script.lookup(name)
    return node.scry()


def pop_call():
    """
    :doc: label
    :name: renpy.pop_call

    Pops the current call from the call stack, without returning to the
    location. Also reverts the values of :func:`dynamic <renpy.dynamic>`
    variables, the same way the Ren'Py return statement would.

    This can be used if a label that is called decides not to return
    to its caller.
    """

    renpy.game.context().pop_call()


pop_return = pop_call


def call_stack_depth():
    """
    :doc: label

    Returns the depth of the call stack of the current context - the number
    of calls that have run without being returned from or popped from the
    call stack.
    """

    return len(renpy.game.context().return_stack)


def game_menu(screen=None):
    """
    :undocumented: Probably not what we want in the presence of
    screens.
    """

    if screen is None:
        call_in_new_context("_game_menu")
    else:
        call_in_new_context("_game_menu", _game_menu_screen=screen)


def mode(mode):
    """
    :undocumented:

    Causes Ren'Py to enter the named mode, or stay in that mode if it's
    already in it.
    """

    ctx = renpy.game.context()

    if not ctx.use_modes:
        return

    modes = ctx.modes

    try:
        ctx.use_modes = False

        if mode != modes[0]:
            for c in renpy.config.mode_callbacks:
                c(mode, modes)

    finally:
        ctx.use_modes = True

    if mode in modes:
        modes.remove(mode)

    modes.insert(0, mode)


def get_mode():
    """
    :doc: modes

    Returns the current mode, or None if it is not defined.
    """

    ctx = renpy.game.context()

    if not ctx.use_modes:
        return None

    modes = ctx.modes

    return modes[0]


def end_replay():
    """
    :doc: replay

    If we're in a replay, ends the replay immediately. Otherwise, does
    nothing.
    """

    if renpy.store._in_replay:
        raise renpy.game.EndReplay()


def get_return_stack():
    """
    :doc: label

    Returns a list giving the current return stack. The return stack is a
    list of statement names.

    The statement names will be strings (for labels), or opaque tuples (for
    non-label statements).
    """

    return renpy.game.context().get_return_stack()


def set_return_stack(stack):
    """
    :doc: label

    Sets the current return stack. The return stack is a list of statement
    names.

    Statement names may be strings (for labels) or opaque tuples (for
    non-label statements).

    The most common use of this is to use::

        renpy.set_return_stack([])

    to clear the return stack.
    """

    renpy.game.context().set_return_stack(stack)


def get_line_log():
    """
    :undocumented:

    Returns the list of lines that have been shown since the last time
    :func:`renpy.clear_line_log` was called.
    """

    return renpy.game.context().line_log[:]


def clear_line_log():
    """
    :undocumented:

    Clears the line log.
    """

    renpy.game.context().line_log = [ ]


def get_skipping():
    """
    :doc: other

    Returns "slow" if the Ren'Py is skipping, "fast" if Ren'Py is fast skipping,
    and None if it is not skipping.
    """

    return renpy.config.skipping


def is_skipping():
    """
    :doc: other

    Returns True if Ren'Py is currently skipping (in fast or slow skip mode),
    or False otherwise.
    """

    return not not renpy.config.skipping


def stop_skipping():
    """
    :doc: other

    Stops skipping, if Ren'Py is currently skipping.
    """

    renpy.config.skipping = None


def is_init_phase():
    """
    :doc: other

    Returns True if Ren'Py is currently executing init code, or False otherwise.
    """

    return renpy.game.context().init_phase


def add_to_all_stores(name, value):
    """
    :doc: other

    Adds the `value` by the `name` to all creator defined namespaces. If the name
    already exist in that namespace - do nothing for it.

    This function may only be run from inside an init block. It is an
    error to run this function once the game has started.
    """

    if not is_init_phase():
        raise Exception("add_to_all_stores is only allowed in init code.")

    for _k, ns in renpy.python.store_dicts.items():

        if name not in ns:
            ns[name] = value


def clear_game_runtime():
    """
    :doc: other

    Resets the game runtime counter.
    """

    renpy.game.contexts[0].runtime = 0


def get_game_runtime():
    """
    :doc: other

    Returns the game runtime counter.

    The game runtime counter counts the number of seconds that have
    elapsed while waiting for user input in the top-level context.
    (It does not count time spent in the main or game menus.)
    """

    return renpy.game.contexts[0].runtime
