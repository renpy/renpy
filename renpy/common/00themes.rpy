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

init -1400 python:

    class _Theme(object):

        # Using theme as a decorator is what we do to create a new theme.
        def __call__(self, func):
            setattr(self, func.func_name, func)
            return func

    _theme = theme = _Theme()
    del _Theme

    # Public only for compatiblity purposes.
    def RoundRect(color, small=False):
        if small:
            size = 6
        else:
            if config.screen_width <= 640:
                size = 6
            else:
                size = 12

        return Frame(theme.OneOrTwoColor("_roundrect/rr%dg.png" % size, color), size, size)

init -1110 python hide:

    @theme
    def clear_frames():
        style.frame.clear()

    @theme
    def clear_buttons():
        style.button.clear()
        style.button_text.clear()
        style.radio_button.clear()
        style.radio_button_text.clear()
        style.check_button.clear()
        style.check_button_text.clear()
        style.small_button.clear()
        style.small_button_text.clear()

    @theme
    def clear_large_buttons():
        style.large_button.clear()
        style.large_button_text.clear()

    @theme
    def clear_labels():
        style.label.clear()
        style.label_text.clear()

    @theme
    def clear_prompts():
        style.prompt.clear()
        style.prompt_text.clear()

    @theme
    def clear_bars():
        style.bar.clear()
        style.vbar.clear()
        style.scrollbar.clear()
        style.vscrollbar.clear()
        style.slider.clear()
        style.vslider.clear()

        style.vbar.bar_vertical = True
        style.vslider.bar_vertical = True
        style.vscrollbar.bar_vertical = True
        style.vscrollbar.bar_invert = True


    # This recolors the given image using one or two colors.
    @theme
    def OneOrTwoColor(image, color):
        if len(color) == 2:
            return im.Twocolor(image, color[0], color[1])
        else:
            return im.Twocolor(image, color, color)

    def roundrect_based_theme(name, file_prefix, Box=None, frame_png=None):

        if Box is None:
            def Box(color, ignored):
                return Frame(theme.OneOrTwoColor(file_prefix + "_box.png", color), 12, 12)

        if frame_png is not None:
            def FrameBox(color, ignored):
                return Frame(theme.OneOrTwoColor(file_prefix + frame_png, color), 12, 12)
        else:
            FrameBox = Box

        def frames(
            less_rounded,
            frame):

            theme.clear_frames()

            style.frame.background = Box(frame, less_rounded)

            style.frame.xpadding = 6
            style.frame.ypadding = 6

        setattr(theme, name + "_frames", frames)


        def buttons(text_size,
                    less_rounded,
                    widget,
                    widget_hover,
                    widget_text,
                    widget_selected,
                    disabled,
                    disabled_text):

            theme.clear_buttons()

            style.button.background = Box(widget, less_rounded)
            style.button.hover_background = Box(widget_hover, less_rounded)
            style.button.insensitive_background = Box(disabled, less_rounded)

            style.button_text.size = text_size
            style.button_text.color = widget_text
            style.button_text.selected_color = widget_selected
            style.button_text.insensitive_color = disabled_text

            if less_rounded:
                style.button.xpadding = 6
            else:
                style.button.xpadding = 12

            style.button.ypadding = 1
            style.button.xmargin = 1
            style.button.ymargin = 1

            style.button_text.xalign = 0.5
            style.button_text.yalign = 0.5
            style.button_text.text_align = 0.5

        setattr(theme, name + "_buttons", buttons)

        def large_buttons(
            text_size,
            less_rounded,
            widget,
            widget_hover,
            widget_text,
            widget_selected,
            disabled,
            disabled_text):

            theme.clear_large_buttons()

            if less_rounded:
                style.large_button.xpadding = 6
            else:
                style.large_button.xpadding = 12

            style.large_button.ypadding = 1
            style.large_button.xmargin = 1
            style.large_button.ymargin = 1

            style.large_button.background = Box(widget, less_rounded)
            style.large_button.hover_background = Box(widget_hover, less_rounded)
            style.large_button.insensitive_background = Box(disabled, less_rounded)

            style.large_button_text.size = text_size
            style.large_button_text.color = widget_text
            style.large_button_text.selected_color = widget_selected
            style.large_button_text.insensitive_color = disabled_text

            style.large_button_text.xalign = 0
            style.large_button_text.yalign = 0

        setattr(theme, name + "_large_buttons", large_buttons)

        def labels(
            text_size,
            label):

            theme.clear_labels()

            style.label_text.size = text_size
            style.label_text.color = label

        setattr(theme, name + "_labels", labels)

        def prompts(
            text_size,
            label):

            theme.clear_prompts()

            style.prompt_text.size = text_size
            style.prompt_text.color = label

            style.prompt.xalign = 0.5
            style.prompt_text.text_align = 0.5
            style.prompt_text.layout = "subtitle"

        setattr(theme, name + "_prompts", prompts)


        def bars(
            widget,
            widget_hover):

            theme.clear_bars()

            def img(name, color, x, y):
                rv = theme.OneOrTwoColor(file_prefix + name + ".png", color)
                if x is not None:
                    rv = Frame(rv, x, y, tile=True)
                return rv

            # Bars.
            style.bar.ymaximum = 24
            style.bar.left_gutter = 6
            style.bar.right_gutter = 6
            style.bar.thumb_offset = 6

            style.bar.left_bar = img("slider_full", widget, 12, 0)
            style.bar.right_bar = img("slider_empty", widget, 12, 0)
            style.bar.thumb = img("slider_thumb", widget, None, None)
            style.bar.hover_left_bar = img("slider_full", widget_hover, 12, 0)
            style.bar.hover_right_bar = img("slider_empty", widget_hover, 12, 0)
            style.bar.hover_thumb = img("slider_thumb", widget_hover, None, None)

            style.vbar.xmaximum = 24
            style.vbar.top_gutter = 6
            style.vbar.bottom_gutter = 6
            style.vbar.thumb_offset = 6

            style.vbar.bottom_bar = img("vslider_full", widget, 0, 12)
            style.vbar.top_bar = img("vslider_empty", widget, 0, 12)
            style.vbar.thumb = img("vslider_thumb", widget, None, None)
            style.vbar.hover_bottom_bar = img("vslider_full", widget_hover, 0, 12)
            style.vbar.hover_top_bar = img("vslider_empty", widget_hover, 0, 12)
            style.vbar.hover_thumb = img("vslider_thumb", widget_hover, None, None)

            # Sliders.
            style.slider.ymaximum = 24
            style.slider.left_gutter = 6
            style.slider.right_gutter = 6
            style.slider.thumb_offset = 6

            style.slider.left_bar = img("slider_full", widget, 12, 0)
            style.slider.right_bar = img("slider_empty", widget, 12, 0)
            style.slider.thumb = img("slider_thumb", widget, None, None)
            style.slider.hover_left_bar = img("slider_full", widget_hover, 12, 0)
            style.slider.hover_right_bar = img("slider_empty", widget_hover, 12, 0)
            style.slider.hover_thumb = img("slider_thumb", widget_hover, None, None)

            style.vslider.xmaximum = 24
            style.vslider.top_gutter = 6
            style.vslider.bottom_gutter = 6
            style.vslider.thumb_offset = 6

            style.vslider.bottom_bar = img("vslider_full", widget, 0, 12)
            style.vslider.top_bar = img("vslider_empty", widget, 0, 12)
            style.vslider.thumb = img("vslider_thumb", widget, None, None)
            style.vslider.hover_bottom_bar = img("vslider_full", widget_hover, 0, 12)
            style.vslider.hover_top_bar = img("vslider_empty", widget_hover, 0, 12)
            style.vslider.hover_thumb = img("vslider_thumb", widget_hover, None, None)


            # Scrollbars.
            style.scrollbar.left_gutter = 6
            style.scrollbar.right_gutter = 6
            style.scrollbar.thumb_offset = 6
            style.scrollbar.ymaximum = 12

            style.scrollbar.left_bar = img("scrollbar", widget, 12, 0)
            style.scrollbar.right_bar = img("scrollbar", widget, 12, 0)
            style.scrollbar.thumb = img("scrollbar_thumb", widget, None, None)
            style.scrollbar.hover_left_bar = img("scrollbar", widget_hover, 12, 0)
            style.scrollbar.hover_right_bar = img("scrollbar", widget_hover, 12, 0)
            style.scrollbar.hover_thumb = img("scrollbar_thumb", widget_hover, None, None)

            style.vscrollbar.top_gutter = 6
            style.vscrollbar.bottom_gutter = 6
            style.vscrollbar.thumb_offset = 6
            style.vscrollbar.xmaximum = 12

            style.vscrollbar.left_bar = img("vscrollbar", widget, 0, 12)
            style.vscrollbar.right_bar = img("vscrollbar", widget, 0, 12)
            style.vscrollbar.thumb = img("vscrollbar_thumb", widget, None, None)
            style.vscrollbar.hover_left_bar = img("vscrollbar", widget_hover, 0, 12)
            style.vscrollbar.hover_right_bar = img("vscrollbar", widget_hover, 0, 12)
            style.vscrollbar.hover_thumb = img("vscrollbar_thumb", widget_hover, None, None)

        setattr(theme, name + "_bars", bars)

        def main(
            widget = (0, 60, 120, 255),
            widget_hover = (0, 80, 160, 255),
            widget_text = (200, 225, 255, 255),
            widget_selected = (255, 255, 200, 255),
            disabled = (64, 64, 64, 255),
            disabled_text = (200, 200, 200, 255),
            label = (255, 255, 255, 255),
            frame = (100, 150, 200, 255),

            text_size=None,
            small_text_size=None,
            less_rounded = False,

            # Compat for the old roundrect theme.
            window = None,
            button_menu = None,
            rounded_window = True,
            outline_bars = False,
            mm_root = None,
            gm_root = None):

            if button_menu is None:
                if (config.script_version is not None) and (config.script_version < (6, 9, 0)):
                    button_menu = True
                else:
                    button_menu = False

            layout.defaults()

            if config.screen_width <= 640:
                text_size = text_size or 18
                small_text_size = small_text_size or 12
                less_rounded = True

            else:
                text_size = text_size or 22
                small_text_size = small_text_size or 16
                radius = 12

            frames(
                less_rounded,
                frame)

            buttons(
                text_size,
                less_rounded,
                widget,
                widget_hover,
                widget_text,
                widget_selected,
                disabled,
                disabled_text)

            large_buttons(
                small_text_size,
                less_rounded,
                widget,
                widget_hover,
                widget_text,
                widget_selected,
                disabled,
                disabled_text)

            labels(
                text_size,
                label)

            prompts(
                text_size,
                label)

            bars(
                widget,
                widget_hover)

            if mm_root is not None:
                style.mm_root.background = mm_root

            if gm_root is not None:
                style.gm_root.background = gm_root

            if window is not None:

                if rounded_window:
                    style.window.background = RoundRect(window, less_rounded)
                    style.window.xpadding = 6
                    style.window.xmargin = 6
                    style.window.ypadding = 6
                    style.window.ymargin = 6
                else:
                    style.window.background = Solid(window)
                    style.window.xpadding = 6
                    style.window.xmargin = 0
                    style.window.ypadding = 6
                    style.window.ymargin = 0


            if button_menu:
                layout.button_menu()

        setattr(theme, name, main)

    roundrect_based_theme("roundrect", "_roundrect/rr", RoundRect)
    roundrect_based_theme("bordered", "_theme_bordered/br")
    roundrect_based_theme("diamond", "_theme_diamond/d")
    roundrect_based_theme("tv", "_theme_tv/t")
    roundrect_based_theme("glow", "_theme_glow/g", None, "_outline.png")
    roundrect_based_theme("regal", "_theme_regal/re")
    roundrect_based_theme("crayon", "_theme_crayon/cry")
    roundrect_based_theme("threeD", "_theme_threeD/th")
    roundrect_based_theme("marker", "_theme_marker/ink")
    roundrect_based_theme("austen", "_theme_austen/au")

    @theme
    def ancient():

        layout.defaults()

        style.frame.background = Solid((0, 0, 128, 128))
        style.frame.xpadding = 10
        style.frame.ypadding = 10
        style.frame.xmargin = 10
        style.frame.ymargin = 5

        style.menu_frame.set_parent(style.default)

        dark_cyan = (0, 192, 255, 255)
        bright_cyan = (0, 255, 255, 255)
        dark_red = (255, 128, 128, 255)
        bright_red = (255, 64, 64, 255)
        green = (0, 128, 0, 255)

        style.button_text.color = dark_cyan
        style.button_text.hover_color = bright_cyan
        style.button_text.insensitive_color = (192, 192, 192, 255)
        style.button_text.size = 24
        style.button_text.drop_shadow = (2, 2)
        style.button_text.drop_shadow_color = "#000"

        style.button_text.selected_color = dark_red
        style.button_text.selected_hover_color = bright_red

        style.button_text.xalign = 0.5
        style.button_text.text_align = 0.5

        style.bar.ymaximum = 22
        style.bar.left_bar = Solid(bright_cyan)
        style.bar.right_bar = Solid((0, 0, 0, 128))
        style.bar.thumb = None
        style.bar.thumb_offset = 0
        style.bar.thumb_shadow = None

        style.vbar.xmaximum = 22
        style.vbar.bottom_bar = Solid(bright_cyan)
        style.vbar.top_bar = Solid((0, 0, 0, 128))
        style.vbar.thumb = None
        style.vbar.thumb_offset = 0
        style.vbar.thumb_shadow = None

        style.slider.ymaximum = 22
        style.slider.left_bar = Solid(bright_cyan)
        style.slider.right_bar = Solid((0, 0, 0, 128))
        style.slider.thumb = None
        style.slider.thumb_offset = 0
        style.slider.thumb_shadow = None

        style.vslider.xmaximum = 22
        style.vslider.bottom_bar = Solid(bright_cyan)
        style.vslider.top_bar = Solid((0, 0, 0, 128))
        style.vslider.thumb = None
        style.vslider.thumb_offset = 0
        style.vslider.thumb_shadow = None

        style.scrollbar.ymaximum = 22
        style.scrollbar.left_bar = Solid("#0008")
        style.scrollbar.right_bar = Solid("#0008")
        style.scrollbar.thumb = Solid(bright_cyan)
        style.scrollbar.thumb_offset = 0
        style.scrollbar.thumb_shadow = None

        style.vscrollbar.xmaximum = 22
        style.vscrollbar.top_bar = Solid("#0008")
        style.vscrollbar.bottom_bar = Solid("#0008")
        style.vscrollbar.thumb = Solid(bright_cyan)
        style.vscrollbar.thumb_offset = 0
        style.vscrollbar.thumb_shadow = None

        style.large_button.xpadding = 5
        style.large_button.ypadding = 2
        style.large_button.xmargin = 5
        style.large_button.ymargin = 2
        style.large_button.background = "#fff"
        style.large_button.hover_background = "#ffc"

        style.large_button_text.size = 16
        style.large_button_text.drop_shadow = (1, 1)
        style.large_button_text.xalign = 0
        style.large_button_text.text_align = 0

        style.label_text.size = 24
        style.label_text.color = green
        style.label_text.drop_shadow = (1, 1)
        style.label_text.drop_shadow_color = "#000"

        style.prompt_text.size = 24
        style.prompt_text.color = green
        style.prompt_text.layout = "subtitle"
        style.prompt_text.text_align = 0.5
        style.prompt_text.drop_shadow = (1, 1)
        style.prompt_text.drop_shadow_color = "#000"

        style.mm_root.background = "#e9d8bc"
        style.gm_root.background = "#e9d8bc"


    @theme
    def outline_frames():
        theme.clear_frames()

    @theme
    def outline_buttons(
        inside,
        idle,
        hover,
        selected,
        insensitive,
        text_size):

        theme.clear_buttons()

        style.button.xmargin = 4

        style.button_text.size = text_size
        style.button_text.color = inside
        style.button_text.outlines = [ (2, idle) ]
        style.button_text.hover_outlines = [ (2, hover) ]
        style.button_text.selected_outlines = [ (2, selected) ]
        style.button_text.selected_hover_outlines = [ (2, hover) ]
        style.button_text.insensitive_outlines = [ (2, insensitive) ]


    @theme
    def outline_large_buttons(
        inside,
        idle,
        hover,
        selected,
        insensitive,
        text_size,
        large_button):

        theme.clear_large_buttons()

        style.large_button.xmargin = 4
        style.large_button.ymargin = 2

        style.large_button.background = large_button

        style.large_button_text.size = text_size
        style.large_button_text.color = inside

        style.large_button_text.outlines = [ (2, idle) ]
        style.large_button_text.hover_outlines = [ (2, hover) ]
        style.large_button_text.selected_outlines = [ (2, selected) ]
        style.large_button_text.selected_hover_outlines = [ (2, hover) ]
        style.large_button_text.insensitive_outlines = [ (2, insensitive) ]

    @theme
    def outline_prompts(
        inside,
        prompt,
        text_size):

        theme.clear_prompts()

        style.prompt_text.color = inside
        style.prompt_text.outlines = [ (2, prompt) ]
        style.prompt_text.size = text_size

    @theme
    def outline_labels(
        inside,
        label,
        text_size):

        theme.clear_labels()

        style.label_text.color = inside
        style.label_text.outlines = [ (2, label) ]
        style.label_text.size = text_size

    @theme
    def outline_bars(
        inside,
        idle,
        hover):

        theme.clear_bars()

        def color(fn, c):
            return im.Twocolor("_outline/" + fn + ".png", inside, c)

        style.bar.ymaximum = 16
        style.bar.left_bar = Frame(color("circle", idle), 7, 0)
        style.bar.right_bar = Frame(color("bar", idle), 0, 0)
        style.bar.left_gutter = 16
        style.bar.bar_resizing = True

        style.slider.ymaximum = 16
        style.slider.left_bar = Frame(color("bar", idle), 0, 0)
        style.slider.right_bar = Frame(color("bar", idle), 0, 0)
        style.slider.thumb = color("circle", idle)
        style.slider.hover_left_bar = Frame(color("bar", hover), 0, 0)
        style.slider.hover_right_bar = Frame(color("bar", hover), 0, 0)
        style.slider.hover_thumb = color("circle", hover)

        style.scrollbar.ymaximum = 16
        style.scrollbar.left_bar = Frame(color("bar", idle), 0, 0)
        style.scrollbar.right_bar = Frame(color("bar", idle), 0, 0)
        style.scrollbar.thumb = Frame(color("circle", idle), 7, 0)
        style.scrollbar.hover_left_bar = Frame(color("bar", hover), 0, 0)
        style.scrollbar.hover_right_bar = Frame(color("bar", hover), 0, 0)
        style.scrollbar.hover_thumb = Frame(color("circle", hover), 7, 0)

        style.vbar.xmaximum = 16
        style.vbar.bottom_bar = Frame(color("circle", idle), 0, 7)
        style.vbar.top_bar = Frame(color("vbar", idle), 0, 0)
        style.vbar.bottom_gutter = 16
        style.vbar.bar_resizing = True

        style.vslider.xmaximum = 16
        style.vslider.top_bar = Frame(color("vbar", idle), 0, 0)
        style.vslider.bottom_bar = Frame(color("vbar", idle), 0, 0)
        style.vslider.thumb = color("circle", idle)
        style.vslider.hover_top_bar = Frame(color("vbar", hover), 0, 0)
        style.vslider.hover_bottom_bar = Frame(color("vbar", hover), 0, 0)
        style.vslider.hover_thumb = color("circle", hover)

        style.vscrollbar.xmaximum = 16
        style.vscrollbar.top_bar = Frame(color("vbar", idle), 0, 0)
        style.vscrollbar.bottom_bar = Frame(color("vbar", idle), 0, 0)
        style.vscrollbar.thumb = Frame(color("circle", idle), 0, 7)
        style.vscrollbar.hover_top_bar = Frame(color("vbar", hover), 0, 0)
        style.vscrollbar.hover_bottom_bar = Frame(color("vbar", hover), 0, 0)
        style.vscrollbar.hover_thumb = Frame(color("circle", hover), 0, 7)

    @theme
    def outline(
        inside="#fff",
        idle="#e66",
        hover="#48f",
        selected="#84f",
        insensitive="#ccc",
        label="#484",
        prompt="#484",
        background="#fee",
        large_button="#fff8f8",
        text_size=22,
        small_text_size=16,
        ):

        layout.defaults()

        theme.outline_frames()

        theme.outline_buttons(
            inside,
            idle,
            hover,
            selected,
            insensitive,
            text_size)

        theme.outline_large_buttons(
            inside,
            idle,
            hover,
            selected,
            insensitive,
            small_text_size,
            large_button)

        theme.outline_prompts(
            inside,
            prompt,
            text_size)

        theme.outline_labels(
            inside,
            label,
            text_size)

        theme.outline_bars(
            inside,
            idle,
            hover)

        style.mm_root.background = background
        style.gm_root.background = background

    @theme
    def image_buttons(d):
        for k, (idle, hover, selected_idle, selected_hover, insensitive) in d.iteritems():
            s = style.button[k]
            s.xpadding = 0
            s.ypadding = 0
            s.background = None
            s.foreground = None
            s.idle_child = idle
            s.hover_child = hover
            s.selected_idle_child = selected_idle
            s.selected_hover_child = selected_hover
            s.insensitive_child = insensitive
            s.focus_mask = True


    @theme
    def image_labels(d):
        for k, l in d.iteritems():
            s = style.label[k]
            s.xpadding = 0
            s.ypadding = 0
            s.background = None
            s.foreground = None
            s.child = k


    config.image_buttons = { }
    config.image_labels = { }

# Theme: A White Tulip
# Coding: Jake Staines (http://www.eviscerate.net/)
# Graphics: Ren (http://x-Ren-x.deviantart.com/)
# Font: Andrew Paglinawan (www.andrewpaglinawan.com)
init -1110 python:

    def __AWTBox(colour):
        base_image = im.MatrixColor("_theme_awt/frame.png", im.matrix.opacity(0.45))
        colour_tint = im.MatrixColor("_theme_awt/frame.png", im.matrix.colorize(colour, colour))
        colour_tint = im.MatrixColor(colour_tint, im.matrix.opacity(0.4))
        frame_image = im.Composite(
                                        (220, 147),
                                        (0, 0), base_image,
                                        (0, 0), colour_tint,
                                        (0, 0), "_theme_awt/frame_overlay.png"
                                        )

        return Frame(frame_image, 4, 4)

    def __AWTButton(image, colour, highlight, low_sat=False):
        base_image = "_theme_awt/" + image + ".png"
        colour_tint = im.MatrixColor("_theme_awt/" + image + ".png", im.matrix.colorize(colour, colour))
        opacity = 0.5
        if highlight:
            opacity = 0.3
        if low_sat:
            opacity = opacity * 0.4
        colour_tint = im.MatrixColor(colour_tint, im.matrix.opacity(opacity))
        if highlight:
            button_image = im.Composite(
                                            (203, 47),
                                            (0, 0), base_image,
                                            (0, 0), colour_tint,
                                            (0, 0), "_theme_awt/" + image + "_overlay_highlight.png"
                                            )
        else:
            button_image = im.Composite(
                                            (203, 47),
                                            (0, 0), base_image,
                                            (0, 0), colour_tint,
                                            (0, 0), "_theme_awt/" + image + "_overlay.png"
                                            )

        return Frame(button_image, 4, 6)

    def __AWTBullet(image):
        return Transform(image, yalign=0.5, xalign=0.0)

init -1110 python hide:

    @theme
    def a_white_tulip_frames(frame):

        theme.clear_frames()

        style.frame.background = __AWTBox(frame)

        style.frame.xpadding = 9
        style.frame.ypadding = 9

    @theme
    def a_white_tulip_buttons(text_size,
            widget,
            widget_hover,
            widget_text,
            widget_selected,
            disabled,
            disabled_text,
            small,
            font="_theme_awt/Quicksand-Regular.ttf"):

        theme.clear_buttons()

        style.button.background = __AWTButton("button", widget, False)
        style.button.hover_background = __AWTButton("button", widget_hover, True)
        style.button.selected_background = __AWTButton("button_selected", widget_hover, False, low_sat=True)
        style.button.selected_hover_background = __AWTButton("button_selected", widget_hover, True, low_sat=True)
        style.button.insensitive_background = __AWTButton("button", disabled, False)

        style.button_text.font = font
        style.button_text.size = text_size
        style.button_text.color = widget_text

        style.button_text.selected_color = widget_text
        style.button_text.selected_xoffset = 2
        style.button_text.selected_yoffset = 2

        style.button_text.insensitive_color = "#0000"


        style.button_text.outlines = [
                                                        (2, "#20202008", 2, 2),
                                                        (1, "#40404015", 2, 2),
                                                        (0, "#80808030", 2, 2),
                                                        (0, widget_text, 1, 0),

                                                    ]

        style.button_text.hover_outlines = [
                                                        (2, "#20202008", 2, 2),
                                                        (1, "#40404015", 2, 2),
                                                        (0, "#80808030", 2, 2),
                                                        (0, widget_text, 1, 0),
                                                    ]

        style.button_text.selected_outlines = [
                                                        (2, "#20202008", 2, 2),
                                                        (1, "#40404015", 2, 2),
                                                        (0, "#80808030", 2, 2),
                                                        (0, widget_text, 1, 0),
                                                    ]

        style.button_text.insensitive_outlines = [
                                                        (1, "#fff4", 2, 1),
                                                        (1, "#3334", 0, -1),
                                                    ]


        style.button.xpadding = 9

        if small:
            style.button.ypadding = 2
        else:
            style.button.ypadding = 6

        style.button.xmargin = 3
        style.button.ymargin = 3

        style.button_text.xalign = 0.5
        style.button_text.yalign = 0.5
        style.button_text.text_align = 0.5

        # Radio Buttons

        def set_radio_style(s, colour):

            selected = im.MatrixColor("_theme_awt/radio_base.png", im.matrix.colorize(colour, colour))
            selected = im.MatrixColor(selected, im.matrix.opacity(0.75))
            selected = im.Composite( (17, 18),
                                                (0, 0), "_theme_awt/radio_unselected.png",
                                                (0, 0), "_theme_awt/radio_base.png",
                                                (0, 0), selected,
                                                (0, 0), "_theme_awt/radio_base_overlay.png"
                                                )

            hover = im.MatrixColor("_theme_awt/radio_base.png", im.matrix.colorize(colour, colour))
            hover = im.MatrixColor(hover, im.matrix.opacity(0.75))
            hover = im.Composite( (17, 18),
                                                (0, 0), "_theme_awt/radio_unselected.png",
                                                (0, 0), "_theme_awt/radio_base.png",
                                                (0, 0), hover,
                                                (0, 0), "_theme_awt/radio_selected_hover.png"
                                                )

            s.background = __AWTBullet("_theme_awt/radio_unselected.png")
            s.hover_background = __AWTBullet("_theme_awt/radio_unselected_hover.png")
            s.insensitive_background = __AWTBullet("_theme_awt/radio_unselected.png")
            s.selected_background = __AWTBullet(selected)
            s.selected_hover_background = __AWTBullet(hover)

            s.left_padding = 23
            s.left_margin = 10

        def set_radio_text_style(s):
            s.selected_color = widget_text
            s.xoffset = 2
            s.yoffset = 2


            s.xalign = 0.0
            s.text_align = 0.0

        set_radio_style(style.radio_button, widget)
        set_radio_text_style(style.radio_button_text)

        set_radio_style(style.check_button, widget)
        set_radio_text_style(style.check_button_text)

    @theme
    def a_white_tulip_large_buttons(text_size,
            widget,
            widget_hover,
            widget_text,
            widget_selected,
            disabled,
            disabled_text,
            small,
            font="_theme_awt/Quicksand-Regular.ttf"):

        theme.clear_large_buttons()

        style.large_button.background = __AWTButton("button", widget, False)
        style.large_button.hover_background = __AWTButton("button", widget_hover, True)
        style.large_button.selected_background = __AWTButton("button_selected", widget_hover, False)
        style.large_button.selected_hover_background = __AWTButton("button_selected", widget_hover, True)
        style.large_button.insensitive_background = __AWTButton("button", disabled, False)

        style.large_button_text.font = font
        style.large_button_text.size = text_size
        style.large_button_text.color = widget_text
        style.large_button_text.selected_color = widget_selected
        style.large_button_text.insensitive_color = disabled_text

        style.large_button_text.outlines = [
                                                        (2, "#20202008", 2, 2),
                                                        (1, "#40404015", 2, 2),
                                                        (0, "#80808030", 2, 2),
                                                        (0, widget_text, 1, 0),
                                                    ]

        style.large_button_text.selected_outlines = [
                                                        (2, "#20202008", 2, 2),
                                                        (1, "#40404015", 2, 2),
                                                        (0, "#80808030", 2, 2),
                                                        (0, widget_selected, 1, 0),
                                                    ]

        style.large_button_text.insensitive_outlines = [
                                                        (2, "#20202008", 2, 2),
                                                        (1, "#40404015", 2, 2),
                                                        (0, "#80808030", 2, 2),
                                                        (0, disabled_text, 1, 0),
                                                    ]


        style.large_button.xpadding = 9

        if small:
            style.large_button.top_padding = 2
            style.large_button.bottom_padding = 4
        else:
            style.large_button.top_padding = 6
            style.large_button.bottom_padding = 9

        style.large_button.xmargin = 3
        style.large_button.ymargin = 3

        style.large_button_text.xalign = 0.5
        style.large_button_text.yalign = 0.5
        style.large_button_text.text_align = 0.5

    @theme
    def a_white_tulip_labels(
        text_size,
        label):

        theme.clear_labels()

        style.label_text.size = text_size
        style.label_text.color = label
        style.label_text.outlines = [
                                                        (0, label, 1, 0),
                                                        (1, "#FFF", 0, 0),
                                                        (1, "#FFF", 1, 0),
                                                        (2, "#FFF4", 0, 0),
                                                        (2, "#FFF4", 1, 0),

                                                    ]

        style.label.bottom_margin = 5

    @theme
    def a_white_tulip_prompts(
            text_size,
            label):

        theme.clear_prompts()

        style.prompt_text.size = text_size
        style.prompt_text.color = label

        style.prompt.xalign = 0.5
        style.prompt_text.text_align = 0.5
        style.prompt_text.layout = "subtitle"

    @theme
    def a_white_tulip_bars(
            widget,
            widget_hover):

        theme.clear_bars()

        def img(name, colour, width, height, x, y):
            i = im.MatrixColor("_theme_awt/" + name + ".png", im.matrix.colorize(colour, colour))
            i = im.MatrixColor(i, im.matrix.opacity(0.5))
            i = im.Composite(
                (width, height),
                (0, 0), "_theme_awt/" + name + ".png",
                (0, 0), i,
                )
            if x is not None:
                i = Frame(i, x, y, tile=True)
            return i

        def himg(name, colour, width, height, x, y):
            i = im.MatrixColor("_theme_awt/" + name + ".png", im.matrix.colorize(colour, colour))
            i = im.MatrixColor(i, im.matrix.opacity(0.5))
            i = im.Composite(
                (width, height),
                (0, 0), "_theme_awt/" + name + ".png",
                (0, 0), i,
                (0, 0), "_theme_awt/" + name + "_overlay.png"
                )
            if x is not None:
                i = Frame(i, x, y, tile=True)
            return i

        # Bars.
        style.bar.ymaximum = 27
        style.bar.left_gutter = 14
        style.bar.right_gutter = 12
        style.bar.thumb_offset = 10

        style.bar.left_bar = himg("bar_full", widget, 42, 27, 13, 0)
        style.bar.right_bar = Frame("_theme_awt/slider_empty_all.png", 13, 0, tile=True)
        style.bar.thumb = himg("bar_thumb", widget, 20, 25, None, None)

        style.vbar.xmaximum = 27
        style.vbar.top_gutter = 11
        style.vbar.bottom_gutter = 14
        style.vbar.thumb_offset = 10

        style.vbar.right_bar = himg("v_bar_full", widget, 27, 42, 0, 15)
        style.vbar.left_bar = Frame("_theme_awt/vslider_empty_all.png", 0, 13, tile=True)
        style.vbar.thumb = himg("v_bar_thumb", widget, 25, 20, None, None)


        # Sliders
        style.slider.ymaximum = 27
        style.slider.left_gutter = 13
        style.slider.right_gutter = 12
        style.slider.thumb_offset = 14.5

        style.slider.left_bar = himg("slider_full", widget, 42, 27, 13, 0)
        style.slider.right_bar = Frame("_theme_awt/slider_empty_all.png", 13, 0, tile=True)
        style.slider.thumb = himg("vthumb", widget, 29, 30, None, None)

        style.slider.hover_left_bar = himg("slider_full", widget_hover, 42, 27, 13, 0)
        style.slider.hover_thumb = himg("vthumb", widget_hover, 29, 30, None, None)

        style.vslider.xmaximum = 27
        style.vslider.top_gutter = 14
        style.vslider.bottom_gutter = 10
        style.vslider.thumb_offset = 15

        style.vslider.right_bar = himg("vslider_full", widget, 27, 42, 0, 13)
        style.vslider.left_bar = Frame("_theme_awt/vslider_empty_all.png", 0, 13, tile=True)
        style.vslider.thumb = himg("vthumb", widget, 29, 30, None, None)

        style.vslider.hover_right_bar = himg("vslider_full", widget_hover, 27, 42, 0, 13)
        style.vslider.hover_thumb = himg("vthumb", widget_hover, 29, 30, None, None)

        # Scrollbars.
        style.scrollbar.left_gutter = 30
        style.scrollbar.right_gutter = 30
        style.scrollbar.thumb_offset = 32.5
        style.scrollbar.ymaximum = 27

        style.scrollbar.left_bar = Frame("_theme_awt/slider_empty_all.png", 13, 0, tile=True)
        style.scrollbar.right_bar = Frame("_theme_awt/slider_empty_all.png", 13, 0, tile=True)
        style.scrollbar.thumb = himg("scroller", widget, 65, 29, None, None)

        style.scrollbar.hover_left_bar = Frame("_theme_awt/slider_empty_all.png", 13, 0, tile=True)
        style.scrollbar.hover_thumb = himg("scroller", widget_hover, 65, 29, None, None)

        style.vscrollbar.top_gutter = 30
        style.vscrollbar.bottom_gutter = 29
        style.vscrollbar.thumb_offset = 32.5
        style.vscrollbar.xmaximum = 27

        style.vscrollbar.left_bar = Frame("_theme_awt/vslider_empty_all.png", 0, 13, tile=True)
        style.vscrollbar.right_bar = Frame("_theme_awt/vslider_empty_all.png", 0, 13, tile=True)
        style.vscrollbar.thumb = himg("vscroller", widget, 28, 65, None, None)

        style.vscrollbar.hover_left_bar = Frame("_theme_awt/vslider_empty_all.png", 0, 13, tile=True)
        style.vscrollbar.hover_thumb = himg("vscroller", widget_hover, 28, 65, None, None)

    @theme
    def a_white_tulip(
            widget = "#c1c6d3",
            widget_hover = "#d7dbe5",
            widget_text = "#6b6b6b",
            widget_selected = "#c1c6d3",
            disabled = "#b4b4b4",
            disabled_text = "#6b6b6b",
            label = "#6b6b6b",
            frame = "#9391c9",
            text_size=None,
            small_text_size=None,
            window = None,
            button_menu = None,
            mm_root = "#ffffff",
            gm_root = "#ffffff",
            regular_font = "_theme_awt/Quicksand-Regular.ttf",
            bold_font = "_theme_awt/Quicksand-Bold.ttf",

            # for compatibility - unused:
            **properties
            ):

        # First off, we're hard-coding the text because we're already making everything
        # brighter and whiter than it was before, so light-coloured text - even when it was
        # previously over a dark background - just won't look right.

        widget_text = "#636363"
        disabled_text = "#6b6b6b"
        label = "#6b6b6b"

        if button_menu is None:
            if (config.script_version is not None) and (config.script_version < (6, 9, 0)):
                button_menu = True
            else:
                button_menu = False

        layout.defaults()

        small = False

        if config.screen_width <= 640:
            text_size = text_size or 12
            small_text_size = small_text_size or 8
            small = True
        else:
            text_size = text_size or 17
            small_text_size = small_text_size or 12

        theme.a_white_tulip_frames(frame)

        theme.a_white_tulip_buttons(
            text_size,
            widget,
            widget_hover,
            widget_text,
            widget_selected,
            disabled,
            disabled_text,
            small)

        theme.a_white_tulip_large_buttons(
            small_text_size,
            widget,
            widget_hover,
            widget_text,
            widget_selected,
            disabled,
            disabled_text,
            small)

        theme.a_white_tulip_labels(
            text_size,
            label)

        theme.a_white_tulip_prompts(
            text_size,
            label)

        theme.a_white_tulip_bars(
            widget,
            widget_hover)

        if mm_root is not None:
            style.mm_root.background = mm_root

        if gm_root is not None:
            style.gm_root.background = gm_root

        if window is None:
            window = frame

        style.window.background = __AWTBox(window)
        style.window.xpadding = 9
        style.window.xmargin = 6
        style.window.top_padding = 9
        style.window.bottom_padding = 35
        style.window.ymargin = 6

        style.say_dialogue.font = regular_font
        style.say_dialogue.color = widget_text
        style.say_dialogue.outlines = [
                                                    (0, widget_text, 1, 0)
                                                ]

        style.say_label.font = bold_font
        style.say_label.color = widget_text
        style.say_label.outlines = [
                                                    (2, "#20202008", 2, 2),
                                                    (1, "#40404015", 2, 2),
                                                    (0, "#80808030", 2, 2)
                                                ]

        if button_menu:
            layout.button_menu()

        style.quick_button.bottom_margin = 15
        style.quick_button.right_margin = 15

        style.file_picker_text.first_indent = 9
        style.file_picker_text.rest_indent = 9


init 1400 python:

    if not "compat" in _layout.provided:
        theme.image_buttons(config.image_buttons)
        theme.image_labels(config.image_labels)
