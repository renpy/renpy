=================
Automated Testing
=================

Ren'Py allows creators to put automated tests in their games to make sure that
alterations to the game don't break existing functionality. This is especially
useful for large games, or for games that are frequently updated.

The two main components of the testing system are the ``testcase`` and
``testsuite`` statements.

The :func:`renpy.is_in_test` function is helpful to know whether a test is currently
executing or not.


Quick Start
===========

This section shows a minimal example using statements that are common in
real testcases:

- ``run Jump("...")`` to start from a known label.
- ``advance until screen "choice"`` to get to a menu.
- ``click "Choice Text"`` to pick a menu option.
- ``click id "..." until not screen "..."`` to keep clicking until a screen disappears.

Add the following Ren'Py code to your game script:

.. code-block:: renpy

    screen quickstart_popup():
        modal True

        frame:
            xalign 0.5
            yalign 0.5

            vbox:
                spacing 12
                text "Quick Start Popup"

                textbutton "Close":
                    id "quickstart_close"
                    action Hide("quickstart_popup")


    label quickstart_demo:
        "Welcome to the testcase quick start demo."

        show screen quickstart_popup
        "Close the popup to continue."

        menu:
            "Take the map":
                "You picked the map."
            "Leave it":
                "You left the map behind."

        "End of demo."
        return

    # ==== Test cases ====
    # These can go in the same file, or in a separate file (e.g. testcases.rpy).

    testsuite quick_start:
        before testcase:
            # Make sure each test has the same starting point
            run Jump("quickstart_demo")
            advance until screen "quickstart_popup"

        testcase choose_map:
            pause 0.5
            click id "quickstart_close" until not screen "quickstart_popup"
            pause 0.5
            advance until screen "choice"
            click "Take the map"
            advance until "You picked the map."
            pause 0.5

        testcase leave_map:
            pause 0.5
            click id "quickstart_close" until not screen "quickstart_popup"
            pause 0.5
            advance until screen "choice"
            click "Leave it"
            advance until "You left the map behind."
            pause 0.5

After saving the file, run the test using the launcher or the command line.
See :ref:`running-testcases` for additional details.

Launcher
--------
You can run the test from the launcher by selecting "Run Testcases" from the Ren'Py launcher.
If the button does not appear, try launching the game first (or recompiling), then
click the "Refresh" button in the launcher.

Command Line
------------

If you're running the test from the command line, the command should look something like this:

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            ./renpy.sh /path/to/game test quick_start

    .. tab:: Windows

        .. code-block:: bat

            .\lib\py3-windows-x86_64\python.exe renpy.py C:\path\to\game test quick_start

.. note ::

    The pauses in this demo are not necessary, they are just there to make the test
    execute more slowly so you can see what's happening.
    In a real test, you can remove them to make the test run faster.

.. _running-testcases:

Running Testcases
=================

Launcher
--------

To run tests from the launcher, select the project and press the "Run Testcases" button.
If the button is not visible, do the following:

1. Ensure that you have at least one testcase defined in your game.
2. Launch the game normally by clicking the "Launch Project" button.
3. Click the "Refresh" button in the launcher.

This will run the "global" test suite by default.

.. _test-command-line:

Command Line
------------

To run tests from the :doc:`command line <cli>`, open a terminal in the Ren'Py SDK directory and
use the test command:

.. tabs::

    .. tab:: Linux / macOS

        .. code-block:: bash

            cd /path/to/renpy
            ./renpy.sh <basedir> test [<filters>] [options...]

    .. tab:: Windows

        .. code-block:: bat

            cd C:\path\to\renpy
            .\lib\py3-windows-x86_64\python.exe renpy.py <basedir> test [<filters>] [options...]

.. option:: <basedir>

    Specifies the path to the project.

.. option:: <filters>

    Specifies the test cases or suites to run. If not given, the "global"
    test suite will be run. Filters are case-sensitive.

    Multiple filters can be provided, separated by a space.
    These are combined, so that a test will be run if it
    matches any of the filters.

    See :ref:`test-filter-examples` for examples.

.. option:: --enable-all

    Executes all test cases and test suites, regardless of their ``enabled`` property.
    Does not work if a specific test case or suite is specified.

.. option:: --overwrite-screenshots

    Overwrite existing screenshots when a
    :ref:`screenshot statement <test-screenshot-statement>` is executed.

.. option:: --hide-header

    Disables the header at the start of the test run.

.. option:: --hide-execution {no|hooks|testcases|all}

    Hides information about test execution. ``--hide-execution hooks`` hides hooks,
    ``--hide-execution testcases`` hides test cases and hooks, and ``--hide-execution all``
    hides everything.

.. option:: --hide-summary

    Disables the summary at the end of the test run.

.. option:: --report-detailed

    Shows detailed information about each test during the run.

.. option:: --report-skipped

    Shows information about skipped tests. This option should be used together
    with ``--report-detailed``.

.. _test-filter-examples:

Filter Examples
^^^^^^^^^^^^^^^

Consider a game with the following test structure::

    testsuite math:
        testcase addition: ...
            parameter (a, b) = [(2, 1), (3, 1), (3, 2)]
        testcase subtraction: ...
            parameter (a, b) = [(2, 1), (3, 1), (3, 2)]
        testcase shapes: ...

        testsuite graphs:
            testcase dot: ...
            testcase save: ...

    testsuite audio:
        testcase save: ...
        testcase load: ...

    testsuite sprites:
        testcase save: ...
        testcase load: ...

    testcase reload: ...

All tests live inside the implicit root suite called ``global``.

**Running all tests**

Omitting filters, or using ``global``, runs everything:

======================  ==============
Command                 Selected Tests
======================  ==============
``test``                All tests
``test global``         All tests
======================  ==============

**Selecting a suite or test case**

Use ``.`` to separate suite names:

========================  ==============
Command                   Selected Tests
========================  ==============
``test reload``           ``reload``
``test audio``            ``audio.save``, ``audio.load``
``test audio.save``       ``audio.save``
``test math``             ``math.addition``, ``math.subtraction``, ``math.shapes``,
                          ``math.graphs.dot``, ``math.graphs.save``
``test math.graphs``      ``math.graphs.dot``, ``math.graphs.save``
``test math.graphs.dot``  ``math.graphs.dot``
========================  ==============

You may optionally add ``global.`` to the start of the filter, but it is not required.
For example, ``test math`` and ``test global.math`` will both select the same tests.

**Wildcards**

``*`` matches any sequence of characters within a single name segment.
One ``*`` cannot cross a ``.`` boundary.

================  ==============
Command           Selected Tests
================  ==============
``test re*``      ``reload``
``test math.s*``  ``math.subtraction``, ``math.shapes``
``test *.save``   ``audio.save``, ``sprites.save``
================  ==============


**Parameters**

When a test case uses the ``parameter`` keyword, each value combination is a separate run.

See :ref:`parameterized-tests` for more information.

==================================  ==============
Command                             Selected Tests
==================================  ==============
``test "math.addition(a=2, b=1)"``  ``math.addition(a=2, b=1)``
``test "math.addition(a=3)"``       ``addition(a=3, b=1)``, ``addition(a=3, b=2)``
``test "math.*(a=3, b=2)"``         ``addition(a=3, b=2)``, ``subtraction(a=3, b=2)``
==================================  ==============

.. note::

    Quote filters that contain parentheses to prevent the shell from interpreting them.

**Multiple filters**

Separate filters with spaces. A test is selected if it matches *any* filter:

=============================   ==============
Command                         Selected Tests
=============================   ==============
``test audio sprites``          ``audio.save``, ``audio.load``, ``sprites.save``,
                                ``sprites.load``
``test *.save math``            ``sprites.save``, ``sounds.save``, plus all of ``math``
=============================   ==============

**Quick Reference**

======  =========================  =======
Symbol  Meaning                    Example
======  =========================  =======
``.``   Test suite separator       ``math.graphs``
``*``   Wildcard (one level only)  ``*.save``, ``math.s*``
``()``  Parameter values           ``addition(a=2, b=1)``
======  =========================  =======

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
  Ren'Py code outside labels.

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

    A block of test statements that is executed at the beginning of the testsuite,
    before running any tests contained within the current suite.

.. describe:: before testsuite

    A block of test statements that is executed before each test suite
    within the current suite.

.. describe:: before testcase

    A block of test statements that is executed before each test case
    within the current suite.

.. describe:: after testcase

    A block of test statements that is executed repeatedly, running after each test case
    in the current suite. This is run even if the testcase fails or raises an
    exception.

.. describe:: after testsuite

    A block of test statements that is executed repeatedly, running after each test suite
    in the current suite. This is run even if the testsuite fails or raises an
    exception.

.. describe:: teardown

    A block of test statements that is executed after running all tests
    contained within the current suite. This is run even if a test
    fails or raises an exception.

The ``before *`` and ``after *`` hooks take the following properties:

.. var:: depth

    Controls how many levels of nested tests the hook applies to.

    - ``-1``: Run hook for all nested tests, at any depth
    - ``0``: Run hook for only direct children of this suite (no nesting)
    - Positive number: Run hook for tests up to that many levels deep

    **Defaults:**

    - ``-1`` for ``before testcase`` and ``after testcase`` (runs for all nested testcases)
    - ``0`` for ``before testsuite`` and ``after testsuite`` (runs for direct child testsuites only)

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

        label test_demo:
            ""This is a demo for testcases.""
            ""It has a few messages and a menu.""
            menu:
                ""First Choice"":
                    ""Selected first choice.""
                ""Second Choice"":
                    ""Selected second choice.""
                ""Third Choice"":
                    ""Selected third choice.""
            return

        testsuite global:
            setup:
                $ print(""global :: setup"")
                skip until screen ""main_menu""

            before testsuite:
                $ print(""global :: before testsuite"")
                if not screen ""main_menu"":
                    run MainMenu(confirm=False)
                click ""Start""

            before testcase:
                $ print(""global :: before testcase"")

            after testcase:
                $ print(""global :: after testcase"")

            after testsuite:
                $ print(""global :: after testsuite"")

            teardown:
                $ print(""global :: teardown"")
                exit

            testsuite basic:
                testcase first_testcase:
                    $ print(""basic.first_testcase"")
                    advance

            testsuite test_choices:
                setup:
                    $ print(""test_choices :: setup"")

                before testcase:
                    $ print(""test_choices :: before testcase"")
                    run Jump(""test_demo"")
                    advance until screen ""choice""

                after testcase:
                    $ print(""test_choices :: after testcase"")

                teardown:
                    $ print(""test_choices :: teardown"")

                testcase choice1:
                    $ print(""test_choices.choice1"")
                    click ""First Choice""

                testcase choice2:
                    enabled False
                    $ print(""test_choices.choice2 (disabled)"")
                    click ""Second Choice""

                testcase choice3:
                    $ print(""test_choices.choice3"")
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

                        **basic**.first_testcase

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

                        **test_choices**.choice1

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

                        **test_choices**.choice3

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
    statement in the ``after`` hook of the testsuite::

        testsuite global:
            teardown:
                exit

.. _skipping-testcases:

Skipping Testcases
==================

If a testcase is skipped, it will not be executed. In addition, the
``before testcase`` and ``after testcase`` hooks of the testsuite will not be executed
for that testcase.

If *all* tests are skipped in a testsuite, then the ``setup`` and
``teardown`` hooks will not be executed either. In addition, the
``before testsuite`` and ``after testsuite`` hooks will not be executed from
the parent testsuite(s).

.. _parameterized-tests:

Parameterized Tests
===================

A test case can run multiple times with different values by using the ``parameter`` property.

To do this, give a variable name and a list of values. The test will run once
for each value in the list. For example::

    testcase click_buttons:
        parameter button_name = ["Load", "Save"]
        click expression button_name

This runs twice: first clicking "Load", then clicking "Save".

Parameters should be thought of as defining multiple testsuites or testcases, with
the hooks (including ``setup`` and ``teardown``) being run for each value.

Grouped Parameters
------------------

It is possible to specify several variables at once by grouping them
in parentheses and giving a list of value groups. For example::

    testcase addition:
        parameter (x, y, z) = [ (1, 2, 3), (2, 3, 5), (3, 5, 8) ]
        assert eval (x + y == z)

This will run three times, using the following values:
``(x=1, y=2, z=3)``, ``(x=2, y=3, z=5)``, and ``(x=3, y=5, z=8)``.

Parameter Combinations
----------------------

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


Using Parameters in Expressions
-------------------------------

You can use parameters in any test property that takes an expression.

For example, here's a test that runs three times, once for each value of ``x``.
The test will pass when ``x`` is 0 or 1, and will be expected to fail (``xfail``) when ``x`` is 2::

    testcase choice_test:
        parameter x = [0, 1, 2]
        xfail x == 2

        assert eval (x < 2)

You can also use parameters to select screens or buttons by name.
For example, this test will click either the "first" or "second" choice,
depending on the value of ``choice_text``::

    testcase show_menu:
        parameter screen_name = ["preferences", "load"]

        run ShowMenu(screen_name)
        pause until screen screen_name
        run Return()

Parameters can be used, preceded by ``expression``, to select a button by
parameter name.

    testcase click_buttons:
        parameter button_name = ["Load", "Save"]

        click expression button_name

Parameters can also be used inside Python code blocks.
For example, this test prints the current values of ``x`` and ``y``,
and then clicks at that position::

    testcase param_test:
        parameter (x, y) = [(0.0, 0.0), (0.5, 0.5), (1.0, 1.0)]

        $ print(f"Clicking at position ({x}, {y})")
        click pos (x, y)

Parameterized Test Suites
-------------------------

Parameters can also be provided to the whole test suite. In this case, all hooks and test cases
inside the suite will run once for each parameter set.

Each parameterized run will execute the ``setup``, ``before/after testsuite``,
and ``teardown`` hooks.

For example::

    testsuite math_tests:
        parameter (x, y, z) = [ (1, 2, 3), (2, 3, 5), (3, 5, 8) ]

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
            parameter (x, y) = [(0.0, 0.0), (0.5, 0.5)]

            advance until screen "choice"
            click choice_text
            click pos (x, y)

This will run four times, once for each combination of ``(choice_text, (x, y))``:

    ``("first", (0.0, 0.0))``, ``("first", (0.5, 0.5))``,
    ``("second", (0.0, 0.0))``, ``("second", (0.5, 0.5))``

.. warning::

    Parameters are passed by reference. If you change a mutable parameter (e.g. a list or dict),
    that value will be affected in all other tests that share the same object.

Exceptions And Failures
=======================
If an error occurs during a test case:

1. The test case will stop executing immediately
2. The ``after testcase`` hook of the testsuite containing the test case will run
3. If there are more test cases, they will continue to be executed (including the
   ``before testcase`` hook)
4. If no more test cases exist, the ``after testsuite`` hook of the testsuite will run

If an error occurs during a hook (eg. ``before testcase``):

1. The test suite will stop executing immediately
2. If the suite was called by another suite, the parent suite will continue
   executing.
3. If no parent suite exists, the game will end the test run.


Test Reporting
===================

After a test run, a report is printed to the console, listing all test cases
and their results. If the :option:`--report-detailed` option is provided, the report
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

.. var:: _test.timeout

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

.. var:: _test.vc_revision

    The version control (often git) revision of the current source tree, if available.
    Defaults to the :envvar:`RENPY_TEST_VC_REVISION` :doc:`environment variable <environment_variables>`,
    or an empty string if not set.


.. _test-statements:

Test Statements
===============

Test statements are the building blocks of test cases. They can be broadly
divided into three categories: command statements, condition/selector statements, and
control statements.

Command statements may be followed by the :ref:`test-repeat-statement` and
:ref:`test-until-statement` statements.

The syntax descriptions on this page use the following notation:

- ``[]`` encloses an optional group.
- ``<name>`` is a required value supplied by the test author.
- ``<name: type>`` is a value with a documented type.
- Literal words outside ``<>`` must be written verbatim.
- Parentheses and commas shown in syntax are literal punctuation.

For example, ``click [pos (<x: int>, <y: int>)]``:

- ``click`` is a literal string that must be typed as-is.
- Everything between ``[]`` is optional.
- ``pos (`` is a literal string that must be typed as-is.
- ``<x: int>`` describes that the x-coordinate takes an integer.
- ``<y: int>`` describes that the y-coordinate takes an integer.
- ``)`` is a literal string that must be typed as-is.

Valid statements include:

- ``click``
- ``click pos (0, 0)``
- ``click pos (10, 50)``


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

    .. describe:: pause [<seconds: float>]

Pauses test execution for a given number of seconds.
The duration may be omitted if used with an
:ref:`test-until-statement` clause.  ::

    pause 5.0
    pause until screen "inventory"

Run
^^^^^^^^^^

    Type: :dfn:`Command`

    .. describe:: run <action>

Runs the provided :doc:`screen-language action <screen_actions>` (or list of
actions).

The statement waits until the supplied action is available, then invokes it.
This is equivalent to waiting for a button with this action to become sensitive,
then clicking it.

::

    run Start("chapter_1")
    run Jump("chapter_3")
    run Preference("main volume", 0.5)

.. _test-skip-statement:

Skip
^^^^^^^^^^

    Type: :dfn:`Command`

    .. describe:: skip [fast]

Causes the game to begin skipping. If the game is in a menu,
then this exits the menu and returns to the game. Otherwise, it enables in-game skipping.

If ``fast`` is provided, the game will skip directly to the next menu choice.

::

    skip
    skip fast
    skip until screen "choice"


Mouse Commands
----------------

Properties that are common to all mouse commands:

.. describe:: <target>

Equivalent to ``[<selector>] [pos (<x: int or float>, <y: int or float>)]``

- ``<selector>``: A :ref:`Selector Statement <test-selectors>` like ``id "my_button"`` or ``"Text"``.
- ``pos``: An (x, y) pair. If a coordinate is an integer, an absolute number of pixels is used.
  If a coordinate is a float, it is treated as a normalized coordinate from ``0.0``
  (the left/top edge) to ``1.0`` (the right/bottom edge), relative to the width or
  height of the target. When no selector is given, the float is relative to the
  screen width or height.

.. note::

    A float value of ``1.0`` maps to ``width - 1`` (or ``height - 1``),
    so ``1.0`` maps to the last pixel **within** the target
    rather than one past the edge.

========  =======  =======
Selector  ``pos``  Result
========  =======  =======
No        No       Current mouse position\*
Yes       No       A random focusable point within the selector
No        Yes      The point relative to the screen
Yes       Yes      The point relative to the selector
========  =======  =======

\* *If the mouse was never moved before, a random screen position is used.*

.. describe:: button <int>

Determines which button the simulated mouse uses. Defaults to ``1``.

    - ``1``: Left click
    - ``2``: Right click
    - ``3``: Middle click
    - ``4`` and ``5``: Additional buttons found on some devices


Click
^^^^^^^^^^

    Type: :dfn:`Command`

    .. describe:: click [<target>] [button <int>]

Executes a simulated click on the screen.

.. ``always`` is not documented because useless in the case of the click clause by itself

::

    # Click at the current mouse position
    click

    # Click a button with specific text
    click "Start"

    # Click a button using an expression.
    $ button_name = "Load"
    click expression button_name

    # Right-click on a specific target.
    click id "inventory_button" button 2

    # Click the center of the selected target.
    click id "inventory_button" pos (0.5, 0.5)


.. note::

    Do not use ``click`` to advance dialogue. The result depends on the current mouse
    position and may activate unrelated screen elements. Use
    :ref:`advance <test-advance-statement>` or :ref:`skip <test-skip-statement>` instead.

Drag
^^^^^^^^^^

    Type: :dfn:`Command`

    .. describe:: drag <target> to <target> [button <int>] [steps <int>]

Simulates a drag action on the screen. It takes the following properties:

- The first ``<target>`` specifies the starting point of the drag.
- The second ``<target>``  specifies the ending point of the drag.
- ``steps`` specifies how many intermediate steps the drag should take.
  Defaults to ``10``. More steps result in a smoother drag, but also take more time.

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

    .. describe:: move <target>

Moves the virtual test mouse to a given position on the screen.

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

    .. describe:: scroll [amount <int>] [<target>]

Simulates a scroll event. It takes the following optional properties:

- ``amount`` specifies how many "notches" to scroll. Defaults to ``1``.
  Positive values scroll down, negative values scroll up.

::

    scroll "bar"
    scroll id "inventory_scroll"
    scroll amount 10 id "inventory_scroll" pos (0.5, 0.5)
    scroll # scrolls down at the current mouse position

.. note::

    This simulates a mousewheel event and may not directly change an adjustment.

    Consider using the Scroll action from :doc:`screen_actions`. ::

        run Scroll("inventory_scroll", "increase", amount="step", delay=1.0)

Keyboard Commands
-----------------

Keysym
^^^^^^^^^^

.. _test-keysym-statement:

    Type: :dfn:`Command`

    .. describe:: keysym <str> [<target>]

Simulates a keysym event. This includes the keys of :doc:`config.keymap <keymap>`.

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

    .. describe:: type <str> [<target>]

Types the provided string as if it were typed on the keyboard.

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

        assert screen "main_menu" and eval renpy.is_in_test()
        advance until "ask her right" or label "chapter_five"
        click "Next" until not screen "choice"

.. _test-eval-statement:

Eval
^^^^^^^^^

    Type: :dfn:`Condition`

    .. describe:: eval <python_expression>

Evaluates the provided Python expression. This exists only to be used inside condition-taking test
statements like ``assert``, ``if`` or ``until``. ::

    assert eval some_function(args)
    assert eval (x + y == z) # Parentheses may be used optionally
    if eval persistent.should_advance:

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

    .. describe:: label <name: str>

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
    assert label chapter_1 # fails since the label was reached and passed by the advance statements

.. warning::

    This test statement should not be confused with the Ren'Py native
    :ref:`label <label-statement>` statement it refers to, or with the unrelated
    :ref:`label element <sl-label>` used in screens.

.. _test-selectors:

Selector Statements
-------------------

Selector statements are used to check if a certain element is on the screen,
and to use that element for further actions.

Selectors are a special kind of condition.

In command signatures, ``<selector>`` represents any selector form documented
in this section, including ``screen <name: str>``, ``id <name: str>``,
a quoted text selector, or ``expression <expression>``.

Displayable Selector
^^^^^^^^^^^^^^^^^^^^

    Type: :dfn:`Condition, Selector`

Selects a displayed screen or displayable by screen name or id, optionally restricted to a layer.

It takes one or more of the following properties:

    .. describe:: screen <name: str>

        The name of the screen to check.

    .. describe:: id <name: str>

        The id of the element to check.

    .. describe:: layer <name: str>

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

    .. describe:: "<text>" [raw]
    .. describe:: expression <expression> [raw]

The ``text`` selector takes a string which resolves to a target
found on the screen. The search is performed by going through all focusable
elements on the screen (which are typically buttons and the main textbox),
and looking through their text and :propref:`alt` text.

This search is case-insensitive and looks for the shortest match.
For example, if the string ``"log"`` is given, and the screen contains
the texts ``"LOGS"`` and ``"illogical"``, the target
will be the ``"LOGS"`` text.

If ``raw`` is given, the search is performed on the text as given in the
script, before translation and :ref:`interpolation <text-interpolation>`.
If not given, the search is performed on the text as it appears on screen,
after translation and interpolation.

If ``expression`` is given, the string to search for is determined by evaluating the provided expression.

::

    # This may be in a button
    skip until "Start Game"

    # This may be in the main textbox
    advance until "Hey, that's not fair!"

    # Case-insensitive search
    assert "AsK HeR RighT AwaY"

    # Search unsubstituted text
    assert "Welcome, Eileen!"
    assert "Welcome, [player_name]!" raw

    # Search untranslated text after changing the language
    run Language("japanese")
    assert "スタート"
    assert "Start" raw

.. note ::

    Prefer `id` selectors for stable UI tests.
    Use text selectors when the visible wording itself is part of the behavior being tested.

Control Statements
------------------

These statements control the flow of the test execution.

Assert
^^^^^^^^^^

    Type: :dfn:`Control`

    .. describe:: assert <condition> [timeout <seconds: float>] [xfail <bool>]

Verifies that the condition is true when the assert statement is executed.

If a ``timeout`` is given, the statement will wait up to that many seconds
for the condition to be met. If ``timeout`` is not given, the assertion is tested
immediately.

If the condition is not met, a RenpyTestTimeoutError is raised.

If ``xfail`` is set to ``True``, the assert statement is expected to fail.
This inverts the meaning of the statement: if the condition is met, the
assertion fails. If the condition is not met, the assertion passes.

::

    # Selector condition only.
    assert screen "main_menu"

    # Python condition only.
    assert eval persistent.seen_intro

    # Combined Python and selector conditions.
    assert eval persistent.seen_intro and screen "main_menu"

    # With timeout
    assert id "start_button" timeout 5.0

.. seealso::

    - `Python asserts <https://docs.python.org/reference/simple_stmts.html#the-assert-statement>`__
    - `Boolean evaluation <https://docs.python.org/library/stdtypes.html#truth-value-testing>`__

For
^^^

    Type: :dfn:`Control`

    .. describe:: for <variable> in <iterable>

Executes a block of test statements for each item in the provided
iterable. ``<iterable>`` is evaluated as a Python expression.
You can use `break` and `continue` statements to control the flow of the loop.

Example::

    # Click "Next" three times
    for _ in range(3):
        click "Next"

    # Click each of the choices, skipping "Trade" if the shop is not unlocked
    for choice in ["Talk", "Trade", "Leave"]:
        if eval (choice == "Trade" and not persistent.shop_unlocked):
            continue
        click expression choice
        if screen "shop":
            break

    # Click each of the tabs in the stats screen, skipping "Quests" if quests are not enabled
    for stat_tab in ["Stats", "Skills", "Quests"]:
        click expression stat_tab
        if eval (stat_tab == "Quests" and not persistent.quests_enabled):
            continue
        assert expression stat_tab timeout 2.0

If
^^^^^^^^^

    Type: :dfn:`Control`

    .. describe:: if <condition>

Executes a block of test statements if the provided condition is met.

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

.. _test-repeat-statement:

Repeat
^^^^^^^^^

    Type: :dfn:`Control`

    .. describe:: <command> repeat <count: int> [timeout <seconds: float>]

Repeats a statement for a given number of times. It consists of a
Command statement on the left-hand side and a number of repetitions
on the right-hand side, separated by the word ``repeat``. ::

    click "+" repeat 3
    keysym "K_BACKSPACE" repeat 10
    advance repeat 3

.. _test-screenshot-statement:

Screenshot
^^^^^^^^^^

    Type: :dfn:`Control`

    .. describe:: screenshot <path: str> [max_pixel_difference <int or float>] [crop (<x: int>, <y: int>, <width: int>, <height: int>)]

Takes a screenshot of the current screen and saves it to the provided path.

If the file already exists, the current screenshot is compared to the existing
file. If the files differ by more than ``max_pixel_difference`` pixels, a
RenpyTestScreenshotError is raised.

- ``path`` specifies the path (relative to ``_test.screenshot_directory``)
  where the screenshot will be saved. It may include a file extension.
  Only ``.png`` is supported.
- ``max_pixel_difference`` specifies how many pixels may differ between
  the taken screenshot and an existing screenshot for the test to pass.
  Integer values specify the number of pixels, while float values
  specify a percentage of the total number of pixels. Defaults to ``0``.
- ``crop`` specifies a rectangle to crop the screenshot to, given as
  ``(x, y, width, height)``. Coordinates must be given as integers.

If ``_test.vc_revision`` is set, the value is automatically appended to the filename
as ``@{_test.vc_revision}.png``. This allows the developer to track changes to
screenshots over time. For example, :file:`screens/main_menu.png` becomes
:file:`screens/main_menu@a1b2c3d.png`.

To overwrite an existing screenshot, either delete the file or run the test with
the :option:`--overwrite-screenshots` command-line option.

::

    screenshot "screens/main_menu.png"
    screenshot "screens/inventory" max_pixel_difference 0.01
    screenshot "button.png" crop (10, 10, 100, 50)

This may be used in a parameterized test to take multiple screenshots::

    testcase screen_tester:
        parameter screen_name = ["inventory", "stats", "map"]

        run Show(screen_name)
        screenshot f"screens/{screen_name}.png"

.. _test-until-statement:

Until
^^^^^^^^^

    Type: :dfn:`Control`

    .. describe:: <command> until <condition> [timeout <seconds: float>]

Repeats the command until the condition becomes true.
If the condition does not become true before the timeout, the test fails.

This timeout temporarily overrides the global ``_test.timeout`` setting.
A RenpyTestTimeoutError is raised if the statement times out.

::

    advance until screen "choice"
    click "Next"
    advance until label "chapter_5"

    skip until screen "inventory" timeout 20.0

While
^^^^^

    Type: :dfn:`Control`

    .. describe:: while <condition>

Executes a block of test statements while the provided
condition remains met. You can use `break` and `continue` statements
to control the flow of the loop.

Example::

    $ should_advance = True
    while eval should_advance:
        advance
        if screen "main_menu":
            break

        $ should_advance = some_evaluation_function()


Python Blocks And Dollar-Lines
------------------------------

A :ref:`python block <python-statement>` or a :ref:`dollar-line` can be added
within a testcase. Unlike in normal Ren'Py code, the python blocks don't take
the ``in substore`` parameter, but they do take the ``hide`` keyword. Both
allow execution of arbitrary python code.

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

See Also
========

You can find real tests in the Ren'Py source code:

* `<https://github.com/renpy/renpy/blob/master/tutorial/game/testcases.rpy>`_
* `<https://github.com/renpy/renpy/blob/master/gui/game/testcases.rpy>`_
* `<https://github.com/renpy/renpy/blob/master/launcher/game/testcases.rpy>`_