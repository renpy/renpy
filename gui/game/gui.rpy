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
# GUI Configuration Variables
################################################################################


## Colors ######################################################################
##
## The colors of text in the interface.

## An accent color used throughout the interface to label and highlight
## text.
define gui.accent_color = "#00b8c3"

## The color used for a text button when it is neither selected nor hovered.
define gui.idle_color = "#555555"

## The small color is used for small text, which needs to be
## brighter/darker to achieve the same effect.
define gui.idle_small_color = "#aaaaaa"

## The color that is used for buttons and bars that are hovered.
define gui.hover_color = Color(gui.accent_color).tint(.6)

## The color used for a text button when it is selected but not focused.
## A button is selected if it is the current screen or preference value
define gui.selected_color = "#ffffff"

## The color used for a text button when it cannot be selected.
define gui.insensitive_color = "#55555580"

## Colors used for the portions of bars that are not filled in. These are
## not used directly, but are used when re-generating bar image files.
define gui.muted_color = "#004e49"
define gui.hover_muted_color = "#006e75"

## The colors used for dialogue and menu choice text.
define gui.text_color = "#ffffff"
define gui.interface_text_color = "#ffffff"

## Fonts and Font Sizes ########################################################

## The font used for in-game text.
define gui.default_font = "DejaVuSans.ttf"

## The font used for out-of-game text.
define gui.interface_font = "DejaVuSans.ttf"

## The size of normal dialogue text.
define gui.text_size = gui.scale(22)

## The size of character names.
define gui.name_text_size = gui.scale(30)

## The size of text in the game's user interface.
define gui.interface_text_size = gui.scale(24)

## The size of labels in the game's user interface.
define gui.label_text_size = gui.scale(30)

## The size of text on the notify screen.
define gui.notify_text_size = gui.scale(16)

## The size of the game's title.
define gui.title_text_size = gui.scale(50)


## Images ######################################################################

## The images used for the main and game menus.
define gui.main_menu_background = "gui/main_menu.png"
define gui.game_menu_background = "gui/game_menu.png"

## This is the icon displayer on the taskbar or dock.
define config.window_icon = "gui/window_icon.png"


## Dialogue ####################################################################
##
## These variables control how dialogue is displayed on the screen one line
## at a time.

## The height of the textbox containing dialogue.
define gui.textbox_height = gui.scale(185)

## The placement of the textbox vertically on the screen. 0.0 is the top, 0.5 is
## center, and 1.0 is the bottom.
define gui.textbox_yalign = 1.0


## The placement of the speaking character's name, relative to the textbox.
## These can be a whole number of pixels from the left or top, or 0.5 to center.
define gui.name_xpos = gui.scale(240)
define gui.name_ypos = gui.scale(0)

## The horizontal alignment of the character's name. This can be 0.0 for
## left-aligned, 0.5 for centered, and 1.0 for right-aligned.
define gui.name_xalign = 0.0

## The width, height, and borders of the box containing the character's
## name, or None to automatically size it.
define gui.namebox_width = None
define gui.namebox_height = None

## The borders of the box containing the character's name, in left, top,
## right, bottom order.
define gui.namebox_borders = Borders(5, 5, 5, 5)

## If True, the background of the namebox will be tiled, if False, the background
## if the namebox will be scaled.
define gui.namebox_tile = False


## The placement of dialogue relative to the textbox. These can be a whole
## number of pixels relative to the left or to, or 0.5 to center.
define gui.text_xpos = gui.scale(268)
define gui.text_ypos = gui.scale(50)

## The maxium width of dialogue text, in pixels.
define gui.text_width = gui.scale(744)

## The horizontal alignment of the character's name. This can be 0.0 for
## left-aligned, 0.5 for centered, and 1.0 for right-aligned.
define gui.text_xalign = 0.0


## Buttons #####################################################################
##
## These variables, along with the image files in gui/button, control aspects
## of how buttons are displayed.

## The width and height of a button, on pixels. If None, Ren'Py computes a size.
define gui.button_width = None
define gui.button_height = gui.scale(36)

## The borders on each side of the button, in left, top, right, bottom order.
define gui.button_borders = Borders(gui.scale(4), gui.scale(4), gui.scale(4), gui.scale(4))

## If True, the backgound image will be tiled. If False, the background image
## will be linearly scaled.
define gui.button_tile = False

## The font used by the button.
define gui.button_text_font = gui.interface_font

## The size of the text used by the button.
define gui.button_text_size = gui.interface_text_size

# The color of button text in various states.
define gui.button_text_idle_color = gui.idle_color
define gui.button_text_hover_color = gui.hover_color
define gui.button_text_selected_color = gui.accent_color
define gui.button_text_insensitive_color = gui.insensitive_color

# The horizontal alignment of the button text. (0.0 is left, 0.5 is center,
# 1.0 is right).
define gui.button_text_xalign = 0.0


## These variables override settings for different kinds of buttons. Please
## see the gui documentation for the kinds of buttons available, and what
## each is used for.
##
## These customizations are used by the default interface:

define gui.radio_button_borders = Borders(gui.scale(25), gui.scale(4), gui.scale(4), gui.scale(4))

define gui.check_button_borders = Borders(gui.scale(25), gui.scale(4), gui.scale(4), gui.scale(4))

define gui.confirm_button_text_xalign = 0.5

define gui.page_button_borders = Borders(gui.scale(10), gui.scale(4), gui.scale(10), gui.scale(4))

define gui.quick_button_borders = Borders(gui.scale(10), gui.scale(4), gui.scale(10), gui.scale(0))
define gui.quick_button_text_size = gui.scale(14)
define gui.quick_button_text_idle_color = gui.idle_small_color

## You can also add your own customizations, by adding code. For example, you
## can uncomment the following line:

# define gui.navigation_button_width = 250


## Choice Buttons ##############################################################
##
## Choice buttons are used in the in-game menus.

define gui.choice_button_width = gui.scale(790)
define gui.choice_button_height = None
define gui.choice_button_tile = False
define gui.choice_button_borders = Borders(gui.scale(100), gui.scale(5), gui.scale(100), gui.scale(5))
define gui.choice_button_text_font = gui.default_font
define gui.choice_button_text_size = gui.text_size
define gui.choice_button_text_xalign = 0.5
define gui.choice_button_text_idle_color = "#cccccc"
define gui.choice_button_text_hover_color = "#ffffff"


## File Slot Buttons ###########################################################
##
## A file slot button is a special kind of button. It contains a thumbnail
## image, and text describing the contents of the save slot. A save slot
## uses image files in gui/button, like the other kinds of buttons.

## The save slot button.
define gui.slot_button_width = gui.scale(276)
define gui.slot_button_height = gui.scale(206)
define gui.slot_button_borders = Borders(gui.scale(10), gui.scale(10), gui.scale(10), gui.scale(10))
define gui.slot_button_text_size = gui.scale(14)
define gui.slot_button_text_xalign = 0.5
define gui.slot_button_text_idle_color = gui.idle_small_color

## The width and height of thumbnails used by the save slots.
define config.thumbnail_width = gui.scale(256)
define config.thumbnail_height = gui.scale(144)

## The number of columns and rows in the grid of save slots.
define gui.file_slot_cols = 3
define gui.file_slot_rows = 2


## Positioning and Spacing #####################################################
##
## These variables control the positioning and spacing of various user interface
## elements.

## The position of the left side of the navigation buttons, relative
## to the left side of the screen.
define gui.navigation_xpos = gui.scale(40)

## The vertical position of the skip indicator.
define gui.skip_ypos = gui.scale(10)

## The vertical position of the notify screen.
define gui.notify_ypos = gui.scale(45)

## The spacing between menu choices.
define gui.choice_spacing = gui.scale(22)

## Buttons in the navigation section of the main and game menus.
define gui.navigation_spacing = gui.scale(4)

## Preference buttons.
define gui.pref_spacing = gui.scale(0)

## The spacing between file page buttons.
define gui.page_spacing = gui.scale(0)

## The spacing between file slots.
define gui.slot_spacing = gui.scale(10)


## Frames ######################################################################
##
## These variables controls the look of frames that can contain user interface
## components when an overlay or window is not present.

## Generic frames that are introduced by player code.
define gui.frame_borders = Borders(gui.scale(4), gui.scale(4), gui.scale(4), gui.scale(4))

## The frame that is used as part of the confirm screen.
define gui.confirm_frame_borders = Borders(gui.scale(40), gui.scale(40), gui.scale(40), gui.scale(40))

## The frame that is used as part of the skip screen.
define gui.skip_frame_borders = Borders(gui.scale(16), gui.scale(5), gui.scale(50), gui.scale(5))

## The frame that is used as part of the notify screen.
define gui.notify_frame_borders = Borders(gui.scale(16), gui.scale(5), gui.scale(40), gui.scale(5))

## Should frame backgrounds be tiled?
define gui.frame_tile = False


## Bars, Scrollbars, and Sliders ###############################################
##
## These control the look and size of bars, scrollbars, and sliders.
##
## The default GUI only uses sliders and vertical scrollbars.
## All of the other bars are only used in creator-written code.

## The height of horizontal bars, scrollbars, and sliders. The width of
## vertical bars, scrollbars, and sliders.
define gui.bar_size = gui.scale(36)
define gui.scrollbar_size = gui.scale(12)
define gui.slider_size = gui.scale(30)

## True if bar images should be tiled. False if they should be linearly scaled.
define gui.bar_tile = False
define gui.scrollbar_tile = False
define gui.slider_tile = False

## Horizontal borders.
define gui.bar_borders = Borders(gui.scale(4), gui.scale(4), gui.scale(4), gui.scale(4))
define gui.scrollbar_borders = Borders(gui.scale(4), gui.scale(4), gui.scale(4), gui.scale(4))
define gui.slider_borders = Borders(gui.scale(4), gui.scale(4), gui.scale(4), gui.scale(4))

## Vertical borders.
define gui.vbar_borders = Borders(gui.scale(4), gui.scale(4), gui.scale(4), gui.scale(4))
define gui.vscrollbar_borders = Borders(gui.scale(4), gui.scale(4), gui.scale(4), gui.scale(4))
define gui.vslider_borders = Borders(gui.scale(4), gui.scale(4), gui.scale(4), gui.scale(4))

## What to do with unscrollable scrollbars in the gui. "hide" hides them, while
## None shows them.
define gui.unscrollable = "hide"

################################################################################
## Styles.
################################################################################

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


style gui_text:
    font gui.interface_font
    color gui.interface_text_color
    size gui.interface_text_size


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.button_text_properties("button")
    yalign 0.5


style label_text is gui_text:
    color gui.accent_color
    size gui.label_text_size

style prompt_text is gui_text:
    color gui.text_color
    size gui.interface_text_size


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)


################################################################################
## In-game screens
################################################################################


## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It take two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None
## if no name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py
## uses this to manage text display. It can also create displayables with
## id "who" and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):
    style_group "say"

    window:
        id "window"

        text what id "what"

        if who is not None:

            window:
                style "namebox"
                text who id "who"

    # If there's a side image, display it above the text. Do not display
    # on the phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


style window is default
style say_label is default
style say_dialogue is default

style namebox is default
style namebox_label is say_label


style window:
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    color gui.accent_color
    size gui.name_text_size
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos

    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")



## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used
## to pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept
## the various input parameters.
##
## http://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_group "input"

    window:

        vbox:
            xpos gui.text_xpos
            xanchor gui.text_xalign
            ypos gui.text_ypos

            text prompt style "input_prompt"
            input id "input"


style input_prompt is default

style input_prompt:
    xmaximum gui.text_width
    xalign gui.text_xalign
    text_align gui.text_xalign

style input:
    xmaximum gui.text_width
    xalign gui.text_xalign
    text_align gui.text_xalign

## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the
## menu statement. The one parameter, items, is a list of objects, each
## with caption and action fields.
##
## http://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_group "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


## When this is true, labels will spoken by the narrator rather then
## displayed as empty buttons.
define config.narrator_menu = True


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos gui.scale(270)
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the
## out-of-game menus.

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
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.button_text_properties("quick_button")


################################################################################
# Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
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
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.button_text_properties("navigation_button")


## Main Menu screen ############################################################
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
    xsize gui.scale(280)
    yfill True

    background "gui/overlay/main_menu.png"

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
    size gui.title_text_size


## Game Menu screen ############################################################
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

                        side_yfill True

                        transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial 1.0

                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        side_yfill True

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

    background "gui/overlay/game_menu.png"

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
    unscrollable gui.unscrollable

style game_menu_side:
    spacing gui.scale(10)

style game_menu_label:
    xpos gui.scale(50)
    ysize gui.scale(120)

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset gui.scale(-30)


## About screen ################################################################
##
## This screen gives credit and copyright information about the game and
## Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one.
    ## The vbox child is then included inside the viewport inside the
    ## game_menu screen.
    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            ## gui.about is usually set in options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


## This is redefined in options.rpy to add text to the about screen.
define gui.about = ""


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and
## load it again. Since they share nearly everything in common, both
## are implemented in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save
## https://www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu

    use file_slots(_("Save"))


screen load():

    tag menu

    use file_slots(_("Load"))


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


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding gui.scale(50)
    ypadding gui.scale(3)

style page_label_text:
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.button_text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.button_text_properties("slot_button")


## Preferences screen ##########################################################
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
                        style_prefix "radio"
                        label _("Display")
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "radio"
                    label _("Rollback Side")
                    textbutton _("Disable") action Preference("rollback side", "disable")
                    textbutton _("Left") action Preference("rollback side", "left")
                    textbutton _("Right") action Preference("rollback side", "right")

                vbox:
                    style_prefix "check"
                    label _("Skip")
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                ## Additional vboxes of type "radio_pref" or "check_pref" can be added here, to
                ## add additional creator-defined preferences.

            null height gui.scale(50)

            hbox:
                style_prefix "slider"
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
                        style "mute_all_button"


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_pref_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.scale(10)
    bottom_margin gui.scale(2)

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize gui.scale(225)

style radio_vbox:
    spacing gui.pref_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style radio_button_text:
    properties gui.button_text_properties("radio_button")

style check_vbox:
    spacing gui.pref_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.button_text_properties("check_button")

style slider_slider:
    xsize gui.scale(350)

style slider_button:
    yalign 0.5
    left_margin gui.scale(10)

style slider_vbox:
    xsize gui.scale(450)


## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player.
## While there isn't anything special about this screen, it does have to
## access the dialogue history stored in _history_list.
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


## The number of blocks of dialogue history Ren'Py will keep.
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


## Help screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses
## other screens (keyboard_help, mouse_help, and gamepad_help) to display the
## actual help.

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
    properties gui.button_properties("help_button")
    xmargin gui.scale(8)

style help_button_text:
    properties gui.button_text_properties("help_button")

style help_label:
    xsize gui.scale(250)
    right_padding gui.scale(20)

style help_label_text:
    size gui.text_size
    xalign 1.0
    text_align 1.0


################################################################################
## Additional screens
################################################################################


## Confirm screen ##############################################################
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


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    text_align 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.button_text_properties("confirm_button")


## Skip indicator screen #######################################################
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
            spacing gui.scale(6)

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
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    # We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    # glyph in it.
    font "DejaVuSans.ttf"


## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example,
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
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    size gui.notify_text_size


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
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
## Medium and Touch Variants
##
## This section changes certain styes to make them more suitable for use with
## touch devices like tablets.
################################################################################

style pref_vbox:
    variant "medium"
    xsize gui.scale(450)

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
        gui.quick_button_borders = Borders(gui.scale(60), gui.scale(14), gui.scale(60), gui.scale(0))


################################################################################
## Small Variants
##
## This section changes many sizes and images to make the game suitable for
## a small phone screen.
################################################################################

# init python:
#
#     if renpy.variant("small"):
#         gui.text_size = gui.scale(30)
#         gui.notify_text_size = gui.scale(25)
#         gui.interface_text_size = gui.scale(36)
#         gui.label_text_size = gui.scale(36)
#
#         gui.file_slot_cols = 2
#         gui.file_slot_rows = 2
#
#         gui.slider_size = gui.scale(44)
#         gui.thumb_size = gui.scale(15)
#
# style window:
#     variant "small"
#     xpadding gui.scale(90)
#     ysize gui.scale(240)
#     background "gui/phone/textbox.png"
#
# style choice_button:
#     variant "small"
#     xsize gui.scale(1190)
#     xpadding gui.scale(100)
#     ypadding gui.scale(8)
#
# style nvl_window:
#     variant "small"
#     background "gui/phone/nvl.png"
#     xpadding gui.scale(120)
#
# style nvl_entry:
#     variant "small"
#     ysize gui.scale(170)
#
# style nvl_dialogue:
#     variant "small"
#     ypos gui.scale(6)
#
# style quick_button_text:
#     variant "small"
#     size gui.scale(20)
#
# style main_menu_frame:
#     variant "small"
#     background "gui/phone/overlay/main_menu.png"
#
# style game_menu_outer_frame:
#     variant "small"
#     background "gui/phone/overlay/game_menu.png"
#
# style game_menu_navigation_frame:
#     variant "small"
#     xsize gui.scale(340)
#
# style game_menu_content_frame:
#     variant "small"
#     top_margin 0
#
# style navigation_vbox:
#     variant "small"
#     xsize gui.scale(334)
#
# style pref_vbox:
#     variant "small"
#     xsize gui.scale(400)
#
# style slider_pref_vbox:
#     variant "small"
#     xsize None
#
# style slider_pref_slider:
#     variant "small"
#     xsize gui.scale(600)
#
# style history_window:
#     variant "small"
#     ysize gui.scale(190)
#
# style history_who:
#     variant "small"
#     xmaximum gui.scale(150)
#     min_width gui.scale(150)
#     text_align 1.0
#     size gui.text_size
#
# style history_text:
#     variant "small"
#     ypos gui.scale(4)
#     size gui.scale(25)
#
# style history_label:
#     variant "small"
#     xfill True
#
# style history_label_text:
#     variant "small"
#     xalign 0.5
#
# style confirm_frame:
#     variant "small"
#     xsize gui.scale(844)
#     ysize gui.scale(475)
#
# style notify_frame:
#     variant "small"
#     ypos gui.scale(55)

