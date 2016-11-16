.. _menus:
.. _menu-statement:

=============
In-Game Menus
=============

In many visual novels, the player is asked to make choices that
control the outcome of the story. The Ren'Py language contains a menus
statement that makes it easy to present choices to the user.

Here's an example of a menu statement::

    menu:
         "What should I do?"

         "Drink coffee.":
             "I drink the coffee, and it's good to the last drop."

         "Drink tea.":
             $ drank_tea = True

             "I drink the tea, trying not to make a political statement as I do."

         "Genuflect.":
             jump genuflect_ending

    label after_menu:

         "After having my drink, I got on with my morning."

The menu statement begins with the keyword menu. This may be followed
by a label name, in which case it's equivalent to preceding the menu
with that label. For example::

    menu drink_menu:
        ...

The menu statement is followed by an indented block. This block may
contain a :ref:`say statement <say-statement>`, and must contain at
least one menu choice. If the say statement is present, it is
displayed on the screen at the same time as the menu.

**Menu Choices.**
A menu choice is an option the user can select from the in-game
menu. A menu choice begins with a string. The string may be followed
by an if-clause, which makes the choice conditional. The menu choice
ends with a colon, and must be followed by a block of Ren'Py
statements.

When the choice is selected, the block of code is run. If execution
reaches the end of this block of code, it continues with the statement
after the end of the menu statement.

An if-clause consists of the keyword ``if``, followed by a python
expression. The menu choice is only displayed if the expression is
true. In the following menu::

    menu:
        "Go left.":
            ...
        "Go right.":
            ...
        "Fly above." if drank_tea:
            ...

The third choice will only be presented if the drank_tea variable is
true.
