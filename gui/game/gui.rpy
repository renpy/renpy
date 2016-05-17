################################################################################
## Initialization
##
## The offset ensures that these statements run before all others, while the
## gui.init statement initializes the gui, and sets the width and height of
## the game window.

init offset = -1

init python:
    gui.init(1280, 720)


################################################################################
## Colors
##
## The colors of various aspects of the interface.

## An accent color used throughout the interface.
define gui.accent_color = "#00b8c3"

## A version of the accent color that's used when buttons are hovered.
define gui.hover_color = Color(gui.accent_color).tint(.6)

## The color used for a text button when it is selected but not focused.
## A button is selected if it is the current screen or preference value
define gui.selected_color = "#ffffff"

## The color used for a text button when it is neither selected nor hovered.
define gui.idle_color = "#555555"

## The small color is used for small buttons, which need to be brighter/darker
## to achieve the same effect.
define gui.idle_small_color = "#aaaaaa"

## The color used for a text button when it cannot be selected.
define gui.insensitive_color = "#55555580"

## The colors used for dialogue and menu choice text.
define gui.text_color = "#ffffff"
define gui.interface_text_color = "#ffffff"
define gui.choice_text_color = "#cccccc"

## The images used for the main and game menus.
define gui.main_menu_background = "gui/main_menu.png"
define gui.game_menu_background = "gui/game_menu.png"


################################################################################
## Fonts and Font Sizes

define gui.default_font = "DejaVuSans.ttf"
define gui.interface_font = "DejaVuSans.ttf"
define gui.glyph_font = "DejaVuSans.ttf"

define gui.tiny_size = gui.scale(14)
define gui.notify_size = gui.scale(16)
define gui.text_size = gui.scale(22)
define gui.interface_size = gui.scale(24)
define gui.label_size = gui.scale(30)
define gui.title_size = gui.scale(50)


################################################################################
## Window icon.

## This is the icon displayer on the taskbar or dock.
define config.window_icon = "gui/window_icon.png"


################################################################################
## Borders
##
## Borders objects control both the size of the left, top, right, and bottom
## borders used by a Frame, and optionally additional padding added to each
## side.

## Interface buttons.
define gui.button_borders = Borders(gui.scale(4), gui.scale(4), gui.scale(4), gui.scale(4))
define gui.medium_button_borders = Borders(gui.scale(4), gui.scale(4), gui.scale(4), gui.scale(4))
define gui.small_button_borders = Borders(gui.scale(4), gui.scale(4), gui.scale(4), gui.scale(4), pad_left=gui.scale(10), pad_right=gui.scale(10))
define gui.check_button_borders = Borders(gui.scale(25), gui.scale(4), gui.scale(4), gui.scale(4))
define gui.radio_button_borders = Borders(gui.scale(25), gui.scale(4), gui.scale(4), gui.scale(4))

## Choice buttons used by the menu statement.
define gui.choice_borders = Borders(gui.scale(100), gui.scale(5), gui.scale(100), gui.scale(5))

## Bars, scrollbars, and sliders.
define gui.bar_borders = Borders(gui.scale(4), gui.scale(4), gui.scale(4), gui.scale(4))
define gui.scrollbar_borders = Borders(gui.scale(4), gui.scale(4), gui.scale(4), gui.scale(4))
define gui.slider_borders = Borders(gui.scale(4), gui.scale(4), gui.scale(4), gui.scale(4))
define gui.vbar_borders = Borders(gui.scale(4), gui.scale(4), gui.scale(4), gui.scale(4))
define gui.vscrollbar_borders = Borders(gui.scale(4), gui.scale(4), gui.scale(4), gui.scale(4))
define gui.vslider_borders = Borders(gui.scale(4), gui.scale(4), gui.scale(4), gui.scale(4))

## Frames.
define gui.frame_borders = Borders(gui.scale(4), gui.scale(4), gui.scale(4), gui.scale(4))


################################################################################
## Sizes
##
## These control the size of various things in the interface.


## The height of horizontal and width of vertical bars, scrollbars, and sliders.
define gui.bar_size = gui.scale(30)
define gui.scrollbar_size = gui.scale(10)
define gui.slider_size = gui.scale(30)

## The width of the thumb on a horizontal slider, and the height of the thumb
## on a vertical slider.
define gui.slider_thumb_size = gui.scale(10)


################################################################################
## Sizes
##
## The spacing used between various elements of the interface.

## The spacing between menu choices.
define gui.choice_spacing = gui.scale(22)

## Buttons in the navigation section of the main and game menus.
define gui.navigation_spacing = gui.scale(4)

## Preference buttons.
define gui.pref_spacing = gui.scale(0)

## The spacing between file page buttons.
define gui.page_spacing = gui.scale(0)


################################################################################
## Basic in-game styles.

style default:
    font gui.default_font
    size gui.text_size

style input:
    color gui.accent_color

style hyperlink_text:
    color gui.accent_color
    hover_color gui.hover_color
    hover_underline True


################################################################################
## Style common user interface components.

style button_text is gui_text
style check_button is button
style check_button_text is button_text
style radio_button is button
style radio_button_text is button_text
style medium_button is button
style medium_button_text is button_text
style small_button is button
style small_button_text is button_text
style label_text is gui_text
style prompt_text is gui_text

## Used for non-interactive text inside the gui.
style gui_text:
    font gui.interface_font
    color gui.interface_text_color
    size gui.text_size


## Used for the text of all buttons.
style button_text:
    size gui.interface_size
    color gui.idle_color
    insensitive_color gui.insensitive_color
    selected_color gui.selected_color
    hover_color gui.hover_color

## Used for full-sized buttons, like navigation buttons.
style button:
    padding gui.button_borders.padding
    background Frame("gui/button/[prefix_]background.png", gui.button_borders)

## Used for medium-sized buttons, like the sound test and mute buttons.
style medium_button:
    padding gui.medium_button_borders.padding
    background Frame("gui/button/medium/[prefix_]background.png", gui.medium_button_borders)

## Used for small-sized buttons, like the file page navigation buttons.
style small_button:
    padding gui.small_button_borders.padding
    background Frame("gui/button/small/[prefix_]background.png", gui.small_button_borders)

## Used for checkbox buttons in the preferences.
style check_button:
    padding gui.check_button_borders.padding
    background Frame("gui/button/check/[prefix_]background.png", gui.check_button_borders)

## Used for radio buttons in the preferences.
style radio_button:
    padding gui.radio_button_borders.padding
    background Frame("gui/button/radio/[prefix_]background.png", gui.radio_button_borders)


## Labels a portion of the interface.
style label_text:
    color gui.accent_color
    size gui.interface_size

## Asks the user a question in the interface.
style prompt_text:
    color gui.text_color
    size gui.interface_size


## Bars are used to display value data to the user.
style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left_bar.png", gui.bar_borders)
    right_bar Frame("gui/bar/right_bar.png", gui.bar_borders)

## Scrollbars are used to scroll viewports.
style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders)

## Sliders are used to adjust values.
style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders)
    thumb Frame("gui/slider/horizontal_[prefix_]thumb.png", gui.slider_borders, xsize=gui.slider_thumb_size)


## Vertical equivalents of bar, scrollbar, and slider.

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top_bar.png", gui.vbar_borders)
    bottom_bar Frame("gui/bar/bottom_bar.png", gui.vbar_borders)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders)

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders)
    thumb Frame("gui/slider/vertical_[prefix_]thumb.png", gui.vslider_borders, ysize=gui.slider_thumb_size)


## A frame that is intended to contain interface elements and make them usable
## outside of the menus.
style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders)


################################################################################
## Say

screen say(who, what):
    style_group "say"

    window:
        id "window"

        vbox:

            null height gui.scale(5)

            if who:
                text who id "who" xoffset gui.scale(-10)
            else:
                text " " id "who" xoffset gui.scale(-10)

            null height gui.scale(5)

            text what id "what"

    # If there's a side image, display it above the text. Do not display
    # on the phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0

style window is default
style say_label is default
style say_dialogue is default

style window:
    xalign 0.5
    xfill True
    xpadding gui.scale(268)
    yalign 1.0
    ysize gui.scale(185)

    background "gui/textbox.png"

style say_label:
    color gui.accent_color
    size gui.label_size

###############################################################################
## CTC


## This transform is also used by the skip screen, below.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat

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



################################################################################
## Input
##
## Screen that's used to display renpy.input()
##
## http://www.renpy.org/doc/html/screen_special.html#input
screen input(prompt):
    style_group "input"

    window:

        vbox:
            xsize gui.scale(744)
            xalign 0.5

            null height gui.scale(5)

            text " " style "say_label"

            null height gui.scale(5)

            text prompt style "input_prompt"

            input id "input"

style input_prompt is default


##############################################################################
## Choice
##
## Screen that's used to display in-game menus.
##
## http://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_group "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action

# Use the narrator to speak menu captions.
define config.narrator_menu = True

style choice_vbox is vbox
style choice_button is default
style choice_button_text is default

style choice_vbox:

    xalign 0.5
    ypos gui.scale(270)
    yanchor 0.5

    # Add some space between choices.
    spacing gui.choice_spacing

style choice_button is default:
    xsize gui.scale(790)
    padding gui.choice_borders.padding
    background Frame("gui/choice/[prefix_]background.png", gui.choice_borders)

style choice_button_text is default:
    color gui.choice_text_color
    hover_color gui.text_color

    # Center the text.
    xalign 0.5
    text_align 0.5
    layout "subtitle"

##############################################################################
## Nvl
##
## Screen used for nvl-mode dialogue and menus.
##
## http://www.renpy.org/doc/html/screen_special.html#nvl

screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.scale(10)

        vpgrid:
            cols 1
            yinitial 1.0

            # Display dialogue.
            for d in dialogue:

                window:
                    id d.window_id

                    has hbox:
                        yfill True
                        spacing gui.scale(20)

                    if d.who is not None:

                        text d.who:
                            id d.who_id

                    else:

                        text " ":
                            style "nvl_label"

                    text d.what:
                        id d.what_id

        # Displays the menu, if given. The menu may be displayed incorrectly
        # if config.narrator_menu is set to True, as it is above.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_menu_button"

    add SideImage() xalign 0.0 yalign 1.0

define config.nvl_list_length = 6

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_menu_button is button
style nvl_menu_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    xpadding gui.scale(240)
    top_padding gui.scale(10)
    bottom_padding gui.scale(20)

    background "gui/nvl.png"

style nvl_entry:
    xfill True
    ysize gui.scale(115)

style nvl_label:
    xmaximum gui.scale(150)
    min_width gui.scale(150)
    text_align 1.0

style nvl_dialogue:
    ypos gui.scale(7)

style nvl_menu_button:
    left_padding gui.scale(170)

style nvl_menu_button_text:
    insensitive_color gui.text_color



################################################################################
## Quick Menu

screen quick_menu():

    # Ensure this appears on top of other screens.
    zorder 100

    # Add an in-game quick menu.
    hbox:
        style_group "quick"

        xalign 0.5
        yalign 1.0

        textbutton _("Back") action Rollback()
        textbutton _("History") action ShowMenu('history')
        textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
        textbutton _("Auto") action Preference("auto-forward", "toggle")
        textbutton _("Save") action ShowMenu('save')
        textbutton _("Q.Save") action QuickSave()
        textbutton _("Q.Load") action QuickLoad()
        textbutton _("Prefs") action ShowMenu('preferences')

style quick_button is default
style quick_button_text is button_text

style quick_button:
    xpadding gui.scale(10)

style quick_button_text:
    size gui.tiny_size

init python:
    config.overlay_screens.append("quick_menu")


################################################################################
## Navigation
##
## This screen serves to navigate within the main and game menus.

screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.scale(40)
        xmaximum gui.scale(227)
        yalign 0.5

        spacing gui.navigation_spacing

        if main_menu:

            textbutton _("Start") action Start()

        else:

            textbutton _("History") action ShowMenu("history")

            textbutton _("Save") action ShowMenu("save")

        textbutton _("Load") action ShowMenu("load")

        textbutton _("Preferences") action ShowMenu("preferences")

        if _in_replay:

            textbutton _("End Replay") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Main Menu") action MainMenu()

        textbutton _("About") action ShowMenu("about")


        # Help seems to be unimportant on Android and iOS. The Quit button
        # is banned on iOS, and unnecessary in Android.
        if renpy.variant("pc"):

            textbutton _("Help") action ShowMenu("help")

            textbutton _("Quit") action Quit(confirm=not main_menu)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"

##############################################################################
## Main Menu
##
## Used to display the main menu when Ren'Py starts.
##
## http://www.renpy.org/doc/html/screen_special.html#main-menu
##
## This lays out the main menu and its backgrounds, but uses the navigation
## screen to actually supply the main menu buttons.

screen main_menu():

    # This ensures that any other menu screen is replaced.
    tag menu

    style_prefix "main_menu"

    add gui.main_menu_background

    # This empty frame darkens the main menu.
    frame:
        pass

    # The actual contents of the main menu are in the navigation screen, above.
    use navigation

    if gui.show_name:

        vbox:
            text "[config.name!t]":
                style "main_menu_title"

            text "[config.version]":
                style "main_menu_version"

## Should we show the name and version of the game?
define gui.show_name = True

style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize gui.scale(280)
    yfill True

    background "gui/overlay/main.png"

style main_menu_vbox:
    xalign 1.0
    xoffset gui.scale(-20)
    xmaximum gui.scale(800)
    yalign 1.0
    yoffset gui.scale(-20)

style main_menu_text:
    xalign 1.0

    layout "subtitle"
    text_align 1.0
    color gui.accent_color

style main_menu_title:
    size gui.title_size


##############################################################################
## Game Menu
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
## When used with children (the expected case), it transcludes those children
## in an hbox after the space reserved for navigation.

screen game_menu(title, scroll=None):

    # Add the backgrounds.
    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    style_prefix "game_menu"

    frame:
        style "game_menu_outer_frame"

        hbox:

            # Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial 1.0

                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("Return"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")

style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding gui.scale(30)
    top_padding gui.scale(120)

    background "gui/overlay/game.png"

style game_menu_navigation_frame:
    xsize gui.scale(280)
    yfill True

style game_menu_content_frame:
    left_margin gui.scale(40)
    right_margin gui.scale(20)
    top_margin gui.scale(10)

style game_menu_viewport:
    xsize gui.scale(920)

style game_menu_vscrollbar:
    unscrollable "hide"

style game_menu_side:
    spacing gui.scale(10)

style game_menu_label:
    xpos gui.scale(50)
    ysize gui.scale(120)

style game_menu_label_text:
    size gui.title_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.scale(40)
    xmaximum gui.scale(227)
    yalign 1.0
    yoffset gui.scale(-30)

screen file_slots(title):

    default page_name_value = FilePageNameInputValue()

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter
            ## event before any of the buttons do.
            order_reverse True

            # The page name, which can be edited by clicking on a button.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        add FileScreenshot(slot)

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            hbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                spacing gui.page_spacing

                textbutton _("<") action FilePagePrevious()

                textbutton _("{#auto_page}A") action FilePage("auto")

                textbutton _("{#quick_page}Q") action FilePage("quick")

                # range(1, 10) gives the numbers from 1 to 9.
                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)

                textbutton _(">") action FilePageNext()

screen load():

    tag menu

    use file_slots(_("Load"))

screen save():

    tag menu

    use file_slots(_("Save"))

define config.thumbnail_width = gui.scale(256)
define config.thumbnail_height = gui.scale(144)
define gui.file_slot_cols = 3
define gui.file_slot_rows = 2

style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_small_button
style page_button_text is gui_small_button_text

style slot_button is empty
style slot_text is gui_button_text
style slot_time_text is slot_text
style slot_name_text is slot_text

style page_label:
    xpadding gui.scale(50)
    ypadding gui.scale(3)

style page_label_text:
    text_align 0.5
    layout "subtitle"

style slot_button:
    background "gui/idle_file_slot.png"
    hover_background "gui/hover_file_slot.png"

    # Note that xsize and ysize include the margins.

    xsize gui.scale(296)
    xpadding gui.scale(10)
    xmargin gui.scale(10)

    ysize gui.scale(226)
    ypadding gui.scale(10)
    ymargin gui.scale(5)

style slot_text:
    xalign 0.5

    color gui.idle_small_color
    layout "subtitle"
    size gui.tiny_size
    text_align 0.5

style slot_time_text:
    ypos gui.scale(146)

style slot_name_text:
    ypos gui.scale(164)


screen preferences():

    tag menu

    if renpy.mobile:
        $ cols = 2
    else:
        $ cols = 4

    use game_menu(_("Preferences"), scroll="viewport"):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc"):

                    vbox:
                        style_prefix "radio_pref"
                        label _("Display")
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "radio_pref"
                    label _("Rollback Side")
                    textbutton _("Disable") action Preference("rollback side", "disable")
                    textbutton _("Left") action Preference("rollback side", "left")
                    textbutton _("Right") action Preference("rollback side", "right")

                vbox:
                    style_prefix "check_pref"
                    label _("Skip")
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

            null height gui.scale(50)

            hbox:
                style_prefix "slider_pref"
                box_wrap True

                vbox:

                    label _("Text Speed")

                    bar value Preference("text speed")

                    label _("Auto-Forward Time")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("Music Volume")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Sound Volume")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Voice Volume")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)

                    textbutton _("Mute All"):
                        action Preference("all mute", "toggle")
                        style "mute_all_pref_button"


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_pref_label is pref_label
style radio_pref_label_text is pref_label_text
style radio_pref_button is gui_radio_button
style radio_pref_button_text is gui_radio_button_text
style radio_pref_vbox is pref_vbox

style check_pref_label is pref_label
style check_pref_label_text is pref_label_text
style check_pref_button is gui_check_button
style check_pref_button_text is gui_check_button_text
style radio_pref_vbox is pref_vbox

style slider_pref_label is pref_label
style slider_pref_label_text is pref_label_text
style slider_pref_slider is gui_slider
style slider_pref_button is gui_medium_button
style slider_pref_button_text is gui_medium_button_text
style slider_pref_vbox is pref_vbox

style mute_all_pref_button is gui_medium_button
style mute_all_pref_button_text is gui_medium_button_text

# Used for preferences that describe choices.
style pref_label:
    ysize gui.scale(30)

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize gui.scale(230)

style radio_pref_vbox:
    spacing gui.pref_spacing

style radio_pref_button:
    size_group "preferences"

style check_pref_vbox:
    spacing gui.pref_spacing

style check_pref_button:
    size_group "preferences"

# Used for preferences controlled by sliders.
style slider_pref_slider:
    xsize gui.scale(350)

style slider_pref_label:
    top_margin gui.scale(10)
    bottom_margin gui.scale(3)

# Used for buttons associated with bars - the test buttons.
style slider_pref_button:
    yalign 1.0
    left_margin gui.scale(10)

# Used for the "Mute All" button.
style mute_all_pref_button:
    top_margin gui.scale(10)

style slider_pref_vbox:
    xsize gui.scale(460)


##############################################################################
## History

screen history():

    tag menu

    # Avoid predicting this screen. It's big, and all the images should be
    # predicted by one of the other screens.
    predict False

    use game_menu(_("History"), scroll="vpgrid"):

        style_prefix "history"

        for h in _history_list:

            window:
                has hbox:
                    yfill True
                    spacing gui.scale(20)

                    text (h.who or " "):
                        style "history_who"

                        # Take the color of the who text from the
                        # Character, if set.
                        if "color" in h.who_args:
                            color h.who_args["color"]

                text h.what

        if not _history_list:
            label _("The dialogue history is empty.")


define config.history_length = 250

style history_window is empty
style history_who is say_label
style history_text is gui_text
style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.scale(140)

style history_who:
    xmaximum gui.scale(150)
    min_width gui.scale(150)
    text_align 1.0

style history_text:
    ypos gui.scale(7)

style history_label:
    xfill True

style history_label_text:
    xalign 0.5

##############################################################################
## Confirm
##
## Screen that asks the user a yes or no question.
##
## http://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while the confirm screen is
    ## being displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing gui.scale(30)

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing gui.scale(100)

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    ## Right-click and escape answer "no".
    key "game_menu" action no_action


define config.quit_action = Quit()

style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    xalign .5
    xsize gui.scale(600)
    xpadding gui.scale(75)

    yalign .5
    ysize gui.scale(250)
    ypadding gui.scale(50)


style confirm_prompt_text:
    text_align 0.5
    layout "subtitle"

style confirm_button:
    size_group "confirm"

style confirm_button_text:
    xalign 0.5


##############################################################################
## About
##
## A screen that gives copyright information about the game and Ren'Py.
screen about():

    tag menu

    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            ## gui.about is usually set in options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")

define gui.about = ""

style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_size


##############################################################################
## Help
##
## A screen that gives information about key and mouse bindings.
screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Help"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing gui.scale(15)

            hbox:

                textbutton _("Keyboard") action SetScreenVariable("device", "keyboard")
                textbutton _("Mouse") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help

screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Space")
        text _("Advances dialogue without selecting choices.")

    hbox:
        label _("Arrow Keys")
        text _("Navigates the interface.")

    hbox:
        label _("Escape")
        text _("Accesses the game menu.")

    hbox:
        label _("Ctrl")
        text _("Skips dialogue while held down.")

    hbox:
        label _("Tab")
        text _("Toggles dialogue skipping.")

    hbox:
        label _("Page Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Page Down")
        text _("Rolls forward to later dialogue.")

    hbox:
        label "H"
        text _("Hides the user interface.")

    hbox:
        label "S"
        text _("Takes a screenshot.")

    hbox:
        label "V"
        text _("Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}.")

screen mouse_help():

    hbox:
        label _("Left Click")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Middle Click")
        text _("Hides the user interface.")

    hbox:
        label _("Right Click")
        text _("Accesses the game menu.")

    hbox:
        label _("Mouse Wheel Up\nClick Rollback Side")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Mouse Wheel Down")
        text _("Rolls forward to later dialogue.")

screen gamepad_help():

    hbox:
        label _("Right Trigger\nA/Bottom Button")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label ("Left Trigger\nLeft Shoulder")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Right Shoulder")
        text _("Rolls forward to later dialogue.")

    hbox:
        label _("D-Pad, Sticks")
        text _("Navigates the interface.")

    hbox:
        label _("Start, Guide")
        text _("Accesses the game menu.")

    hbox:
        label _("Y/Top Button")
        text _("Hides the user interface.")

    textbutton _("Calibrate") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    xmargin gui.scale(8)

style help_label:
    xsize gui.scale(250)
    right_padding gui.scale(20)

style help_label_text:
    size gui.text_size
    xalign 1.0
    text_align 1.0

##############################################################################
# Skip Indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing gui.scale(6)

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.scale(10)
    ypadding gui.scale(5)
    left_padding gui.scale(16)
    right_padding gui.scale(40)

    background Frame("gui/skip.png", gui.scale(16), gui.scale(5), gui.scale(50), gui.scale(5))

style skip_text:
    size gui.notify_size

style skip_triangle:
    # We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    # glyph in it.
    font gui.glyph_font


################################################################################
## Message notification.

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text message

    # This controls how long it takes between when the screen is
    # first shown, and when it begins hiding.
    timer 3.25 action Hide('notify')

transform notify_appear:
    # These control the actions on show and hide.
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0

style notify_frame is empty
style notify_text is gui_text

style notify_frame:
        background Frame("gui/notify.png", gui.scale(16), gui.scale(5), gui.scale(50), gui.scale(5))

        left_padding gui.scale(16)
        right_padding gui.scale(40)

        ypos gui.scale(45)
        ypadding gui.scale(5)

style notify_text:
    size gui.notify_size

################################################################################
## Tablet variants.

style pref_vbox:
    variant "medium"
    xsize gui.scale(460)

screen quick_menu():
    variant "touch"

    # Ensure this appears on top of other screens.
    zorder 100

    # Add an in-game quick menu.
    hbox:
        style_group "quick"

        xalign 0.5
        yalign 1.0

        textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
        textbutton _("Menu") action ShowMenu()
        textbutton _("Auto") action Preference("auto-forward", "toggle")

style quick_button:
    variant "touch"

    xpadding gui.scale(60)
    top_padding gui.scale(14)

################################################################################
## Phone Variant

init python:

    if renpy.variant("small"):
        gui.text_size = gui.scale(30)
        gui.notify_size = gui.scale(25)
        gui.interface_size = gui.scale(36)
        gui.label_size = gui.scale(36)

        gui.file_slot_cols = 2
        gui.file_slot_rows = 2

        gui.slider_size = gui.scale(44)
        gui.thumb_size = gui.scale(15)

style window:
    variant "small"
    xpadding gui.scale(90)
    ysize gui.scale(240)
    background "gui/phone/textbox.png"

style choice_button:
    variant "small"
    xsize gui.scale(1190)
    xpadding gui.scale(100)
    ypadding gui.scale(8)

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"
    xpadding gui.scale(120)

style nvl_entry:
    variant "small"
    ysize gui.scale(170)

style nvl_dialogue:
    variant "small"
    ypos gui.scale(6)

style quick_button_text:
    variant "small"
    size gui.scale(20)

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game.png"

style game_menu_navigation_frame:
    variant "small"
    xsize gui.scale(340)

style game_menu_content_frame:
    variant "small"
    top_margin 0

style navigation_vbox:
    variant "small"
    xsize gui.scale(334)

style pref_vbox:
    variant "small"
    xsize gui.scale(400)

style slider_pref_vbox:
    variant "small"
    xsize None

style slider_pref_slider:
    variant "small"
    xsize gui.scale(600)

style history_window:
    variant "small"
    ysize gui.scale(190)

style history_who:
    variant "small"
    xmaximum gui.scale(150)
    min_width gui.scale(150)
    text_align 1.0
    size gui.text_size

style history_text:
    variant "small"
    ypos gui.scale(4)
    size gui.scale(25)

style history_label:
    variant "small"
    xfill True

style history_label_text:
    variant "small"
    xalign 0.5

style confirm_frame:
    variant "small"
    xsize gui.scale(844)
    ysize gui.scale(475)

style notify_frame:
    variant "small"
    ypos gui.scale(55)

