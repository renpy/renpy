# This file consists of renpy functions that aren't expected to be
# touched by the user too much. We reserve the _ prefix for names
# defined in the library.

# It's strongly reccomended that you don't edit this file, as future
# releases of Ren'Py will probably change this file to include more
# functionality.

# It's also strongly recommended that you leave this file in the
# game directory, so its functionality is included in your game.



init -500:
    python:

        # These are settings that the user can tweak to control the
        # look of the main menu and the load/save/escape screens.

        # Used to store library settings.
        library = object()

        # The number of files to show at once.
        library.file_page_length = 4

        # A small amount of padding.
        library.padding = 5

        # The width of a thumbnail.
        library.thumbnail_width = 100

        # The height of a thumbnail.
        library.thumbnail_height = 75

        # The contents of the main menu.
        library.main_menu = [
            ( "Start Game", "start" ),
            ( "Continue Game", "_continue" ),
            ( "Quit Game", "_quit" ),
            ]

        # Used to translate strings in the library.
        library.translations = { }

        # This is updated to give the user an idea of where a save is
        # taking place.
        save_name = ''

# The function that's used to translate strings in the game menu.
init:
    python:
        def _(s):
            """
            Translates s into another language or something.
            """
            
            if s in library.translations:
                return library.translations[s]
            else:
                return s

##############################################################################

init:

    python:
        # Called to make a screenshot happen.
        def _screenshot():
            renpy.screenshot("screenshot.bmp")

        # Are the windows currently hidden?
        _windows_hidden = False

        # Hides the windows.
        def _hide_windows():
            global _windows_hidden

            if _windows_hidden:
                return

            try:
                _windows_hidden = True
                renpy.interact(renpy.SayBehavior())
            finally:
                _windows_hidden = False

        # A keymouse object that we use on the mainmenu and gamemenu
        # screens.
        _keymouse = renpy.KeymouseBehavior()
                
    # Set up the default keymap.    
    python hide:
        # The default keymap.
        km = renpy.Keymap(
            K_PAGEUP = renpy.rollback,
            mouse_4 = renpy.rollback,
            s = _screenshot,
            f = renpy.toggle_fullscreen,
            m = renpy.toggle_music,
            K_ESCAPE = renpy.curried_call_in_new_context("_game_menu"),
            mouse_3 = renpy.curried_call_in_new_context("_game_menu"),
            mouse_2 = _hide_windows,
            )

        config.underlay = [ km ]

    return
        
# This is the true starting point of the program. Sssh... Don't
# tell anyone.
label _start:
    jump _main_menu

# This shows the main menu to the user. 
label _main_menu:    

    # Let the user completely override the main menu.
    if renpy.has_label("main_menu"):
        jump main_menu

label _library_main_menu:
    
    python hide:

        # Show the main menu screen.
        vbox = renpy.VBox()

        for text, label in library.main_menu:
            vbox.add(renpy.TextButton(text, clicked=_return(label)))

        menu_window = renpy.Window(vbox, style='mm_menu_window')
        
        fixed = renpy.Fixed()
        fixed.add(menu_window)

        root_window = renpy.Window(fixed, style='mm_root_window')

        store._result = renpy.interact(_keymouse, root_window,
                                       suppress_overlay=True,
                                       suppress_underlay=True)

    # Computed jump to the appropriate label.
    $ renpy.jump(_result)

    return

# Used to call the game menu. 
label _continue:
    $ renpy.call_in_new_context("_load_menu")

    jump _library_main_menu
    

##############################################################################
# 
# Code for the game menu.

init -500:
    python:
        
        # This returns a window containing the game menu navigation
        # buttons, set up to jump to the appropriate screen sections.
        def _game_nav(selected):

            buttons = [
                ( "return", _("Return to Game"), "_return"),
                ( "load", _("Load Game"), "_load_screen" ),
                ( "save", _("Save Game"), "_save_screen" ),
                ( "prefs", _("Preferences"), "_prefs_screen" ),
                ( "mainmenu", _("Main Menu"), "_full_restart" ),
                ( "quit", _("Quit Game"), "_confirm_quit" ),
                ]

            vbox = renpy.VBox()
            win = renpy.Window(vbox, style='gm_nav_window')

            for key, label, target in buttons:
                style="button"
                text_style="button_text"
                
                if key == selected:
                    style = 'selected_button'
                    text_style = 'selected_button_text'

                def clicked(target=target):
                    renpy.jump(target)
                    
                tb = renpy.TextButton(label,
                                      style=style,
                                      text_style=text_style,
                                      clicked=clicked)
                vbox.add(tb)

            return win
                
        def _game_interact(selected, *widgets):

            fixed = renpy.Fixed()
            win = renpy.Window(fixed, style='gm_root_window')
            fixed.add(_game_nav(selected))

            for w in widgets:
                fixed.add(w)

            return renpy.interact(_keymouse, win,
                                  suppress_underlay=True,
                                  suppress_overlay=True
                                  )

        _file_picker_index = 0

        def _render_filename(filename, newest_filename):

            if filename is None:
                return renpy.Text(_("Save in new slot."), style='file_picker_new_slot')

            hbox = renpy.HBox(padding=library.padding)

            if filename == newest_filename:
                hbox.add(renpy.Text(_("New"), style='file_picker_new'))
            else:
                hbox.add(renpy.Text(_("Old"), style='file_picker_old'))

            hbox.add(renpy.load_screenshot(filename))

            hbox.add(renpy.Text(renpy.load_extra_info(filename), style='file_picker_extra_info'  ))

            return hbox

        # This displays a file picker that can chose a save file from
        # the list of save files.
        def _file_picker(selected, files):

            nsg = renpy.newest_save_game()

            while True:

                if _file_picker_index >= len(files):
                    store._file_picker_index -= library.file_page_length

                if _file_picker_index < 0:
                    store._file_picker_index = 0

                fpi = _file_picker_index

                cur_files = files[fpi:fpi + library.file_page_length]

                vbox = renpy.VBox()

                hbox = renpy.HBox(padding=library.padding * 3)

                def tb(cond, label, clicked):
                    if cond:
                        style = 'button'
                        text_style = 'button_text'
                    else:
                        style = 'disabled_button'
                        text_style = 'disabled_button_text'

                    return renpy.TextButton(label, style=style, text_style=text_style, clicked=clicked)


                hbox.add(tb(fpi > 0,
                            _('Previous Page'), _return(("fpidelta", -1))))
                hbox.add(tb(fpi + library.file_page_length < len(files),
                            _('Next Page'), _return(("fpidelta", +1))))
                vbox.add(hbox)

                for i in cur_files:
                    child = _render_filename(i, nsg)
                    
                    button = renpy.Button(child,
                                          style='file_picker_entry',
                                          clicked=_return(("return", i)))

                    vbox.add(button)

                win = renpy.Window(vbox, style='file_picker_window')

                result = _game_interact(selected, win)

                type, value = result

                if type == "return":
                    return value

                if type == "fpidelta":
                    store._file_picker_index += value * library.file_page_length
                
        def _yesno_prompt(screen, message):

            prompt = renpy.Text(message, style='yesno_prompt')
            yes = renpy.TextButton(_("Yes"), style='yesno_yes',
                               clicked=_return(True))
            no =  renpy.TextButton(_("No"), style='yesno_no',
                               clicked=_return(False))

            return _game_interact(screen, prompt, yes, no) 
            
        # Returns a button for a single preference and value.
        def _prefbutton(label, var, value):

            def clicked():
                setattr(_preferences, var, value)
                return True

            style = 'button'
            text_style = 'button_text'

            if getattr(_preferences, var) == value:
                style = 'selected_button'
                text_style = 'selected_button_text'

            return renpy.TextButton(_(label), style=style,
                                    text_style=text_style, clicked=clicked)

        # Returns a vbox for a single preference.
        def _prefvbox(label, var, entries):

            rv = renpy.VBox(style='prefs_pref')
            rv.add(renpy.Text(_(label), style='prefs_label'))

            for blabel, value in entries:
                rv.add(_prefbutton(blabel, var, value))

            return rv

            
                                        

label _load_menu:
    $ renpy.take_screenshot((library.thumbnail_width, library.thumbnail_height))

    jump _load_screen

label _game_menu:
    $ renpy.take_screenshot((library.thumbnail_width, library.thumbnail_height))

    jump _save_screen

label _load_screen:

    python:
        _fn = _file_picker("load", renpy.saved_game_filenames() )

    python:
        renpy.load(_fn)

    jump _load_screen

label _save_screen:
    $ _fn = _file_picker("save", renpy.saved_game_filenames() + [ None ] )

    if not _fn or _yesno_prompt("save", _("Are you sure you want to overwrite your save?")):
        $ renpy.save(_fn, renpy.time.strftime("%Y-%m-%d %H:%M:%S\n") + save_name)

    jump _save_screen

# The preferences screen.
label _prefs_screen:

    python hide:
        prefs_left = [
            ( 'Display', 'fullscreen',
              [ ('Window', False), ('Fullscreen', True) ] ),
            ( 'Music', 'music',
              [ ('Enabled', True), ('Disabled', False) ] ),
            ( 'Sound Effects', 'sound',
              [ ('Enabled', True), ('Disabled', False) ] ),
            ]

        prefs_right = [
            ('CTRL Skips', 'skip_unseen',
             [ ('Seen Messages', False), ('All Messages', True) ] ),
            ('Transitions', 'transitions',
             [ ('All', 2), ('Some', 1), ('None', 0) ]),
            ]

        if config.annoying_text_cps:
            prefs_right.append(('Text Display', 'fast_text', [ ('Slow', False), ('Fast', True) ]))

        vbox_left = renpy.VBox(padding=library.padding * 3, style='prefs_left')

        for label, var, entries in prefs_left:
            vbox_left.add(_prefvbox(label, var, entries))

        vbox_right = renpy.VBox(padding=library.padding * 3, style='prefs_right')

        for label, var, entries in prefs_right:
            vbox_right.add(_prefvbox(label, var, entries))

        _game_interact("prefs", vbox_left, vbox_right)

    jump _prefs_screen
        
        


# Asks the user if he wants to quit.
label _confirm_quit:
    if _yesno_prompt("quit", _("Are you sure you want to end the game?")):
        jump _quit
    else:
        jump _return

label _quit:
    $ renpy.quit()

label _full_restart:
    $ renpy.full_restart()

# Return to the game, after restoring the keymap.
label _return:

    return

# Random nice things to have.
init:
    $ centered = Character(None, what_style="centered_text", window_style="centered_window")
    image text = renpy.ParameterizedText(style="centered_text")
    
        
