.. _screen-actions:

=====================================
Screen Actions, Values, and Functions
=====================================

Ren'Py ships with a number of actions, values, and functions intended
for use with screens and the screen language.

Actions
=======

Many of the displayables created in the screen language take actions
as arguments, which are invoked typically when a button is activated,
hovered, or unhovered. Actions may also determine when a button is
selected or insensitive.

An action is in the general case a subclass of the :class:`Action`
class, as are the actions listed in this page. Alternatively, a python
callable (like a function or a bound method) taking no arguments can be
used as an action. It will be called when the action is to be invoked.
If the callable, or the \__call\__ method of the :class:`Action`
subclass, returns a value, then that value is returned from an
interaction. This is what the Return action does, for example.

An action may also be a list of actions, in which case the actions in
the list are run in order.

To run an action from Python, use :func:`renpy.run`.

.. include:: inc/run

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
    combined with the page to create the filename.

`page`
    The page that this action acts on. This is one of "auto",
    "quick", or a positive integer. If None, the page is determined
    automatically, based on a persistent page number.

.. include:: inc/file_action

Audio Actions
-------------

The concept of channels and how they work, as well as most information
about audio in Ren'Py, is explained at :ref:`audio`.

.. include:: inc/audio_action


Focus Actions
-------------

.. include:: inc/focus_action

Other Actions
-------------

These are other actions, not found anywhere else.

.. include:: inc/other_action

The Action class
----------------

The advantage to inheriting from the Action class, instead of using a
function or callable, is that it allows you to override the methods that
determine when a button should be sensitive, and when it is selected.

.. class:: Action

   To define a new action, inherit from this class. Override the
   methods in this class to change the behavior of the action.

   .. method:: __call__(self)

       This is the method that is called when the action is
       activated. In many cases, returning a non-None value from the
       action will cause the current interaction to end.

       This method must be overridden, as the default method will
       raise NotImplemented (and hence cause Ren'Py to report an
       error).

   .. method:: get_sensitive(self)

       This is called to determine if the button with this action
       should be sensitive. It should return true if the button is
       sensitive.

       Note that __call__ can be called, even if this returns False.

       The default implementation returns True.

   .. method:: get_selected(self)

       This should return true if the button should be rendered as a
       selected button, and false otherwise.

       The default implemention returns False.

   .. method:: get_tooltip(self)

       This gets a default tooltip for this button, if a specific
       tooltip is not assigned. It should return the tooltip value,
       or None if a tooltip is not known.

       This defaults to returning None.

   .. method:: periodic(self, st)

       This method is called once at the start of each interaction,
       and then is called periodically thereafter. If it returns a
       number, it will be called before that many seconds elapse, but
       it might be called sooner.

       The main use of this is to call
       :func:`renpy.restart_interaction` if the value of
       get_selected or get_sensitive should change.

       It takes one argument:

       `st`
           The number of seconds since the screen or displayable this
           action is associated with was first shown.

   .. method:: unhovered(self)

       When the action is used as the `hovered` parameter to a button (or
       similar object), this method is called when the object loses focus.


.. _bar-values:

Bar Values
==========

Bar values are used with bars, to set the bar value, and to allow the bar
to adjust an underlying property. All of the following classes that have
the `step` keyword also accept the `force_step` keyword whose behavior is
described in :func:`ui.adjustment`. In addition to the values listed below,
it is also possible to subclass the :class:`BarValue` class.

.. include:: inc/value

The BarValue class
------------------

.. class:: BarValue

    To define a new BarValue, inherit from this class and override
    some of the methods.

    .. method:: get_adjustment(self)

        This method is called to get an adjustment object for the
        bar. It should create the adjustment with
        :func:`ui.adjustment`, and then return the object created this
        way.

        This method must be overridden, as the default method will
        raise NotImplemented (and hence cause Ren'Py to report an
        error).

    .. method:: get_style(self)

        This is used to determine the style of bars that use this
        value. It should return a tuple of two style names or style
        objects. The first is used for a bar, and the
        second for vbar.

        This defaults to ("bar", "vbar").

    .. method:: get_tooltip(self)

       This gets a default tooltip for this button, if a specific
       tooltip is not assigned. It should return the tooltip value,
       or None if a tooltip is not known.

       This defaults to returning None.

    .. method:: replaces(self, other)

        This is called when a BarValue replaces another BarValue, such
        as when a screen is updated. It can be used to update this
        BarValue from the other. It is called before get_adjustment.

        Note that `other` is not necessarily the same type as `self`.

    .. method:: periodic(self, st)

       This method is called once at the start of each interaction. If
       it returns a number of seconds, it will be called before that
       many seconds elapse, but it might be called sooner. It is
       called after get_adjustment.

       It can be used to update the value of the bar over time, like
       :func:`AnimatedValue` does. To do this, get_adjustment should
       store the adjustment, and periodic should call the
       adjustment's changed method.


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

The InputValue class
--------------------

.. class:: InputValue

    To define a new InputValue, inherit from this class, override
    some or all of the methods, and set the value of the default
    field.

    .. attribute: editable

        If true, this field is editable at all.

    .. attribute:: default

        If true, the input is eligible to be editable by default. (That
        is, it may be given the caret when the screen is shown.)

    .. method:: get_text(self)

        Returns the default text of the input. This must be implemented.

    .. method:: set_text(self, s)

        Called when the text of the input is changed, with the new text.
        This must be implemented.

    .. method:: enter(self)

        Called when the user presses enter. If this returns a non-None
        value, that value is returned from the interacton. This may also
        raise renpy.IgnoreEvent() to ignore the press. Otherwise, the
        enter-press is propagated to other displayables.

    The following actions are available as methods on InputValue:

    .. method:: Enable()

        Returns an action that enables text editing on the input.

    .. method:: Disable()

        Returns an action that disables text editing on the input.

    .. method:: Toggle()

        Returns an action that toggles text editing on the input.


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

.. _tooltips:

Tooltips
--------

Tooltips can now be accessed by the tooltip property available on all
displayables, and the GetTooltip function. The GetTooltip function
returns the value of the tooltip property when the displayable
gains focus.

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

The :ref:`nearrect` displayable can be used to display "popup-style" tooltips,
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
