# Copyright 2008 PyTom
#
# Please see the LICENSE.txt distributed with Ren'Py for permission to
# copy and modify.

# Common stuff that's used by the various Ren'Py menus. This includes
# the default definitions of config.main_menu and config.game_menu, as
# well as the default definitions of the various preferences (and the objects
# holding those preferences)

init -1150 python:

    config.main_menu = [
        (u"Start Game", "start", "True"),
        (u"Continue Game", _intra_jumps("load_screen", "main_game_transition"), "True"),
        (u"Preferences", _intra_jumps("preferences_screen", "main_game_transition"), "True"),
        (u"Quit", ui.jumps("_quit"), "True")
        ]

    
    config.game_menu = [
        ( None, u"Return", ui.jumps("_return"), 'True'),
        ( "preferences", u"Preferences", _intra_jumps("preferences_screen", "intra_transition"), 'True' ),
        ( "save", u"Save Game", _intra_jumps("save_screen", "intra_transition"), 'not main_menu' ),
        ( "load", u"Load Game", _intra_jumps("load_screen", "intra_transition"), 'True'),
        ( None, u"Main Menu", ui.callsinnewcontext("_main_menu_prompt"), 'not main_menu' ),
        ( None, u"Quit", ui.callsinnewcontext("_quit_prompt"), 'True' ),
        ]

label _quit_prompt:
    if layout.yesno_prompt(None, u"Are you sure you want to quit?"):
        jump _quit
    else:
        return

label _main_menu_prompt:
    if layout.yesno_prompt(None, u"Are you sure you want to return to the main menu?\nThis will lose unsaved progress."):
        $ renpy.full_restart(reason='main_menu')
    else:
        return

    
 
