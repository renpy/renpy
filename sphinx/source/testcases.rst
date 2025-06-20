=====================
Integrated test suite
=====================

Ren'py allows creators to put tests in their games to make sure that an
alteration to the code didn't break the game.

Testcase statement
==================

The ``testcase`` statement creates a named testcase, it takes a name, a colon,
and a block which contains successive test statements (see below). Testcases are
similar to Ren'py :ref:`labels <label-statement>`, with a few specificities:

- The Testcase statement takes test statements, the Ren'py label statement takes
  Ren'py code. Both are mutually excusive.
- There is no testcase equivalent of the return statement: like in a python
  block, the removal of indentation and the end of the block closes the testcase.
- There can be no test statement outside of a testcase block, while there can be
  Ren'py code oustside labels (in init blocks for example).

::

    testcase default:
        "Start"
        exit

The testcase named ``default`` will be executed first - the other ones may be
called by the default testcase.

Note that when a testcase finishes executing, the game doesn't close itself
(unless the ``exit`` statement is used). Instead, it will just remain where it
ended up in the game, awaiting user action.

.. should an exception during a callback call prevent subsequent callbacks from being called ?

There is no equivalent callback for code being executed before the tests
happen, as such code can simply be put inside a python block at the beginning
of the testcase, or in ``init python`` blocks.

The :func:`renpy.is_in_test` function is helpful to know whether a test is currently
executing or not.

Test statements
===============

The following statements can be written in ``testcase`` blocks.

python blocks and dollar-lines
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

if statement
------------

This statement, like a python ``if`` statement, takes a block.

Unlike the Ren'py or python versions however, it only takes a
:ref:`test clause <test-clauses>`, instead of a general python expression.
The provided clause being ready is the actual condition for the block to execute
or not.

Example::

    if label "chapter_five":
        exit

A normal python/renpy ``if`` can be replicated using the :ref:`test-eval-clause`\ ::

    if eval (persistent.should_advance and
             i_should_advance["now"]):
        click

.. there is no elif nor else clause

assert statement
----------------

Similarly to a python assert, this statement takes a :ref:`clause <test-clauses>`
and raises an AssertError if the clause is not ready at the time when the assert
statement executes.

A python assert can be replicated with::

    assert eval some_function(args)

About python assert statements, see the python documentation
`regarding asserts <https://docs.python.org/reference/simple_stmts.html#the-assert-statement>`__
and
`about boolean evaluation <https://docs.python.org/library/stdtypes.html#truth-value-testing>`__.

.. note::

    The regular ``assert`` python statement is not guaranteed to work in Ren'py.
    Notably, it was disabled in version 7, and in some older versions.

    Therefore, the following may not actually check what it's supposed to check::

        $ assert some_function(args)

    In some versions of Ren'py or depending on unpredictable conditions,
    ``some_function`` may not even get called. The assert test statement should
    be used instead.

jump statement
--------------

call statement
--------------

.. reminder that there is no return statement in testcases

.. to jump to a renpy label, use the run clause:: run Jump("label_name")

clause statement
----------------

A :ref:`clause <test-clauses>` can be given, just by itself. ::

    pause 5
    click

until statement
---------------

This statement consists in two :ref:`clauses <test-clauses>`, separated by the
word ``until``.

If and when the clause on the right is ready, it is executed and control is
passed to the next statement. Otherwise, the left clause is executed until the
right clause is ready, and then the right clause is executed.

This is basically an inline while loop. ::

    click until eval renpy.get_screen("choice")
    "ask her right"
    click until "It's an interactive book."

exit statement
--------------

Quits the game without calling the confirmation screen.
Does not save the game when quitting::

    if eval need_to_confirm:
        run Quit(confirm=True) # asks for confirmation, and autosaves

    if eval persistent.quit_test_using_action:
        run Quit(confirm=False) # does not ask, but still autosaves

    exit # neither asks nor autosaves

.. _test-clauses:

Test clauses
============

Clauses are defined by two things: what it does when they are executed, and
under what circumstances they are ready. They can be part of ``if``, ``assert``
or ``until`` test statements, or they can simply be given on their own (see
above).

.. for each one, say what makes it ready

pass clause
--------------

Does not do anything. It's a no-op, allowing for empty testcases. ::

    testcase not_yet_implemented:
        pass

It is always ready.

click clause
---------------

Executes a simulated click on the screen. It takes the following optional
properties:

- ``button`` specifies which button of the simulated mouse is to be clicked
  with. It takes an integer and defaults to 1. 1 is a left-click, 2 is a
  right-click, 3 is a scrollwheel-click, 4 and 5 are additional buttons found on
  some mouses. Normally only 1 and 2 trigger any response from Ren'py.
- ``pos`` specifies where to click, as a pair of x/y coordinates. Coordinates
  are taken relative to the screen. Floats between 0.0 and 1.0 are supported as
  a fraction of the screen size in either dimension. ``absolute`` and other
  means of expressing positions are not supported, since you can't move the
  mouse to a subpixel-precise position.

.. ``always`` is not documented because useless in the case of the click clause by itself

Click behaves like a :ref:`pattern <test-pattern>`\ -taking clause which would
not be given a pattern: if no ``pos`` is provided, it will look for a neutral
place where a click would not occur on a focusable element.

.. give example for both

This clause is always ready.

The :func:`has_default_focus` function is a helpful accessor to know whether a
game can be advanced by a bare ``click`` clause or not::

    click until eval (not renpy.has_default_focus())

string expression clause
------------------------

This clause consists in a simple string, which is interpreted as a
:ref:`pattern <test-pattern>`. It executes by simulating a click on the target
identified by the pattern.

It takes three optional properties:

- ``button`` - same as the click clause
- ``pos`` - same as the click clause, but the position is relative to the
  focusable area of the target. If the position is ommitted or is invalid, for example if a
  button is 100x100 pixels and the given ``pos`` is (105, 150), then the ``pos``
  is ignored and a random position within the target is used instead.
- ``always`` does not take a value. It overrides the readiness of the clause,
  making it always ready.

This clause is ready if and when its pattern resolves to a suitable target found
on the screen, or if it is given the ``always`` property. ::

    testcase play_the_game:
        "start"

run clause
-------------

Runs the provided :doc:`screen-language action <screen_actions>` (or list of
actions).

Ready if and when a button containing the provided action (or list) would be
sensitive. ::

    testcase chapter_3:
        run Jump("chapter_3")

pause clause
---------------

Pauses test execution for a given number of seconds.

This clause is always ready. ::

    pause 5.0

Similar to the :ref:`pause-statement`, but requires a value (there is no
click-to-continue pause in tests).

label clause
---------------

Does not do anything when executed. This clause only exists to be used inside
clause-taking test statements like ``assert``, ``if`` or ``until``.

The label clause is ready if and when the provided label has been passed between
the current test statement and the one just before.

Attention, this means that the following example does not work::

    "play chapter 1"
    # passing the "chapter_1" label
    pause 1
    assert label chapter_1

It will not work because no renpy label will have been reached between the
statement containing the label clause and the preceding statement, which in this
case are the assert statement and the pause statement, respectively. The same
happens in the following example::

    "play chapter 1"
    # passing the "chapter_1" label
    assert label chapter_1 # works
    assert label chapter_1 # fails

The chapter_1 label is not reached between the first label clause and the second
label clause, therefore the second label clause fails (technically, the clause
is not ready and the assert fails).

In both examples, the assert label statement would have worked if it were placed
on its own, directly after the ``"play chapter 1"`` string expression statement
(or after the comment, which doesn't count as a statement)::

    "play chapter 1"
    # passing the "chapter_1" label
    assert label chapter_1
    # all fine

.. warning::

    This clause should not be confused with the Ren'py native
    :ref:`label <label-statement>` statement it refers to, or with the unrelated
    :ref:`screen-language label element <sl-label>`.

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

.. _test-eval-clause:

eval clause
-----------

This clause is ready if and when the provided expression evaluates to a true
value, in a boolean context.

When executed, does not do anything other than evaluating the expression it is
given. This clause exists only to be used inside clause-taking test statements
like ``assert``, ``if`` or ``until``, effectively turning ``assert`` and ``if``
into their non-clause-taking python equivalents::

    assert eval (renpy.is_in_test() and
                 ("Ren'py" in renpy.version_string))

.. note::

    Differences between a dollar-line and the eval clause :

    - A dollar-line executes any python statement, which does not necessarily
      have a value - for example ``$ import math`` - while the eval clause
      requires an expression, a.k.a something having a value.
    - The eval clause provides a value to an ``if`` or ``until`` statement,
      while these statements can't take a dollar sign, much less a dollar-line.

..

    When the returned value of a function call is to be ignored, both are technically equivalent::

        $ print("Test 1")
        eval print("Test 2")

    This is because functions always return a value (None being a value), unless they raise an exception.

type clause
--------------

.. simulate a key-pressing or the typing of text

..
    It is ready if a pattern is not provided,
    or if one is provided and a suitable target is found on the screen.
    For the clauses taking the ``always`` property, that property overrides the readiness of the clause.

..
    warning disambiguation this has nothing to do with the python builtin

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

Boolean clause operations
-------------------------

Test clauses support the ``not``, ``and`` and ``or`` operators: an expression
containing clauses linked with these operators can be provided in lieu of a
single clause. That expression must always be enclosed in parentheses.

The readiness of a boolean clause expression is the computation of the readiness
of the clauses it contains:
- ``(not a)`` is ready if and when ``a`` is not ready
- ``(a and b)`` is ready when both ``a`` and ``b`` are ready
- ``(a or b)`` is ready when either ``a`` or ``b`` is ready.

What happens when boolean clause operations execute is a little more complex.
When executed:
- ``not`` doesn't do anything.
- ``and`` executes both clauses if both are ready, and the left one otherwise.
- ``or`` executes its ready clause(s), if any, and the right one otherwise. (TODO : maybe it should execute the ready clause if only one is, and the right one otherwise)

More information can be found in the python documentation
`regarding these operators <https://docs.python.org/3/reference/expressions.html#boolean-operations>`__
as for why it works that way. The readiness and the behavior of such expressions
when executed can be inferred by replacing each clause in the expression with
its respective readiness, and working out which of the clause is the result of
the operation.

.. _test-pattern:

Patterns
===============

Some clauses take a pattern, which helps positioning the mouse or locating where
a clause will do what it does.

The ``pattern`` property takes a string (except in the case of the string
expression clause, where it is the string itself) which resolves to a target
found on the screen, based on the shortest match among the alt text of focusable
screen elements (typically, buttons). The search is case-insensitive.

If no pattern is given, the virtual test mouse is positioned to the last
previous location where a click happened, or to the specified position, if any.
If that position lies on a focusable element, a random position in the screen
which does not overlap a focusable element is chosen instead.

If a pattern is given, the mouse is positioned to the last previous location
where a click happened, or to the specified position, if any. If that position
does not lie inside the targeted element, a random position within it is chosen
instead. To that end, things like :propref:`focus_mask` are taken into account.

If a pattern is given and if it does not resolve to a target at the time when
the clause using it executes, an exception is raised (terminating the test). To
test whether a given pattern resolves to a target at a given time, the readiness
condition of a string expression clause can be evaluated inside an if statement::

    if "ask her right": # if there is a focusable element containing that text on screen
        # add a clause using that pattern
