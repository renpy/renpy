screen front_page:
    
    frame:
        style_group "l"
        
        has vbox
        
        label _("Welcome back to Ren'Py 6.14. What would you like to do?") style "l_prompt"

        text _("Open an existing project:")

        hbox:
            box_wrap True
            for p in projects:
                textbutton "[p.name!q]" style "l_list" action project.Select(p, "view_project") size_group "project"
        
        use small_spacer
        
        textbutton _("Create a new project.") action Return(True)
        
        use small_spacer
        
        hbox:
            xfill True
            textbutton _("Launch Ren'Py tutorial.") action Return()
            textbutton _("(open project)"): 
                action project.Select("tutorial") 
                xalign 1.0 
                style "l_alternate"

        hbox:
            xfill True
            textbutton _("Launch \"The Question.\"") action Return()
            textbutton _("(open project)"): 
                action project.Select("the_question")
                xalign 1.0 
                style "l_alternate"
        
        use small_spacer    
            
        hbox:
            xfill True
            textbutton "View documentation." action Return(True)
            textbutton _(" (web version)") action Return() xalign 1.0 style "l_alternate"
        
        textbutton _("Visit the web site.") action Return()
        textbutton _("Visit the games list.") action Return()
        
        use small_spacer
        
        textbutton _("Check for Ren'Py updates.") action Return(True)
        textbutton _("Configure launcher settings.") action Return(True)

        use small_spacer
        
        textbutton _("Quit") action Quit(confirm=False)
        
        
label main_menu:
    return
    
label start:
label front_page:
        
    call screen front_page(projects=project.manager.projects)
    
    