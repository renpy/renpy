Creator-Defined Statements
==========================

Creator-defined statements allow you to add your own statements to Ren'Py. This
makes it possible to add things that are not supported by the current syntax of
Ren'Py. creator-defined statements are currently limited to a single line, and may
not contain blocks.

Creator-defined statements must be defined in a python early block. What's more,
the filename containing the user-defined statement must be be loaded earlier
than any file that uses it. Since Ren'Py loads files in unicode sort order, it
generally makes sense to prefix the name of any file containing a user-defined
statement with 00. A user-defined statement cannot be used in the file in which
it is defined.

.. include:: inc/statement_register

Lint Utility Functions
----------------------

These functions are useful in writing lint functions.

.. include:: inc/lint

The creates a new statement "line" that allows lines of text to be specified
without quotes. ::

    python early:
        
        def parse_smartline(lex):
            who = lex.simple_expression()
            what = lex.rest()
            return (who, what)
        
        def execute_smartline(o):
            who, what = o
            renpy.say(who, what)

        def lint_smartline(o):
            who, what = o
            try:
                eval(who)
            except:
                renpy.error("Character not defined: %s" % who)
        
            tte = renpy.text.extras.check_text_tags(what)
            if tte:
                renpy.error(tte)
        
        renpy.statements.register("line", parse=parse_smartline, execute=execute_smartline, lint=lint_smartline)

This is used like ::

    line e "These quotes will show up," Eileen said, "and don't need to be backslashed."
