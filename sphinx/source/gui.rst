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

    .. var:: config.name = _('Old School High School')

    .. var:: config.version = "1.0"

    .. var:: gui.about = _("Created by PyTom.\n\nHigh school backgrounds by Mugenjohncel.")

For convenience, it might make sense to .. var:: gui.about using a triple-quoted
string, in which case line endings are respected. ::

    .. var:: gui.about = _("""\
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

.. var:: gui.name_text_size = 45

    Sets the size of character names.

By default, the character name label uses the accent color. The color can
be easily changed when defining a character::

    .. var:: e = Character("Eileen", who_color="#104010")

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

gui/button/choice_idle_background.png
    This image is used as the background of choice buttons that are not
    focused.

gui/button/choice_hover_background.png
    This image is used as the background of choice buttons that are focused.

By default, text is placed in the central 75% of these images. There are
also a couple of variables that control the color of the text in choice
buttons.

.. var:: gui.choice_button_text_idle_color = '#888888'

    The color used for the text of unfocused choice buttons.

.. var:: gui.choice_text_hover_color = '#0066cc'

    The color used for the text of focused choice buttons.

These should suffice for simple customization, where the size of the images
does not need to be changed. For more complex customizations, check out the
section on buttons, below.

.. ifconfig:: renpy_figures

    .. figure:: oshs/game/gui/button/choice_idle_background.png
        :width: 100%

        An example gui/button/idle_background.png image.

    .. figure:: oshs/game/gui/button/choice_hover_background.png
        :width: 100%

        An example gui/button/choice_hover_background.png image.

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

Regenerating Images
-------------------

Some of the adjustments either partially or completely effect image
files. As a result, the changes only take effect when the image files
themselves are updated, which can be done by choosing "Change GUI" in
the launcher, and telling it to regenerate image files.

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

gui/overlay/confirm.png
    The overlay used in the confirm screen to darken the background.

.. ifconfig:: renpy_figures

    Here are a pair of example overlay images, and what the game looks like
    with the overlay images added.

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

    The color used for small text (like the date and name of a save slot,
    and quick menu buttons) when not hovered. This color often needs to be a
    bit lighter or darker than idle_color to compensate for the smaller size
    of the font.

.. var:: gui.hover_color = '#3284d6'

    The color used by focused items in the gui, including the text of
    of buttons and the thumbs (movable areas) of sliders and scrollbars.

.. var:: gui.selected_color = '#555555'

    The color used by the text of selected buttons. (This takes priority
    over the hover and idle colors.)

.. var:: gui.insensitive_color = '#8888887f'

    The color used by the text of buttons that are insensitive to user input.
    (For example, the rollback button when no rollback is possible.)

.. var:: gui.interface_text_color = '#404040'

    The color used by static text in the game interface, such as text on the
    help and about screens.

.. var:: gui.muted_color = '#6080d0'
.. var:: gui.hover_muted_color = '#8080f0'

    Muted colors, used for the sections of bars, scrollbars, and sliders that
    do not represent the value or visible area. (These are only used when
    generating images, and will not take effect until images are regenerated
    in the launcher.)

In additional to :var:`gui.default_font`, the following variables selects the
fonts used for text. These fonts should also be placed in the game directory.

.. var:: gui.interface_font = "ArchitectsDaughter.ttf"

    The font used for text for user interface elements, like the main and
    game menus, buttons, and so on.

.. var:: gui.glyph_font = "DejaVuSans.ttf"

    A font used for certain glyphs, such as the arrow glyphs used by the skip
    indicator. DejaVuSans is a reasonable default for these glyphs, and is
    automatically included with every Ren'Py game.

In addition to :var:`gui.text_size` and :var:`gui.name_text_size`, the following
variables control text sizes.

.. var:: gui.interface_text_size = 36

    The size of static text in the game's user interface, and the default size
    of button text in the game's interface.

.. var:: gui.label_text_size = 45

    The size of section labels in the game's user interface.

.. var:: gui.notify_text_size = 24

    The size of notification text.

.. var:: gui.title_text_size = 75

    The size of the game's title.

.. ifconfig:: renpy_figures

    .. figure:: gui/text.jpg
        :width: 100%

        The game menu after customizing text colors, fonts, and sizes.

Borders
-------

There are a number of GUI components - such as buttons and bars - that use
scalable backgrounds confgured using Border objects. Before discussing,
how to customize buttons and bars, we'll first describe how this works.

Borders are given to the :func:`Frame` displayable.
A Frame takes an image, and divides it into nine parts - the four corners,
the four sides, and the center. The corners always remain the same size,
the left and right sides are stretched vertically, the top and bottom sides
are stretched horizontally, and the center is stretched in both directions.

A Borders object gives the size of each of the borders, in left, top, right,
bottom order. So if the following border image is used:

.. image:: oshs/game/images/borders.png

along with the following borders::

    Borders(40, 40, 40, 40)

one possible result is this:

.. image:: gui/borders1.png

As the child changes size, so will the background.

A Border object can also be given padding, including negative padding that
causes the child to overlap the borders. For example, these borders::

    Borders(40, 40, 40, 40, -20, -20, -20, -20)

allow the child to overlap the sides. Note that due to this overlap, the
result is smaller, since the borders themselves now take up less space.

.. image:: gui/borders2.png

Borders can also be tiled, rather than scaled. This is invoked by variables,
and produces this result.

.. image:: gui/borders3.png

These example images are a bit ugly, since we need to show what's going on.
In practice, this system can produce quite pleasing results. This is the case when
a Frame displayable is used as the background of a frame window holding
user interface components.

These frame windows can be customized in two ways. The first is by changing the
background image file:

gui/frame.png
    The image used as the background of frames windows.

And the second is by customizing variables.

.. var:: gui.frame_borders = Borders(15, 15, 15, 15)

    The borders applied to frame windows.

.. var:: gui.confirm_frame_borders = Borders(60, 60, 60, 60)

    The borders applied to the fame used in the confirm screen.

.. var:: gui.frame_tile

    If true, the sides and center of the confirm screen are tiled. If false,
    they are scaled.

.. ifconfig:: renpy_figures

    .. figure:: oshs/game/gui/frame.png
        :width: 100%

        An example gui/frame.png image.

    .. figure:: gui/frame_confirm.jpg
        :width: 100%

        The confirm screen after applying the customizations given
        above.

Buttons
-------

The Ren'Py user interface includes a large number of buttons, buttons
that come in different sizes and that are used for different purposes.
The various kinds of buttons are:

button
    A basic button. Used for navigation within the user interface.

choice_button
    A button used for choices in the in-game menu.

quick_button
    A button, displayed in-game, that is intended to allow quick access
    to the game menu.

navigation_button
    A button used in main and game menu for navigation between screens,
    and to start the game.

page_button
    A button used to switch between pages on the load and save screens.

slot_button
    Buttons that represent file slots, and contain a thumbnail, the save
    time, and an optional save name. These are described in more detail
    below.

radio_button
    A button used for multiple-choice preferences on the preferences
    screen.

check_button
    A button used for toggleable preferences on the preferences screen.

test_button
    A button used to test audio playback on the preferences screen. This
    should be the same height as a horizontal slider.

help_button
    A button used to select what kind of help the player wants.

confirm_button
    A button used on the confirm screen to select yes or no.


The following image files are used to customize button backgrounds,
if they exist.

gui/button/idle_background.png
    The background image used by buttons that are not focused.

gui/button/hover_background.png
    The background image used by buttons that are focused.

gui/button/selected_idle_background.png
    The background image used by buttons that are selected but not
    focused. This is optional, and is used in preference to
    idle_background.png if it exists.

gui/button/selected_hover_background.png
    The background image used by buttons that are selected but not
    focused. This is optional, and is used in preference to
    hover_background.png if it exists.

More specific backgrounds can be given for each kind of button, by
prefixing it with the kind. For example, gui/button/check_idle_background.png
is used as the background of check buttons that are not focused.

Four image files are used as foreground decorations on radio and check
buttons, to indicate if the option is chosen or not.

gui/button/check_foreground.png, gui/button/radio_foreground.png
    These images are used when a check or radio button is not selected.

gui/button/check_selected_foreground.png, gui/button/radio_selected_foreground.png
    These images are used when a check or radio button is selected.


The following variables set various properties of buttons:

.. var:: gui.button_width = None
.. var:: gui.button_height = 64

    The width and height of a button, in pixels. If None, the size is
    automatically determined based on the size of the text inside a button,
    and the borders given below.

.. var:: gui.button_borders = Borders(10, 10, 10, 10)

    The borders surrounding a button, in left, top, right, bottom order.

.. var:: gui.button_tile = True

    If true, the sides and center of the button background are tiled to
    increase or  decrease their size. If false, the sides and center are
    scaled.

.. var:: gui.button_text_font = gui.interface_font
.. var:: gui.button_text_size = gui.interface_text_size

    The font and size of the button text.

.. var:: gui.button_text_idle_color = gui.idle_color
.. var:: gui.button_text_hover_color = gui.hover_color
.. var:: gui.button_text_selected_color = gui.accent_color
.. var:: gui.button_text_insensitive_color = gui.insensitive_color

    The color of the button text in various states.

.. var:: gui.button_text_xalign = 0.0

    The horizontal alignment of the button text. 0.0 is left-aligned,
    0.5 is centered, and 1.0 is right-aligned.


These variables can be prefixed with the button kind to configure a
property for a particular kind of button. For example,
:var:`gui.choice_button_text_idle_color` configures the color of
an idle choice button.

For example, we customize these variables in our sample game.

.. var:: gui.navigation_button_width = 290

    Increases the width of navigation buttons.

.. var:: gui.radio_button_borders = Borders(40, 10, 10, 10)
.. var:: gui.check_button_borders = Borders(40, 10, 10, 10)

    Increases the width of radio and check button borders, leaving extra
    space on the left for the check mark.


.. ifconfig:: renpy_figures

    Here's an example of how the play screen can be customized.

    .. figure:: oshs/game/gui/button/idle_background.png

        An example gui/button/idle_background.png image.

    .. figure:: oshs/game/gui/button/hover_background.png

        An example gui/button/hover_background.png image.

    .. figure:: oshs/game/gui/button/check_foreground.png

        An image that can be used as gui/button/check_foreground.png and
        gui/button/radio_foreground.png.

    .. figure:: oshs/game/gui/button/check_selected_foreground.png

        An image that can be used as gui/button/check_selected_foreground.png and
        gui/button/radio_selected_foreground.png.

    .. figure:: gui/button_preferences.jpg
        :width: 100%

        The preferences screen with the customizations described in this
        section applied.

Save Slot Buttons
------------------

The load and save screens use slot buttons, which are buttons that present
a thumbnail and information about when the file was saved. The following
variables are quite useful when it comes to customizing the size of
the save slots.

.. var:: gui.slot_button_width = 414
.. var:: gui.slot_button_height = 309

    The width and height of the save slot button.

.. var:: gui.slot_button_borders = Borders(15, 15, 15, 15)

    The borders applied to each save slot.

.. var:: config.thumbnail_width = 384
.. var:: config.thumbnail_height = 216

    The width and height of the save thumbnails. Note that these live in
    the config namespace, not the gui namespace. These do not take effect
    until the file is saved and loaded.

.. var:: gui.file_slot_cols = 3
.. var:: gui.file_slot_rows = 2

    The number of columns and rows in the grid of save slots.

There are the background images used for save slots.

gui/button/slot_idle_background.png
    The image used for the background of save slots that are not focused.

gui/button/slot_hover_background.png
    The image used for the background of save slots that arefocused.

.. ifconfig:: renpy_figures

    Putting those to use, we get:

    .. figure:: oshs/game/gui/button/slot_idle_background.png

        An example gui/button/slot_idle_background.png image.

    .. figure:: oshs/game/gui/button/slot_hover_background.png

        An example gui/button/slot/slot_hover_background.png image.

    .. figure:: gui/slot_save.jpg

        The save screen after applying the customizations given in this
        section.

Sliders
-------

Sliders are a type of bar that is used in the preferences screen to
allow the player to adjust preference with a large number of values.
By default, the gui only uses horizontal sliders, but in-game code
may also use vertical sliders.

Sliders are customized with the following images:

gui/slider/horizontal_idle_bar.png, gui/slider/horizontal_hover_bar.png, gui/slider/vertical_idle_bar.png, gui/slider/vertical_hover_bar.png
    Images used for vertical and idle bar backgrounds in idle and
    hover states.

gui/slider/horizontal_idle_thumb.png, gui/slider/horizontal_hover_thumb.png, gui/slider/vertical_idle_thumb.png, gui/slider/vertical_hover_thumb.png
    Images used for the thumb - the movable part of the bar.

The following variables are also used:

.. var:: gui.slider_size = 64

    The height of horizontal sliders, and width of vertical sliders.

.. var:: gui.slider_tile = True

    If true, the frame containing the bar of a slider is tiled. If False,
    if it scaled.

.. var:: gui.slider_borders = Borders(6, 6, 6, 6)
.. var:: gui.vslider_borders = Borders(6, 6, 6, 6)

    The borders that are used with the Frame containing the bar image.

.. ifconfig:: renpy_figures

    Here's an example of how we customize the horizontal slider.

    .. figure:: oshs/game/gui/slider/horizontal_idle_bar.png

        An example gui/slider/horizontal_idle_bar.png image.

    .. figure:: oshs/game/gui/slider/horizontal_hover_bar.png

        An example gui/slider/horizontal_hover_bar.png image.

    .. figure:: oshs/game/gui/slider/horizontal_idle_thumb.png

        An example gui/slider/horizontal_idle_thumb.png image.

    .. figure:: oshs/game/gui/slider/horizontal_hover_thumb.png

        An example gui/slider/horizontal_hover_thumb.png image.

    .. figure:: gui/slider_preferences.jpg
        :width: 100%

        The preferences screen after applying the customizations given in this
        section.



Scrollbars
----------

Scrollbars are bars that are used to scroll viewports. In the gui,
the most obvious place a scrollbar is used is the history screen,
but vertical scrollbars can be used on other screens as well.

Sliders are customized with the following images:

gui/scrollbar/horizontal_idle_bar.png, gui/scrollbar/horizontal_hover_bar.png, gui/scrollbar/vertical_idle_bar.png, gui/scrollbar/vertical_hover_bar.png
    Images used for vertical and idle bar backgrounds in idle and
    hover states.

gui/scrollbar/horizontal_idle_thumb.png, gui/scrollbar/horizontal_hover_thumb.png, gui/scrollbar/vertical_idle_thumb.png, gui/scrollbar/vertical_hover_thumb.png
    Images used for the thumb - the movable part of the bar.

The following variables are also used:

.. var:: gui.scrollbar_size = 24

    The height of horizontal scrollbars, and width of vertical scrollbars.

.. var:: gui.scrollbar_tile = True

    If true, the frame containing the bar of a scrollbar is tiled. If False,
    if it scaled.

.. var:: gui.scrollbar_borders = Borders(10, 6, 10, 6)
.. var:: gui.vscrollbar_borders = Borders(6, 10, 6, 10)

    The borders that are used with the Frame containing the bar image.

.. var:: gui.unscrollable = "hide"

    This controls what to do if the bar is unscrollable. "hide" hides
    the bar, while None keeps it shown.

.. ifconfig:: renpy_figures

    Here's an example of how we customize the vertical scrollbar.

    .. figure:: oshs/game/gui/scrollbar/vertical_idle_bar.png
        :height: 150

        An example gui/scrollbar/vertical_idle_bar.png image.

    .. figure:: oshs/game/gui/scrollbar/vertical_hover_bar.png
        :height: 150

        An example gui/scrollbar/vertical_hover_bar.png image.

    .. figure:: oshs/game/gui/scrollbar/vertical_idle_thumb.png
        :height: 150

        An example gui/scrollbar/vertical_idle_thumb.png image.

    .. figure:: oshs/game/gui/scrollbar/vertical_hover_thumb.png
        :height: 150

        An example gui/scrollbar/vertical_hover_thumb.png image.

    .. figure:: gui/scrollbar_history.jpg
        :width: 100%

        The history screen after applying the customizations given in this
        section.

Bars
----

Plain old bars are used to display a number to the player. They're not
used in the gui, but can be used in creator-defined screens.

A bar can customized by editing the following images:

gui/bar/left.png, gui/bar/bottom.png
    Images that are used for the filled section of horizontal and vertical bars.

gui/bar/right.pbg, gui/bar/top.png
    Images that are used for the filled section of horizontal and vertical bars.

There are also the usual variables that control bars:

.. var:: gui.bar_size = 64

    The height of horizontal bars, and width of vertical bars.

.. var:: gui.bar_tile = False

    If true, the bar images are tiled. If false, the images are linearly
    scaled.

.. var:: gui.bar_borders = Borders(10, 10, 10, 10)
.. var:: gui.bar_borders = Borders(10, 10, 10, 10)

    The borders that are used with the Frames containing the bar images.


.. ifconfig:: renpy_figures

    Here's an example of how we customize horizontal bars.

    .. figure:: oshs/game/gui/bar/left.png
        :width: 100%

        An example gui/bar/left.png image.

    .. figure:: oshs/game/gui/bar/right.png
        :width: 100%

        An example gui/bar/right.png image.

    .. figure:: gui/bar.jpg
        :width: 100%

        A screen we defined to give an example of a bar.


Skip and Notify
---------------

The skip and notify screens both display frames with messages in them. Both
use custom frame background images:


gui/skip.png
    The background of the skip indicator.

gui/notify.png
    The background of the notify screen.

The variables that control these are:

.. var:: gui.skip_frame_borders = Borders(24, 8, 75, 8)

    The borders of the frame that is used by the skip screen.

.. var:: gui.notify_frame_borders = Borders(24, 8, 60, 8)

    The borders of the frame that is used by the notify screen.

.. var:: gui.skip_ypos = 15

    The vertical position of the skip indicator, in pixels from the top of the
    window.

.. var:: gui.notify_ypos = 68

    The vertical position of the notify message, in pixels from the top of the
    window.

.. ifconfig:: renpy_figures

    Here are some example images we can use to customize these screens.

    .. figure:: oshs/game/gui/skip.png
        :width: 100%

        An example gui/skip.png image.

    .. figure:: oshs/game/gui/notify.png
        :width: 100%

        An example gui/notify.png image.

    .. figure:: gui/skip_notify.jpg

        These skip and notify screens in action.


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



