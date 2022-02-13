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
        until
        test clauses:
            run
            pause
            label
            drag
            scroll
            numeric expression (proposed)
            pass (proposed)
            advance (proposed)
            pattern clauses:
                type
                move
                click
                string expression

=====================
Integrated test suite
=====================

Ren'py allows creators to put tests in their games to make sure that an alteration to the code didn't break the game.
Blah.

.. introduce the testcase statement itself, like the `transform:` statement
.. note about there being no return statement, unlike label the deindent closes the block

Test statements
===============

if statement
------------
..
    not the same as the renpy or python versions :
    it can't take all python values, only a test clause
    the clause being ready is the actual condition for the block to execute or not

python block statement
----------------------
.. difference with the default python block statement, apart from the hide/store params ?

dollar line
-----------
.. same interrogations as with python blocks

assert statement
----------------
..
    like a python assert, raises an AssertionError when the value it is given does not evaluate to a true value
    links to python doc regarding asserts, and to stdtypes about boolean evaluation
    note about regular asserts usually not working outside of this case in regular python blocks in renpy

jump statement
--------------

call statement
--------------

    .. reminding (for both jump and call) that there is no return statement in testcases

until statement
---------------
..
    between one left clause and one right clause, on a single line
    executes the left clause until the right clause is ready
    then executes the right clause once before returning
    executes the left one once ?
    basically an inline (do-?)while loop


Clause statements
=================

Test clauses are a subset of test statements, which have the property of being ready or not ready.
They can be part of (test-)if or until statements, or they can be simply on their own.
A non-ready clause on its own will not cause an error when executed, at worse it will result in a noop.

.. for each one, say what makes it ready

run statement
-------------
..
    executes the provided screen-language action (link to the doc page about actions)
    ready if a button containing the action would be sensitive.

pause statement
---------------
..
    pauses for the given number of seconds
    always ready

label statement
---------------
..
    (check this) does not *do* anything
    ready when execution just passes (or passed) the given label

drag statement
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

scroll statement
----------------
..
    takes a string giving it a pattern
    ready when the target (pattern) is found
    If the target is a bar, scrolls it down a page. If already at the bottom, returns it to the top.

.. propositions (still clauses but not approved or not implemented) :

numeric expression
------------------
.. (proposed alias to pause clause, may be integrated into expression)

pass statement
--------------
..
    (proposed noop)
    always ready

advance statement
-----------------
..
    like the press of space in renpy
    unready during a choice for example (only if that's detectable)
    `advance until "A video game"`

Pattern clauses
===============

Pattern clauses are a subset of clause statements. They share a number of things.

type statement
--------------
.. simulate a key-pressing or the typing of text

move statement
--------------

click statement
---------------

string expression
-----------------
.. alias for the click statement, giving it a target
