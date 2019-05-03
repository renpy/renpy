# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

init -1:

    # Fonts.
    define gui.LIGHT_FONT = "fonts/Roboto-Light.ttf"
    define gui.REGULAR_FONT = "fonts/Roboto-Regular.ttf"

    # Used to scale the size of fonts.
    define gui.FONT_SCALE = 1.0

    # Should places where the regular font used be bolded?
    define gui.REGULAR_BOLD = False

init -1 python:

    config.defer_styles = True

    # The color of non-interactive text.
    TEXT = "#545454"

    # Colors for buttons in various states.
    IDLE = "#42637b"
    HOVER = "#d86b45"
    DISABLED = "#808080"

    # Colors for reversed text buttons (selected list entries).
    REVERSE_IDLE = "#78a5c5"
    REVERSE_HOVER = "#d86b45"
    REVERSE_TEXT = "#ffffff"

    # Colors for the scrollbar thumb.
    SCROLLBAR_IDLE = "#dfdfdf"
    SCROLLBAR_HOVER = "#d86b45"

    # An image used as a separator pattern.
    PATTERN = "images/pattern.png"

    # A displayable used for the background of everything.
    BACKGROUND = "images/background.png"

    # A displayable used for the background of windows
    # containing commands, preferences, and navigation info.
    WINDOW = Frame("images/window.png", 0, 0, tile=True)

    # A displayable used for the background of the projects list.
    PROJECTS_WINDOW = Null()

    # A displayable used the background of information boxes.
    INFO_WINDOW = "#f9f9f9"

    # Colors for the titles of information boxes.
    ERROR_COLOR = "#d15353"
    INFO_COLOR = "#545454"
    INTERACTION_COLOR = "#d19753"
    QUESTION_COLOR = "#d19753"

    # The color of input text.
    INPUT_COLOR = "#d86b45"


init 1 python:

    def size(n):
        """
        Adjusts the font size if we're in large-print mode.
        """

        if persistent.large_print and n < 18:
            n = 18

        n = int(n * gui.FONT_SCALE)

        return n

    def light_font():
        if persistent.large_print:
            return gui.REGULAR_FONT

        return gui.LIGHT_FONT

    def regular_font():
        return gui.REGULAR_FONT

    INDENT = 20
    HALF_INDENT = 10

    SCROLLBAR_SIZE = 16

    SEPARATOR = Frame(PATTERN, 0, 0, tile=True, ymaximum=5, yalign=1.0)
    SEPARATOR2 = Frame(PATTERN, 0, 0, tile=True, ymaximum=10, yalign=1.0)

    SPACER_HEIGHT = 8
    SPACER = Null(height=SPACER_HEIGHT)

    HALF_SPACER_HEIGHT = 4
    HALF_SPACER = Null(height=HALF_SPACER_HEIGHT)

    # DIVIDING THE SCREEN
    ONETHIRD = 258
    TWOTHIRDS = 496
    ONEHALF = 377

    def checkbox(full, color):
        if full:
            return im.Twocolor("images/checkbox_full.png", color, color, style="l_checkbox_box")
        else:
            return im.Twocolor("images/checkbox_empty.png", color, color, style="l_checkbox_box")



# The default style.
style l_default is default:
    font light_font()
    color TEXT
    idle_color IDLE
    hover_color HOVER
    size size(18)

style l_text is l_default

style l_button is l_default
style l_button_text is l_default:
    insensitive_color DISABLED
    selected_font regular_font()
    selected_bold gui.REGULAR_BOLD

# A small button, used at the bottom of the screen.
style l_link is l_default
style l_link_text is l_default:
    size size(14)
    font light_font()

# Action buttons on the bottom of the screen.
style l_right_button is l_default:
    xalign 1.0
    ypos 600 - 128 + 12
    left_margin 8 + INDENT
    right_margin 10 + INDENT

style l_right_button_text is l_default:
    size size(30)

style l_left_button is l_right_button:
    xalign 0.0

style l_left_button_text is l_right_button_text


# The root frame. This contains everything but the bottom navigation,
# and buttons.
style l_root is l_default:
    background BACKGROUND
    xpadding 10
    top_padding 64
    bottom_padding 128

# An inner window.
style l_window is l_default:
    background WINDOW
    left_padding 6
    xfill True
    yfill True

# Normal size labels.
style l_label is l_default:
    xfill True
    top_padding 10
    bottom_padding 8
    bottom_margin 12
    background SEPARATOR

style l_label_text is l_default:
    size size(24)
    xpos INDENT
    yoffset 6

style l_label_small is l_default:
    xfill True
    bottom_padding 8
    bottom_margin HALF_SPACER_HEIGHT
    background SEPARATOR

# Small labels.
style l_label_small_text is l_default:
    xpos INDENT
    yoffset 6
    size size(20)

# Alternate labels. This nests inside an l_label, and gives a button
# or label that's nested inside another label.

style l_alternate is l_default:
    xalign 1.0
    yalign 1.0
    yoffset 4
    right_margin INDENT

style l_alternate_text is l_default:
    size size(14)
    font light_font()
    text_align 1.0

style l_small_button is l_button

style l_small_button_text is l_button_text:
    size size(14)

style l_small_text is l_text:
    size size(14)

# Indents its contents.
style l_indent is l_default:
    left_margin INDENT

# Indents its contents and pads vertically.
style l_indent_margin is l_indent:
    ymargin 6

# Lists.
style l_list is l_default:
    left_padding HALF_INDENT
    xfill True
    selected_background REVERSE_IDLE
    selected_hover_background REVERSE_HOVER

style l_list_text is l_default:
    idle_color IDLE
    hover_color HOVER
    selected_idle_color REVERSE_TEXT
    selected_hover_color REVERSE_TEXT
    insensitive_color DISABLED

style l_list2 is l_list:
    left_padding (HALF_INDENT + INDENT)

style l_list2_text is l_list_text

# Scrollbar.
style l_vscrollbar is l_default:
    thumb Fixed(
        Solid(SCROLLBAR_IDLE, xmaximum=8, xalign=0.5),
        Image("images/vscrollbar_center.png", xalign=0.5, yalign=0.5),
        xmaximum = SCROLLBAR_SIZE)
    hover_thumb Fixed(
        Solid(SCROLLBAR_HOVER, xmaximum=8, xalign=0.5),
        Image("images/vscrollbar_center.png", xalign=0.5, yalign=0.5),
        xmaximum = SCROLLBAR_SIZE)
    xmaximum SCROLLBAR_SIZE
    bar_vertical True
    bar_invert True
    unscrollable "hide"

# Information window.
style l_info_vbox is vbox:
    yalign 0.5
    xalign 0.5
    xfill True

style l_info_frame is l_default:
    ypadding 21
    xfill True
    background Fixed(
        INFO_WINDOW,
        Frame(PATTERN, 0, 0, tile=True, ymaximum=5, yalign=0.0, yoffset=8),
        Frame(PATTERN, 0, 0, tile=True, ymaximum=5, yalign=1.0, yoffset=-8),
        )
    yminimum 180
    ypos 75

style l_info_label is l_default:
    xalign 0.5
    ypos 75
    yanchor 1.0
    yoffset 12

style l_info_label_text is l_default:
    size size(36)

style l_info_text is l_default:
    xalign 0.5

style l_info_button is l_button:
    xalign 0.5
    xmargin 50

style l_info_button_text is l_button_text:
    text_align 0.5
    layout "subtitle"

# Progress bar.
style l_progress_frame is l_default:
    background Frame(PATTERN, 0, 0, tile=True)
    ypadding 5

style l_progress_bar is l_default:
    left_bar REVERSE_IDLE
    right_bar Null()
    ymaximum 24

# Navigation.
style l_navigation_button is l_button:
    size_group "navigation"
    right_margin INDENT
    top_margin 3

style l_navigation_button_text is l_button_text:
    size size(14)
    font regular_font()

style l_navigation_text is l_text:
    size size(14)
    font light_font()
    color TEXT

# Checkboxes.
style l_checkbox is l_button:
    left_padding INDENT
    background checkbox(False, IDLE)
    hover_background checkbox(False, HOVER)
    selected_idle_background checkbox(True, IDLE)
    selected_hover_background checkbox(True, HOVER)
    insensitive_background checkbox(False, DISABLED)

style l_checkbox_box:
    yanchor 0.5
    ypos 11

style l_checkbox_text is l_button_text:
    selected_font light_font()
    selected_bold False

# Lines up with a checkbox.
style l_nonbox is l_button:
    xpadding INDENT

style l_nonbox_text is l_button_text:
    selected_font light_font()

# Projects list.
style l_projects is l_default:
    background PROJECTS_WINDOW

style hyperlink_text:
    size size(18)
    font light_font()
    color IDLE
    hover_color HOVER
