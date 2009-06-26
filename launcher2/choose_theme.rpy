init -1 python:
    style_backup = renpy.style.backup()

init python:

    current_theme = None

    def show_roundrect_theme(name):
        """
         Changes from the current theme to the roundrect theme named
         `name`.
         """

        if current_theme == name:
            return

        store.current_theme = name
        
        td = theme_data[name].copy()
        del td["theme"]

        renpy.style.restore(style_backup)
        theme.roundrect(rounded_window=False, **td)
        customize_styles()
        renpy.style.rebuild()
        
        renpy.jump("repeat_choose_roundrect_theme")
        
    curried_show_roundrect_theme = renpy.curry(show_roundrect_theme)

    # Used to have buttons not do anything.
    def does_nothing(*args):
        return
    

label choose_theme:
label choose_roundrect_theme:
    
    python:

        current_theme = None
        theme_adjustment = ui.adjustment()

label repeat_choose_roundrect_theme:

    python hide:

        tip = _("Please choose a theme for your project.")
        
        themes = theme_data.keys()
        themes.sort()

        screen()
        ui.vbox()
        title("Choose Theme")

        ui.grid(2, 1, padding=10, xfill=True)

        # The scroll area, that lets the user pick a theme.
        scrolled('top', theme_adjustment)
        ui.vbox()
        
        for i in themes:
             button(i, ui.returns(True), "", hovered=curried_show_roundrect_theme(i), unhovered=does_nothing)

        ui.close() # vbox
        ui.close() # scrolled


        # The sample area, that shows what the theme looks like.
        ui.window(style='default', background="#444", xpadding=1, ypadding=1)
        ui.window(style='gm_root', xpadding=5, ypadding=5)
        ui.vbox(5)

        # Display Preference.
        ui.window(style=style.prefs_pref_frame)
        ui.vbox(style=style.prefs_pref_box)
        
        ui.hbox(style=style.prefs_pref_choicebox)
        
        layout.label(_("Display"), "prefs")
        layout.button(_("Window"), "prefs", clicked=does_nothing, selected=True)
        layout.button(_("Fullscreen"), "prefs", clicked=does_nothing, selected=False)

        ui.close()
        ui.close()

        # Volume Preference
        ui.window(style=style.prefs_pref_frame)
        ui.vbox(style=style.prefs_pref_box)

        layout.label("Music Volume", "prefs")
        ui.vbox(style=style.prefs_volume_box)

        ui.bar(128,
               92,
               changed=does_nothing,
               style=style.prefs_volume_slider)

        layout.button(u"Test", "soundtest", clicked=does_nothing)

        ui.close()
        ui.close()

        
        # Frame, etc. go here.
        
        ui.close() # vbox

        ui.close() # grid

        ui.close() # vbox

        set_tooltip(tip)
        interact()
        

