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

        # The number of columns of files to show at once.
        library.file_page_cols = 2

        # The number of rows of files to show at once.
        library.file_page_rows = 5

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
            ( "Preferences", "_preferences" ),
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

        # Transition that occurs when entering the game menu.
        library.enter_transition = None

        # Transition that occurs when leaving the game menu.
        library.exit_transition = None

        # True if the skip indicator should be shown.
        library.skip_indicator = True

        # This is updated to give the user an idea of where a save is
        # taking place.
        save_name = ''

        # True if we're at the main menu, false otherwise.
        _at_main_menu = False

        # True if we can save, false otherwise.
        _can_save = True

        def _button_factory(label,
                            type=None,
                            selected=None,
                            disabled=False,
                            clicked=None,
                            **properties):
            """
            This function is called to create the various buttons used
            in the game menu. By overriding this function, one can
            (for example) replace the default textbuttons with image buttons.
            When it is called, it's expected to add a button to the screen.

            @param label: The label of this button, before translation. 

            @param type: The type of the button. One of "mm" (main menu),
            "gm_nav" (game menu), "file_picker_nav", "yesno", or "prefs".

            @param selected: True if the button is selected, False if not,
            or None if it doesn't matter.

            @param disabled: True if the button is disabled, False if not.

            @param clicked: A function that should be executed when the
            button is clicked.

            @param properties: Addtional layout properties.
            """

            style = type

            if selected and not disabled:
                style += "_selected"

            if disabled:
                clicked = None

            style = style + "_button"
            text_style = style + "_text"

            ui.textbutton(_(label), style=style, text_style=text_style, clicked=clicked, **properties)

        def _label_factory(label, type, **properties):
            """
            This function is called to create a new label. It can be
            overridden by the user to change how these labels are created.

            @param label: The label of the box.

            @param type: "prefs" or "yesno". 

            @param properties: This may contain position properties.
            """

            ui.text(_(label), style=type + "_label", **properties)

        # The function that's used to translate strings in the game menu.
        def _(s):
            """
            Translates s into another language or something.
            """
            
            if s in library.translations:
                return library.translations[s]
            else:
                return s

        # Are the windows currently hidden?
        _windows_hidden = False

    # Set up the default keymap.    
    python hide:

        # Called to make a screenshot happen.
        def screenshot():
            renpy.screenshot("screenshot.bmp")

        def invoke_game_menu():
            renpy.play(library.enter_sound)
            renpy.call_in_new_context('_game_menu')

        def toggle_skipping():
            config.skipping = not config.skipping

        # The default keymap.
        km = renpy.Keymap(
            rollback = renpy.rollback,
            screenshot = screenshot,
            toggle_fullscreen = renpy.toggle_fullscreen,
            toggle_music = renpy.toggle_music,
            toggle_skip = toggle_skipping,
            game_menu = invoke_game_menu,
            hide_windows = renpy.curried_call_in_new_context("_hide_windows")
            )

        config.underlay = [ km ]


    # The skip indicator.
    python hide:

        def skip_indicator():

            if config.allow_skipping and library.skip_indicator:

                ui.conditional("config.skipping")
                ui.text(_("Skip Mode"), style='skip_indicator')

        config.overlay_functions.append(skip_indicator)

    return

label _hide_windows:

    if _windows_hidden:
        return

    python:
        _windows_hidden = True
        ui.saybehavior()
        ui.interact(suppress_overlay=True)
        _windows_hidden = False

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

    scene

    python hide:

        ui.add(renpy.Keymap(toggle_fullscreen = renpy.toggle_fullscreen))
        ui.keymousebehavior()

        ui.window(style='mm_root_window')
        ui.fixed()

        ui.window(style='mm_menu_window')
        ui.vbox()

        for text, label in library.main_menu:
            _button_factory(text, "mm", clicked=ui.returns(label))

        ui.close()
        ui.close()

        store._result = ui.interact(suppress_overlay = True,
                                    suppress_underlay = True)

    # Computed jump to the appropriate label.
    $ renpy.jump(_result)

    return

# Used to call the game menu. 
label _continue:
    $ _can_save = False
    $ _at_main_menu = True
    
    $ renpy.call_in_new_context("_game_menu_load")

    $ _can_save = True
    $ _at_main_menu = False

    jump _main_menu

# Used to call the game menu. 
label _preferences:
    $ _can_save = False
    $ _at_main_menu = True
    
    $ renpy.call_in_new_context("_game_menu_preferences")

    $ _can_save = True
    $ _at_main_menu = False

    jump _main_menu
    

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
            ui.vbox(focus='gm_nav')
            
            for key, label, target, enabled in library.game_menu:

                clicked = ui.jumps(target)
                disabled = False

                if not eval(enabled):
                    disabled = True
                    clicked = None
                             
                _button_factory(label, "gm_nav", selected=(key==selected),
                                disabled=disabled, clicked=clicked)

            ui.close()
            ui.close()
                
        def _game_interact():
            
            return ui.interact(suppress_underlay=True,
                               suppress_overlay=True)


        def _render_new_slot(name, save):
            
            if save:
                clicked=ui.returns(("return", (name, False)))
                enable_hover = True
            else:
                clicked = None
                enable_hover = True

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

            # The number of slots in a page.
            file_page_length = library.file_page_cols * library.file_page_rows

            saves, newest = renpy.saved_games()

            # The index of the first entry in the page.
            fpi = _scratch.file_picker_index

            if fpi is None:
                fpi = 0

                if newest:
                    fpi = (int(newest) - 1) // file_page_length * file_page_length

                if fpi < 0:
                    fpi = 0

                
            while True:

                if fpi < 0:
                    fpi = 0

                _scratch.file_picker_index = fpi

                # Show Navigation
                _game_nav(selected)
                
                ui.window(style='file_picker_window')
                ui.vbox() # whole thing.
                
                # Draw the navigation.
                ui.hbox(padding=library.padding * 10, style='file_picker_navbox') # nav buttons.

                def tb(cond, label, clicked):
                    _button_factory(label, "file_picker_nav", disabled=not cond, clicked=clicked)

                # Previous
                tb(fpi > 0, _('Previous'), ui.returns(("fpidelta", -1)))

                # Quick Access
                for i in range(0, library.file_quick_access_pages):
                    target = i * file_page_length
                    tb(fpi != target, str(i + 1), ui.returns(("fpiset", target)))

                # Next
                tb(True, _('Next'), ui.returns(("fpidelta", +1)))

                # Done with nav buttons.
                ui.close()

                # This draws a single slot.
                def entry(offset):
                    i = fpi + offset

                    name = str(i + 1)

                    if name not in saves:
                        _render_new_slot(name, save)
                    else:
                        _render_savefile(name, saves[name], newest)
                    
                # Actually draw a slot.
                ui.grid(library.file_page_cols,
                        library.file_page_rows,
                        style='file_picker_grid',
                        transpose=True) # slots

                for i in range(0, file_page_length):
                    entry(i)

                ui.close() # slots

                ui.close() # whole thing

                result = _game_interact()
                type, value = result

                if type == "return":
                    return value

                if type == "fpidelta":
                    fpi += value * file_page_length

                if type == "fpiset":
                    fpi = value

                
        def _yesno_prompt(screen, message):

            _game_nav(screen)

            ui.window(style='yesno_window')
            ui.vbox(library.padding * 10, xpos=0.5, xanchor='center', ypos=0.5, yanchor='center')

            _label_factory(message, "yesno", xpos=0.5, xanchor='center')

            ui.grid(5, 1, xfill=True)

            # The extra nulls are because we want equal whitespace surrounding
            # the two buttons. It should work as long as we have xfill=True
            ui.null()
            _button_factory("Yes", 'yesno', clicked=ui.returns(True), xpos=0.5, xanchor='center')
            ui.null()
            _button_factory("No", 'yesno', clicked=ui.returns(False), xpos=0.5, xanchor='center')
            ui.null()

            ui.close()
            ui.close()

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
label _enter_game_menu:
    scene
    $ renpy.movie_stop()
    $ renpy.take_screenshot((library.thumbnail_width, library.thumbnail_height))

    if library.enter_transition:
        $ renpy.transition(library.enter_transition)

    if renpy.has_label("enter_game_menu"):
        call enter_game_menu

    return

# Entry points from the game into menu-space.
label _game_menu:
label _game_menu_save:
    call _enter_game_menu
    jump _save_screen

label _game_menu_load:
    call _enter_game_menu
    jump _load_screen

label _game_menu_preferences:
    call _enter_game_menu
    jump _prefs_screen

label _confirm_quit:
    call _enter_game_menu
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

    if library.exit_transition:
        $ renpy.transition(library.exit_transition)

    return

# Random nice things to have.
init:
    $ centered = Character(None, what_style="centered_text", window_style="centered_window")
    image text = renpy.ParameterizedText(style="centered_text")
    
        
