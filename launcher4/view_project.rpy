screen view_project:
    
    $ p = project.current
    
    frame:
        style_group "l"
        
        has vbox
        
        label _("You're working with \"[p.name!q]\". What you you like to do?") style "l_prompt"
    
        text _("Open a directory:")
        hbox:
            textbutton _("game") style "l_list" size_group "directory" action Return()
            textbutton _("base") style "l_list" size_group "directory" action Return()
            textbutton _("image") style "l_list" size_group "directory" action Return()
        
        use small_spacer
        
        hbox:
            xfill True
            textbutton _("Edit the script.") action Return()
            textbutton _("(open all)") action Return() xalign 1.0 style "l_alternate"
            
        use small_spacer
        
        textbutton _("Check for errors and show statistics. (Lint)") action Return()
        textbutton _("Update translation files.") action Return()
        
        use small_spacer
        
        textbutton _("Clear persistent data.") action Return()

        use small_spacer
        
        textbutton _("Build distributions.") action Return()
            
    $ left_label = "Launch"
    $ left_action = project.Launch()
    $ right_label = "Back"
    $ right_action = Jump("front_page")
    
    use bottom_buttons
    
label view_project:
    call screen view_project
    