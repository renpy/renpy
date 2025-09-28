==================
Integrated Testing
==================

Ren'py allows creators to put tests in their games to make sure that an
alteration to the code didn't break the game.

The two main components of the testing system are the ``testcase`` and
``testsuite`` statements.

The :func:`renpy.is_in_test` function is helpful to know whether a test is currently
executing or not.


Testcase Statement
==================

The ``testcase`` statement creates a named test case. Each testcase contains a
block of test statements (see below). Testcases are similar to Ren'py
:ref:`labels <label-statement>`, with a few differences:

- The Ren'py label statement takes Ren'py code, while the testcase statement
  takes test statements (listed on this page). They are mutually exclusive.
- There is no testcase equivalent of the return statement.
- There can be no test statement outside of a testcase block, while there can be
  Ren'py code outside labels (in init blocks for example).

.. var:: skip = False

    Whether or not to skip the testcase. See :ref:`skipping-testcases`
    for more information.

Testsuite Statement
===================

The ``testsuite`` statement is a special variant of ``testcase`` that can be
used to group test cases together. Test suites may be nested inside each other,
and they can contain testcases, other testsuites, or both.

The default testsuite is named ``all``, and it is automatically created
by Ren'py. It contains all other top-level testcases in the game.

Hooks
-----
The ``testsuite`` statement can contain the following hooks:

.. describe:: before

    A block of test statements that is executed once, before the first
    testcase in the suite.

.. describe:: before_each

    A block of test statements that is executed repeatedly, before each testcase
    in the suite is run.

.. describe:: after_each

    A block of test statements that is executed repeatedly, after each testcase
    in the suite is run. The is run even if the testcase fails or raises an
    exception.

.. describe:: after

    A block of test statements that is executed once, after all the testcases
    in the suite are run. This is run even if the testcases fail or raise an
    exception.

.. note::

    When a testsuite finishes executing, the game doesn't close itself.
    Instead, it will return control of the game back to the player,
    awaiting user input.

    To close the game after a testsuite, you can use the ``exit`` test
    statement in the ``after`` hook of the testsuite. For example::

        testsuite global:
            teardown
                exit

        testcase default:
            click "Start"

Lifecycle Of A Test Run
=======================

To understand how testcases and testsuites are executed, it is helpful to
understand the lifecycle of a test. The following example illustrates this.

.. csv-table::
   :header: "Code", "Execution Order"
   :widths: 50, 50

   "::

        testsuite global:
            setup:
                pause until main_menu

            before testsuite:
                if not screen main_menu:
                    run MainMenu(confirm=False)
                click ""Start""

            testsuite basic:
                testcase first_testcase:
                    advance

            testsuite test_choices:
                setup:
                    run Jump(""chapter1"")

                before testcase:
                    advance until menu choice

                testcase choice1:
                    click ""First Choice""

                testcase choice2(enabled=False):
                    click ""Second Choice""

                testcase choice3:
                    click ""Third Choice""

                after testcase:
                    $ print(""Finished a choice test."")

                teardown
                    $ print(""Finished all choice tests."")

            after testsuite:
                if not screen main_menu:
                    run MainMenu(confirm=False)

            teardown
                exit

    ",".. container :: execution-block

            .. container :: execution-entry

                **global** :: before

            .. container :: execution-block2

                .. container :: execution-entry

                    **global** :: before testsuite

                .. container :: execution-block2

                    .. container :: execution-entry3

                        **simple** :: first_testcase

                .. container :: execution-entry

                    **global** :: after testsuite

            .. container :: execution-block2

                .. container :: execution-entry

                    **global** :: before testsuite

                .. container :: execution-entry2

                    **test_choices** :: before

                .. container :: execution-block2

                    .. container :: execution-entry2

                        **test_choices** :: before testcase

                    .. container :: execution-entry3

                        **test_choices** :: choice1

                    .. container :: execution-entry2

                        **test_choices** :: after testcase

                .. container :: execution-block2

                    .. container :: execution-entry2

                        **test_choices** :: before testcase

                    .. container :: execution-entry3

                        **test_choices** :: choice3

                    .. container :: execution-entry2

                        **test_choices** :: after testcase

                .. container :: execution-entry2

                    **test_choices** :: after

                .. container :: execution-entry

                    **global** :: after testsuite

            .. container :: execution-entry

                **global** :: after
    "

.. _skipping-testcases:

Skipping Testcases
------------------
If a testcase is skipped, it will not be executed. In addition, the
``before testcase`` and ``after testcase`` hooks of the testsuite will not be executed
for that testcase.

If *all* tests are skipped in the testsuite, then the ``before`` and
``after`` hooks of the testsuite will not be executed either. However, if
at least one test is not skipped, the ``before`` and ``after`` hooks will
run as usual.

Exceptions And Failures
-----------------------
If an error occurs during a test case:

1. The test case will stop executing immediately
2. The ``after testcase`` hook of the testsuite containing the test case will run
3. If there are more test cases, they will be executed next (including the
   ``before testcase`` hook)
4. If no more test cases exist, the ``after`` hook of the testsuite will run

If an error occurs during a hook (eg. ``before testcase``):

1. The test suite will stop executing immediately
2. If the suite was called by another suite, the parent suite will continue
   executing.
3. If no parent suite exists, the game will end the test run.


.. _test-clauses:

Basic Actions
=============

Clauses are defined by two things: what it does when they are executed, and
under what circumstances they are ready. They can be part of ``if``, ``assert``
or ``until`` test statements, or they can simply be given on their own (see
above).

.. for each one, say what makes it ready

Advance
--------------

Advances the game by one dialogue line. It is ready when the game can be
advanced by a click, and fails otherwise. ::

    advance
    advance until screen choice

Exit
--------------

.. TODO: Check if this is true

Quits the game without calling the confirmation screen.
Does not save the game when quitting::

    if eval need_to_confirm:
        run Quit(confirm=True) # asks for confirmation, and autosaves

    if eval persistent.quit_test_using_action:
        run Quit(confirm=False) # does not ask, but still autosaves

    exit # neither asks nor autosaves


Pass
--------------

Does not do anything. It's a no-op, allowing for empty testcases.

This clause is always ready. ::

    testcase not_yet_implemented:
        pass


Pause
---------------

Pauses test execution for a given number of seconds. Similar to the
:ref:`pause-statement`, but requires a value, or it can be specified without
a time if it is followed by an `until` clause.

This clause is always ready. ::

    pause 5.0
    pause until screen inventory


Python Blocks And Dollar-Lines
------------------------------

A :ref:`python block <python-statement>` or a :ref:`dollar-line` can be added
within a testcase. Unlike in normal Ren'py code, the python blocks don't take
the ``in substore`` parameter, but it does take the ``hide`` keyword. They
(both) allow execution of arbitrary python code.

Init code gets executed before the test occurs, so functions and classes defined
in ``init python`` blocks can be called in test python blocks and in test
dollar-lines. For example::

    init python in test:
        def afunction():
            if renpy.is_in_test():
                return "test"
            return "not test"

    testcase default:
        $ print(test.afunction()) # ends up in the console


Run
-------------

Runs the provided :doc:`screen-language action <screen_actions>` (or list of
actions).

Ready if and when a button containing the provided action (or list) would be
sensitive. ::

    testcase chapter_3:
        run Jump("chapter_3")


Skip
---------------

.. Update once the until condition is implemented

Enables skip mode, which allows the player to skip through the game
until the next dialogue line. This clause is always ready. ::

    skip
    skip until screen choice


.. _test-conditions:

Conditions
===================

Conditions are used to check whether a certain condition is true or not.
They are not executed, but they are used in condition-taking test statements
like ``if``, ``assert`` or ``until``.


Boolean Values
------------------

Test can use the literal boolean values ``True`` and ``False``.
These are always ready. :: ::

    if True:
        click "Start"

    if False:
        click "Start" # does not execute, since the condition is always false



Boolean Operations
------------------

.. csv-table::
   :header: "Command", "Used as condition", "Can be executed", "Takes selector"
   :widths: 40, 20, 20, 20

    "advance", "no", "yes", "no"
    "exit", "no", "yes", "no"
    "pass", "no", "yes", "no"
    "run", "no", "yes", "no"
    "skip", "no", "yes", "no"

    "not", "yes", "no", "yes"
    "and", "yes", "no", "yes"
    "or", "yes", "no", "yes"
    "eval", "yes", "no", "yes"
    "True", "yes", "no", "no"
    "False", "yes", "no", "no"
    "label", "yes", "no", "no"
    "screen", "yes", "no", "no"
    "id", "yes", "no", "no"
    "pattern", "yes", "no", "no"

    "if", "no", "no", "yes"
    "elif", "no", "no", "yes"
    "assert", "no", "no", "yes"
    "until", "no", "no", "yes"
    "repeat", "no", "no", "yes"

    "click", "no", "yes", "yes"
    "move", "no", "yes", "yes"
    "scroll", "no", "yes", "yes"
    "drag", "no", "yes", "yes"
    "keysym", "no", "yes", "yes"
    "type", "no", "yes", "yes"

Test clauses support the ``not``, ``and`` and ``or`` operators.
That expression may or may not be enclosed in parentheses.

The readiness of a boolean clause expression is the computation of the readiness
of the clauses it contains:

- ``(not a)`` is ready if and when ``a`` is not ready
- ``(a and b)`` is ready when both ``a`` and ``b`` are ready
- ``(a or b)`` is ready when either ``a`` or ``b`` is ready.

.. _test-eval-clause:

Eval
-----------

This clause is ready if and when the provided expression evaluates to a true
value, in a boolean context.

This clause exists only to be used inside condition-taking test
statements like ``assert``, ``if`` or ``until``. ::

    assert eval (renpy.is_in_test() and ("Ren'py" in renpy.version_string))

.. note::

    Differences between a dollar-line and the eval clause :

    - Eval cannot be used on a line by itself, it must be used inside a
      statement like ``if`` or ``until``, while dollar-lines must be on
      their own line.
    - A dollar-line executes any python statement, which does not necessarily
      have a value - for example ``$ import math`` - while the eval clause
      requires a return value.


..

Label
---------------

The label clause is ready if and when the provided label has been passed between
the current test statement and the one just before.

Considering the following example::

    run Jump("chapter_1")
    assert label chapter_1 # works
    assert label chapter_1 # fails

The first ``assert`` statement works because the label ``chapter_1`` has been
reached by the ``run Jump("chapter_1")`` statement. The second ``assert``
statement fails because the label ``chapter_1`` has not been reached again
since the first ``assert`` statement.

That also means the following example will not work::

    run Jump("chapter_1")
    advance repeat 3
    assert label chapter_1 # fails

It fails because no renpy label will have been reached between the
``advance`` statement and the ``assert`` statement.

.. warning::

    This clause should not be confused with the Ren'py native
    :ref:`label <label-statement>` statement it refers to, or with the unrelated
    :ref:`label element <sl-label>` used in screens.



Selector Statements
===================

Selector statements are used to check if a certain element is on the screen,
and to use that element for further actions.

Selectors are a special kind of condition.

Displayable Selector
--------------------

Check if a screen or element with given id is currently displayed.

It takes one parameter, the name of the screen. It takes the following properties:

.. TODO: Which ones need quotes, which ones don't?

.. describe:: screen

    The name of the screen to check.

.. describe:: id

    The id of the element to check.

.. describe:: layer

    The layer on which the screen is displayed. If not given, the layer is
    automatically determined by the screen name.

::

    if screen main_menu:
        click "Start"

    advance until screen choice

    click "Close" until not id "close_button"



.. _test-text-selector:

Text Selector
-------------

The ``text`` selector takes a string (except in the case of the string
expression clause, where it is the string itself) which resolves to a target
found on the screen, based on the shortest match among the alt text of focusable
screen elements (typically, buttons). The search is case-insensitive.

If no text is given, the virtual test mouse is positioned to the last
previous location where a click happened, or to the specified position, if any.
If that position lies on a focusable element, a random position in the screen
which does not overlap a focusable element is chosen instead.

If text is given, the mouse is positioned to the last previous location
where a click happened, or to the specified position, if any. If that position
does not lie inside the targeted element, a random position within it is chosen
instead. To that end, things like :propref:`focus_mask` are taken into account.

If text is given and if it does not resolve to a target at the time when
the clause using it executes, an exception is raised (terminating the test). To
test whether a given text resolves to a target at a given time, the readiness
condition of a string expression clause can be evaluated inside an if statement::

    if "ask her right": # if there is a focusable element containing that text on screen
        # add a clause using that text




Selector-Driven Actions
=======================

Action statements are used to perform actions in the game, such as clicking
buttons, pressing buttons, or scrolling menus.

Click
---------------

Executes a simulated click on the screen. It takes the following optional
properties:

- ``button`` specifies which button of the simulated mouse is to be clicked
  with. It takes an integer and defaults to 1. 1 is a left-click, 2 is a
  right-click, 3 is a middle-click, 4 and 5 are additional buttons found on
  some mouses. Normally only 1 and 2 trigger any response from Ren'py.
- ``pos`` specifies where to click, as a pair of x/y coordinates. Coordinates
  are taken relative to the screen. Floats between 0.0 and 1.0 are supported as
  a fraction of the screen size in either dimension. ``absolute`` and other
  means of expressing positions are not supported, since you can't move the
  mouse to a subpixel-precise position.

.. ``always`` is not documented because useless in the case of the click clause by itself

Click behaves like a :ref:`pattern <test-text-selector>`\ -taking clause which would
not be given a pattern: if no ``pos`` is provided, it will look for a neutral
place where a click would not occur on a focusable element.

.. give example for both

This clause is always ready.

Drag
--------------

..
    simulate the mouse dragging something from one place to another
    by maintaining click blabla
    takes an iterable of points to follow as an itinerary
    each point must be given as a pair of x/y coordinates, or None
    each occurrence of None will be replaced with a coordinate within the focused area of the screen
    (the position of the virtual test mouse if already inside it, or a random position within if not)
    needs to be given at least two points
    ready if the thing it has been told to type in is found, or if no target has been given
    show example of ((None, 10), (None, 100)) being an only-vertical movement downwards


Keysym
--------------

A keysym is a string that represents a key on the keyboard. It can be used
to simulate a key press in the game. The keysym can be a single key, such
TODO

Move
--------------

..
    `move (position) [pattern (string)]`
    moves the virtual test mouse to the provided position, within the area targeted by the pattern
    or, if none is given, within the whole screen

..
    It is ready if a pattern is not provided,
    or if one is provided and a suitable target is found on the screen.
    For the clauses taking the ``always`` property, that property overrides the readiness of the clause.


Scroll
----------------

..
    takes a string giving it a pattern
    ready when the target (pattern) is found
    If the target is a bar, scrolls it down a page. If already at the bottom, returns it to the top.

Type
--------------

.. simulate a key-pressing or the typing of text

..
    It is ready if a pattern is not provided,
    or if one is provided and a suitable target is found on the screen.
    For the clauses taking the ``always`` property, that property overrides the readiness of the clause.

..
    warning disambiguation this has nothing to do with the python builtin




Control Statements
==================

These statements control the flow of the test execution.

Assert
----------------

This statement takes a :ref:`clause <test-clauses>` and raises a
RenpyTestAssertionError if the clause is not ready at the time when
the assert statement executes. ::

    assert screen main_menu
    assert eval some_function(args)

.. seealso::

    - `Python asserts <https://docs.python.org/reference/simple_stmts.html#the-assert-statement>`__
    - `Boolean evaluation <https://docs.python.org/library/stdtypes.html#truth-value-testing>`__



If
------------

This statement, like a python ``if`` statement, takes a block.

Unlike the Ren'py or python versions however, it only takes a
:ref:`test clause <test-clauses>`, instead of a general python expression.
The provided clause being ready is the actual condition for the block to execute
or not.

Example::

    if label "chapter_five":
        exit

A normal python/renpy ``if`` can be replicated using the :ref:`test-eval-clause`. ::

    if eval (persistent.should_advance and i_should_advance["now"]):
        advance

The ``elif`` and ``else`` statements can be used to add
additional conditions to the ``if`` statement. ::

    if eval persistent.should_advance:
        advance
    elif eval i_should_advance["now"]:
        advance
    else:
        click "Start"


Repeat
----------------

Repeats a statement for a given number of times. It consists a
:ref:`clause <test-clauses>` and a number of repetitions,
separated by the word ``repeat``. ::

    click "+" repeat 3
    keysym "K_BACKSPACE" repeat 10
    advance repeat 3



Until
---------------

Repeats a statement until a condition is met. It consists of a
:ref:`clause <test-clauses>` and a condition,
separated by the word ``until``.

If and when the clause on the right is ready, control is
passed to the next statement. Otherwise, the left clause is executed until the
right clause is ready.

This is basically an inline while loop. ::

    advance until screen choice
    "ask her right away"
    advance until "It's an interactive book."
