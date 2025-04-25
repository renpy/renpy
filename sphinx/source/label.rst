Labels & Control Flow
=====================

.. _label-statement:

Label Statement
---------------

Label statements allow the given name to be assigned to a program point. They
exist solely to be called or jumped to, either from Ren'Py script, Python
functions, or from screens. ::

    label sample1:
        "Here is 'sample1' label."

    label sample2(a="default"):
        "Here is 'sample2' label."
        "a = [a]"

A label statement may have a block associated with it. In that case, control
enters the block whenever the label statement is reached, and proceeds with the
statement after the label statement whenever the end of the block is reached:
the following code, when jumping to the "origin" label, produces the "a, b, c"
sequence. ::

    label origin:
    "a"
    label hasblock:
        "b"
    "c"
    return

There are two kinds of labels: *global* and *local* labels. Global labels live
in one global namespace shared across all project files and thus should have unique
names per game. A local label on the other hand refer to a global label, so several
local labels in the game can have the same name, provided they are related to
different global labels. To declare a local label, prefix its name with a period
``.``, and put it under a global label which it will belong to.
For example::

    label global_label:
        "Under a global label.."
    label .local_label:
        "..resides a local one."
        jump .another_local
    label .another_local:
        "And another !"
        jump .local_label

Local labels can be referenced directly inside the same global label they are
declared in, or by their full name, consisting of global and local name parts::

    label another_global:
        "Now lets jump inside a local label located somewhere else."
        jump global_label.local_name

The label statement may take an optional list of parameters. These parameters
are processed as described in :pep:`570`, with two exceptions:

First, the values of default parameters are evaluated at call time.

Second, the variables are scoped dynamically, rather than lexically. This means
that when a variable gets its value from a label parameter, it will be reverted
(to the previous value of the variable if it had one, or to the absence of the
variable otherwise) when a return statement is reached. It also means that given
a statement using a certain variable, that variable may or may not get its value
from a label parameter depending on how the statement was reached ; that is not
possible in pure Python code. ::

    default a = 3

    label start:
        menu:
            "Call":
                call label_with_params(5)
            "Jump":
                jump label_without_params
        jump start

    label label_with_params(a):
    label label_without_params:
        e "a = [a]" # displays 5 or 3 depending on what path was taken
        return

It doesn't generally make sense to have a label with parameters be reached by a
jump or a previous statement. For an example of labels with parameters, see the
:ref:`call statement <call-statement>`.


.. _jump-statement:

Jump Statement
--------------

The jump statement is used to transfer control to the given label.

If the ``expression`` keyword is present, the expression following it is
evaluated, and the string so computed is used as the label name of the
statement to jump to. If the ``expression`` keyword is not present, the label
name of the statement to jump to must be explicitly given.

A local label name can be passed, either with ``expression`` or without,
and either with the global label prepended ("global_label.local_label"),
or starting with a dot (".local_label").

Unlike call, jump does not push the next statement onto a stack. As a
result, there's no way to return to where you've jumped from. ::

    label loop_start:

        e "Oh no! It looks like we're trapped in an infinite loop."

        jump loop_start

.. _call-statement:

Call Statement
--------------

The call statement is used to transfer control to the given label. It
also pushes the next statement onto the call stack, allowing the return statement
to return control to the statement following the call.

If the ``expression`` keyword is present, the expression following it is evaluated, and the
resulting string is used as the name of the label to call. If the
``expression`` keyword is not present, the name of the label to call must be
explicitly given.

A local label name can be passed, either with ``expression`` or without,
and either with the global label prepended ("global_label.local_label"),
or starting with a dot (".local_label").

If the optional ``from`` clause is present, it has the effect of including a label
statement with the given name as the statement immediately following the call
statement. An explicit label helps to ensure that saved games with return
stacks can return to the proper place when loaded on a changed script.

The call statement may take arguments, which are processed as described in :pep:`448`.

When using a call expression with an arguments list, the ``pass`` keyword must
be inserted between the expression and the arguments list. Otherwise, the
arguments list will be parsed as part of the expression, not as part of the
call. ::

    label start:

        e "First, we will call a subroutine."

        call subroutine

        call subroutine(2)

        call expression "sub" + "routine" pass (count=3)

        return

    # ...

    label subroutine(count=1):

        e "I came here [count] time(s)."
        e "Next, we will return from the subroutine."

        return

.. warning::

    Publishing a game without ``from`` clauses for each ``call`` statement
    is dangerous, if you intend to publish updates of the game later on.
    If no such clauses are added, and if you edit the file containing the
    ``call`` instruction, there is a potential risk for saves made inside
    the called label to become broken.

    Using the "Add from clauses to calls" option when building a game's
    distribution can solve that issue.

.. _return-statement:

Return Statement
----------------

The ``return`` statement pops the top statement off of the call stack, and transfers
control to it. If the call stack is empty, the return statement restarts
Ren'Py, returning control to the main menu.

If the optional expression is given to return, it is evaluated, and it's result
is stored in the ``_return`` variable. This variable is dynamically scoped to each
context.

.. _special-labels:

Special Labels
--------------

The following labels are used by Ren'Py:

``start``
    By default, Ren'Py jumps to this label when the game starts.

``quit``
    If it exists, this label is called in a new context when the user
    quits the game.

``after_load``
    If it exists, this label is called when a game is loaded. It can be
    use to fix data when the game is updated. If data is changed by this
    label, :func:`renpy.block_rollback` should be called to prevent those
    changes from being reverted if the player rolls back past the load
    point.

``splashscreen``
    If it exists, this label is called when the game is first run, before
    showing the main menu. Please see :ref:`Adding a Splashscreen <adding-a-splashscreen>`.

``before_main_menu``
    If it exists, this label is called before the main menu. It is used in
    rare cases to set up the main menu, for example by starting a movie
    playing in the background.

``main_menu``
    If it exists, this label is called instead of the main menu. If it returns,
    Ren'Py will start the game at the ``start`` label. For example, the
    following will immediately start the game without displaying the
    main menu. ::

        label main_menu:
            return

``after_warp``
    If it is existed, this label is called after a warp but before the warped-to
    statement executes. Please see :ref:`Warping to a line <warping_to_a_line>`.

``hide_windows``
    If it exists, this label is called when the player hides the windows with
    the right mouse button or the H key. If this returns true, the hide is
    cancelled (it's assumed the hide has occurred). Otherwise, the hide
    continues.

Ren'Py also uses the following labels to show some of the :doc:`special screens <screen_special>`:

* ``main_menu_screen``
* ``load_screen``
* ``save_screen``
* ``preferences_screen``
* ``joystick_preferences_screen``

Labels & Control Flow Functions
-------------------------------

.. include:: inc/label

.. _context:

Contexts
--------

Contexts are used internally by Ren'Py to manage the changeable and saveable
state of the game. Contexts include:

* the currently running Ren'Py statement,
* the call stack, as described above, and the names and former values of dynamic
  variables created by :func:`renpy.dynamic`,
* the images currently being shown (and information about them like their attributes,
  the transforms applied to them and so on),
* the screens being shown, and the variables inside them,
* the audio that is playing or queued.

Most of the time there is only one context at play, and only one instance of each
of these elements exists. This changes when entering the main or game menus;
everything above can be changed, and will be restored when leaving the menu
context. Some of these changes are automatic, like the screens layer being
cleared when entering a context.

Ren'Py also creates new contexts as part of :ref:`replay` and when
:func:`hiding the interface <HideInterface>`.

The creation of :ref:`screen language <screens>` has considerably lessened the need
for creating contexts.

Rollback is only enabled in the base context (meaning, when there is only
one context), and only the base context is saved, which is why the game menu
uses a context.

.. include:: inc/context
