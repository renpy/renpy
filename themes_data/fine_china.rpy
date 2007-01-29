## 'Fine China' color scheme
##

init -1:
    python hide:

        ## We then want to call a theme function. themes.roundrect is
        ## a theme that features the use of rounded rectangles. It's
        ## the only theme we currently support.
        ##
        ## The theme function takes a number of parameters that can
        ## customize the color scheme.
        theme.roundrect(

            ## The color of an idle widget face.
            widget = "#6A7183",

            ## The color of a focused widget face.
            widget_hover = "#1A2B47",

            ## The color of the text in a widget.
            widget_text = "#C9C9CB",

            ## The color of the text in a selected widget. (For
            ## example, the current value of a preference.)
            widget_selected = "#E3E3E4",

            ## The color of a disabled widget face. 
            disabled = "#ADB9CC",

            ## The color of disabled widget text.
            disabled_text = "#DFBA14",

            ## The color of informational labels.
            label = "#39435E",

            ## The color of a frame containing widgets.
            frame = "#ADB9CC",

            ## If this is True, in-game menus are placed in the center
            ## the screen. If False, they are placed inside a window
            ## at the bottom of the screen.
            button_menu = True,

            ## The background of the main menu. This can be a color
            ## beginning with '#', or an image filename. The latter
            ## should take up the full height and width of the screen.
            mm_root = "#F7F7FA",

            ## The background of the game menu. This can be a color
            ## beginning with '#', or an image filename. The latter
            ## should take up the full height and width of the screen.
            gm_root = "#F7F7FA",

            ## And we're done with the theme. The theme will customize
            ## various styles, so if we want to change them, we should
            ## do so below.            
            )
