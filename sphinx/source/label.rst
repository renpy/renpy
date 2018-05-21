Labels & Control Flow
=====================

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
statement after the label statement whenever the end of the block is reached.

There are two kinds of labels: *global* and *local* labels. Global labels live
in one global scope shared across all project files and thus should have unique
names per game. Local labels logically reside inside the scope of the global label
they are declared in. To declare a local label, prefix its name with a period ``.``.
For example::

    label global_label:
        "Inside a global label.."
    label .local_name:
        "..resides a local one."
        jump .local_name

Local labels can be referenced directly inside the same global label they are
declared in or by their full name, consisting of global and local name parts: ::

    label another_global:
        "Now lets jump inside local label located somewhere else."
        jump global_label.local_name

The label statement may take an optional list of parameters. These parameters
are processed as described in PEP 3102, with two exceptions:

* The values of default parameters are evaluated at call time.
* The variables are dynamically, rather than lexically, scoped.

.. _jump-statement:

Jump Statement
--------------

The jump statement is used to transfer control to the given label.

If the ``expression`` keyword is present, the expression following it is
evaluated, and the string so computed is used as the label name of the
statement to jump to. If the ``expression`` keyword is not present, the label
name of the statement to jump to must be explicitly given.

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
string so computed is used as the name of the label to call. If the
``expression`` keyword is not present, the name of the statement to call must be
explicitly given.

If the optional from clause is present, it has the effect of including a label
statement with the given name as the statement immediately following the call
statement. An explicit label helps to ensure that saved games with return
stacks can return to the proper place when loaded on a changed script. ::

    e "First, we will call a subroutine."

    call subroutine

    call subroutine(2)

    call expression "subroutine" pass (count=3)

    # ...

    label subroutine(count=1):

        e "I came here [count] time(s)."
        e "Next, we will return from the subroutine."

        return

The call statement may take arguments, which are processed as described in :pep:`3102`.

When using a call expression with an arguments list, the ``pass`` keyword must
be inserted between the expression and the arguments list. Otherwise, the
arguments list will be parsed as part of the expression, not as part of the
call.

.. _return-statement:

Return Statement
----------------

The ``return`` statement pops the top statement off of the call stack, and transfers
control to it. If the call stack is empty, the return statement restarts
Ren'Py, returning control to the main menu.

If the optional expression is given to return, it is evaluated, and it's result
is stored in the ``_return`` variable. This variable is dynamically scoped to each
context.

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
    use to fix data when the game is updated.

``splashscreen``
    If it exists, this label is called when the game is first run, before
    showing the main menu.

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

Labels & Control Flow Functions
-------------------------------

.. include:: inc/label
