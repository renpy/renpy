# This file contains a minimal set of style changes needed to have
# Ren'Py work with a game that's 640x480 in size. 

init 1:
    # Change the screen width.
    $ config.screen_width = 640
    $ config.screen_height = 480

    # Font sizes.
    $ style.default.size = 20
    $ style.button_text.size = 20
    $ style.file_picker_text.size = 14

    # Perhaps change the fudge factor on windows, if line spacing
    # looks weird.
    if renpy.windows():
        $ style.default.line_height_fudge = -4

    $ style.file_picker_entry.xminimum = 320
    $ library.thumbnail_width = 60
    $ library.thumbnail_height = 45 
