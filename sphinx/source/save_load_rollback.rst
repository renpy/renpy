=============================
Saving, Loading, and Rollback
=============================

Ren'Py has support for saving game state, loading game state, and rolling
back to a previous game state. Although implemented in a slightly different
fashion, rollback can be thought of as saving the game at the start of each
statement that interacts with the user, and loading saves when the user
rolls back.


.. note::
    While we usually attempt to keep save compatibility between releases, this
    compatibility is not guaranteed. We may decide to break save-compatibility
    if doing so provides a sufficiently large benefit.

What is Saved
=============

Ren'Py attempts to save the game state. This includes both internal state
and Python state.

The internal state consists of all aspects of Ren'Py that are intended to
change once the game has started, and includes:

* The current statement, and all statements that can be returned to.
* The images and displayables that are being shown.
* The screens being shown, and the values of variables within those
  screens.
* The music that Ren'Py is playing.
* The list of nvl-mode text blocks.

The Python state consists of the variables in the store that have changed since
the game began, and all objects reachable from those variables. Note that it's
the change to the variables that matters – changes to fields in objects will
not cause those objects to be saved.

Variables set using the :ref:`default statement <default-statement>` will
always be saved.

In this example::

    define a = 1
    define o = object()
    default c = 17

    label start:
        $ b = 1
        $ o.value = 42

only `b` and `c` will be saved. `A` will not be saved because it does not change once
the game begins. `O` is not saved because it does not change – the object it
refers to changes, but the variable itself does not.

What isn't Saved
================

Python variables that are not changed after the game begins will not be
saved. This can be a major problem if a variable that is not saved and one that is
refer to the same object. (Alias the object.) In this example::

    init python:
        a = object()
        a.f = 1

    label start:
        $ b = a
        $ b.f = 2

        "a.f=[a.f] b.f=[b.f]"

`a` and `b` are aliased. Saving and loading may break this aliasing, causing
`a` and `b` to refer to different objects. Since this can be very confusing,
it's best to avoid aliasing saved and unsaved variables. (This is rare to
encounter directly, but might come up when an unsaved variable and saved field
alias.)

There are several other kinds of state that isn't saved:

control flow path
    Ren'Py only saves the current statement, and the statement it needs
    to return to. It doesn't remember how it got there. Importantly, statements
    (including variable assignments) that are added to the game won't run.

mappings of image names to displayables
    Since this mapping is not saved, the image may change to a new image
    when the game loads again. This allows an image to change to a new
    file as the game evolves.

configuration variables, styles, and style properties
    Configuration variables and styles aren't saved as part of the game.
    Therefore, they should only be changed in ``init`` blocks, and left alone
    once the game has started.


Where Ren'Py Saves
==================

Saves occur at the start of a Ren'Py statement in the outermost interaction
context.

What's important here is to note that saving occurs at the **start** of a
statement. If a load or rollback occurs in the middle of a statement that
interacts multiple times, the state will be the state that was active
when the statement began.

This can be a problem in Python-defined statements. In::

    python:

        i = 0

        while i < 10:

            i += 1

            narrator("The count is now [i].")

if the user saves and loads in the middle, the loop will begin anew. Using
Ren'Py script – rather than Python – to loop avoids this problem.::

    $ i = 0

    while i < 10:

        $ i += 1

        "The count is now [i]."


What Ren'Py Can Save
====================

Ren'Py uses the Python pickle system to save game state. This module can
save:

* Basic types, such as True, False, None, int, str, float, complex, str, and Unicode objects.
* Compound types, like lists, tuples, sets, and dicts.
* Creator-defined objects, classes, functions, methods, and bound methods. For
  pickling these functions to succeed, they must remain available under their
  original names.
* Character, Displayable, Transform, and Transition objects.

.. _cant-save:

What Ren'Py Can't Save
======================

There are certain types that cannot be pickled:

* Render objects.
* Iterator objects.
* Generator objects.
* Coroutine tasks and futures, like those created with ``async`` and ``await``.
* File-like objects.
* Network sockets, and objects that enclose them.
* Inner functions and lambdas.

This may not be an exhaustive list.

Objects that can't be pickled can still be used, provided that their use
is combined to namespaces that aren't saved by Ren'Py (like init variables,
namespaces inside functions, or ``python hide`` blocks.)

For example, using a file object like::

    $ monika_file = open(config.gamedir + "/monika.chr", "w")
    $ monika_file.write("Do not delete.\r\n")
    $ monika_file.close()

Won't work, as ``f`` could be saved between any of the three Python statements.
Putting this in a ``python hide`` block will work::

    python hide:

        monika_file = open(config.gamedir + "/monika.chr", "w")
        monika_file.write("Do not delete.\r\n")
        monika_file.close()

(Of course, using the python ``with`` statement would be cleaner.) ::

    python hide:

        with open(config.gamedir + "/monika.chr", "w") as monika_file:
            monika_file.write("Do not delete.\r\n")

Coroutines, like those made with ``async``, ``await``, or the ``asyncio``
are similar. If you have::

    init python:

        import asyncio

        async def sleep_func():
            await asyncio.sleep(1)
            await asyncio.sleep(1)

then::

    $ sleep_task = sleep_func()
    $ asyncio.run(sleep_task)

will have problems, since `sleep_task` can't be saved. But if it's not assigned
to a variable::

    $ asyncio.run(sleep_func())

will run fine.

.. _save-functions:

Save Functions and Variables
============================

There is one variable that is used by the high-level save system:
:var:`save_name`.

This is a string that is stored with each save. It can be used to give
a name to the save, to help users tell them apart.

More per-save data customization can be done with the Json supplementary
data system, see :var:`config.save_json_callbacks`.

There are a number of high-level save actions and functions defined in the
:doc:`screen actions <screen_actions>`. In addition, there are the following
low-level save and load actions.


.. include:: inc/loadsave

Retaining Data After Load
=========================

When a game is loaded, the state of the game is reset (using the rollback
system described below) to the state of the game when the current statement
began executing.

In some cases, this may not be desirable. For example, when a screen allows
editing of a value, we may want to retain that value when the game is
loaded. When renpy.retain_after_load is called, data will not be reverted
when a game is saved and loaded before the end of the next checkpointed
interaction.

Note that while data is not changed, control is reset to the start of the
current statement. That statement will execute again, with the new data
in place at the start of the statement.

For example::

    screen edit_value:
        hbox:
            text "[value]"
            textbutton "+" action SetVariable("value", value + 1)
            textbutton "-" action SetVariable("value", value - 1)
            textbutton "+" action Return(True)

    label start:
        $ value = 0
        $ renpy.retain_after_load()
        call screen edit_value


.. include:: inc/retain_after_load

.. _rollback:

Rollback
========

Rollback allows the user to revert the game to an earlier state in
much the same way as undo/redo systems that are available in most
modern applications. While the system takes care of maintaining the
visuals and game variables during rollback events, there are several
things that should be considered while creating a game.


What Data is Rolled Back?
==========================

Rollback affects variables that have been changed after the init phase, and
objects of revertable types reachable from those variables. The short version
is that lists, dicts, and sets created in Ren'Py script are revertable as are
instances of classes defined in Ren'Py scripts. Data created inside Python
or inside Ren'Py usually isn't revertable.

In more detail, inside the stores
that Python embedded inside Ren'Py scripts run in, the object, list, dict, and
set types have been replaced with equivalent types that are revertable. Objects
that inherit from these types are also revertable. The :class:`renpy.Displayable`
type inherits from the revertable object type.

To make the use of revertable objects more convenient, Ren'Py modifies Python
found inside Ren'Py script files in the following way.

* Literal lists, dicts, and sets are automatically converted to the
  revertable equivalent.
* List, dict, and set comprehensions are also automatically converted to
  the revertable equivalent.
* Other python syntax, such as extended unpacking, that can create lists,
  dicts, or sets converts the result to the revertable equivalent. However,
  for performance reasons, double-starred parameters to functions and methods
  (that create dictionaries of extra keyword arguments) are not converted
  to revertable objects.
* Classes that do not inherit from any other types automatically inherit
  from the revertable object.

In addition:

* The methods and operators of revertable types have been modified to return
  revertable objects when a list, dict, or set is produced.
* Built in functions that return lists, dicts, and sets return a revertable
  equivalent.

Calling into Python code will not generally produce a revertable object. Some
cases where you'll get an object that may not participate in rollback are:

* Calling methods on built-in types, like the str.split method.
* When the object is created in a Python module that's been imported, and
  then return to Ren'Py. (For example, an instance of collections.defaultdict
  won't participate in rollback.)
* Objects returned from Ren'Py's API, unless documented otherwise.

If such data needs to participate in rollback, it may make sense to convert
it to a type that does partipate. For example::

    # Calling list inside Python-in-Ren'Py converts a non-revertable list
    # into a revertable one.
    $ attrs = list(renpy.get_attributes("eileen"))


Supporting Rollback and Roll Forward
====================================

Most Ren'Py statements automatically support rollback and roll forward. If
you call :func:`ui.interact` directly, you'll need to add support for rollback
and roll-forward yourself. This can be done using the following structure::


    # This is None if we're not rolling back, or else the value that was
    # passed to checkpoint last time if we're rolling forward.
    roll_forward = renpy.roll_forward_info()

    # Set up the screen here...

    # Interact with the user.
    rv = ui.interact(roll_forward=roll_forward)

    # Store the result of the interaction.
    renpy.checkpoint(rv)

It's important that your game does not interact with the user after renpy.checkpoint
has been called. (If you do, the user may not be able to rollback.)

.. include:: inc/rollback

Blocking Rollback
=================

.. warning::

    Blocking rollback is a user-unfriendly thing to do. If a user mistakenly
    clicks on an unintended choice, he or she will be unable to correct their
    mistake. Since rollback is equivalent to saving and loading, your users
    will be forced to save more often, breaking game engagement.

It is possible to disable rollback in part or in full. If rollback is
not wanted at all, it can simply be turned off through the
:var:`config.rollback_enabled` option.

More common is a partial block of rollback. This can be achieved by the
:func:`renpy.block_rollback` function. When called, it will instruct
Ren'Py not to roll back before that point. For example::

    label final_answer:
        "Is that your final answer?"

    menu:
        "Yes":
            jump no_return
        "No":
            "We have ways of making you talk."
            "You should contemplate them."
            "I'll ask you one more time..."
            jump final_answer

    label no_return:
        $ renpy.block_rollback()

        "So be it. There's no turning back now."

When the label no_return is reached, Ren'Py won't allow a rollback
back to the menu.


Fixing Rollback
===============

Fixing rollback provides for an intermediate choice between
unconstrained rollback and blocking rollback entirely. Rollback is
allowed, but the user is not allowed to make changes to their
decisions. Fixing rollback is done with the :func:`renpy.fix_rollback`
function, as shown in the following example::

    label final_answer:
        "Is that your final answer?"
    menu:
        "Yes":
            jump no_return
        "No":
            "We have ways of making you talk."
            "You should contemplate them."
            "I'll ask you one more time..."
            jump final_answer

    label no_return:
        $ renpy.fix_rollback()

        "So be it. There's no turning back now."

Now, after the fix_rollback function is called, it will still be
possible for the user to roll back to the menu. However, it will not be
possible to make a different choice.

There are some caveats to consider when designing a game for
fix_rollback. Ren'Py will automatically take care of locking any data
that is given to :func:`checkpoint`. However, due to the generic nature
of Ren'Py, it is possible to write scripts that bypass this and
change things in ways that may have unpredictable results.  Most notably,
``call screen`` doesn't work well with fixed rollback. It is up
to the creator to block rollback at problematic locations.

The internal user interaction options for menus, :func:`renpy.input`
and :func:`renpy.imagemap` are designed to fully work with fix_rollback.

Styling Fixed Rollback
======================

Because fix_rollback changes the functionality of menus and imagemaps,
it is advisable to reflect this in the appearance. To do this, it is
important to understand how the widget states of the menu buttons are
changed. There are two modes that can be selected through the
:var:`config.fix_rollback_without_choice` option.

The default option will set the chosen option to "selected", thereby
activating the style properties with the "selected\_" prefix. All other
buttons will be made insensitive and show using the properties with the
"insensitive\_" prefix. Effectively this leaves the menu with a single
selectable choice.

When the :var:`config.fix_rollback_without_choice` option is set to
False, all buttons are made insensitive. This means that the chosen
option will use the "selected_insensitive\_" prefix for the style
properties while the other buttons use properties with the
"insensitive\_" prefix.

Fixed Rollback and Custom Screens
=================================

To simplify the creation of custom screens, two actions are
provided to help with the most common uses. The :func:`ui.ChoiceReturn` action
returns the value when the button it is attached to is clicked. The
:func:`ui.ChoiceJump` action can be used to jump to a script label. However, this
action only works properly when the screen is called trough a
``call screen`` statement.

Examples::

    screen demo_imagemap():
        roll_forward True

        imagemap:
            ground "imagemap_ground.jpg"
            hover "imagemap_hover.jpg"
            selected_idle "imagemap_selected_idle.jpg"
            selected_hover "imagemap_hover.jpg"

            hotspot (8, 200, 78, 78) action ui.ChoiceJump("swimming", "go_swimming", block_all=False)
            hotspot (204, 50, 78, 78) action ui.ChoiceJump("science", "go_science_club", block_all=False)
            hotspot (452, 79, 78, 78) action ui.ChoiceJump("art", "go_art_lessons", block_all=False)
            hotspot (602, 316, 78, 78) action ui.ChoiceJump("home", "go_home", block_all=False)

::

    screen rps():
        roll_forward True

        hbox:
            imagebutton:
                idle "rock.png"
                hover "rock_hover.png"
                selected_insensitive "rock_hover.png"
                action ui.ChoiceReturn("rock", "Rock", block_all=True)
            imagebutton:
                idle "paper.png"
                hover "paper_hover.png"
                selected_insensitive "paper_hover.png"
                action ui.ChoiceReturn("paper", "Paper", block_all=True)
            imagebutton:
                idle "scissors.png"
                hover "scissors_hover.png"
                selected_insensitive "scissors_hover.png"
                action ui.ChoiceReturn("scissors", "Scissors", block_all=True)

            if renpy.in_fixed_rollback():
                textbutton "Advance":
                    action Return(renpy.roll_forward_info())
                    # required because of the block_all=True in all the other buttons

    label dough:
        call screen rps
        $ chosen = _return
        $ renpy.fix_rollback()
        m "[chosen]!"

When writing custom Python routines that must play nice with the
fix_rollback system there are a few simple things to know. First of all
the :func:`renpy.in_fixed_rollback` function can be used to determine whether
the game is currently in fixed rollback state. Second, when in
fixed rollback state, :func:`ui.interact` will always return the
supplied roll_forward data regardless of what action was performed. This
effectively means that when the :func:`ui.interact`/:func:`renpy.checkpoint`
functions are used, most of the work is done.


Rollback-blocking and -fixing Functions
=======================================

.. include:: inc/blockrollback

NoRollback
==========

.. include:: inc/norollback

For example::

    init python:

        class MyClass(NoRollback):
            def __init__(self):
                self.value = 0

    label start:
        $ o = MyClass()

        "Welcome!"

        $ o.value += 1

        "o.value is [o.value]. It will increase each time you rollback and then click ahead."

Rollback-Supporting Classes
===========================

The following classes exist to help support the use of rollback in your
game. They may be useful in some circumstances.

.. include:: inc/rollbackclasses
