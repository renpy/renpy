# This file contains the code to implement the Ren'Py preferences
# screen.

init -450:
    python:

        # Used to collect the various preferences the system knows
        # about.
        library.left_preferences = [ ]
        library.right_preferences = [ ]

        class _Preference(object):
            """
            This is a class that's used to represent a preference that
            may be shown to the user.
            """

            def __init__(self, name, field, values):
                """
                @param name: The name of this preference. It will be
                displayed to the user.

                @param variable: The field on the _preferences object
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
                """

                self.name = name
                self.field = field
                self.values = values

            def render_preference(self):
                values = [ (name, val) for name, val, cond in self.values
                           if cond is None or renpy.eval(cond) ]

                if not values:
                    return

                ui.vbox(style='prefs_pref')
                ui.text(_(self.name), style='prefs_label')

                cur = getattr(_preferences, self.field)

                for name, value in values:

                    style = 'prefs_button'
                    text_style = 'prefs_button_text'

                    if cur == value:
                        style = 'prefs_selected_button'
                        text_style = 'prefs_selected_button_text'

                    def clicked(value=value):
                        setattr(_preferences, self.field, value)
                        return True

                    ui.textbutton(_(name),
                                  style=style,
                                  text_style=text_style,
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
            

        library.left_preferences = [ p1, p2, p3 ]

        p4 = _Preference('CTRL Skips', 'skip_unseen', [
            ('Seen Messages', False, None),
            ('All Messages', True, None),
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
            

        library.right_preferences = [ p4, p5, p6 ]

label _prefs_screen:

    python hide:

        _game_nav("prefs")

        ui.vbox(library.padding * 3, style='prefs_left')
        for i in library.left_preferences:
            i.render_preference()
        ui.close()
                    
        ui.vbox(library.padding * 3, style='prefs_right')
        for i in library.right_preferences:
            i.render_preference()
        ui.close()

        _game_interact()

    jump _prefs_screen
    
        

            
                        

                         
                         
