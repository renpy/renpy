.. _python:

Python Statements
=================

Ren'Py is written in the Python programming language, and includes
support for including Python inside Ren'Py scripts. Python
support can be used for many things, from setting a flag to creating
new displayables. This chapter covers ways in which Ren'Py scripts can
directly invoke Python, through the various python statements.


.. _python-statement:

Python
------

The python statement takes a block of Python, and runs the block
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
    block of Python in an anonymous scope. The scope will be lost when the
    python block terminates.

    This allows Python to use temporary variables that can't be
    saved - but it means that the store needs to be accessed as fields
    on the store object, rather than directly.

``in``

   The ``in`` modifier takes a name. Instead of executing in the
   default store, the Python will execute in the store with that
   name.


One-line Python Statement
-------------------------

A common case is to have a single line of Python that runs in the
default store. For example, a Python one-liner can be used to
initialize or update a flag. To make writing Python one-liners
more convenient, there is the one-line python statement.

The one-line python statement begins with the dollar-sign ($)
character, and contains everything else on that line. Here
are some example of python one-liners::

    # Set a flag.
    $ flag = True

    # Initialize a variable.
    $ romance_points = 0

    # Increment a variable.
    $ romance_points += 1

    # Call a function that exposes Ren'Py functionality.
    $ renpy.movie_cutscene("opening.ogv")

Python one-liners always run in the default store.


.. _init-python-statement:

Init Python Statement
---------------------

The ``init python`` statement runs Python at initialization time,
before the game loads. Among other things, this can be used to define
classes and functions, or to initialize styles, config variables, or
persistent data. ::

    init python:

        def auto_voice_function(ident):
            return "voice/" + ident + ".ogg"

        config.auto_voice = auto_voice_function

        if persistent.endings is None:
            persistent.endings = set()

    init 1 python:

        # The bad ending is always unlocked.
        persistent.endings.add("bad_ending")

A priority number can be placed between ``init`` and ``python``. When
a priority is not given, 0 is used. Init  statements are run in priority
order, from lowest to highest. Init statements of the same priority are run in
unicode order by filename, and then from top to bottom within a file.

To avoid conflict with Ren'Py, creators should use priorities in the
range -999 to 999. Priorities of less than 0 are generally used for
libraries and to set up themes. Normal init statements should have a priority
of 0 or higher.

Init python statements also take the ``hide`` or ``in`` clauses.

Variables that have their value set in an init python block are not
saved, loaded, and do not participate in rollback. Therefore, these
variables should not be changed after init is over.

.. _define-statement:

Define Statement
----------------

The define statement sets a single variable to a value at init time.
For example::

    define e = Character("Eileen")

is equivalent to::

    init python:
        e = Character("Eileen")

The define statement can take an optional named store (see below), by
prepending it to the variable name with a dot. For example::

    define character.e = Character("Eileen")

One advantage of using the define statement is that it records the
filename and line number at which the assignment occurred, and
makes that available to the navigation feature of the launcher.

Variables that are defined using the define statement are treated
as constant, are not saved or loaded, and should not be changed.
(Ren'Py does not enforce this, but will produce undefined behavior
when this is not the case.)

.. _default-statement:

Default Statement
-----------------

The default statement sets a single variable to a value if that variable
is not defined when the game starts, or after a new game is loaded. For
example::

    default points = 0

When the variable ``points`` is not defined at game start, this statement is
equivalent to::

    label start:
        $ points = 0

When the variable ``points`` is not defined at game load, it's equivalent to::

    label after_load:
        $ points = 0

The default statement can take an optional named store (see below), by
prepending it to the variable name with a dot. For example::

    default schedule.day = 0


.. _init-offset-statement:

Init Offset Statement
---------------------

The init offset statement sets a priority offset for all statements
that run at init time. (init, init python, define, default, screen,
transform, style, and more.) The offset applies to all following
statements in the current block and chold blocks, up to the next
init priority statement. The statement::

    init offset = 42

sets the priority offset to 42. In::

    init offset = 2
    define foo = 2

    init offset = 1
    define foo = 1

    init offset = 0

The first define statement is run at priority 2, which means it runs
after the second define statement, and hence ``foo`` winds up with
a value of 2.

Names in the Store
------------------

The default place that Ren'Py stores Python variables is called the
store. It's important to make sure that the names you use in the
store do not conflict.

The define statement assigns a value to a variable, even when it's
used to define a character. This means that it's not possible to
use the same name for a character and a flag.

The following faulty script::

    define e = Character("Eileen")

    label start:

        $ e = 0

        e "Hello, world."

        $ e += 1
        e "You scored a point!"

will not work, because the variable `e` is being used as both a
character and a flag. Other things that are usually placed into
the store are transitions and transforms.

Names beginning with underscore (\_) are reserved for Ren'Py's
internal use. In addition, there is an :ref:`Index of Reserved Names <reserved-names>`.


Other Named Stores
------------------

Named stores provide a way of organizing Python functions and variables
into modules. By placing Python in modules, you can minimize the chance of name
conflicts.

Named stores can be accessed by supplying the ``in`` clause to
``python`` or ``init python``, all of which run Python in a named
store. Each store corresponds to a Python module. The default store is
``store``, while a named store is accessed as ``store``.`name`. These
python modules can be imported using the Python import statement,
while names in the modules can be imported using the Python from
statement.

For example::

    init python in mystore:

        serial_number = 0

        def serial():

            global serial_number
            serial_number += 1
            return serial_number

    init python:
        import store.mystore as mystore

    label start:
        $ serial = mystore.serial()


Named stores participate in save, load, and rollback in the same way
that the default store does. The defined statement can be used to
define names in a named store.


.. _python-modules:

First and Third Party Python Modules and Packages
-------------------------------------------------

Ren'Py can import pure-python modules and packages. First-party modules
and packages - ones  written for the game - can be placed directly
into the game directory. Third party packages can be placed into the
game/python-packages directory.

For example, to install the requests package, one can change into the
game's base directory, and run the command::

    pip install --target game/python-packages requests

In either case, the module or package can be imported from an init python
block::

    init python:
        import requests

.. warning::

    Python defined in .rpy files is transformed to allow rollback
    to work. Python imported from .py files is not. As a result,
    objects created in Python will not work with rollback, and
    probably should not be changed after creation.
