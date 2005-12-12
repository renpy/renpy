# This file contains the code to implement the Ren'Py preferences
# screen.

init -450:
    python:

        # This is a map from the name of the style that is applied to
        # a list of preferences that should be placed into a vbox
        # with that style.
        library.preferences = { }

        # This is a map from preference name to that preference
        # object, that can be used in rearranging preferences.
        library.all_preferences = { }

        # If true, the preference choices will be arranged in an
        # hbox.
        library.hbox_pref_choices = False


        def _prefs_screen_run(prefs_map):

            _game_nav("prefs")

            ### prefs_window default
            # (window) A window containing all preferences.

            ui.window(style='prefs_window')
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

                library.all_preferences[name] = self

            def render_preference(self):
                values = [ (name, val) for name, val, cond in self.values
                           if cond is None or renpy.eval(cond) ]

                if not values:
                    return

                ### prefs_pref default
                # (window) A window containing an individual
                # preference.

                ### prefs_pref_vbox thin_vbox
                # (box) The style of the vbox containing a preference.

                ### prefs_label default
                # (text) The style that is applied to the label of
                # a block of preferences.


                ui.window(style='prefs_pref')
                ui.vbox(style='prefs_pref_vbox')

                _label_factory(self.name, "prefs")

                cur = getattr(self.base, self.field)

                ### prefs_hbox default
                # If library.hbox_pref_choices is True, the style
                # of the hbox containing the choices.

                if library.hbox_pref_choices:
                    ui.hbox(style='prefs_hbox')

                for name, value in values:

                    ### prefs_button button
                    # (window, hover) The style of an unselected preferences
                    # button.

                    ### prefs_button_text button_text
                    # (text, hover) The style of the text of an unselected
                    # preferences button.

                    ### prefs_selected_button selected_button
                    # (window, hover) The style of a selected preferences
                    # button.

                    ### prefs_selected_button_text selected_button_text
                    # (text, hover) The style of the text of a selected
                    # preferences button.

                    def clicked(value=value):
                        setattr(self.base, self.field, value)
                        return True
                    
                    _button_factory(name, "prefs",
                                    selected=cur==value,
                                    clicked=clicked)
                
                if library.hbox_pref_choices:
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
                
                library.all_preferences[name] = self

            def render_preference(self):

                if not eval(self.enable):
                    return

                sound = eval(self.sound)

                ui.window(style='prefs_pref')
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

                    _button_factory("Test", "prefs", clicked=clicked)
                    
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

                library.all_preferences[name] = self

            def render_preference(self):

                if not eval(self.enable):
                    return
                
                ui.window(style='prefs_pref')
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

                library.all_preferences[name] = self

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

                ui.window(style='prefs_pref')
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
                
            
                    

    python hide:

        # Enablers for some preferences.
        library.has_music = True
        library.has_sound = True
        library.sample_sound = None
        library.has_transitions = True
        library.has_cps = True
        library.has_afm = True
        library.has_skipping = True
        library.has_skip_after_choice = True
    

        # Left

        pl1 = _Preference('Display', 'fullscreen', [
            ('Window', False, None),
            ('Fullscreen', True, None),
            ])

        pl2 = _Preference('Transitions', 'transitions', [
            ('All', 2, 'library.has_transitions'),
            ('Some', 1, 'library.has_transitions and default_transition'),
            ('None', 0, 'library.has_transitions'),
            ])


        # Center

        pc1 = _Preference('TAB and CTRL Skip', 'skip_unseen', [
            ('Seen Messages', False, 'config.allow_skipping and library.has_skipping'),
            ('All Messages', True, 'config.allow_skipping and library.has_skipping'),
            ])

        
        pc2= _Preference('After Choices', 'skip_after_choices', [
            ('Stop Skipping', False, 'config.allow_skipping and library.has_skip_after_choice'),
            ('Continue Skipping', True, 'config.allow_skipping and library.has_skip_after_choice'),
            ])

        def cps_render(n):
            if n == 0:
                return "Infinite"
            else:
                return str(n)

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

            
        pc3 = _SliderPreference('Text Speed', 100, cps_get, cps_set,
                                'library.has_cps')


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

        pc4 = _SliderPreference('Auto-Forward Time', 40, afm_get, afm_set,
                                'library.has_afm')

        # Right

        pr1 = _VolumePreference("Music Volume", 'music', 'library.has_music')
        pr2 = _VolumePreference("Sound Volume", 'sfx', 'library.has_sound', 'library.sample_sound')
                                                        

#         pr1 = _Preference('Music', 'music', [
#             ('Enabled', True, 'library.has_music'),
#             ('Disabled', False, 'library.has_music'),
#             ])
            
#         pr2 = _Preference('Sound Effects', 'sound', [
#             ('Enabled', True, 'library.has_sound'),
#             ('Disabled', False, 'library.has_sound'),
#             ])

        ### prefs_column default
        # The style of a vbox containing a column of preferences.

        ### prefs_left prefs_column
        # The position of the left column of preferences.
        
        ### prefs_center prefs_column
        # The position of the center column of preferences.

        ### prefs_right prefs_column
        # The position of the right column of preferences.
            
        library.preferences['prefs_left'] = [
            library.all_preferences['Display'],
            library.all_preferences['Transitions'],
            ]
        
        library.preferences['prefs_center'] = [
            library.all_preferences['TAB and CTRL Skip'],
            library.all_preferences['After Choices'],
            library.all_preferences['Text Speed'],
            library.all_preferences['Auto-Forward Time'],
            ]
        
        library.preferences['prefs_right'] = [
            library.all_preferences['Music Volume'],
            library.all_preferences['Sound Volume'],
            ]


label _prefs_screen:

    $ _prefs_screen_run(library.preferences)

    jump _prefs_screen
    
    
        

            
                        

                         
                         
