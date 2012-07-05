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
                    xmaximum ONEHALF
                    xfill True
                    
                    has vbox

                    # Projects directory selection.
                    add SEPARATOR2
                    
                    frame:
                        style "l_indent"
                        has vbox
                        
                        text _("Projects Directory:")
            
                        add HALF_SPACER
            
                        
                        frame style "l_indent": 
                            if persistent.projects_directory:
                                textbutton _("[persistent.projects_directory!q]") action Jump("projects_directory_preference")
                            else:
                                textbutton _("Not Set") action Jump("projects_directory_preference")
                                
                        
                    add SPACER

                    # Text editor selection.
                    add SEPARATOR2
                    
                    frame:
                        style "l_indent"
                        has vbox
                        
                        text _("Text Editor:")
            
                        add HALF_SPACER
                        
                        frame style "l_indent": 
                            if persistent.editor:
                                textbutton persistent.editor action Jump("editor_preference")
                            else:
                                textbutton _("Not Set") action Jump("editor_preference")
                        
                    add SPACER

                    # Update URL selection.
                    add SEPARATOR2
                    
                    frame:
                        style "l_indent"
                        has vbox
                        
                        text _("Update Channel:")

                        add HALF_SPACER 
                        
                        for source, url in UPDATE_URLS:
                            textbutton source action SetField(persistent, "update_url", url) style "l_list"

                    add SPACER

                    
                frame:
                    style "l_indent"
                    xmaximum ONEHALF
                    xfill True
                    
                    has vbox
                    add SEPARATOR2
                    
                    frame:
                        style "l_indent"
                        has vbox
                        
                        text _("Navigation Options:")
                    
                        add HALF_SPACER
                    
                        textbutton "Include private names" style "l_checkbox" action ToggleField(persistent, "navigate_private")
                        textbutton "Include library names" style "l_checkbox" action ToggleField(persistent, "navigate_library")

                    add SPACER
                    add SEPARATOR2
                    
                    frame:
                        style "l_indent"
                        has vbox
                        
                        text _("Actions:")
                    
                        add HALF_SPACER

                        textbutton _("Open launcher as project") style "l_nonbox" action [ project.Select("launcher"), Jump("front_page") ]


    textbutton _("Back") action Jump("front_page") style "l_left_button"

label projects_directory_preference:
    call choose_projects_directory
    jump preferences


label preferences:
    call screen preferences
    
