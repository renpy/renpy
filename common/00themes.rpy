# Copyright 2004-2006 PyTom
#
# Please see the LICENSE.txt distributed with Ren'Py for permission to
# copy and modify.

init -402:
    python:

        _roundrect_radius = 12

        def RoundRect(color, size=None):
            """
            Creates a roundrect displayable. Size should be one of
            6 or 12, while color is the color of the roundrect.
            """

            if size is None:
                size = _roundrect_radius

            return Frame(im.Color("rr%d.png" % size, color), size, size)
            
        def _display_button_menu(menuitems):

            narration = [ s for s, i in menuitems if i is None and s ]
            menuitems = [ (s, i) for s, i in menuitems if i is not None or not s ]

            if narration:
                renpy.say(None, "\n".join(narration), interact=False)

            return renpy.display_menu(menuitems)

        def _button_menu():

            store.menu = _display_button_menu

            style.menu.clear()

            style.menu.box_spacing = 2

            style.menu_window.clear()
            style.menu_window.take(style.default)
            style.menu_window.xpos = 0.5
            style.menu_window.xanchor = 0.5
            style.menu_window.ypos = 0.5
            style.menu_window.yanchor = 0.5

            style.menu_choice.clear()
            style.menu_choice.take(style.button_text)

            style.menu_choice_button.clear()
            style.menu_choice_button.take(style.button)

            style.menu_choice_chosen.clear()
            style.menu_choice_chosen_button.clear()

            style.menu_choice_button.xminimum = int(config.screen_width * 0.75)
            style.menu_choice_button.xmaximum = int(config.screen_width * 0.75)



    python hide:

        store.theme = object()
        
        def theme_roundrect(
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
            centered = False,
            button_menu = True,
            ):

            """This enables the use of the roundrect theme. By
               default, this theme styles the game in a blue color
               scheme. However, by supplying one or more of the
               parameters given below, the color scheme can be
               changed.

               @param widget: The background color of non-focued
               buttons and sliders.

               @param widget_hover: The background color of focused
               buttons and sliders.

               @param widget_text: The text color of non-selected buttons.

               @param widget_selected: The text color of selected buttons.

               @param disabled: The background color of disabled buttons.

               @param disabled_text: The text color of disabled buttons.

               @param label: The text color of non-selected labels.

               @param frame: The background color of frames.

               @param mm_root: A displayable (such as
               an Image or Solid) that will be used as
               the background for the main menu.

               @param gm_root: A displayable (such as
               an Image or Solid) that will be used as
               the background for the game menu.

               @param centered: If True, the buttons and sliders will
               be centered in the frames or windows that contain
               them. If False, the default, they will be pushed to the
               right side.
               """

            if config.screen_width <= 640:
                size = 18
                small = 14

                big = False

                spacing = 0
                pref_spacing = 5
                title_spacing = 6

                frame_width = 200
                widget_width = 160

                config.thumbnail_width = 60
                config.thumbnail_height = 45

                config.file_page_cols = 2
                config.file_page_rows = 4
                # style.file_picker_frame.xmaximum = 450

                prefcols = [ 110, 320, 530 ]
                nav_xpos = 530

            else:

                size = 22
                small = 18

                big = True

                spacing = 0
                pref_spacing = 10
                title_spacing = 12

                frame_width = 250
                widget_width = 200

                prefcols = [ 137, 400, 663 ]

                if config.screen_width == 800:
                    nav_xpos = 663
                else:
                    nav_xpos = 5.0 / 6.0

            rrslider_empty = "rrslider_empty.png"
            rrslider_full = "rrslider_full.png"
            rrslider_thumb = "rrslider_thumb.png"
            rrslider_radius = 6
            rrslider_height = 24


            def rrframe(sty):
                sty.background = RoundRect(frame)
                sty.xpadding = 6
                sty.ypadding = 6

            if big:
                store._roundrect_radius = 12
            else:
                store._roundrect_radius = 6

            style.button.clear()
            style.button.background = RoundRect(widget)
            style.button.hover_background = RoundRect(widget_hover)
            style.button.xminimum = widget_width
            style.button.ypadding = 1
            style.button.xpadding = _roundrect_radius
            style.button.xmargin = 1
            style.button.ymargin = 1

            style.button_text.clear()
            style.button_text.drop_shadow = None
            style.button_text.color = widget_text
            style.button_text.size = size
            style.button_text.xpos = 0.5
            style.button_text.xanchor = 0.5
            style.button_text.ypos = 0.5
            style.button_text.yanchor = 0.5
            style.button_text.textalign = 0.5 

            style.button.insensitive_background = RoundRect(disabled)
            style.button_text.insensitive_color = disabled_text

            style.button_text.selected_color = widget_selected 

            style.menu_button.clear()
            
            style.mm_root.background = mm_root
            style.gm_root.background = gm_root

            style.mm_menu_frame_vbox.box_spacing = spacing
            rrframe(style.mm_menu_frame)
            style.mm_menu_frame.xpos = nav_xpos
            style.mm_menu_frame.xanchor = 0.5

            style.gm_nav_vbox.box_spacing = spacing
            rrframe(style.gm_nav_frame)
            style.gm_nav_frame.xpos = nav_xpos
            style.gm_nav_frame.xanchor = 0.5

            rrframe(style.prefs_pref_frame)
            del style.prefs_pref_frame.bottom_margin
            style.prefs_pref_frame.xfill = True

            style.prefs_pref_vbox.box_spacing = spacing
            style.prefs_pref_vbox.box_first_spacing = title_spacing
            style.prefs_pref_vbox.xfill = True

            style.prefs_frame.ypadding = pref_spacing

            style.prefs_column.box_spacing = pref_spacing
            style.prefs_column.xmaximum = frame_width

            style.prefs_left.xpos = prefcols[0]
            style.prefs_center.xpos = prefcols[1]
            style.prefs_right.xpos = prefcols[2]

            style.prefs_label.color = label
            style.prefs_label.size = size
            style.prefs_label.drop_shadow = 0
            style.prefs_label.xpos = 0
            style.prefs_label.xanchor = 0

            if centered:
                style.prefs_button.xpos = 0.5
                style.prefs_button.xanchor = 0.5
            else:
                style.prefs_button.xpos = 1.0
                style.prefs_button.xanchor = 1.0


            style.bar.ymaximum = rrslider_height
            style.bar.left_gutter = rrslider_radius
            style.bar.right_gutter = rrslider_radius
            style.bar.thumb_offset = -rrslider_radius

            style.prefs_slider.xmaximum=widget_width
            del style.prefs_slider.ymaximum

            style.bar.left_bar = Frame(im.Color(rrslider_full, widget), rrslider_radius * 2, 0)
            style.bar.right_bar = Frame(im.Color(rrslider_empty, widget), rrslider_radius * 2, 0)
            style.bar.thumb = im.Color(rrslider_thumb, widget)

            style.bar.hover_left_bar = Frame(im.Color(rrslider_full, widget_hover), rrslider_radius * 2, 0)
            style.bar.hover_right_bar = Frame(im.Color(rrslider_empty, widget_hover), rrslider_radius * 2, 0)
            style.bar.hover_thumb = im.Color(rrslider_thumb, widget_hover)

            if centered:
                style.prefs_slider.xpos = 0.5
                style.prefs_slider.xanchor = 0.5
            else:                
                style.prefs_slider.xpos = 1.0
                style.prefs_slider.xanchor = 1.0

            style.soundtest_button.xminimum = 0

            # Joystick

            style.prefs_joystick.xmaximum = 600
            style.prefs_joystick.xpos = 0.5
            style.prefs_joystick.xanchor = 0.5
            style.prefs_js_button.background = RoundRect(widget, 6)
            style.prefs_js_button.hover_background = RoundRect(widget_hover, 6)
            style.prefs_js_button_text.drop_shadow = None
            style.prefs_js_button_text.size = small
            style.prefs_js_button.xminimum = 450

            rrframe(style.js_frame)
            del style.js_frame.yminimum
            style.js_frame.ypadding = .05
            style.js_frame.xpadding = rrslider_radius
            style.js_frame.xmargin = .05
            style.js_frame.ypos = .1
            style.js_frame.yanchor = 0

            style.js_function_label.xpos = 0.5
            style.js_function_label.xanchor = 0.5

            style.js_prompt_label.xpos = 0.5
            style.js_prompt_label.xanchor = 0.5

            # Yes/No

            rrframe(style.yesno_frame)
            del style.yesno_frame.yminimum
            style.yesno_frame.ypadding = .05
            style.yesno_frame.xpadding = rrslider_radius
            style.yesno_frame.xmargin = .05
            style.yesno_frame.ypos = .1
            style.yesno_frame.yanchor = 0

            style.yesno_label.color = label
            style.yesno_label.drop_shadow = None

            # File Picker

            rrframe(style.file_picker_frame)
            style.file_picker_frame.xmargin = 6
            style.file_picker_frame.ymargin = 6

            style.file_picker_frame_vbox.box_spacing = 4            
            style.file_picker_nav_button.xminimum = 0

            style.file_picker_navbox.box_spacing = spacing
            del style.file_picker_navbox.xpos

            style.file_picker_entry.background = RoundRect(widget)
            style.file_picker_entry.hover_background = RoundRect(widget_hover)
            style.file_picker_entry.xpadding = _roundrect_radius
            style.file_picker_entry.xmargin = 2

            style.file_picker_text.size = small
            style.file_picker_text.drop_shadow = None
            style.file_picker_text.color = widget_text
            style.file_picker_new.color = widget_selected
            
            config.file_quick_access_pages = 10

            # In-game.

            style.window.background = RoundRect(window)
            style.window.xpadding = 6
            style.window.ypadding = 6
            style.window.xmargin = 6
            style.window.ymargin = 6

            style.default.size = size
            style.default.drop_shadow = None

            rrframe(style.frame)
            style.frame.xpadding = 6
            style.frame.ypadding = 6
            style.frame.xmargin = 6
            style.frame.ymargin = 6

            if button_menu:
                _button_menu()

        theme.roundrect = theme_roundrect

        def theme_roundrect_red(**params):
            """
            This sets up a red/pink variant of the roundrect theme.
            """
            
            args = dict(widget=(150, 50, 50, 255),
                        widget_hover=(200, 50, 50, 255),
                        widget_text=(255, 225, 225, 255),
                        frame=(225, 115, 115, 192),
                        mm_root=Solid((255, 225, 225, 255)),
                        gm_root=Solid((255, 225, 225, 255)),
                        )

            args.update(params)
            theme.roundrect(**args)

        theme.roundrect_red = theme_roundrect_red

#         def magic(h, s, lmul=1.0, loff=0.0,  **params):

#             colors = dict(
#                 widget=(.25, 1.0),
#                 disabled=(.25, 0.0),
#                 widget_hover=(.33, 1.0),
#                 widget_text=(.90, 1.0),
#                 disabled_text=(.90, 0.0),
#                 frame=(.55, 1.0),
#                 )

#             import colorsys

#             def rgba(h, l, s, a):
#                 l = l * lmul + loff
                
#                 r, g, b = colorsys.hls_to_rgb(h, l, s)
#                 return (int(r * 255),
#                         int(g * 255),
#                         int(b * 255),
#                         a)

#             for name, (l, ss) in colors.iteritems():
#                 params.setdefault(name, rgba(h, l, ss * s, 255))

#             params.setdefault("mm_root", Solid(rgba(h, .93, ss * 1.0, 255)))
#             params.setdefault("gm_root", Solid(rgba(h, .93, ss * 1.0, 255)))

#             theme.roundrect(**params)


#         magic(.58, 1.0)
#         magic(0, .5, .5, .5)


    
