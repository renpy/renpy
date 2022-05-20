==================
Screens and Python
==================

Ren'Py supports defining screens in Python, as well as in the Ren'Py
screen language. A Python screen is created by supplying a screen
function to the :func:`renpy.define_screen` function. It can then
be used like it was any other screen.

The screen function should have parameters corresponding to the scope
variables it expects, and it should ignore extra keyword
arguments. (That is, it should have `**kwargs` at the end of its
parameter list.) It is then expected to call the UI functions to add
displayables to the screen.The screen function is called whenever an
interaction starts or restarts.

To ensure that this restarting is seamless to the user (and
not causing things to reset), it's important that every call to a UI
function supply the `id` argument. As a screen is re-created, Ren'Py
will update each displayable with the contents of the old displayable
with the same id. Ids are generated automatically by the screen
language, but when doing things by hand, they must be manually
specified.

.. warning::

    UI Functions are deprecated and not recommended.

Here's an example Python screen::

    init python:
        def say_screen(who, what, **kwargs):
            ui.window(id="window")
            ui.vbox(id="say_vbox")

            ui.text(who, id="who")
            ui.text(what, id="what")

            ui.close()

        renpy.define_screen("say", say_screen)



Screen Functions
================

The following functions support the definition, display, and hiding of
screens.

.. include:: inc/screens

UI Functions
============

.. note::

    The implementation of Ren'Py has changed, and UI functions that
    create displayables can now be far slower than their screen language
    equivalents.

The UI functions are Python equivalents of the screen language
statements. For each screen language statement, there is a ui function
with the same name. For example, ui.text corresponds to the text
statement, and ui.add corresponds to the add statement.

There is a simple mapping between screen language parameters and
arguments and Python arguments. Screen language parameters
become positional arguments, while properties become keyword
arguments. For example, the screen language statement: ::

   text "Hello, World" size 40 xalign 0.5

becomes: ::

   ui.text("Hello, World", size=40, xalign=0.5)

(It really should have an `id` parameter added.)

There are three groups of UI functions, corresponding to the number
of children they take.

.. When updating this list, be sure to update the documentation for
   the layout statement in screens.rst as well.

The following UI functions do not take any children.

* ui.add
* ui.bar
* ui.imagebutton
* ui.input
* ui.key
* ui.label
* ui.null
* ui.text
* ui.textbutton
* ui.timer
* ui.vbar
* ui.hotspot
* ui.hotbar
* ui.spritemanager

The following UI functions take a single child. They must be given
that child – use :func:`ui.null` if the child is missing.

* ui.button
* ui.frame
* ui.transform
* ui.window
* ui.drag

The following UI functions take multiple children. They continue
taking children until :func:`ui.close` is called.

* ui.fixed
* ui.grid
* ui.hbox
* ui.side
* ui.vbox
* ui.imagemap
* ui.draggroup

There are a few UI functions that do not correspond to screen language
statements, as they correspond to concepts that are not present in the
screen language.

.. include:: inc/ui
