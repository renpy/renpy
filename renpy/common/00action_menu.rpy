# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init -1500 python:

                
    ##########################################################################
    # Menu-related actions.

    config.show_menu_enable = { "save" : "(not renpy.context()._main_menu) and (not _in_replay)" }

    class ShowMenu(Action):
        """
         :doc: menu_action

         Causes us to enter the game menu, if we're not there already. If we
         are in the game menu, then this shows a screen or jumps to a label.

         `screen` is usually the name of a screen, which is shown using
         the screen mechanism. If the screen doesn't exist, then "_screen"
         is appended to it, and that label is jumped to.

         * ShowMenu("load")
         * ShowMenu("save")
         * ShowMenu("preferences")

         This can also be used to show user-defined menu screens. For
         example, if one has a "stats" screen defined, one can
         show it as part of the game menu using:

         * ShowMenu("stats")

         ShowMenu without an argument will enter the game menu at the
         default screen, taken from _game_menu_screen.
         
         """

        def __init__(self, screen=None):
            self.screen = screen

        def predict(self):
            if renpy.has_screen(self.screen):
                renpy.predict_screen(self.screen)

        def __call__(self):

            if not self.get_sensitive():
                return
            
            orig_screen = screen = self.screen or store._game_menu_screen

            if not (renpy.has_screen(screen) or renpy.has_label(screen)):
                screen = screen + "_screen"
                
            # Ugly. We have different code depending on if we're in the
            # game menu or not.
            if renpy.context()._menu:

                if renpy.has_screen(screen):

                    renpy.transition(config.intra_transition)
                    renpy.show_screen(screen, _transient=True)
                    renpy.restart_interaction()
                    
                elif renpy.has_label(screen):
                    renpy.transition(config.intra_transition)

                    ui.layer("screens")
                    ui.remove_above(None)
                    ui.close()

                    renpy.jump(screen)

                else:
                    raise Exception("%r is not a screen or a label." % orig_screen)

            else:
                renpy.call_in_new_context("_game_menu", _game_menu_screen=screen)

        def get_selected(self):
            return renpy.get_screen(self.screen)

        def get_sensitive(self):
            if self.screen in config.show_menu_enable:
                return eval(config.show_menu_enable[self.screen])
            else:
                return True
        
            
    class Start(Action):
        """
         :doc: menu_action
         
         Causes Ren'Py to jump out of the menu context to the named
         label. The main use of this is to start a new game from the
         main menu. Common uses are:

         * Start() - Start at the start label.
         * Start("foo") - Start at the "foo" label.
         """
        
        def __init__(self, label="start"):
            self.label = label

        def __call__(self):
            renpy.jump_out_of_context(self.label)

            
    class MainMenu(Action):
        """
         :doc: menu_action

         Causes Ren'Py to return to the main menu.

         `confirm`
              If true, causes Ren'Py to ask the user if he wishes to
              return to the main menu, rather than returning
              directly.
         """

        def __init__(self, confirm=True):
            self.confirm = confirm
        
        def __call__(self):

            if not self.get_sensitive():
                return

            if self.confirm:
                layout.yesno_screen(layout.MAIN_MENU, MainMenu(False))
            else:
                renpy.full_restart()

        def get_sensitive(self):
            return not renpy.context()._main_menu


    class Quit(Action):
        """
         :doc: menu_action

         Quits the game.

         `confirm`
              If true, prompts the user if he wants to quit, rather
              than quitting directly.
         """
        
        def __init__(self, confirm=True):
            self.confirm = confirm

        def __call__(self):

            if self.confirm:
                renpy.loadsave.force_autosave()
                layout.yesno_screen(layout.QUIT, Quit(False))
            else:            
                renpy.quit()

            
    class Skip(Action):
        """
         :doc: other_action

         Causes the game to begin skipping. If the game is in a menu
         context, then this returns to the game. Otherwise, it just
         enables skipping.
         """
                
        def __call__(self):
            if not self.get_sensitive():
                return

            if renpy.context()._menu:
                renpy.jump("_return_skipping")
            else:
                config.skipping = not config.skipping
                renpy.restart_interaction()

        def get_selected(self):
            return config.skipping
                
        def get_sensitive(self):
            return config.allow_skipping and (not renpy.context()._main_menu)


    class Help(Action):
        """
         :doc: other_action

         Displays help.

         `help`
              If this is a string giving a label in the programe, then
              that label is called in a new context when the button is
              chosen. Otherwise, it should be a string giving a file
              that is opened in a web browser. If None, the value of
              config.help is used in the same wayt.
         """

        def __init__(self, help=None):
            self.help = help
        
        def __call__(self):
            _help(self.help)
                   
