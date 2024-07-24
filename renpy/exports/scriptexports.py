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
    rv = [ ]

    for i in renpy.game.script.namemap:
        if isinstance(i, basestring):
            rv.append(i)

    return renpy.revertable.RevertableSet(rv)


@renpy_pure
def munged_filename():
    return renpy.lexer.munge_filename(renpy.exports.get_filename_line()[0])


loaded_modules = set()


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

    old_locked = renpy.config.locked
    renpy.config.locked = False

    initcode = renpy.game.script.load_module(name)

    context = renpy.execution.Context(False)
    context.init_phase = True
    renpy.game.contexts.append(context)

    context.make_dynamic(kwargs)
    renpy.store.__dict__.update(kwargs) # @UndefinedVariable

    for _prio, node in initcode: # @UnusedVariable
        if isinstance(node, renpy.ast.Node):
            renpy.game.context().run(node)
        else:
            node()

    context.pop_all_dynamic()

    renpy.game.contexts.pop()

    renpy.config.locked = old_locked


def load_string(s, filename="<string>"):
    """
    :doc: other

    Loads `s` as Ren'Py script that can be called.

    Returns the name of the first statement in s.

    `filename` is the name of the filename that statements in the string will
    appear to be from.
    """

    old_exception_info = renpy.game.exception_info

    try:

        old_locked = renpy.config.locked
        renpy.config.locked = False

        stmts, initcode = renpy.game.script.load_string(filename, str(s))

        if stmts is None:
            return None

        context = renpy.execution.Context(False)
        context.init_phase = True
        renpy.game.contexts.append(context)

        for _prio, node in initcode:
            if isinstance(node, renpy.ast.Node):
                renpy.game.context().run(node)
            else:
                node()

        context.pop_all_dynamic()
        renpy.game.contexts.pop()

        renpy.config.locked = old_locked

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

        old_locked = renpy.config.locked
        renpy.config.locked = False

        renpy.game.script.load_languages.add(language)

        initcode = renpy.game.script.load_script()

        context = renpy.execution.Context(False)
        context.init_phase = True
        renpy.game.contexts.append(context)

        for _prio, node in initcode:
            if isinstance(node, renpy.ast.Node):
                renpy.game.context().run(node)
            else:
                node()

        context.pop_all_dynamic()
        renpy.game.contexts.pop()

        renpy.config.locked = old_locked

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
