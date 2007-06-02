# Copyright 2004-2007 PyTom
#
# Please see the LICENSE.txt distributed with Ren'Py for permission to
# copy and modify.

# This file contains code for the game menu, and associated
# functionality that looks an awful lot like it.

init -1160 python:

    ######################################################################
    # First up, we define a bunch of configuration variable, which the
    # user can change.

    # The contents of the game menu choices.
    config.game_menu = [
            ( "return", u"Return", ui.jumps("_return"), 'True'),
            ( "skipping", u"Begin Skipping", ui.jumps("_return_skipping"), 'config.allow_skipping and not renpy.context().main_menu'),
            ( "prefs", u"Preferences", _intra_jumps("_prefs_screen", "intra_transition"), 'True' ),
            ( "save", u"Save Game", _intra_jumps("_save_screen", "intra_transition"), 'not renpy.context().main_menu' ),
            ( "load", u"Load Game", _intra_jumps("_load_screen", "intra_transition"), 'True'),
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

    # Transition that's used when going from the main to the game
    # menu.
    config.main_game_transition = None

    # Transition that's used when going from the game to the main
    # menu.
    config.game_main_transition = None

    # Transition that's used at the end of the game, when returning
    # to the main menu.
    config.end_game_transition = None

    # Transition that's used at the end of the splash screen, when
    # it is shown.
    config.end_splash_transition = None


    # This lets us disable the file pager. (So we only have one
    # page of files.)
    config.disable_file_pager = False

    # This lets us disable the thumbnails in the file pager.
    config.disable_thumbnails = False

    # How we format time.
    config.time_format = "%b %d, %H:%M"

    # How we format loade_save slot formats.
    config.file_entry_format = "%(time)s\n%(save_name)s"

    # Do we have autosave and quicksave?
    config.has_autosave = True
    config.has_quicksave = False

    # If True, we will be prompted before loading a game. (This can
    # be changed from inside the game code, so that one can load from
    # the first few screens but not after that.)
    _load_prompt = True

    # The screen that we go to when entering the game menu.
    _game_menu_screen = "_save_screen"

    ######################################################################
    # Styles
    
    style.gm_root = Style(style.default, heavy=True, help='The root window of the game menu.')

    style.gm_nav_frame = Style(style.default, heavy=True, help='The frame containing the navigation buttons.')
    style.gm_nav_vbox = Style(style.thin_vbox, heavy=True, help='The vbox containing the navigation buttons.')
    style.gm_nav_button = Style(style.menu_button, heavy=True, help='A navigation button.')
    style.gm_nav_button_text = Style(style.menu_button_text, heavy=True, help='A navigation button label.')

    style.file_picker_entry = Style(style.menu_button, heavy=True, help='A button you click to save or load a file.')
    style.file_picker_entry_box = Style(style.thin_hbox, heavy=True, help='The box inside that button.')
    style.file_picker_text = Style(style.default, heavy=True, help='Base style for text inside a file picker entry.')
    style.file_picker_new = Style(style.file_picker_text, heavy=True, help='The number of the newest file.')
    style.file_picker_old = Style(style.file_picker_text, heavy=True, help='The number of non-newest files.')
    style.file_picker_extra_info = Style(style.file_picker_text, heavy=True, help='Extra text (the date and save info) of a file.')
    style.file_picker_empty_slot = Style(style.file_picker_text, heavy=True, help='The style of "Empty Slot" text.')
    style.file_picker_frame = Style(style.default, heavy=True, help='The frame containing the file picker.')
    style.file_picker_frame_vbox = Style(style.thin_vbox, heavy=True, help='The box containing file picker navigation and the file picker grid.')
    style.file_picker_navbox = Style(style.thick_hbox, heavy=True, help='The box containing the file picker navigation buttons.')
    style.file_picker_nav_button = Style(style.menu_button, heavy=True, help='A file picker navigation button.')
    style.file_picker_nav_button_text = Style(style.menu_button_text, heavy=True, help='A file picker navigation button label.')
    style.file_picker_grid = Style(style.default, heavy=True, help='The grid containing the entries in the file picker.')

    style.yesno_frame = Style(style.default, heavy=True, help='The frame containing the yes/no dialog.')
    style.yesno_frame_vbox = Style(style.thick_vbox, heavy=True, help='Separates the label from the buttons in a yes/no dialog.')
    style.yesno_label = Style(style.default, heavy=True, help='The label of a yes/no dialog.')
    style.yesno_button_hbox = Style(style.thick_hbox, heavy=True, help="The box containing the Yes and No buttons.")
    style.yesno_button = Style(style.menu_button, heavy=True, help='A Yes/No button.')
    style.yesno_button_text = Style(style.menu_button_text, heavy=True, help='A Yes/No button label.')
    
    style.error_root = Style(style.default)
    style.error_title = Style(style.default)
    style.error_body = Style(style.default)


    
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

        ui.window(style='gm_root')
        ui.null()

        if not screen:
            return

        if not config.game_menu_positions:
            ui.window(style='gm_nav_frame')
            ui.vbox(focus='gm_nav', style='gm_nav_vbox')

        for i, (key, label, clicked, enabled) in enumerate(config.game_menu):

            disabled = False

            if not eval(enabled):
                disabled = True
                clicked = None

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
    def _render_savefile(index, name, filename, extra_info, screenshot, mtime, newest, clickable, **positions):

        if clickable:
            clicked = ui.returns(("return", (filename, True)))
        else:
            clicked = None

        ui.button(style=style.file_picker_entry[index],
                  clicked=clicked,
                  **positions)

        ui.hbox(style=style.file_picker_entry_box[index])

        if not config.disable_thumbnails:
            ui.add(screenshot)

        if newest:
            ui.text(name + ". ", style=style.file_picker_new[index])
        else:
            ui.text(name + ". ", style=style.file_picker_old[index])


        s = config.file_entry_format % dict(
            time=renpy.time.strftime(config.time_format,
                                     renpy.time.localtime(mtime)),
            save_name=extra_info)

        ui.text(s, style=style.file_picker_extra_info[index])

        ui.close()

    # This renders an empty slot in the file picker.
    def _render_new_slot(index, name, filename, clickable, **positions):

        if clickable:
            clicked=ui.returns(("return", (filename, False)))
            enable_hover = True
        else:
            clicked = None
            enable_hover = True

        ui.button(style=style.file_picker_entry[index],
                  clicked=clicked,
                  enable_hover=enable_hover,
                  **positions)

        ui.hbox(style=style.file_picker_entry_box[index])

        if not config.disable_thumbnails:
            ui.null(width=config.thumbnail_width,
                    height=config.thumbnail_height)


        ui.text(name + ". ", style=style.file_picker_old[index])

        ui.text(_(u"Empty Slot."), style=style.file_picker_empty_slot[index])
        ui.close()

    _scratch.file_picker_page = None

    # The names of the various pages that the file picker knows
    # about.
    def _file_picker_pages():

        rv = [ ]

        if config.has_autosave:
            rv.append("Auto")

        if config.has_quicksave:
            rv.append("Quick")

        for i in range(1, config.file_quick_access_pages + 1):
            rv.append(str(i))

        return rv


    # This function is given a page, and should map it to the names
    # of the files on that page.
    def _file_picker_page_files(page):

        per_page = config.file_page_cols * config.file_page_rows
        rv = [ ]

        if config.has_autosave:
            if page == 0:
                for i in range(1, per_page + 1):
                    rv.append(("auto-" + str(i), "a" + str(i), True))

                return rv
            else:
                page -= 1

        if config.has_quicksave:
            if page == 0:
                for i in range(1, per_page + 1):
                    rv.append(("quick-" + str(i), "q" + str(i), True))

                return rv
            else:
                page -= 1

        for i in range(per_page * page + 1, per_page * page + 1 + per_page):
            rv.append(("%d" % i, "%d" % i, False))

        return rv

    # Given a filename, returns the page that filename is on. 
    def _file_picker_file_page(filename):

        per_page = config.file_page_cols * config.file_page_rows

        base = 0

        if config.has_autosave:
            if filename.startswith("auto-"):
                return base
            else:
                base += 1

        if config.has_quicksave:
            if filename.startswith("quick-"):
                return base
            else:
                base += 1

        return base + int((int(filename) - 1) / per_page)


    # This displays a file picker that can chose a save file from
    # the list of save files.
    def _file_picker(selected, save):

        # The number of slots in a page.
        file_page_length = config.file_page_cols * config.file_page_rows

        saved_games = renpy.list_saved_games(regexp=r'(auto-|quick-)?[0-9]+')

        newest = None
        newest_mtime = None
        save_info = { }

        if config.file_picker_positions:
            positions = config.file_picker_positions
        else:
            positions = { }

        for fn, extra_info, screenshot, mtime in saved_games:
            save_info[fn] = (extra_info, screenshot, mtime)

            if not fn.startswith("auto-") and mtime > newest_mtime:
                newest = fn
                newest_mtime = mtime


        # The index of the first entry in the page.
        fpp = _scratch.file_picker_page

        if fpp is None:

            if newest:
                fpp = _file_picker_file_page(newest)
            else:
                fpp = _file_picker_file_page("1")


        while True:

            if fpp < 0:
                fpp = 0

            _scratch.file_picker_page = fpp

            # Show navigation
            _game_nav(selected)

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
                tb(fpp > 0, _(u'Previous'), ui.returns(("fppdelta", -1)), selected=False)
    
                # Quick Access
                for i, name in enumerate(_file_picker_pages()):
                    tb(True, name, ui.returns(("fppset", i)), fpp == i)

                # Next
                tb(True, _(u'Next'), ui.returns(("fppdelta", +1)), False)

                # Done with nav buttons.
                if not config.file_picker_positions:
                    ui.close()

            # This draws a single slot.
            def entry(name, filename, offset, ro):
                place = positions.get("entry_" + str(offset + 1), { })

                if filename not in save_info:
                    clickable = save and not ro

                    _render_new_slot(offset, name, filename, clickable, **place)
                else:
                    clickable = not save or not ro

                    extra_info, screenshot, mtime = save_info[filename]
                    _render_savefile(offset, name, filename, extra_info, screenshot,
                                     mtime, newest == filename, clickable, **place)

            if not config.file_picker_positions:
                ui.grid(config.file_page_cols,
                        config.file_page_rows,
                        style='file_picker_grid',
                        transpose=True) # slots

            for i, (filename, name, ro) in enumerate(_file_picker_page_files(fpp)):
                entry(name, filename, i, ro)

            if not config.file_picker_positions:                    
                ui.close() # slots
                ui.close() # whole thing

            result = _game_interact()
            type, value = result

            if type == "return":
                return value

            if type == "fppdelta":
                fpp += value

            if type == "fppset":
                fpp = value


    # This renders a yes/no prompt, as part of the game menu. If
    # screen is None, then it omits the game menu navigation. 
    def _yesno_prompt(screen, message):
        """
        @param screen: The screen button that should be highlighted when this prompt is shown. If None, then no game menu navigation is shown.

        @param message: The message that is shown to the user to prompt them to answer yes or no.

        This function returns True if the user clicks Yes, or False if the user clicks No.
        """

        renpy.transition(config.intra_transition)

        _game_nav(screen)

        ui.window(style='yesno_frame')
        ui.vbox(style='yesno_frame_vbox')

        _label_factory(message, "yesno")

        ui.hbox(style='yesno_button_hbox')
        
        # The extra nulls are because we want equal whitespace surrounding
        # the two buttons. It should work as long as we have xfill=True
        _button_factory(u"Yes", 'yesno', clicked=ui.returns(True))
        _button_factory(u"No", 'yesno', clicked=ui.returns(False))

        ui.close()
        ui.close()

        rv =  _game_interact()
        renpy.transition(config.intra_transition)
        return rv


    def _show_exception(title, message):

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
            renpy.full_restart(reason='main_menu')
        else:
            return


# Run at the end of init, to set up autosaving based on the user's
# choices.
init 1160 python:

    if config.has_autosave:
        config.autosave_slots = config.file_page_cols * config.file_page_rows
    else:
        config.autosave_frequency = None
            
            
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
    if not _game_menu_screen:
        return

    $ renpy.play(config.enter_sound)
    
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

init -1160:
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
        $ renpy.transition(config.game_main_transition)
        jump _main_menu

    $ renpy.transition(config.exit_transition)

    return
