==========================
Lifecycle of a Ren'Py game
==========================

When launching a Ren'Py game, be it from the executable or from the launcher, it follows a series
of steps up until the point where it is closed. This page exposes the various phases of this
lifecycle, and various related statements.

Boot Time
=========

There are a lot of things happening before the game window appears. This is the boot time. The
only thing that's possibly visible at that point is the :ref:`presplash <presplash>`.

.. _early-phase:

Script Parsing Phase
--------------------

To read the game's code, Ren'Py reads each of the game's ``.rpy`` (and ``_ren.py``) files one by
one. That's the "parsing" phase, or "early" phase. The order that files are read in is:

1. Files inside :file`renpy/common` are loaded using  using the full path, in unicode order.

2. Only if :file:`game/libs/libs.txt` exists, files in game/libs are loaded using the filename only,
   in unicode order. (In this order, :file:`game/libs/plants/aloe.rpy` will load before :file:`game/libs/animals/zebra.rpy`.)

3. Files in :file:`game` are loaded using the full path, in unicode order. (In this order,
   :file:`game/animals/zebra.rpy` will load before :file:`game/plants/aloe.rpy`.)

4. Only if :file:`game/mods/mods.txt` exists, files in game/mods are loaded using the filename only,
   in unicode order. (In this order, :file:`game/mods/plants/aloe.rpy` will load before :file:`game/mods/animals/zebra.rpy`.)

The precise order of file loading mostly affects :doc:`cds`.

The first creator-written code being executed is what's written in ``python early`` blocks. These
are executed after the file they're in has been read and parsed, but before the next file gets
read. This is why statements which modify how parsing works, like :doc:`cds`,
:ref:`creator-defined-sl` or new custom :ref:`warpers`, must be written in ``python early``
blocks.

The ``init python early`` syntax is sometimes encountered, but it's redundant and doesn't change
anything in how the code gets executed compared to ``python early``.

.. _init-phase:

Init Phase
----------

After parsing/early phase, the "init" phase starts. Several statements are executed at that time,
including the :ref:`init-python-statement`, the :ref:`define-statement`, the
:ref:`transform-statement`, the :ref:`image-statement`, the :ref:`screen-statement`, and the
:doc:`style <style>` statement.

The init phase is divided in successive epochs, or init priorities.
Contrary to what the term may imply, epochs of lower priority are executed before
epochs of higher priority. It is suggested that games use init priorities of -99 to 99.
Libraries and mods can use from -999 to -100 and 100 to 999. Init priorities outside of the
range -999 to 999 are reserved for Ren'Py's internal use.

.. image define default transform (init) screen (testcase) (translation) style

By default, these statements are executed at init offset 0. However, they can be offset using
the :ref:`init-offset-statement` or by other means. The :ref:`image-statement` is an exception to
both of these rules, as it executes at an init priority of 500 by default, and the init offset
statement adds or substracts from this 500, rather than replacing it.

Automatic image definition from the :ref:`image-directory` occurs at init priority 0.

Note that while the :ref:`default <default-statement>` statements are not executed at init time,
the priority of the statements influences the order in which they will be executed, relative to
one another.

.. _init-offset-statement:

Init Offset Statement
^^^^^^^^^^^^^^^^^^^^^

The ``init offset`` statement sets a priority offset for all statements
that run at init time. It should be placed at the top of the file, and it applies to all following
statements in the current block and child blocks, up to the next
init priority statement. The statement::

    init offset = 42

sets the priority offset to 42. In::

    init offset = 2
    define foo = 2

    init offset = 1
    define foo = 1

    init offset = 0

The first define statement is run at priority 2, which means it runs
after the second define statement, and hence ``foo`` winds up with
a value of 2.

Script Execution
================

This is what happens once the game window becomes visible. This is when normal Ren'Py statements
execute, and when the rules described in :doc:`label` apply. This is also the time when the
variables from :ref:`default statements <default-statement>` are set for the first time - as
opposed to :ref:`define statements <define-statement>` which are set at init time.

Config variables should not be changed once normal game execution starts.

Splashscreen
------------

If it exists, the :ref:`splashscreen <adding-a-splashscreen>` label is executed until it returns.

A splashscreen is only displayed once per time Ren'Py is run, and is skipped when
script execution restarts.

Main Menu
---------

If it exists, the ``before_main_menu`` label is executed. Then, once it returns, the
:ref:`main_menu <main-menu-screen>` screen is shown, unless a ``main_menu`` label exists, in which
case it is executed instead. See :ref:`special-labels` for more information.

The main menu itself is run in its own :ref:`context <context>`. Ren'Py can leave this
context by calling the :class:`Start` action, which also jumps to a label or to the ``start`` label
if none is specified. Returning from the ``main_menu`` label also enters the in-game phase at the
``start`` label, while loading a game enters the in-game phase at the spot where the game was saved.

In-Game Phase
-------------

This is the phase in which an actual playthrough of the game occurs, and this is
the mode in which players generally spend most of their time. This phase continues
until the game quits, or the game restarts and the player returns to the main menu.

During the in-game phase, the :class:`ShowMenu` action can be used to display a
screen in a new context.

The In-game phase continues until either the player quits or restarts the game
to return to the main menu. The game may be restarted by returning when no
call is on the stack, as explained explained in :doc:`label`. The game may
also be restarted by the :class:`MainMenu` action or the :func:`renpy.full_restart`
function.

When the game restarts, all non-persistent data is reset to what it was at the
end of the script execution phase, and then the script execution phase begins
again, skipping the splashscreen.
