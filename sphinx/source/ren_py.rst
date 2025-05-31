=================================
\_ren.py Files - Ren'Py in Python
=================================

In more complicated games, it's possible to have files that consist of mostly
Python, with a small number of Ren'Py statements, like ``init python:``, to
introduce the Python code to Ren'Py. Ren'Py has an alternative way to write
these Python-heavy files. Files with a name ending in ``_ren.py`` can be
written in Python syntax, which is then transformed to Ren'Py script and
processed.

There are two main reasons to take advantage of this:

* Using the \_ren.py syntax removes an extra layer of indentation that
  needs to be placed before every line of Python.
* Editors can open \_ren.py files using tools that are specialized for
  Python, allowing the editor to perform code analysis and refactoring
  operations that aren't available for Python-in-Ren'Py.

Ren'Py in Python files have names that end with \_ren.py, for example,
``actions_ren.py``. These files are processed in the same unicode order
that .rpy files are processed, so ``actions_ren.py`` is processed at the
same place that ``actions.rpy`` would have been. It's an error to have
both a \_ren.py and a .rpy file with the same root - for example,
``actions.rpy`` and ``actions_ren.py`` conflict, and will cause an
error if both exist in the same directory.

Syntax and Transformation
-------------------------

Ren'Py in Python files contain three types of sections.

* A single ignored section starts the file. This can be used for Python
  imports and other constructs that will help the editors and other tools,
  but aren't part of the game and will not be executed by Ren'Py.

* One or more Ren'Py sections, which contain Ren'Py script. Ren'Py script
  is generally used to introduce Python sections, and also sets the indentation
  of that Python.

  A Ren'Py section is introduced with ``"""renpy`` on a line by itself,
  and is terminated with ``"""`` on a line by itself. Both the start and
  the end need to be placed at the start of a line, without any indentation
  before it. If either is indented, the file will not be processed correctly.

* One or more Python sections. Python sections occur after Ren'Py sections,
  and are indented to the indentation level of the last non-whitespace, non-comment
  line in the Ren'Py section. If that line ends with a colon (:), the Python is
  indented by 4 more spaces.

This transformation is used to create the equivalent of a .rpy file in memory,
and this file is compiled in the usual way. Notably, Ren'Py in Python runs in the
Ren'Py store (rather than in an isolated module), and the Python code is subject
to the transformations that enable rollback and save/load to work - see
:doc:`python` and :ref:`rollback`.

Modular counterpart
-------
Replacing \_ren.py with \_rpym.py turns the regular script file into a loadable module.
So, if you want to load `path/to/some_module_rpym.py`, you can do it as follows::

    renpy.load_module('path/to/some_module') # _rpym.py suffix would be redundant

Example
-------

Here's an example of a \_ren.py file::

    # This is not included in the game. It's here so that an editor knows
    # the type of strength.
    strength = 100

    """renpy
    init python:
    """

    class BoostStrength(Action):
        """
        Boosts the strength of the player by 10.
        """

        def __call__(self):
            global strength
            strength += 10
            renpy.restart_interaction()

This file is transformed into (with some blank lines removed)::

    init python:

        class BoostStrength(Action):
            """
            Boosts the strength of the player by 10.
            """

            def __call__(self):
                global strength
                strength += 10
                renpy.restart_interaction()
