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
        library.file_page_length = 10

        # The number of pages to add quick access buttons for.
        library.file_quick_access_pages = 5

        # A small amount of padding.
        library.padding = 2

        # The width of a thumbnail.
        library.thumbnail_width = 66

        # The height of a thumbnail.
        library.thumbnail_height = 50

        # The contents of the main menu.
        library.main_menu = [
            ( "Start Game", "start" ),
            ( "Continue Game", "_continue" ),
            ( "Quit Game", "_quit" ),
            ]

        # The contents of the game menu choices.
        library.game_menu = [
                ( "return", "Return", "_return", 'True'),
                ( "prefs", "Preferences", "_prefs_screen", 'True' ),
                ( "save", "Save Game", "_save_screen", '_can_save' ),
                ( "load", "Load Game", "_load_screen", 'True'),
                ( "mainmenu", "Main Menu", "_full_restart", 'not _at_main_menu' ),
                ( "quit", "Quit", "_quit_screen", 'True' ),
                ]

        # Used to translate strings in the library.
        library.translations = { }

        # Sound played when entering the library without clicking a
        # button.
        library.enter_sound = None

        # Sound played when leaving the library without clicking a
        # button.
        library.exit_sound = None


        # This is updated to give the user an idea of where a save is
        # taking place.
        save_name = ''

        # True if we're at the main menu, false otherwise.
        _at_main_menu = False

        # True if we can save, false otherwise.
        _can_save = True

        # The function that's used to translate strings in the game menu.
        def _(s):
            """
            Translates s into another language or something.
            """
            
            if s in library.translations:
                return library.translations[s]
            else:
                return s

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


    # Set up the default keymap.    
    python hide:

        def invoke_game_menu():
            renpy.play(library.enter_sound)
            renpy.call_in_new_context('_game_menu')

        # The default keymap.
        km = renpy.Keymap(
            rollback = renpy.rollback,
            screenshot = _screenshot,
            toggle_fullscreen = renpy.toggle_fullscreen,
            toggle_music = renpy.toggle_music,
            game_menu = invoke_game_menu,
            hide_windows = _hide_windows,
            )

        config.underlay = [ km ]

    return
        
# This is the true starting point of the program. Sssh... Don't
# tell anyone.
label _start:

    if renpy.has_label("splashscreen") and not _restart:
        call splashscreen

    jump _main_menu

# This shows the main menu to the user. 
label _main_menu:    

    # Let the user completely override the main menu.
    if renpy.has_label("main_menu"):
        jump main_menu

label _library_main_menu:

    python hide:

        ui.keymousebehavior()

        ui.window(style='mm_root_window')
        ui.fixed()

        ui.window(style='mm_menu_window')
        ui.vbox()

        for text, label in library.main_menu:
            ui.textbutton(text, clicked=ui.returns(label))

        ui.close()
        ui.close()

        store._result = renpy.interact(suppress_overlay = True,
                                       suppress_underlay = True)

    # Computed jump to the appropriate label.
    $ renpy.jump(_result)

    return

# Used to call the game menu. 
label _continue:
    $ _can_save = False
    $ _at_main_menu = True
    
    $ renpy.call_in_new_context("_load_menu")

    $ _can_save = True
    $ _at_main_menu = False

    jump _library_main_menu
    

##############################################################################
# 
# Code for the game menu.

init -500:
    python:

        # This is used to store scratch data that's used by the
        # library, but shouldn't be saved out as part of the savegame.
        _scratch = object()

        
        # This returns a window containing the game menu navigation
        # buttons, set up to jump to the appropriate screen sections.
        def _game_nav(selected):

            ui.keymousebehavior()

            ui.add(renpy.Keymap(game_menu=ui.jumps("_noisy_return")))

            ui.window(style='gm_root_window')
            ui.fixed()

            ui.window(style='gm_nav_window')
            ui.vbox()
            
            for key, label, target, enabled in library.game_menu:
                style="gm_nav_button"
                text_style="gm_nav_button_text"
                
                if key == selected:
                    style = 'gm_nav_selected_button'
                    text_style = 'gm_nav_selected_button_text'

                clicked = ui.jumps(target)

                if not eval(enabled):
                    style = 'gm_nav_disabled_button'
                    text_style = 'gm_nav_disabled_button_text'

                    clicked = lambda : None
                             
                    
                ui.textbutton(_(label), style=style, text_style=text_style,
                              clicked=clicked)

            ui.close()
            ui.close()
                
        def _game_interact():
            
            return renpy.interact(suppress_underlay=True,
                                  suppress_overlay=True)


        def _render_new_slot(name, save):
            
            if save:
                clicked=ui.returns(("return", (name, False)))
                enable_hover = True
            else:
                clicked=None
                enable_hover = False

            ui.button(style='file_picker_entry',
                      clicked=clicked,
                      enable_hover=enable_hover)
            
            ui.hbox(padding=library.padding)
            ui.null(width=library.thumbnail_width,
                    height=library.thumbnail_height)
            ui.text(name + ". ", style='file_picker_old')
            ui.text(_("Empty Slot."), style='file_picker_empty_slot')
            ui.close()
                      
            
        def _render_savefile(name, info, newest):

            image, extra = info

            ui.button(style='file_picker_entry',
                      clicked=ui.returns(("return", (name, True))))
            
            ui.hbox(padding=library.padding)
            ui.add(image)
            
            if name == newest:
                ui.text(name + ". ", style='file_picker_new')
            else:
                ui.text(name + ". ", style='file_picker_old')

            
            ui.text(extra, style='file_picker_extra_info')

            ui.close()
            

        _scratch.file_picker_index = None

        # This displays a file picker that can chose a save file from
        # the list of save files.
        def _file_picker(selected, save):

            saves, newest = renpy.saved_games()

            # The index of the first entry in the page.
            fpi = _scratch.file_picker_index

            if fpi is None:
                fpi = 0

                if newest:
                    fpi = int(newest) // library.file_page_length * library.file_page_length

                
            # The length of a half-page of files.
            hfpl = library.file_page_length // 2

            while True:

                if fpi < 0:
                    fpi = 0

                _scratch.file_picker_index = fpi

                # Show Navigation
                _game_nav(selected)
                
                ui.window(style='file_picker_window')

                ui.vbox() # whole thing.
                
                ui.hbox(padding=library.padding * 10, style='file_picker_navbox') # nav buttons.

                def tb(cond, label, clicked):
                    if cond:
                        style = 'button'
                        text_style = 'button_text'
                    else:
                        style = 'disabled_button'
                        text_style = 'disabled_button_text'

                    ui.textbutton(label, style=style, text_style=text_style, clicked=clicked)


                tb(fpi > 0, _('Previous'), ui.returns(("fpidelta", -1)))

                for i in range(0, library.file_quick_access_pages):
                    target = i * library.file_page_length
                    tb(fpi != target, str(i + 1), ui.returns(("fpiset", target)))

                tb(True, _('Next'), ui.returns(("fpidelta", +1)))

                ui.close() # nav buttons.

                def entry(offset):
                    i = fpi + offset

                    name = str(i + 1)

                    if name not in saves:
                        _render_new_slot(name, save)
                    else:
                        _render_savefile(name, saves[name], newest)
                    

                ui.hbox() # slots

                ui.vbox()
                for i in range(0, hfpl):
                    entry(i)
                ui.close()

                ui.vbox()
                for i in range(hfpl, hfpl * 2):
                    entry(i)
                ui.close()
                    
                ui.close() # slots

                ui.close() # whole thing

                result = _game_interact()
                type, value = result

                if type == "return":
                    return value

                if type == "fpidelta":
                    fpi += value * library.file_page_length

                if type == "fpiset":
                    fpi = value

                
        def _yesno_prompt(screen, message):

            _game_nav(screen)

            ui.text(message, style='yesno_prompt')
            ui.textbutton(_("Yes"), style='yesno_yes', clicked=ui.returns(True))
            ui.textbutton(_("No"), style='yesno_no', clicked=ui.returns(False))

            return _game_interact()

        def _show_exception(title, message):
            ui.add(Solid((0, 0, 0, 255)))
            ui.vbox()

            ui.text(title, color=(255, 128, 128, 255))
            ui.text("")
            ui.text(message)
            ui.text("")
            ui.text("Please click to continue.")

            ui.close()

            ui.saybehavior()

            ui.interact()
                     


# Factored this all into one place, to make our lives a bit easier.
label _take_screenshot:
    $ renpy.take_screenshot((library.thumbnail_width, library.thumbnail_height))
    return

# Entry points from the game into menu-space.
label _load_menu:
    call _take_screenshot
    jump _load_screen

label _game_menu:
    call _take_screenshot
    jump _save_screen

label _confirm_quit:
    call _take_screenshot
    jump _quit_screen

# Menu screens.
label _load_screen:

    python:
        _fn, _exists = _file_picker("load", False )

    python:
        renpy.load(_fn)

    jump _load_screen

label _save_screen:
    $ _fn, _exists = _file_picker("save", True)

    if not _exists or _yesno_prompt("save", _("Are you sure you want to overwrite your save?")):
        python hide:

            if save_name:
                full_save_name = "\n" + save_name
            else:
                full_save_name = ""

            try:
                renpy.save(_fn, renpy.time.strftime("%b %d, %H:%M") +
                           full_save_name)

            except Exception, e:

                if config.debug:
                    raise
                
                message = ( "The error message was:\n\n" +
                            e.__class__.__name__  + ": " + unicode(e) + "\n\n" +
                            "You may want to try saving in a different slot, or playing for a while and trying again later.")

                _show_exception(_("Save Failed."), message)
                
                
    jump _save_screen

# Asks the user if he wants to quit.
label _quit_screen:
    if _yesno_prompt("quit", _("Are you sure you want to end the game?")):
        jump _quit
    else:
        jump _return

label _quit:
    $ renpy.quit()

label _full_restart:
    $ renpy.full_restart()

# Make some noise, then return.
label _noisy_return:
    $ renpy.play(library.exit_sound)

# Return to the game.
label _return:
    return

# Random nice things to have.
init:
    $ centered = Character(None, what_style="centered_text", window_style="centered_window")
    image text = renpy.ParameterizedText(style="centered_text")
    
        
