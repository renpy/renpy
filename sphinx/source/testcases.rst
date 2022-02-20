.. _testcases:

..
    testcase statement
    test statements:
        if
        python
        $
        assert
        jump
        call
        clause
        until
        pass
        exit
    test clauses:
        run
        pause
        label
        drag
        scroll
        pass
        type
        move
        click
        string expression
        eval

=====================
Integrated test suite
=====================

Ren'py allows creators to put tests in their games to make sure that an alteration to the code didn't break
the game.
Blah.

.. introduce the testcase statement itself, like the `transform:` statement
.. note about there being no return statement, unlike label the deindent closes the block

Test statements
===============
.. give an example for each one

python block statement
----------------------
.. difference with the default python block statement, apart from the hide/store params ?

dollar line
-----------
.. same interrogations as with python blocks

if statement
------------
This statement, like a python ``if`` statement, text a block.
Unlike the Ren'py or python versions however, it only takes a test clause, instead of a general python expression.
The provided clause being ready is the actual condition for the block to execute or not.

A normal python/renpy ``if`` can be emulated using the ``eval`` clause : ::

    if eval (persistent.should_advance and
             i_should_advance["now"]):
        click

..
    there is no elif nor else clause

assert statement
----------------
Like a python assert, this statement raises an AssertionError if and when the value it is given does not
evaluate to a true value. See the python documentation
`regarding asserts <https://docs.python.org/reference/simple_stmts.html#the-assert-statement>`_ and
about `boolean evaluation <https://docs.python.org/library/stdtypes.html#truth-value-testing>`_.

..
    .. note::

        The regular ``assert`` python statement is not guaranteed to work in Ren'py. It was disabled in
        version 7 and earlier.

jump statement
--------------

call statement
--------------

    .. reminding (for both jump and call) that there is no return statement in testcases

clause statement
----------------
A clause can be given, just by itself. ::

    pause 5

until statement
---------------
Takes two clauses, separated by the word ``until``.
If and when the right clause is ready, executes it and passes to the next statement.
If not, executes the left clause until the right clause is ready, then executes the right clause.

This is basically an inline while loop. ::

    click until "It's an interactive book."

pass statement
--------------
Does not do anything. It's a no-op, allowing empty testcases.

exit statement
--------------
Quits the game without calling the confirmation screen.
Does not save the game when quitting : ::

    if eval persistent.quit_test_with_action:
        run Quit(True) # does not confirm, but autosaves
    exit # neither confirms nor autosaves

Test clauses
============

Clauses have the property of being ready or not ready.
They can be part of (test-)if or until statements, or they can be simply on their own (see above).
It is safe to evaluate the readiness of a clause which could raise an exception if executed : ::

    if label preferences:
        "Dark theme"

.. for each one, say what makes it ready

run clause
-------------
Runs the provided :ref:`screen-language action <screen-actions>`.

Ready if and when a button containing the provided action would be sensitive.

.. does it accept a list of actions ?

pause clause
---------------
Pauses for a given number of seconds. Always ready.

label clause
---------------
This is a control, assert-like clause. It does not *do* anything when executed, but raises an
exception if the given label has not been passed by the script since the last executed test statement (or clause).

Attention, this means that a working label clause in a clause statement will be broken if, for example,
a pause clause in a clause statement gets added before it.

Ready if and when the provided label has just been passed.

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

scroll clause
----------------
..
    takes a string giving it a pattern
    ready when the target (pattern) is found
    If the target is a bar, scrolls it down a page. If already at the bottom, returns it to the top.

eval clause
-----------
Does not do anything when executed. This clause only exists to live inside ``if`` and ``until`` statements.

.. The provided expression can span on several lines, if wrapped in parentheses.

Ready if and when the provided value is true, in a boolean context.

.. note::

    Differences between a dollar-line, the assert statement and the eval clause :

    - A dollar-line executes any python statement, which does not necessarily have a value - for example
      ``$ test_variable = 5`` - while the assert statement and the eval clause require an expression, a.k.a
      something with a value.
    - The assert statement controls whether the provided value is correct or not.
    - The eval clause provides a value to an ``if`` or ``until`` statement.

type clause
--------------
.. simulate a key-pressing or the typing of text

move clause
--------------
..
    `move (position) [pattern (string)]`
    moves the virtual test mouse to the provided position, within the area targeted by the pattern
    or, if none is given, within the whole screen

click clause
---------------

string expression
-----------------
..
    alias for the click statement, giving it a target
    raises an exception if the pattern is not found

..
    Their readiness condition (for type, move, clock and string) : it is ready if a pattern is not provided,
    or if one is provided and a suitable target is found on the screen.
    For the clauses taking the ``always`` property, that property overrides the readiness of the clause.

Patterns
===============

Some clauses take a pattern.
The ``pattern`` property (or in the case of the string expression, the string itself) takes a string
which resolves to a target found on the screen, based on the shorted match in the alt text of
focusable screen elements. The search is case-insensitive.

..
    If no pattern is given, the virtual test mouse is positioned to the last previous location where
    a click happened. If that position lies on a focusable element, a random position in the screen
    which does not overlap a focusable element is chosen instead.

    If a pattern is given, the mouse is positioned to the last previous location where a click happened.
    If that position does not lie inside the targeted element, a random position within it is chosen instead.

.. :func:`has_default_focus`, simple accessor to whether a game can be advanced by a bare click or not
