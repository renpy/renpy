# Screen system support.

init -1140 python:
    
    class Return(Action):
        """
         Causes the current interaction to return the supplied value. This is
         often used with menus and imagemaps, to select what the return value
         of the interaction is.
         """

        def __init__(self, value=True):
            self.value = value

        def __call__(self):

            if main_menu:
                ShowMenu("main_menu")()
            else:
                return self.value

    
    class Jump(Action):
        """
         Causes control to transfer to the given label. This can be used in
         conjunction with renpy.run_screen to define an imagemap that jumps
         to a label when run.
         """
        
        def __init__(self, label):
            self.label = label

        def __call__(self):
            renpy.jump(self.label)

            
    class Show(Action):
        """
         This causes another screen to be shown. `screen` is a string
         giving the name of the screen. The keyword arguments are
         passed to the screen being shown.
         """
         
        def __init__(self, screen, **kwargs):
            self.screen = screen
            self.kwargs = kwargs

        def __call__(self):
            renpy.show_screen(self.screen, **self.kwargs)
            renpy.restart_interaction()
            
        def get_selected(self):
            return renpy.showing(self.screen)


    def ShowTransient(screen, **kwargs):
        return Show(screen, _transient=True, **kwargs)
        
        
    class Hide(Action):
        """
         This causes the screen named `screen` to be hidden, if it is shown. 
         """
         
        def __init__(self, screen):
            self.screen = screen

        def __call__(self):
            renpy.hide_screen(self.screen)
            renpy.restart_interaction()

            
    ##########################################################################
    # Menu-related actions.

    config.show_menu_enable = { "save" : "not main_menu" }

            
    class ShowMenu(Action):
        """
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

        def __call__(self):

            orig_screen = screen = self.screen or store._game_menu_screen

            if not (renpy.has_screen(screen) or renpy.has_label(screen)):
                screen = screen + "_screen"
            
            # Ugly. We have different code depending on if we're in the
            # game menu or not.
            if renpy.context()._menu:

                if renpy.has_screen(screen):
                    renpy.show_screen(screen)
                    renpy.restart_interaction()
                    
                elif renpy.has_label(screen):
                    renpy.jump(screen)

                else:
                    raise Exception("%r is not a screen or a label." % orig_screen)

            else:
                renpy.calls_in_new_context("_game_menu", _game_menu_screen=screen)

        def get_selected(self):
            return renpy.showing(self.screen)

        def get_sensitive(self):
            if self.screen in config.show_menu_enable:
                return eval(config.show_menu_enable[self.screen])
            else:
                return True
        
            
    class Start(Action):
        """
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
         Causes Ren'Py to return to the main menu.
         """

        def __init__(self, confirm=True):
            self.confirm = confirm
        
        def __call__(self):
            # TODO: confirm

            renpy.full_restart()

        def get_sensitive(self):
            return not main_menu
        


    class Quit(Action):
        
        def __init__(self, confirm=True):
            self.confirm = True

        def __call__(self):
            # TODO: Confirm

            renpy.quit()

    class Skip(Action):

        def __call__(self):
            if renpy.context()._menu:
                renpy.jump("_return_skipping")
            else:
                config.skipping = not config.skipping
                renpy.restart_interaction()

        def get_selected(self):
            return config.skipping
                
        def get_sensitive(self):
            return config.allow_skipping and (not main_menu)
        
    def AutoForward(Action):
        return Preference("auto-forward")
    
        
    ##########################################################################
    # Functions that set variables or fields.

    class SetField(Action):
        """
         Causes the a field on an object to be set to a given value.
         `object` is the object, `field` is a string giving the name of the
         field to set, and `value` is the value to set it to.
         """

        def __init__(self, object, field, value):
            self.object = object
            self.field = field
            self.value = value
        
        def __call__(self):
            setattr(self.object, self.field, self.value)
            renpy.restart_interaction()

        def get_selected(self):
            return getattr(self.object, self.field) == self.value

        
    def SetVariable(variable, value):
        """
         Causes the variable to be set to the given value.
         """

        return SetField(store, variable, value)

    
    class ToggleField(Action):
        """
         Toggles a field on an object. Toggling means to invert the boolean
         value of that field when the action is performed.
         """
        
        def __init__(self, object, field, true_value=None, false_value=None):
            self.object = object
            self.field = field
            self.true_value = true_value
            self.false_value = false_value
        
        def __call__(self):
            value = getattr(self.object, self.field)

            if self.true_value is not None:
                value = (value == self.true_value)

            value = not value

            if self.true_value is not None:
                if value:
                    value = self.true_value
                else:
                    value = self.false_value
                    
            setattr(self.object, self.field, value)
            renpy.restart_interaction()

        def get_selected(self):
            rv = getattr(self.object, self.field)

            if self.true_value is not None:
                rv = (rv == self.true_value)

            return rv

        
    def ToggleVariable(variable):
        """
         Toggles a variable.
         """

        return ToggleField(store, variable)

    

    ##########################################################################
    # BarValues

    class StaticValue(BarValue):
        """
         A statically-supplied value.
         """

        def __init__(self, value=0.0, range=1.0):
            self.value = value
            self.range = range

        def __call__(self):
            return ui.adjustment(value=self.value, range=self.range, adjustable=False)

    # Need some sort of animated value?

    class FieldValue(BarValue):
        """
         The value of a field on an object.
         """
        
        def __init__(self, object, field, range, max_is_zero=False, style="bar"):
            self.object = object
            self.field = field
            self.range = range
            self.max_is_zero = max_is_zero
            self.style = style
            
        def changed(self, value):

            if self.max_is_zero:
                if value == 0:
                    value = self.range
                else:
                    value = value + 1
            
            setattr(self.object, self.field, value)
            
        def __call__(self):

            value = getattr(self.object, self.field)
            
            if self.max_is_zero:
                if value == 0:
                    value = self.range
                else:
                    value = value - 1
                        
            return ui.adjustment(
                range=self.range,
                value=value,
                changed=self.changed)

        def get_style(self):
            return self.style

        
    class MixerValue(BarValue):
        """
         The value of a mixer.
         """
        
        def __init__(self, mixer):
            self.mixer = mixer

        def set_mixer(self, value):
            _preferences.set_volume(self.mixer, value)
            
        def __call__(self):
            return ui.adjustment(
                range=1.0,
                value=_preferences.get_volume(self.mixer),
                changed=self.set_mixer)

        def get_style(self):
            return "slider"
        
    ##########################################################################
    # BarValues

    def Preference(name, value=None):
        """
         This constructs the approprate action or value from a preference.
         The preference name should be the name given in the standard
         menus, while the value should be either the name of a choice,
         "toggle" to cycle through choices, a specific value, or left off
         in the case of buttons.

         Actions that can be used with buttons and hotspots are:

         * Preference("display", "fullscreen") - displays in fullscreen mode.
         * Preference("display", "window") - displays in windowed mode.
         * Preference("display", "toggle") - toggle display mode.

         * Preference("transitions", "all") - show all transitions.
         * Preference("transitions", "none") - do not show transitions.
         * Preference("transitions", "toggle") - toggle transitions.

         * Preference("text speed", 0) - make test appear instantaneously.
         * Preference("text speed", 142) - set text speed to 142 characters per second.

         * Preference("joystick") - Show the joystick preferences.

         * Preference("skip", "seen") - Only skip seen messages.
         * Preference("skip", "all") - Skip unseen messages.
         * Preference("skip", "toggle") - Toggle skipping.

         * Preference("begin skipping") - Starts skipping.

         * Preference("after choices", "skip") - Skip after choices.
         * Preference("after choices", "stop") - Stop skipping after choices.
         * Preference("after choices", "toggle") - Toggle skipping after choices.

         * Preference("auto-forward time", 0) - Set the auto-forward time to infinite.
         * Preference("auto-forward time", 10) - Set the auto-forward time (unit is seconds per 250 characters).

         * Preference("auto-forward", "enable") - Enable auto-forward mode.
         * Preference("auto-forward", "disable") - Disable auto-forward mode.
         * Preference("auto-forward", "toggle") - Toggle auto-forward mode.
         
         Values that can be used with bars are:

         * Preference("text speed")
         * Preference("auto-forward time")
         * Preference("music volume")
         * Preference("sound volume")
         * Preference("voice volume")                  
         """

        name = name.lower()

        if isinstance(value, basestring):
            value = value.lower()

        if name == "display":
            if value == "fullscreen":
                return SetField(_preferences, "fullscreen", True)
            elif value == "window":
                return SetField(_preferences, "fullscreen", False)
            elif value == "toggle":
                return ToggleField(_preferences, "fullscreen")

        elif name == "transitions":

            if value == "all":
                return SetField(_preferences, "transitions", 2)
            elif value == "some":
                return SetField(_preferences, "transitions", 1)
            elif value == "none":
                return SetField(_preferences, "transitions", 0)
            elif value == "toggle":
                return ToggleField(_preferences, "transitions", true_value=2, false_value=0)

        elif name == "text speed":
            
            if value is None:
                return FieldValue(_preferences, "text_cps", range=200, max_is_zero=True, style="slider")
            elif isinstance(value, int):
                return SetField(_preferences, "text_cps", value)

        elif name == "joystick" or name == "joystick...":

            return ShowMenu("joystick_preferences")

        elif name == "skip":
            
            if value == "all messages" or value == "all":
                return SetField(_preferences, "skip_unseen", True)
            elif value == "seen messages" or value == "seen":
                return SetField(_preferences, "skip_unseen", False)
            elif value == "toggle":
                return ToggleField(_preferences, "skip_unseen")

        elif name == "skip":
            
            if value == "all messages" or value == "all":
                return SetField(_preferences, "skip_unseen", True)
            elif value == "seen messages" or value == "seen":
                return SetField(_preferences, "skip_unseen", False)
            elif value == "toggle":
                return ToggleField(_preferences, "skip_unseen")

        elif name == "begin skipping":

            return Skip()

        elif name == "after choices":
            
            if value == "keep skipping" or value == "keep" or value == "skip":
                return SetField(_preferences, "skip_after_choices", True)
            elif value == "stop skipping" or value == "stop":
                return SetField(_preferences, "skip_after_choices", False)
            elif value == "toggle":
                return ToggleField(_preferences, "skip_after_choices")
            
        elif name == "auto-forward time":

            if value is None:
                return FieldValue(_preferences, "afm_time", range=40, max_is_zero=True, style="slider")
            elif isinstance(value, int):
                return SetField(_preferences, "afm_time", value)

        elif name == "auto-forward":

            if value == "enable":
                return SetField(_preferences, "afm_enable", True)
            elif value == "disable":
                return SetField(_preferences, "afm_enable", False)
            elif value == "toggle":
                return ToggleField(_preferences, "afm_enable")
            
        elif name == "music volume":

            if value is None:
                return MixerValue('music')

        elif name == "sound volume":

            if value is None:
                return MixerValue('sfx')

        elif name == "voice volume":

            if value is None:
                return MixerValue('voice')

            
                                  
        
