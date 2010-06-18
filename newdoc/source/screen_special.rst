====================
Special Screen Names
====================

There are two kinds of special screen names in Ren'Py. The first are
screens that will be automatically displayed when Ren'Py script
language commands (or their programmatic equivalents) are run. The
other type are menu screens. These have conventional names for
conventional functionality, but screens can be omitted or changed as
is deemed necessary.

On this page, we'll give example screens. It's important to realize
that, while some screens must have minimal functionality, the screen
system makes it possible to add additional functionality to
screens. For example, while the standard say screen only displays
text, the screen systen makes it easy to add features like skipping,
auto-forward mode, or muting.

Some special screens take parameters. These parameters can be accessed
as variables in the screen's scope.

Some of the screens also have special ids associated with them. A
special id should be assigned to a displayable of a given type. It can
cause properties to be assigned to that displayable, and can make that
displayable accessible to calling code.

In-Game Screens
===============

These screens are automatically displayed when certain Ren'Py
statements execute.

Say
---

The ``say`` screen is called by the say statement, when displaying
ADV-mode dialogue. It is displayed with the following parameters:

`who`
    The text of the name of the speaking character.
`what`
    The dialogue being said by the speaking character.

It's expected declare displayables with the following ids:

"who"
    A text displayable, displaying the name of the speaking
    character. The character object can be given arguments that style
    this displayable.

"what"
    A text displayable, displaying the dialogue being said by the
    speaking character. The character object can be given arguments that style
    this displayable. **A displayable with this id must be defined**,
    as Ren'Py uses it to calculate auto-forward-mode time,
    click-to-continue, and other things.

"window"
    A window or frame. This conventionally contains the who and what
    text. The character object can be given arguments that style
    this displayable.

::

   screen say:
        # TODO
    

Choice
------

The ``choice`` screen is used to display the in-game choices created
with the menu statement. It is given the following parameter:

`items`
    This is a list of (`label`, `action`) tuples, corresponding to
    menu choices. `Label` is text, and the screen is expected to
    display that text in a way that causes `action` to be invoked when
    it is selected.

::

    screen choice:
        # TODO

Input
-----

The ``input`` screen is used to display :func:`renpy.input`. It is not
given any parameters, but is given one special id:

"input"
    An input displayable, which must exist. This is given all the
    parameters supplied to renpy.input, so it must exist.

::

    screen input:
         # TODO


NVL
---

The ``nvl`` screen is used to display NVL-mode dialogue. It is given
the following parameter:

`dialogue`
    This is a list of ( `who`, `what`, `who_id`, `what_id`,
    `window_id`) tuples, each of which corresponds to a line of
    dialogue on the screen. `Who` and `what` are strings containing
    the speaking character and the line of dialogue, respectively. The
    ids should be assigned to the who and what text displayables, and
    a window containing each unit of dialogue.

::

    screen nvl:
        # TODO

NVL_Choice
----------

The ``nvl_choice`` screen is used to display an NVL-mode menu. Its two
parameters are a combination of those of the ``nvl`` and ``choice``
screens. 


`dialogue`
    This is a list of ( `who`, `what`, `who_id`, `what_id`,
    `window_id`) tuples, each of which corresponds to a line of
    dialogue on the screen. `Who` and `what` are strings containing
    the speaking character and the line of dialogue, respectively. The
    ids should be assigned to the who and what text displayables, and
    a window containing each unit of dialogue.

`items`
    This is a list of (`label`, `action`) tuples, corresponding to
    menu choices. `Label` is text, and the screen is expected to
    display that text in a way that causes `action` to be invoked when
    it is selected.


Menu Screens
============

These are the menu screens. The ``main_menu`` and ``yesno_prompt`` are
invoked implictly.  When the user invokes the game menu, the screen
named in :data:`_game_menu_screen` will be displayed. (This defaults
to ``save``.)

Remember, menu screens can be combined and modified fairly freely.

Main Menu
---------

The ``main_menu`` screen is the first screen shown when the game
begins.

::

    screen main_menu:
        # TODO

Save
----

The ``save`` screen is used to select a file in which to save the
game.

::

    screen save:
        # TODO

Load
----

The ``load`` screen is used to select a file from which to load the
game.

::

    screen load:
        # TODO
        
Preferences
-----------

The ``preferences`` screen is used to select options that control the
display of the game.

::

    screen preferences:
        # TODO

Yesno_Prompt
------------

The ``yesno_prompt`` message is used to ask yes/no choices of the
user. It takes the following parameters:

`message`
    The message to display to the user. This is one of:

    * layout.ARE_YOU_SURE - "Are you sure?" This should be
      the default if the message is unknown.    
    * layout.DELETE_SAVE - "Are you sure you want to delete this save?"
    * layout.OVERWRITE_SAVE - "Are you sure you want to overwrite your save?"
    * layout.LOADING - "Loading will lose unsaved progress.\nAre you sure you want to do this?"
    * layout.QUIT - "Are you sure you want to quit?"
    * layout.MAIN_MENU - "Are you sure you want to return to the main\nmenu? This will lose unsaved progress."

    The values of the variables are strings, which means they can be
    displayed using a text displayable.

`yes_action`
    The action to run when the user picks "Yes".

`no_action`
    The action to run when the user picks "No".

::

    screen yesno_prompt:
        # TODO
