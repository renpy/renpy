=====================================
Screen Actions, Values, and Functions
=====================================

Ren'Py ships with a number of actions, values, and functions intended
for use with screens and the screen language.

Actions
=======

Actions are be invoked when a button (including imagebuttons,
textbuttons, and hotspots) is activated, hovered, or
unhovered. Actions may determine when a button is selected or
insensitive.

Along with these actions, an action may be a function that does not
take any arguments. The function is called when the action is
invoked. If the action returns a value, then the value is returned
from an interaction.

An action may also be a list of actions, the actions in the list are
run in order.

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

File Actions
------------

These actions handle saving, loading, and deleting of files. Many of these
take the `name` and `page` arguments.

`name`
    The name of the file to save to. This can be a string or an integer. It's
    combined with a 

`page`
    The page that this action acts on. Thgis is one of "auto",
    "quick", or a positive integer. If None, the page is determined
    automatically, based on a persistent page number. 

.. include:: inc/file_action

Other Actions
-------------

These are other actions, not found anywhere else.

.. include:: inc/other_action

Values
======

Values are used with bars, to set the bar value, and to allow the bar
to adjust an underlying property.

.. include:: inc/value

Functions
=========

These functions are useful in association with screens.

Preferences
-----------

While all preferences can be defined based on the Actions and Values
given above, it requires some knowledge of Ren'Py to figure out the
correct one to use. The preferences constructor makes this easy,
by creation an action or value, as appropriate, based on the
names used in the default preferences screen.

.. include:: inc/preference_action


File Functions
--------------

These functions return useful information about files. They use the
same default page as the file actions.

.. include:: inc/file_action_function


