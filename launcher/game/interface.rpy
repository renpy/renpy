# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

################################################################################
# Interface actions.
init python in interface:
    from store import OpenURL, config, Return
    import store

    import os.path
    import contextlib
    
    RENPY_URL = "http://www.renpy.org"
    RENPY_GAMES_URL = "http://games.renpy.org"    
    DOC_PATH = os.path.join(config.renpy_base, "doc/index.html")
    DOC_URL = "http://www.renpy.org/doc/html/"

    LICENSE_PATH = os.path.join(config.renpy_base, "doc/license.html")
    LICENSE_URL = "http://www.renpy.org/doc/html/license.html"
    
    if os.path.exists(DOC_PATH):
        DOC_LOCAL_URL = "file:///" + DOC_PATH
    else:
        DOC_LOCAL_URL = None

    if os.path.exists(LICENSE_PATH):
        LICENSE_LOCAL_URL = "file:///" + LICENSE_PATH
    else:
        LICENSE_LOCAL_URL = None
    
    def OpenDocumentation():
        """
        An action that opens the documentation.
        """
                    
        if DOC_LOCAL_URL is not None:
            return OpenURL(DOC_LOCAL_URL)
        else:
            return OpenURL(DOC_URL)

    def OpenLicense():
        """
        An action that opens the license.
        """
                    
        if LICENSE_LOCAL_URL is not None:
            return OpenURL(LICENSE_LOCAL_URL)
        else:
            return OpenURL(LICENSE_URL)
    
    
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
                    textbutton _("About") style "l_link" action Jump("about")
                
                hbox:
                    spacing INDENT
                    xalign 1.0

                    if ability.can_update:
                        textbutton _("update") action Jump("update") style "l_link"
                    
                    textbutton _("preferences") style "l_link" action Jump("preferences")
                    textbutton _("quit") style "l_link" action Quit(confirm=False)

                    
screen common:
    
    default complete = None
    default total = None
    default yes = None
    default no = None
    
    frame:
        style "l_root"

        frame:
            style_group "l_info"
        
            has vbox
            
            text message:
                text_align 0.5
                xalign 0.5
                layout "subtitle"
        
            if complete is not None:
                add SPACER
                
                frame:
                    style "l_progress_frame"
                    
                    bar:
                        range total
                        value complete
                        style "l_progress_bar"
        
            if submessage:
                add SPACER

                text submessage:
                    text_align 0.5
                    xalign 0.5
                    layout "subtitle"

            if yes:
                add SPACER
                
                hbox:
                    xalign 0.5
                    textbutton _("Yes") style "l_button" action yes
                    null width 160
                    textbutton _("No") style "l_button" action no
                

        label title text_color title_color style "l_info_label"

    if back:
        textbutton _("Back") action Return(False) style "l_left_button"
        
    if continue_:
        textbutton _("Continue") action Return(True) style "l_right_button"


screen launcher_input:

    frame:
        style "l_root"

        frame:
            style_group "l_info"
        
            has vbox
            
            text message

            add SPACER

            input style "l_default" size 24 xalign 0.5 default default color INPUT_COLOR 

            if filename:
                add SPACER
                text _("Due to package format limitations, non-ASCII file and directory names are not allowed.")
            
        label _("[title]") style "l_info_label" text_color QUESTION_COLOR

    
    if cancel:
        textbutton _("Cancel") action cancel style "l_left_button"
  
init python in interface:

    import traceback
    
    def common(title, title_color, message, submessage=None, back=False, continue_=False, pause0=False, **kwargs):
        """
        Displays the info, interaction, and processing screens.

        `title`
            The title of the screen.
        
        `message`
            The main message that is displayed when the screen is.
        
        `submessage`
            If not None, a message that is displayed below the main message.
        
        `back`
            If True, a back button will be present. If it's clicked, False will
            be returned.
        
        `continue_`
            If True, a continue button will be present. If it's clicked, True 
            will be returned.
        
        `pause0`
            If True, a zero-length pause will be inserted before calling the 
            screen. This will display it to the user and then immediately 
            return.
        
        
        Other keyword arguments are passed to the screen itself.
        """

        if pause0:
            ui.pausebehavior(0)
            
        return renpy.call_screen("common", title=title, title_color=title_color, message=message, submessage=submessage, back=back, continue_=continue_, **kwargs) 

    
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

        common(_("ERROR"), store.ERROR_COLOR, message=message, submessage=submessage, back=True, **kwargs)
        

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
            import traceback
            traceback.print_exc()

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
                if filename and (filename != "withslash") and (("\\" in rv) or ("/" in rv)):
                    error(_("File and directory names may not contain / or \\."), label=None)
                    continue
                    
                try:
                    rv.encode("ascii")
                except:
                    error(_("File and directory names must consist of ASCII characters."), label=None)
                    continue

            return rv

    def info(message, submessage=None, pause=True, **kwargs):
        """
        Displays an informational message to the user. The user will be asked to click to 
        confirm that he has read the message.
        
        `message`
            The message to display. 
        
        `pause`
            True if we should pause while showing the info.
        
        Keyword arguments are passed into the screen so that they can be substituted into
        the message.
        """
        
        if pause:
            common(_("INFORMATION"), store.INFO_COLOR, message, submessage, continue_=True, **kwargs)
        else:
            common(_("INFORMATION"), store.INFO_COLOR, message, submessage, pause=0, **kwargs)
    
    
    def interaction(title, message, submessage=None, **kwargs):
        """
        Put up on the screen while an interaction with an external program occurs.
        This shows the message, then immediately returns.

        `title`
            The title of the interaction.
        
        `message`
            The message itself.
        
        `submessage`
            An optional sub message.
        """

        common(title, store.INTERACTION_COLOR, message, submessage, pause0=True, **kwargs)
        
    def processing(message, submessage=None, complete=None, total=None, **kwargs):
        """
        Indicates to the user that processing is taking place. This should be used when
        there is an indefinite amount of work to be done.
        
        `message`
            The message to display. 
        
        `submessage`
            An additional message to display.

        `complete`
            The fraction complete the step is.
        
        `total`
            The total amount of work to do in this step.
        
        Keyword arguments are passed into the screen so that they can be substituted into
        the message.
        """

        common(_("PROCESSING"), store.INTERACTION_COLOR, message, submessage, pause0=True, complete=complete, total=total, **kwargs) 

        
    def yesno(message, yes=Return(True), no=Return(False), **kwargs):
        """
        Asks the user a yes or no question.
        
        `message`
            The question to ask.
        
        `yes`
            The action to perform if the user answers yes.
        
        `no`
            The action to perform if the user answer no.
        """

        return common(_("QUESTION"), store.QUESTION_COLOR, message, yes=yes, no=no, **kwargs)
        
