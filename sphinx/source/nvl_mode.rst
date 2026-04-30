NVL-Mode Tutorial
=================

There are two main styles of presentation used for visual
novels. ADV-style games present dialogue and narration one line at a
time, generally in a window at the bottom of the screen. NVL-style
games present multiple lines on the screen at a time, in a window that
takes up the entire screen.

In this tutorial, we will explain how to make an NVL-mode game using
Ren'Py. This tutorial assumes that you are already familiar with the
basics of Ren'Py, as explained in the :doc:`Quickstart manual<quickstart>`.

Getting Started
---------------

NVL-mode can be added to a Ren'Py script in two steps. The first is to
declare the characters to use NVL-mode, and the second is to add ``nvl
clear`` statements at the end of each page.

Characters can be declared to use NVL-mode by adding a ``kind=nvl``
parameter to each of the Character declarations. For example, if we
use the character declarations from the Quickstart manual::

    define s = Character('Sylvie', color="#c8ffc8")
    define m = Character('Me', color="#c8c8ff")

Changed to use NVL-mode, those declarations become::

    define s = Character('Sylvie', kind=nvl, color="#c8ffc8")
    define m = Character('Me', kind=nvl, color="#c8c8ff")

An NVL-mode narrator can also be used by including the following
definition::

    define narrator = nvl_narrator

Note that we have also added an NVL-mode declaration of
``narrator``. The ``narrator`` character is used to speak
lines that do not have another character name associated with it.

If we ran the game like this, the first few lines would display
normally, but after a while, lines would begin displaying below the
bottom of the screen. To break the script into pages, include an ``nvl
clear`` statement after each page.

The following is an example script with pagination::

    label start:
        "I'll ask her..."

        m "Um... will you..."
        m "Will you be my artist for a visual novel?"

        nvl clear

        "Silence."
        "She is shocked, and then..."

        s "Sure, but what is a \"visual novel?\""

        nvl clear

While nvl-mode games generally have more text per paragraph, this
example demonstrates a basic NVL-mode script. (Suitable for use in a
kinetic novel that does not have transitions.)

.. _nvl-monologue-mode:

:ref:`Monologue mode <monologue-mode>` works with NVL-mode as well.
Including the ``{clear}`` text tag on a line by itself is the equivalent
of an ``nvl clear`` statement without leaving monologue mode. For example::

    label start:
        s """
        This is one block of text in monologue mode.

        This is a second block, on the same page as the first.

        {clear}

        The page just cleared!
        """

.. _nvl-mode-menu:

NVL-mode Menus
--------------

By default, menus are displayed in ADV-mode, taking up the full
screen. There is also an alternate NVL-mode menu presentation, which
displays the menus immediately after the current page of NVL-mode
text.

To access this alternate menu presentation, write::

    define menu = nvl_menu

The menu will disappear after the choice has been made, so it usually
makes sense to follow menus with an "nvl clear" or some sort of
indication as to the choice.

:ref:`Menu arguments <menu-arguments>` can also be used to access
a NVL-mode menu. This is done by providing a true `nvl` argument
that is set to True. This is useful when mixing NVL-mode and ADV-mode
menus in a single game. ::

    menu (nvl=True):
        "I prefer NVL-mode.":
            pass

        "ADV-mode is more for me.":
            pass


Showing and Hiding the NVL-mode Window
--------------------------------------

The NVL-mode window can be controlled with the standard ``window show``
and ``window hide`` statements. To select the default transitions to be
used for showing and hiding the window, add the following to your game::

    init python:
        config.window_hide_transition = dissolve
        config.window_show_transition = dissolve

The default :var:`config.empty_window` should select appropriate window
automatically, but setting :var:`config.empty_window` to ``nvl_show_core``
will force the NVL-mode window to be displayed during a transition.::

    init python:
        config.empty_window = nvl_show_core

An example of using the window commands to show and hide the window is::

    label meadow:

        nvl clear

        window hide
        scene bg meadow
        with fade
        window show

        "We reached the meadows just outside our hometown. Autumn was so
         beautiful here."
        "When we were children, we often played here."

        m "Hey... ummm..."

        window hide
        show sylvie smile
        with dissolve
        window show

        "She turned to me and smiled."
        "I'll ask her..."
        m "Ummm... will you..."
        m "Will you be my artist for a visual novel?"

There are also explicit ``nvl show`` and ``nvl hide`` commands that show
hide the NVL-mode window. These take an optional transition, and can be
used in games that use a mix of NVL-mode and ADV-mode windows.

Customizing Characters
----------------------

NVL-mode characters can be customized to have several looks, hopefully allowing
you to pick the one that is most appropriate to the game you are creating.

1. The default look has a character's name to the left, and
   dialogue indented to the right of the name. The color of the name is
   controlled by the ''color'' parameter. ::

    define s = Character('Sylvie', kind=nvl, color="#c8ffc8")

2. A second look has the character's name embedded in with the
   text. Dialogue spoken by the character is enclosed in quotes. Note
   that here, the character's name is placed in the ''what_prefix''
   parameter, along with the open quote. (The close quote is placed in
   the ''what_suffix'' parameter.) ::

    define s = Character(None, kind=nvl, what_prefix="Sylvie: \"",
                         what_suffix="\"")

3. A third look dispenses with the character name entirely, while
   putting the dialogue in quotes. ::

    define s = Character(None, kind=nvl, what_prefix="\"", what_suffix="\"")

4. Since the third look might make it hard to distinguish who's
   speaking, we can tint the dialogue using the ''what_color''
   parameter. ::

    define s = Character(None, kind=nvl, what_prefix="\"", what_suffix="\"",
                         what_color="#c8ffc8")

5. Of course, a completely uncustomized NVL-mode character can be
   used, if you want to take total control of what is shown. (This is
   often used for the narrator.) ::

    define s = Character(None, kind=nvl)


Config Variables
----------------

The following config variables control nvl-related functionality.

.. var:: config.nvl_layer = "screens"

    The layer the nvl screens are shown on.

.. var:: config.nvl_list_length = None

    If not None, the maximum length of the list of NVL dialogue.
    This can be set (often in conjunction with forcing the dialogue to
    have a fixed height) in order to emulate an infinite scrolling
    NVL window.

.. var:: config.nvl_page_ctc = None

    If not None, this is the click-to-continue indicator that is used for NVL mode
    characters that are at the end of a page. (That is, immediately
    followed by an nvl clear statement.) This replaces the ctc parameter
    of :func:`Character`.

.. var:: config.nvl_page_ctc_position = "nestled"

    If not None, this is the click-to-continue indicator position that is used for NVL mode
    characters that are at the end of a page. (That is, immediately
    followed by an nvl clear statement.) This replaces the ctc_position parameter
    of :func:`Character`.

.. var:: config.nvl_paged_rollback = False

    If true, NVL-mode rollback will occur a full page at a time.

Python Functions
----------------

.. include:: inc/nvl


Paged Rollback
--------------

Paged rollback causes Ren'Py to rollback one NVL-mode page at a time,
rather than one block of text at a time.  It can be enabled by
including the following in your script. ::

    init python:
        config.nvl_paged_rollback = True


Script of The Question (NVL-mode Edition)
-----------------------------------------

You can view the full script of the NVL-mode edition of ''The Question''
:doc:`here <thequestion_nvl>`.
