.. _testcases:

=====================
Integrated test suite
=====================

Ren'py allows creators to put tests in their games to make sure that an alteration to the code didn't break
the game.
Blah.

Testcase statement
==================

The ``testcase`` statement creates a named testcase, which is made of successive test statements.
Testcases are similar to Ren'py :ref:`labels <labels-control-flow>`, with a few specificities:

- The Testcase statement takes test statements, the Ren'py label statement takes Ren'py code. Both are mutually
  excusive.
- There is no testcase equivalent of the return statement: like in a python block, the removal of
  indentation and the end of the block closes the testcase.
- There can be no test statement outside of a testcase block, while there can be Ren'py code oustside labels (in
  init blocks for example).
::

    testcase default:
        "Start"
        exit

The testcase named ``default`` is the one which will be executed by default.

Note that when a testcase finishes executing, the game doesn't close itself (unless the ``exit`` statement is
used). Instead, it just remains where it is in the game, awaiting user action.

When that happens, or if the game quits before that happens (because of an ``exit``, following
an exception, or for another reason), the functions added to the :var:`config.end_testcase_callbacks` list are
called without arguments. This allows for clean-up code to be executed whatever may happen during the tests.

.. should an exception during a callback call prevent subsequent callbacks from being called ?

There is no equivalent callback for code being executed before the tests happens, as such code can simply be
put inside a python block at the beginning of the testcase.

The :func:`is_in_test` function is helpful to know whether a test is currently executing or not.

Test statements
===============
.. give an example for each one

python blocks and dollar-lines
------------------------------
A :ref:`python block <python-statement>` or a :ref:`dollar-line` can be added within a testcase.
Unlike in normal Ren'py code, the python blocks don't take the ``in substore`` or ``hide`` parameters.

.. difference with the default python blocks and dollar lines, apart from the hide/store params ?

if statement
------------
This statement, like a python ``if`` statement, takes a block.
Unlike the Ren'py or python versions however, it only takes a test clause, instead of a general python expression.
The provided clause being ready is the actual condition for the block to execute or not.
Example::

    if label "chapter_five":
        exit

A normal python/renpy ``if`` can be replicated using the ``eval`` clause::

    if eval (persistent.should_advance and
             i_should_advance["now"]):
        click

..
    there is no elif nor else clause

assert statement
----------------
Similarly to a python assert, this statement takes a clause and raises an AssertError if the clause is not ready
at the time when the assert statement executes.

A python assert can be replicated with::

    assert eval some_function(args)

About python assert statements, see the python documentation
`regarding asserts <https://docs.python.org/reference/simple_stmts.html#the-assert-statement>`_ and
`about boolean evaluation <https://docs.python.org/library/stdtypes.html#truth-value-testing>`_.

.. note::

    The regular ``assert`` python statement is not guaranteed to work in Ren'py. Notably, it is disabled in
    version 7, and in some versions before that.

    Therefore, the following may not actually check what it's supposed to check::

        $ assert some_function(args)

    In some versions of renpy or depending on unpredictable conditions, ``some_function`` may not even be called.
    The first assert example should be used instead.

jump statement
--------------

call statement
--------------

.. reminder that there is no return statement in testcases

.. to jump to a renpy label, use the run clause:: run Jump("label_name")

clause statement
----------------
A clause can be given, just by itself. ::

    pause 5

    click

until statement
---------------
This statement consists in two clauses, separated by the word ``until``.
If and when the right clause is ready, it is executed and control is passed to the next statement.
If not, the left clause is executed until the right clause is ready, then the right clause is executed.

This is basically an inline while loop. ::

    click until "It's an interactive book."

pass statement
--------------
Does not do anything. It's a no-op, allowing empty testcases. ::

    testcase not_yet_implemented:
        pass

exit statement
--------------
Quits the game without calling the confirmation screen.
Does not save the game when quitting::

    if eval need_to_confirm:
        run Quit(confirm=True) # asks for confirmation, and autosaves
    if eval persistent.quit_test_with_action:
        run Quit(confirm=False) # does not ask, but still autosaves
    exit # neither asks nor autosaves

Test clauses
============
Clauses have the property of being ready or not ready.
They can be part of ``if``, ``assert`` or ``until`` test statements, or they can be
simply on their own (see above). It is safe to evaluate the readiness of a clause which could raise
an exception if executed::

    if label preferences:
        "Dark theme"

.. for each one, say what makes it ready

click clause
---------------
Executes a simulated click on the screen.
It takes the following optional properties:

- ``button`` specifies which button of the simulated mouse is to be clicked with.
  1 is a left-click, 2 is a right-click, 3 is a scrollwheel-click, 4 and 5 are additional buttons on some mouses.
  Normally only 1 and 2 trigger any response from renpy.
  Takes an integer and defaults to 1.
- ``pos`` specifies where to click, as a pair of x/y coordinates.
  Coordinates are taken relative to the screen. Floats between 0.0 and 1.0 are supported as a fraction
  of the screen size in either dimension. ``absolute`` and other means of expressing positions
  are not currently supported.

.. ``always`` is not documented because useless in the case of the click clause by itself

Click behaves like a pattern-taking clause which would not be given a pattern : if no ``pos`` is provided, it will
look for a neutral place where a click would not occur on a focusable element.

.. give example for both

This clause is always ready.

The :func:`has_default_focus` function is a helpful accessor to know whether a game can be advanced
by a bare ``click`` or not. ::

    click until eval (not has_default_focus())

string expression clause
------------------------
This clause consists in a simple string, which is interpreted as a pattern (see the Patterns section below).
It executes by simulating a click on the target identified by the pattern.

It takes three optional properties:

- ``button`` - same as the click clause
- ``pos`` - same as the click clause, but the position is relative to the focusable area of the target.
  If the position is invalid, for example if a button is 100x100 pixels and the given ``pos`` is (105, 150),
  the ``pos`` is ignored and a random position within the target is used instead.
- ``always`` does not take a value. It overrides the readiness of the clause, making it always ready.

This clause is ready if and when a suitable target is found on the screen, or if it is given
the ``always`` property.

run clause
-------------
Runs the provided :ref:`screen-language action <screen-actions>` or list of actions.

Ready if and when a button containing the provided action (or list) would be sensitive.

pause clause
---------------
Pauses for a given number of seconds.

This clause is always ready.

.. link to renpy pause statement and ATL pause statement

label clause
---------------
Does not do anything when executed. This clause only exists to be used inside clause-taking test statements
like ``assert``, ``if`` or ``until``.

The label clause is ready if and when the provided label has been passed between the current test statement
and the one before.

Attention, this means that the following example does not work::

    "play chapter 1"
    # passing the "chapter_1" label
    pause 1
    assert label chapter_1

It will not work because no renpy label will have been reached between the statement containing the label clause
and the preceding statement. In this case, these are the assert statement and the pause statement, respectively.
The same happens in the following example::

    "play chapter 1"
    # passing the "chapter_1" label
    assert label chapter_1
    assert label chapter_1

The chapter_1 label is not reached between the first label clause and the second label clause, therefore the
second label clause fails (technically, the clause is not ready and the assert fails).

In both examples, the assert label statement would have worked if it were placed on its own, directly after the
``"play chapter 1"`` string-expression statement (or after the comment, which doesn't count)::

    "play chapter 1"
    # passing the "chapter_1" label
    assert label chapter_1
    # all fine

.. warning disambiguation, link to both renpy label and SL label

drag clause
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

.. warning disambiguation ? probably not necessary

scroll clause
----------------
..
    takes a string giving it a pattern
    ready when the target (pattern) is found
    If the target is a bar, scrolls it down a page. If already at the bottom, returns it to the top.

eval clause
-----------
Does not do anything when executed, except evaluating the expression it is given. This clause only exists to be
used inside clause-taking test statements like ``assert``, ``if`` or ``until``, effectively turning ``assert`` and
``if`` into their non-clause-taking python equivalents.

.. The provided expression can span on several lines, if wrapped in parentheses.

Ready if and when the provided value is true, in a boolean context.

.. note::

    Differences between a dollar-line and the eval clause :

    - A dollar-line executes any python statement, which does not necessarily have a value - for example
      ``$ import math`` - while the eval clause require an expression, a.k.a
      something having a value.
    - The eval clause provides a value to an ``if`` or ``until`` statement, while these statements can't take a
      dollar sign, much less a dollar-line.

..
    When the returned value of a function call is to be ignored, both are technically equivalent::

        $ print("Test 1")
        eval print("Test 2")

    This is because functions always return a value (None being a value), unless they raise an exception.

..
    warning disambiguation this is also a python builtin
    say it's not a good idea to use it

type clause
--------------
.. simulate a key-pressing or the typing of text

..
    It is ready if a pattern is not provided,
    or if one is provided and a suitable target is found on the screen.
    For the clauses taking the ``always`` property, that property overrides the readiness of the clause.

..
    warning disambiguation this is also a python builtin
    link to python doc

move clause
--------------
..
    `move (position) [pattern (string)]`
    moves the virtual test mouse to the provided position, within the area targeted by the pattern
    or, if none is given, within the whole screen

..
    It is ready if a pattern is not provided,
    or if one is provided and a suitable target is found on the screen.
    For the clauses taking the ``always`` property, that property overrides the readiness of the clause.

Patterns
===============

Some clauses take a pattern, which helps positioning the mouse or locating where a clause will do something.
The ``pattern`` property (which in the case of the string expression clause, is the string itself) takes a string
which resolves to a target found on the screen, based on the shorted match in the alt text of
focusable screen elements (typically, buttons). The search is case-insensitive.

If no pattern is given, the virtual test mouse is positioned to the last previous location where
a click happened, or to the specified position, if any. If that position lies on a focusable element,
a random position in the screen which does not overlap a focusable element is chosen instead.

If a pattern is given, the mouse is positioned to the last previous location where a click happened,
or to the specified position, if any. If that position does not lie inside the targeted element,
a random position within it is chosen instead. To that end, things like focus_mask are taken into account.

If a pattern is given and if it does not resolve to a target at the time when the clause using it executes,
an exception is raised (terminating the test). To test whether a given pattern resolves to a target at a given
time, the readiness condition of a string expression clause can be evaluated inside an if statement.
