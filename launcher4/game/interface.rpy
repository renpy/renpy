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
            
            left_margin (10 + INDENT)
            right_margin (10 + INDENT)
            xfill True
            ypos 536
            yanchor 0.0
            
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
                    textbutton _("preferences") style "l_link" action Jump("preferences")
                    textbutton _("quit") style "l_link" action Quit(confirm=False)

                    
screen info:
    
    frame:
        style "l_root"

        frame:
            style_group "l_info"
        
            has vbox
            
            text message

            if pause:

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
            
        label _("ERROR") style "l_info_label" text_color "#d15353"

    if label:
        textbutton _("Back") action Jump("label") style "l_left_button"
    else:
        textbutton _("Back") action Return(True) style "l_left_button"
  

screen launcher_input:

    frame:
        style "l_root"

        frame:
            style_group "l_info"
        
            has vbox
            
            text message

            add SPACER

            input style "l_default" size 24 xalign 0.5 default default

            if filename:
                add SPACER
                text _("Due to package format limitations, non-ASCII file and directory names are not allowed.")
            
        label _("[title]") style "l_info_label" text_color "#d19753"

    
    if cancel:
        textbutton _("Cancel") action cancel style "l_left_button"
    
    
  
  
init python in interface:

    import traceback
    
    def info(message, pause=True, **kwargs):
        """
        Displays an informational message to the user. The user will be asked to click to 
        confirm that he has read the message.
        
        `message`
            The message to display. 
        
        `pause`
            True if we should pause before 
        
        Keyword arguments are passed into the screen so that they can be substituted into
        the message.
        """
        
        if pause:
            ui.saybehavior()
        
        renpy.call_screen("info", message=message, pause=pause, **kwargs)
        
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
            The label to redirect to when the user finishes displaying the error. None
            to just return.
        
        Keyword arguments are passed into the screen so that they can be substituted into
        the message.
        """
        
        ui.saybehavior()
        renpy.call_screen("error", message=message, submessage=submessage, label=label, **kwargs)

        if label:
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
                
    def input(title, message, filename=False, sanitize=True, cancel=None, default=""):
        """
        Requests typewritten input from the user.
        """
        
        rv = default
        
        while True:
            
            rv = renpy.call_screen("launcher_input", title=title, message=message, filename=filename, cancel=cancel, default=rv)
            
            if sanitize:
                if ("[" in rv) or ("{" in rv):
                    error(_("Text input may not contain the {{ or [[ characters."), label=None)
                    continue
                    
            if filename:
                if ("\\" in rv) or ("/" in rv):
                    error(_("File and directory names may not contain / or \\."), label=None)
                    continue
                    
                try:
                    rv.encode("ascii")
                except:
                    error(_("File and directory names must consist of ASCII characters."), label=None)
                    continue

            return rv
            