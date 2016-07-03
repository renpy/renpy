################################################################################
## Initialization
##
## The offset ensures that these statements run before all others, while the
## gui.init statement initializes the gui, and sets the width and height of
## the game window.

init offset = -1

init python:
    gui.init(1920, 1080)


################################################################################
## Colors
##
## The colors of text in the interface.

## An accent color used throughout the interface to label and highlight text.
define gui.accent_color = '#000060'

## The color used for a text button when it is neither selected nor hovered.
define gui.idle_color = '#606060'

## The small color is used for small buttons, which need to be brighter/darker
## to achieve the same effect.
define gui.idle_small_color = '#404040'

## A version of the accent color that's used when buttons are hovered.
define gui.hover_color = '#3284d6'

## The color used for a text button when it is selected but not focused. A
## button is selected if it is the current screen or preference value
define gui.selected_color = '#000060'

## The color used for a text button when it cannot be selected.
define gui.insensitive_color = '#8888887f'

## Colors used for the portions of bars that are not filled in. These are not
## used directly, but are used when re-generating bar image files.
define gui.muted_color = '#6080d0'
define gui.hover_muted_color = '#8080f0'

## The colors used for dialogue and menu choice text.
define gui.text_color = '#402000'
define gui.interface_text_color = '#404040'
define gui.choice_idle_color = "#cccccc"
define gui.choice_hover_color = "#0066cc"


################################################################################
## Images


## The images used for the main and game menus.
define gui.main_menu_background = "gui/main_menu.png"
define gui.game_menu_background = "gui/game_menu.png"


################################################################################
## Fonts and Font Sizes

define gui.default_font = "ArchitectsDaughter.ttf"
define gui.interface_font = "ArchitectsDaughter.ttf"
define gui.quick_button_font = "ArchitectsDaughter.ttf"
define gui.glyph_font = "DejaVuSans.ttf"

define gui.notify_text_size = 24
define gui.text_size = 33
define gui.interface_text_size = 36
define gui.label_text_size = 45
define gui.title_size = 75

define gui.button_text_size = 30
define gui.medium_button_text_size = 30
define gui.small_button_text_size = 36
define gui.quick_button_text_size = 21
define gui.slot_text_size = 21


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
define gui.button_borders = Borders(20, 20, 20, 20, tile=True)
define gui.medium_button_borders = Borders(20, 20, 30, 20, tile=True)
define gui.small_button_borders = Borders(20, 20, 30, 20, tile=True)
define gui.check_button_borders = Borders(45, 20, 20, 20, tile=True)
define gui.radio_button_borders = Borders(45, 20, 20, 20, tile=True)
define gui.quick_button_borders = Borders(15, 6, 15, 0)
define gui.slot_borders = Borders(15, 15, 15, 15)

## Choice buttons used by the menu statement.
define gui.choice_borders = Borders(150, 8, 150, 8)

## Bars, scrollbars, and sliders.
define gui.bar_borders = Borders(6, 6, 6, 6)
define gui.scrollbar_borders = Borders(6, 6, 6, 6)
define gui.slider_borders = Borders(6, 6, 6, 6)
define gui.vbar_borders = Borders(6, 6, 6, 6)
define gui.vscrollbar_borders = Borders(6, 6, 6, 6)
define gui.vslider_borders = Borders(6, 6, 6, 6)

## Frames.
define gui.frame_borders = Borders(6, 6, 6, 6)
define gui.namebox_borders = Borders(75, 6, 75, 6)


################################################################################
## Sizes
##
## These control the size of various things in the interface.


## The height of horizontal and width of vertical bars, scrollbars, and
## sliders.
define gui.bar_size = 54
define gui.scrollbar_size = 18
define gui.slider_size = 45

## The widths and heights of various buttons. Setting these to None allows
## Ren'Py to choose a width or height.
define gui.button_width = 350
define gui.medium_button_width = None
define gui.small_button_width = None
define gui.quick_button_width = None
define gui.slot_width = 414

define gui.button_height = 64
define gui.medium_button_height = 55
define gui.small_button_height = 64
define gui.quick_button_height = 45
define gui.slot_height = 309


################################################################################
## Sizes
##
## The spacing used between various elements of the interface.

## The spacing between menu choices.
define gui.choice_spacing = 33

## Buttons in the navigation section of the main and game menus.
define gui.navigation_spacing = 0

## Preference buttons.
define gui.pref_spacing = 0

## The spacing between file page buttons.
define gui.page_spacing = 0

## The spacing between file slots.
define gui.slot_spacing = 15

################################################################################
## Basic in-game styles.

style default:
    font gui.default_font
    size gui.text_size
    color gui.text_color

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
    size gui.interface_text_size

## Used for the text of all buttons.
style button_text:
    yalign 0.5
    size gui.button_text_size
    color gui.idle_color
    insensitive_color gui.insensitive_color
    selected_color gui.selected_color
    hover_color gui.hover_color

## Used for full-sized buttons, like navigation buttons.
style button:
    padding gui.button_borders.padding
    background Frame("gui/button/[prefix_]background.png", gui.button_borders)
    xsize gui.button_width
    ysize gui.button_height

## Used for medium-sized buttons, like the sound test and mute buttons.
style medium_button:
    padding gui.medium_button_borders.padding
    background Frame([ "gui/button/medium_[prefix_]background.png", "gui/button/[prefix_]background.png" ], gui.medium_button_borders)
    xsize gui.medium_button_width
    ysize gui.medium_button_height

style medium_button_text:
    size gui.medium_button_text_size

## Used for small-sized buttons, like the file page navigation buttons.
style small_button:
    padding gui.small_button_borders.padding
    background Frame([ "gui/button/small_[prefix_]background.png", "gui/button/[prefix_]background.png" ], gui.small_button_borders)
    xsize gui.medium_button_width
    ysize gui.medium_button_height

style small_button_text:
    size gui.medium_button_text_size

## Used for checkbox buttons in the preferences.
style check_button:
    padding gui.check_button_borders.padding
    background Frame([ "gui/button/check_[prefix_]background.png", "gui/button/[prefix_]background.png" ], gui.check_button_borders)
    foreground "gui/button/check_[prefix_]foreground.png"

## Used for radio buttons in the preferences.
style radio_button:
    padding gui.radio_button_borders.padding
    background Frame([ "gui/button/radio_[prefix_]background.png", "gui/button/[prefix_]background.png" ], gui.radio_button_borders)
    foreground "gui/button/check_[prefix_]foreground.png"


## Labels a portion of the interface.
style label_text:
    color gui.accent_color
    size gui.interface_text_size

## Asks the user a question in the interface.
style prompt_text:
    color gui.text_color
    size gui.interface_text_size


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
    thumb "gui/slider/horizontal_[prefix_]thumb.png"


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
    thumb "gui/slider/vertical_[prefix_]thumb.png"


## A frame that is intended to contain interface elements and make them usable
## outside of the menus.
style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders)


################################################################################
## Say
##
## The say screen is used to display dialogue to the player. It take two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if
## no name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):
    style_group "say"

    window:
        id "window"

        vbox:
            xfill True

            null height 8

            if (who is not None) and gui.two_window:

                window:
                    style "namebox"
                    text who id "who"

            elif who is not None:

                text who id "who" xoffset -15

            else:

                text " " id "who" xoffset -15

            null height 8

            text what id "what"

    # If there's a side image, display it above the text. Do not display
    # on the phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


## A flag used by the say screen to determine if it should show the
## character's name in a second window.
define gui.two_window = False


style window is default
style say_label is default
style say_dialogue is default

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    xpadding 402
    yalign 1.0
    ysize 278

    background "gui/textbox.png"

style say_label:
    color gui.accent_color
    size gui.label_text_size

style namebox:
    xalign 0.5
    yoffset -33

    padding gui.namebox_borders.padding
    background Frame("gui/namebox.png", gui.namebox_borders)


################################################################################
## Input
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## http://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_group "input"

    window:

        vbox:
            xsize 1116
            xalign 0.5

            null height 8

            text " " style "say_label"

            null height 8

            text prompt style "input_prompt"

            input id "input"


style input_prompt is default


##############################################################################
## Choice
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with
## caption and action fields.
##
## http://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_group "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


## When this is true, labels will spoken by the narrator rather then displayed
## as empty buttons.
define config.narrator_menu = True


style choice_vbox is vbox
style choice_button is default
style choice_button_text is default

style choice_vbox:

    xalign 0.5
    ypos 405
    yanchor 0.5

    # Add some space between choices.
    spacing gui.choice_spacing

style choice_button is default:
    xsize 1185
    padding gui.choice_borders.padding
    background Frame("gui/choice/[prefix_]background.png", gui.choice_borders)

style choice_button_text is default:
    color gui.choice_idle_color
    hover_color gui.choice_hover_color

    # Center the text.
    xalign 0.5
    text_align 0.5
    layout "subtitle"


##############################################################################
## Nvl
##
## This screen is used for NVL-mode dialogue and menus.
##
## http://www.renpy.org/doc/html/screen_special.html#nvl

screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing 15

        vpgrid:
            cols 1
            yinitial 1.0

            # Display dialogue.
            for d in dialogue:

                window:
                    id d.window_id

                    has hbox:
                        yfill True
                        spacing 30

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


## This controls the maximum number of NVL-mode entries that can be displayed
## at once.
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

    xpadding 360
    top_padding 15
    bottom_padding 30

    background "gui/nvl.png"

style nvl_entry:
    xfill True
    ysize 173

style nvl_label:
    xmaximum 225
    min_width 225
    text_align 1.0

style nvl_dialogue:
    ypos 11

style nvl_menu_button:
    left_padding 255

style nvl_menu_button_text:
    insensitive_color gui.text_color


################################################################################
## Quick Menu
##
## The quick menu is displayed in-game to provide easy access to the out-of-
## game menus.

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


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
init python:
    config.overlay_screens.append("quick_menu")


style quick_button is default
style quick_button_text is button_text

style quick_button:
    padding gui.quick_button_borders.padding
    background Frame("gui/button/quick_[prefix_]background.png",  gui.quick_button_borders)
    xsize gui.quick_button_width
    ysize gui.quick_button_height

style quick_button_text:
    font gui.quick_button_font
    size gui.quick_button_text_size


################################################################################
## Navigation
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

screen navigation():

    vbox:
        style_prefix "navigation"

        xpos 60
        xmaximum 341
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

        if renpy.variant("pc"):

            ## Help isn't necessary or relevant to mobile devices.
            textbutton _("Help") action ShowMenu("help")

            ## The quit button is banned on iOS and unnecessary on Android.
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

screen main_menu():

    # This ensures that any other menu screen is replaced.
    tag menu

    style_prefix "main_menu"

    add gui.main_menu_background

    # This empty frame darkens the main menu.
    frame:
        pass

    ## The use statement includes another screen inside this one. The actual
    ## contents of the main menu are in the navigation screen.
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
    xsize 420
    yfill True

    background "gui/overlay/main_menu.png"

style main_menu_vbox:
    xalign 1.0
    xoffset -30
    xmaximum 1200
    yalign 1.0
    yoffset -30

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
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid". When
## this screen is used, a child given to this screen is included inside it.

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
    bottom_padding 45
    top_padding 180

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin 60
    right_margin 30
    top_margin 15

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable "hide"

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 75
    ysize 180

style game_menu_label_text:
    size gui.title_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos 60
    xmaximum 341
    yalign 1.0
    yoffset -45


##############################################################################
## About
##
## This screen gives credit and copyright information about the game and
## Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            ## gui.about is usually set in options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


## This can be set in options.rpy to add text to the about screen.
define gui.about = ""


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


##############################################################################
## Load and Save Screens
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are
## implemented in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save
## https://www.renpy.org/doc/html/screen_special.html#load

screen file_slots(title):

    default page_name_value = FilePageNameInputValue()

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter event before any of
            ## the buttons do.
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

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

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


screen save():

    tag menu

    use file_slots(_("Save"))


screen load():

    tag menu

    use file_slots(_("Load"))


## The width and height of the thumbnails used by the save slots.
define config.thumbnail_width = 384
define config.thumbnail_height = 216

## The layout of the save slots.
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
    xpadding 75
    ypadding 5

style page_label_text:
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style slot_button:
    xsize gui.slot_width
    ysize gui.slot_height
    padding gui.slot_borders.padding

    background "gui/slot/[prefix_]background.png"

style slot_text:
    xalign 0.5

    color gui.idle_small_color
    layout "subtitle"
    size gui.slot_text_size
    text_align 0.5


##############################################################################
## Preferences
##
## The preferences screen allows the player to configure the game to better
## suit themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

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

                ## Additional vboxes of type "radio_pref" or "check_pref" can
                ## be added here, to add additional creator-defined
                ## preferences.

            null height 75

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

style pref_label:
    top_margin 15
    bottom_margin 5

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_pref_vbox:
    spacing gui.pref_spacing

style radio_pref_button:
    size_group "preferences"

style check_pref_vbox:
    spacing gui.pref_spacing

style check_pref_button:
    size_group "preferences"

style slider_pref_slider:
    xsize 525

style slider_pref_label:
    top_margin 15
    bottom_margin 5

style slider_pref_button:
    yalign 1.0
    left_margin 15

style slider_pref_vbox:
    xsize 675


##############################################################################
## History
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

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
                    spacing 30

                    text (h.who or " "):
                        style "history_who"

                        # Take the color of the who text from the
                        # Character, if set.
                        if "color" in h.who_args:
                            color h.who_args["color"]

                text h.what

        if not _history_list:
            label _("The dialogue history is empty.")


## The number of blocks of dialogue history Ren'Py will keep.
define config.history_length = 250


style history_window is empty
style history_who is say_label
style history_text is gui_text
style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize 210

style history_who:
    xmaximum 225
    min_width 225
    text_align 1.0

style history_text:
    ypos 11

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


##############################################################################
## Confirm
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or
## no question.
##
## http://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    ## Right-click and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    xalign .5
    xsize 900
    yalign .5
    ysize 375

style confirm_prompt_text:
    text_align 0.5
    layout "subtitle"

style confirm_button:
    size_group "confirm"

style confirm_button_text:
    xalign 0.5


##############################################################################
## Help
##
## A screen that gives information about key and mouse bindings. It uses other
## screens (keyboard_help, mouse_help, and gamepad_help) to display the actual
## help.

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Help"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 23

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
        text _("Navigate the interface.")

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
        text _("Advance dialogue and activates the interface.")

    hbox:
        label ("Left Trigger\nLeft Shoulder")
        text _("Roll back to earlier dialogue.")

    hbox:
        label _("Right Shoulder")
        text _("Roll forward to later dialogue.")

    hbox:
        label _("D-Pad, Sticks")
        text _("Navigate the interface.")

    hbox:
        label _("Start, Guide")
        text _("Access the game menu.")

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
    xmargin 12

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    text_align 1.0


##############################################################################
## Skip Indicator
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos 15
    ypadding 8
    left_padding 24
    right_padding 60

    background Frame("gui/skip.png", 24, 8, 75, 8)

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    # We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    # glyph in it.
    font gui.glyph_font

################################################################################
## Message notification.
##
## The notification screen is used to show the player a message. (For example,
## when the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text message

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
        background Frame("gui/notify.png", 24, 8, 75, 8)

        left_padding 24
        right_padding 60

        ypos 68
        ypadding 8

style notify_text:
    size gui.notify_text_size


################################################################################
## Medium and Touch Variants
##
## This section changes certain styes to make them more suitable for use with
## a tablet.

style pref_vbox:
    variant "medium"
    xsize 675

## Since a mouse may not be present, we replace the quick menu with a version
## that uses fewer and bigger buttons that are easier to touch.
screen quick_menu():
    variant "touch"

    zorder 100

    hbox:
        style_group "quick"

        xalign 0.5
        yalign 1.0

        textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
        textbutton _("Menu") action ShowMenu()
        textbutton _("Auto") action Preference("auto-forward", "toggle")

init python:

    if renpy.variant("touch"):
        gui.quick_button_borders = Borders(90, 21, 90, 0)


################################################################################
## Small Variants
##
## This section changes many sizes and images to make the game suitable for a
## small phone screen.

init python:

    if renpy.variant("small"):
        gui.text_size = 45
        gui.notify_text_size = 38
        gui.interface_text_size = 54
        gui.label_text_size = 54

        gui.file_slot_cols = 2
        gui.file_slot_rows = 2

        gui.slider_size = 66
        gui.thumb_size = 23

style window:
    variant "small"
    xpadding 135
    ysize 360
    background "gui/phone/textbox.png"

style choice_button:
    variant "small"
    xsize 1785
    xpadding 150
    ypadding 12

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"
    xpadding 180

style nvl_entry:
    variant "small"
    ysize 255

style nvl_dialogue:
    variant "small"
    ypos 9

style quick_button_text:
    variant "small"
    size 30

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style navigation_vbox:
    variant "small"
    xsize 501

style pref_vbox:
    variant "small"
    xsize 600

style slider_pref_vbox:
    variant "small"
    xsize None

style slider_pref_slider:
    variant "small"
    xsize 900

style history_window:
    variant "small"
    ysize 285

style history_who:
    variant "small"
    xmaximum 225
    min_width 225
    text_align 1.0
    size gui.text_size

style history_text:
    variant "small"
    ypos 6
    size 38

style history_label:
    variant "small"
    xfill True

style history_label_text:
    variant "small"
    xalign 0.5

style confirm_frame:
    variant "small"
    xsize 1266
    ysize 713

style notify_frame:
    variant "small"
    ypos 83


