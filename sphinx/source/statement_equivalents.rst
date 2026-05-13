=====================
Statement Equivalents
=====================

To allow Ren'Py to be scripted in Python, each Ren'Py statement has
a Python equivalent. This usually consists of a Python function,
but may also consist of a pattern of Python calls that perform an action
equivalent to the statement.

Note that using statement equivalents in lieu of the original statements
usually removes any possible :ref:`lint` checks and prediction
optimizations, making your game less easily checkable and possibly less
fluid. It can also disable features in certain cases.

Dialogue
========

.. warning::

    Several features, such as skipping already-seen dialogues, are not
    available using the python version and only enabled when using the native
    say statement.

The Ren'Py :ref:`say-statement` is equivalent to calling the character
object (when any is present) as a function. Displaying narration (meaning when
no character is supplied) can be done the same way, by using the ``narrator``
character. ::

    e "Hello, world."
    $ e("Hello, world.")

    "And then the sun exploded."
    $ narrator("And then the sun exploded.")

.. _say-proxy:

Proxy functions
---------------

This equivalence of characters and function objects works in the other
direction as well. It is possible to declare a Python function, and
then use that function in the place of a character object in a native say statement.
For example, the following function uses a variable to choose between
two characters. ::

    define lucy_normal = Character("Lucy")
    define lucy_evil = Character("Evil Lucy")

    init python:

        def l(what, **kwargs):
            if lucy_is_evil:
                lucy_evil(what, **kwargs)
            else:
                lucy_normal(what, **kwargs)

    label start:

        $ lucy_is_evil = False

        l "Usually, I feel quite normal."

        $ lucy_is_evil = True

        l "But sometimes, I get really mad!"

A function used in this way should either ignore unknown keyword
arguments, or pass them to a character function. Doing this will
allow the game to continue working if future versions of Ren'Py add additional
keyword arguments to character calls.

Note that unlike other possible arguments, ``interact=True`` will always be
passed to the function - unless manually passing ``(interact=False)``. A
:ref:`say-with-arguments` sees the arguments (including the supplementary
`interact`) passed to the function. For example::

    e "Hello, world." (what_size=32)

resolves to the following call::

    e("Hello, world.", what_size=32, interact=True)

Note that it's not required to pass ``interact=True`` when calling a Character
object for it to work as intended. The following works just as well::

    $ e("Hello, world.", what_size=32)

When e is a Character, this is further equivalent to::

    $ Character(kind=e, what_size=32)("Hello, world.")

But it's possible to use :var:`config.say_arguments_callback` or
have ``e`` wrap a character to do things differently.

There is one additional way of replacing the say statement using Python:

.. include:: inc/se_say

Dialogue Window Management
--------------------------

:ref:`Window management <dialogue-window-management>` is performed by setting
the :var:`_window` and :var:`_window_auto` variables, and by using the following
two functions:

.. include:: inc/window

Choice Menus
============

The :doc:`menu statement <menus>` has an equivalent Python function.

.. include:: inc/se_menu


Displaying Images
=================

The image, scene, show, and hide statements each have an equivalent
Python function (see :doc:`displaying_images` for the original statements).

.. include:: inc/se_images

Transitions
===========

The equivalent of the :ref:`with-statement` is the :func:`renpy.with_statement`
function.

.. include:: inc/se_with

Jump
====

The equivalent of the :ref:`jump-statement` is the :func:`renpy.jump` function.

.. include:: inc/se_jump

Call
====

The equivalent of the :ref:`call-statement` is the :func:`renpy.call` function.

.. include:: inc/se_call

Pause
=====

The equivalent of the :ref:`pause-statement` is the :func:`renpy.pause` function.

.. include:: inc/se_pause

Layeredimage
============

The :ref:`layeredimage-statement` statement has Python equivalents. The group
statement does not: the name of the group is supplied to :class:`Attribute`,
and the ``auto`` feature can be implemented using :func:`renpy.list_images`.

.. include:: inc/li
