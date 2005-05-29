# This function implements a commentary track, which is a special kind of
# say statement that only displays if commentary is set to on in the
# new preference that this mode creates. Making this unlockable is easy,
# but is left as an exercise for the reader.
#
# Use it by putting in lines like:
#
# commentary "Hey! This is commentary!"

init -10:

    python:

        # The style for the commentary window.
        style.create('commentary_window', 'window', 'The commentary window.')

        style.commentary_window.background = Solid((0, 0, 0, 192))
        style.commentary_window.ypos = 0.0
        style.commentary_window.yanchor = 'top'


        # Ensure that the commentary attribute exists.
        if persistent.commentary is None:
            persistent.commentary = False


        commentary = Character(None, window_style='commentary_window',
                               condition = 'persistent.commentary')

    python hide:

        cp = _Preference('Commentary', 'commentary', [
            ('Enabled', True, 'True'),
            ('Disabled', False, 'True')
            ], base=persistent)

        library.preferences['prefs_right'].append(cp)

        
                             
