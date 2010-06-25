# Screen system support.

init -1140 python:

    def __yesno_prompt(message, yes=None, no=None):
        if renpy.has_screen("yesno_prompt"):

            yes_action = [ Hide("yesno_prompt") ]
            no_action = [ Hide("yesno_prompt") ]

            if yes is not None:
                yes_action.append(yes)
            if no is not None:
                no_action.append(no)
            
            renpy.display.show_screen(
                "yesno_prompt", 
                message=message,
                yes_action=yes_action,
                no_action=no_action)
        
        if renpy.invoke_in_new_context(layout.yesno_prompt, None, message):
            if yes is not None:
                yes()
        else:
            if no is not None:
                no()
                
    class Return(Action):
        """
         :doc: control_action
         
         Causes the current interaction to return the supplied value. This is
         often used with menus and imagemaps, to select what the return value
         of the interaction is.

         When in a menu, this returns from the menu.
         """

        def __init__(self, value=True):
            self.value = value

        def __call__(self):

            if renpy.context()._main_menu:
                ShowMenu("main_menu")()
            else:
                return self.value

    
    class Jump(Action):
        """
         :doc: control_action
         
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
         :doc: control_action
         
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
        """
         :doc: control_action

         Shows a transient screen. A transient screen will be hidden when
         the current interaction completes.
         """

        return Show(screen, _transient=True, **kwargs)
        
        
    class Hide(Action):
        """
         :doc: control_action
         
         This causes the screen named `screen` to be hidden, if it is shown. 
         """
         
        def __init__(self, screen):
            self.screen = screen

        def __call__(self):
            renpy.hide_screen(self.screen)
            renpy.restart_interaction()

                
    class Screenshot(Action):
        """
         :doc: other_action
         
         Takes a screenshot.
         """
        
        def __call__(self):
            _screenshot()


    class InvertSelected(Action):
        """
         :doc: other_action
         
         This inverts the selection state of the provided action, while
         proxying over all of the other methods.
         """

        def __init__(self, action):
            self.action = action

        def __call__(self):
            return self.action.__call__()

        def get_selected(self):
            return not self.action.get_selected()
        
        def get_sensitive(self):
            return self.action.get_sensitive()

        def periodic(self, st):
            return self.action.periodic(st)
        
        
         
    ##########################################################################
    # Menu-related actions.

    config.show_menu_enable = { "save" : "not renpy.context()._main_menu" }

            
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
                    renpy.scene(layer='screens')
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
                __yesno_prompt(layout.MAIN_MENU, MainMenu(False))
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
            self.confirm = True

        def __call__(self):

            if self.confirm:
                __yesno_prompt(layout.QUIT, Quit(False))
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
        
    def AutoForward(Action):
        return Preference("auto-forward")
    
        
    ##########################################################################
    # Functions that set variables or fields.

    class SetField(Action):
        """
         :doc: data_action

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
         :doc: data_action

         Causes `variable` to be set to `value`.
         """

        return SetField(store, variable, value)

    
    class SetDict(Action):
        """
         :doc: data_action

         Causes the value of `key` in `dict` to be set to `value`.
         """

        def __init__(self, dict, key, value):
            self.dict = dict
            self.key = key
            self.value = value

        def __call__(self):
            self.dict[self.key] = self.value
            renpy.restart_interaction()

        def get_selected(self):
            return self.dict[self.key] == self.value

    
    class ToggleField(Action):
        """
         :doc: data_action

         Toggles `field` on `object`. Toggling means to invert the boolean
         value of that field when the action is performed.

         `true_value`
             If not None, then this is the true value we use.
         `false_value`
             If not None, then this is the false value we use. 
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


    def ToggleVariable(variable, true_value=None, false_value=None):
        """
         :doc: data_action

         Toggles `variable`.

         `true_value`
             If not None, then this is the true value we use.
         `false_value`
             If not None, then this is the false value we use. 
         """

        return ToggleField(store, variable, true_value=true_value, false_value=false_value)

    
    class ToggleDict(Action):
        """
         :doc: data_action

         Toggles the value of `key` in `dict`. Toggling means to invert the
         value when the action is performed.

         `true_value`
             If not None, then this is the true value we use.
         `false_value`
             If not None, then this is the false value we use. 
         """
        
        def __init__(self, dict, key, true_value=None, false_value=None):
            self.dict = dict
            self.key = key
            self.true_value = true_value
            self.false_value = false_value
        
        def __call__(self):
            value = self.dict[self.key]

            if self.true_value is not None:
                value = (value == self.true_value)

            value = not value

            if self.true_value is not None:
                if value:
                    value = self.true_value
                else:
                    value = self.false_value

            self.dict[self.key] = value
            renpy.restart_interaction()

        def get_selected(self):
            rv = self.dict[self.key]

            if self.true_value is not None:
                rv = (rv == self.true_value)

            return rv


    ##########################################################################
    # Audio actions.

    class Play(Action):
        """
         :doc: audio_action
         
         Causes an audio file to be played on a given channel.
         
         `channel`
             The channel to play the sound on.
         `file`
             The file to play.

         Any keyword arguments are passed to :func:`renpy.music.play`
         """
             
        def __init__(self, channel, file, **kwargs):
            self.channel = channel
            self.file = file
            self.kwargs = kwargs
            self.selected = self.get_selected()

        def __call__(self):
            renpy.music.play(self.file, channel=self.channel, **self.kwargs)
            renpy.restart_interaction()
            
        def get_selected(self):
            return renpy.music.get_playing(self.channel) == self.file            

        def periodic(self):
            if self.selected != self.get_selected():
                renpy.restart_interaction()

            return .1

        
    class Queue(Action):
        """
         :doc: audio_action

         Causes an audio file to be queued on a given channel.

         `channel`
             The channel to play the sound on.
         `file`
             The file to play.

         Any keyword arguments are passed to :func:`renpy.music.queue`
         """

        def __init__(self, channel, file, **kwargs):
            self.channel = channel
            self.file = file
            self.kwargs = kwargs

        def __call__(self):
            renpy.music.queue(self.file, channel=self.channel, **self.kwargs)
            renpy.restart_interaction()

            
    class Stop(Action):
        """
         :doc: audio_action

         Causes an audio channel to be stopped.

         `channel`
             The channel to play the sound on.
         `file`
             The file to play.

         Any keyword arguments are passed to :func:`renpy.music.play`
         """

        def __init__(self, channel, **kwargs):
            self.channel = channel
            self.kwargs = kwargs

        def __call__(self):
            renpy.music.stop(channel=self.channel, **self.kwargs)
            renpy.restart_interaction()

        
    
    ##########################################################################
    # BarValues

    class StaticValue(BarValue):
        """
         :doc: value

         This allows a value to be specified statically.

         `value`
              The value itself, a number.

         `range`
              The range of the value.
         """

        def __init__(self, value=0.0, range=1.0):
            self.value = value
            self.range = range

        def get_adjustment(self):
            return ui.adjustment(value=self.value, range=self.range, adjustable=False)

    class AnimatedValue(BarValue):
        """
         :doc: value

         This animates a value, taking `delay` seconds to vary the value from
         `old_value` to `value`.

         `value`
             The value itself, a number.

         `range`
             The range of the value, a number.

         `delay`
             The time it takes to animate the value, in seconds. Defaults
             to 1.0.
         
         `old_value`
             The old value. If this is None, then the value is taken from the
             AnimatedValue we replaced, if any. Otherwise, it is initialized
             to `value`.
         """

        def __init__(self, value=0.0, range=1.0, delay=1.0, old_value=None):
            if old_value == None:
                old_value = value

            self.value = value
            self.range = range
            self.delay = delay
            self.old_value = old_value
            self.start_time = None

            self.adjustment = None
            
        def get_adjustment(self):
            self.adjustment = ui.adjustment(value=self.value, range=self.range, adjustable=False)
            return self.adjustment
            
        def periodic(self, st):

            if self.start_time is None:
                self.start_time = st
            
            if self.value == self.old_value:
                return

            fraction = st - (self.start_time) / self.delay
            fraction = min(1.0, fraction)

            value = self.old_value + fraction * (self.value - self.old_value)

            self.adjustment.change(value)

            if fraction != 1.0:
                return 0

        def replaces(self, other):

            if not isinstance(other, AnimatedValue):
                return

            if self.value == other.value:
                self.start_time = other.start_time
                self.old_value = other.old_value
            else:
                self.old_value = other.value
                self.start_time = None

    class FieldValue(BarValue):
        """
         :doc: value
         
         A value that allows the user to adjust the value of a field
         on an object.

         `object`
             The object.
         `field`
             The field, a string.
         `range`
             The range to adjust over.
         `max_is_zero`
             If True, then when the field is zero, the value of the
             bar will be range, and all other values will be shifted
             down by 1. This works both ways - when the bar is set to
             the maximum, the field is set to 0.

             This is used internally, for some preferences.
         `style`
             The styles of the bar created.
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
            
        def get_adjustment(self):

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
            return self.style, "v" + self.style

        
    class MixerValue(BarValue):
        """
         :doc: value

         The value of an audio mixer.

         `mixer`
             The name of the mixer to adjust. This is usually one of
             "music", "sfx", or "voice", but user code can create new
             mixers.
         """
        
        def __init__(self, mixer):
            self.mixer = mixer

        def set_mixer(self, value):
            _preferences.set_volume(self.mixer, value)
            
        def get_adjustment(self):
            return ui.adjustment(
                range=1.0,
                value=_preferences.get_volume(self.mixer),
                changed=self.set_mixer)

        def get_style(self):
            return "slider", "vslider"

    class XScrollValue(BarValue):
        """
         :doc: value

         The value of an adjustment that horizontally scrolls the the viewport with the
         given id, on the current screen. The viewport must be defined
         before a bar with this value is.
         """

        def __init__(self, viewport):
            self.viewport = viewport

        def get_adjustment(self):
            w = renpy.get_widget(None, self.viewport)
            if not isinstance(w, Viewport):
                raise Exception("The displayable with id %r is not declared, or not a viewport.")

            return w.xadjustment

        def get_style(self):
            return "scrollbar", "vscrollbar"

    class YScrollValue(BarValue):
        """
         :doc: value

         The value of an adjustment that vertically scrolls the the viewport with the
         given id, on the current screen. The viewport must be defined
         before a bar with this value is.
         """

        def __init__(self, viewport):
            self.viewport = viewport

        def get_adjustment(self):
            w = renpy.get_widget(None, self.viewport)
            if not isinstance(w, Viewport):
                raise Exception("The displayable with id %r is not declared, or not a viewport.")

            return w.yadjustment

        def get_style(self):
            return "scrollbar", "vscrollbar"
         
    ##########################################################################
    # File functions

    if persistent._file_page is None:
        persistent._file_page = "1"

    def __filename(name, page=None):

        if page is None:
            page = persistent._file_page
            

        return str(page) + "-" + str(name)

    def FileLoadable(name, page=None):
        """
         :doc: file_action_function

         This is a function that returns true
         if the file is loadable, and false otherwise.
         """

        if renpy.scan_saved_game(__filename(name, page)):
            return True
        else:
            return False
    
    def FileScreenshot(name, empty=None, page=None):
        """
         :doc: file_action_function
                  
         Returns the screenshot associated with the given file. If the
         file is not loadable, then `empty` is returned, unless it's None,
         in which case, a Null displayable is created.

         The return value is a displayable.
         """

        save_data = renpy.scan_saved_game(__filename(name, page))

        if save_data is None:
            if empty is not None:
                return empty
            else:
                return Null(config.thumbnail_width, config.thumbnail_height)

        extra_info, displayable, save_time = save_data

        return displayable

            
    def FileTime(name, format="%b %d, %H:%M", empty="", page=None):
        """
         :doc: file_action_function 
         
         Returns the time the file was saved, formatted according
         to the supplied `format`. If the file is not found, `empty` is
         returned.

         The return value is a string.
         """
        
        save_data = renpy.scan_saved_game(__filename(name, page))

        if save_data is None:
            return empty

        import time

        extra_info, displayable, save_time = save_data
        
        return time.strftime(format, time.localtime(save_time))

    def FileSaveName(name, empty="", page=None):
        """
         :doc: file_action_function
         
         Return the save_name that was in effect when the file was saved,
         or `empty` if the file does not exist.
         """

        save_data = renpy.scan_saved_game(__filename(name, page))

        if save_data is None:
            return empty

        extra_info, displayable, save_time = save_data
        
        return extra_info


    class FileSave(Action):
        """
         :doc: file_action

         Saves the file.

         The button with this slot is selected if it's marked as the
         newest save file.
         
         `confirm`
             If true, then we will prompt before overwriting a file.

         `newest`
             If true, then this file will be marked as the newest save
             file when it's saved. (Set this to false for a quicksave,
             for example.)
         """

        def __init__(self, name, confirm=True, newest=True, page=None):
            self.name = name
            self.confirm = confirm
            self.page = page
            self.newest = newest
            
        def __call__(self):

            if not self.get_sensitive():
                return
            
            fn = __filename(self.name, self.page)

            if renpy.scan_saved_game(fn):
                if self.confirm:
                    __yesno_prompt(layout.OVERWRITE_SAVE, FileSave(self.name, False, self.newest, self.page))
                    return
                
            renpy.save(fn, extra_info=save_name)

            if self.newest:
                persistent._file_newest = fn
                
            renpy.restart_interaction()

        def get_sensitive(self):
            if renpy.context()._main_menu:
                return False
            elif persistent._file_page == "auto":
                return False
            else:
                return True

        def get_selected(self):
            return persistent._file_newest == __filename(self.name, self.page)
            
    class FileLoad(Action):
        """
         :doc: file_action

         Loads the file.

         `confirm`
             If true, prompt if loading the file will end the game.
         """
        
        def __init__(self, name, confirm=True, page=None):
            self.name = name
            self.confirm = confirm
            self.page = page
            
        def __call__(self):

            if not self.get_sensitive():
                return
            
            fn = __filename(self.name, self.page)
            
            if not renpy.context()._main_menu:
                if self.confirm:
                    __yesno_prompt(layout.LOADING, FileLoad(self.name, False, self.page))
                    return

            renpy.load(fn)

        def get_sensitive(self):
            return renpy.scan_saved_game(__filename(self.name, self.page))

        def get_selected(self):
            return persistent._file_newest == __filename(self.name, self.page)

    class FileDelete(Action):
        """
         :doc: file_action

         Deletes the file.

         `confirm`
             If true, prompts before deleting a file.
         """
        
        def __init__(self, name, confirm=True, page=None):
            self.name = name
            self.confirm = confirm
            self.page = page
            
        def __call__(self):

            if not self.get_sensitive():
                return
            
            fn = __filename(self.name, self.page)
            
            if self.confirm:
                __yesno_prompt(layout.DELETE_SAVE, FileDelete(self.name, False, self.page))
                return

            renpy.unlink_save(fn)

        def get_sensitive(self):
            return renpy.scan_saved_game(__filename(self.name, self.page))

        def get_selected(self):
            return persistent._file_newest == __filename(self.name, self.page)

        
    def FileAction(name, page=None):
        """
         :doc: file_action

         "Does the right thing" with the file. This means loading it if the
         load screen is showing, and saving to it otherwise.
         """
        
        if renpy.current_screen().screen_name[0] == "load":
            return FileLoad(name, page)
        else:
            return FileSave(name, page)
         

    class FilePage(Action):
        """
         :doc: file_action

         Sets the file page to `page`, which should be one of "auto", "quick",
         or an integer.
         """
        
        def __init__(self, page):
            self.page = str(page)

        def __call__(self):
            if not self.get_sensitive():
                return

            persistent._file_page = self.page
            renpy.restart_interaction()

        def get_sensitive(self):
            if self.page == "auto" and not config.has_autosave:
                return False
            elif self.page == "quicksave" and not config.has_quicksave:
                return False
            else:
                return True

        def get_selected(self):
            return self.page == persistent._file_page
                
            
    class FilePageNext(Action):
        """
         :doc: file_action

         Goes to the next file page. (It's always possible to get to the
         next file page.)
         """

        def __init__(self):

            page = persistent._file_page

            if page == "auto":
                if config.has_quicksave:
                    page = "quick"
                else:
                    page = "1"

            elif page == "quick":
                page = "1"

            else:
                page = str(int(page) + 1)

            self.page = page
                
        def __call__(self):
            if not self.get_sensitive():
                return

            persistent._file_page = self.page
            renpy.restart_interaction()


    class FilePagePrevious(Action):
        """
         :doc: file_action

         Goes to the previous file page, if possible.
         """

        def __init__(self):

            page = persistent._file_page
        
            if page == "auto":
                page = None

            elif page == "quick":
                if config.has_autosave:
                    page = "auto"
                else:
                    page = None

            elif page == "1":
                if config.has_quicksave:
                    page = "quick"
                elif config.has_autosave:
                    page = "auto"
                else:
                    page = None

            else:
                page = str(int(page) - 1)

            self.page = page
                
        def __call__(self):
            if not self.get_sensitive():
                return

            persistent._file_page = self.page
            renpy.restart_interaction()

        def get_sensitive(self):
            return self.page

    class FileTakeScreenshot(Action):
        """
         :doc: file_action

         Take a screenshot to be used when the game is saved. This can
         be used to ensure that the screenshot is accurate, by taking
         a pictue of the screen before a file save screen is shown.
         """

        def __call__(self):
            renpy.take_screenshot()
        
            
    ##########################################################################
    # Preferences Constructor

    def Preference(name, value=None):
        """
         :doc: preference_action
         
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

         * Preference("music mute", "enable") - Mute the music mixer.
         * Preference("music mute", "disable") - Un-mute the music mixer.
         * Preference("music mute", "toggle") - Toggle music mute.

         * Preference("sound mute", "enable") - Mute the sound mixer.
         * Preference("sound mute", "disable") - Un-mute the sound mixer.
         * Preference("sound mute", "toggle") - Toggle sound mute.

         * Preference("voice mute", "enable") - Mute the voice mixer.
         * Preference("voice mute", "disable") - Un-mute the voice mixer.
         * Preference("voice mute", "toggle") - Toggle voice  mute.
         
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

        elif name == "music mute":

            if value == "enable":
                return SetDict(_preferences.mute, "music", True)
            elif value == "disable":
                return SetDict(_preferences.mute, "music", False)
            elif value == "toggle":
                return ToggleDict(_preferences.mute, "music")

        elif name == "sound mute":

            if value == "enable":
                return SetDict(_preferences.mute, "sfx", True)
            elif value == "disable":
                return SetDict(_preferences.mute, "sfx", False)
            elif value == "toggle":
                return ToggleDict(_preferences.mute, "sfx")

        elif name == "voice mute":

            if value == "enable":
                return SetDict(_preferences.mute, "voice", True)
            elif value == "disable":
                return SetDict(_preferences.mute, "voice", False)
            elif value == "toggle":
                return ToggleDict(_preferences.mute, "voice")

        else:
            raise Exception("Preference(%r, %r) is unknown." % (name , value))


    # What we do on a quit, by default.
    config.quit_action = ShowMenu("_confirm_quit")

    
# This is used to ensure a fixed click-to-continue indicator is shown on
# its own layer.
screen _ctc:
    add ctc
    
