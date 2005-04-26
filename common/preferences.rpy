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
                    

    python hide:

        # Enablers for some preferences.
        library.has_music = True
        library.has_sound = True
        library.has_transitions = True


        p1 = _Preference('Display', 'fullscreen', [
            ('Window', False, None),
            ('Fullscreen', True, None),
            ])

        p2 = _Preference('Music', 'music', [
            ('Enabled', True, 'library.has_music'),
            ('Disabled', False, 'library.has_music'),
            ])
            
        p3 = _Preference('Sound Effects', 'sound', [
            ('Enabled', True, 'library.has_sound'),
            ('Disabled', False, 'library.has_sound'),
            ])
            

        library.preferences['prefs_left'] = [ p1, p2, p3 ]

        p4 = _Preference('TAB and CTRL Skip', 'skip_unseen', [
            ('Seen Messages', False, 'config.allow_skipping'),
            ('All Messages', True, 'config.allow_skipping'),
            ])

        p5 = _Preference('Transitions', 'transitions', [
            ('All', 2, 'library.has_transitions'),
            ('Some', 1, 'library.has_transitions and default_transition'),
            ('None', 0, 'library.has_transitions'),
            ])

        p6 = _Preference('Text Display', 'fast_text', [
            ('Fast', True, 'config.annoying_text_cps'),
            ('Slow', False, 'config.annoying_text_cps'),
            ])
            

        library.preferences['prefs_right'] = [ p4, p5, p6 ]

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
    
        

            
                        

                         
                         
