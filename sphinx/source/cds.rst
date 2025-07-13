Creator-Defined Statements
==========================

Creator-Defined Statements (CDS) allow you to add your own statements to
Ren'Py's scripting language. This makes it possible to add functionality that
is not supported by the current syntax.

CDS can be more flexible than the direct Python code equivalent.

For example, picking a line of dialogue at random::

    label introduction:
        python:
            greetings = ['Hello.', 'Welcome.', 'Can I help you?']
            greeting = renpy.random.choice(greetings)

        "[greeting]"


Ren'Py's parser does not know ahead of time what happens in the python block or how it should be executed.
It does not do anything with this code until execution and triggers an error if an exception occurs.

Using a CDS allows you to:

- Check the correctness of the parsed syntax (For example, check that the items in the list sent to renpy.random.choice have valid text)

- Ignore incorrect data at execution (For non-critical functions, it is often better to skip the execution than to throw an exception)

- Predict Displayables (If the function uses them)

- Give you addition information during :ref:`lint` (If at runtime an error was ignored you can have a report here).

For example, the above behaviour, but written as a CDS::

    python early:
        def parse_random(lexer):
            subblock_lexer = lexer.subblock_lexer()
            choices = []

            while subblock_lexer.advance():
                with subblock_lexer.catch_error():
                    statement = subblock_lexer.renpy_statement()
                    choices.append(statement)

            return choices


        def next_random(choices):
            return renpy.random.choice(choices)


        def lint_random(parsed_object):
            for i in parsed_object:
                    check = renpy.check_text_tags(i.block[0].what)
                    if check:
                        renpy.error(check)


        renpy.register_statement(
            name="random",
            block=True,
            parse=parse_random,
            next=next_random,
            lint=lint_random,
        )


``random`` is now available as a statement::

    label introduction:
        random:
            "Hello."
            "Welcome."
            "Can I help you?"


Using a CDS does not guarantee that the execution will be successful,
but the better you code your statement, the better Ren'Py can "understand" what
you expect from it.


Usage
-----

Creator-Defined Statements (CDS) must conform to the following rules:

- They must be defined in a ``python early`` block.

- They cannot be used in the same file in which they are defined.

- The file containing the CDS must be loaded earlier than any file that uses it.
  (Since Ren'Py loads files in the Unicode sort order of their path, it generally makes sense to
  prefix the name of any file containing a CDS with 01 or some other small number. See :ref:`early-phase` for
  more information about the order in which Ren'Py loads files, with special details about the  game/libs/ and
  game/mods/ directories.)

Creator-Defined Statements are registered using the :func:`renpy.register_statement`
function. This functions takes other functions that perform operations on the content of the CDS.

For example, a new statement named ``line`` that allows lines of text to be specified
without quotes.

::

    line e "These quotes will show up," Eileen said, "and don't need to be backslashed."

The parse function will be sent the lexed content for parsing.
The execute function should run an operation on the parsed content.
The lint function should report any errors in the parsed content.

::

    python early:
        def parse_smartline(lexer):
            who = lexer.simple_expression()
            what = lexer.rest()
            return (who, what)

        def execute_smartline(parsed_object):
            who, what = parsed_object
            renpy.say(eval(who), what)

        def lint_smartline(parsed_object):
            who, what = parsed_object
            try:
                eval(who)
            except Exception:
                renpy.error("Character not defined: {}".format(who))

            tte = renpy.check_text_tags(what)
            if tte:
                renpy.error(tte)

        renpy.register_statement(
            "line",
            parse=parse_smartline,
            execute=execute_smartline,
            lint=lint_smartline,
        )


API Reference
-------------

.. include:: inc/statement_register


Lexer object
~~~~~~~~~~~~

A custom statement's parse function takes an instance of a Lexer object.

.. class:: Lexer

    .. method:: error(msg)

        :param str msg: Message to add to the list of detected parsing errors.

        Add `msg` (with the current position) to the list of detected
        parsing errors. This interrupts the parsing of the current statement,
        but does not prevent further parsing.

    .. method:: require(thing, name=None)

        Try to parse `thing` and report an error if it cannot be done.

        If `thing` is a string, try to parse it using :func:`match`.

        Otherwise, thing must be another method on this lexer object which is
        called without arguments.

        If `name` is not specified, the name of the method will be used in the
        message (or `thing` if it's a string), otherwise `name` will be used.

    .. method:: eol()

        :return: True if the lexer is at the end of the line, else False.
        :rtype: bool

    .. method:: expect_eol()

        If not at the end of the line, raise an error.

    .. method:: expect_noblock(stmt)

        Called to indicate this statement does not expect a block.
        If a block is found, raise an error. `stmt` should be a string,
        it will be added to the message with an error.

    .. method:: expect_block(stmt)

        Called to indicate that the statement requires that a non-empty
        block is present. `stmt` should be a string, it will be added
        to the message with an error.

    .. method:: has_block()

        :return: True if the current line has a non-empty block, else False.
        :rtype: bool

    .. method:: match(re)

        Match an arbitrary regexp string.

        All of the statements in the lexer that match things are implemented
        in terms of this function. They first skip whitespace, then attempt
        to match against the line. If the match succeeds, the matched text
        is returned. Otherwise, None is returned, and the state of the lexer
        is unchanged.

    .. method:: keyword(s)

        Match `s` as a keyword.

    .. method:: name()

        Match a name. This does not match built-in keywords.

    .. method:: word()

        :return: The text of the matched word.
        :rtype: str

        Match any word, including keywords.

    .. method:: image_name_component()

        Match an image name component. Unlike a word, an image name
        component can begin with a number.

    .. method:: string()

        Match a Ren'Py string.

    .. method:: integer()

        :return: String containing the found integer.
        :rtype: str

        Match an integer.

    .. method:: float()

        :return: String containing the found floating point number.
        :rtype: str

        Match a floating point number.

    .. method:: label_name(declare=False)

        Match a label name, either absolute or relative. If `declare`
        is true, then the global label name is set. (Note that this does not
        actually declare the label - the statement is required to do that
        by returning it from the `label` function.)

    .. method:: simple_expression()

        Match a simple Python expression, returns it as a string.
        This is often used when you expect a variable name.
        It is not recommended to change the result. The correct action is
        to evaluate the result in the future.

    .. method:: delimited_python(delim)

        Match a Python expression that ends in a `delim`, for example ':'.
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

        Skip whitespace, then return the rest of the line.

    .. method:: checkpoint()

        Return an opaque object representing the current state of the lexer.

    .. method:: revert(o)

        When `o` is the object returned from checkpoint(), reverts the state
        of the lexer to what it was when checkpoint() was called. (This is
        used for backtracking.)

    .. method:: subblock_lexer()

        :return: A Lexer for the block associated with the current line.

    .. method:: advance()

        In a subblock lexer, advance to the next line. This must be called
        before the first line, so the first line can be parsed. Return True
        if we've successfully advanced to a line in the block, or False
        if we have advanced beyond all lines in the block.

    .. method:: renpy_statement()

        When called, this parses the current line as a Ren'Py script statement,
        generating an error if this is not possible. This method returns
        an opaque object that can be returned from the `next` function passed to
        :func:`renpy.register_statement`, or passed
        to :func:`renpy.jump` or :func:`renpy.call`. This object should
        not be stored except as part of the parse result of the statement.

        When the statement returned from this completes, control is
        transferred to the statement after the creator-defined statement.
        (Which might be the statement created using post_execute).

    .. method:: renpy_block(empty=False)

        Parse all of the remaining lines in the current block
        as Ren'Py script, and return a SubParse corresponding to the
        first statement in the block. The block is chained together such
        that all statements in the block are run, and then control is
        transferred to the statement after this creator-defined statement.

        Note that this parses the current block. In the more likely
        case that you'd like to parse the subblock of the current
        statement, the correct way to do that is::

            def mystatement_parse(l):

                l.require(':')
                l.expect_eol()
                l.expect_block("mystatement")

                child = l.subblock_lexer().renpy_block()

                return { "child" : child }

        `empty`
            If True, allows an empty block to be parsed. (An empty block
            is equivalent to a block with a single ``pass`` statement.)

            If False, an empty block triggers an error.

    .. method:: catch_error()

        This is a context decorator, used in conjunction with the with
        statement, that catches and reports lexer errors inside its
        context block, then continues after the block.

        Here's an example of how it can be used to report multiple errors
        in a single subblock. ::

            def mystatement_parse(l):

                l.require(':')
                l.expect_eol()
                l.expect_block("mystatement")

                strings = [ ]
                ll = l.subblock_lexer()

                while ll.advance():
                    with ll.catch_error():
                        strings.append(ll.require(ll.string))
                        ll.expect_noblock("string inside mystatement")
                        ll.expect_eol()

                return { "strings" : strings }

A function allows you to lex arbitrary strings:

.. include:: inc/lexer


Lint Utility Functions
~~~~~~~~~~~~~~~~~~~~~~

These functions are useful when writing lint functions.

.. include:: inc/lint
