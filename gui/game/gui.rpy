################################################################################
## Sizes
##
## These will need to be changed if you change the size of the game. Remember
## to click "Window" in preferences to ensure the window itself is resized.

init offset = -1

init python:
    gui.init(1280, 720)

################################################################################
## Colors
##
## The colors of various aspects of the interface.

## An accent color used throughout the interface.
define gui.ACCENT_COLOR = "#00b8c3"

## A version of the accent color that's used when buttons are hovered.
define gui.HOVER_COLOR = Color(gui.ACCENT_COLOR).tint(.6)

## The color used for a text button when it is selected but not focused.
## A button is selected if it is the current screen or preference value
define gui.SELECTED_COLOR = "#ffffff"

## The color used for a text button when it is neither selected nor hovered.
define gui.IDLE_COLOR = "#555555"

## The small color is used for small buttons, which need to be brighter/darker
## to achieve the same effect.
define gui.IDLE_SMALL_COLOR = "#aaaaaa"

## The color used for a text button when it cannot be selected.
define gui.INSENSITIVE_COLOR = "#55555580"

## The color used for dialogue and menu choice text.
define gui.TEXT_COLOR = "#ffffff"
define gui.CHOICE_COLOR = "#cccccc"

## The images used for the main and game menus.
define gui.MAIN_MENU_BACKGROUND = "gui/main_menu.png"
define gui.GAME_MENU_BACKGROUND = "gui/game_menu.png"


################################################################################
## Fonts and Font Sizes

define gui.DEFAULT_FONT = "DejaVuSans.ttf"
define gui.INTERFACE_FONT = "DejaVuSans.ttf"
define gui.GLYPH_FONT = "DejaVuSans.ttf"

define gui.TINY_SIZE = gui.scale(14)
define gui.NOTIFY_SIZE = gui.scale(16)
define gui.TEXT_SIZE = gui.scale(22)
define gui.INTERFACE_SIZE = gui.scale(24)
define gui.LABEL_SIZE = gui.scale(30)
define gui.TITLE_SIZE = gui.scale(50)


################################################################################
## Window icon.

## This is the icon displayer on the taskbar or dock.
define config.window_icon = "gui/window_icon.png"


################################################################################
## Padding and Spacing

## This is the default amout of padding that is used by gui.Frame, and
## styles that use gui.Frame.

define gui.LEFT_PADDING = gui.scale(4)
define gui.RIGHT_PADDING = gui.scale(4)
define gui.TOP_PADDING = gui.scale(4)
define gui.BOTTOM_PADDING = gui.scale(4)

## These override the horizontal padding for check and radio buttons.

define gui.CHECKBOX_LEFT_PADDING = gui.scale(25)
define gui.CHECKBOX_RIGHT_PADDING = gui.scale(4)

## If True, gui.Frames will use tiling, rather than scaling.

define gui.TILE_FRAME = False

## The spacing between groups of buttons and labels.

define gui.NAVIGATION_SPACING = gui.scale(4)
define gui.PREF_SPACING = gui.scale(0)
define gui.PAGE_SPACING = gui.scale(0)


define gui.BAR_SIZE = gui.scale(30)
define gui.SLIDER_SIZE = gui.scale(30)
define gui.SLIDER_THUMB_SIZE = gui.scale(10)
define gui.SCROLLBAR_SIZE = gui.scale(10)


################################################################################
## Basic in-game styles.

style default:
    font gui.DEFAULT_FONT
    size gui.TEXT_SIZE

style input:
    color gui.ACCENT_COLOR

style hyperlink_text:
    color gui.ACCENT_COLOR
    hover_color gui.HOVER_COLOR
    hover_underline True


################################################################################
## Padding style mix-ins.

## These can be taken by other styles to add appropriate amount of padding
## to frames and other components.

style padding:
    left_padding gui.LEFT_PADDING
    right_padding gui.RIGHT_PADDING
    top_padding gui.TOP_PADDING
    bottom_padding gui.BOTTOM_PADDING

style checkbox_padding:
    left_padding gui.CHECKBOX_LEFT_PADDING
    right_padding gui.CHECKBOX_RIGHT_PADDING
    top_padding gui.TOP_PADDING
    bottom_padding gui.BOTTOM_PADDING


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

## Used for text inside the gui.
style gui_text:
    font gui.INTERFACE_FONT
    size gui.TEXT_SIZE

## Used for full-sized buttons, like navigation buttons.
style button:
    take padding

    background gui.Frame("gui/button/idle.png")
    hover_background gui.Frame("gui/button/hover.png")
    selected_background gui.Frame("gui/button/selected_idle.png")
    selected_hover_background gui.Frame("gui/button/selected_hover.png")

style button_text:
    size gui.INTERFACE_SIZE
    color gui.IDLE_COLOR
    insensitive_color gui.INSENSITIVE_COLOR
    selected_color gui.SELECTED_COLOR
    hover_color gui.HOVER_COLOR
    selected_hover_color gui.HOVER_COLOR

## Used for checkbox-like buttons
style check_button:
    take checkbox_padding

    background gui.Frame("gui/button/check/idle.png")
    hover_background gui.Frame("gui/button/check/hover.png")
    selected_background gui.Frame("gui/button/check/selected_idle.png")
    selected_hover_background gui.Frame("gui/button/check/selected_hover.png")

style radio_button:
    take checkbox_padding

    background gui.Frame("gui/button/radio/idle.png")
    hover_background gui.Frame("gui/button/radio/hover.png")
    selected_background gui.Frame("gui/button/radio/selected_idle.png")
    selected_hover_background gui.Frame("gui/button/radio/selected_hover.png")

style medium_button:

    background gui.Frame("gui/button/medium/idle.png")
    hover_background gui.Frame("gui/button/medium/hover.png")
    selected_background gui.Frame("gui/button/medium/selected_idle.png")
    selected_hover_background gui.Frame("gui/button/medium/selected_hover.png")

style small_button:
    left_padding gui.scale(10) + gui.LEFT_PADDING
    right_padding gui.scale(10) + gui.RIGHT_PADDING

    background gui.Frame("gui/button/medium/idle.png")
    hover_background gui.Frame("gui/button/medium/hover.png")
    selected_background gui.Frame("gui/button/medium/selected_idle.png")
    selected_hover_background gui.Frame("gui/button/medium/selected_hover.png")

style label_text:
    color gui.ACCENT_COLOR
    size gui.INTERFACE_SIZE

style prompt_text:
    color gui.TEXT_COLOR
    size gui.INTERFACE_SIZE

style bar:
    ysize gui.BAR_SIZE

    left_bar gui.Frame("gui/bar/left.png")
    right_bar gui.Frame("gui/bar/right.png")

style scrollbar:
    ysize gui.SCROLLBAR_SIZE

    left_bar gui.Frame("gui/scrollbar/horizontal_idle.png")
    thumb gui.Frame("gui/scrollbar/horizontal_idle_thumb.png", xsize=gui.SLIDER_THUMB_SIZE)
    right_bar gui.Frame("gui/scrollbar/horizontal_idle.png")

    hover_left_bar gui.Frame("gui/scrollbar/horizontal_hover.png")
    hover_thumb gui.Frame("gui/scrollbar/horizontal_hover_thumb.png", xsize=gui.SLIDER_THUMB_SIZE)
    hover_right_bar gui.Frame("gui/scrollbar/horizontal_hover.png")


style slider:
    ysize gui.SLIDER_SIZE

    left_bar gui.Frame("gui/slider/horizontal_idle.png")
    thumb gui.Frame("gui/slider/horizontal_idle_thumb.png")
    right_bar gui.Frame("gui/slider/horizontal_idle.png")

    hover_left_bar gui.Frame("gui/slider/horizontal_hover.png")
    hover_thumb gui.Frame("gui/slider/horizontal_hover_thumb.png")
    hover_right_bar gui.Frame("gui/slider/horizontal_hover.png")

style vbar:
    xsize gui.BAR_SIZE

    bar_vertical True
    left_bar gui.Frame("gui/bar/top.png")
    right_bar gui.Frame("gui/bar/bottom.png")

style vscrollbar:
    xsize gui.SCROLLBAR_SIZE
    bar_vertical True
    bar_invert True

    left_bar gui.Frame("gui/scrollbar/vertical_idle.png")
    thumb gui.Frame("gui/scrollbar/vertical_idle_thumb.png")
    right_bar gui.Frame("gui/scrollbar/vertical_idle.png")

    hover_left_bar gui.Frame("gui/scrollbar/vertical_hover.png")
    hover_thumb gui.Frame("gui/scrollbar/vertical_hover_thumb.png")
    hover_right_bar gui.Frame("gui/scrollbar/vertical_hover.png")

style vslider:
    xsize gui.SLIDER_SIZE
    bar_vertical True

    left_bar gui.Frame("gui/slider/vertical_idle.png")
    thumb gui.Frame("gui/slider/vertical_idle_thumb.png", ysize=gui.SLIDER_THUMB_SIZE)
    right_bar gui.Frame("gui/slider/vertical_idle.png")

    hover_left_bar gui.Frame("gui/slider/vertical_hover.png")
    hover_thumb gui.Frame("gui/slider/vertical_hover_thumb.png", ysize=gui.SLIDER_THUMB_SIZE)
    hover_right_bar gui.Frame("gui/slider/vertical_hover.png")

style frame:
    take padding
    background gui.Frame("gui/frame.png")


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
    color gui.ACCENT_COLOR
    size gui.LABEL_SIZE

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
    color gui.ACCENT_COLOR
    font gui.GLYPH_FONT



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
    spacing gui.scale(22)

style choice_button is default:
    background gui.Frame("gui/choice/idle.png")
    hover_background gui.Frame("gui/choice/hover.png")

    xsize gui.scale(790)
    xpadding gui.scale(100)
    ypadding gui.scale(5)

style choice_button_text is default:
    color gui.CHOICE_COLOR
    hover_color gui.TEXT_COLOR

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
    insensitive_color gui.TEXT_COLOR



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
style quick_button_text is default

style quick_button:
    xpadding gui.scale(10)

style quick_button_text:
    size gui.TINY_SIZE

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

        spacing gui.NAVIGATION_SPACING

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

    add gui.MAIN_MENU_BACKGROUND

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
    color gui.ACCENT_COLOR

style main_menu_title:
    size gui.TITLE_SIZE


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
        add gui.MAIN_MENU_BACKGROUND
    else:
        add gui.GAME_MENU_BACKGROUND

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
    size gui.TITLE_SIZE
    color gui.ACCENT_COLOR
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

                spacing gui.PAGE_SPACING

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

    color gui.IDLE_SMALL_COLOR
    layout "subtitle"
    size gui.TINY_SIZE
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
    spacing gui.PREF_SPACING

style radio_pref_button:
    size_group "preferences"

style check_pref_vbox:
    spacing gui.PREF_SPACING

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

    modal True

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

    # Right-click and escape answer "no".
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
    size gui.LABEL_SIZE


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
    size gui.TEXT_SIZE
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
    size gui.NOTIFY_SIZE

style skip_triangle:
    # We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    # glyph in it.
    font gui.GLYPH_FONT


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
    size gui.NOTIFY_SIZE

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
        gui.TEXT_SIZE = gui.scale(30)
        gui.NOTIFY_SIZE = gui.scale(25)
        gui.INTERFACE_SIZE = gui.scale(36)
        gui.LABEL_SIZE = gui.scale(36)

        gui.file_slot_cols = 2
        gui.file_slot_rows = 2

        gui.SLIDER_SIZE = gui.scale(44)
        gui.THUMB_SIZE = gui.scale(15)

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
    size gui.TEXT_SIZE

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

