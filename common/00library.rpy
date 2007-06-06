# Copyright 2004-2007 PyTom
#
# Please see the LICENSE.txt distributed with Ren'Py for permission to
# copy and modify.

# This file consists of renpy functions that aren't expected to be
# touched by the user too much. We reserve the _ prefix for names
# defined in the library.

init -1180:
    python:
        
        # These are settings that the user can tweak to control the
        # look of the main menu and the load/save/escape screens.

        # The minimum version of the module we work with. Don't change
        # this unless you know what you're doing.
        config.module_version = 6002001

        # Should we warn the user if the module is missing or has a bad
        # version?
        config.module_warning = False

        # Used to translate strings in the config.
        config.translations = { }

        # Used internally to maintain compatiblity with old
        # translations of strings.
        config.old_names = { }

        # True if the skip indicator should be shown.
        config.skip_indicator = True

        # Used to ensure library compatibility.
        config.script_version = None

        # A dict of 5-tuples mapping button labels to image buttons.
        config.image_buttons = { }

        # A dict mapping label to image.
        config.image_labels = { }

        # Maps from button or label to additional properties.
        config.button_properties = { }
        config.button_text_properties = { }
        config.label_properties = { }

        # Defaults for preferences.
        config.default_fullscreen = None
        config.default_text_cps = None        
        
        # This is updated to give the user an idea of where a save is
        # taking place.
        save_name = ''

        style.skip_indicator = Style(style.default, heavy=True, help='The skip indicator.')

        # This is used to jump to a label with a transition.
        def _intra_jumps_core(label, transition):
            if config.intra_transition:
                renpy.transition(getattr(config, transition))

            renpy.jump(label)

        _intra_jumps = renpy.curry(_intra_jumps_core)
        
        def _button_factory(label,
                            type=None,
                            selected=None,
                            disabled=False,
                            clicked=None,
                            properties={},
                            index=None,
                            **props):
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

            props.update(properties)
            props.update(config.button_properties.get(label, { }))
            
            if disabled:
                clicked = None

            if label in config.image_buttons:
                (idle, hover, sel_idle, sel_hover, disabled) = config.image_buttons[label]

                if not clicked:
                    ui.image(disabled, **properties)
                elif selected:
                    ui.imagebutton(sel_idle, sel_hover, clicked=clicked, **props)
                else:
                    ui.imagebutton(idle, hover, clicked=clicked, **props)

                return

            if selected and not disabled:
                role = "selected_"
            else:
                role = ""

            button_style = type + "_button"
            text_style = type + "_button_text"

            if index is None:
                index = label
            
            button_style = getattr(style, button_style)[index]
            text_style = getattr(style, text_style)[index]
            
            ui.button(style=button_style, clicked=clicked, role=role, **props)
            ui.text(_(label), style=text_style, **config.button_text_properties.get(label, { }))
            
        def _label_factory(label, type, properties={}, **props):
            """
            This function is called to create a new label. It can be
            overridden by the user to change how these labels are created.

            @param label: The label of the box.

            @param type: "prefs" or "yesno". (perhaps more by now.)

            @param properties: This may contain position properties.
            """

            props.update(properties)
            props.update(config.label_properties.get(label, { }))

            if label in config.image_labels:
                ui.image(config.image_labels[label], **props)
                return

            style = getattr(store.style, type + "_label")[label]
            
            ui.text(_(label), style=style, **props)

        # The function that's used to translate strings in the game menu.
        def _(s):
            """
            Translates s into another language or something.
            """
            
            if s in config.translations:
                return config.translations[s]

            if s in config.old_names and config.old_names[s] in config.translations:
                return config.translations[config.old_names[s]]

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

        def launch_editor():
            if not config.developer:
                return
            
            filename, line = renpy.get_filename_line()
            renpy.launch_editor([ filename ], line)


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
            launch_editor = launch_editor,
            dump_styles = dump_styles,
            reload_game = reload_game,
            )

        config.underlay = [ km ]


    # The skip indicator.
    python hide:

        def skip_indicator():

            ### skip_indicator default
            # (text) The style and placement of the skip indicator.            

            if config.skipping == "slow" and config.skip_indicator:
                ui.text(_(u"Skip Mode"), style='skip_indicator')

            if config.skipping == "fast" and config.skip_indicator:
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
        ui.saybehavior(dismiss=['dismiss', 'hide_windows'])
        ui.interact(suppress_overlay=True)
        _windows_hidden = False

    return

    
# This code here handles check for the correct version of the Ren'Py module.

label _check_module:

    if not config.module_warning:
        return

    python hide:
        module_info = _(u"While Ren'Py games may be playable without the renpy module, some features may be disabled. For more information, read the module/README.txt file or go to http://www.bishoujo.us/renpy/.")

        if renpy.module_version() == 0:
            _show_exception(_(u"renpy module not found."),
                            _(u"The renpy module could not be loaded on your system.") + "\n\n" + module_info)
        elif renpy.module_version() < config.module_version:
            _show_exception(_(u"Old renpy module found."),
                            _(u"An old version (%d) of the Ren'Py module was found on your system, while this game requires version %d.") % (renpy.module_version(), config.module_version) + "\n\n" + module_info)

    return
    

                         
label _save_reload_game:
    python hide:
        renpy.take_screenshot((config.thumbnail_width, config.thumbnail_height))
                
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

init -1001:
    # Random nice things to have.
    $ centered = Character(None, what_style="centered_text", window_style="centered_window")
    image text = renpy.ParameterizedText(style="centered_text")

    # Lock the library object.
    $ config.locked = True


# Implement config.default_fullscreen and config.default_text_cps.
init 1180 python:

    if not persistent._set_preferences:
        persistent._set_preferences = True
        
        if config.default_fullscreen is not None:
            _preferences.fullscreen = config.default_fullscreen

        if config.default_text_cps is not None:
            _preferences.text_cps = config.default_text_cps

# Implement the inspector:
init 1180 python:

    if config.developer:

        def _inspector(l):

            ui.add("#000")
            ui.window(xmargin=20, ymargin=20, style='default')
            ui.vbox()

            ui.text("Style Inspector")
            ui.text("")


            if not l:
                ui.text("Nothing to inspect.")
            
            for depth, width, height, d in l:

                s = d.style

                while s:
                    if s.name:
                        break
                    
                    if s.parent:
                        s = style.get(s.parent)
                    else:
                        break
                        
                name = s.name[0] + "".join([ "[%r]" % i for i in s.name[1:] ]) 

                ui.text("  " * depth + u" \u2022 " + d.__class__.__name__ + " : " + name + " (%dx%d)" % (width, height))

            ui.text("")
            ui.text("(click to continue)")
                
            ui.close()
            ui.saybehavior()
            ui.interact(suppress_overlay=True, suppress_underlay=True)
            
            return

        config.inspector = _inspector
        

    
# Implement the extend character-like object.
init -1180 python:

    config.extend_interjection = "{fast}"
    
    def extend(what, interact=True):
        who = _last_say_who

        if who is not None:
            who = eval(who)
        
        if isinstance(who, NVLCharacter):
            nvl_erase()

        what = _last_say_what + config.extend_interjection + what
            
        renpy.exports.say(who, what, interact=interact)
        store._last_say_what = what
        
    extend.record_say = False
