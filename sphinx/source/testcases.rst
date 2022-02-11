.. _testcases:

=====================
Integrated test suite
=====================

Ren'py allows creators to put tests in their games to make sure that an alteration to the code didn't break the game.
Blah.

.. introduce the testcase statement itself, like the `transform:` statement
.. note about there being no return statement, unlike label the deindent closes the block

Test statements
===============

.. if (takes a block)
    not the same as the renpy or python versions :
    its condition is not any python value, it's a test clause

.. python (takes a block)
    difference with the default python block statement, apart from the hide/store params ?

.. $
    same interrogations as with python blocks

.. assert
    like a python assert, raises an AssertionError when the value it is given does not evaluate to a true value
    links to python doc regarding asserts, and to stdtypes about boolean evaluation
    note about regular asserts usually not working outside of this case in regular python blocks in renpy

.. jump

.. call

    .. reminding (for both jump and call) that there is no return statement in testcases

.. until (weird, can be after a clause)
    can take another clause


.. clauses :

.. run

.. pause

.. label

.. type

.. drag

.. move

.. click (with the bare-string variant ? or document it as expression ?)

.. scroll

.. string ? (if not documented in click or move)
