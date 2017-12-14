.. _gui-advanced:

============
Advanced GUI
============

This section has some odds and ends about advanced usage of the gui.


Python Functions
================

There are some Python functions that support the GUI.

.. include:: inc/gui


More on gui.rebuild
--------------------

The gui.rebuild function is a rather slow function that updates the GUI
to reflect the current state of Ren'Py. What it does is:

* Re-runs all of the define statements that define variables in the gui
  namespace.
* Re-runs all of the translate python blocks for the current language.
* Re-runs all of the style statements.
* Rebuilds all of the styles in the system.

Note that init python blocks are not re-run on gui.rebuild. In this way, ::

    define gui.text_size = persistent.text_size

and::

    init python:
        gui.text_size = persistent.text_size

are different.

The default statement, the gui namespace, and gui.rebuild
---------------------------------------------------------

The default statement has changed semantics when applied to the gui
namespace. When applied to a variable in the gui namespace, the
default statement runs interleaved with the define statement, and
the default statements are not re-run when gui.rebuild is called.

What this means is that if we have::

    default gui.accent_color = "#c04040"
    define gui.hover_color = gui.accent_color

The first time the game is run, the accent color will be set, and then
the hover color will be set to the accent color. (Both are then used to
set various style colors.)

However, if as part of the game script, we have::

    $ gui.accent_color = "#4040c0"
    $ gui.rebuild()

Ren'Py will only re-run the define, so it will set the hover color to
the accent color, and then update the styles. This makes it possible
to have parts of the gui that change as the game progresses.


