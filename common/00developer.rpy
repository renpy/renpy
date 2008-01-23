# Entry point for the developer console.
label _developer:

    if not config.developer:
        return

    call _enter_menu

label _developer_screen:

    python hide:

        ui.window(style=style.gm_root)
        ui.null()
        
        ui.frame(xpos=10, ypos=10, style=style.menu_frame)
        ui.vbox(box_first_spacing=10)
        layout.label(u"Developer Menu", None)

        sg = ui.size_group()

        layout.button("Return", None, clicked=ui.returns(True), size_group=sg)
        layout.button("Reload Game (Shift+R)", None, clicked=ui.callsinnewcontext("_save_reload_game"), size_group=sg)
        layout.button("Variable Viewer", None, clicked=ui.jumps("_debugger_screen"), size_group=sg)
        layout.button("Theme Test", None, clicked=ui.jumps("_theme_test"), size_group=sg)
        layout.button("Style Hierarchy", None, clicked=ui.jumps("_style_hierarchy"), size_group=sg)
        
        ui.close()
        ui.interact()
        
    return 
        
label _debugger_screen:

    python hide:

        ui.window(style=style.gm_root)
        ui.null()

        ui.frame(ymargin=10, xmargin=10, style=style.menu_frame)
        ui.side(['t', 'c', 'r', 'b'])

        layout.label("Variable Viewer", None)

        entries = [ ]
        
        ebc = renpy.game.log.ever_been_changed
        ebc = list(ebc)
        ebc.sort()

        ebc.remove("nvl_list")

        import repr
        aRepr = repr.Repr()
        aRepr.maxstring = 40

        for var in ebc:
            if not hasattr(store, var):
                continue

            if var.startswith("__00"):
                continue

            if var.startswith("_") and not var.startswith("__"):
                continue

            val = aRepr.repr(getattr(store, var))
            entries.append((0, (var + " = " + val).replace("{", "{{")))

        if entries:
            vp = ui.viewport(mousewheel=True)
            layout.list(entries)
            ui.bar(adjustment=vp.yadjustment, style='vscrollbar')
        else:
            ui.text("No variables have changed since the game started.", style='text')
            ui.null()

        layout.button(u"Return to the Debug Menu", None, clicked=ui.returns(True))

        ui.close()
        
        ui.interact()
        
    jump _developer_screen

label _theme_test:

    python hide:

        # Never gets pickled
        def role(b):
            if b:
                return "selected_"
            else:
                return ""
        
        toggle_var = True
        adj = ui.adjustment(100, 25)
        
        while True:

            ui.window(style=style.gm_root)
            ui.null()

            # Buttons
            ui.hbox(box_spacing=10, xpos=10, ypos=10)

            ui.vbox(box_spacing=10)

            sg = ui.size_group()

            ui.frame(style='menu_frame')
            ui.vbox()
            layout.label("Button", None)
            ui.textbutton("Button", size_group=sg, clicked=ui.returns("gndn"))
            ui.textbutton("Button (Selected)", size_group=sg, clicked=ui.returns("gndn"), role=role(True))
            ui.textbutton("Small", clicked=ui.returns("gndn"), style='small_button')
            ui.close()

            ui.frame(style='menu_frame')
            ui.vbox()
            layout.label("Radio Button", None)
            ui.textbutton("True", size_group=sg, clicked=ui.returns("set"), role=role(toggle_var), style='radio_button')
            ui.textbutton("False", size_group=sg, clicked=ui.returns("unset"), role=role(not toggle_var), style='radio_button')
            ui.close()

            ui.frame(style='menu_frame')
            ui.vbox()
            layout.label("Check Button", None)
            ui.textbutton("Check Button", size_group=sg, clicked=ui.returns("toggle"), role=role(toggle_var), style='check_button')
            ui.close()

            ui.frame(style='menu_frame')
            ui.bar(adjustment=adj, style='bar', xmaximum=200)

            ui.close() # vbox

            ui.frame(style='menu_frame')
            ui.bar(adjustment=adj, style='vbar', ymaximum=200)

            ui.vbox(box_spacing=10)
            
            ui.frame(style='menu_frame', xmaximum=0.9)
            ui.vbox(box_spacing=20)
            layout.prompt("This a prompt. Hopefully, we've made this long enough to wrap around at least once.", None)
            ui.text("This is text, and hopefully we've made it long enough to wrap around at least once.", style='text')
            ui.text("This is small text, and hopefully we've made it long enough to wrap around at least once.", style='small_text')
            ui.close()

            ui.frame(style='menu_frame')
            ui.side(['c', 'b', 'r' ], spacing=2)

            data = [
                (0, 'line 0 (spacing 0)'),
                (1, 'line 1 (spacing 1, and this line is selected)'),
                (1, 'line 2 (spacing 1)'),
                (2, 'line 3 (spacing 2)'),
                (1, 'line 4 (spacing 1)'),
                (0, 'line 5 (spacing 0)'),
                (1, 'line 6 (spacing 1)'),
                (2, 'line 7 (spacing 2)'),
                (1, 'line 8 (spacing 1)'),
                (2, 'line 9 (spacing 2)'),
                ]

            vp = ui.viewport(xmaximum=250, ymaximum=100)
            layout.list(data, selected=1)

            ui.bar(adjustment=vp.xadjustment, style='scrollbar')
            ui.bar(adjustment=vp.yadjustment, style='vscrollbar')
            ui.close()
            
            ui.close() # vbox
            ui.close() # hbox

            ui.frame(style='menu_frame', xalign=.01, yalign=.99)
            ui.textbutton("Return to the Debug Menu", clicked=ui.returns("return"))
            
            rv = ui.interact()
            if rv == "return":
                renpy.jump("_developer_screen")

            elif rv == "set":
                toggle_var = True
            elif rv == "unset":
                toggle_var = False
            elif rv == "toggle":
                toggle_var = not toggle_var

label _style_hierarchy:

    python hide:

        ui.window(style=style.gm_root)
        ui.null()

        ui.frame(ymargin=10, xmargin=10, style=style.menu_frame)
        ui.side(['t', 'c', 'r', 'b'], spacing=2)

        layout.label("Style Hierarchy", None)

        hier = renpy.style.style_hierarchy()

        entries = [ (i[0], i[1] + " - " + str(i[2])) for i in hier if i[2] ]
        
        vp = ui.viewport(mousewheel=True)
        layout.list(entries)
        ui.bar(adjustment=vp.yadjustment, style='vscrollbar')

        layout.button(u"Return to the Debug Menu", None, clicked=ui.returns(True))
        
        ui.close()
        
        ui.interact()
        
    jump _developer_screen
    
            
                      
                      
        
