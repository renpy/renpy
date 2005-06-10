# This file contains the code to implement the Ren'Py preferences
# screen.

init -450:
    python:

        # This is a map from the name of the style that is applied to
        # a list of preferences that should be placed into a vbox
        # with that style.
        library.preferences = { }

        class _Preference(object):
            """
            This is a class that's used to represent a preference that
            may be shown to the user.
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

            def render_preference(self):
                values = [ (name, val) for name, val, cond in self.values
                           if cond is None or renpy.eval(cond) ]

                if not values:
                    return

                ui.window(style='prefs_pref')
                ui.vbox()

                _label_factory(self.name, "prefs")

                cur = getattr(self.base, self.field)

                for name, value in values:

                    def clicked(value=value):
                        setattr(self.base, self.field, value)
                        return True

                    _button_factory(name, "prefs",
                                    selected=cur==value,
                                    clicked=clicked)
                    
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

            def render_preference(self):
                
                if not renpy.eval(self.cond):
                    return

                ui.window(style='prefs_pref')
                ui.vbox()

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
        library.has_transitions = True
        library.has_cps = True
        library.has_afm = True


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
            ('Seen Messages', False, 'config.allow_skipping'),
            ('All Messages', True, 'config.allow_skipping'),
            ])


        def cps_render(n):
            if n == 0:
                return "Infinite"
            else:
                return str(n)
            
        pc2 = _PreferenceSpinner('Text Speed (CPS)', 'text_cps',
                                0, 500, 10, 'library.has_cps',
                                render=cps_render)

        def afm_render(n):
            if n == 0:
                return "Disabled"
            else:
                return str(n)

        pc3 = _PreferenceSpinner('Auto Forward Time', 'afm_time',
                                0, 60, 1, 'library.has_afm',
                                render=afm_render)

        # Right

        pr1 = _Preference('Music', 'music', [
            ('Enabled', True, 'library.has_music'),
            ('Disabled', False, 'library.has_music'),
            ])
            
        pr2 = _Preference('Sound Effects', 'sound', [
            ('Enabled', True, 'library.has_sound'),
            ('Disabled', False, 'library.has_sound'),
            ])
            
        library.preferences['prefs_left'] = [ pl1, pl2 ]
        library.preferences['prefs_center'] = [ pc1, pc2, pc3 ]
        library.preferences['prefs_right'] = [ pr1, pr2 ]



label _prefs_screen:

    python hide:

        _game_nav("prefs")

        ui.window(style='prefs_window')
        ui.fixed()


        for style, prefs in library.preferences.iteritems():

            ui.vbox(library.padding * 3, style=style)
            for i in prefs:
                i.render_preference()
            ui.close()

        ui.close()

        _game_interact()

    jump _prefs_screen
    
        

            
                        

                         
                         
