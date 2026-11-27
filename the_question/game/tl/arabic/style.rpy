translate arabic python:
    ## Right-align interface and button text. Buttons with their own alignment,
    ## such as the centered choice buttons, keep it.
    gui.interface_text_xalign = 1.0
    gui.button_text_xalign = 1.0
    gui.main_menu_text_xalign = 1.0

    ## Dialogue.
    gui.dialogue_text_xalign = 1.0
    gui.dialogue_text_line_leading = 3 # Prevents tanween (اً) from leaking into upper lines
    gui.dialogue_text_line_spacing = 3
    gui.name_xalign = 1.0

    gui.dialogue_xpos = config.screen_width - gui.dialogue_xpos
    gui.name_xpos = config.screen_width - gui.name_xpos

    ## Main and game menu navigation.
    gui.navigation_xpos = config.screen_width - gui.navigation_xpos

    ## Make room for the checkbox on the right side of the button.
    gui.radio_button_borders = Borders(4, 4, 25, 4)
    gui.check_button_borders = Borders(4, 4, 25, 4)

    ## Skip indicator and notification frames.
    gui.skip_frame_borders = Borders(50, 5, 16, 5)
    gui.notify_frame_borders = Borders(40, 5, 16, 5)

    ## History. The positions are mirrored by the history styles below.
    gui.history_name_xalign = 0.0
    gui.history_text_xalign = 1.0

    ## NVL-mode.
    gui.nvl_name_xpos = config.screen_width - gui.nvl_name_xpos
    gui.nvl_name_xalign = 0.0
    gui.nvl_text_xpos = config.screen_width - gui.nvl_text_xpos
    gui.nvl_text_xalign = 1.0
    gui.nvl_thought_xpos = config.screen_width - gui.nvl_thought_xpos
    gui.nvl_thought_xalign = 1.0
    gui.nvl_button_xpos = config.screen_width - gui.nvl_button_xpos
    gui.nvl_button_xalign = 1.0


################################################################################
## General layout
################################################################################

translate arabic style hbox:
    box_reverse True
    xalign 1.0

translate arabic style vbox:
    xalign 1.0

translate arabic style button:
    xalign 1.0

translate arabic style label:
    xalign 1.0

# Inspector style
translate arabic style _default:
    font "DejaVuSans.ttf"

################################################################################
## Bars and sliders
################################################################################

## The minimum value is on the right, and the maximum value is on the left.

translate arabic style bar:
    bar_invert True
    left_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)

translate arabic style slider:
    bar_invert True
    xalign 1.0


################################################################################
## Main menu
################################################################################

translate arabic style main_menu_frame:
    xalign 1.0
    background Transform("gui/overlay/main_menu.png", xzoom=-1.0, xalign=1.0)

translate arabic style main_menu_frame:
    variant "small"
    background Transform("gui/phone/overlay/main_menu.png", xzoom=-1.0, xalign=1.0)

## The game's title. xfill makes the text align to the right edge of the box,
## rather than to the right edge of its widest line.
translate arabic style main_menu_vbox:
    xalign 0.0
    xoffset 20
    xfill True

translate arabic style navigation_vbox:
    xanchor 1.0


################################################################################
## Game menu
################################################################################

translate arabic style game_menu_outer_frame:
    xfill True
    background Transform("gui/overlay/game_menu.png", xzoom=-1.0)

translate arabic style game_menu_outer_frame:
    variant "small"
    background Transform("gui/phone/overlay/game_menu.png", xzoom=-1.0)

translate arabic style game_menu_content_frame:
    left_margin 20
    right_margin 40

## The title of the menu.
translate arabic style game_menu_label:
    xalign 1.0
    xoffset -50

translate arabic style return_button:
    xanchor 1.0

## Fill the viewport, so that its contents can be aligned to the right.
translate arabic style game_menu_vbox:
    xfill True

## The scrollbar goes to the left of the viewport. A side always places it on the
## right, so the viewport is moved right by the width of the scrollbar and its
## spacing, and the scrollbar is moved left by the width of the viewport and the
## spacing.

translate arabic style game_menu_viewport:
    xoffset gui.scrollbar_size + 10

translate arabic style game_menu_vpgrid:
    xsize 920
    xoffset gui.scrollbar_size + 10

translate arabic style game_menu_vscrollbar:
    xoffset -(920 + 10)

translate arabic style game_menu_vpgrid:
    variant "small"
    xsize 870

translate arabic style game_menu_vscrollbar:
    variant "small"
    xoffset -(870 + 10)


################################################################################
## About screen
################################################################################

translate arabic style about_small:
    textalign 0.0


################################################################################
## Preferences screen
################################################################################

translate arabic style radio_button:
    foreground Transform("gui/button/radio_[prefix_]foreground.png", xzoom=-1.0, xalign=1.0)

## This also applies to the "Mute All" button.
translate arabic style check_button:
    foreground Transform("gui/button/check_[prefix_]foreground.png", xzoom=-1.0, xalign=1.0)

## The "Test" buttons are to the left of their sliders.
translate arabic style slider_button:
    left_margin 0
    right_margin 10


################################################################################
## History screen
################################################################################

## These measure the gui positions from the right side of each entry.

translate arabic style history_name:
    xpos 1.0
    xoffset -gui.history_name_xpos

translate arabic style history_text:
    xpos 1.0
    xoffset -gui.history_text_xpos


################################################################################
## Help screen
################################################################################

translate arabic style help_label:
    left_padding 20
    right_padding 0

translate arabic style help_label_text:
    xalign 0.0
    textalign 0.0


################################################################################
## Skip indicator and notify screens
################################################################################

translate arabic style skip_frame:
    xalign 1.0
    background Frame(Transform("gui/skip.png", xzoom=-1.0), gui.skip_frame_borders, tile=gui.frame_tile)

translate arabic style notify_frame:
    xalign 1.0
    background Frame(Transform("gui/notify.png", xzoom=-1.0), gui.notify_frame_borders, tile=gui.frame_tile)
