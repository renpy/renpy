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
            return self.value

        # TODO: Figure out how this should work @ the main menu.

        
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

    class ShowMenu(Action):
        """
         Causes us to enter the game menu, if we're not there already. If we
         are in the game menu, then this shows the screen, or if no screen
         is defined, jumps to the label.

         `screen` is either a screen or a label. Useful calls include:

         * ShowMenu("load_screen")
         * ShowMenu("save_screen")
         * ShowMenu("preferences_screen")

         This can also be used to show user-defined menu screens. For
         example, if one has a "menu stats" screen defined, one can
         show it as part of the game menu using:

         * ShowMenu("menu stats")
         """

        def __init__(self, screen):
            self.screen = screen

        def __call__(self):
            
            # Ugly. We have different code depending on if we're in the
            # game menu or not.
            if renpy.context()._menu:

                if renpy.has_screen(self.screen):
                    renpy.game.show_screen(self.screen)

                elif renpy.has_label(self.screen):
                    renpy.jump(self.screen)

                else:
                    raise Exception("%r is not a screen or a label." % self.screen)

            else:
                renpy.calls_in_new_context(self.screen)

        def get_selected(self):
            return renpy.showing(self.screen)

            
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
            return not getattr(renpy.context(), "main_menu", True)


    class Quit(Action):
        
        def __init__(self, confirm=True):
            self.confirm = True

        def __call__(self):
            # TODO: Confirm

            renpy.quit()
            
            
        
    ##########################################################################
    # Functions that set variables or fields.

    # class Set(Action):
    #     def __init__(self, var, value):
    #         self.var = var
    #         self.value = value

    #     def __call__(self)
    #         renpy.get_current_screen().scope[self.var] = self.value
    #         renpy.restart_interaction()

    #     def get_selected(self):
    #         return renpy.get_current_screen().scope[self.var] == self.value
        
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

    
    def SetPreference(variable, value):
        """
         Causes the preference variable to be set to the given value. Useful
         invocations include:

         * SetPreference("afm_enable", True) - Enable auto-forward mode.
         * SetPreference("afm_enable", False) - Disable auto-forward mode.
         * SetPreference("fullscreen", True) - Fullscreen mode.
         * SetPreference("fullscreen", False) - Windowed mode.
         * SetPreference("skip_after_choices", True) - Keep skipping after a choice.
         * SetPreference("skip_after_choices", False) - Do not skip after choices.
         * SetPreference("skip_unseen", True) - Skip unseen text.
         * SetPreference("skip_unseen", False) - Do not skip unseen text.
         * SetPreference("transitions", 2) - Show all transitions.
         * SetPreference("transitions", 0) - Do not show transitions.
         """
         
        return SetField(_preferences, variable, value)

    
    # class Toggle(Action):
    #     def __init__(self, var):
    #         self.var = var

    #     def __call__(self)
    #         renpy.get_current_screen().scope[self.var] = not renpy.get_current_screen().scope[self.var]
    #         renpy.restart_interaction()

    #     def get_selected(self):
    #         return renpy.get_current_screen().scope[self.var]
        
    class ToggleField(Action):
        """
         Toggles a field on an object. Toggling means to invert the boolean
         value of that field when the action is performed.
         """
        
        def __init__(self, object, field):
            self.object = object
            self.field = field
        
        def __call__(self):
            setattr(self.object, self.field, not getattr(self.object, self.field))
            renpy.restart_interaction()

        def get_selected(self):
            return getattr(self.object, self.field)

        
    def ToggleVariable(variable):
        """
         Toggles a variable.
         """

        return ToggleField(store, variable)

    
    def TogglePreference(variable):
        """
         Toggles a preference variable. Useful invocations include:

         * TogglePreference("afm_enable") - Toggle auto-forward mode.
         * TogglePreference("fullscreen") - Toggle full-screen mode.
         * TogglePreference("skip_after_choices") - Toggle skipping after choices.
         * TogglePreference("skip_unseen") - Toggle skipping unseen text.
         """

        return ToggleField(_preferences, variable)

    
    def ToggleSkipping():
        """
         Toggles skipping.
         """

        return ToggleField(config, "skipping")


    

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

    # PreferenceValue
    # MixerValue

    class FieldValue(BarValue):
        """
         The value of a field on an object.
         """
        
        def __init__(self, object, field, range):
            self.object = object
            self.field = field
            self.range = range

        def changed(self, value):
            setattr(self.object, self.field, value)
            
        def __call__(self, object):
            return ui.adjustment(
                range=self.range,
                value=getattr(self.object, self.field),
                changed=self.changed)

        def get_style(self):
            return "slider"

        
    def PreferenceValue(variable):
        """
         The value of a preference. There are two variables that can be used:

         * PreferenceValue("text_cps") - Adjust the text speed.
         * PreferenceValue("afm_time") - Adjust the auto-forward speed.
         """

        if variable == "text_cps":
            return FieldValue(_preferences, "text_cps", 200)
        elif variable == "afm_time":
            return FieldValue(_preferences, "afm_time", 40)
        else:
            raise Exception("Unknown variable %r in PreferenceValue." % variable)
        
        
    class MixerValue(BarValue):
        """
         The value of a mixer.
         """
        
        def __init__(self, mixer):
            self.mixer = mixer

        def set_mixer(self, value):
            _preferences.set_mixer(self.mixer, value)
            
        def __call__(self):
            return ui.adjustment(
                range=1.0,
                value=_preferences.get_mixer(self.mixer),
                changed=self.set_mixer)

        def get_style(self):
            return "slider"
        
