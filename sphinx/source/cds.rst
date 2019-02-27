.. _cds:

Creator-Defined Statements
==========================

Creator-defined statements allow you to add your own statements to Ren'Py. This
makes it possible to add things that are not supported by the current syntax of
Ren'Py.

Creator-defined statements must be defined in a ``python early`` block. What's more,
the filename containing the user-defined statement must be be loaded earlier
than any file that uses it. Since Ren'Py loads files in Unicode sort order, it
generally makes sense to prefix the name of any file containing a user-defined
statement with 01, or some other small number.

A user-defined statement cannot be used in the file in which it is defined.

Creator-defined statement are registered using the :func:`renpy.register_statement`
function.

.. include:: inc/statement_register

The parse method takes a Lexer object:

.. class:: Lexer

    .. method:: error(msg)

        Adds a `msg` (with the current position) in the list of detected
        parsing errors. This interrupts the parsing of the current statement,
        but does not prevent further parsing.

    .. method:: require(thing, name=None)

        Tries to parse `thing`, and reports an error if it cannot be done.

        If `thing` is a string, tries to parse it using :func:`match`.
        Otherwise, thing must be a other method on this lexer object,
        which is called without arguments. If `name` is not specified,
        the name of the method will be used in the message
        (or `thing` if it's a string), otherwise the `name` will be used.

    .. method:: eol()

        True if the lexer is at the end of the line.

    .. method:: expect_eol()

        If we are not at the end of the line, raise an error.

    .. method:: expect_noblock(stmt)

        Called to indicate this statement does not expect a block.
        If a block is found, raises an error. `stmt` should be a string,
        it will be added to the message with an error.

    .. method:: expect_block(stmt)

        Called to indicate that the statement requires that a non-empty
        block is present. `stmt` should be a string, it will be added
        to the message with an error.

    .. method:: match(re)

        Matches an arbitrary regexp string.

        All of the statements in the lexer that match things are implemented
        in terms of this function. They first skip whitespace, then attempt
        to match against the line. If the match succeeds, the matched text
        is returned. Otherwise, None is returned, and the state of the lexer
        is unchanged.

    .. method:: keyword(s)

        Matches `s` as a keyword.

    .. method:: name()

        Matches a name. This does not match built-in keywords.

    .. method:: word()

        Matches any word, including keywords. Returns the text of the
        matched word.

    .. method:: image_name_component()

        Matches an image name component. Unlike a word, a image name
        component can begin with a number.

    .. method:: string()

        Matches a Ren'Py string.

    .. method:: integer()

        Matches an integer, returns a string containing the integer.

    .. method:: float()

        Matches a floating point number, returns a string containing the
        floating point number.

    .. method:: label_name(declare=False)

        Matches a label name, either absolute or relative. If `declare`
        is true, then the global label name is set. (Note that this does not
        actually declare the label - the statement is required to do that
        by returning it from the `label` function.)

    .. method:: simple_expression()

        Matches a simple Python expression, returns it as a string.
        This is often used when you expect a variable name.
        It is not recommended to change the result. The correct action is
        to evaluate the result in the future.

    .. method:: delimited_python(delim)

        Matches a Python expression that ends in a `delim`, for example ':'.
        This is often used when you expect a condition until the delimiter.
        It is not recommended to change the result. The correct action is
        to evaluate the result in the future. This raises an error if
        end of line is reached before the delimiter.

    .. method:: arguments()

        This must be called before the parentheses with the arguments list,
        if they are not specified returns None, otherwise
        returns an object representing the arguments to a function
        call. This object has an ``evaluate`` method on it that
        takes an optional `scope` dictionary, and returns a tuple
        in which the first component is a tuple of positional arguments,
        and the second component is a dictionary of keyword arguments.

    .. method:: rest()

        Skips whitespace, then returns the rest of the line.

    .. method:: checkpoint()

        Returns an opaque object representing the current state of the lexer.

    .. method:: revert(o)

        When `o` is the object returned from checkpoint(), reverts the state
        of the lexer to what it was when checkpoint() was called. (This is
        used for backtracking.)

    .. method:: subblock_lexer()

        Return a Lexer for the block associated with the current line.

    .. method:: advance()

        In a subblock lexer, advances to the next line. This must be called
        before the first line, so the first line can be parsed. Returns True
        if we've successfully advanced to a line in the block, or False
        if we have advanced beyond all lines in the block.


Lint Utility Functions
----------------------

These functions are useful in writing lint functions.

.. include:: inc/lint

Example
-------

This creates a new statement ``line`` that allows lines of text to be specified
without quotes. ::

    python early:

        def parse_smartline(lex):
            who = lex.simple_expression()
            what = lex.rest()
            return (who, what)

        def execute_smartline(o):
            who, what = o
            renpy.say(eval(who), what)

        def lint_smartline(o):
            who, what = o
            try:
                eval(who)
            except:
                renpy.error("Character not defined: %s" % who)

            tte = renpy.check_text_tags(what)
            if tte:
                renpy.error(tte)

        renpy.register_statement("line", parse=parse_smartline, execute=execute_smartline, lint=lint_smartline)

This can be used by writing::

    line e "These quotes will show up," Eileen said, "and don't need to be backslashed."
