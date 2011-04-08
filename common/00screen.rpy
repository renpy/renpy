# Screen system support.

init -1140 python:

    class Return(Action):
        """
         :doc: control_action
         
         Causes the current interaction to return the supplied value. This is
         often used with menus and imagemaps, to select what the return value
         of the interaction is.

         When in a menu, this returns from the menu.
         """

        def __init__(self, value=None):
            self.value = value

        def __call__(self):

            if self.value is None:
                if renpy.context()._main_menu:
                    ShowMenu("main_menu")()
                else:
                    return True

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

         If not None, `transition` is use to show the new screen.
         """
         
        def __init__(self, screen, transition=None, **kwargs):
            self.screen = screen
            self.kwargs = kwargs
            self.transition = transition

        def predict(self):
            renpy.predict_screen(self.screen, **self.kwargs)
            
        def __call__(self):
            renpy.show_screen(self.screen, **self.kwargs)

            if self.transition is not None:
                renpy.transition(self.transition)

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

         `transition`
             If not None, a transition that occurs when hiding the screen.
         """
         
        def __init__(self, screen, transition=None):
            self.screen = screen
            self.transition = transition
            
        def __call__(self):
            renpy.hide_screen(self.screen)

            if self.transition is not None:
                renpy.transition(self.transition)
            
            renpy.restart_interaction()

                
    class Screenshot(Action):
        """
         :doc: other_action
         
         Takes a screenshot.
         """
        
        def __call__(self):
            _screenshot()

    def HideInterface():
        """
         :doc other_action
        
         Causes the interface to be hidden until the user clicks.
         """

        return ui.callsinnewcontext("_hide_windows")

    
    class With(Action):
        """
         :doc: other_action

         Causes `transition` to occur.
         """

        def __init__(self, transition):
            self.transition = transition 
            
        def __call__(self):
            renpy.transition(self.transition)
            renpy.restart_interaction()

    class Notify(Action):
        """
         :doc: other_action

         Displays `message` using :func:`renpy.notify`. 
         """

        def __init__(self, message):
            self.message = message
        
        def predict(self):
            renpy.predict_screen("notify")
        
        def __call__(self):
            renpy.notify(self.message)
            
            
            
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

        def predict(self):
            self.action.predict()
        
    def If(expression, true=None, false=None):
        """
         :doc: other_action

         This returns `true` if `expression` is true, and `false`
         otherwise. Use this to select an action based on an expression.
         Note that the default, None, can be used as an action that causes
         a button to be disabled.
         """
         
        if expression:
            return true
        else:
            return false
         
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

    def SetScreenVariable(name, value):
        """
        :doc: data_action

        Causes the variable `name` associated with the current screen to 
        be set to `value`.
        """
        
        cs = renpy.current_screen()
        if cs is not None:
            return SetDict(cs.scope, name, value)
        else:
            return None
    
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

    def ToggleScreenVariable(name, true_value=None, false_value=None):
        """
         :doc: data_action

         Toggles the value of the variable `name` in the current screen.

         `true_value`
             If not None, then this is the true value we use.
         `false_value`
             If not None, then this is the false value we use. 
         """
    
        cs = renpy.current_screen()

        if cs is not None:
            return ToggleDict(cs.scope, name, true_value=true_value, false_value=None)
        else:
            return None

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

        def periodic(self, st):
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

            fraction = (st - self.start_time) / self.delay
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
                if value == self.range:
                    value = 0
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
                raise Exception("The displayable with id %r is not declared, or not a viewport." % self.viewport)

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
                raise Exception("The displayable with id %r is not declared, or not a viewport." % self.viewport)

            return w.yadjustment

        def get_style(self):
            return "scrollbar", "vscrollbar"
         
    ##########################################################################
    # File functions

    config.linear_saves_page_size = None
        
    if persistent._file_page is None:
        persistent._file_page = "1"

    def __filename(name, page=None):

        if page is None:
            page = persistent._file_page

        if config.linear_saves_page_size is not None:
            try:
                page = int(page)
                name = int(name)
                return str((page - 1) * config.linear_saves_page_size + name)
            except ValueError:
                pass
            
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

         `page`
             The name of the page that it will be saved to.
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
                    layout.yesno_screen(layout.OVERWRITE_SAVE, FileSave(self.name, False, self.newest, self.page))
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
            if not self.confirm:
                return False
            
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
                    layout.yesno_screen(layout.LOADING, FileLoad(self.name, False, self.page))
                    return

            renpy.load(fn)

        def get_sensitive(self):
            return renpy.scan_saved_game(__filename(self.name, self.page))

        def get_selected(self):
            if not self.confirm:
                return False

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
                layout.yesno_screen(layout.DELETE_SAVE, FileDelete(self.name, False, self.page))
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
            return FileLoad(name, page=page)
        else:
            return FileSave(name, page=page)
         

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
            elif self.page == "quick" and not config.has_quicksave:
                return False
            else:
                return True

        def get_selected(self):
            return self.page == persistent._file_page
                
    def FilePageName(auto="a", quick="q"):
        """
         :doc: file_action_function

         Returns the name of the current file page, as a string. If a normal
         page, this returns the page number. Otherwise, it returns
         `auto` or `quick`.
         """

        page = persistent._file_page

        if page == "quick":
            return quick
        elif page == "auto":
            return auto
        else:
            return page

    def FileSlotName(slot, slots_per_page, auto="a", quick="q", format="%s%d"):
        """
         :doc: file_action_function

         Returns the name of the numbered slot. This assumes that slots on
         normal pages are numbered in a linear order starting with 1, and
         that page numbers start with 1. When slot is 2, and slots_per_page
         is 10, and the other variables are the defauts:

         * When the first page is slowing, this returns "2".
         * When the second page is showing, this returns "12".
         * When the auto page is showing, this returns "a2".
         * When the quicksave page is showing, this returns "q2".

         `slot`
             The number of the slot to access.

         `slots_per_page`
             The number of slots per page.

         `auto`
             A prefix to use for the auto page.

         `quick`
             A prefix to use for the quick page.

         `format`
             The formatting code to use. This is given two arguments: A string
             giving the page prefix, and an integer giving the slot number.
         """

        page = persistent._file_page

        if page == "quick":
            prefix = quick
            page = 0
        elif page == "auto":
            prefix = auto
            page = 0
        else:
            prefix = ""
            page = int(page) - 1

        return format % (prefix, page * slots_per_page + slot)
         
        
    class FilePageNext(Action):
        """
         :doc: file_action

         Goes to the next file page.

         `max`
             If set, this should be an integer that gives the number of
             the maximum file page we can go to.
         """

        def __init__(self, max=None):

            page = persistent._file_page

            if page == "auto":
                if config.has_quicksave:
                    page = "quick"
                else:
                    page = "1"

            elif page == "quick":
                page = "1"

            else:
                page = int(page) + 1

                if max is not None:
                    if page > max:
                        page = None

                if page is not None:
                    page = str(page)

            self.page = page
                
        def __call__(self):
            if not self.get_sensitive():
                return

            persistent._file_page = self.page
            renpy.restart_interaction()

        def get_sensitive(self):
            return self.page is not None
            

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
    # Side Images
    
    def SideImage(tag="side"):
        """
        :doc: side_image_function
    
        Returns the side image associated with the currently speaking character, 
        or a Null displayable if no such side image exists.
        """
        
        name = renpy.get_side_image(tag)
        if name is None:
            return Null()
        else:
            return ImageReference(name)


    ##########################################################################
    # Preferences Constructor

    class __DisplayAction(Action):
        def __init__(self, factor):
            self.width = int(factor * config.screen_width)
            self.height = int(factor * config.screen_height)            

        def __call__(self):
            renpy.set_physical_size((self.width, self.height))
            renpy.restart_interaction()
            
        def get_sensitive(self):
            if self.width == config.screen_width and self.height == config.screen_height:
                return True
                
            return renpy.get_renderer_info()["resizable"]
            
        def get_selected(self):
            if _preferences.fullscreen:
                return False

            return (self.width, self.height) == renpy.get_physical_size()
                    

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
         * Preference("display", "window") - displays in windowed mode at 1x normal size.
         * Preference("display", 2.0) - displays in windowed mode at 2.0x normal size.
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
                return __DisplayAction(1.0)
            elif value == "toggle":
                return ToggleField(_preferences, "fullscreen")
            elif isinstance(value, (int, float)):
                return __DisplayAction(value)

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
    config.quit_action = ui.gamemenus("_confirm_quit")

    #########################################################################    

    class __TooltipAction(object):

        def __init__(self, tooltip, value):
            self.tooltip = tooltip
            self.value = value

        def __call__(self):
            if self.tooltip.value != self.value:
                self.tooltip.value = self.value
                renpy.restart_interaction()            

        def unhovered(self):
            if self.tooltip.value != self.tooltip.default:
                self.tooltip.value = self.tooltip.default
                renpy.restart_interaction()            

    class Tooltip(object):
        """
        :doc: tooltips
        
        A tooltip object can be used to define a portion of a screen that is 
        updated when the mouse hovers an area. 
        
        A tooltip object has a ``value`` field, which is set to the `default`
        value passed to the constructor when the tooltip is created. When 
        a button using an action creadted by the tooltip is hovered, the 
        value field changes to the value associated with the action. 
        """
                   
        def __init__(self, default):
            self.value = default
            self.default = default

        def action(self, value):
            """
            :doc: tooltips method
            
            Returns an action that is generally used as the hovered property
            of a button. When the button is hovered, the value field of this 
            tooltip is set to `value`. When the buttton loses focus, the
            value field of this tooltip reverts to the default.
            """
        
            return __TooltipAction(self, value)
    
# This is used to ensure a fixed click-to-continue indicator is shown on
# its own layer.
screen _ctc:
    add ctc
    
# These are used by renpy.notify.

transform _notify_transform:
    # These control the position.
    xalign .02 yalign .015

    # These control the actions on show and hide.
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0

screen notify:
    zorder 100

    text message at _notify_transform

    # This controls how long it takes between when the screen is
    # first shown, and when it begins hiding.
    timer 3.25 action Hide('notify')

