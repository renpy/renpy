# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

# This file is responsible for creating and defining the default styles
# used by the system.

# This file should be considered part of the Ren'Py library, and not
# something that needs to be modified by the user. Instead, just update
# the appropriate style property in an init: block in your script.
#
# For example, to change the default window backgrounds to a
# transparent dark red, add:
#
# init:
#     $ style.window.background = "#8008"
#
# to your script. No need to mess around here, it will just make your
# life harder when a new version of Ren'Py is released.

init -1800 python hide:

    # Style Declarations #################################################

    style.default = Style(None, help='root of style hierarchy')
    style.text = Style(style.default, help='style of text')

    style.fixed = Style(style.default, help='fixed layouts')
    style.hbox = Style(style.default, help='horizontal boxes')
    style.vbox = Style(style.default, help='vertical boxes')
    style.grid = Style(style.default, help='grid layouts')
    style.side = Style(style.default, help='side layouts')

    style.window = Style(style.default, help='windows created with ui.window')

    style.image_placement = Style(style.default, help='default placement of images on the screen')
    style.image = Style(style.default, help="default style of images")

    style.motion = Style(style.default, help="default style of motions and zooms.")
    style.animation = Style(style.default, help="default style of animations.")

    style.say_label = Style(style.default, help='the name of the character speaking dialogue.')
    style.say_dialogue = Style(style.default, help='used for dialogue text')
    style.say_thought = Style(style.default, help='used by the default narrator')
    style.say_window = Style(style.window, help='windows containing dialogue and thoughts')
    style.say_who_window = Style(style.window, help='window containing the label in two-window-say mode')
    style.say_two_window_vbox = Style(style.vbox, help='vbox containing the two windows in two-window-say mode')
    style.say_vbox = Style(style.vbox, help='contains the label (if present) and the body of dialogue')

    style.menu = Style(style.default, help='the vbox containing an in-game menu')
    style.menu_caption = Style(style.default, help='in-game menu caption text')
    style.menu_choice = Style(style.default, help='text of an in-game menu choice')
    style.menu_choice_button = Style(style.default, help='buttons containing in-game menu choices')
    style.menu_choice_chosen = Style(style.menu_choice, help='text of an in-game menu choice that has been chosen')
    style.menu_choice_chosen_button = Style(style.menu_choice_button, help='buttons containing chosen in-game menu choices')
    style.menu_window = Style(style.window, help='a window containing a menu')

    style.input = Style(style.default, help='style of an input control')
    style.input_text = Style(style.input, help='text of an input box')
    style.input_prompt = Style(style.default, help='prompt of an input box')
    style.input_window = Style(style.window, help='window of an input box')

    style.centered_window = Style(style.default, help='window containing centered text')
    style.centered_text = Style(style.default, help='centered text')
    style.centered_vtext = Style(style.default, help='centered text')

    style.imagemap = Style(style.image_placement, help='default style of imagemaps')
    style.hotspot = Style(style.default, help='default style of hotspots inside imagemaps')
    style.hotbar = Style(style.default, help='default style of hotbars inside imagemaps')
    style.imagemap_button = style.hotspot

    style.image_button = Style(style.default, help='default style of image buttons')
    style.image_button_image = Style(style.default, help='default style of images inside image buttons')

    style.hyperlink = Style(style.default, help=None) # ignored
    style.hyperlink_text = Style(style.default, help='hyperlinked text')
    style.ruby_text = Style(style.default, help='ruby text')

    style.viewport = Style(style.default, help='default style of viewports')
    style.transform = Style(style.motion, help='default style of transforms')

    style.list = Style(style.default)
    style.list_box = Style(style.vbox)
    style.list_row = Style(style.default)
    style.list_row_box = Style(style.hbox)
    style.list_spacer = Style(style.default)
    style.list_text = Style(style.default)

    style.tile = Style(style.default, help='default style of tile')

    # Not used - but some old games might customize it.
    style.error_root = Style(style.default)

# The base styles that can be customized by themes.

    style.frame = Style(style.default, help='base style for frames.')
    style.menu_frame = Style(style.frame, help='base style for frames used in the game and main menus.')

    style.button = Style(style.default, help='base style for buttons.')
    style.button_text = Style(style.default, help='base style for button text')

    style.small_button = Style(style.button, help="base style for small buttons")
    style.small_button_text = Style(style.button_text, help="base style for small button text")
    style.radio_button = Style(style.button, help="base style for radio buttons")
    style.radio_button_text = Style(style.button_text, help="base style for radio button text")
    style.check_button = Style(style.button, help="base style for check buttons")
    style.check_button_text = Style(style.button_text, help="base style for check button text")

    style.large_button = Style(style.default, help="base style for large buttons")
    style.large_button_text = Style(style.default, help="base style for large button text")

    style.label = Style(style.default, help="base style for windows surrounding labels")
    style.label_text = Style(style.default, help="base style for label text")

    style.prompt = Style(style.default, help="base style for windows surrounding prompts")
    style.prompt_text = Style(style.default, help="base style for prompt text")

    style.bar = Style(style.default, help='base style for horizontal bars')
    style.vbar = Style(style.default, help='base style for vertical bars')

    style.slider = Style(style.default, help='base style for horizontal sliders')
    style.vslider = Style(style.default, help='base style for vertical sliders')

    style.scrollbar = Style(style.default, help='base style for horizontal scrollbars')
    style.vscrollbar = Style(style.default, help='base style for vertical scollbars')

    style.mm_root = Style(style.default, help="main menu root window")
    style.gm_root = Style(style.default, help="game menu root window")


init -1800 python:

    # Colors #############################################################

    # The Default Style ###################################################

    # Text properties.
    style.default.font = "DejaVuSans.ttf"
    style.default.language = "unicode"
    style.default.antialias = True
    style.default.size = 22
    style.default.color = (255, 255, 255, 255)
    style.default.black_color = (0, 0, 0, 255)
    style.default.bold = False
    style.default.italic = False
    style.default.underline = False
    style.default.strikethrough = False
    style.default.kerning = 0.0
    style.default.drop_shadow = None
    style.default.drop_shadow_color = (0, 0, 0, 255)
    style.default.outlines = [ ]
    style.default.minwidth = 0
    style.default.text_align = 0
    style.default.justify = False
    style.default.text_y_fudge = 0
    style.default.first_indent = 0
    style.default.rest_indent = 0
    style.default.line_spacing = 0
    style.default.line_leading = 0
    style.default.line_overlap_split = 0
    style.default.layout = "tex"
    style.default.subtitle_width = 0.9
    style.default.slow_cps = None
    style.default.slow_cps_multiplier = 1.0
    style.default.slow_abortable = False
    # style.default.hyperlink_functions (set in 00library.rpy)

    # Window properties.
    style.default.background = None
    style.default.xpadding = 0
    style.default.ypadding = 0
    style.default.xmargin = 0
    style.default.ymargin = 0
    style.default.xfill = False
    style.default.yfill = False
    style.default.xminimum = 0 # Includes margins and padding.
    style.default.yminimum = 0 # Includes margins and padding.

    # Placement properties.
    style.default.xpos = None # 0
    style.default.ypos = None # 0
    style.default.xanchor = None # 0
    style.default.yanchor = None # 0
    style.default.xmaximum = None
    style.default.ymaximum = None
    style.default.xoffset = 0
    style.default.yoffset = 0
    style.default.subpixel = False

    # Sound properties.
    style.default.sound = None

    # Box properties.
    style.default.spacing = 0
    style.default.first_spacing = None
    style.default.box_layout = None
    style.default.box_wrap = False
    style.default.box_reverse = False
    style.default.order_reverse = False

    # Focus properties.
    style.default.focus_mask = None
    style.default.focus_rect = None

    # Bar properties.
    style.default.fore_bar = Null()
    style.default.aft_bar = Null()
    style.default.thumb = None
    style.default.thumb_shadow = None
    style.default.left_gutter = 0
    style.default.right_gutter = 0
    style.default.thumb_offset = 0
    style.default.unscrollable = None

    # Misc.
    style.default.activate_sound = None
    style.default.clipping = False

    # Boxes.
    style.hbox.box_layout = 'horizontal'
    style.vbox.box_layout = 'vertical'

    # Motions, zooms, rotozooms, and transforms.
    style.motion.xanchor = 0
    style.motion.yanchor = 0
    style.motion.xpos = 0
    style.motion.ypos = 0

    # Windows.
    style.window.background = Solid((0, 0, 0, 192))
    style.window.xpadding = 6
    style.window.ypadding = 6
    style.window.xmargin = 0
    style.window.ymargin = 0
    style.window.xfill = True
    style.window.yfill = False
    style.window.yminimum = 150 # Includes margins and padding.
    style.window.xalign = 0.5
    style.window.yalign = 1.0

    # Dialogue
    style.say_label.bold = True
    style.say_vbox.spacing = 8

    # Two window styles.
    style.say_who_window.xminimum = 200
    style.say_who_window.yminimum = 34
    style.say_who_window.xfill = False
    style.say_who_window.xalign = 0

    style.say_two_window_vbox.yalign = 1.0

    # Menus.
    style.menu_choice.idle_color = "#0ff"
    style.menu_choice.hover_color = "#ff0"
    style.input.color = "#ff0"

    # Styles used by centered.
    style.centered_window.xalign = 0.5
    style.centered_window.xfill = False
    style.centered_window.yalign = 0.5
    style.centered_window.yfill = False
    style.centered_window.xpadding = 10

    style.centered_text.textalign = 0.5
    style.centered_text.xalign = 0.5
    style.centered_text.yalign = 0.5
    style.centered_text.layout = "subtitle"

    style.centered_vtext.textalign = 0.5
    style.centered_vtext.xalign = 0.5
    style.centered_vtext.yalign = 0.5
    style.centered_vtext.vertical = True

    # Hyperlinks.
    style.hyperlink_text.underline = True
    style.hyperlink_text.hover_color = "#0ff"
    style.hyperlink_text.idle_color = "#08f"

    # Ruby.
    style.ruby_text.size = 22
    style.ruby_text.xoffset = 0
    style.default.ruby_style = style.ruby_text

    # Bars.
    style.default.bar_invert = False
    style.default.bar_resizing = False
    style.default.bar_vertical = False

    style.vbar.bar_vertical = True
    style.vslider.bar_vertical = True
    style.vscrollbar.bar_vertical = True
    style.vscrollbar.bar_invert = True

    # Viewport
    style.viewport.clipping = True

    # Transform
    style.transform.subpixel = True

    # Menu windows.
    style.mm_root.background = "#000"
    style.mm_root.xfill = True
    style.mm_root.yfill = True

    style.gm_root.background = "#000"
    style.gm_root.xfill = True
    style.gm_root.yfill = True

    # Lists.
    style.list_row.xfill = True

    style.list_row.ymargin = 0
    style.list_row.background = "#eee"
    style.list_row[1].background = "#ddd"
    style.list_row.hover_background = "#fff"
    style.list_row[1].hover_background = "#fff"
    style.list_row.selected_background = "#cce"
    style.list_row[1].selected_background = "#cce"
    style.list_text.color = "#000"
    style.list_text.size = 14
    style.list_spacer.xminimum = 15

    # Tile
    style.tile.clipping = True
