.. _statement-equivalents:

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
fluid.

Dialogue
========

The Ren'Py :ref:`say-statement` is equivalent to calling the character
object as a function. The following displays the same line twice::

    e "Hello, world."

    $ e("Hello, world.")

Displaying narration can be done the same way, by using the
``narrator`` character. When calling a character, it's possible to
supply the keyword argument ``interact``. When ``interact`` is False,
Ren'Py will display the character dialogue box, and will then
return before performing an interaction.

This equivalence of characters and function objects works in the other
direction as well. It is possible to declare a Python function, and
then use that function in the place of a character object. For
example, the following function uses a variable to choose between
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
allow the game to continue working if Ren'Py adds additional keyword
arguments to character calls.

.. include:: inc/se_say

Choice Menus
============

The :ref:`menu statement <menus>` has an equivalent Python function.

.. include:: inc/se_menu


Displaying Images
=================

The image, scene, show, and hide statements each have an equivalent
Python function (see :ref:`displaying-images` for the original statements).

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
