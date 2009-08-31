# This file contains the various components of the launcher interface.

init -11 python:
    style.launcher_base = Style(style.default)

    style.launcher_text = Style(style.launcher_base)
    style.launcher_text.size = 15
    style.launcher_text.color = "#333"
    style.launcher_text.justify = True
    
    style.launcher_title = Style(style.launcher_base)
    style.launcher_title.size = 26
    style.launcher_title.color = "#333"

    style.launcher_button_text = Style(style.launcher_base)
    style.launcher_button_text.size = 20
    style.launcher_button_text.color = "#03c"
    style.launcher_button_text.hover_color = "#088"
    style.launcher_button_text.insensitive_color = "#aaa"
    style.launcher_button_text.minwidth = 250

    style.launcher_small_button_text = Style(style.launcher_button_text)
    style.launcher_small_button_text.size = 15

    style.launcher_tooltip = Style(style.default)
    style.launcher_tooltip.color = "#fff"
    style.launcher_tooltip.size = 14


init 11 python hide:

    props = { }
    for i in style.default.properties:
        props.update(i)

    if props["font"] == "DejaVuSans.ttf":
        style.launcher_base.setdefault(font="DejaVuSerif.ttf")

init 11 python:

    import time

    # Settings.
    config.developer = True

    # Make backup of styles.
    style_backup = renpy.style.backup()
    
    # Style customizations. These need to be in a function so that we can
    # change them when we're choosing a theme.
    def customize_styles():
        style.window.yminimum = 60
        style.window.left_padding = 60

        style.hyperlink_text.color = "#03c"
        style.hyperlink_text.hover_color = "#00c"
        style.hyperlink_text.size = 15
        style.hyperlink_text.underline = False
                
    customize_styles()
        
    tooltip = _(u"Welcome!")

    def show_tooltip(st, at):
        return Text(tooltip, color="#fff", size=14), None

    def set_tooltip(s):
        global tooltip
        
        if tooltip != s:
            tooltip = s
            renpy.restart_interaction()

    tooltips = renpy.curry(set_tooltip)

    def unset_tooltip(s):
        global tooltip

        if s and tooltip == s:
            tooltip = ""
            renpy.restart_interaction()

    untooltips = renpy.curry(unset_tooltip)
            
            
    def screen():
        """
         Display a screen. This should be called before any code that
         draws to the screen.
         """

        ui.add(Solid("#fff"))
        
        ui.window(yalign=1.0)
        ui.add(DynamicDisplayable(show_tooltip))

        ui.image("eileen_small.png", xalign=0.0, yalign=1.0)
        
        ui.window(xmargin=20, top_margin=4, bottom_margin=85, style='default')
        
    def interact():
        """
         Closes the screen, and causes an interaction to occur.
         """
        
        return ui.interact(suppress_overlay=True, suppress_underlay=True)

    def title(s):
        """
         Display a title on the screen.
         """

        ui.window(style="default", bottom_margin=4, top_margin=12)
        ui.text(s, style="launcher_title")
                
    def text(s):
        """
         Display text on the screen.
         """
        
        ui.text(s, style="launcher_text")
        
    def button(s, clicked=None, subtitle="", hovered=None, unhovered=None):
        """
         Displays a button with caption `s`.
         """

        if subtitle is not None:
            if hovered is None:
                hovered = tooltips(subtitle)
                
            if unhovered is None:
                unhovered = untooltips(subtitle)
        
        ui.button(style="default", clicked=clicked,
                  hovered=hovered, unhovered=unhovered,
                  top_padding=3, bottom_padding=3)

        ui.text(s, style="launcher_button_text")

    def small_button(s, clicked=None, subtitle="", hovered=None, unhovered=None):
        """
         Displays a button with caption `s`.
         """

        if hovered is None:
            hovered = tooltips(subtitle)

        if unhovered is None:
            unhovered = untooltips(subtitle)
        
        ui.button(style="default", clicked=clicked,
                  hovered=hovered, unhovered=unhovered,
                  top_padding=0, bottom_padding=0)

        ui.text(s, style="launcher_small_button_text")

    def toggle_button(s, checked, clicked=None, subtitle=""):
        """
         Displays a button with caption `s`.
         """
        
        hovered = tooltips(subtitle)
        unhovered = untooltips(subtitle)

        if checked:
            s = u"{font=DejaVuSans.ttf}\u25a3{/font} " + s
        else:
            s = u"{font=DejaVuSans.ttf}\u25a1{/font} " + s
        
        ui.button(style="default", clicked=clicked,
                  hovered=hovered, unhovered=unhovered,
                  top_padding=0, bottom_padding=0)

        ui.text(s, style="launcher_small_button_text")
        
    def scrolled(cancel, yadj=None):

        if yadj is None:
            yadj = ui.adjustment()

        ui.side(['r', 'b', 'c'])

        ui.bar(adjustment=yadj, style='lscrollbar')
        
        if cancel:
            ui.vbox()
            ui.null(height=12)
            button(_(u"Cancel"), clicked=ui.jumps(cancel))
            ui.close()
        else:
            ui.null()               
                    
        ui.viewport(yadjustment=yadj, mousewheel=True)

        # Left up to the user to close.

    def error(message, target="top"):
        """
         Displays an error to the user, and lets him click to return to
         `target`.
         """

        set_tooltip("")
        
        screen()
        
        ui.vbox()
        title(_(u"Error"))
        text(message)

        ui.null(height=20)
        
        if target is None:
            clicked = ui.returns(True)
        else:
            clicked = ui.jumps(target)
        
        button(_(u"Return"), clicked, None)
        ui.close()

        interact()

    def info(t, message):
        """
         Displays an informational message to the user, and immediately
         returns.
         """

        ui.pausebehavior(0)

        screen()
        
        ui.vbox()
        title(t)
        text(message)
        ui.close()

        interact()
        
    def yesno(t, message):
        """
         Asks a yes/no question of the user.
         """

        set_tooltip("")
        
        screen()

        ui.vbox()
        title(t)
        text(message)
        button(_(u"Yes"), ui.returns(True), "")
        button(_(u"No"), ui.returns(False), "")
        ui.close()

        return interact()
         
    def text_variable(t, value, returns, tooltip=""):

        text(t)
        small_button(value, ui.returns(returns), tooltip)
        ui.null(height=5)

    def input(t, prompt, value, cancel=None):

        set_tooltip(_(u"Press enter when done."))

        while True:
        
            screen()
            ui.vbox()

            title(t)
            text(prompt)
            ui.null(height=10)
            ui.input(value, size=20, color="#00c")

            if cancel is not None:
                ui.null(height=20)
                button(_(u"Cancel"), ui.jumps(cancel), "")

            ui.close()

            value = interact()
            value = value.strip()
            
            if not value:
                error(
                    _(u"The string cannot be empty. Please enter some text."),
                    None)

                continue
                
            try:
                value = value.encode("ascii")
            except:
                error(
                    _(u"Non-ASCII filenames are not allowed. This is because Zip files cannot reliably represent non-ASCII filenames."),
                    None)

                continue
                
            break
            
        return value

    # The time progress was last updated. We only update the progress
    # every 10th of a second, so that we don't waste time doing
    # such updates.
    progress_time = 0


    def progress(what, limit, amount):
        """
         Show progress to the user.
         """
        
        global progress_time
        
        t = time.time()
        if t < progress_time + .1:
            return

        progress_time = t

        set_tooltip(_(u"Processed %d of %d files.") % (amount + 1, limit))
        
        ui.pausebehavior(0)

        screen()

        ui.vbox(xfill=True)

        title(what)
        ui.null(height=20)
        ui.bar(limit, amount, xmaximum=300, xalign=0.5, style='lbar')

        ui.close()
        interact()
        
        
        
        
    
