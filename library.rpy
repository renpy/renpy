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

        # This is updated to give the user an idea of where a save is
        # taking place.
        save_name = ''
        

##############################################################################

init:

    python:
        # Called to make a screenshot happen.
        def _screenshot():
            renpy.screenshot("screenshot.bmp")



# Installs the keymap that lets the user do things like invoke the
# game menu.
label _install_keymap:
    
    # Set up the default keymap.    
    python hide:
        config.underlay = [ ]
        config.overlay = [ ]

        # The default keymap.
        km = renpy.Keymap(
            K_PAGEUP = renpy.rollback,
            mouse_4 = renpy.rollback,
            s = _screenshot,
            f = renpy.toggle_fullscreen,
            m = renpy.toggle_music,
            K_ESCAPE = renpy.curried_call_in_new_context("_game_menu"),
            mouse_3 = renpy.curried_call_in_new_context("_game_menu"),
            )

        config.underlay.append(km)

    return
        
# This is the true starting point of the program. Sssh... Don't
# tell anyone.
label _start:

    $ _started = False

    call _main_menu

    $ _started = True
    call _install_keymap
    
    jump start

# This shows the main menu to the user. 
label _main_menu:

    # jump start

    python hide:

        vbox = renpy.VBox()

        vbox.add(renpy.TextButton('New Game', clicked=_return("start")))
        vbox.add(renpy.TextButton('Continue Game', clicked=_return("continue")))
        vbox.add(renpy.TextButton('Quit', clicked=_return("quit")))

        menu_window = renpy.Window(vbox, style='mm_menu_window')
        
        fixed = renpy.Fixed()
        fixed.add(menu_window)

        root_window = renpy.Window(fixed, style='mm_root_window')

        store._result = renpy.interact(root_window)

    if _result == "start":
        pass
    elif _result == "continue":
        $ renpy.call_in_new_context("_game_menu")
    elif _result == "quit":
        $ renpy.quit()

    return

##############################################################################
# 
# Code for the game menu.

init -500:
    python:
        
        # This returns a window containing the game menu navigation
        # buttons, set up to jump to the appropriate screen sections.
        def _game_nav(selected):

            buttons = [
                ( "return", "Return to Game", "_return"),
                ( "load", "Load Game", "_load_screen" ),
                ( "save", "Save Game", "_save_screen" ),
                # ( "prefs", "Preferences", "_prefs_screen" ),
                ( "mainmenu", "Main Menu", "_full_restart" ),
                ( "quit", "Quit Game", "_quit" ),
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

            return renpy.interact(win)

        _file_picker_index = 0

        def _render_filename(filename, newest_filename):

            if filename is None:
                return renpy.Text("Save in new slot.", style='file_picker_new_slot')

            hbox = renpy.HBox(padding=library.padding)

            if filename == newest_filename:
                hbox.add(renpy.Text("New", style='file_picker_new'))
            else:
                hbox.add(renpy.Text("Old", style='file_picker_old'))

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
                            'Previous Page', _return(("fpidelta", -1))))
                hbox.add(tb(fpi + library.file_page_length < len(files),
                            'Next Page', _return(("fpidelta", +1))))
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
                
                                        

label _game_menu:

    # disable keystrokes.
    $ config.underlay = [ ]    
    $ config.overlay = [ ]
    $ renpy.take_screenshot((library.thumbnail_width, library.thumbnail_height))
    $ renpy.set_overlay([])

    if _started:
        jump _save_screen
    else:
        jump _load_screen

label _load_screen:

    python:
        _fn = _file_picker("load", renpy.saved_game_filenames() )

    call _install_keymap

    python:
        renpy.load(_fn)

    jump _game_menu

label _save_screen:

    python hide:
        fn = _file_picker("save", renpy.saved_game_filenames() + [ None ] )
        renpy.save(fn, renpy.time.strftime("%Y-%m-%d %H:%M:%S\n") + save_name)

    jump _save_screen

label _quit:
    $ renpy.quit()

label _full_restart:
    $ renpy.full_restart()

# Return to the game, after restoring the keymap.
label _return:

    call _install_keymap
    return

