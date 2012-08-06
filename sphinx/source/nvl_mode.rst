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
the character declarations from the Quickstart manual are::

    define s = Character('Sylvie', color="#c8ffc8")
    define m = Character('Me', color="#c8c8ff")

Changed to use NVL-mode, those declarations become::

    define s = Character('Sylvie', kind=nvl, color="#c8ffc8")
    define m = Character('Me', kind=nvl, color="#c8c8ff")
    define narrator = Character(None, kind=nvl)

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

Menus
-----

By default, menus are displayed in ADV-mode, taking up the full
screen. There is also an alternate NVL-mode menu presentation, which
displays the menus immediately after the current page of NVL-mode
text.

To access this alternate menu presentation, write::

    init python:
        menu = nvl_menu

The menu will disappear after the choice has been made, so it usually
makes sense to follow menus with an "nvl clear" or some sort of
indication as to the choice.

Showing and Hiding the NVL-mode Window
--------------------------------------

The NVL-mode window can be controlled with the standard ``window show``
and ``window hide`` statements. To enable this, add the following code
to your game::

    init python:
        config.empty_window = nvl_show_core
        config.window_hide_transition = dissolve
        config.window_show_transition = dissolve

Setting :var:`config.empty_window` to ``nvl_show_core``
will cause the NVL-mode window to be displayed during a
transition. (The last two lines select the default transitions to be
used for showing and hiding the window.)

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

Customizing Menus
-----------------

There are a few styles that control the look of the menus. Here's some
code showing how to customize them. See :doc:`style` for more information
about styles. ::

    init python:

        # The color of a menu choice when it isn't hovered.
        style.nvl_menu_choice.idle_color = "#ccccccff"

        # The color of a menu choice when it is hovered.
        style.nvl_menu_choice.hover_color = "#ffffffff"

        # The color of the background of a menu choice, when it isn't
        # hovered.
        style.nvl_menu_choice_button.idle_background = "#00000000"

        # The color of the background of a menu choice, when it is
        # hovered.
        style.nvl_menu_choice_button.hover_background = "#ff000044"

        # How far from the left menu choices should be indented.
        style.nvl_menu_choice_button.left_margin = 20

Customizing the NVL window
--------------------------

There are a few styles that control the NVL window; here's some code showing
how to customize them.  See :doc:`style` for more information
about styles. ::

    init python:

        # Set the background of the NVL window; this image should be the
        # same size as the screen.
        style.nvl_window.background = "nvl_window.png"

        # Add some additional padding around the contents of the NVL window.
        # This keeps the text inside the borders of our image.
        style.nvl_window.xpadding = 55
        style.nvl_window.ypadding = 55

        # Set the spacing between each block of text on the page.
        # The default is 10 pixels.
        style.nvl_vbox.box_spacing = 10

You can also completely customize the screen used to display NVL text, which
is named ``nvl``; see :ref:`nvl-screen`.


Paged Rollback
--------------

Paged rollback causes Ren'Py to rollback one NVL-mode page at a time,
rather than one block of text at a time.  It can be enabled by
including the following code in your script. ::

    init python:
        config.nvl_paged_rollback = True

Script of The Question (NVL-mode Edition)
-----------------------------------------

You can view the full script of the NVL-mode edition of ''The Question''
:ref:`here <thequestion_nvl>`.

