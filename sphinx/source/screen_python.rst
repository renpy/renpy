==================
Screens and Python
==================

Screen Functions
================

The following functions support various operations related to screens.

.. include:: inc/screens

.. include:: inc/ui

Actions
=======

Many of the displayables created in the screen language take actions
as arguments. An action is one of three things:

* A callable Python object (like a function or bound method) that
  takes no arguments.
* An object of a class that inherits from the Action class.
* A list of other Actions.

The advantage to inheriting from the Action class is that it allows
you to override the methods that determine when a button should be
sensitive, and when it is selected.

.. class:: Action

    To define a new action, inherit from this class. Override the
    methods in this class to change the behavior of the action.

    .. method:: __call__(self)

        This is the method that is called when the action is
        activated. In many cases, returning a non-None value from the
        action will cause the current interaction to end.

        This method must be overridden, as the default method will
        raise a NotImplementedError (and hence cause Ren'Py to
        report an error).

    .. method:: get_sensitive(self)

        This is called to determine if the button with this action
        should be sensitive. It should return true if the button is
        sensitive.

        Note that __call__ can be called, even if this returns False.

        The default implementation returns True.

    .. method:: get_selected(self)

        This should return true if the button should be rendered as a
        selected button, and false otherwise.

        The default implementation returns False.

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

    .. attribute:: alt

        The text-to-speech text used for buttons that use this Action, if
        the button does not have the :propref:`alt` property set. This can
        set to a string in the class, or in the constructor, or it can be
        a Python property that returns a string.

To run an action from Python, use :func:`renpy.run`.

.. include:: inc/run

BarValues
=========

When creating a bar, vbar, or hotbar, a BarValue object can be supplied as
the `value` property. Methods on the BarValue object are called to get
the adjustment and styles.


.. class:: BarValue

    To define a new BarValue, inherit from this class and override
    some of the methods.

    .. method:: get_adjustment(self)

        This method is called to get an adjustment object for the
        bar. It should create the adjustment with
        :func:`ui.adjustment`, and then return the object created this
        way.

        This method must be overridden, as the default method will
        raise NotImplementedError (and hence cause Ren'Py to report an
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

    .. attribute:: alt

        The text-to-speech text used for bars that use this BarValue, if
        the bar does not have the :propref:`alt` property set. This can
        set to a string in the class, or in the constructor, or it can be
        a Python property that returns a string.


InputValue
==========

When creating an input, an InputValue object can be supplied as the
`value` property. Methods on the InputValue object are called to
get and set the text, determine if the input is editable, and handle
the enter key being pressed.

.. class:: InputValue

    To define a new InputValue, inherit from this class, override
    some or all of the methods, and set the value of the default
    field.

    .. attribute:: editable

        If not true, disables the input field from being editable at all.

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
        value, that value is returned from the interaction. This may also
        raise :exc:`renpy.IgnoreEvent` to ignore the press. Otherwise, the
        enter-press is propagated to other displayables.

    The following actions are available as methods on InputValue:

    .. method:: Enable()

        Returns an action that enables text editing on the input.

    .. method:: Disable()

        Returns an action that disables text editing on the input.

    .. method:: Toggle()

        Returns an action that toggles text editing on the input.


.. _creator-defined-sl:

Creator-Defined Screen Language Statements
==========================================

Ren'Py supports defining custom screen language statements. Creator-defined screen
language statements are wrappers for the screen language :ref:`use statement <sl-use>`.
Positional arguments remain positional arguments, properties become keyword
arguments, and if the statement takes a block, so does the use statement. For
example, the custom screen language statement::

    titledwindow "Test Window":
        icon "icon.png"

        text "This is a test."

becomes::

    use titledwindow("Test Window", icon="icon.png"):
        text "This is a test."

Creator-defined screen language statements must be registered in a ``python early`` block.
What's more, the filename containing the creator-defined statement must be be loaded earlier
than any file that uses it. Since Ren'Py loads files in the Unicode sort order of their paths,
it generally makes sense to prefix the name of any file registering a user-defined
statement with 01, or some other small number.

Creator-defined screen language statements are registered with the renpy.register_sl_statement
function:

.. include:: inc/custom_sl

As an example of a creator-defined screen language statement, here's an
implementation of the ``titledwindow`` statement given above. First, the
statement must be registered in a ``python early`` block in a file that is loaded
early – a name like 01custom.rpy will often load soon enough. The registration
call looks like::


    python early:
        renpy.register_sl_statement("titledwindow", children=1).add_positional("title").add_property("icon").add_property("pos")

Then, we define a screen that implements the custom statement. This screen can be defined in
any file. One such screen is::

    screen titledwindow(title, icon=None, pos=(0, 0)):
        drag:
            pos pos

            frame:
                background "#00000080"

                has vbox

                hbox:
                    if icon is not None:
                        add icon

                    text title

                null height 15

                transclude


When are used large property groups like a `add_property_group`, it makes sense to use
the \*\*properties syntax with a properties keyword in some place. For example::

    screen titledwindow(title, icon=None, **properties):
        frame:
            # When background not in properties it will use it as default value.
            background "#00000080"

            properties properties

            has vbox

            hbox:
                if icon is not None:
                    add icon

                text title

            null height 15

            transclude

Custom defined screen language statements support the ``as`` clause, which takes the name of the variable. If present,
this variable will be assigned the value of `main` in the scope of the screen.
