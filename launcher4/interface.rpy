init python:
    INDENT = 20
    HALF_INDENT = 10
    SCROLLBAR_SIZE = 16
    SEPARATOR = Frame("pattern.png", 0, 0, tile=True, ymaximum=5, yalign=1.0)
    SPACER = Null(height=12)
    HALF_SPACER = Null(height=6)
    
    # Colors.
    TEXT = "#545454"
    IDLE = "#42637b"
    LIGHT_IDLE = "#78a5c5"
    SCROLLBAR_IDLE = "#dfdfdf"
    HOVER = "#d86b45"
    WHITE = "#ffffff"
    
    # Default style.
    style.l_default = Style(style.default)
    style.l_default.font = "Roboto-Light.ttf"
    style.l_default.color = TEXT
    style.l_default.idle_color = IDLE
    style.l_default.hover_color = HOVER
    style.l_default.size = 18
    
    style.l_text = Style(style.l_default)

    style.l_button = Style(style.l_default)
    style.l_button_text = Style(style.l_default)

    # A small button, used at the bottom of the screen.
    style.l_link = Style(style.l_default)
    style.l_link_text = Style(style.l_default)
    style.l_link_text.size = 14

    # The bottom-right action button.
    style.l_right_button = Style(style.l_default)
    style.l_right_button.xalign = 1.0
    style.l_right_button.ypos = 600 - 128 + 3
    style.l_right_button.xmargin = 6
    style.l_right_button_text = Style(style.l_default)
    style.l_right_button_text.size = 30

    style.l_left_button = Style(style.l_right_button)
    style.l_left_button.xalign = 0.0
    style.l_left_button_text = Style(style.l_right_button_text)
    
    
    # The root frame. This contains everything but the bottom navigation, back
    # button, and tooltip button.
    style.l_root = Style(style.l_default)
    style.l_root.background = "background.png"
    style.l_root.xpadding = 10
    style.l_root.top_padding = 64
    style.l_root.bottom_padding = 128
    
    # An inner window.
    style.l_window = Style(style.l_default)
    style.l_window.background = Frame("window.png", 0, 0, tile=True)
    style.l_window.left_padding = 6
    style.l_window.right_margin = 0
    style.l_window.xfill = True
    style.l_window.yfill = True
    
    # Normal-sized labels.
    style.l_label = Style(style.l_default)
    style.l_label.xfill = True
    style.l_label.top_padding = 10
    style.l_label.bottom_padding = 8
    style.l_label.bottom_margin = 12
    style.l_label.background = SEPARATOR    
    style.l_label_text = Style(style.l_default)
    style.l_label_text.size = 24
    style.l_label_text.xpos = INDENT
    style.l_label_text.yoffset = 6
    
    # Alternate labels. This nests inside an l_label, and gives a button
    # or label that's nested inside another label.
    style.l_alternate = Style(style.l_default)
    style.l_alternate.xalign = 1.0
    style.l_alternate.yalign = 1.0
    style.l_alternate.right_margin = INDENT
    style.l_alternate_text = Style(style.l_default)
    style.l_alternate_text.yoffset = 4
    style.l_alternate_text.size = 14
    style.l_alternate_text.text_align = 1.0
    
    # Indents its contents by 16 pixels.
    style.l_indent = Style(style.l_default)
    style.l_indent.left_margin = INDENT
    
    # List button.
    style.l_list = Style(style.l_default)
    style.l_list.left_padding = HALF_INDENT
    style.l_list.xfill = True
    style.l_list.selected_background = LIGHT_IDLE
    style.l_list.selected_hover_background = HOVER
    style.l_list_text = Style(style.l_default)
    style.l_list_text.idle_color = IDLE
    style.l_list_text.hover_color = HOVER
    style.l_list_text.selected_idle_color = WHITE
    style.l_list_text.selected_hover_color = WHITE
    
    # Scrollbar.
    style.l_vscrollbar = Style(style.l_default)
    style.l_vscrollbar.thumb = Fixed(
        Solid(SCROLLBAR_IDLE, xmaximum=8, xalign=0.5),
        Image("vscrollbar_center.png", xalign=0.5, yalign=0.5),
        xmaximum = SCROLLBAR_SIZE)
    style.l_vscrollbar.hover_thumb = Fixed(
        Solid(HOVER, xmaximum=8, xalign=0.5),
        Image("vscrollbar_center.png", xalign=0.5, yalign=0.5),
        xmaximum = SCROLLBAR_SIZE)
    style.l_vscrollbar.xmaximum = SCROLLBAR_SIZE
    style.l_vscrollbar.bar_vertical = True
    style.l_vscrollbar.bar_invert = True
    
    
    # Information window.
    
    
    style.l_info_vbox = Style(style.vbox)
    style.l_info_vbox.yalign = 0.5
    style.l_info_vbox.xalign = 0.5
    style.l_info_vbox.xfill = True
    
    style.l_info_frame = Style(style.l_default)
    style.l_info_frame.ypadding = 21
    style.l_info_frame.xfill = True
    style.l_info_frame.background = Fixed(
        "#f9f9f9",
        Frame("pattern.png", 0, 0, tile=True, ymaximum=5, yalign=0.0, yoffset=8),
        Frame("pattern.png", 0, 0, tile=True, ymaximum=5, yalign=1.0, yoffset=-8),
        )    
    style.l_info_frame.yminimum = 180
    style.l_info_frame.ypos = 100
    
    style.l_info_label = Style(style.l_default)
    style.l_info_label.xalign = 0.5
    style.l_info_label.ypos = 100
    style.l_info_label.yanchor = 1.0
    style.l_info_label.yoffset = 12
    style.l_info_label_text = Style(style.l_default)
    style.l_info_label_text.size = 36
    
    style.l_info_text = Style(style.l_default)
    style.l_info_text.xalign = 0.5
        
    style.l_info_button = Style(style.l_button)
    style.l_info_button.xalign = 0.5
    style.l_info_button_text = Style(style.l_button_text)
    

    
################################################################################
# Interface actions.
init python in interface:
    from store import OpenURL, config

    import os.path
    import contextlib
    
    RENPY_URL = "http://www.renpy.org"
    RENPY_GAMES_URL = "http://games.renpy.org"    
    DOC_PATH = os.path.join(config.renpy_base, "doc/index.html")
    DOC_URL = "http://www.renpy.org/doc/html/"
    
    if os.path.exists(DOC_PATH):
        DOC_LOCAL_URL = "file:///" + DOC_PATH
    else:
        DOC_LOCAL_URL = None
    
    def OpenDocumentation():
        """
        An action that opens the documentation.
        """
                    
        if DOC_LOCAL_URL is not None:
            return OpenURL(DOC_LOCAL_URL)
        else:
            return OpenURL(DOC_URL)
    
    
    # Should we display the bottom links?
    links = True
    
    @contextlib.contextmanager
    def nolinks():
        global links
        links = False
        
        try:
            yield
        finally:
            links = True
    
# This displays the bottom of the screen. If the tooltip is not None, this displays the
# tooltip. Otherwise, it displays a list of links (to various websites, and to the 
# preferences and update screen), or is just blank.
screen bottom_info:
    
    zorder 100
    
    if interface.links:
        
        frame:
            style_group "l"
            style "l_default"
            
            xmargin 6
            xfill True
            ypos 536
            yanchor 0.5
            
            hbox:
                xfill True
                
                hbox:
                    spacing INDENT
                    textbutton _("Documentation") style "l_link" action interface.OpenDocumentation()
                    textbutton _("Ren'Py Website") style "l_link" action OpenURL(interface.RENPY_URL)
                    textbutton _("Ren'Py Games List") style "l_link" action OpenURL(interface.RENPY_GAMES_URL)
                    textbutton _("About") style "l_link"
                
                hbox:
                    spacing INDENT
                    xalign 1.0

                    textbutton _("update") style "l_link"
                    textbutton _("preferences") style "l_link"
                    textbutton _("quit") style "l_link" action Quit(confirm=False)

                    
screen info:
    
    frame:
        style "l_root"

        frame:
            style_group "l_info"
        
            has vbox
            
            text message
            
            add SPACER 
            add SPACER 
            
            textbutton _("Continue") action Return(True)
            
        label _("INFORMATION") style "l_info_label"

screen processing:
    
    frame:
        style "l_root"

        frame:
            style_group "l_info"
        
            has vbox
            
            text message
            
        label _("PROCESSING") style "l_info_label"
        
    use bottom_info

    
screen error:
    frame:
        style "l_root"

        frame:
            style_group "l_info"
        
            has vbox
            
            text message
            
            if submessage:
                add SPACER
                add SPACER
                text submessage
            
        label _("ERROR") style "l_info_label" text_color "d15353"

    textbutton _("Back") action Return(True) style "l_left_button"
  
init python in interface:

    import traceback
    
    def info(message, **kwargs):
        """
        Displays an informational message to the user. The user will be asked to click to 
        confirm that he has read the message.
        
        `message`
            The message to display. 
        
        Keyword arguments are passed into the screen so that they can be substituted into
        the message.
        """
        
        ui.saybehavior()
        renpy.call_screen("info", message=message, **kwargs)
        
    def processing(message, **kwargs):
        """
        Indicates to the user that processing is taking place. This should be used when
        there is an indefinite amount of work to be done.
        
        `message`
            The message to display. 
        
        Keyword arguments are passed into the screen so that they can be substituted into
        the message.
        """
            
        # We can show the links if we want, since the user won't be able to 
        # click on them (the screen is not shown for long enough.)
        
        ui.pausebehavior(0)
        renpy.call_screen("processing", message=message, **kwargs)
    
    def error(message, submessage=None, label="front_page", **kwargs):
        """
        Indicates to the user that an error has occured.
        
        `message`
            The message to display. 

        `submessage`
            Optional secondary message information. For example, this may be 
            used to display an exception string.
            
        `label`
            The label to redirect to when the user finishes displaying the error.
        
        Keyword arguments are passed into the screen so that they can be substituted into
        the message.
        """
        
        ui.saybehavior()
        renpy.call_screen("error", message=message, submessage=submessage, **kwargs)
        renpy.jump(label)

    @contextlib.contextmanager
    def error_handling(what, label="front_page"):
        """
        This is a context manager that catches exceptions and displays them using 
        interface.error.
        
        `what`
            What we're doing when the error occurs. This is usually written using 
            the present participle.
            
        `label`
            The label to jump to when error handling finishes.
           
        As an example of usage::
        
            with interface.error_handling("opening the log file"):
                f = open("log.txt", "w")            
        """
            
                
        try:
            yield
        except Exception, e:
            error(_("While [what!q], an error occured:"), 
                _("[exception!q]"), 
                what=what, 
                exception=traceback.format_exception_only(type(e), e)[-1][:-1])
                
            