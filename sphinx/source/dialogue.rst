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

        "Bam!!" with vpunch

The first form of the say statement consists of a string by
itself. This form is used for narration, with the narration being the
contents of the string.

The second form consists of two strings. The first string is the name
of the character who is speaking, and the second is the dialogue being
spoken.

The third form consists of a simple expression followed by a
string. The simple expression should evaluate to either a string
giving a character name, or a Character object. In the latter case,
the character object is used to control how the dialogue is shown.

The final form consists of a string and a with clause which has a
transition. In this case, the string is shown and a screen is shaken
at the same time.


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

The define statement causes its expression to be evaluated, and assigned to the
supplied name. If not inside an init block, the define statement will
automatically be run with init priority 0.

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


For example::

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

``centered``
    A character that causes what it says to be displayed centered,
    in the middle of the screen, outside of any window.

``vcentered``
    A character that causes what it says to be displayed centered
    in vertically oriented text, in the middle of the screen,
    outside of any window.

``extend``
     A character that causes the last character to speak to say a line
     of dialogue consisting of the last line of dialogue spoken, "{fast}",
     and the dialogue given to extend. This can be used to have the screen
     change over the course of dialogue.

     Extend is aware of NVL-mode, and treats it correctly.

For example::

    # Show the first line of dialogue, wait for a click, change expression, and show
    # the rest.

    show eileen concerned
    e "Sometimes, I feel sad."
    show eileen happy
    extend " But I usually quickly get over it!"

    # Similar, but automatically changes the expression when the first line is finished
    # showing. This only makes sense when the user doesn't have text speed set all the
    # way up.

    show eileen concerned
    e "Sometimes, I feel sad.{nw}"
    show eileen happy
    extend " But I usually quickly get over it!"

.. _dialogue-window-management:

Dialogue Window Management
--------------------------

Ren'Py includes several statements that allow for management of the
dialogue window. As dialogue window is always shown during dialogue,
these statements control the presence or absence of the window during
non-dialogue interactions.

``window show``

The window show statement causes the window to be shown.
It takes as an argument an optional transition, which is used to show the
window. If the transition is omitted, :var:`config.window_show_transition`
is used.

``window hide``

The window hide statement causes the window to be hidden. It takes as an
argument an optional transition, which is used to hide the window. If
the transition is omitted,  :var:`config.window_hide_transition` is
used.

``window auto``

This enables automatic management of the window. The window is shown
before statements listed in :var:`config.window_auto_show` - by default,
say statements. The window is hidden before statements listed in
:var:`config.window_auto_hide` - by default, ``scene`` and ``call screen``
statements. (Only statements are considered, not statement equivalent
functions.)

The ``window auto`` statement uses :var:`config.window_show_transition`
and :var:`config.window_hide_transition` to show and hide the window,
respectively. ``window auto`` is cancelled by ``window show`` or ``window hide``.

For example::

    window show # shows the window with the default transition, if any.
    pause       # the window is shown during this pause.
    window hide # hides the window.
    pause       # the window is hidden during this pause.

    window show dissolve # shows the window with dissolve.
    pause                # the window is shown during this pause.
    window hide dissolve # hides the window with dissolve.
    pause                # the window is hidden during this pause.


    window auto

    "The window is automatically shown before this line of dialogue."
    pause                # the window is shown during this pause.

    scene bg washington  # the window is hidden before the scene change.
    with dissolve

Dialogue window management is subject to the "show empty window"
:func:`Preference`. If the preference is disabled, the statements above
have no effect.

Python Equivalents
------------------

.. note::

   This may only make sense if you've read the :ref:`python` section.

When the first parameter to a say statement is present and an expression,
the say statement is equivalent to calling that expressing with the dialogue
and an `interact` argument of True. For example::

    e "Hello, world."

is equivalent to::

    $ e("Hello, world.", interact=True)

The say statement will search the ``character`` named store before the default
store. If you want to have a character with the same name as a variable in
the default store, it can be defined using::

    define character.e = Character("Eileen")

This character can then be used alongside a variable in the default store::

    label start:

        # This is a terrible variable name.
        e = 100

        e "Our starting energy is [e] units."

Window management is performed by setting the :var:`_window` and
:var:`_window_auto` variables, and by using the following two functions:

.. include:: inc/window
