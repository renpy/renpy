.. _modes:

=====
Modes
=====

In Ren'Py, a mode is a concise way of describing the type of an
interaction. When a mode is reported to Ren'Py, user-defined callbacks
can be run. These calbacks can be used to react to a change in mode,
perhaps by reconfiguring the user interface. For example, one can
cause a transition to occur when switching from ADV-mode to NVL-mode,
or when going to a menu, etc.

The goal of the mode systems is to provide a powerful and flexible
way of detecting and responding to these changes.

Default Modes
=============

The following are the modes corresponding to built-in interactions:

start
    This is the mode that Ren'Py is in when a new context is
    created, such as at the start of a game. Ren'Py never
    automatically enters this mode, but instead, initializes the list
    of modes to include start.

say
    The mode Ren'Py enters when an ADV-mode say executes.

menu
    The mode Ren'Py enters when an ADV-mode menu executes.

nvl
    The mode Ren'Py enters when an NVL-mode say executes.

nvl_menu
    The mode Ren'Py enters when an NVL-mode menu executes.

pause
    The mode Ren'Py enters when :func:`renpy.pause` is run. This is
    also the mode Ren'Py is in when a ``pause`` statement of indefinite
    duration occurs.

with
    The mode Ren'Py enters when a transition introduced by the ``with``
    statement occurs. This is also used for ``pause`` statement with
    a duration specified.

    Note that the with mode is entered at the start of the with
    statement, which is after any preceding scene, show, or hide
    statements have been run.

screen
    The mode Ren'Py enters when a screen is invoked using the ``call
    screen`` statement.

imagemap
    The mode Ren'Py enters when an old-style imagemap is invoked using
    :func:`renpy.imagemap`.

input
    The mode Ren'Py enters when text input is requested using the
    :func:`renpy.input` function.

Other modes can be entered by calling the renpy.mode function.

.. include:: inc/modes


Mode Callbacks
==============

The :var:`config.mode_callbacks` variable contains a list of mode
callbacks that are invoked whenever Ren'Py enters a mode. The mode
callbacks are called with two parameters:

mode
    A string giving the name of the mode that we are entering.

old_modes
    A list of strings, giving the modes that the system has previously
    entered, ordered from most recent to least recent.

Note that when entering a mode we're already in, the first item in
`old_modes` will be equal to `mode`.


Example Mode Callbacks
----------------------

This mode callback causes transitions to occur when switching from ADV
to NVL mode, and vice-versa. This ships as part of Ren'Py, so there's
no need to actually use it. ::

    init python:
        def _nvl_adv_callback(mode, old_modes):

            old = old_modes[0]

            if config.adv_nvl_transition:
                if mode == "nvl" or mode == "nvl_menu":
                    if old == "say" or old == "menu":
                        nvl_show(config.adv_nvl_transition)

            if config.nvl_adv_transition:
                if mode == "say" or mode == "menu":
                    if old == "nvl" or old == "nvl_menu":
                        nvl_hide(config.nvl_adv_transition)

        config.mode_callbacks.append(_nvl_adv_callback)
