# This file contains code that's used to display the editor button,
# and the code that launches the editor with the given filename.

# This file can serve as an example of how to use an overlay, I guess.

init:

    # This lets us control if the editor button is shown or not.
    $ show_editor_button = False

    python hide:

        # This function is called at least one per interaction.
        def overlay():

            # If we don't want to show the editor button, do nothing.
            if not show_editor_button:
                return

            # Figure out the filename and the line number.
            import os.path
            filename, line = renpy.get_filename_line()
            filename = os.path.basename(filename)

            # The function that is called when the button is clicked.
            def clicked():

                # We want to look for the filename in config.gamedir,
                # rather then using the full filename given by
                # get_filename_line. This is because the filename is fixed
                # when the file is compiled, and so may have changed before
                # the script is run. config.gamedir is computed when Ren'Py
                # starts up, and so should always be right.
                fullfn = config.gamedir + "/" + filename

                # If the file exists, then we launch it in the editor, using
                # the undocumented launch_editor function.
                if os.path.exists(fullfn):
                    renpy.launch_editor([ fullfn ], line)

            # Display the button, modifying its look so that it doesn't
            # take up an excessive amount of space.
            ui.button(clicked=clicked,
                      xpos=798, xanchor=1.0, ypos=2, xpadding=6, xminimum=200,
                      background=RoundRect((0, 60, 120, 255), 6),
                      hover_background=RoundRect((0, 80, 160, 255), 6),
                      )

            # The button contains this text. We can't use ui.textbutton,
            # since we want to restyle things.
            ui.text("%s:%d" % (filename, line),
                    style="button_text",
                    size=14)

        # Append the overlay function to the list of overlay functions.
        config.overlay_functions.append(overlay)
