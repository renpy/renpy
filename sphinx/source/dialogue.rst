Dialogue and Narration
======================

Text is fundamental to visual novels, and generally quite important to
storytelling-based games. This text may consist of dialogue labeled
with the character that is saying it, and narration, which does not
have a speaker. (For convenience, we will lump both dialogue and
narration together as dialogue, except where the differences are
important.) It's also important that the user be able to customize the
look of dialogue to suit their game.

In Ren'Py, most dialogue is written using say statements. The look of
dialogue may be customized on a per-character basis by using Character
objects.

.. _say-statement:

Say Statement
-------------

The say statement is used for dialogue and narration. Since it's
almost always the most frequently used statement in Ren'Py scripts,
the say statement has a syntax that minimizes the overhead in
writing it. Some example say statements are::

    ###
        "This is narration."

        "Eileen" "This is dialogue, with an explicit character name."

        e "This is dialogue, using a character object instead."

The first form of the say statement consists of a string by
itself. This form is used for narration, with the narration being the
contents of the string.

The second form consists of two strings. The first string is the name
of the character who is speaking, and the second is the dialogue being
spoken.

The final form is consists of a simple expression followed by a
string. The simple expression should evaluate to either a string
giving a character name, or a Character object. In the latter case,
the character object is used to control how the dialogue is shown.

Although the precise details of what a say statement does is
controlled by the character object used, the usual effect of a say
statement is to display dialogue on the screen until the user clicks
to dismiss it, then to remove that dialogue on the screen.

Certain characters have special meaning to Ren'Py, and so can't be
used in dialogue strings. The ``{`` character begins a text tag, and
the ``[`` character begins a substitution. To use them in dialogue,
double them. It may also be necessary to precede a quote with a
backslash to prevent it from closing the string. For example::

   ###
       "I walked past a sign saying, \"Let's give it 100%!\""


Defining Character Objects
--------------------------

By creating a Character object and using it in a say statement, you
can customize the look (and to some extent, the behavior) of
dialogue. Characters are created by using the define statement to
assign a Character to a variable. For example::

    define e = Character("Eileen",
                         who_color="#c8ffc8")


Once this is done, the character can be used in a say statement::

    ###
        e "Hello, world."

Character is a python function, that takes a large number of keyword
arguments. These keyword arguments control the behavior of the
character.

.. include:: inc/character

Say with Image Attributes
-------------------------

When a character is defined with an associated image tag, say
statement involving that character may have image attributes
placed between the character name and the second string.

In this form, if an image with the given tag is showing, Ren'Py will
issue a show command involving the character tag and the
attributes. If the image is not shown, Ren'Py will store the
attributes for use by side images, but will not show an image.


For example, the code::

    define e = Character("Eileen", image="eileen")

    label start:

        show eileen mad
        e "I'm a little upset at you."

        e happy "But it's just a passing thing."
    
is equivalent to::

    define e = Character("Eileen")

    label start:

        show eileen mad
        e "I'm a little upset at you."

        show eileen happy        
        e "But it's just a passing thing."

To cause a transition to occur whenever the images are changed in this way, set
:var:`config.say_attribute_transition` to a transition.

Example Characters
------------------

Here are a few example characters::

    # A character that has its dialogue enclosed in parenthesis.
    define e = Character("Eileen", what_prefix='"', what_suffix='"')

    # A character that pulls its name from a variable.
    define p = Character("player_name", dynamic=True)

Special Characters
------------------

A few character names are defined by default, and are used
automatically in certain situations. Intentionally redefining these
characters can change the behavior of Ren'Py, but accidentally using
them can be a problem.

``adv``
    The default kind of character used by Character. This sets up a
    character such that one line is displayed on the screen at a
    time.

``nvl``
    A kind of Character that causes dialogue to be displayed in
    :ref:`NVL-mode`, with multiple lines of text on the screen
    at once.

``narrator``
    The character that's used to display narration, by say statements
    without a character name.

``name_only``
    A character that is used to display dialogue in which the
    character name is given as a string. This character is copied to a
    new character with the given name, and then that new character is
    used to display the dialogue.

   
