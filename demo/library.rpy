# This file consists of renpy functions that aren't expected to be
# touched by the user too much. We reserve the _ prefix for names
# defined in the library.

# It's strongly reccomended that you don't edit this file, as future
# releases of Ren'Py will probably change this file to include more
# functionality.

# It's also strongly recommended that you leave this file in the
# game directory, so its functionality is included in your game.

label _enable_overlay:
    
    # Set up the default keymap.    
    python hide:
        config.underlay = [ ]
        config.overlay = [ ]

        # The default keymap.
        km = renpy.Keymap(
            K_PAGEUP = renpy.rollback,
            f = renpy.toggle_fullscreen,
            s = renpy.screenshot,
            )

        config.underlay.append(km)


    # If the user gives an enable_overlay function, call that.
    if renpy.has_label('enable_overlay'):
        call enable_overlay

    return
        
        
        
    

# This is the true starting point of the program. Sssh... Don't
# tell anyone.
label _start:
    
    call _enable_overlay
    jump start
