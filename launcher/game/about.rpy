# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

screen about:
    
    $ version = renpy.version()
    
    frame:
        style_group "l"
        style "l_root"
        
        window:
            xfill True
            
            has vbox xfill True

            add "logo.png" xalign 0.5 yoffset -5

            null height 15
            
            text _("[version!q]") xalign 0.5 bold True
            
            null height 20

            textbutton _("View license") action interface.OpenLicense() xalign 0.5
            
    textbutton _("Back") action Jump("front_page") style "l_left_button"

label about:
    call screen about
    
