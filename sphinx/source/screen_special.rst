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
text, the screen system makes it easy to add features like skipping,
auto-forward mode, or muting.

Some special screens take parameters. These parameters can be accessed
as variables in the screen's scope.

Some of the screens also have special ids associated with them. A
special id should be assigned to a displayable of a given type. It can
cause properties to be assigned to that displayable, and can make that
displayable accessible to the part of Ren'Py that displays the screen.

In-Game Screens
===============

These screens are automatically displayed when certain Ren'Py
statements execute.

.. _say-screen:

Say
---

The ``say`` screen is called by the say statement, when displaying
ADV-mode dialogue. It is displayed with the following parameters:

`who`
    The text of the name of the speaking character.
`what`
    The dialogue being said by the speaking character.

It's expected to declare displayables with the following ids:

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

    screen say(who, what):

        window id "window":
            has vbox

            if who:
                text who id "who"

            text what id "what"


.. _choice-screen:

Choice
------

The ``choice`` screen is used to display the in-game choices created
with the menu statement. It is given the following parameter:

`items`
    This is a list of menu entry objects, representing each of the
    choices in the menu. Each of the objects has the following
    fields on it:

    .. attribute:: caption

        A string giving the caption of the menu choice.

    .. attribute:: action

        An action that should be invoked when the menu choice is
        chosen. This may be None if this is a menu caption, and
        :var:`config.narrator_menu` is False.

    .. attribute:: chosen

        This is True if this choice has been chosen at least once
        in any playthrough of the game.

    .. attribute:: args

        This is a tuple that contains any positional arguments passed
        to the menu choice.

    .. attribute:: kwargs

        This is a dictionary that contains any keyword arguments passed
        to the menu choice.

    These items, and the actions within, become invalid when the menu
    statement ends.

In addition, any arguments passed to a menu statement are passed in during
the call to the screen.

::

    screen choice(items):

        window:
            style "menu_window"

            vbox:
                style "menu"

                for i in items:

                    if i.action:

                        button:
                            action i.action
                            style "menu_choice_button"

                            text i.caption style "menu_choice"

                    else:
                        text i.caption style "menu_caption"


.. _input-screen:

Input
-----

The ``input`` screen is used to display :func:`renpy.input`. It is given one
parameter:

`prompt`
    The prompt text supplied to renpy.input.

It is expected to declare a displayable with the following id:

"input"
    An input displayable, which must exist. This is given all the
    parameters supplied to renpy.input, so it must exist.

::

    screen input(prompt):

        window:
            has vbox

            text prompt
            input id "input"


.. _nvl-screen:

NVL
---

The ``nvl`` screen is used to display NVL-mode dialogue. It is given
the following parameter:

`dialogue`
    A list of NVL Entry objects, each of which corresponds to a line
    of dialogue to be displayed. Each entry has the following
    fields:

    .. attribute:: current

        True if this is the current line of dialogue. The current
        line of dialogue must have its what text displayed with an
        id of "what".

    .. attribute:: who

        The name of the speaking character, or None of there is no
        such name.

    .. attribute:: what

        The text being spoken.

    .. attribute:: who_id, what_id, window_id

        Preferred ids for the speaker, dialogue, and window associated with an
        entry.

    .. attribute:: who_args, what_args, window_args

        Properties associated with the speaker, dialogue, and window. These
        are automatically applied if the id is set as above, but are also
        made available separately.

    .. attribute:: multiple

        If :doc:`multiple character dialogue <multiple>`, this is
        a two component tuple. The first component is the one-based number
        of the dialogue block, and the second is the total number of dialogue
        blocks in the multiple statement.

`items`
    This is the same list of items that would be supplied to the
    :ref:`choice screen <choice-screen>`. If this is empty,
    the menu should not be shown.

When `items` is not present, the NVL screen is expected to always
give a text widget an id of "what". Ren'Py uses it to calculate
auto-forward-mode time, click-to-continue, and other things. (This is
satisfied automatically if the default what_id is used.)

Ren'Py also supports an ``nvl_choice`` screen, which takes the same
parameters as ``nvl``, and is used in preference to ``nvl`` when
an in-game choice is presented to the user, if it exists.

::

    screen nvl(dialogue, items=None):

        window:
            style "nvl_window"

            has vbox:
                style "nvl_vbox"

            # Display dialogue.
            for d in dialogue:
                window:
                    id d.window_id

                    has hbox:
                        spacing 10

                    if d.who is not None:
                        text d.who id d.who_id

                    text d.what id d.what_id

            # Display a menu, if given.
            if items:

                vbox:
                    id "menu"

                    for i in items:

                        if action:

                            button:
                                style "nvl_menu_choice_button"
                                action i.action

                                text i.caption style "nvl_menu_choice"

                        else:

                            text i.caption style "nvl_dialogue"


.. _notify-screen:

Notify
------

The ``notify`` screen is used by :func:`renpy.notify` to display
notifications to the user. It's generally used in conjunction with a
transform to handle the entire task of notification. It's given a
single parameter:

`message`
    The message to display.

The default notify screen, and its associated transform, are::

    screen notify(message):
        zorder 100

        text "[message!tq]" at _notify_transform

        # This controls how long it takes between when the screen is
        # first shown, and when it begins hiding.
        timer 3.25 action Hide('notify')

    transform _notify_transform:
        # These control the position.
        xalign .02 yalign .015

        # These control the actions on show and hide.
        on show:
            alpha 0
            linear .25 alpha 1.0
        on hide:
            linear .5 alpha 0.0


.. _skip-indicator:

Skip Indicator
--------------

If present, ``skip_indicator`` screen is displayed when skipping is in progress,
and hidden when skipping finishes. It takes no parameters.

Here's a very simple skip indicator screen::


    screen skip_indicator():

        zorder 100

        text _("Skipping")


.. _ctc-screen:

CTC (Click-To-Continue)
-----------------------

If present, the ``ctc`` screen is displayed when dialogue has finished
showing, to prompt the player to click to display more text. It may be
given a single parameter and multiple keyword arguments.

`arg`
    The ctc displayable selected by the :func:`Character`. This is one of
    the `ctc`, `ctc_pause`, or `ctc_timedpause` arguments to Character,
    as appropriate. If no CTC is given to the Character, this argument is not passed at
    all.

In addition, there are several parameters that are only passed if the screen requires
them.

`ctc_kind`
    The kind of CTC to display. One of "last" (for the last CTC on a line),
    "pause", or "timedpause".

`ctc_last`
    The `ctc` argument to :func:`Character`.

`ctc_pause`
    The `ctc_pause` argument to :func:`Character`.

`ctc_timedpause`
    The `ctc_timedpause` argument to :func:`Character`.


Here's a very simple ctc screen::

    screen ctc(arg=None):

        zorder 100

        hbox:
            xalign 0.98
            yalign 0.98

            add arg

            text _("Click to Continue"):
                size 12



Out-Of-Game Menu Screens
========================

These are the menu screens. The ``main_menu`` and ``yesno_prompt`` are
invoked implicitly.  When the user invokes the game menu, the screen
named in :data:`_game_menu_screen` will be displayed. (This defaults
to ``save``.)

Remember, menu screens can be combined and modified fairly freely.

.. _main-menu-screen:

Main Menu
---------

The ``main_menu`` screen is the first screen shown when the game
begins.

::

    screen main_menu():

        # This ensures that any other menu screen is replaced.
        tag menu

        # The background of the main menu.
        window:
            style "mm_root"

        # The main menu buttons.
        frame:
            style_prefix "mm"
            xalign .98
            yalign .98

            has vbox

            textbutton _("Start Game") action Start()
            textbutton _("Load Game") action ShowMenu("load")
            textbutton _("Preferences") action ShowMenu("preferences")
            textbutton _("Help") action Help()
            textbutton _("Quit") action Quit(confirm=False)

    style mm_button:
        size_group "mm"

.. _navigation-screen:

Navigation
----------

The ``navigation`` screen isn't special to Ren'Py. But by convention,
we place the game menu navigation in a screen named ``navigation``, and
then use that screen from the save, load and preferences screens.

::

    screen navigation():

        # The background of the game menu.
        window:
            style "gm_root"

        # The various buttons.
        frame:
            style_prefix "gm_nav"
            xalign .98
            yalign .98

            has vbox

            textbutton _("Return") action Return()
            textbutton _("Preferences") action ShowMenu("preferences")
            textbutton _("Save Game") action ShowMenu("save")
            textbutton _("Load Game") action ShowMenu("load")
            textbutton _("Main Menu") action MainMenu()
            textbutton _("Help") action Help()
            textbutton _("Quit") action Quit()

    style gm_nav_button:
        size_group "gm_nav"

.. _save-screen:

Save
----

The ``save`` screen is used to select a file in which to save the
game.

::

    screen save():

        # This ensures that any other menu screen is replaced.
        tag menu

        use navigation

        frame:
            has vbox

            # The buttons at the top allow the user to pick a
            # page of files.
            hbox:
                textbutton _("Previous") action FilePagePrevious()
                textbutton _("Auto") action FilePage("auto")

                for i in range(1, 9):
                    textbutton str(i) action FilePage(i)

                textbutton _("Next") action FilePageNext()

            # Display a grid of file slots.
            grid 2 5:
                transpose True
                xfill True

                # Display ten file slots, numbered 1 - 10.
                for i in range(1, 11):

                    # Each file slot is a button.
                    button:
                        action FileAction(i)
                        xfill True
                        style "large_button"

                        has hbox

                        # Add the screenshot and the description to the
                        # button.
                        add FileScreenshot(i)
                        text ( " %2d. " % i
                               + FileTime(i, empty=_("Empty Slot."))
                               + "\n"
                               + FileSaveName(i)) style "large_button_text"

.. _load-screen:

Load
----

The ``load`` screen is used to select a file from which to load the
game.

::

    screen load():

        # This ensures that any other menu screen is replaced.
        tag menu

        use navigation

        frame:
            has vbox

            # The buttons at the top allow the user to pick a
            # page of files.
            hbox:
                textbutton _("Previous") action FilePagePrevious()
                textbutton _("Auto") action FilePage("auto")

                for i in range(1, 9):
                    textbutton str(i) action FilePage(i)

                textbutton _("Next") action FilePageNext()

            # Display a grid of file slots.
            grid 2 5:
                transpose True
                xfill True

                # Display ten file slots, numbered 1 - 10.
                for i in range(1, 11):

                    # Each file slot is a button.
                    button:
                        action FileAction(i)
                        xfill True
                        style "large_button"

                        has hbox

                        # Add the screenshot and the description to the
                        # button.
                        add FileScreenshot(i)
                        text ( " %2d. " % i
                               + FileTime(i, empty=_("Empty Slot."))
                               + "\n"
                               + FileSaveName(i)) style "large_button_text"

.. _preferences-screen:

Preferences
-----------

The ``preferences`` screen is used to select options that control the
display of the game.

In general, the preferences are either actions or bar values returned
from :func:`Preference`.

::

    screen preferences():

        tag menu

        # Include the navigation.
        use navigation

        # Put the navigation columns in a three-wide grid.
        grid 3 1:
            style_prefix "prefs"
            xfill True

            # The left column.
            vbox:
                frame:
                    style_prefix "pref"
                    has vbox

                    label _("Display")
                    textbutton _("Window") action Preference("display", "window")
                    textbutton _("Fullscreen") action Preference("display", "fullscreen")

                frame:
                    style_prefix "pref"
                    has vbox

                    label _("Transitions")
                    textbutton _("All") action Preference("transitions", "all")
                    textbutton _("None") action Preference("transitions", "none")

                frame:
                    style_prefix "pref"
                    has vbox

                    label _("Text Speed")
                    bar value Preference("text speed")

                frame:
                    style_prefix "pref"
                    has vbox

                    textbutton _("Joystick...") action ShowMenu("joystick_preferences")

            vbox:

                frame:
                    style_prefix "pref"
                    has vbox

                    label _("Skip")
                    textbutton _("Seen Messages") action Preference("skip", "seen")
                    textbutton _("All Messages") action Preference("skip", "all")

                frame:
                    style_prefix "pref"
                    has vbox

                    textbutton _("Begin Skipping") action Skip()

                frame:
                    style_prefix "pref"
                    has vbox

                    label _("After Choices")
                    textbutton _("Stop Skipping") action Preference("after choices", "stop")
                    textbutton _("Keep Skipping") action Preference("after choices", "skip")

                frame:
                    style_prefix "pref"
                    has vbox

                    label _("Auto-Forward Time")
                    bar value Preference("auto-forward time")

            vbox:

                frame:
                    style_prefix "pref"
                    has vbox

                    label _("Music Volume")
                    bar value Preference("music volume")

                frame:
                    style_prefix "pref"
                    has vbox

                    label _("Sound Volume")
                    bar value Preference("sound volume")
                    textbutton "Test" action Play("sound", "sound_test.ogg") style "soundtest_button"

                frame:
                    style_prefix "pref"
                    has vbox

                    label _("Voice Volume")
                    bar value Preference("voice volume")
                    textbutton "Test" action Play("voice", "voice_test.ogg") style "soundtest_button"

    style pref_frame:
        xfill True
        xmargin 5
        top_margin 5

    style pref_vbox:
        xfill True

    style pref_button:
        size_group "pref"
        xalign 1.0

    style pref_slider:
        xmaximum 192
        xalign 1.0

    style soundtest_button:
        xalign 1.0

.. _yesno-prompt-screen:
.. _confirm-screen:

Confirm
-------

The ``confirm`` screen is used to ask yes/no choices of the
user. It takes the following parameters:

`message`
    The message to display to the user. At least the following messages are used by Ren'Py:

    * gui.ARE_YOU_SURE - "Are you sure?" This should be the default if the message is unknown.
    * gui.DELETE_SAVE - "Are you sure you want to delete this save?"
    * gui.OVERWRITE_SAVE - "Are you sure you want to overwrite your save?"
    * gui.LOADING - "Loading will lose unsaved progress.\nAre you sure you want to do this?"
    * gui.QUIT - "Are you sure you want to quit?"
    * gui.MAIN_MENU - "Are you sure you want to return to the main\nmenu? This will lose unsaved progress."
    * gui.CONTINUE - "Are you sure you want to continue where you left off?"
    * gui.END_REPLAY - "Are you sure you want to end the replay?"
    * gui.SLOW_SKIP - "Are you sure you want to begin skipping?"
    * gui.FAST_SKIP_SEEN - "Are you sure you want to skip to the next choice?"
    * gui.FAST_SKIP_UNSEEN - "Are you sure you want to skip unseen dialogue to the next choice?"
    * UNKNOWN_TOKEN - This save was created on a different device. Maliciously constructed save files can harm your computer. Do you trust this save's
      creator and everyone who could have changed the file?
    * TRUST_TOKEN - Do you trust the device the save was created on? You should only choose yes if you are the device's sole user.

    The values of the variables are strings, which means they can be
    displayed using a text displayable.

`yes_action`
    The action to run when the user picks "Yes".

`no_action`
    The action to run when the user picks "No".

Until Ren'Py 6.99.10, this screen was known as the ``yesno_prompt`` screen.
If no ``confirm`` screen is present, ``yesno_prompt`` is used instead.

This screen will also be called by the :func:`renpy.confirm` function and the :func:`Confirm` action.

::

    screen confirm(message, yes_action, no_action):

        modal True

        window:
            style "gm_root"

        frame:
            style_prefix "confirm"

            xfill True
            xmargin 50
            ypadding 25
            yalign .25

            vbox:
                xfill True
                spacing 25

                text _(message):
                    textalign 0.5
                    xalign 0.5

                hbox:
                    spacing 100
                    xalign .5
                    textbutton _("Yes") action yes_action
                    textbutton _("No") action no_action
