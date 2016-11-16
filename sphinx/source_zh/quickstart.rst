
==========

Welcome to the Ren'Py quickstart manual. The purpose of this manual is
to demonstrate how you can make a Ren'Py game from scratch, in a few
easy steps. We'll do this by showing how to make a simple game, *The
Question*, from scratch. This manual contains a number of examples,
which are included as part of the demo game.

The Ren'Py Launcher
-------------------


Before you begin making a game, you should first take some time to
learn how the Ren'Py launcher works. The launcher lets you create,
manage, edit, and run Ren'Py projects.

**Getting Started.** To get started you'll want to
`download Ren'Py <https://www.renpy.org/latest.html>`_.

Once you've downloaded Ren'Py, you'll want to extract it. This can
generally be done by right-clicking on the package file, and picking
"Extract" if that's an option, or "Open" if it's not. Follow the
prompts, and you'll have a working copy of Ren'Py.

.. note::

    Please be sure you've extracted Ren'Py to its own directory or
    folder on disk. If you try to run it from inside a ZIP file, it
    won't work properly.

Once you've extracted Ren'Py, you'll need to run it.

* On Windows, run the ``renpy`` or ``renpy.exe`` program.
* On Mac OS X, run the ``renpy`` application.
* On Linux, run the ``renpy.sh`` script.


After running this, the Ren'Py launcher should run.

The Ren'Py launcher has been translated to multiple languages. To
change the language, choose "preferences" and then select the language.

.. image:: launcher.png
   :align: right

**Choosing and Launching a Project.** You should first see what the
completed *The Question* game looks like. To do this, start the Ren'Py
launcher, and choose "The Question" from the first screen. Choose
"Launch Project" to start *The Question*.

You can get back to the Ren'Py demo by doing the same thing, but
choosing "Tutorial" instead of "The Question".

**Creating a new Project.**
Create a new project by choosing "Create New Project" from the
launcher. The launcher will then ask you for a project name. Since
"The Question" is already taken, you should enter something different,
like "My Question". The launcher will then ask you to choose a color
theme for the project. It doesn't matter what you pick at this point,
just choose something that appeals to you. You'll be returned to the
top menu of the launcher with your new game chosen.

A Simple Game
-------------

::

    label start:
        "I'll ask her..."

        "Me" "Um... will you..."
        "Me" "Will you be my artist for a visual novel?"

        "Silence."
        "She is shocked, and then..."

        "Sylvie" "Sure, but what is a \"visual novel?\""

This is perhaps one of the simplest Ren'Py games. It doesn't include
any pictures or anything like that, but it does show a conversation
between the two characters.

To try this out, go into the launcher, select the "My Question
Project", and choose "script.rpy" from under Edit File. Ren'Py may
ask you to select a text editor, after which it will download the
editor you select. When it finishes, script.rpy will open in an
editor.  Erase everything in script.rpy, as we're starting from
scratch, so you don't need what's there. Copy the example above into
script.rpy, and save it.

You're now ready to run this example. Go back to the launcher, and
choose "Launch Project". Ren'Py will start up. Notice how, without any
extra work, Ren'Py has given you menus that let you load and save the
game, and change various preferences. When ready, click "Launch Project",
and play through this example game.

This example shows some of the commonly-used Ren'Py statements.

The first line is a label statement. The label statement is used to
give a name to a place in the program. In this case, we create a label
named ``start``. The start label is special, as it's where Ren'Py
scripts begin running when the user clicks "Start Game" on the main
menu.

The other lines are say statements. There are two forms of the say
statement. The first is a string (beginning with a double-quote,
containing characters, and ending with a double-quote) on a line by
itself, which is used for narration, and the thoughts of the main
character. The second form consists of two strings. It's used for
dialogue, with the first string being a character name and the second
being what that character is saying.

Note that all the say statements are indented by four spaces. This is
because they are a block underneath the label statement. In Ren'Py,
blocks must be indented relative to the prior statement, and all of
the statements in a block must be indented by the same amount.

When strings contain double-quote characters, those characters need to
be preceded by a backslash. This is done in the last line of our
example.

While this simple game isn't much to look at, it's an example of how
easy it is to get something working in Ren'Py. We'll add the pictures
in a little bit, but first, let's see how to declare characters.

Init
----

The init statement is used to execute blocks of Ren'Py statements before the
script executes. Init blocks are used to define images and characters, to set
up unchanging game data structures, and to customize Ren'Py. Code inside init
blocks should not interact with the user or change any of the layers, and so
should not contain say, menu, scene, show, or hide statements, as well as calls
to any function that can do these things.

An init statement is introduced with the keyword init, followed by an optional
priority number, and a mandatory colon. If the priority is not given, it
defaults to 0. Priority numbers should be in the range -999 to 999. Numbers
outside of this range are reserved for Ren'Py code.

The priority number is used to determine when the code inside the init block
executes. Init blocks are executed in priority order from low to high. Within a
file, init blocks with the same priority are run in order from the top of the
file to the bottom. The order of evaluation of priority blocks with the same
priority between files is undefined.

The init blocks are all run once, during a special init phase. When control
reaches the end of an init block during normal execution, execution of that
block ends. If an init statement is encountered during normal execution, the
init block is not run. Instead, control passes to the next statement.

Characters
----------

One problem with the first example is that it requires you to
repeatedly type the name of a character each time they speak. In a
dialogue-heavy game, this might be a lot of typing. Also, both
character names are displayed in the same way, in fairly boring white
text. To fix this, Ren'Py lets you define characters in advance. This
lets you associate a short name with a character, and to change the
color of the character's name.

::

    define s = Character('Sylvie', color="#c8ffc8")
    define m = Character('Me', color="#c8c8ff")

    label start:
        "I'll ask her..."

        m "Um... will you..."
        m "Will you be my artist for a visual novel?"

        "Silence."
        "She is shocked, and then..."

        s "Sure, but what is a \"visual novel?\""


The first and and second lines define characters. The first line
defines a character with the short name of "s", the long name
"Sylvie", with a name that is shown in a greenish color. (The colors
are red-green-blue hex triples, as used in web pages.)

The second line creates a character with a short name "m", a long name
"Me", with the name shown in a reddish color. Other characters can be
defined by copying one of the character lines, and changing the short
name, long name, and color.

We've also changed the say statements to use character objects instead
of a character name string. This tells Ren'Py to use the characters we
defined in the init block.

Images
------

A visual novel isn't much of a visual novel without pictures. Let's
add some pictures to our game.

::

    image bg meadow = "meadow.jpg"
    image bg uni = "uni.jpg"

    image sylvie smile = "sylvie_smile.png"
    image sylvie surprised = "sylvie_surprised.png"

    define s = Character('Sylvie', color="#c8ffc8")
    define m = Character('Me', color="#c8c8ff")

    label start:
        scene bg meadow
        show sylvie smile

        "I'll ask her..."

        m "Um... will you..."
        m "Will you be my artist for a visual novel?"

        show sylvie surprised

        "Silence."
        "She is shocked, and then..."

        show sylvie smile

        s "Sure, but what is a \"visual novel?\""


The first new thing we needed to do was to declare the images, using
image statements on lines 2, 3, 5, and 6, inside the init block. These
image statements give an image name, and the filename the image is
found in.

For example, line 5 declares an image named "sylvie smile", found in
the filename "sylvie_smile.png", with the tag "sylvie".

We have a scene statement on line 12. This statement clears out the
screen, and shows the "bg meadow" image. The next line is a show
statement, which shows the "sylvie smile" image on the screen.

The first part of an image name is the image tag. If an image is being
shown, and another image with the same tag is on the screen, then the
image that's on the screen is replaced with the one being shown. This
happens on line 19, the second show statement. Before line 19 is run,
the image "sylvie smile" is on the screen. When line 19 is run, that
image is replaces with "sylvie surprised", since they share the
"sylvie" tag.

For Ren'Py to find the image files, they need to be placed in the game
directory of the current project. The game directory can be found at
"`Project-Name`/game/", or by clicking the "Game Directory" button in
the launcher. You'll probably want to copy the image files from the
"the_question/game/" directory into the "my_question/game/" directory,
so you can run this example.

Ren'Py does not make any distinction between character and background
art, as they're both treated as images. In general, character art
needs to be transparent, which means it should be a PNG or WEBP
file. Background art can be JPEG, PNG, or WEBP files. By convention,
background images start with the "bg" tag.

**Hide Statement.**
Ren'Py also supports a hide statement, which hides the given image.

::

    label leaving:

        s "I'll get right on it!"

        hide sylvie

        "..."

        m "That wasn't what I meant!"

It's actually pretty rare that you'll need to use hide. Show can be
used when a character is changing emotions, while scene is used when
everyone leaves. You only need to use hide when a character leaves and
the scene stays the same.

Transitions
-----------

Simply having pictures pop in and out is boring, so Ren'Py implements
transitions that can make changes to the screen more
interesting. Transitions change the screen from what it looked like at
the end of the last interaction (dialogue, menu, or transition), to
what it looks like after any scene, show, and hide statements.

::

    label start:
        scene bg uni
        show sylvie smile

        s "Oh, hi, do we walk home together?"
        m "Yes..."
        "I said and my voice was already shaking."

        scene bg meadow
        with fade

        "We reached the meadows just outside our hometown."
        "Autumn was so beautiful here."
        "When we were children, we often played here."
        m "Hey... ummm..."

        show sylvie smile
        with dissolve

        "She turned to me and smiled."
        "I'll ask her..."
        m "Ummm... will you..."
        m "Will you be my artist for a visual novel?"

The with statement takes the name of a transition to use. The most
common one is ``dissolve`` which dissolves from one screen to the
next. Another useful transition is ``fade`` which fades the
screen to black, and then fades in the new screen.

When a transition is placed after multiple scene, show, or hide
statements, it applies to them all at once. If you were to write::

    ###
        scene bg meadow
        show sylvie smile
        with dissolve

Both the "bg meadow" and "sylvie smiles" would be dissolved in at the
same time. To dissolve them in one at a time, you need to write two
with statements::

    ###
        scene bg meadow
        with dissolve
        show sylvie smile
        with dissolve

This first dissolves in the meadow, and then dissolves in sylvie. If
you wanted to instantly show the meadow, and then show sylvie, you
could write::

    ###
        scene bg meadow
        with None
        show sylvie smile
        with dissolve

Here, None is used to indicate a special transition that updates
Ren'Py's idea of what the prior screen was, without actually showing
anything to the user.

Positions
---------

By default, images are shown centered horizontally, and with their
bottom edge touching the bottom of the screen. This is usually okay
for backgrounds and single characters, but when showing more than one
character on the screen it probably makes sense to do it at another
position. It also might make sense to reposition a character for story
purposes.

::

   ###
        show sylvie smile at right

To do this repositioning, add an at-clause to a show statement. The at
clause takes a position, and shows the image at that position. Ren'Py
includes several pre-defined positions: ``left`` for the left side of
the screen, ``right`` for the right side, ``center`` for centered
horizontally (the default), and ``truecenter`` for centered
horizontally and vertically.

A user can define their own positions, and event complicated moves,
but that's outside of the scope of this quickstart.

Music and Sound
---------------

Most games play music in the background. Music is played with the play music
statement. It can take either a string containing a filename, or a list of filenames
to be played. When the list is given, the item of it is played in order. ::

    ###
        play music "illurock.ogg"
        play music ["1.ogg", "2.ogg"]


When changing music, one can supply a fadeout and a fadein clause, which
are used to fade out the old music and fade in the new music. ::

    ###
        play music "illurock.ogg" fadeout 1.0 fadein 1.0

And if you supply a loop clause, it loops. if you supply a noloop clause, it
doesn't loop. In Ren'Py, music files automatically loop until they are stopped
by the user. ::

    ###
        play music "illurock.ogg" loop
        play music "illurock.ogg" noloop

Music can be stopped with the stop music statement, which can also
optionally take a fadeout clause. ::

    ###
        stop music

Sound effects can be played with the play sound statement. It defaults to not looping. ::

    ###
        play sound "effect.ogg"

The play sound statement can have same clauses with the play music statement.

Ren'Py support many formats for sound and music, but OGG Vorbis is
preferred. Like image files, sound and music files must be placed in
the game directory.

Pause Statement
---------------

The pause statement causes Ren'Py to pause until the mouse is clicked. If the
optional expression is given, it will be evaluated to a number, and the pause
will automatically terminate once that number of seconds has elapsed.

Ending the Game
---------------

You can end the game by running the return statement, without having
called anything. Before doing this, it's best to put something in the
game that indicates that the game is ending, and perhaps giving the
user an ending number or ending name. ::

    ###
        ".:. Good Ending."

        return

That's all you need to make a kinetic novel, a game without any
choices in it. Now, we'll look at what it takes to make a game that
presents menus to the user.

Menus, Labels, and Jumps
-------------------------

The menu statement lets you present a choice to the user::

    ###
        s "Sure, but what's a \"visual novel?\""

    menu:
        "It's a story with pictures.":
             jump vn

        "It's a hentai game.":
             jump hentai

    label vn:
        m "It's a story with pictures and music."
        jump marry

    label hentai:
        m "Why it's a game with lots of sex."
        jump marry

    label marry:
        scene black
        with dissolve

        "--- years later ---"

This example shows how menus are used with Ren'Py. The menu statement
introduces an in-game-menu. The menu statement takes a block of lines,
each consisting of a string followed by a colon. These are the menu
choices which are presented to the user. Each menu choice should be
followed by a block of one or more Ren'Py statements. When a choice is
chosen, the statements following it are run.

In our example, each menu choice runs a jump statement. The jump
statement transfers control to a label defined using the label
statement. The code following that label is run.

In our example above, after Sylvie asks her question, the user is
presented with a menu containing two choices. If the user picks "It's
a story with pictures.", the first jump statement is run, and control
is transferred to the ``vn`` label. This will cause the pov character to
say "It's a story with pictures and music.", after which control is
transferred to the ``marry`` label.

Labels may be defined in any file that is in the game directory, and
ends with .rpy. The filename doesn't matter to Ren'Py, only the labels
contained within it. A label may only appear in a single file.

Python and If Statements
------------------------

While simple (and even fairly complex) games can be made using only
using menus and jump statements, after a point it becomes necessary to
store the user's choices in variables, and access them again
later. This is what Ren'Py's python support is for.

Python support can be accessed in two ways. A line beginning with a
dollar-sign is a single-line python statement, while the keyword
"python:" is used to introduce a block of python statements.

Python makes it easy to store flags in response to user input. Just
initialize the flag at the start of the game::

    label start:
        $ bl_game = False

You can then change the flag in code that is chosen by menus::

    label hentai:

        $ bl_game = True

        m "Why it's a game with lots of sex."
        s "You mean, like a boy's love game?"
        s "I've always wanted to make one of those."
        s "I'll get right on it!"

        jump marry

And check it later::

        "And so, we became a visual novel creating team."
        "We made games and had a lot of fun making them."

        if bl_game:
            "Well, apart from that boy's love game she insisted on making."

        "And one day..."

Of course, python variables need not be simple True/False values. They
can be arbitrary python values. They can be used to store the player's
name, to store a points score, or for any other purpose. Since Ren'Py
includes the ability to use the full Python programming language, many
things are possible.

Releasing Your Game
-------------------

Once you've made a game, there are a number of things you should do
before releasing it:

**Check for a new version of Ren'Py.**
   New versions of Ren'Py are released on a regular basis, to fix bugs
   and add new features. Before releasing, click update in the launcher
   to update Ren'Py to the latest version. You can also download new
   versions and view a list of changes at
   `http://www.renpy.org/latest.html <http://www.renpy.org/latest.html>`_.

**Check the Script.**
   From the front page of the launcher, choose "Check Script
   (Lint)". This will check your games for errors that may affect some
   users. These errors can affect users on the Mac and Linux
   platforms, so it's important to fix them all, even if you don't see
   them on your computer.

**Build Distributions.**
   From the front page of the launcher, choose "Build Distributions". Based
   on the information contained in options.rpy, the launcher will build one
   or more archive files containing your game.

**Test.**
   Lint is not a substitute for thorough testing. It's your
   responsibility to check your game before it is released. Consider asking
   friends to help beta-test your game, as often a tester can find problems
   you can't.

**Release.**
   You should post the generated files (for Windows, Mac, and Linux) up
   on the web somewhere, and tell people where to download them
   from. Congratulations, you've released a game!

   Please also add your released game to our `games database <http://games.renpy.org>`_,
   so we can keep track of the Ren'Py games being made.

Script of The Question
-----------------------

You can view the full script of ''The Question'' :ref:`here <thequestion>`.

Where do we go from here?
-------------------------

This Quickstart has barely scratched the surface of what Ren'Py is
capable of. For simplicity's sake, we've omitted many features Ren'Py
supports. To get a feel for what Ren'Py is capable of, we suggest
playing through the Tutorial, and having Eileen demonstrate these features
to you.

You may also want to read the rest of this (complex) manual, as it's
the definitive guide to Ren'Py.

On the Ren'Py website, there's the a `FAQ <http://www.renpy.org/wiki/renpy/doc/FAQ>`_ giving answers to
common questions, and a `Cookbook <http://www.renpy.org/wiki/renpy/doc/cookbook/Cookbook>`_ giving
useful code snippets. If you have questions, we suggest asking them at
the `Lemma Soft Forums <http://lemmasoft.renai.us/forums/>`_, the
official forum of Ren'Py. This is the central hub of the Ren'Py
community, where we welcome new users and the questions they bring.

Thank you for choosing the Ren'Py visual novel engine. We look forward
to seeing what you create with it!
