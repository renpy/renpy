.. _gui-advanced:

============
Advanced GUI
============

This section has some odds and ends about advanced usage of the GUI.


Python Functions
================

There are some Python functions that support the GUI.

.. include:: inc/gui

.. function:: gui.button_text_properties(kind=None, accent=False):

    An obsolete alias for :func:`gui.text_properties`.

More on gui.rebuild
--------------------

The gui.rebuild function is a rather slow function that updates the GUI
to reflect the current state of Ren'Py. What it does is:

* Re-runs all of the ``define`` statements that define variables in the gui
  namespace.
* Re-runs all of the ``translate python`` blocks for the current language.
* Re-runs all of the ``style`` statements.
* Rebuilds all of the styles in the system.

Note that ``init python`` blocks are not re-run on ``gui.rebuild``. In this way, ::

    define gui.text_size = persistent.text_size

and::

    init python:
        gui.text_size = persistent.text_size

are different.

The default statement, the gui namespace, and gui.rebuild
---------------------------------------------------------

The ``default`` statement has changed semantics when applied to the ``gui``
namespace. When applied to a variable in the ``gui`` namespace, the
default statement runs interleaved with the define statement, and
the default statements are not re-run when :func:`gui.rebuild` is called.

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
to have parts of the GUI that change as the game progresses.

.. _gui-preferences:

GUI Preferences
===============

Ren'Py also supports a GUI preference system, consisting of a single function
and a pair of actions.

.. include:: inc/gui_preference

Example
-------

The GUI preference system is used by calling :func:`gui.preference` when defining
variables, with the name of the preference and the default value.
For example, one can use GUI preferences to define the text font and
size. ::

    define gui.text_font = gui.preference("font", "DejaVuSans.ttf")
    define gui.text_size = gui.preference("size", 22)

It's then possible to use the :class:`gui.SetPreference` and :class:`gui.TogglePreference`
actions to add change the values of the preferences. Here's some examples
that can be added to the preferences screen. ::

    vbox:
        style_prefix "check"
        label _("Options")
        textbutton _("OpenDyslexic") action gui.TogglePreference("font", "OpenDyslexic-Regular.otf", "DejaVuSans.ttf")

    vbox:
        style_prefix "radio"
        label _("Text Size")
        textbutton _("Small") action gui.SetPreference("size", 20)
        textbutton _("Medium") action gui.SetPreference("size", 22)
        textbutton _("Big") action gui.SetPreference("size", 24)
