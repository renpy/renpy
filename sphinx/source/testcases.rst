==================
Automated Testing
==================

Ren'Py allows creators to put automated tests in their games to make sure that
alterations to the game don't break existing functionality. This is especially
useful for large games, or for games that are frequently updated.

The two main components of the testing system are the ``testcase`` and
``testsuite`` statements.

The :func:`renpy.is_in_test` function is helpful to know whether a test is currently
executing or not.

.. _testcase-statement:

Testcase Statement
==================

The ``testcase`` statement creates a named test case. Each case contains a
block of test statements (see below). Test cases are similar to Ren'Py
:ref:`labels <label-statement>`, with a few differences:

- The Ren'Py label statement takes Ren'Py code, while the testcase statement
  takes test statements (listed on this page). They are mutually exclusive.
- There is no testcase equivalent of the return statement.
- There can be no test statement outside of a test block, while there can be
  Ren'Py code outside labels (in init blocks for example).

It takes the following properties:

.. var:: description

    A string describing the test case. This is used in the test report.

.. var:: enabled

    If this expression evaluates to ``False``, this test is skipped.
    Defaults to ``True``.

    This can conditionally disable tests, for example on platforms
    where they are not supported. ::

        testcase windows:
            enabled renpy.windows
            ...

        testcase not_on_mobile:
            enabled not renpy.mobile
            ...

    See :ref:`skipping-testcases` for more information.

.. var:: only

    If this expression evaluates to ``True``, only this test case
    (and other tests with ``only True``) will be run. Defaults to ``False``.

    See :ref:`skipping-testcases` for more information.

.. var:: xfail

    If this expression evaluates to ``True``, the test is expected to fail.
    If the test does fail, it will be marked as xfailed instead of failed.
    Defaults to ``False``.

.. var:: parameter

    A variable name (or tuple of variable names) and a list of values (or
    list of tuples of values). The test will run once for each value (or
    tuple of values) in the list.

    A test may have multiple ``parameter`` properties, in which case
    the test will run for every possible combination of the values.

    See :ref:`parameterized-tests` for more information.


Testsuite Statement
===================

The ``testsuite`` statement is used to group test cases together. Test suites
can contain test cases, other test suites, and hooks (see below).

The default test suite is named ``global``, and it is automatically created
by Ren'Py if not specified by the user. It contains all other top-level test suites
and test cases in the game.

It takes the same properties as the :ref:`testcase statement <testcase-statement>`.

Hooks
-----
The ``testsuite`` statement can contain the following hooks:

.. describe:: setup

    A block of test statements that is executed once, before running any tests
    contained within the current suite.

.. describe:: before testsuite

    A block of test statements that is executed repeatedly, running before each test suite
    within the current suite.

.. describe:: before testcase

    A block of test statements that is executed repeatedly, running before each test case
    within the current suite.

.. describe:: after testcase

    A block of test statements that is executed repeatedly, running after each test case
    in the current suite. The is run even if the testcase fails or raises an
    exception.

.. describe:: after testsuite

    A block of test statements that is executed repeatedly, running after each test suite
    in the current suite. The is run even if the testsuite fails or raises an
    exception.

.. describe:: teardown

    A block of test statements that is executed once, after running all tests
    contained within the current suite. This is run even if a test
    fails or raises an exception.

The ``before *`` and ``after *`` hooks take the following properties:

.. var:: depth

    An integer specifying how deep the hook should apply.

    For testcases, defaults to ``-1``, meaning it applies to all nested test suites and test cases.

    For testsuites, defaults to ``0``, meaning it applies only to test suites directly
    contained within the current suite.

    For more information, see :ref:`lifecycle-of-a-test-run`.

.. _lifecycle-of-a-test-run:

Lifecycle of a Test Run
=======================

This section describes the order in which testcases and testsuites are
executed, and how the hooks are called. The following example illustrates this:

.. csv-table::
   :header: "Code", "Execution Order"
   :widths: 50, 50

   "::

        testsuite global:
            # Hooks
            setup:
                skip until main_menu

            before testsuite:
                if not screen ""main_menu"":
                    run MainMenu(confirm=False)
                click ""Start""

            before testcase:
                $ print(""Starting a testcase."")

            after testcase:
                $ print(""Finished a testcase."")

            after testsuite:
                $ print(""Finished a testsuite."")

            teardown
                exit

            # Subtests
            testsuite basic:
                testcase first_testcase:
                    advance

            testsuite test_choices:
                # Hooks
                setup:
                    run Jump(""chapter1"")

                before testcase:
                    advance until menu choice

                after testcase:
                    $ print(""Finished a choice test."")

                teardown
                    $ print(""Finished all choice tests."")

                # Subtests
                testcase choice1:
                    click ""First Choice""

                testcase choice2(enabled=False):
                    click ""Second Choice""

                testcase choice3:
                    click ""Third Choice""


    ",".. container :: execution-block

            .. container :: execution-entry

                **global** :: setup

            .. container :: execution-block2

                .. container :: execution-entry

                    **global** :: before testsuite

                .. container :: execution-block2

                    .. container :: execution-entry2

                        **global** :: before testcase

                    .. container :: execution-entry3

                        **simple** :: first_testcase

                    .. container :: execution-entry2

                        **global** :: after testcase

                .. container :: execution-entry

                    **global** :: after testsuite

            .. container :: execution-block2

                .. container :: execution-entry

                    **global** :: before testsuite

                .. container :: execution-entry2

                    **test_choices** :: setup

                .. container :: execution-block2

                    .. container :: execution-entry2

                        **global** :: before testcase

                    .. container :: execution-entry2

                        **test_choices** :: before testcase

                    .. container :: execution-entry3

                        **test_choices** :: choice1

                    .. container :: execution-entry2

                        **test_choices** :: after testcase

                    .. container :: execution-entry2

                        **global** :: after testcase

                .. container :: execution-block2

                    .. container :: execution-entry2

                        **global** :: before testcase

                    .. container :: execution-entry2

                        **test_choices** :: before testcase

                    .. container :: execution-entry3

                        **test_choices** :: choice3

                    .. container :: execution-entry2

                        **test_choices** :: after testcase

                    .. container :: execution-entry2

                        **global** :: after testcase

                .. container :: execution-entry2

                    **test_choices** :: teardown

                .. container :: execution-entry

                    **global** :: after testsuite

            .. container :: execution-entry

                **global** :: teardown
    "

Note that ``global :: before testcase`` and ``global :: after testcase`` are
executed before and after each test case, even if the test case is inside a
nested test suite.

In order to limit the scope of a hook, set its ``depth`` property.
Setting it to ``0`` will make the hook execute only for tests
directly inside the test suite containing the hook.

For example::

    testsuite global:
        before testcase:
            depth 0
            $ print("Starting a testcase.")

On the other hand, the ``before testsuite`` and ``after testsuite`` hooks
have a default ``depth`` of ``0``, meaning they will only execute for testsuites
directly inside the testsuite containing the hook.

To increase the scope of a hook to include nested testsuites and testcases,
set its ``depth`` property to ``-1`` (for infinite depth) or to a positive
integer (for a specific depth).

.. note::

    When a testsuite finishes executing, the game doesn't close itself.
    Instead, it will return control of the game back to the player,
    awaiting user input.

    To close the game after a testsuite, you can use the ``exit`` test
    statement in the ``after`` hook of the testsuite. For example::

        testsuite global:
            teardown
                exit

.. _skipping-testcases:

Skipping Testcases
------------------
If a testcase is skipped, it will not be executed. In addition, the
``before testcase`` and ``after testcase`` hooks of the testsuite will not be executed
for that testcase.

If *all* tests are skipped in a testsuite, then the ``setup`` and
``teardown`` hooks will not be executed either. In addition, the
``before testsuite`` and ``after testsuite`` hooks will not be executed from
the parent testsuite(s).

.. _parameterized-tests:

Parameterized Tests
--------------------

A test case can run multiple times with different values by using the ``parameter`` property.

To do this, give a variable name and a list of values. The test will run once
for each value in the list. For example::

    testcase example:
        parameter x = [1, 2, 3]
        assert eval (x > 0)

This will run the test three times: once with ``x = 1``, once with ``x = 2``,
and once with ``x = 3``.

Each run will execute the ``before testcase`` and ``after testcase`` hooks,
and each test is reported separately in the test report.

Grouped Parameters
^^^^^^^^^^^^^^^^^^

It is possible to specify several variables at once by grouping them
in parentheses and giving a list of value groups. For example::

    testcase addition:
        parameter (x, y, z) = [ (1, 2, 3), (2, 3, 5), (3, 5, 8) ]

        assert eval (x + y == z)

This will run three times, each time using one set of values:
``(1, 2, 3)``, ``(2, 3, 5)``, and ``(3, 5, 8)``.

Parameter Combinations
^^^^^^^^^^^^^^^^^^^^^^

If multiple ``parameter`` properties are provided, the test case will run
for every possible combination of the values. For example::

    testcase combinations:
        parameter a = [1, 2]
        parameter b = [3, 4]
        parameter c = [5, 6]

        assert eval (a + b + c in [9, 10, 11, 12])

This will run eight times, once for each combination of ``(a, b, c)``:

    ``(1, 3, 5)``, ``(1, 3, 6)``, ``(1, 4, 5)``, ``(1, 4, 6)``, ``(2, 3, 5)``, ``(2, 3, 6)``, ``(2, 4, 5)``, ``(2, 4, 6)``

It is possible to mix grouped parameters with non-grouped parameters. For example::

    testcase mixed:
        parameter a = [1, 2]
        parameter (b, c) = [ (3, 5), (4, 6) ]

        assert eval (a + b + c in [9, 10, 11, 12])

This will run four times, using these combinations for ``(a, (b, c))``:

    ``(1, (3, 5))``, ``(1, (4, 6))``, ``(2, (3, 5))``, ``(2, (4, 6))``


Selective Enable and Xfail
^^^^^^^^^^^^^^^^^^^^^^^^^^

If a parameterized test case has its ``enabled`` property evaluate to ``False``,
that particular run will be skipped, but other runs will continue to execute.

Similarly, if the ``xfail`` property evaluates to ``True``, that particular
run will be marked as xfailed if it fails, but other runs will pass or fail normally.

For example, the following test will pass for ``x=0`` and ``x=1``, and will xfail for ``x=2``::

    testcase choice_test:
        parameter x = [0, 1, 2]
        xfail x == 2

        assert eval (x < 2)


Test Suites
^^^^^^^^^^^
Parameters can also be provided to the whole test suite. In this case, all hooks and test cases
inside the suite will run once for each parameter set.

Each parameterized run will execute the ``setup``, ``before/after testsuite``,
and ``teardown`` hooks.

For example::

    testsuite math_tests:
        parameter (x, y, z) [ (1, 2, 3), (2, 3, 5), (3, 5, 8) ]

        setup:
            $ print(f"Running math tests with x={x}, y={y}, z={z}")

        testcase addition:
            assert eval (x + y == z)

        testcase multiplication:
            assert eval (x*y == z*y - y*y)

Parameters may be nested, and all combinations will be tested. For example::

    testsuite parameter_field:
        parameter choice_text = ["first", "second"]

        testcase param_test2:
            parameter (x, y) = [(0.0, 0.0), (0.5,0.5)]

            advance until screen "choice"
            click choice_text
            click pos (x, y)

This will run four times, once for each combination of ``(choice_text, (x, y))``:

    ``("first", (0.0, 0.0))``, ``("first", (0.5, 0.5))``,
    ``("second", (0.0, 0.0))``, ``("second", (0.5, 0.5))``

.. warning::

    Test parameters are passed directly to tests, without any copying. If you change
    a parameter that is mutable (eg. a list or dictionary) inside a test, that change
    will affect other tests using the same object.

Exceptions And Failures
-----------------------
If an error occurs during a test case:

1. The test case will stop executing immediately
2. The ``after testcase`` hook of the testsuite containing the test case will run
3. If there are more test cases, they will continue to be executed (including the
   ``before testcase`` hook)
4. If no more test cases exist, the ``after`` hook of the testsuite will run

If an error occurs during a hook (eg. ``before testcase``):

1. The test suite will stop executing immediately
2. If the suite was called by another suite, the parent suite will continue
   executing.
3. If no parent suite exists, the game will end the test run.

Test Launch Options
===================

The test system accepts the following :doc:`command-line options <cli>`:

.. option:: --enable_all

    If provided, all test cases and test suites will be executed, regardless
    of their ``enabled`` property.

.. option:: --overwrite_screenshots

    If provided, existing screenshots will be overwritten when a
    :ref:`screenshot statement <test-screenshot-statement>` is executed.

.. option:: --hide-header

    If provided, the header at the start of the test run will be disabled.

.. option:: --hide-execution [no|hooks|testcases|all]

    If provided, test execution output will be hidden. ``hooks`` hides hooks,
    ``testcases`` hides test cases and hooks, and ``all`` hides everything.

.. option:: --hide-summary

    If provided, the summary at the end of the test run will be disabled.

.. option:: --report-detailed

    If provided, detailed information about each test will be shown during
    the run.

.. option:: --report-skipped

    If provided, information about skipped tests will be shown. This option
    should be used together with ``--report-detailed``.


Test Reporting
===================

After a test run, a report is printed to the console, listing all test cases
and their results. If the ``--print_details`` option is provided, the report
will include additional information about each test.

Below is an example of a test report after successfully testing "The Question":

.. image :: testcases_the_question.png
    :alt: Test report example
    :class: screenshot

Test results
------------

A test can have one of the following results:

- **Passed**: The test executed successfully, without any errors.
- **Failed**: The test executed, but one of the statements failed.
- **XFailed**: The test was expected to fail (because its ``xfail``
  property evaluated to ``True``), and it did fail.
- **XPassed**: The test was expected to fail (because its ``xfail``
  property evaluated to ``True``), but it passed instead.
- **Skipped**: The test was skipped, either because its ``enabled``
  property evaluated to ``False``, or because another test with ``only True``
  exists.

In general, a test is considered successful if it passed or xfailed,
and unsuccessful if it failed or xpassed.

Test Settings
=================

The following variables can be set to change the behavior of tests:

.. var:: _test.maximum_framerate

    A boolean specifying whether to use maximum framerate mode during tests.
    This will unlock the framerate beyond your screens refresh rate if possible.
    Defaults to ``True``.

.. var :: _test.timeout

    A float specifying the maximum number of seconds a test statement
    should wait for a condition to be met. Defaults to ``10.0``.

    This can be overridden on a per-statement basis by providing a ``timeout``
    property to statements that support it (like ``assert`` and ``until``).

.. var:: _test.force

    A boolean specifying whether to force the test to proceed even if
    ``renpy.config.suppress_underlay`` is ``True``. Defaults to ``False``.

.. var:: _test.transition_timeout

    A float specifying the maximum number of seconds to wait for a transition
    to complete before skipping it and proceeding with the test.
    Defaults to ``5.0``.

.. var:: _test.focus_trials

    An integer specifying how many times the test system should try to find
    a valid spot to :ref:`move the mouse <test-move-statement>` when using a
    selector without a position. Defaults to ``100``.

.. var:: _test.screenshot_directory

    A string specifying the directory to store screenshots in.
    Defaults to ``tests/screenshots``.


.. _test-statements:

Test Statements
===============

Test statements are the building blocks of test cases. They can be broadly
divided into three categories: command statements, condition/selector statements, and
control statements.

Basic Commands
--------------

.. _test-advance-statement:

Advance
^^^^^^^^^^

    Type: :dfn:`Command`

    .. describe:: advance

Advances the game by one dialogue line. ::

    advance
    advance until screen "choice"


Exit
^^^^^^^^^^

    Type: :dfn:`Command`

    .. describe:: exit

Quits the game without calling the confirmation screen.
Does not save the game when quitting. ::

    if eval need_to_confirm:
        # Asks for confirmation, and autosaves if config.autosave_on_quit is True
        run Quit(confirm=True)

    if eval persistent.quit_test_using_action:
        # Does not ask, but still autosaves if config.autosave_on_quit is True
        run Quit(confirm=False)

    exit # neither asks nor autosaves

Pass
^^^^^^^^^^

    Type: :dfn:`Command`

    .. describe:: pass

Does not do anything. It's a no-op, allowing for empty testcases. ::

    testcase not_yet_implemented:
        pass

Pause
^^^^^^^^^^

    Type: :dfn:`Command`

    .. describe:: pause [time (float)]

Pauses test execution for a given number of seconds. Similar to the
:ref:`pause-statement`, but requires a value, or it can be specified without
a time if it is followed by an `until` clause. ::

    pause 5.0
    pause until screen "inventory"

Run
^^^^^^^^^^

    Type: :dfn:`Command`

    .. describe:: run <action>

Runs the provided :doc:`screen-language action <screen_actions>` (or list of
actions).

Ready if and when a button containing the provided action (or list) would be
sensitive. ::

    testcase chapter_3:
        run Jump("chapter_3")

.. _test-skip-statement:

Skip
^^^^^^^^^^

    Type: :dfn:`Command`

    .. describe:: skip [fast]

Causes the game to begin skipping. If the game is in a menu context,
then this returns to the game. Otherwise, it just enables skipping.

If ``fast`` is provided, the game will skip directly to the next menu choice.

::

    skip
    skip fast
    skip until screen "choice"


Mouse Commands
----------------

Click
^^^^^^^^^^

    Type: :dfn:`Command`

    .. describe:: click [button (int)] [selector] [pos (x, y)]

Executes a simulated click on the screen. It takes the following optional
properties:

- ``button`` specifies which button of the simulated mouse is to be clicked
    with. It takes an integer and defaults to 1. 1 is a left-click, 2 is a
    right-click, 3 is a middle-click, 4 and 5 are additional buttons found on
    some mouses. Normally only 1 and 2 trigger any response from Ren'Py.

If ``selector`` and/or ``pos`` are given, the virtual test mouse is moved according to
the rules of the :ref:`move statement <test-move-statement>` before the click is sent.

.. ``always`` is not documented because useless in the case of the click clause by itself

Click behaves like a :ref:`pattern <test-text-selector>`\ -taking clause which would
not be given a pattern: if no ``pos`` is provided, it will look for a neutral
place where a click would not occur on a focusable element.

.. give example for both

.. note::

    Use the :ref:`advance <test-advance-statement>` or :ref:`skip <test-skip-statement>`
    statements if you want to advance the game's dialogue.
    Clicking may result in unpredictable results, depending on where the mouse
    is positioned and what is currently on the screen.

Drag
^^^^^^^^^^

    Type: :dfn:`Command`

    .. describe:: drag <[selector] [pos (x, y)]> to <[selector] [pos (x, y)]> [button (int)] [steps (int)]

Simulates a drag action on the screen. It takes the following properties:

- The first part (before the ``to``) specifies the starting point of the drag.
  It takes an optional ``selector`` and/or ``pos`` property, which are
  interpreted according to the rules of the :ref:`move statement <test-move-statement>`.
- The second part (after the ``to``) specifies the ending point of the drag.
  It also takes an optional ``selector`` and/or ``pos`` property, which are
  interpreted according to the rules of the :ref:`move statement <test-move-statement>`.
- ``button`` specifies which button of the simulated mouse is to be used
  for the drag. It takes an integer and defaults to 1. 1 is a left-click, 2 is a
  right-click, 3 is a middle-click, 4 and 5 are additional buttons found on
  some mouses. Normally only 1 and 2 trigger any response from Ren'Py.
- ``steps`` specifies how many intermediate steps the drag should take.
  It takes an integer and defaults to `10`. More steps result in a smoother
  drag, but also take more time.

::

    drag id "item_icon" to id "inventory_slot_3" button 1 steps 20
    drag pos (100, 200) to pos (400, 500) button 1
    drag id "item_icon" pos (0.5, 0.5) to pos (300, 400) steps 5
    drag pos (50, 50) to id "inventory_slot_1"
    drag pos (50, 50) to pos (150, 150)

.. _test-move-statement:

Move
^^^^^^^^^^

    Type: :dfn:`Command`

    .. describe:: move [selector] [pos (x, y)]

Moves the virtual test mouse to a given position on the screen.

If a ``selector`` is given, and:

- If ``pos`` is specified, the mouse is moved to that position relative to the selector.
- If no ``pos`` is specified, the mouse attempts to find a pixel that would focus the
  selector if clicked. This takes into account things like :propref:`focus_mask`.

If no ``selector`` is given, and:

- If ``pos`` is specified, the mouse is moved to that position relative to the screen.
- If no ``pos`` is specified, an error is thrown.

::

    # Move to a random clickable point within `back_btn`
    move id "back_btn"

    # Move to the center of `back_btn`
    move id "back_btn" pos (0.5, 0.5)

    # Move to a point 20 pixels right and 10 pixels down from the top-left corner of `back_btn`
    move id "back_btn" pos (20, 10)

    # Move to the top right corner of the screen
    move pos (1.0, 0.0)

    # Move to a point 20 pixels right and 10 pixels down from the top-left corner of the screen
    move pos (20, 10)

Scroll
^^^^^^^^^^

    Type: :dfn:`Command`

    .. describe:: scroll [amount (int)] [selector] [pos (x, y)]

Simulates a scroll event. It takes the following optional properties:

- ``amount`` specifies how many "notches" to scroll. It takes an integer
  and defaults to ``1``. Positive values scroll down, negative values scroll up.
- If ``selector`` and/or ``pos`` are given, the virtual test mouse is moved according to
  the rules of the :ref:`move statement <test-move-statement>` before the scroll is sent.

::

    scroll "bar"
    scroll id "inventory_scroll"
    scroll amount 10 id "inventory_scroll" pos (0.5, 0.5)
    scroll # scrolls down at the current mouse position

.. note::

    This only simulates the mousewheel event. You may consider using
    the Scroll action from :doc:`screen_actions`. ::

        run Scroll("inventory_scroll", "increase", amount="step", delay=1.0)

Keyboard Commands
-----------------

Keysym
^^^^^^^^^^

.. _test-keysym-statement:

    Type: :dfn:`Command`

    .. describe:: keysym <keysym> [selector] [pos (x, y)]

Simulate a keysym event. This includes the keys of :doc:`config.keymap <keymap>`.

If ``selector`` and/or ``pos`` are given, the virtual test mouse is moved according to
the rules of the :ref:`move statement <test-move-statement>` before the keysym is sent.

::

    keysym "skip"
    keysym "help"
    keysym "ctrl_K_a"
    keysym "K_BACKSPACE" repeat 30
    keysym "pad_a_press"

.. _test-type-statement:

Type
^^^^^^^^^^

    Type: :dfn:`Command`

    .. describe:: type <string> [selector] [pos (x, y)]

Types the provided string as if it was typed on the keyboard.

If ``selector`` and/or ``pos`` are given, the virtual test mouse is moved according to
the rules of the :ref:`move statement <test-move-statement>` before the text is sent.

::

    type "Hello, World!"

.. _test-conditions:

Condition Statements
--------------------

Conditions are used to check whether a certain condition is true or not.
They are used in condition-taking test statements
like ``if``, ``assert`` or ``until``.


Boolean Values
^^^^^^^^^^^^^^^^

Tests can use the literal boolean values ``True`` and ``False``.
These are always ready. ::

    if True:
        click "Start"

    if False:
        click "Settings" # does not execute, since the condition is always false


Boolean Operations
^^^^^^^^^^^^^^^^^^

    Conditions support the ``not``, ``and`` and ``or`` operators.
    That expression may or may not be enclosed in parentheses. ::

        assert eval (renpy.is_in_test() and screen "main_menu")
        advance until "ask her right" or label "chapter_five"
        click "Next" until not screen "choice"

.. _test-eval-statement:

Eval
^^^^^^^^^

    Type: :dfn:`Condition`

    .. describe:: eval <expression>

Evaluates the provided python expression. This exists only to be used inside condition-taking test
statements like ``assert``, ``if`` or ``until``. ::

    assert eval (renpy.is_in_test() and ("Ren'Py" in renpy.version_string))

.. note::

    Differences between a dollar-line and the eval clause:

    - Eval cannot be used on a line by itself, it must be used inside a
      statement like ``if`` or ``until``, while dollar-lines must be on
      their own line.
    - A dollar-line executes any python statement, which does not necessarily
      have a value - for example ``$ import math`` - while the eval clause
      requires a return value.

Label
^^^^^^^^^

    Type: :dfn:`Condition`

    .. describe:: label <labelname>

Checks if the provided Ren'Py label has been reached since the last time
a test statement was executed.

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

.. warning::

    This test statement should not be confused with the Ren'Py native
    :ref:`label <label-statement>` statement it refers to, or with the unrelated
    :ref:`label element <sl-label>` used in screens.

Selector Statements
-------------------

Selector statements are used to check if a certain element is on the screen,
and to use that element for further actions.

Selectors are a special kind of condition.

Displayable Selector
^^^^^^^^^^^^^^^^^^^^

    Type: :dfn:`Condition, Selector`

Check if a screen or element with given id is currently displayed.

It takes one parameter, the name of the screen. It takes the following properties:

    .. TODO: Which ones need quotes, which ones don't?

    .. describe:: screen <name>

        The name of the screen to check.

    .. describe:: id <name>

        The id of the element to check.

    .. describe:: layer <name>

        The layer on which the screen is displayed. If not given, the layer is
        automatically determined by the screen name.

::

    if screen "main_menu":
        click "Start"

    advance until id "inventory_viewport" layer "overlay"

    click "Close" until not id "close_button"


.. _test-text-selector:

Text Selector
^^^^^^^^^^^^^^^^^^^^

    Type: :dfn:`Condition, Selector`

    .. describe:: "<text>"

The ``text`` selector takes a string which resolves to a target
found on the screen. The search is performed by going through all focusable
elements on the screen (which are typically buttons and the main textbox),
and looking through their :propref:`alt` text.


This search is case-insensitive and looks for the shortest match.
For example, if the string ``"log"`` is given, and the screen contains
the texts ``"CATALOG"`` and ``"illogical"``, the target
will be the ``"CATALOG"`` text.


::

    # This may be in a button
    skip until "Start Game"

    # This may be in the main textbox
    advance until "Hey, that's not fair!"

    # Case-insensitive search
    assert "AsK HeR RighT AwaY"


Control Statements
------------------

These statements control the flow of the test execution.

Assert
^^^^^^^^^^

    Type: :dfn:`Control`

    .. describe:: assert <condition> [timeout (float)] [xfail (bool)]

This statement takes a condition and raise a
RenpyTestAssertionError if the condition is not met at the time when
the assert statement executes.

If a ``timeout`` is given, the statement will wait up to that many seconds
for the condition to be met. If the condition is not met within that time,
the assertion fails.

If ``xfail`` is set to ``True``, the assert statement is expected to fail.
This inverts the meaning of the statement: if the condition is met, the
assertion fails. If the condition is not met, the assertion passes.

::

    assert screen "main_menu"
    assert eval some_function(args)
    assert id "start_button" timeout 5.0

.. seealso::

    - `Python asserts <https://docs.python.org/reference/simple_stmts.html#the-assert-statement>`__
    - `Boolean evaluation <https://docs.python.org/library/stdtypes.html#truth-value-testing>`__


If
^^^^^^^^^

    Type: :dfn:`Control`

    .. describe:: if <condition>

This statement executes a block of test statements if and when the provided
condition is met.

Example::

    if label "chapter_five":
        exit

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
^^^^^^^^^

    Type: :dfn:`Control`

    .. describe:: <command> repeat <number> [timeout (float)]

Repeats a statement for a given number of times. It consists of an
Command statement on the left-hand side and a number of repetitions
on the right-hand side, separated by the word ``repeat``. ::

    click "+" repeat 3
    keysym "K_BACKSPACE" repeat 10
    advance repeat 3

.. _test-screenshot-statement:

Screenshot
^^^^^^^^^^

    Type: :dfn:`Command`

    .. describe:: screenshot <path> [max_pixel_difference (int or float)] [crop (x1, y1, x2, y2)]

Takes a screenshot of the current screen and saves it to the provided path.

- ``path`` specifies the path (relative to ``_test.screenshot_directory``)
  where the screenshot will be saved. It may include a file extension.
  Only ``.png`` is supported.
- ``max_pixel_difference`` specifies how many pixels may differ between
  the taken screenshot and an existing screenshot for the test to pass.
  Integer values specify the number of pixels, while float values
  specify a percentage of the total number of pixels. Defaults to ``0``.
- ``crop`` specifies a rectangle to crop the screenshot to, given as
  ``(x1, y1, x2, y2)``. Coordinates must be given as integers.

If the project is in a git repository, the hash of the current commit is
automatically appended to the filename as ``@{hash}.png``. This allows
the developer to track changes to screenshots over time.

If the file already exists, the current screenshot is compared to the existing
file. If the files differ by more than ``max_pixel_difference`` pixels, a
RenpyTestScreenshotError is raised.

To overwrite an existing screenshot, either delete the file or run the test with
the ``--overwrite_screenshots`` command-line option.

::

    screenshot "screens/main_menu.png"
    screenshot "screens/inventory" max_pixel_difference 0.01
    screenshot "button.png" crop (10, 10, 100, 50)

This may be used in a parameterized test to take multiple screenshots::

    testcase screen_tester:
        parameter screen_name = ["inventory", "stats", "map"]

        run Show(screen_name)
        screenshot f"screens/{screen_name}.png"

Until
^^^^^^^^^

    Type: :dfn:`Control`

    .. describe:: <command> until <condition> [timeout (float)]

Repeats a statement until a condition is met. It consists of an
Command statement on the left-hand side and a condition on the right-hand
side, separated by the word ``until``.

If and when the condition on the right is met, control is
passed to the next statement. Otherwise, the left-hand statement
is executed repeatedly until the condition is ready.

If a ``timeout`` is given, the statement will wait up to that many seconds
for the condition to be met. If the condition is not met within that time,
a RenpyTestTimeoutError is raised.

This timeout temporarily overrides the global ``_test.timeout`` setting.

::

    advance until screen "choice"
    click "Next"
    advance until label "chapter_5"

    skip until screen "inventory" timeout 20.0


Python Blocks And Dollar-Lines
------------------------------

A :ref:`python block <python-statement>` or a :ref:`dollar-line` can be added
within a testcase. Unlike in normal Ren'Py code, the python blocks don't take
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