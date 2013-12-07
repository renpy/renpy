.. _statement-equivalents:

=====================
Statement Equivalents
=====================

To allow Ren'Py to be scripted in python, each Ren'Py statement has
equivalent Python code. This usually consists of a Python function,
but may also consist of a code pattern that performs an action
equivalent to the statement.


Dialogue
========

The Ren'Py say statement is equivalent to calling the character object
as a function. The following code displays the same line twice::

    e "Hello, world."

    $ e("Hello, world.")

Displaying narration can be done the same way, by using the
``narrator`` character. When calling a character, it's possible to
supply the keyword argument `interact`. When interact is false,
Ren'Py will display the character dialogue box, and will then
return before performing an interaction.

This equivalence of characters and function objects works in the other
direction as well. It is possible to declare a python function, and
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

The menu statement has an equivalent Python function.

.. include:: inc/se_menu


Displaying Images
=================

The image, scene, show, and hide statements each have an equivalent
python function.

.. include:: inc/se_images

Transitions
===========

The equivalent of the with statement is the renpy.with_statement
function.

.. include:: inc/se_with

Jump
====

The equivalent of the jump statement is the renpy.jump function.

.. include:: inc/se_jump

Call
====

The equivalent of the call statement is the renpy.call function.

.. include:: inc/se_call
