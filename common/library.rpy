# This file consists of renpy functions that aren't expected to be
# touched by the user too much. We reserve the _ prefix for names
# defined in the library.

init -500:
    python:

        # These are settings that the user can tweak to control the
        # look of the main menu and the load/save/escape screens.

        # The class that stores library variables.
        class _Library(object):
            def __setattr__(self, name, value):

                if getattr(self, 'lock', False):
                    if not name in vars(self):
                        raise Exception('library.%s is not a known configuration variable.' % name)

                if name == "script_version":
                    _set_script_version(value)

                object.__setattr__(self, name, value)
                
                
            

        # Used to store library settings.
        library = _Library()

        # The minimum version of the module we work with. Don't change
        # this unless you know what you're doing.
        library.module_version = 5005000

        # Should we warn the user if the module is missing or has a bad
        # version?
        library.module_warning = False

        # Used to translate strings in the library.
        library.translations = { }

        # Used internally to maintain compatiblity with old
        # translations of strings.
        library.old_names = { }

        # True if the skip indicator should be shown.
        library.skip_indicator = True

        # Used to ensure library compatibility.
        library.script_version = None

        # This is updated to give the user an idea of where a save is
        # taking place.
        save_name = ''

        def _button_factory(label,
                            type=None,
                            selected=None,
                            disabled=False,
                            clicked=None,
                            properties={}):
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
                role = "selected_"
            else:
                role = ""

            if disabled:
                clicked = None

            style = style + "_button"
            text_style = style + "_text"

            ui.textbutton(_(label), style=style, text_style=text_style, clicked=clicked, role=role, **properties)

        def _label_factory(label, type, properties={}):
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

            if s in library.old_names and library.old_names[s] in library.translations:
                return library.translations[library.old_names[s]]

            return s

        # Are the windows currently hidden?
        _windows_hidden = False

    # Set up the default keymap.    
    python hide:

        # Called to make a screenshot happen.
        def screenshot():
            import os.path

            i = 1
            while True:
                fn = "screenshot%04d.png" % i
                if not os.path.exists(fn):
                    break
                i += 1
            
            renpy.screenshot(fn)

        def dump_styles():
            if config.developer:
                renpy.style.write_text("styles.txt")

        def invoke_game_menu():
            renpy.play(library.enter_sound)
            renpy.call_in_new_context('_game_menu')

        def toggle_skipping():

            if not config.skipping:
                config.skipping = "slow"
            else:
                config.skipping = None

            renpy.restart_interaction()

        def fast_skip():
            if config.fast_skipping or config.developer:
                config.skipping = "fast"

        def reload_game():
            if not config.developer:
                return

            renpy.call_in_new_context("_save_reload_game")



        # The default keymap.
        km = renpy.Keymap(
            rollback = renpy.rollback,
            screenshot = screenshot,
            toggle_fullscreen = renpy.toggle_fullscreen,
            toggle_music = renpy.toggle_music,
            toggle_skip = toggle_skipping,
            fast_skip = fast_skip,
            game_menu = invoke_game_menu,
            hide_windows = renpy.curried_call_in_new_context("_hide_windows"),
            launch_editor = renpy.launch_editor,
            dump_styles = dump_styles,
            reload_game = reload_game,
            )

        config.underlay = [ km ]


    # The skip indicator.
    python hide:

        def skip_indicator():

            ### skip_indicator default
            # (text) The style and placement of the skip indicator.            

            if config.skipping == "slow" and library.skip_indicator:
                ui.text(_(u"Skip Mode"), style='skip_indicator')

            if config.skipping == "fast" and library.skip_indicator:
                ui.text(_(u"Fast Skip Mode"), style='skip_indicator')

        config.overlay_functions.append(skip_indicator)

    # The default hyperlink handler.
    python hide:

        def hyperlink_function(target):
            renpy.call_in_new_context(target)
            return

        config.hyperlink_callback = hyperlink_function
        

    # The default with callback.
    python:
        _window_during_transitions = False

        def _default_with_callback(trans, paired=None):
            if (_window_during_transitions and not
                renpy.context_nesting_level() and
                not renpy.count_displayables_in_layer('transient')):

                narrator("", interact=False)

            return trans
        
        config.with_callback = _default_with_callback


label _hide_windows:

    if _windows_hidden:
        return

    python:
        _windows_hidden = True
        ui.saybehavior()
        ui.saybehavior(dismiss='hide_windows')
        ui.interact(suppress_overlay=True)
        _windows_hidden = False

    return

    
# This code here handles check for the correct version of the Ren'Py module.

label _check_module:

    if not library.module_warning:
        return

    python hide:
        module_info = _(u"While Ren'Py games may be playable without the renpy module, some features may be disabled. For more information, read the module/README.txt file or go to http://www.bishoujo.us/renpy/.")

        if renpy.module_version() == 0:
            _show_exception(_(u"renpy module not found."),
                            _(u"The renpy module could not be loaded on your system.") + "\n\n" + module_info)
        elif renpy.module_version() < library.module_version:
            _show_exception(_(u"Old renpy module found."),
                            _(u"An old version (%d) of the Ren'Py module was found on your system, while this game requires version %d.") % (renpy.module_version(), library.module_version) + "\n\n" + module_info)

    return
    

                         
label _save_reload_game:
    python hide:
        renpy.take_screenshot((library.thumbnail_width, library.thumbnail_height))
                
        ui.add(Solid((0, 0, 0, 255)))
        ui.text("Saving game...",
                size=32, xalign=0.5, yalign=0.5, color=(255, 255, 255, 255))

        renpy.pause(0)
        renpy.save("reload", "reload save game")

        persistent._reload_save = "reload"
        
        ui.add(Solid((0, 0, 0, 255)))
        ui.text("Reloading script...",
                size=32, xalign=0.5, yalign=0.5, color=(255, 255, 255, 255))

        renpy.pause(0)
        
        renpy.utter_restart()

label _load_reload_game:

    if not persistent._reload_save:
        return

    python hide:
        save = persistent._reload_save
        persistent._reload_save = 0

        ui.add(Solid((0, 0, 0, 255)))
        ui.text("Reloading game...",
                size=32, xalign=0.5, yalign=0.5, color=(255, 255, 255, 255))

        renpy.pause(0)
        
        renpy.load(save)

    return


init -401:
    # Random nice things to have.
    $ centered = Character(None, what_style="centered_text", window_style="centered_window")
    image text = renpy.ParameterizedText(style="centered_text")

    # Lock the library object.
    $ library.lock = True

    
