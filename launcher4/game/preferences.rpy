define foo = 1

screen preferences:
    
    frame:
        style_group "l"
        style "l_root"
        
        window:
    
            has vbox

            label _("Launcher Preferences")
            
            add HALF_SPACER

            
            hbox:
                frame:
                    style "l_indent"
                    xmaximum 496
                    xfill True
                    
                    has vbox
                                        
                    # Projects directory selection.
                    add SEPARATOR2
                    
                    frame:
                        style "l_indent"
                        has vbox
                        
                        text _("Projects Directory:")
                        
                    add SPACER

                    # Update URL selection.

                    add SEPARATOR2
                    
                    frame:
                        style "l_indent"
                        has vbox
                        
                        text _("Update URL:")
                        
                    add SPACER

                    # Navigation Options.

                    add SEPARATOR2
                    
                    frame:
                        style "l_indent"
                        has vbox
                        
                        text _("Navigation Options:")
                    
                        add HALF_SPACER
                    
                        textbutton "Include private names." style "l_checkbox" action ToggleField(persistent, "navigate_private")
                        textbutton "Include library names." style "l_checkbox" action ToggleField(persistent, "navigate_library")
                        
                        add HALF_SPACER
                        
                        textbutton "Open launcher project." style "l_nonbox" action project.Select("launcher4")
                    
                    
                    

                    
                frame:
                    style "l_indent"
                    xmaximum 258
                    xfill True

                    has vbox

                    add SEPARATOR2
                    
                    frame:
                        style "l_indent"                        
                        has vbox
                        
                        text _("Text Editor:")
                    
                        add HALF_SPACER
                        
                        viewport:
                            scrollbars "vertical"
                            mousewheel True
                            
                            has vbox
                            
                            for name, action in editor.editor_action_list():
                                textbutton "[name!q]":
                                    action action
                                    style "l_list"


#            frame style "l_indent":
 
#                has vbox
 
#                textbutton _("Show symbols defined in common/") style "l_checkbox" action SetVariable("foo", 1)
#                textbutton _("Show hidden symbols.") style "l_checkbox" action SetVariable("foo", 2)
                
    textbutton _("Back") action Jump("front_page") style "l_left_button"

label preferences:
    call screen preferences