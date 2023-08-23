=====================================
Screen Actions, Values, and Functions
=====================================

Ren'Py ships with a number of actions, values, and functions intended
for use with screens and the screen language.

Actions
=======

Actions are invoked when a button (including imagebuttons,
textbuttons, and hotspots) is activated, hovered, or
unhovered. Actions may determine when a button is selected or
insensitive.

Along with these actions, an action may be a function that does not
take any arguments. The function is called when the action is
invoked. If the action returns a value, then the value is returned
from an interaction.

A list of actions can usually be provided in lieu of a single action,
in which case the actions in the list are run in order. A list of
actions is sensitive if all of the actions are sensitive, and selected
if any of them are ; that unless :func:`SensitiveIf` or :func:`SelectedIf`,
respectively, is part of the list.

Control Actions
---------------

These are actions that manage screens, interaction results, and control flow.

.. include:: inc/control_action

Data Actions
------------

These set or toggle data.

.. include:: inc/data_action

Menu Actions
------------

These actions invoke menus, or are primarily useful while in the main
or game menus.

.. include:: inc/menu_action

.. _file-actions:

File Actions
------------

These actions handle saving, loading, and deleting of files. Many of these
take the `name` and `page` arguments.

`name`
    The name of the file to save to. This can be a string or an integer. It's
    combined with the page to create the filename.

`page`
    The page that this action acts on. This is one of "auto",
    "quick", or a positive integer. If None, the page is determined
    automatically, based on a persistent page number.

These are converted to a slot name using :var:`config.file_slotname_callback`,
if it's set.

.. include:: inc/file_action

Sync Actions
------------

.. include:: inc/sync


.. _audio-actions:

Audio Actions
-------------

The concept of channels and how they work, as well as most information
about audio in Ren'Py, is explained at :doc:`audio`.

.. include:: inc/audio_action


Focus Actions
-------------

.. include:: inc/focus_action

Other Actions
-------------

These are other actions, not found anywhere else.

.. include:: inc/other_action

Additional actions are available in other pages of this documentation, such
as :class:`Language`, :class:`Replay` and :class:`EndReplay`,
:class:`gui.SetPreference` and :class:`gui.TogglePreference`,
:class:`StylePreference`, and the :ref:`voice actions <voice-actions>`.

Other actions can be created using the :class:`Action` class.


.. _bar-values:

Bar Values
==========

Bar values are used with bars, to set the bar value, and to allow the bar
to adjust an underlying property. To create a new bar value, subclass
the :class:`BarValue` class. All classes that have the `step` keyword also accept
the `force_step` keyword whose behavior is described in :func:`ui.adjustment`.

.. include:: inc/value


.. _input-values:

Input Values
============

Input values are used with text inputs, to set the default text, to accept
changed text, to respond to the enter key, and to determine if the text is
editable by default. To create a new input value, subclass the :class:`InputValue`
class.

Ren'Py-defined input values inherit from InputValue, which means that
all values also include Enable(), Disable(), and Toggle() methods that return
actions that enable, disable, and toggle editing, respectively. See also
the :func:`DisableAllInputValues` action.

.. include:: inc/input_value


Functions and Classes
=====================

These functions and classes are useful in association with screens.

Preferences
-----------

While all preferences can be defined based on the Actions and Values
given above, it requires some knowledge of Ren'Py to figure out the
correct one to use. The preferences constructor makes this easy,
by creation an action or value, as appropriate, based on the
names used in the default preferences screen.

.. include:: inc/preference_action

.. include:: inc/preference_functions

Gamepad
-------

These functions and actions work with the gamepad.

.. include:: inc/gamepad

File Functions
--------------

These functions return useful information about files. They use the
same default page as the file actions.

.. include:: inc/file_action_function

Side Image Functions
--------------------

This function returns the side image to use.

.. include:: inc/side_image_function

Other Functions
---------------

.. include:: inc/other_screen_function

.. _tooltips:

Tooltips
--------

Tooltips can now be accessed by the ``tooltip`` property available on all
displayables, and the GetTooltip function. The GetTooltip function
returns the value of the tooltip property when the displayable
gains focus.

As a reminder, values passed to the ``tooltip`` property must support
equality.

Here's an example::

    screen tooltip_example():
        vbox:
            textbutton "North":
                action Return("n")
                tooltip "To meet a polar bear."

            textbutton "South":
                action Return("s")
                tooltip "All the way to the tropics."

            textbutton "East":
                action Return("e")
                tooltip "So we can embrace the dawn."

            textbutton "West":
                action Return("w")
                tooltip "Where to go to see the best sunsets."

            $ tooltip = GetTooltip()

            if tooltip:
                text "[tooltip]"

The :ref:`sl-nearrect` displayable can be used to display "popup-style" tooltips,
and has support for a special "tooltip" focus name, that is set to the location
of the last focus that set a tooltip::

    screen tooltip_example2():
        frame:

            padding (20, 20)
            align (.5, .3)

            has vbox

            textbutton "North":
                action Return("n")
                tooltip "To meet a polar bear."

            textbutton "South":
                action Return("s")
                tooltip "All the way to the tropics."

            textbutton "East":
                action Return("e")
                tooltip "So we can embrace the dawn."

            textbutton "West":
                action Return("w")
                tooltip "Where to go to see the best sunsets."

        # This has to be the last thing shown in the screen.

        $ tooltip = GetTooltip()

        if tooltip:

            nearrect:
                focus "tooltip"
                prefer_top True

                frame:
                    xalign 0.5
                    text tooltip


.. include:: inc/get_tooltip

Legacy
^^^^^^

.. warning:: This has been obsoleted by the above, but you might see it in older projects.

The tooltip class changes the screen when a button is hovered.

.. include:: inc/tooltips

When using a tooltip with a screen, the usual behavior is to create a
tooltip object in a default statement. The value of the tooltip and
the action method can then be used within the screen. The order of
use within a screen doesn't matter – it's possible to use the value
before an action is used.

Tooltips can take on any value. While in the example below we use the
text statement to display a string on the screen, it's also possible
to use the add statement to add a displayable. More complex behavior
is also possible.

::

    screen tooltip_test:

        default tt = Tooltip("No button selected.")

        frame:
            xfill True

            has vbox

            textbutton "One.":
                action Return(1)
                hovered tt.Action("The loneliest number.")

            textbutton "Two.":
                action Return(2)
                hovered tt.Action("Is what it takes.")

            textbutton "Three.":
                action Return(3)
                hovered tt.Action("A crowd.")

            text tt.value
