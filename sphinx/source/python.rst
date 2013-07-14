=================
Python Statements
=================

Ren'Py is written in the Python programmming language, and includes
support for including python code inside Ren'Py scripts. Python
support can be used for many things, from setting a flag to creating
new displayables. This chapter covers ways in which Ren'Py scripts can
directly invoke Ren'Py code, through the various python statements.


.. _python-statement:

Python
------

The python statement takes a block of python code, and runs that code
when control reaches the statement. A basic python statement can be
very simple::

    python:
        flag = True

Python statements can get more complex, when necessary::

    python:
        player_health = max(player_health - damage, 0)
        if enemy_vampire:
            enemy_health = min(enemy_health + damage, enemy_max_health)

There are two modifiers to the python statement that change its
behavior:

``hide``

    If given the hide modifier, the python statement will run the
    code in an anonymous scope. The scope will be lost when the python
    block terminates.

    This allows python code to use temporary variables that can't be
    saved - but it means that the store needs to be accessed as fields
    on the store object, rather than directly.

``in``

   The ``in`` modifier takes a name. Instead of executing in the
   default store, the python code will execute in the store that
   name.

One-line Python Statement
-------------------------

A common case is to have a single line of python that runs in the
default store. For example, a python one-liner can be used to
initialize or update a flag. To make writing python one-liners
more convenient, there is the one-line python statement.

The one-line python statement begins with the dollar-sign ($)
character, and contains all of the code on that line. Here
are some example of python one-liners::

    # Set a flag.
    $ flag = True

    # Increment a variable.
    $ rabu_rabu_points += 1

    # Call a function that exposes Ren'Py functionality.
    $ renpy.movie_cutscene("opening.ogv")

Python one-liners always run in the default store.

Named Stores
------------

Named stores provide a way of organizing python code into modules. By
placing code in modules, you can minimize the chance of name
conflicts.

Named stores can be accessed by supplying the ``in`` clause to
``python`` or ``init python``, code can run accessed in a named
store. Each store corresponds to a python module. The default store is
``store``, while a named store is accessed a ``store``.`name`. These
python modules can be imported using the python import statement,
while names in the modules can be imported using the python from
statement.

Named stores participate in save, load, and rollback in the same way
that the default store does.


TODO:

* Note that names beginning with a single _ are reserved for Ren'Py's
  use.
