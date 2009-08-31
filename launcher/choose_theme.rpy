init python:

    import codecs
    import re
    import sys
    
    ##########################################################################
    # Code to update options.rpy
    
    def list_logical_lines(filename):
        """
         This reads in filename, and turns it into a list of logical
         lines. 
        """

        f = codecs.open(filename, "rb", "utf-8")
        data = f.read()
        f.close()

        # The result.
        rv = []

        # The current position we're looking at in the buffer.
        pos = 0

        # Looping over the lines in the file.
        while pos < len(data):

            # The line that we're building up.
            line = ""

           # The number of open parenthesis there are right now.
            parendepth = 0

            # Looping over the characters in a single logical line.
            while pos < len(data):

                c = data[pos]

                if c == '\n' and not parendepth:
                    rv.append(line)

                    pos += 1
                    # This helps out error checking.
                    line = ""
                    break

                # Backslash/newline.
                if c == "\\" and data[pos+1] == "\n":
                    pos += 2
                    line += "\\\n"
                    continue

                # Parenthesis.
                if c in ('(', '[', '{'):
                    parendepth += 1

                if c in ('}', ']', ')') and parendepth:
                    parendepth -= 1

                # Comments.
                if c == '#':
                    while data[pos] != '\n':
                        line += data[pos]
                        pos += 1

                    continue

                # Strings.
                if c in ('"', "'", "`"):
                    delim = c
                    line += c
                    pos += 1

                    escape = False

                    while pos < len(data):

                        c = data[pos]

                        if escape:
                            escape = False
                            pos += 1
                            line += c
                            continue

                        if c == delim:
                            pos += 1
                            line += c
                            break

                        if c == '\\':
                            escape = True

                        line += c
                        pos += 1

                        continue

                    continue
                    
                line += c
                pos += 1

        if line:
            rv.append(line)

        return rv


    def switch_theme(name):
        """
         Switches the theme of the current project to the named theme.
         """

        theme_functions = set(i[1] for i in themes)

        td = theme_data[name].copy()
        td["name"] = name

        # Did we change the file at all?
        changed = False

        filename = os.path.join(project.gamedir, "options.rpy")

        out = codecs.open(filename + ".new", "wb", "utf-8")
        
        for l in list_logical_lines(filename):

            m = re.match(r'    theme.(\w+)\(', l)
            if m:
                if m.group(1) in theme_functions:
                    l = theme_templates[td["theme"]] % td
                    changed = True
                    
            out.write(l + "\n")

        out.close()

        if changed:
            try:
                os.unlink(filename + ".bak")
            except:
                pass

            os.rename(filename, filename + ".bak")
            os.rename(filename + ".new", filename)
            
        else:
            os.unlink(filename + ".new")

            error(_(u"Could not modify options.rpy. Perhaps it was changed too much."))
            
        set_tooltip(_(u"Theme changed to %s.") % name)
        renpy.jump("top")

    curried_switch_theme = renpy.curry(switch_theme)
        
    

    ##########################################################################
    # Code that handles display.
    
    current_theme = None

    def show_theme(name, target):
        """
         Changes from the current theme to the roundrect theme named
         `name`.
         """

        if current_theme == name:
            return

        store.current_theme = name
        
        td = theme_data[name].copy()
        kind = td["theme"]
        del td["theme"]

        if kind == "roundrect":
            td["rounded_window"] = False
        
        renpy.style.restore(style_backup)
        getattr(theme, kind)(**td)
        customize_styles()
        renpy.style.rebuild()
        
        renpy.jump(target)
        
    curried_show_theme = renpy.curry(show_theme)

    def theme_demo():
        # The sample area, that shows what the theme looks like.
        ui.window(style='default', background="#444", xpadding=1, ypadding=1)
        ui.window(style='gm_root', xpadding=5, ypadding=5)
        ui.vbox(5)

        # Display Preference.
        ui.window(style=style.prefs_pref_frame)
        ui.vbox(style=style.prefs_pref_box)
        
        ui.hbox(style=style.prefs_pref_choicebox)
        
        layout.label(_(u"Display"), "prefs")
        layout.button(_(u"Window"), "prefs", clicked=does_nothing, selected=True)
        layout.button(_(u"Fullscreen"), "prefs", clicked=does_nothing, selected=False)
        layout.button(_(u"Planetarium"), "prefs", clicked=None, selected=False)

        ui.close()
        ui.close()

        # Volume Preference
        ui.window(style=style.prefs_pref_frame)
        ui.vbox(style=style.prefs_pref_box)

        layout.label(_(u"Music Volume"), "prefs")
        ui.vbox(style=style.prefs_volume_box)

        ui.bar(128,
               92,
               changed=does_nothing,
               style=style.prefs_volume_slider)

        layout.button(_(u"Test"), "soundtest", clicked=does_nothing)

        ui.close()
        ui.close()
        
        ui.close() # vbox
        
    
    # Used to have buttons not do anything.
    def does_nothing(*args):
        return


label choose_theme:

    python:
        if not os.path.exists(os.path.join(project.gamedir, "options.rpy")):
            error(_(u"The options.rpy file does not exist in the game directory, so this launcher cannot change the theme."))

        current_theme = None
        theme_adjustment = ui.adjustment()

label repeat_choose_theme:

    python hide:
        
        tip = _(u"Themes control the basic look of interface elements. You'll be able to pick a color scheme next.")

        screen()
        ui.vbox()
        title(_(u"Choose Theme"))

        ui.grid(2, 1, padding=10, xfill=True)

        # The scroll area, that lets the user pick a theme.
        scrolled('top', theme_adjustment)
        ui.vbox()
        
        for name, function, exemplar in themes:
             button(name,
                    ui.returns(function),
                    "",
                    hovered=curried_show_theme(exemplar, "repeat_choose_theme"),
                    unhovered=does_nothing)

        ui.close() # vbox
        ui.close() # scrolled

        theme_demo()
        
        ui.close() # grid
        ui.close() # vbox

        set_tooltip(tip)
        store.theme_function = interact()    

        
label choose_color_scheme:
    
    python:

        current_theme = None
        theme_adjustment = ui.adjustment()
        
label repeat_choose_color_scheme:

    python hide:

        tip = _(u"Please choose a color scheme for your project.")

        themes = [ k for k,v in theme_data.iteritems() if v["theme"] == theme_function ]
        themes.sort()

        screen()
        ui.vbox()
        title(_(u"Choose Color Scheme"))

        ui.grid(2, 1, padding=10, xfill=True)

        # The scroll area, that lets the user pick a theme.
        scrolled('choose_theme', theme_adjustment)
        ui.vbox()
        
        for i in themes:
             button(i,
                    curried_switch_theme(i),
                    "",
                    hovered=curried_show_theme(i, "repeat_choose_color_scheme"),
                    unhovered=does_nothing)

        ui.close() # vbox
        ui.close() # scrolled

        theme_demo()
        
        ui.close() # grid
        ui.close() # vbox

        set_tooltip(tip)
        interact()
        

