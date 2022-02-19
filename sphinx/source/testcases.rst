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
        advance (proposed)
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
.. turn into a clause ?

jump statement
--------------

call statement
--------------

    .. reminding (for both jump and call) that there is no return statement in testcases

clause statement
----------------
..
    takes a single clause (a way of saying-without-saying that clauses are statements)

until statement
---------------
..
    between one left clause and one right clause, on a single line
    executes the left clause until the right clause is ready
    then executes the right clause once before returning
    executes the left one once ?
    basically an inline (do-?)while loop

pass statement
--------------
..
    a noop

exit statement
--------------
..
    quits the game, ending the game without confirmation

Test clauses
============

Clauses have the property of being ready or not ready.
They can be part of (test-)if or until statements, or they can be simply on their own (see above).
A non-ready clause on its own will not cause an error when executed, at worse it will result in a noop.

.. for each one, say what makes it ready

run clause
-------------
..
    executes the provided screen-language action (link to the doc page about actions)
    ready if a button containing the action would be sensitive.

pause clause
---------------
..
    pauses for the given number of seconds
    always ready

label clause
---------------
..
    does not *do* anything meaningful when executed
    raises an exception if the provided label is not being passed or has not just been passed when it's executed
    watch out, pretty sensitive about "just being passed", adding a (test) timed pause before a working label
    will make it fail
    similar to an assert statement, except it's a clause and it only applies to label conditions

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

.. propositions (still clauses but not approved or not implemented) :

pass clause
--------------
..
    (proposed noop)
    always ready

eval clause
-----------
..
    does not do anything meaningful when executed, even less than the label clause
    is ready if and when the given value is true in a boolean way

advance clause
-----------------
..
    like the press of space in renpy
    unready during a choice for example (only if that's detectable)
    `advance until "A video game"`

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
    do something if/when the pattern is not found
    instead of just blocking

..
    Their readiness condition (for type, move, clock and string) : it is ready if a pattern is not provided,
    or if one is provided and a suitable target is found on the screen.
    For the clauses taking the ``always`` property, that property overrides the readiness of the clause.

Patterns
===============

Some clauses take a pattern.
The ``pattern`` property (or in the case of the string expression, the string itself) takes a string
which resolves to a target found on the screen, based on the shorted match in the alt text of
focusable screen elements.
