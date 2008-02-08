# Copyright 2004-2008 PyTom
#
# Please see the LICENSE.txt distributed with Ren'Py for permission to
# copy and modify.

init -1110 python:

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

    @theme
    def roundrect_frames(
        less_rounded,
        frame):

        theme.clear_frames()
        
        style.frame.background = RoundRect(frame, less_rounded)

        style.frame.xpadding = 6
        style.frame.ypadding = 6
        
            
    @theme
    def roundrect_buttons(text_size,
                          less_rounded,
                          widget,
                          widget_hover,
                          widget_text,
                          widget_selected,
                          disabled,
                          disabled_text):

        theme.clear_buttons()
        
        style.button.background = RoundRect(widget, less_rounded)
        style.button.hover_background = RoundRect(widget_hover, less_rounded)
        style.button.insensitive_background = RoundRect(disabled, less_rounded)

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

    @theme
    def roundrect_large_buttons(
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
        
        style.large_button.background = RoundRect(widget, less_rounded)
        style.large_button.hover_background = RoundRect(widget_hover, less_rounded)
        style.large_button.insensitive_background = RoundRect(disabled, less_rounded)

        style.large_button_text.size = text_size
        style.large_button_text.color = widget_text
        style.large_button_text.selected_color = widget_selected
        style.large_button_text.insensitive_color = disabled_text

        style.large_button_text.xalign = 0
        style.large_button_text.yalign = 0

    @theme
    def roundrect_labels(
        text_size,
        label):

        theme.clear_labels()
        
        style.label_text.size = text_size
        style.label_text.color = label

    @theme
    def roundrect_prompts(
        text_size,
        label):

        theme.clear_prompts()

        style.prompt_text.size = text_size
        style.prompt_text.color = label
        
        style.prompt.xalign = 0.5
        style.prompt_text.text_align = 0.5
        style.prompt_text.layout = "subtitle"
        
    @theme
    def roundrect_bars(
        widget,
        widget_hover):

        theme.clear_bars()
        
        def img(name, color, x, y):
            rv = theme.OneOrTwoColor("_roundrect/" + name + ".png", color)
            if x is not None:
                rv = Frame(rv, x, y)
            return rv

        # Bars.
        style.bar.ymaximum = 24
        style.bar.left_gutter = 6
        style.bar.right_gutter = 6
        style.bar.thumb_offset = 6

        style.bar.left_bar = img("rrslider_full", widget, 12, 0)
        style.bar.right_bar = img("rrslider_empty", widget, 12, 0)
        style.bar.thumb = img("rrslider_thumb", widget, None, None)
        style.bar.hover_left_bar = img("rrslider_full", widget_hover, 12, 0)
        style.bar.hover_right_bar = img("rrslider_empty", widget_hover, 12, 0)
        style.bar.hover_thumb = img("rrslider_thumb", widget_hover, None, None)

        style.vbar.xmaximum = 24
        style.vbar.top_gutter = 6
        style.vbar.bottom_gutter = 6
        style.vbar.thumb_offset = 6

        style.vbar.bottom_bar = img("rrvslider_full", widget, 0, 12)
        style.vbar.top_bar = img("rrvslider_empty", widget, 0, 12)
        style.vbar.thumb = img("rrvslider_thumb", widget, None, None)
        style.vbar.hover_bottom_bar = img("rrvslider_full", widget_hover, 0, 12)
        style.vbar.hover_top_bar = img("rrvslider_empty", widget_hover, 0, 12)
        style.vbar.hover_thumb = img("rrvslider_thumb", widget_hover, None, None)

        # Sliders.
        style.slider.ymaximum = 24
        style.slider.left_gutter = 6
        style.slider.right_gutter = 6
        style.slider.thumb_offset = 6

        style.slider.left_bar = img("rrslider_full", widget, 12, 0)
        style.slider.right_bar = img("rrslider_empty", widget, 12, 0)
        style.slider.thumb = img("rrslider_thumb", widget, None, None)
        style.slider.hover_left_bar = img("rrslider_full", widget_hover, 12, 0)
        style.slider.hover_right_bar = img("rrslider_empty", widget_hover, 12, 0)
        style.slider.hover_thumb = img("rrslider_thumb", widget_hover, None, None)

        style.vslider.xmaximum = 24
        style.vslider.top_gutter = 6
        style.vslider.bottom_gutter = 6
        style.vslider.thumb_offset = 6

        style.vslider.bottom_bar = img("rrvslider_full", widget, 0, 12)
        style.vslider.top_bar = img("rrvslider_empty", widget, 0, 12)
        style.vslider.thumb = img("rrvslider_thumb", widget, None, None)
        style.vslider.hover_bottom_bar = img("rrvslider_full", widget_hover, 0, 12)
        style.vslider.hover_top_bar = img("rrvslider_empty", widget_hover, 0, 12)
        style.vslider.hover_thumb = img("rrvslider_thumb", widget_hover, None, None)

        
        # Scrollbars.
        style.scrollbar.left_gutter = 6
        style.scrollbar.right_gutter = 6
        style.scrollbar.thumb_offset = 6
        style.scrollbar.ymaximum = 12

        style.scrollbar.left_bar = img("rrscrollbar", widget, 12, 0)
        style.scrollbar.right_bar = img("rrscrollbar", widget, 12, 0)
        style.scrollbar.thumb = img("rrscrollbar_thumb", widget, None, None)
        style.scrollbar.hover_left_bar = img("rrscrollbar", widget_hover, 12, 0)
        style.scrollbar.hover_right_bar = img("rrscrollbar", widget_hover, 12, 0)
        style.scrollbar.hover_thumb = img("rrscrollbar_thumb", widget_hover, None, None)
        
        style.vscrollbar.top_gutter = 6
        style.vscrollbar.bottom_gutter = 6
        style.vscrollbar.thumb_offset = 6
        style.vscrollbar.xmaximum = 12

        style.vscrollbar.left_bar = img("rrvscrollbar", widget, 0, 12)
        style.vscrollbar.right_bar = img("rrvscrollbar", widget, 0, 12)
        style.vscrollbar.thumb = img("rrvscrollbar_thumb", widget, None, None)
        style.vscrollbar.hover_left_bar = img("rrvscrollbar", widget_hover, 0, 12)
        style.vscrollbar.hover_right_bar = img("rrvscrollbar", widget_hover, 0, 12)
        style.vscrollbar.hover_thumb = img("rrvscrollbar_thumb", widget_hover, None, None)

    @theme
    def roundrect(
        widget = (0, 60, 120, 255),
        widget_hover = (0, 80, 160, 255),
        widget_text = (200, 225, 255, 255),
        widget_selected = (255, 255, 200, 255),
        disabled = (64, 64, 64, 255),
        disabled_text = (200, 200, 200, 255),
        label = (255, 255, 255, 255),
        frame = (100, 150, 200, 255),
        window = (0, 0, 0, 192),
        mm_root = Solid((220, 235, 255, 255)),
        gm_root = Solid((220, 235, 255, 255)),
        
        text_size=None,
        small_text_size=None,
        less_rounded = False,        
        
        # Compat for the old roundrect theme.
        window = None,
        button_menu = True,
        rounded_window = True,
        outline_bars = False,

        mm_root = None,
        gm_root = None):

        layout.defaults()
        
        if config.screen_width <= 640:
            text_size = text_size or 18
            small_text_size = small_text_size or 12
            less_rounded = True
            
        else:
            text_size = text_size or 22
            small_text_size = small_text_size or 16
            radius = 12

        theme.roundrect_frames(
            less_rounded,
            frame)

        theme.roundrect_buttons(
            text_size,
            less_rounded,
            widget,
            widget_hover,
            widget_text,
            widget_selected,
            disabled,
            disabled_text)

        theme.roundrect_large_buttons(
            small_text_size,
            less_rounded,
            widget,
            widget_hover,
            widget_text,
            widget_selected,
            disabled,
            disabled_text)

        theme.roundrect_labels(
            text_size,
            label)

        theme.roundrect_prompts(
            text_size,
            label)

        theme.roundrect_bars(
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


    theme.outline_drop_shadow = [
        (0, -2),
        (-1, -1), (0, -1), (1, -1),
        (-2, 0), (-1, 0), (1, 0), (2, 0),
        (-1, 1), (0, 1), (1, 1),
        (0, 2)
        ]

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
        style.button_text.drop_shadow = theme.outline_drop_shadow
        style.button_text.drop_shadow_color = idle
        style.button_text.hover_drop_shadow_color = hover
        style.button_text.selected_drop_shadow_color = selected
        style.button_text.selected_hover_drop_shadow_color = hover
        style.button_text.insensitive_drop_shadow_color = insensitive
        

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
        style.large_button_text.drop_shadow = theme.outline_drop_shadow
        style.large_button_text.drop_shadow_color = idle
        style.large_button_text.hover_drop_shadow_color = hover
        style.large_button_text.selected_drop_shadow_color = selected
        style.large_button_text.selected_hover_drop_shadow_color = hover
        style.large_button_text.insensitive_drop_shadow_color = insensitive
        
    @theme
    def outline_prompts(
        inside,
        prompt,
        text_size):

        theme.clear_prompts()
        
        style.prompt_text.color = inside
        style.prompt_text.drop_shadow = theme.outline_drop_shadow
        style.prompt_text.drop_shadow_color = prompt
        style.prompt_text.size = text_size
        
    @theme
    def outline_labels(
        inside,
        label,
        text_size):

        theme.clear_labels()
        
        style.label_text.color = inside
        style.label_text.drop_shadow = theme.outline_drop_shadow
        style.label_text.drop_shadow_color = label
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

init 1110 python:

    if not "compat" in _layout.provided:
        theme.image_buttons(config.image_buttons)
        theme.image_labels(config.image_labels)
        
    
    
        
