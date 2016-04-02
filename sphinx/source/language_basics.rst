===============
Language Basics
===============

Before we can describe the Ren'Py language, we must first describe the
structure of a Ren'Py script. This includes how a files are broken into
blocks made up of lines, and how those lines are broken into the
elements that make up statements.

Files
=====

The script of a Ren'Py game is made up of all the files found under
the game directory ending with the .rpy extension. Ren'Py will
consider each of these files (in unicode order), and will use the
contents of the files as the script.

Generally, there's no difference between a script broken into multiple
files, and a script that consists of one big file. Control can be
transferred between files by jumping to or calling a label in another
file.  This makes the division of a script up into files a matter of
personal style - some game-makers prefer to have small files (like one
per event, or one per day), while others prefer to have one big
script.

To speed up loading time, Ren'Py will compile the ``.rpy`` files into
.rpyc files when it starts up. When a ``.rpy`` file is changed, the ``.rpyc``
file will be updated when Ren'Py starts up. However, if a .rpyc file
exists without a corresponding ``.rpy`` file, the ``.rpyc`` file will be
used. This can lead to problems if a ``.rpy`` file is deleted without
deleting the .rpyc file.

Base Directory
--------------

The base directory is the directory that contains all files that are
distributed with the game. (It may also contain some files that are not
distributed with the game.) Things like README files should be placed in the
base directory, from where they will be distributed.

The base directory is created underneath the Ren'Py directory, and has the name
of your game. For example, if your Ren'Py directory is named renpy-6.11.2, and
your game is named "HelloWorld", your base directory will be
renpy-6.11.2/HelloWorld.

Game Directory
--------------

The game directory is almost always a directory named "game" underneath the
base directory. For example, if your base directory is renpy-6.11.2/HelloWorld,
your game directory will be renpy-6.11.2/HelloWorld/game.

However, Ren'Py searches directories in the following order:

* The name of the executable, without the suffix. For example,
  if the executable is named moonlight.exe, it will look for
  a directory named moonlight under the base directory.
* The name of the executable, without the suffix, and with
  a prefix ending with _ removed. For example, if the executable
  is moonlight_en.exe, Ren'Py will look for a directory named en.
* The directories "game", "data", and "launcher", in that order.

The launcher will only properly recognize the "game" and "data" directories,
however.

The game directory contains all the files used by the game. It, including all
subdirectories, is scanned for .rpy and .rpyc files, and those are combined to
form the game script. It is scanned for .rpa archive files, and those are
automatically used by the game. Finally, when the game gives a path to a file
to load, it is loaded relative to the game directory. (But note that
config.searchpath can change this.)

Comments
========

A Ren'Py script file may contain comments. A comment begins with a
hash mark ('#'), and ends at the end of the line containing the
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

* The last character on the line is a backslash ('\\').

* The line contains an open parenthesis character ('(', '{', or '['),
  that hasn't been matched by the cooresponding close parenthesis
  character (')', '}', or ']', respectively).

* The end of the line occurs during a string.

Once a logical line ends, the next logical line begins at the start of
the next line.

Most statements in the Ren'Py language consist of a single logical
line, while some statements consist of multiple lines.

::

   "This is one logical line"

   "Since this line contains a string, it continues
    even when the line ends."

   $ a = [ "Because of parenthesis, this line also",
           "spans more than one line." ]

Empty logical lines are ignored.


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

* A block ends when a logical line is encountered with less
  indentation than the lines in the block.

Indentation is very important to Ren'Py, and cause syntax or logical
errors when it's incorrect. At the same time, the use of indentation
to convey block structure provides us a way of indicating that
structure without overwhelming the script text.

::

   "This statement, and the if statement that follows, is part of a block."

   if True:

       "But this statement is part of a new block."

       "This is also part of that new block."

   "This is part of the first block, again."


Elements of Statements
======================

Ren'Py statements are made of a few basic parts.

:dfn:`Keyword`
    A keyword is a word that must literally appear in the source
    code. They're used to introduce statements and properties.

    Names beginning with a single underscore (_) are reserved for
    Ren'Py internal use, unless otherwise documented. When a name
    begins with __ but doesn't end with __, it is changed to a
    file-specific version of that name.

:dfn:`Name`
    A name begins with a letter or underscore, which is followed by
    zero or more letters, numbers, and underscores. For our purpose,
    unicode characters between U+00a0 and U+fffd are considered to be
    letters.

:dfn:`Image Name`
    An :dfn:`image name` consists of one or more components, separated by
    spaces. The first component of the image name is called the
    :dfn:`image tag`. The second and later components of the name are
    the :dfn:`image attributes`. An image component consists of a
    string of letters, numbers, and underscores.

    For example, take the image name ``mary beach night happy``. The
    image tag is ``mary``, while the image attributes are,
    ``beach``, ``night``, and ``happy``.

:dfn:`String`
    A string begins with a quote character (one of ", ', or \`),
    contains some sequence of characters, and ends with the same quote
    character.

    The backslash character (\\) is used to escape quotes, special
    characters such as % (written as \\%), [ (written as \\[), and
    { (written as \\{). It's also used to include newlines, using the \\n
    sequence.

    Inside a Ren'Py string, consecutive whitespace is compressed into
    a single whitespace character, unless a space is preceded by a
    backslash. ::

        'Strings can\'t contain their delimiter, unless you escape it.'

:dfn:`Simple Expression`
    A simple expression is a Python expression, used to include Python
    in some parts of the Ren'Py script. A simple expression begins
    with:

    * A name.
    * A string.
    * A number.
    * Any python expression, in parenthesis.

    This can be followed by any number of:

    * A dot followed by a name.
    * A parenthesised python expression.

    As an example, ``3``, ``(3 + 4)``, ``foo.bar``, and ``foo(42)``
    are all simple expressions. But ``3 + 4`` is not, as the
    expression ends at the end of a string.

:dfn:`At List`
    An at list is a list of simple expressions, separated by commas.

:dfn:`Python Expression`
    A python expression is an arbitrary python expression, that may
    not include a colon. These are used to express the conditions in
    the if and while statements.


Common Statement Syntax
=======================

Most Ren'Py statements share a common syntax. With the exception of
the say statement, they begin with a keyword that introduces the
statement. This keyword is followed by a parameter, if the statement
takes one.

The parameter is then followed by one or more properties. Properties
may be supplied in any order, provided each property is only supplied
once. A property starts off with a keyword. For most properties, the
property name is followed by one of the syntax elements given above.

If the statement takes a block, the line ends with a colon
(:). Otherwise, the line just ends.


.. _python-basics:

Python Expression Syntax
========================

.. note::

  It may not be necessary to read this section thoroughly right
  now. Instead, skip ahead, and if you find yourself unable to figure
  out an example, or want to figure out how things actually work, you
  can go back and review this.


Many portions of Ren'Py take python expressions. For example, defining
a new Character involves a call to the Character function. While
Python expressions are very powerful, only a fraction of that power is
necessary to write a basic Ren'Py game.

Here's a synopsis of python expressions.

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
    strings, python strings can't span lines.

:dfn:`True, False, None`
    There are three special values. ``True`` is a true value, ``False`` is
    a false value. ``None`` represents the absence of a value.

:dfn:`Tuple`
    Tuples are used to represent containers where the number of items
    is important. For example, one might use a 2-tuple (also called a
    pair) to represent width and height, or a 4-tuple (x, y, width,
    height) to represent a rectangle.

    Tuples begin with a left-parenthesis ``(``, consist of zero or
    more comma-separated python expressions, and end with a
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

        [ ]
        [ 1 ]
        [ 1, 2 ]
        [ 1, 2, 3 ]

:dfn:`Variable`
    Python expressions can use variables, that store values defined
    using the define statement or python statements. A variable begins
    with a letter or underscore, and then has zero or more letters,
    numbers, or underscores. For example::

       name
       love_love_points
       trebuchet2_range

    Variables beginning with _ are reserved for Ren'Py's use, and
    shouldn't be used by user code.

:dfn:`Field Access`
    Python modules and objects have fields, which can be accessed
    with by following an expression (usually a variable) with a
    dot and the field name. For example::

       config.screen_width

    Consists of a variable (config) followed by a field access
    (screen_width).

:dfn:`Call`
    Python expressions can call a function which returns a value. They
    begin with an expression (usually a variable), followed by a
    left-parenthesis, a comma-separated list of arguments, and a
    right-parenthesis. The argument list begins with the position
    arguments, which are python expressions. These are followed by
    keyword arguments, which consist of the argument name, and equals
    sign, and an expression. In the example example::

        Character("Eileen", type=adv, color="#0f0")

    we call the Character function. It's given one positional
    argument, the string "Eileen". It's given two keyword argument:
    ``type`` with the value of the ``adv`` variable, and ``color``
    with a string value of "#0f0".

    Constructors are a type of function which returns a new object,
    and are called the same way.

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

Since the functions ends with \*\*properties, it means that it can
take :ref:`style properties <style-properties>` as additional keyword
arguments. Other special entries are \*args, which means that it takes
an arbitrary number of positional parameters, and \*\*kwargs, which means
that the keyword arguments are described in the documentation.

Python is a lot more powerful than we have space for in this manual.
To learn Python in more detail, we recommend starting with the Python
tutorial, which is available from
`python.org <http://docs.python.org/release/2.7/tutorial/index.html>`_.
While we don't think a deep knowledge of Python is necessary to work
with Ren'Py, the basics of python statements and expressions is
often helpful.
