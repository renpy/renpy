Conditional Statements
======================

Ren'Py includes several statements that can alter control flow based on
expression values. (This is in addition to the :ref:`jump <jump-statement>`,
:ref:`call <call-statement>` and :ref:`return <return-statement>` statements,
which transfer control unconditionally.

Note that is pages discusses statements that can be used inside Ren'Py
script. Python embedded in a Ren'Py game uses the Python while, if,
and for statements, but can't embed Ren'Py script statements.

.. _if-statement:

If Statement
------------

The ``if`` statement conditionally executes a block of statements if a python
expression is true. It consists of an ``if`` clause, zero or more ``elif``
clauses, and an optional ``else`` clause.

Each clause should be on its own logical line, followed by a block of
statements. The ``if`` and ``elif`` clauses are followed by an expression,
while all clauses end with a colon ``:``.

Examples are::

    if flag:
        e "You've set the flag!"

::

    if points >= 10:
        jump best_ending
    elif points >= 5:
        jump good_ending
    elif points >= 1:
        jump bad_ending
    else:
        jump worst_ending

The expressions in the if statement are evaluated in order, from
first to last. When an expression evaluates to True, the block
corresponding to that statement is executed. When control reaches the
end of the block, it proceeds to the statement following the if
statement.

If all expressions evaluate to False, the block associated with
the ``else`` clause is executed, if the ``else`` clause is present.


.. _while-statement:

While Statement
---------------

The ``while`` statement executes a block of statements while an expression
evaluates True. For example::

    $ count = 10

    while count > 0:

        "T-minus [count]."

        $ count -= 1

    "Liftoff!"

::

    while True:

        "This is the song that never terminates."
        "It goes on and on, my compatriots."

The expression is evaluated when while statement is first reached, and
then each time control reaches the end of the block. When the expression
return a False value, the statement after the while statement is executed.

Ren'Py does not have continue, break, or for statements. Continue and break
statements can be replaced by jumps to labels placed before or after the
while loop, respectively. The first example of a while loop, above, shows
how a while loop can replace a for statement.


.. _pass-statement:

Pass Statement
--------------

The ``pass`` statement can be used when a block is required, but no
statement is suitable. It does nothing.

For example::

    if points >= 10:
        "You're doing great!"
    elif points >= 1:
        pass
    else:
        "Things aren't looking so good."

::

    # event.step() is a function that returns True while there are
    # still events that need to be executed.

    while event.step():
        pass

