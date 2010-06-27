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
the Ren'Py directory ending with the .rpy extension. Ren'Py will
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

* The last character on the line is a backslash ('\').

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
           "spans more than one line. ]

Empty logicial lines are ignored.
           

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

Ren'Py statements are made of a few basic 

:dfn:`Keyword`

    A keyword is a word that must literally appear in the source
    code. They're used to introduce statements and properties.

    Names begining with a single underscore (_) are reserved for
    Ren'Py internal use, unless otherwise documented. When a name
    begins with __ but doesn't end with __, it is changed to a
    file-specfic version of that name.
    
:dfn:`Name`

    A name begins with a letter or underscore, which is followed by
    zero or more letters, numbers, and underscores. For our purpose,
    unicode characters between U+00a0 and U+fffd are considered to be
    letters.

:dfn:`Image Name`

    An image name consists of one or more names, separated by
    spaces. The name ends at the end of the statement, or when a
    keyword is encountered.

    The first component of an image name is known as the :dfn:`image
    tag`. For example, ``eileen happy`` is an image name, and
    ``eileen`` is its image tag.
    
:dfn:`String`

    A string begins with a quote character (one of ", ', or \`),
    contains some sequence of characters, and ends with the same quote
    character.

    The backslash character (\) is used to escape quotes, special
    characters such as % (written as \%) and { (written as \{). It's
    also used to include newlines, using the \n sequence.

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


