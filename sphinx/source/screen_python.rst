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

Warning: UI Functions are deprecated and not recommended.

Here's an example python screen::

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

With the advent of SL2, UI Functions are deprecated and not recommended.

The UI functions are python equivalents of the screen language
statements. For each screen language statement, there is a ui function
with the same name. For example, ui.text corresponds to the text
statement, and ui.add corresponds to the add statement.

There is a simple mapping between screen language parameters and
arguments and python arguments. Screen language parameters
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
that child - use ui.null() if the child is missing.

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

Actions
=======

Many of the displayables created in the screen language take actions
as arguments. An action is one of three things:

* A callable python object (like a function or bound method) that
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

   .. method:: unhovered(self):

       When the action is used as the `hovered` parameter to a button (or
       similar object), this method is called when the object loses focus.

BarValues
=========

When creating a bar, vbar, or hotbar, a BarValue object can be supplied as
the `value` argument. Methods on the BarValue object are called to get
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
        raise NotImplemented (and hence cause Ren'Py to report an
        error).

    .. method:: get_style(self)

        This is used to determine the style of bars that use this
        value. It should return a tuple of two style names or style
        objects. The first is used for a bar, and the
        second for vbar.

        This defaults to ("bar", "vbar").

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

Creator-defined screen language statements must be registered in a python early block.
What's more, the filename containing the creator-defined statement must be be loaded earlier
than any file that uses it. Since Ren'Py loads files in unicode sort order, it
generally makes sense to prefix the name of any file registering a user-defined
statement with 01, or some other small number.

Creator-defined screen language statements are registered with the renpy.register_sl_statement
function:

.. include:: inc/custom_sl

As an example of a creator-defined screen language statement, here's an
implementation of the ``titledwindow`` statement given above. First, the
statement must be registered in a python early block in a file that is loaded
early - a name like 01custom.rpy will often load soon enough. The registration
call looks like::


    python early:
        renpy.register_sl_statement("titledwindow", positional=1, children=1).add_property("icon").add_property("pos")

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
