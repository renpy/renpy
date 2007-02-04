# Copyright 2004-2007 PyTom
#
# Please see the LICENSE.txt distributed with Ren'Py for permission to
# copy and modify.

# This file contains code for the game menu, and associated
# functionality that looks an awful lot like it.

init -499:
    python:

        ######################################################################
        # First up, we define a bunch of configuration variable, which the
        # user can change.

        # The contents of the game menu choices.
        config.game_menu = [
                ( "return", u"Return", ui.jumps("_return"), 'True'),
                ( "skipping", u"Begin Skipping", ui.jumps("_return_skipping"), 'config.allow_skipping and not renpy.context().main_menu'),
                ( "prefs", u"Preferences", _intra_jumps("_prefs_screen"), 'True' ),
                ( "save", u"Save Game", _intra_jumps("_save_screen"), 'not renpy.context().main_menu' ),
                ( "load", u"Load Game", _intra_jumps("_load_screen"), 'True'),
                ( "mainmenu", u"Main Menu", lambda : _mainmenu_prompt(), 'not renpy.context().main_menu' ),
                ( "quit", u"Quit", lambda : _quit_prompt("quit"), 'True' ),
                ]

        # If not None, a map from the names of the game menu
        # navigation buttons to new fixed positions for them on
        # the screen.
        config.game_menu_positions = None

        # Music to play when entering the game menu.
        config.game_menu_music = None

        # The number of columns of files to show at once.
        config.file_page_cols = 2

        # The number of rows of files to show at once.
        config.file_page_rows = 5

        # The number of pages to add quick access buttons for.
        config.file_quick_access_pages = 5

        # The positions of file picker components.
        config.file_picker_positions = None
        
        # The width of a thumbnail.
        config.thumbnail_width = 66

        # The height of a thumbnail.
        config.thumbnail_height = 50

        # Sound played when entering the library without clicking a
        # button.
        config.enter_sound = None

        # Sound played when leaving the library without clicking a
        # button.
        config.exit_sound = None

        # Transition that occurs when entering the game menu.
        config.enter_transition = None

        # Transition that occurs when leaving the game menu.
        config.exit_transition = None

        # Transition that's used when going from one screen to another.
        config.intra_transition = None
        
        # This lets us disable the file pager. (So we only have one
        # page of files.)
        config.disable_file_pager = False

        # This lets us disable the thumbnails in the file pager.
        config.disable_thumbnails = False

        # How we format time.
        config.time_format = "%b %d, %H:%M"

        # How we format loade_save slot formats.
        config.file_entry_format = "%(time)s\n%(save_name)s"

        # If True, we will be prompted before loading a game. (This can
        # be changed from inside the game code, so that one can load from
        # the first few screens but not after that.)
        _load_prompt = True

        # The screen that we go to when entering the game menu.
        _game_menu_screen = "_save_screen"

        ######################################################################
        # Next, support code.

        # This is used to store scratch data that's used by the
        # library, but shouldn't be saved out as part of the savegame.
        _scratch = object()
            
        # This returns a window containing the game menu navigation
        # buttons, set up to jump to the appropriate screen sections.
        #
        # This can be overridden by user code. It's called with the
        # name of the selected screen... one of "mainmenu", "prefs",
        # "save", "load", or "quit", at least for the default game
        # menu. If None, then it's an indication that none of the
        # nav buttons should be shown.
        def _game_nav(screen, buttons=True):

            global _screen
            _screen = screen

            ui.add(renpy.Keymap(toggle_fullscreen = renpy.toggle_fullscreen))
            ui.add(renpy.Keymap(game_menu=ui.jumps("_noisy_return")))

            ### gm_root default
            # (window) The style used for the root window of the game
            # menu. This is primarily used to change the background of
            # the game menu.
 
            ui.window(style='gm_root')
            ui.null()

            if not screen:
                return

            ### gm_nav_frame default
            # (window) The style used by a window containing
            # buttons that allow the user to navigate through the
            # different screens of the game menu.

            ### gm_nav_vbox thin_vbox
            # (box) The style that is used by the box inside the
            # gm_nav_frame

            if not config.game_menu_positions:
                ui.window(style='gm_nav_frame')
                ui.vbox(focus='gm_nav', style='gm_nav_vbox')
            
            for key, label, clicked, enabled in config.game_menu:

                disabled = False

                if not eval(enabled):
                    disabled = True
                    clicked = None

                ### gm_nav_button menu_button
                # (window, hover) The style of a game menu
                # navigation button.

                ### gm_nav_button_text menu_button_text
                # (text, hover) The style of the text of a  game
                # menu navigation button.

                if config.game_menu_positions:
                    kwargs = config.game_menu_positions.get(label, { })
                else:
                    kwargs = { }
                
                _button_factory(label, "gm_nav",
                                selected=(key==screen),
                                disabled=disabled,
                                clicked=clicked,
                                properties=kwargs)

            if not config.game_menu_positions:
                ui.close()

        # This is called from the game menu to interact with the
        # user.  It suppresses all of the underlays and overlays.
        def _game_interact():
            
            return ui.interact(suppress_underlay=True,
                               suppress_overlay=True,
                               mouse="gamemenu")

                      
        # This renders a slot with a file in it, in the file picker.
        def _render_savefile(name, extra_info, screenshot, mtime, newest, **positions):


            ### file_picker_entry menu_button
            # (window, hover) The style that is used for each of the
            # slots in the file picker.
            ui.button(style='file_picker_entry',
                      clicked=ui.returns(("return", (name, True))),
                      **positions)
            
            
            ### file_picker_entry_box thin_hbox
            # (box) The style that is used for the hbox inside of a
            # file picker entry.            
            ui.hbox(style='file_picker_entry_box')

            if not config.disable_thumbnails:
                ui.add(screenshot)

            ### file_picker_text default
            # (text) A base style for all text that is displayed in the
            # file picker.

            ### file_picker_new file_picker_text
            # (text) The style that is applied to the number of the new slot in
            # the file picker.

            ### file_picker_old file_picker_text
            # (text) The style that is applied to the number of the old slot in
            # the file picker.
            
            if newest:
                ui.text(name + ". ", style='file_picker_new')
            else:
                ui.text(name + ". ", style='file_picker_old')

            ### file_picker_extra_info file_picker_text
            # (text) The style that is applied to extra info in the file
            # picker. The extra info is the save time, and the save_name
            # if one exists.

            s = config.file_entry_format % dict(
                time=renpy.time.strftime(config.time_format,
                                         renpy.time.localtime(mtime)),
                save_name=extra_info)


            ui.text(s, style='file_picker_extra_info')

            ui.close()
            
        # This renders an empty slot in the file picker.
        def _render_new_slot(name, save, **positions):
            
            if save:
                clicked=ui.returns(("return", (name, False)))
                enable_hover = True
            else:
                clicked = None
                enable_hover = True
    
            ui.button(style='file_picker_entry',
                      clicked=clicked,
                      enable_hover=enable_hover,
                      **positions)

            ui.hbox(style='file_picker_entry_box')

            if not config.disable_thumbnails:
                ui.null(width=config.thumbnail_width,
                        height=config.thumbnail_height)

            
            ui.text(name + ". ", style='file_picker_old')

            ### file_picker_empty_slot file_picker_text
            # (text) The style that is used for the empty slot indicator
            # in the file picker.
            ui.text(_(u"Empty Slot."), style='file_picker_empty_slot')
            ui.close()

        _scratch.file_picker_index = None

        # This displays a file picker that can chose a save file from
        # the list of save files.
        def _file_picker(selected, save):

            # The number of slots in a page.
            file_page_length = config.file_page_cols * config.file_page_rows

            saved_games = renpy.list_saved_games(regexp=r'[0-9]+')

            newest = None
            newest_mtime = None
            save_info = { }

            if config.file_picker_positions:
                positions = config.file_picker_positions
            else:
                positions = { }
            
            for fn, extra_info, screenshot, mtime in saved_games:
                save_info[fn] = (extra_info, screenshot, mtime)

                if mtime > newest_mtime:
                    newest = fn
                    newest_mtime = mtime


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

                # Show navigation
                _game_nav(selected)


                ### file_picker_frame default
                # (window) A window containing the file picker
                # that is used to choose slots for loading and saving.

                ### file_picker_frame_vbox thin_vbox
                # (box) The vbox containing both the nav and the grid in
                # the file picker.

                if not config.file_picker_positions:

                    ui.window(style='file_picker_frame')
                    ui.vbox(style='file_picker_frame_vbox') # whole thing.
                
                if not config.disable_file_pager:

                    ### file_picker_navbox thick_hbox
                    # (box) The box containing the naviation (next/previous)
                    # buttons in the file picker.

                    ### file_picker_nav_button menu_button
                    # (window, hover) The style that is used for enabled file
                    # picker navigation buttons.

                    ### file_picker_nav_button_text menu_button_text
                    # (text) The style that is used for the label of enabled
                    # file picker navigation buttons.
                   
                    # Draw the navigation.
                    if not config.file_picker_positions:
                        ui.hbox(style='file_picker_navbox') # nav buttons.

                    def tb(cond, label, clicked, selected):
                        _button_factory(label,
                                        "file_picker_nav",
                                        disabled=not cond,
                                        clicked=clicked,
                                        selected=selected,
                                        properties=positions.get("nav_" + label, { }))

                    # Previous
                    tb(fpi > 0, _(u'Previous'), ui.returns(("fpidelta", -1)), selected=False)

                    # Quick Access
                    for i in range(0, config.file_quick_access_pages):
                        target = i * file_page_length
                        tb(True, str(i + 1), ui.returns(("fpiset", target)), fpi == target)

                    # Next
                    tb(True, _(u'Next'), ui.returns(("fpidelta", +1)), False)

                    # Done with nav buttons.
                    if not config.file_picker_positions:
                        ui.close()

                # This draws a single slot.
                def entry(offset):
                    i = fpi + offset

                    name = str(i + 1)

                    place = positions.get("entry_" + str(offset + 1), { })
                    
                    if name not in save_info:
                        _render_new_slot(name, save, **place)
                    else:
                        extra_info, screenshot, mtime = save_info[name]
                        _render_savefile(name, extra_info, screenshot,
                                         mtime, newest == name, **place)
                    
                ### file_picker_grid default
                # The style of the grid containing the file
                # picker entries.

                if not config.file_picker_positions:
                    ui.grid(config.file_page_cols,
                            config.file_page_rows,
                            style='file_picker_grid',
                            transpose=True) # slots

                for i in range(0, file_page_length):
                    entry(i)

                if not config.file_picker_positions:                    
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


        # This renders a yes/no prompt, as part of the game menu. If
        # screen is None, then it omits the game menu navigation. 
        def _yesno_prompt(screen, message):
            """
            @param screen: The screen button that should be highlighted when this prompt is shown. If None, then no game menu navigation is shown.

            @param message: The message that is shown to the user to prompt them to answer yes or no.

            This function returns True if the user clicks Yes, or False if the user clicks No.
            """

            _game_nav(screen)

            ### yesno_frame default
            # (window) The style of a window containing a yes/no prompt.

            ### yesno_frame_vbox thick_vbox
            # (box) The style of a box containing the widgets in a
            # yes/no prompt.

            ui.window(style='yesno_frame')
            ui.vbox(style='yesno_frame_vbox')

            ### yesno_label default
            # (text) The style used for the prompt in a yes/no
            # dialog.

            ### yesno_button menu_button
            # (window, hover) The style of yes/no buttons.

            ### yesno_button_text menu_button_text
            # (window, hover) The style of yes/no button text.

            _label_factory(message, "yesno")

            ui.grid(5, 1, xfill=True)

            # The extra nulls are because we want equal whitespace surrounding
            # the two buttons. It should work as long as we have xfill=True
            ui.null()
            _button_factory(u"Yes", 'yesno', clicked=ui.returns(True))
            ui.null()
            _button_factory(u"No", 'yesno', clicked=ui.returns(False))
            ui.null()

            ui.close()
            ui.close()

            return _game_interact()


        def _show_exception(title, message):

            ### error_root default
            # (window) The style of the window containing internal error
            # messages.

            ### error_title default
            # (text) The style of the text containing the title of an
            # error message.

            ### error_body default
            # (text) The style of the body of an error message.

            ui.window(style='error_root')
            ui.vbox()

            ui.text(title, style='error_title')
            ui.text("")
            ui.text(message, style='error_body')
            ui.text("")
            ui.text(_(u"Please click to continue."), style='error_body')

            ui.close()

            ui.saybehavior()

            ui.interact()

        config.old_names["Are you sure you want to quit?"] = "Are you sure you want to quit the game?"

        def _quit_prompt(screen="quit"):

            def prompt():
               return _yesno_prompt(screen, u"Are you sure you want to quit?")
            
            if renpy.invoke_in_new_context(prompt):
                renpy.quit()
            else:
                return

        config.old_names["Are you sure you want to return to the main menu?\nThis will lose unsaved progress."] = "Are you sure you want to return to the main menu?\nThis will end your game."

        def _mainmenu_prompt(screen="mainmenu"):

            def prompt():
               return _yesno_prompt(screen, u"Are you sure you want to return to the main menu?\nThis will lose unsaved progress.")
            
            if renpy.invoke_in_new_context(prompt):
                renpy.full_restart()
            else:
                return


            
##############################################################################
# The actual menus begin around here.

# First up, we have the code that is common to all of the entry points into
# the game.


# This is the code that executes when entering a menu context, except
# for the scene statement.
label _enter_menu_without_scene:
    $ renpy.movie_stop()
    $ renpy.take_screenshot((config.thumbnail_width, config.thumbnail_height))

    # This may be changed, if we are already in the main menu.
    $ renpy.context().main_menu = False

    return

label _enter_menu:
    call _enter_menu_without_scene from _call_enter_menu_without_scene_1
    $ ui.clear()
    return
    
# Factored this all into one place, to make our lives a bit easier.
label _enter_game_menu:
    call _enter_menu from _call__enter_menu_2
    if config.enter_transition:
        $ renpy.transition(config.enter_transition)

    if renpy.has_label("enter_game_menu"):
        call expression "enter_game_menu" from _call_enter_game_menu_1

    if config.game_menu_music:
        $ renpy.music.play(config.game_menu_music, if_changed=True)

    return

##############################################################################
# Now, we have the actual entry points into the various menu screens.

# Entry points from the game into menu-space.
label _game_menu:
    call _enter_game_menu from _call__enter_game_menu_0

    if renpy.has_label("game_menu"):
        jump expression "game_menu"

    jump expression _game_menu_screen

label _game_menu_save:
    call _enter_game_menu from _call__enter_game_menu_1
    jump _save_screen

label _game_menu_load:
    call _enter_game_menu from _call__enter_game_menu_2
    jump _load_screen

label _game_menu_preferences:
    call _enter_game_menu from _call__enter_game_menu_3
    jump _prefs_screen

label _confirm_quit:
    call _enter_menu from _call__enter_menu_3

    if renpy.has_label("confirm_quit"):
        jump expression "confirm_quit"

    $ _quit_prompt(None)
    return


##############################################################################
# Finally, we have the actual menu screens that are shown to the user.

init -499:
    $ config.old_names["Loading will lose unsaved progress.\nAre you sure you want to do this?"] = "Loading a new game will end your current game.\nAre you sure you want to do this?"

label _load_screen:

    if renpy.has_label("_load_screen_hook"):
        call expression "_load_screen_hook" from _call__load_screen_hook
    
    python hide:

        fn, exists = _file_picker("load", False )

        if not renpy.context().main_menu and _load_prompt:
            if _yesno_prompt("load", u"Loading will lose unsaved progress.\nAre you sure you want to do this?"):
                renpy.load(fn)
        else:                        
            renpy.load(fn)

    jump _load_screen

label _save_screen:
    
    if renpy.has_label("_save_screen_hook"):
        call expression "_save_screen_hook" from _call__save_screen_hook

    $ _fn, _exists = _file_picker("save", True)

    if not _exists or _yesno_prompt("save", u"Are you sure you want to overwrite your save?"):
        python hide:

            if save_name:
                full_save_name = save_name
            else:
                full_save_name = ""

            try:
                renpy.save(_fn, full_save_name)

            except Exception, e:

                if config.debug:
                    raise
                
                message = ( _(u"The error message was:") + "\n\n" + 
                            e.__class__.__name__  + ": " + unicode(e) + "\n\n" +
                            _(u"You may want to try saving in a different slot, or playing for a while and trying again later.") )

                _show_exception(_(u"Save Failed."), message)
                
                
    jump _save_screen

label _quit:
    $ renpy.quit()

label _return_skipping:
    $ config.skipping = "slow"
    jump _return
    

# Make some noise, then return.
label _noisy_return:
    $ renpy.play(config.exit_sound)

# Return to the game.
label _return:

    if renpy.context().main_menu:
        jump _main_menu

    if config.exit_transition:
        $ renpy.transition(config.exit_transition)

    return
