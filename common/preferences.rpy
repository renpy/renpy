# Copyright 2004-2006 PyTom
#
# Please see the LICENSE.txt distributed with Ren'Py for permission to
# copy and modify.

# This file contains the code to implement the Ren'Py preferences
# screen.

init -450:
    python:

        # This is a map from the name of the style that is applied to
        # a list of preferences that should be placed into a vbox
        # with that style.
        config.preferences = { }

        # Ditto, for joystick preferences.
        config.joystick_preferences = { }

        # This is a map from preference name to that preference
        # object, that can be used in rearranging preferences.
        config.all_preferences = { }

        # If true, the preference choices will be arranged in an
        # hbox.
        config.hbox_pref_choices = False

        # A list of (readable name, synthetic key) tuples
        # corresponding to joystick events.
        config.joystick_keys = [
            (u'Left', 'joy_left'),
            (u'Right', 'joy_right'),
            (u'Up', 'joy_up'),
            (u'Down', 'joy_down'),
            (u'Select/Dismiss', 'joy_dismiss'),
            (u'Rollback', 'joy_rollback'),
            (u'Hold to Skip', 'joy_holdskip'),
            (u'Toggle Skip', 'joy_toggleskip'),
            (u'Hide Text', 'joy_hide'),
            (u'Menu', 'joy_menu'),
            ]

        # If True, then we can always get into the joystick
        # preferences.
        config.always_has_joystick = False
        
        def _prefs_screen_run(prefs_map):

            _game_nav("prefs")

            ### prefs_frame default
            # (window) A window containing all preferences.

            ui.window(style='prefs_frame')
            ui.fixed()

            for style, prefs in prefs_map.iteritems():

                ui.vbox(style=style)
                for i in prefs:
                    i.render_preference()
                ui.close()

            ui.close()

            _game_interact()


        class _Preference(object):
            """
            This is a class that's used to represent a multiple-choice
            preference.
            """

            def __init__(self, name, field, values, base=_preferences):
                """
                @param name: The name of this preference. It will be
                displayed to the user.

                @param variable: The field on the base object
                that will be assigned the selected value. This field
                must exist.

                @param values: A list of value name, value, condition
                triples. The value name is the name of this value that
                will be shown to the user. The value is the literal
                python value that will be assigned if this value is
                selected. The condition is a condition that will be
                evaluated to determine if this is a legal value. If no
                conditions are true, this preference will not be
                displayed to the user. A condition of None is always
                considered to be True.

                @param base: The base object on which the variable is
                   read from and set. This defaults to _preferences,
                   the user preferences object.
                """

                self.name = name
                self.field = field
                self.values = values
                self.base = base

                config.all_preferences[name] = self

            def render_preference(self):
                values = [ (name, val) for name, val, cond in self.values
                           if cond is None or renpy.eval(cond) ]

                if not values:
                    return

                ### prefs_pref_frame default
                # (window) A window containing an individual
                # preference.

                ### prefs_pref_vbox thin_vbox
                # (box) The style of the vbox containing a preference.

                ### prefs_label default
                # (text) The style that is applied to the label of
                # a block of preferences.


                ui.window(style='prefs_pref_frame')
                ui.vbox(style='prefs_pref_vbox')

                _label_factory(self.name, "prefs")

                cur = getattr(self.base, self.field)

                ### prefs_hbox default
                # If config.hbox_pref_choices is True, the style
                # of the hbox containing the choices.

                if config.hbox_pref_choices:
                    ui.hbox(style='prefs_hbox')

                for name, value in values:

                    ### prefs_button menu_button
                    # (window, hover) The style of an unselected preferences
                    # button.

                    ### prefs_button_text menu_button_text
                    # (text, hover) The style of the text of an unselected
                    # preferences button.

                    def clicked(value=value):
                        setattr(self.base, self.field, value)
                        return True
                    
                    _button_factory(name, "prefs",
                                    selected=cur==value,
                                    clicked=clicked)
                
                if config.hbox_pref_choices:
                    ui.close()
                    
                ui.close()


        class _VolumePreference(object):
            """
            This represents a preference that controls one of the
            volumes in the system. It is represented as a slider bar,
            and a button that can be pushed to play a sample sound on
            a channel.
            """

            def __init__(self, name, mixer, enable='True', sound='None', channel=0):
                """
                @param name: The name of this preference, as shown to the user.

                @param mixer: The mixer this preference controls.

                @param enable: A string giving a python expression. If
                the expression is evaluates to false, this preference
                is not shown.
                
                @param sound: A string that is evaluated to yield
                another string. The yielded string is expected to give
                a sound file, which is played as the sample sound. (We
                apologize for the convolution of this.)

                @param channel: The number of the channel the sample
                sound is played on.                
                """

                self.name = name
                self.mixer = mixer
                self.enable = enable
                self.sound = sound
                self.channel = channel
                
                config.all_preferences[name] = self

            def render_preference(self):

                if not eval(self.enable):
                    return

                sound = eval(self.sound)

                ui.window(style='prefs_pref_frame')
                ui.vbox(style='prefs_pref_vbox')

                _label_factory(self.name, "prefs")

                def changed(v):

                    if v == 0:
                        _preferences.mute[self.mixer] = True
                    else:
                        _preferences.mute[self.mixer] = False

                    v /= 128.0

                    _preferences.volumes[self.mixer] = v

                ### prefs_volume_slider prefs_slider
                # (bar) The style that is applied to volume
                # sliders.
                
                ui.bar(128,
                       int(_preferences.volumes[self.mixer] * 128),
                       changed=changed,
                       style='prefs_volume_slider')

                if sound:
                    def clicked():
                        renpy.sound.play(sound, channel=self.channel)

                    ### soundtest_button prefs_button
                    # (window, hover) The style of a sound test button.

                    ### soundtest_button_text prefs_button_text
                    # (text, hover) The style of the text of a sound
                    # test  button.

                    _button_factory(u"Test", "soundtest", clicked=clicked)
                    
                ui.close()

        class _SliderPreference(object):
            """
            A class that represents a preference that is controlled by a
            slider.
            """

            def __init__(self, name, range, get, set, enable='True'):
                """
                @param set: The name of this preference, that is shown to the user.

                @param range: An integer giving the maximum value of
                this slider. The slider goes from 0 to range.

                @param get: A function that's called to get the
                initial value of the slider. It's called with no
                arguments, and should return an integet between 0 and
                range, inclusive.

                @param set: A function that's called when the value of
                the slider is set by the user. It is called with a
                single integer, in the range 0 to range, inclusive.

                @param enable: A string giving a python expression. If
                the expression is evaluates to false, this preference
                is not shown.
                """

                self.name = name
                self.range = range
                self.get = get
                self.set = set
                self.enable = enable

                config.all_preferences[name] = self

            def render_preference(self):

                if not eval(self.enable):
                    return
                
                ui.window(style='prefs_pref_frame')
                ui.vbox(style='prefs_pref_vbox')

                _label_factory(self.name, "prefs")

                def changed(v):
                    self.set(v)

                ### prefs_slider bar
                # (bar) The style that is applied to preference
                # sliders.
    
                ui.bar(self.range,
                       self.get(),
                       changed=changed,
                       style='prefs_slider')
                    
                ui.close()
                           

        class _PreferenceSpinner(object):
            """
            This is a class that's used to represent a preference
            spinner, which is a preference that can be incremented
            and decremented, when shown to the user.
            """

            def __init__(self, name, field, minimum, maximum, delta,
                         cond = "True", render = lambda x : str(x),
                         base=_preferences):
                """
                @param name: The name of this preference, that is presented
                to the user.

                @param field: The name of the field on the base object
                that is updated by this spinner.

                @param minimum: The minimum value that this spinner can set
                the value to.

                @param maximum: The maximum value that this spinner can set
                the value to.

                @param delta: The delta by which this spinner is
                incremented or decremented.

                @param cond: If this condition is not true, this spinner is
                not shown.

                @param render: This function is called with the value of
                the field, and is expected to render that value to a
                string.

                @param base: The base object that this spinner updates
                the field on. It defaults to _preferences, the preferences
                object.
                """

                self.name = name
                self.field = field
                self.minimum = minimum
                self.maximum = maximum
                self.delta = delta
                self.cond = cond
                self.render = render
                self.base = base

                config.all_preferences[name] = self

            def render_preference(self):

                ### prefs_spinner default
                # The position of the prefs spinner.

                ### prefs_spinner_label prefs_label
                # (text) This is the style that displays the value of a
                # preference spinner.

                ### prefs_spinner_button prefs_button
                # (window, hover) The style of the + or - buttons in a
                # preference spinner.

                ### prefs_spinner_button_text prefs_button_text
                # (text, hover) The style of the text of the + and - buttons
                # in a preference spinner.
                
                if not renpy.eval(self.cond):
                    return

                ui.window(style='prefs_pref_frame')
                ui.vbox(style='prefs_pref_vbox')

                _label_factory(self.name, "prefs")

                cur = getattr(self.base, self.field)


                def minus_clicked():
                    value = cur - self.delta
                    value = max(self.minimum, value)
                    setattr(self.base, self.field, value)
                    return True

                def plus_clicked():
                    value = cur + self.delta
                    value = min(self.maximum, value)
                    setattr(self.base, self.field, value)
                    return True
                    
                ui.hbox(style='prefs_spinner')
                _button_factory("-", "prefs_spinner", clicked=minus_clicked)
                _label_factory(self.render(cur), "prefs_spinner")
                _button_factory("+", "prefs_spinner", clicked=plus_clicked)
                ui.close()
                    
                ui.close()
                
            
        class _JoystickPreference(object):

            def __init__(self, name):
                self.name = name
                config.all_preferences[name] = self

            def render_preference(self):

                ### prefs_js_frame prefs_pref_frame
                # (window) The window containing a joystick mapping preference.

                ### prefs_js_vbox prefs_pref_vbox
                # (box) A vbox containing a joystick mapping preference.
                
                ### prefs_js_button prefs_button
                # (window, hover) The style of buttons giving a joystick mapping.

                ### prefs_js_button_text prefs_button_text
                # (text, hover) The style of the text in buttons giving a joystick mapping.

                ### js_frame prefs_frame
                # (window) The window containing the joystick message.

                ### js_frame_vbox thick_vbox
                # (window) The vbox containing the joistick mapping message.
                
                ### js_function_label prefs_label
                # (text, position) The style of the joystick mapping function name.

                ### js_prompt_label prefs_label
                # (text, position) The style of the joystick mapping prompt message.
                

                def set_binding(key, label):
                    _game_nav(None)

                    ui.window(style='js_frame')
                    ui.vbox(style='js_frame_vbox')
                    _label_factory(_(u"Joystick Mapping") + " - " + _(label), "js_function")
                    _label_factory(u'Move the joystick or press a joystick button to create the mapping. Click the mouse to remove the mapping.', 'js_prompt')
                    ui.close()

                    ui.saybehavior()
                    ui.add(renpy.display.joystick.JoyBehavior())
                    binding = _game_interact()

                    if not isinstance(binding, basestring):
                        if key in _preferences.joymap:
                            del _preferences.joymap[key]
                    else:
                        _preferences.joymap[key] = binding

                
                ui.window(style='prefs_js_frame')
                ui.vbox(style='prefs_js_vbox')

                _label_factory(self.name, 'prefs')

                for label, key in config.joystick_keys:

                    def clicked(label=label, key=key):
                        renpy.invoke_in_new_context(set_binding, key, label)
                        return True

                    _button_factory(_(label) + " - " + _(_preferences.joymap.get(key, u"Not Assigned")), "prefs_js", clicked=clicked)

#                 def clicked():
#                     for label, key in config.joystick_keys:
#                         renpy.invoke_in_new_context(set_binding, key, label)

#                     return True

#                 _button_factory("Assign All Mappings", "prefs_js", clicked=clicked)

                ui.close()

        class _JumpPreference(object):

            def __init__(self, name, target, condition="True"):
                self.name = name
                self.target = target
                self.condition = condition

                config.all_preferences[name] = self

            def render_preference(self):

                ### prefs_jump prefs_pref_frame
                # (window) The style of a window containing a jump preference.

                ### prefs_jump_button prefs_button
                # (window, hover) The style of a jump preference button.

                ### prefs_jump_button_text prefs_button_text
                # (text, hover) The style of jump preference button text.

                ui.window(style='prefs_jump')

                if eval(self.condition):
                    clicked=ui.jumps(self.target)
                else:
                    clicked=None

                _button_factory(self.name, 'prefs_jump', clicked=clicked)

        def _remove_preference(name):
            """
            Removes the preference with the given name from the
            preferences menu.
            """

            pref = config.all_preferences.get(name, None)
            if not pref:
                return

            for k, v in config.preferences.iteritems():
                if pref in v:
                    v.remove(pref)
            

    python hide:

        # Enablers for some preferences.
        config.has_music = True
        config.has_sound = True
        config.sample_sound = None
        config.has_transitions = True
        config.has_cps = True
        config.has_afm = True
        config.has_skipping = True
        config.has_skip_after_choice = True
    

        # Left

        pl1 = _Preference(u'Display', 'fullscreen', [
            (u'Window', False, None),
            (u'Fullscreen', True, None),
            ])

        pl2 = _Preference(u'Transitions', 'transitions', [
            (u'All', 2, 'config.has_transitions'),
            (u'Some', 1, 'config.has_transitions and default_transition'),
            (u'None', 0, 'config.has_transitions'),
            ])


        # Center

        pc1 = _Preference(u'Skip', 'skip_unseen', [
            (u'Seen Messages', False, 'config.allow_skipping and config.has_skipping'),
            (u'All Messages', True, 'config.allow_skipping and config.has_skipping'),
            ])

        config.old_names['Skip'] = 'TAB and CTRL Skip'
        config.all_preferences['TAB and CTRL Skip'] = pc1

        
        pc2= _Preference(u'After Choices', 'skip_after_choices', [
            (u'Stop Skipping', False, 'config.allow_skipping and config.has_skip_after_choice'),
            (u'Keep Skipping', True, 'config.allow_skipping and config.has_skip_after_choice'),
            ])

        config.old_names['Keep Skipping'] = 'Continue Skipping' 

        def cps_get():
            cps = _preferences.text_cps
            if cps == 0:
                cps = 100
            else:
                cps -= 1
            return cps

        def cps_set(cps):
            cps += 1
            if cps == 101:
                cps = 0
            _preferences.text_cps = cps

            
        pc3 = _SliderPreference(u'Text Speed', 100, cps_get, cps_set,
                                'config.has_cps')


        def afm_get():
            afm = _preferences.afm_time
            if afm == 0:
                afm = 40
            else:
                afm -= 1
            return afm

        def afm_set(afm):
            afm += 1
            if afm == 41:
                afm = 0
            _preferences.afm_time = afm

        pc4 = _SliderPreference(u'Auto-Forward Time', 40, afm_get, afm_set,
                                'config.has_afm')

        # Right

        pr1 = _VolumePreference(u"Music Volume", 'music', 'config.has_music')
        pr2 = _VolumePreference(u"Sound Volume", 'sfx', 'config.has_sound', 'config.sample_sound')
                                                        
        _JumpPreference(u'Joystick...', '_joystick_screen', 'renpy.display.joystick.enabled or config.always_has_joystick')

        _JoystickPreference(u'Joystick Configuration')
        
        # Advanced 

        ### prefs_column default
        # The style of a vbox containing a column of preferences.

        ### prefs_left prefs_column
        # The position of the left column of preferences.
        
        ### prefs_center prefs_column
        # The position of the center column of preferences.

        ### prefs_right prefs_column
        # The position of the right column of preferences.

        ### prefs_joystick prefs_center
        # The position of the column of joystick preferences.
            
        config.preferences['prefs_left'] = [
            config.all_preferences[u'Display'],
            config.all_preferences[u'Transitions'],
            config.all_preferences[u'Joystick...'],
            ]
        
        config.preferences['prefs_center'] = [
            config.all_preferences[u'Skip'],
            config.all_preferences[u'After Choices'],
            config.all_preferences[u'Text Speed'],
            config.all_preferences[u'Auto-Forward Time'],
            ]
        
        config.preferences['prefs_right'] = [
            config.all_preferences[u'Music Volume'],
            config.all_preferences[u'Sound Volume'],
            ]

        config.joystick_preferences['prefs_joystick'] = [
            config.all_preferences[u'Joystick Configuration'],
            ]


label _prefs_screen:

    $ _prefs_screen_run(config.preferences)

    jump _prefs_screen
    
label _joystick_screen:    
        
    $ _prefs_screen_run(config.joystick_preferences)

    jump _joystick_screen

            
                        

                         
                         
