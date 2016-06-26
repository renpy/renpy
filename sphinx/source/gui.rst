.. _gui:

=======================
GUI Customization Guide
=======================

Ren'Py features a GUI system that (we hope) looks attractive out of the box,
can be customized somewhat, and can be replaced entirely if necessary. This
page explains how to do simple and intermediate levels of GUI customization.

For more advanced customization, please take a look at the documentation for
:ref:`styles <styles>` (including the list of :ref:`style properties <style-properties>`
and :ref:`screens <screens>` (including
:ref:`screen actions <screen-actions>` and :ref:`special screens <screen-special>`).

This assumes that you're using a new-style Ren'Py GUI (contained in the gui.rpy
file). Older GUIs (that use the screens.rpy file) should be treated as advanced
gui customization for the purposes of this guide.


Simple GUI Customization
========================

There are a few simple pieces of GUI customization that make sense for
all but the simplest visual novels. What these customizations have in
common is that they do not require editing gui.rpy. These customizations
change the GUI somewhat, but do not drastically change the look of the
GUI.


Change Size and Colors
----------------------

The easiest thing to change about the GUI is to change the size and
color of the GUI. Ren'Py will prompt you to make these choices when
you first create a project, but choosing "Change/Update GUI" in the
launcher will let you change your choice.

When changing the GUI through the launcher, Ren'Py will prompt if you
want to simply change the launcher, or update gui.rpy. Both choices
will overwrite most image files, and overwriting gui.rpy will get rid
of changes to that file.

As a result, you probably want to do this before any other customization.

Ren'Py will prompt for the default resolution of the project, and then
also for the color scheme to use. Once you select those, it will update
the GUI to match your choices.


Options.rpy
-----------

There are a couple of variables in options.rpy that are used by the
gui code.

:var:`config.name`
    A string giving a human-readable name for the game. This is used as the
    window title, and throughout the GUI wherever the title of the
    game is needed.

:var:`config.version`
    A string giving the version of the game. This is presented to the
    user in various places.

:var:`gui.about`
    Additional text that is added to the about screen. If you want multiple
    paragraphs of credits, \\n\\n can be used to separate the paragraphs.

Here's an example of these three defines::

    define config.name = _('Old School High School')

    define config.version = "1.0"

    define gui.about = _("Created by PyTom.\n\nHigh school backgrounds by Mugenjohncel.")

For convenience, it might make sense to define gui.about using a triple-quoted
string, in which case line endings are respected. ::

    define gui.about = _("""\
    Created by PyTom.

    High school backgrounds by Mugenjohncel.""")


Game and Main Menu Background Images
-------------------------------------

The images used by the GUI can be found in the game/gui directory,
which can be opened by choosing "Open Directory: gui" from the
launcher. The relevant files are:

gui/main_menu.png
    A file that contains an image that is used in the background of
    all screens of the main menu.

gui/game_menu.png
    A file that contains an image that is used in the background of
    all screens of the game menu.

.. ifconfig:: renpy_figures

    .. figure:: gui/easy_main_menu.jpg
        :width: 100%

        The main menu, with only gui/main_menu.png replaced.

    .. figure:: gui/easy_game_menu.jpg
        :width: 100%

        The about screen can be part of the game menu (using gui/game_menu.png
        as the background) or the main menu (using gui/main_menu.png as the
        background). Both can be set to the same image.

Say Screen and Textbox
----------------------

The say screen is used to display dialogue to the player. There are a number
of relatively easy customizations that can be performed to the Say screen.
The first is changing the textbox:

gui/textbox.png
    This file contains the background of the text window, displayed as part
    of the say screen. While this should be the full width of the game, text
    is only displayed in the central 60% of the screen, with a 20% border
    on either side.

In addition, there are a number of variables that can be customized to change
the say screen.

.. var:: gui.text_color = "#402000"

    This sets the color of the dialogue text.

.. var:: gui.default_font = "ArchitectsDaughter.ttf"

    This sets the font that is used for dialogue text, menus, inputs, and
    other in-game text. The font file should exist in the game directory.

.. var:: gui.text_size = 33

    Sets the size of the dialogue text. This may need to be increased or
    decreased to fit the selected font in the space alloted.

.. var:: gui.label_size = 45

    Sets the size of character name labels.

By default, the character name label uses the accent color. The color can
be easily changed when defining a character::

    define e = Character("Eileen", who_color="#104010")

.. ifconfig:: renpy_figures

    .. figure:: oshs/game/gui/textbox.png
        :width: 100%

        An example textbox image.

    .. figure:: gui/easy_say_screen.jpg
        :width: 100%

        The say screen, customized using the textbox image and the variable
        settings given above.

Choice Menus
------------

The choice screen is used by the menu statement to display choices to
the player. Again, there  are some relatively easy customizations that
can be performed on the choice screen. The first are the two image
files:

gui/choice/idle_background.png
    This image is used as the background of choice buttons that are not
    focused.

gui/choice/hover_background.png
    This image is used as the background of choice buttons that are focused.

By default, text is placed in the central 75% of these images. The color
of choice text is controlled by two variables:

.. var:: gui.choice_idle_color = '#cccccc'

    The color used for the text of unfocused choice buttons.

.. var:: gui.choice_hover_color = '#0066cc'

    The color used for the text of focused choice buttons.

.. ifconfig:: renpy_figures

    .. figure:: oshs/game/gui/choice/idle_background.png
        :width: 100%

        An example gui/choice/idle_background.png image.

    .. figure:: oshs/game/gui/choice/hover_background.png
        :width: 100%

        An example gui/choice/hover_background.png image.

    .. figure:: gui/easy_choice_screen.jpg
        :width: 100%

        An example of the choice screen, as customized using the images
        and variable settings given above.


Window Icon
-----------

The window icon is the icon that is displayed (in places like the Windows
task bar and Macintosh dock) by a running application.

The window icon can be changed by replacing gui/window_icon.png.

Note that this only changes the icon used by the running game. To change
the icon used by Windows .exe files and Macintosh applications, see the
:ref:`build documentation <special-files>`.



Intermediate GUI Customization
==============================

Next, we will demonstrate the intermediate level of GUI customization.
At the intermediate level, it's possible to change the colors, fonts,
and images used by the game. In general, intermediate customization
keeps the screens mostly the same, with buttons and bars in the same
places, although modifying the screens to add new functionality
is certainly possible.


Overlay Images
--------------

There are also a pair of overlay images. These are used to darken or
lighten the background image to make buttons and other user interface
components more readable. These images are in the overlay directory:

gui/overlay/main_menu.png
    The overlay used by the main menu screen.

gui/overlay/game_menu.png
    The overlay used by game-menu-like screens, including load, save,
    preferences, about, help, etc. This overlay is selected by the
    screen in question, and is used even when at the main menu.


Here are a pair of example overlay images, and what the game looks like
with the overlay images added.


.. ifconfig:: renpy_figures

    .. figure:: oshs/game/gui/overlay/main_menu.png
        :width: 100%

        An example gui/overlay/main_menu.png image.

    .. figure:: oshs/game/gui/overlay/game_menu.png
        :width: 100%

        An example gui/overlay/game_menu.png image.

    .. figure:: gui/overlay_main_menu.jpg
        :width: 100%

        The main menu after changing the overlays.

    .. figure:: gui/overlay_game_menu.jpg
        :width: 100%

        The game menu after changing the overlays.


Colors, Fonts, and Font Sizes
-----------------------------

There are a number of gui variables that can be used to change the color, font,
and size of text.

.. raw:: html

   <p>These variables should generally be set to hexadecimal color
   codes, which are strings of the form "#rrggbb", similar to color codes
   used by web browsers. For example, "#663399" is the code for a shade of
   <a href="http://www.economist.com/blogs/babbage/2014/06/digital-remembrance" style="text-decoration: none; color: rebeccapurple">purple</a>.
   There are many tools online that let you create html color codes, such as
   <a href="http://htmlcolorcodes.com/color-picker/">this one</a>.</p>

In addition to :var:`gui.text_color`, :var:`gui.choice_idle_color`, and :var:`gui.choice_hover_color`,
documented above, the following variables exist:

.. var:: gui.accent_color = '#000060'

    The accent color is used in many places in the GUI, including titles
    and labels.

.. var:: gui.idle_color = '#606060'

    The color used for most buttons when not focused or selected.

.. var:: gui.idle_small_color = '#404040'

    The color used for small text (like the dates of save slots) when not selected.
    This color often needs to be a bit lighter or darker than idle_color to compensate
    for the smaller size of the font.

.. var:: gui.hover_color = '#3284d6'

    The color used by the text of focused buttons.

.. var:: gui.selected_color = '#555555'

    The color used by the text of selected buttons. (This takes priority
    over the selected and idle colors.)

.. var:: gui.insensitive_color = '#8888887f'

    The color used by buttons that are insensitive to user input. (For example,
    the rollback button when no rollback is possible.)

.. var:: gui.interface_text_color = '#404040'

    The color used by static text in the game interface, such as text on the
    help and about screens.

In additional to :var:`gui.default_font`, the following variables selects the
fonts used for text. These fonts should also be placed in the game directory.

.. var:: gui.interface_font = "ArchitectsDaughter.ttf"

    The font used for text for user interface elements, like the main and
    game menus, buttons, and so on.

.. var:: gui.glyph_font = "DejaVuSans.ttf"

    A font used for certain glyphs, such as the arrow glyphs used by the skip
    indicator. DejaVuSans is a reasonable default for these glyphs, and is
    automatically included with every Ren'Py game.

In addition to :var:`gui.text_size` and :var:`gui.label_size`, the following
variables control text sizes.

.. var:: gui.tiny_size = 21

    The smallest size text, used for dates and save names in the file picker.

.. var:: gui.notify_size = 24

    The size of text on the notification screen.

.. var:: gui.interface_size = 36

    The size of text that is part of an interface element like a button or
    an interface label.

.. var:: gui.title_size = 75

    The size of text that's used on the main menu.

.. ifconfig:: renpy_figures

    .. figure:: gui/text.jpg
        :width: 100%

        The game menu after customizing text colors, fonts, and sizes.

Borders
-------



Other
-----



::

    screen ctc():
        style_prefix "ctc"

        # Place on top of normal screens.
        zorder 1

        hbox:
            spacing gui.scale(6)

            xalign 1.0
            xoffset gui.scale(-20)
            yalign 1.0
            yoffset gui.scale(-20)

            text "▶" at delayed_blink(2.0, 3.0) style "ctc_triangle"
            text "▶" at delayed_blink(2.2, 3.0) style "ctc_triangle"
            text "▶" at delayed_blink(2.4, 3.0) style "ctc_triangle"

    style ctc_triangle:
        # We have to use a font that has the BLACK RIGHT-POINTING TRIANGLE glyph
        # in it.
        color gui.accent_color
        font gui.glyph_font



