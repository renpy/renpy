===============
Language Basics
===============

Before we can describe the Ren'Py language, we must first describe the
structure of a Ren'Py script. This includes how files are broken into
blocks made up of lines, and how those lines are broken into the
elements that make up statements.

Files
=====

The script of a Ren'Py game is made up of all the files found under the
:file:`game/` directory ending with the :file:`.rpy` extension. Ren'Py will
consider each of these files and will use the contents of the files as the script.

Generally, there's no difference between a script written in one big file and a
script broken into multiple files. Control can be transferred within the script
(including between files) by jumping to or calling a :doc:`label <label>` in
another file. This makes the division of a script up into files a matter of
personal style : some game creators prefer to have small files (like one
per event, or one per day), while others prefer to have one big script.

To speed up loading time, Ren'Py will compile the :file:`.rpy` files into
:file:`.rpyc` files when it starts up. When a :file:`.rpy` file is changed, the
:file:`.rpyc` file will be updated when Ren'Py starts up. However, if a
:file:`.rpyc` file exists without a corresponding :file:`.rpy` file, the
:file:`.rpyc` file will be used. This can lead to problems if a :file:`.rpy`
file is deleted, or renamed, or moved, without deleting the :file:`.rpyc`
file : the script it contains will still get executed.

Filenames must begin with a letter or number, but may not begin with
"00", as Ren'Py uses such files for its own purposes.

Base Directory
--------------

The base directory is the directory that contains all files that are
distributed with the game (even though not all the files in the base directory
are usually distributed). See also : :doc:`build`. Things like README files
should be placed in the base directory.

The base directory is created within the "Projects Directory", which can be set
in the Launcher, when you create a new game. For example, if your Projects
Directory is named :file:`renpygames`, and your game is named "HelloWorld", your
base directory will be :file:`renpygames/HelloWorld`.

Game Directory
--------------

The game directory is a directory named "game" inside the base directory. For
example, if your base directory is :file:`renpygames/HelloWorld`, your game
directory will be :file:`renpygames/HelloWorld/game`.

The game directory contains all the files used by the game. It, including all
subdirectories, is scanned for :file:`.rpy` and :file:`.rpyc` files, and those
are combined to form the game script. It is scanned for :file:`.rpa` archive
files, and those are automatically used by the game. Finally, when Ren'Py takes
or considers a path to a file, the path is (with very few exceptions) relative
to the game directory (but note that :var:`config.searchpath` can change this).

Comments
========

A Ren'Py script file may contain comments. A comment begins with a
hash mark (``#``), and ends at the end of the line containing the
comment. As an exception, a comment may not be part of a string.

::

    # This is a comment.
    show black # this is also a comment.

    "# This isn't a comment, since it's part of a string."

Ren'Py ignores comments, so the script is treated like the comment
wasn't there.


Logical Lines
=============

A script file is broken up into :dfn:`logical lines`. A logical line
always begins at the start of a line in the file. A logical line ends
at the end of a line, unless:

* The last character on the line is a backslash (``\``).

* The line contains an open parenthesis character (``(``, ``{``, or ``[``),
  that hasn't been matched by the corresponding closing parenthesis
  character (\ ``)``, ``}``, or ``]``, respectively).

* The end of the line occurs during a string - *any* string, even with single
  quotes, as opposed to Python rules.

Once a logical line ends, the next logical line begins at the start of
the next line.

Most statements in the Ren'Py language consist of a single logical line.

::

   "This is one logical line"

   "Since this line contains a string, it continues
    even when the line ends."

   $ a = [ "Because of parenthesis, this line also",
           "spans more than one line." ]

Empty lines are ignored and do not count as logical lines.


Indentation and Blocks
======================

:dfn:`Indentation` is the name we give to the space at the start of
each logical line that's used to line up Ren'Py statements. In
Ren'Py, indentation must consist only of spaces.

Indentation is used to group statements into :dfn:`blocks`. A block is
a group of lines, and often a group of statements. The rules for
dividing a file into blocks are:

* A block is open at the start of a file.

* A new block is started whenever a logical line is indented past the
  previous logical line.

* All logical lines inside a block must have the same indentation.

* A block ends when a non-empty logical line is encountered with less
  indentation than the lines in the block.

Indentation is very important in Ren'Py, as it is in Python, and it can cause
syntax or logical errors when it's incorrect. At the same time, the use of
indentation to express the block structure is far simpler than other languages
using other delimiters.

::

    "This statement, and the if statement that follows, are part of a block."

    if True:

        "But this statement is part of a new block."

        "This is also part of that new block."

    "This is part of the first block, again."


.. _elements-of-statements:

Elements of Statements
======================

Ren'Py statements are made of a few basic parts.

:dfn:`Keyword`
    A keyword is a word that must literally appear in the script of the game.
    Keywords are typically used to introduce statements and properties.

:dfn:`Name`
    A name begins with a letter or underscore, which is followed by
    zero or more letters, numbers, and underscores. For our purpose,
    Unicode characters between U+00a0 and U+fffd are considered to be
    letters.

    .. warning::

        Names beginning with a single underscore (_) are reserved for
        Ren'Py internal use, unless otherwise documented.

        When a name begins with two underscores (__) but doesn't end with two
        underscores, it is changed to a file-specific version of that name.

:dfn:`Image Name`
    An :dfn:`image name` consists of one or more components, separated by
    spaces. The first component of the image name is called the
    :dfn:`image tag`. The second and later components of the name are
    the :dfn:`image attributes`. An image component consists of a
    string of letters, numbers, and underscores.

    For example, take the image name ``mary beach night happy``. The
    image tag is ``mary``, while the image attributes are,
    ``beach``, ``night``, and ``happy``.

    The words ``at``, ``as``, ``behind``, ``onlayer``, ``with``, and ``zorder``, may
    not be used as parts of an image name.

:dfn:`String`
    A string begins with a quote character (one of ", ', or \`), contains some
    sequence of characters, and ends with the same quote character.

    The backslash character (\\) is used to escape quotes, special
    characters such as % (written as \\%), [ (written as \\[), and
    { (written as \\{). It's also used to include newlines, using the \\n
    sequence.

    Inside a Ren'Py string, consecutive sequences of whitespace and line
    breaks are compressed into a single whitespace character, unless a space is
    preceded by a backslash. ::

        'Strings can\'t contain their delimiter, unless you escape it.'

        "There will be a space between the two following
         words."

        "There will be a line break between\nthese."

        "And there will be three spaces between\ \ \ these."

    The ``r`` prefix is supported, and follow more or less the same rules as in
    Python. Other prefixes, like ``u``, ``b`` or ``f``, are not supported.
    Triple-quoted strings are generally not accepted in places where a normal
    string is expected, and when they are, they usually yield a different
    result - see :ref:`monologue-mode` for an example.

    .. note::

        This applies to strings found *directly* in Ren'Py script, such as in
        :ref:`say-statement` or :doc:`menus`. Strings found inside
        :ref:`python statements <python-statement>`, or in expressions (see
        below), follow ordinary Python rules.

:dfn:`Simple Expression`
    A simple expression is a Python expression, used to include Python
    in some parts of the Ren'Py script. A simple expression begins
    with:

    * A name.
    * A string.
    * A number.
    * Any Python expression, in parenthesis.

    This can be followed by any number of:

    * A dot followed by a name.
    * A parenthesised Python expression.

    As an example, ``3``, ``(3 + 4)``, ``foo.bar``, and ``foo(42)``
    are all simple expressions. But ``3 + 4`` is not, as the
    expression ends at the end of a string.

:dfn:`Python Expression`
    A Python expression is an arbitrary Python expression, that may not include
    a colon. These are used to express the conditions in the
    :ref:`if <if-statement>` and :ref:`while <while-statement>` statements.


Common Statement Syntax
=======================

Most Ren'Py statements share a common syntax. With the exception of the
:ref:`say-statement`, they begin with a keyword that introduces the statement.
This keyword is followed by a parameter, if the statement takes one.

The parameter is then followed by one or more properties. Properties
may be supplied in any order, provided each property is only supplied
once. A property starts off with a keyword. For most properties, the
property name is followed by one of the syntax elements given above.

If the statement takes a block, the line ends with a colon (:). Otherwise, the
line just ends.


.. _python-basics:

Python Expression Syntax
========================

.. note::

    It may not be necessary to read this section thoroughly right
    now. Instead, skip ahead, and if you find yourself unable to figure
    out an example, or want to figure out how things actually work, you
    can go back and review this.

Many portions of Ren'Py take Python expressions. For example, defining
a new Character involves a call to the :func:`Character` function. While
Python expressions are very powerful, only a fraction of that power is
necessary to write a basic Ren'Py game.

Here's a synopsis of Python expressions.

:dfn:`Integer`
    An integer is a number without a decimal point. ``3`` and ``42``
    are integers.

:dfn:`Float`
    A float (short for floating-point number) is a number with a
    decimal point. ``.5``, ``7.``, and ``9.0`` are all floats.

:dfn:`String`
    Python strings begin with " or ', and end with the same
    character. \\ is used to escape the end character, and to
    introduce special characters like newlines (\\n). Unlike Ren'Py
    strings, Python strings can't span several lines, or be delimited with \`.

:dfn:`True, False, None`
    There are three special values. ``True`` is a true value, ``False`` is
    a false value. ``None`` represents the absence of a value.

:dfn:`Tuple`
    Tuples are used to represent containers where the number of items
    is important. For example, one might use a 2-tuple (also called a
    pair) to represent width and height, or a 4-tuple (x, y, width,
    height) to represent a rectangle.

    Tuples begin with a left-parenthesis ``(``, consist of zero or
    more comma-separated Python expressions, and end with a
    right-parenthesis ``)``. As a special case, the one-item tuple
    must have a comma following the item. For example::

        ()
        (1,)
        (1, "#555")
        (32, 24, 200, 100)

:dfn:`List`
    Lists are used to represent containers where the number of items
    may vary. A list begins with a ``[``, contains a comma-separated
    list of expressions, and ends with ``]``. For example::

        []
        [1]
        [1, 2]
        [1, 2, 3]

:dfn:`Variable`
    Python expressions can use variables, that store values defined using the
    :ref:`define-statement` or the :ref:`default-statement`. A variable name
    follows the rules of a :dfn:`name` as explained in
    :ref:`elements-of-statements`. For example::

        playername
        love_love_points
        trebuchet2_range

:dfn:`Field Access`
    Python modules and objects have fields, which can be accessed by following
    an expression (usually a variable) with a dot and the field name.
    For example::

       config.screen_width

    consists of a variable (config) followed by a field access
    (screen_width).

:dfn:`Call`
    Python expressions can call a function which returns a value. They
    begin with an expression (usually a variable), followed by a
    left-parenthesis, a comma-separated list of arguments, and a
    right-parenthesis. The argument list begins with the position
    arguments, which are Python expressions. These are followed by
    keyword arguments, which consist of the argument name, an equals
    sign, and an expression. In this example::

        Character("Eileen", type=adv, color="#0f0")

    we call the :func:`Character` function. It's given one positional
    argument, the string "Eileen". It's given two keyword argument:
    ``type`` with the value of the ``adv`` variable, and ``color``
    with a string value of ``"#0f0"``.

    Other objects than functions can be called, and are widely known as
    :dfn:`callables`.

When reading this documentation, you might see a function signature
like:

.. function:: Sample(name, delay, position=(0, 0), **properties)

    A sample function that doesn't actually exist in Ren'Py, but
    is used only in documentation.

This function:

* Has the name "Sample"
* Has two positional parameters, a name and a delay. In a real
  function, the types of these parameters would be made clear
  from the documentation.
* Has one keyword argument, position, which has a default value
  of (0, 0).

Since the functions ends with ``**properties``, it means that it can
take :doc:`style properties <style_properties>` as additional keyword
arguments. Other special entries are ``*args``, which means that it takes
an arbitrary number of positional parameters, and ``**kwargs``, which means
that it takes a wide range of keyword parameters which are usually explained
in the function's documentation.

When you see a ``/`` symbol on its own in a function signature, it means that
the parameters before it are positional-only, and should not be passed by
keyword. When you see a ``*`` symbol on its own, conversely, it means that the
parameters *after* it are keyword-only, which means that they should only be
passed using the ``name=value`` syntax.

Python is a lot more powerful than we have space for in this manual. To learn
Python in more detail, we recommend starting with the Python tutorial, which is
available from `python.org <https://docs.python.org/tutorial/index.html>`__.
While a deep knowledge of Python is not necessary to work with Ren'Py, knowing
the basics of Python statements and expressions is often helpful.
