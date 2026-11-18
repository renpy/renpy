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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals  # type: ignore
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode  # *

import contextlib

import renpy
from renpy.exports.commonexports import renpy_pure


@renpy_pure
def has_label(name):
    """
    :doc: label

    Returns true if `name` is a valid label in the program, or false
    otherwise.

    `name`
        Should be a string to check for the existence of a label. It can
        also be an opaque tuple giving the name of a non-label statement.
    """

    return renpy.game.script.has_label(name)


@renpy_pure
def get_all_labels():
    """
    :doc: label

    Returns the set of all labels defined in the program, including labels
    defined for internal use in the libraries.
    """
    rv = []

    for i in renpy.game.script.namemap.values():
        if isinstance(i.name, str):
            rv.append(i.name)

    return renpy.revertable.RevertableSet(rv)


@renpy_pure
def munged_filename():
    return renpy.lexer.munge_filename(renpy.exports.get_filename_line()[0])


loaded_modules = set()


@contextlib.contextmanager
def unlocked_config():
    """
    Unlocks the config for the duration of the block, restoring the previous state
    even if the block raises.
    """

    old_locked = renpy.config.locked
    renpy.config.locked = False

    try:
        yield
    finally:
        renpy.config.locked = old_locked


def run_initcode(initcode, kwargs=None):
    """
    Runs the (priority, node) pairs in `initcode` in a new init-phase context. If `kwargs` is given,
    it's set in the store for the duration of the run. The context is removed even if an init
    statement raises.
    """

    context = renpy.execution.Context(False)
    context.init_phase = True
    renpy.game.contexts.append(context)

    try:
        if kwargs is not None:
            context.make_dynamic(kwargs)
            renpy.store.__dict__.update(kwargs)

        for _prio, node in initcode:
            node.execute_init()

    finally:
        context.pop_all_dynamic()
        renpy.game.contexts.pop()


def load_module(name, **kwargs):
    """
    :doc: other
    :args: (name)

    This loads the Ren'Py module named name. A Ren'Py module consists of Ren'Py script
    that is loaded into the usual (store) namespace, contained in a file named
    name.rpym or name.rpymc. If a .rpym file exists, and is newer than the
    corresponding .rpymc file, it is loaded and a new .rpymc file is created.

    All of the init blocks (and other init-phase code) in the module are run
    before this function returns. An error is raised if the module name cannot
    be found, or is ambiguous.

    Module loading may only occur from inside an init block.
    """

    if not renpy.game.context().init_phase:
        raise Exception("Module loading is only allowed in init code.")

    if name in loaded_modules:
        return

    loaded_modules.add(name)

    with unlocked_config():
        initcode = renpy.game.script.load_module(name)
        run_initcode(initcode, kwargs)


def load_string(s, filename="<string>"):
    """
    :doc: other

    Loads `s` as Ren'Py script that can be called.

    Returns the name of the first statement in `s`, which can be passed to
    :func:`renpy.call`, :func:`renpy.jump`, or the call and jump statements.
    The script is added to the running game and is not saved in any .rpyc file.

    If `s` contains parse errors, nothing is loaded and this returns None. No
    exception is raised in this case. The errors can be retrieved with
    :func:`renpy.get_parse_errors`.

    Init-phase statements in `s`, such as ``define``, ``default``, and
    ``init python``, are run before this function returns.

    This raises ValueError if `s` contains no statements.

    `filename`
        The name of the file that statements in the string will appear to be
        from.
    """

    old_exception_info = renpy.game.exception_info

    try:
        with unlocked_config():
            stmts, initcode = renpy.game.script.load_string(filename, str(s))

            if stmts is None:
                return None

            if not stmts:
                raise ValueError("The string passed to renpy.load_string contains no statements.")

            run_initcode(initcode)

        renpy.game.script.analyze()

        return stmts[0].name

    finally:
        renpy.game.exception_info = old_exception_info


def load_language(language):
    """
    :undocumented:

    (Here because of commonality with load_string and load_module.)

    Load the script files in tl/language, if not loaded. Runs any
    init code found during the process.
    """

    if language is None:
        return

    if not renpy.config.defer_tl_scripts:
        return

    if language in renpy.game.script.load_languages:
        return

    old_exception_info = renpy.game.exception_info

    try:
        with unlocked_config():
            renpy.game.script.load_languages.add(language)

            initcode = renpy.game.script.load_script()
            run_initcode(initcode)

        if not renpy.game.context().init_phase:
            renpy.game.script.analyze()

        renpy.game.script.update_bytecode()

    finally:
        renpy.game.exception_info = old_exception_info


def include_module(name):
    """
    :doc: other

    Similar to :func:`renpy.load_module`, but instead of loading the module right away,
    inserts it into the init queue somewhere after the current AST node.

    The module may not contain init blocks lower than the block that includes the module.
    For example, if your module contains an init 10 block, the latest you can load it is
    init 10.

    Module loading may only occur from inside an init block.
    """

    if not renpy.game.context().init_phase:
        raise Exception("Module loading is only allowed in init code.")

    renpy.game.script.include_module(name)
